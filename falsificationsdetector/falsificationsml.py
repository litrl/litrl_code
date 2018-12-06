'''
    Copyright Victoria L. Rubin 2017-2018.

    This file is part of Litrl Browser.

    Litrl Browser is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Litrl Browser is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Litrl Browser.  If not, see <https://www.gnu.org/licenses/>.
'''

#-------------------------------------------------------------------------------
# Name:        falsificationsml.py
# Purpose:     detect falsifications in text
#              Warning: This code contains a lot of REALLY offensive + bad words!
#                       These words may be more likely to occur in falsified content.
#
# Created:     01/2018
#
# Language and Information Technology Research Lab
# Faculty of Information and Media Studies (FIMS)
# University of Western Ontario, London, Canada
#-------------------------------------------------------------------------------

import codecs
import numpy as np
import warnings
from numpy import array
from sklearn import svm
from sklearn.model_selection import train_test_split
from pattern.en import tag
from pattern.en import parsetree
from pattern.en import parse
from pattern.en import tokenize
from pattern.en import tree
from pattern.en.wordlist import PROFANITY
from pattern.en.wordlist import TIME

import nltk, re, pprint
from nltk import word_tokenize, ne_chunk, pos_tag
from nltk import sent_tokenize
from nltk import FreqDist
from nltk.tree import Tree
#from statistics import mean
from pattern.en import sentiment

#fix me
slangARRAY=[]
generalizingARRAY=[]
negativeARRAY=[]
positiveARRAY=[]

uncertainwordsARRAY=[]
forwardRef=[]

class falsificationDetector:

    def __init__(self):
        self.AMT_STORIES_FAKE = 138
        self.AMT_STORIES_LEGIT = 138
        self.PATH_LEGIT = './Legit/story_'
        self.PATH_FAKE = './Fake/storyf_'
        self.TRAIN_SIZE = 0.8
        self.loadSwearing()

    def train(self):
        print "Training Falsifications Detector..."
        legitScores = []
        falseScores = []

        avgLegitScores = []
        avgFalseScores = []

        for x in xrange(1, self.AMT_STORIES_LEGIT):
            lineLIST = self.getParagraphs(self.PATH_LEGIT, x)
            legitScore = self.getScores(lineLIST)

            #set up our list of features averages based on the size of our first sample
            if len(avgLegitScores) == 0:
                for c in xrange(len(legitScore)):
                    avgLegitScores.append(0)

            #sum everything to get an average later
            for x in xrange(len(legitScore)):
                avgLegitScores[x] = float(avgLegitScores[x]) + float(legitScore[x])

            legitScores.append(legitScore)
        for x in xrange(1, self.AMT_STORIES_FAKE):
            lineLIST = self.getParagraphs(self.PATH_FAKE, x)
            falseScore = self.getScores(lineLIST)

            #set up our list of features averages based on the size of our first sample
            if len(avgFalseScores) == 0:
                for c in xrange(len(falseScore)):
                    avgFalseScores.append(0)

            #sum everything to get an average later
            for x in xrange(len(falseScore)):
                avgFalseScores[x] = float(avgFalseScores[x]) + float(falseScore[x])

            falseScores.append(falseScore)

        #divide to get avgs
        for x in xrange(len(avgFalseScores)):
            avgFalseScores[x] = avgFalseScores[x] / float(len(avgFalseScores))
        for x in xrange(len(avgLegitScores)):
            avgLegitScores[x] = avgLegitScores[x] / float(len(avgLegitScores))

        print "AVG Legit Scores"
        print avgLegitScores

        print "AVG False Scores"
        print avgFalseScores

        legitTrain, legitTest = train_test_split(legitScores, train_size = self.TRAIN_SIZE)
        falseTrain, falseTest = train_test_split(falseScores, train_size = self.TRAIN_SIZE)

        Xtrain = []
        Ytrain = []

        Xtrain = legitTrain + falseTrain
        for x in xrange(len(legitTrain)):
            Ytrain.append(0)
        for x in xrange(len(falseTrain)):
            Ytrain.append(1)

        Xtest = []
        Ytest = []

        Xtest = legitTest + falseTest
        for x in xrange(len(legitTest)):
            Ytest.append(0)
        for x in xrange(len(falseTest)):
            Ytest.append(1)

        # Perform classification with SVM, kernel=linear
        self.classifier_linear = svm.SVC(kernel='linear', probability = True)
        self.classifier_linear.fit(Xtrain, Ytrain)

        test_pred = self.classifier_linear.predict(Xtest)

        #store the predictions
        npYtest = np.array(Ytest)
        classifierScoreSVM = "Test set score: {:.2f}".format(np.mean(test_pred == npYtest))

        print "Train set Legit Stories Amount: ", str(len(legitTrain))
        print "Train set False Stories Amount: ", str(len(falseTrain))

        print "Test set Legit Stories Amount: ", str(len(legitTest))
        print "Test set False Stories Amount: ", str(len(falseTest))

        print classifierScoreSVM

    def predict(self, text):
        lineLIST = text.split(".")

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            features = self.getScores(lineLIST)
            prediction_linear = self.classifier_linear.predict(features)
            prediction_scores = self.classifier_linear.predict_proba(features)

        betterString = str(prediction_scores[0])[1:-1]
        classValues = betterString.split(" ")
        classValues = filter(None, classValues) # fastest
        return ",".join(classValues) + "," + ",".join(str(featScore) for featScore in features)

    def getScores(self, lineLIST):
        f1 = self.getNoOfParagraphsPerNewsStory(lineLIST)
        f2 = self.getAVGWordLength(lineLIST)     #NOTE: definitely a bug in this function, results are too low
        f3 = self.getAVGNoOfSentencesPerParagraph(lineLIST)
        f4 = self.getAVGNoOfWordsPerSentence(lineLIST)
        f5 = self.getAVGNoOfWordsPerParagraph(lineLIST)
        f6 = self.getPausality(lineLIST)
        f7 = 0 #self.getVerifiableFACTSperSENTENCE(lineLIST) #too slow or infinite loop, disabled
        f8 = self.getEMOTIVENESS(lineLIST)
        f9 = self.getPRONOUNcountperSENTENCE(lineLIST)
        f10 = self.getINFORMALITY(lineLIST)
        f11 = self.getLEXICALdiversity(lineLIST)
        f12 = self.getAFFECT(lineLIST)
        scores = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12]
        return scores

    def getParagraphs(self, filePath, storyNum):
        lineLIST = list()
        fileextension = '.txt'
        fullPath = filePath + str(storyNum) + fileextension
        with codecs.open(fullPath,"rU", encoding="utf-8", errors='ignore') as f:
			for line in f:
				line1 = line.encode('utf-8', errors='ignore')
				line2 = line1.decode('utf-8').strip()
				lineLIST.append(line2)

        return lineLIST

    def getSentences(self, lineLIST):
		ALLsentences=list()
		everyLINE=0
		paragraphcount=0
		sentencecount=0
		Sentences1=[]
		wordCount=0
		for everyPARAGRAPH in lineLIST:
			Sentences1=sent_tokenize(lineLIST[everyLINE])
			ALLsentences.append(Sentences1)
			everyLINE=everyLINE+1
		return ALLsentences

    def getAVGNoOfWordsPerParagraph(self, lineLIST):
		everyLINE=0
		paragraphcount=0
		sentencecount=0
		Sentences1=[]
		wordCount=0
		for everyPARAGRAPH in lineLIST:
			Sentences1=sent_tokenize(lineLIST[everyLINE])
			newsentencecount=len(Sentences1)
			everyLINE=everyLINE+1
			count1=0
			for everysentence in Sentences1:
				if count1<len(Sentences1)and len(Sentences1)>0:
					newSentences1=word_tokenize(Sentences1[count1])
					wordCount=len(newSentences1)+wordCount
					sentencecount=sentencecount+newsentencecount
					count1=count1+1
		paragraphcount=len(lineLIST)
		AVGwordsperParagraph=float(wordCount)/paragraphcount
		return AVGwordsperParagraph

    def getAVGNoOfWordsPerSentence(self, lineLIST):
		everyLINE=0
		paragraphcount=0
		sentencecount=0
		Sentences1=[]
		wordCount=0
		for everyPARAGRAPH in lineLIST:
			Sentences1=sent_tokenize(lineLIST[everyLINE])
			newsentencecount=len(Sentences1)
			everyLINE=everyLINE+1
			count1=0
			for everysentence in Sentences1:
				if count1<len(Sentences1)and len(Sentences1)>0:
					newSentences1=word_tokenize(Sentences1[count1])
					wordCount=len(newSentences1)+wordCount
					sentencecount=sentencecount+newsentencecount
					count1=count1+1
		paragraphcount=len(lineLIST)
		AVGwordsperSentence=float(wordCount)/sentencecount
		return AVGwordsperSentence

    def getAVGNoOfSentencesPerParagraph(self, lineLIST):
		everyLINE=0
		paragraphcount=0
		sentencecount=0
		Sentences1=[]
		wordCount=0
		for everyPARAGRAPH in lineLIST:
			Sentences1=sent_tokenize(lineLIST[everyLINE])
			newsentencecount=len(Sentences1)
			everyLINE=everyLINE+1
			count1=0
			for everysentence in Sentences1:
				if count1<len(Sentences1)and len(Sentences1)>0:
					newSentences1=word_tokenize(Sentences1[count1])
					wordCount=len(newSentences1)+wordCount
					sentencecount=sentencecount+newsentencecount
					count1=count1+1
		paragraphcount=len(lineLIST)
		AVGsentenceperParagraph=float(sentencecount)/paragraphcount
		return AVGsentenceperParagraph

    def getNoOfParagraphsPerNewsStory(self, lineLIST):
		paragraphcount=len(lineLIST)
		return paragraphcount

    def getAVGWordLength(self, lineLIST):
        wordLength=list()
        everyLINE=0
        paragraphcount=0
        sentencecount=0
        Sentences1=[]
        wordCount=0
        for everyPARAGRAPH in lineLIST:
        	Sentences1=sent_tokenize(lineLIST[everyLINE])
        	newsentencecount=len(Sentences1)
        	everyLINE=everyLINE+1
        	count1=0
        	for everysentence in Sentences1:
        		if count1<len(Sentences1)and len(Sentences1)>0:
        			newSentences1=word_tokenize(Sentences1[count1])
        			count1=count1+1
        			for word in newSentences1:
        				lenOfWord=len(word)
                        wordLength.append(lenOfWord)
        sumWordLengths = sum(wordLength)
        return float(sumWordLengths) / float(len(wordLength))

    def getLEXICALdiversity(self, lineLIST):
		everyLINE=0
		paragraphcount=0
		sentencecount=0
		Sentences1=[]
		wordLIST=list()
		setwordLIST=list()
		wordCount=0
		for everyPARAGRAPH in lineLIST:
			Sentences1=sent_tokenize(lineLIST[everyLINE])
			newsentencecount=len(Sentences1)
			everyLINE=everyLINE+1
			count1=0
			for everysentence in Sentences1:
				if count1<len(Sentences1)and len(Sentences1)>0:
					newSentences1=word_tokenize(Sentences1[count1])
					count1=count1+1
					c=0
					for everyword in newSentences1:
						lowercaseCHAR=newSentences1[c].lower()
						wordLIST.append(lowercaseCHAR)
						c=c+1
		setwordLIST=set(wordLIST)
		allTOKENS=float(len(wordLIST))
		setTOKENS=float(len(setwordLIST))
		LexicalDIVERSITY=float(allTOKENS/setTOKENS)
		return LexicalDIVERSITY

    def getPausality(self, lineLIST):
		wordLIST=list()
		everyLINE=0
		paragraphcount=0
		sentencecount=0
		Sentences1=[]
		wordCount=0
		for everyPARAGRAPH in lineLIST:
			Sentences1=sent_tokenize(lineLIST[everyLINE])
			newsentencecount=len(Sentences1)
			sentencecount=sentencecount+newsentencecount
			count1=0
			for everysentence in Sentences1:
				if count1<len(Sentences1)and len(Sentences1)>0:
					newSentences1=word_tokenize(Sentences1[count1])
					count1=count1+1
					c=0
					for everyword in newSentences1:
						lowercaseCHAR=newSentences1[c].lower()
						wordLIST.append(lowercaseCHAR)
						c=c+1
			everyLINE=everyLINE+1
		POS_text =nltk.pos_tag(wordLIST)
		tagged = nltk.FreqDist(tag for (word, tag) in POS_text)
		full_stop=tagged.get('.', None)
		if full_stop==None:
			full_stop=0
		comma=tagged.get(',', None)
		if comma==None:
			comma=0
		question_mark=tagged.get('?', None)
		if question_mark==None:
			question_mark=0
		inverted_comma=tagged.get('\'', None)
		if inverted_comma==None:
			inverted_comma=0
		colon=tagged.get(':', None)
		if colon==None:
			colon=0
		semi_colon=tagged.get(';', None)
		if semi_colon==None:
			semi_colon=0
		quotation_mark=tagged.get('"', None)
		if quotation_mark==None:
			quotation_mark=0
		exclamation_mark=tagged.get('!', None)
		if exclamation_mark==None:
			exclamation_mark=0
		at_mark=tagged.get('@', None)
		if at_mark==None:
			at_mark=0
		ash_mark=tagged.get('#', None)
		if ash_mark==None:
			ash_mark=0
		dollar_mark=tagged.get('$', None)
		if dollar_mark==None:
			dollar_mark=0
		percentage_mark=tagged.get('%', None)
		if percentage_mark==None:
			percentage_mark=0
		and_mark=tagged.get('&', None)
		if and_mark==None:
			and_mark=0
		Punctuations=float(full_stop+comma+question_mark+inverted_comma+colon+semi_colon+quotation_mark+exclamation_mark+at_mark+ash_mark+dollar_mark+percentage_mark+and_mark)
		Pausality=float(Punctuations/sentencecount)
		return Pausality

    def getVerifiableFACTSperSENTENCE(self, lineLIST):
        wordLIST=list()
        named_entities=list()
        continuous_chunk = []
        everyLINE=0
        paragraphcount=0
        sentencecount=0
        Sentences1=[]
        timeCOUNTER=0
        wordCount=0
        for everyPARAGRAPH in lineLIST:
            Sentences1=sent_tokenize(lineLIST[everyLINE].encode('ascii', errors='ignore'))
            newsentencecount=len(Sentences1)
            sentencecount=sentencecount+newsentencecount
            count1=0
            for everysentence in Sentences1:
                if count1<len(Sentences1)and len(Sentences1)>0:
                    newSentences1=word_tokenize(Sentences1[count1])
                    count1=count1+1
                    c=0
                    for everyword in newSentences1:
                        lowercaseCHAR=newSentences1[c].lower()
                        wordLIST.append(lowercaseCHAR)
                        c=c+1
                        if lowercaseCHAR in TIME:
                            timeCOUNTER=timeCOUNTER+1
                    chunked = ne_chunk(pos_tag(everysentence))
                    prev = None
                    current_chunk = []
                    for i in chunked:
						if type(i) == Tree:
							current_chunk.append(" ".join([token for token, pos in i.leaves()]))
						elif current_chunk:
							named_entity = " ".join(current_chunk)
							continuous_chunk.append(named_entity)
							current_chunk = []
						else:
							continue
                    parse_tree = nltk.ne_chunk(nltk.tag.pos_tag(everysentence.split()), binary=True)
                    for t in parse_tree.subtrees():
						if t.label() == 'NE':
							named_entities.append(t)
                    count1=count1+1
            everyLINE=everyLINE+1
        noofnamed_ENTITY=len(named_entities)
        verifableFACTS=float(timeCOUNTER+noofnamed_ENTITY)
        verifableFACTSperSENTENCE=float(verifableFACTS/sentencecount)
        return verifableFACTSperSENTENCE

    def getEMOTIVENESS(self, lineLIST):
		wordLIST=list()
		everyLINE=0
		paragraphcount=0
		sentencecount=0
		Sentences1=[]
		wordCount=0
		for everyPARAGRAPH in lineLIST:
			Sentences1=sent_tokenize(lineLIST[everyLINE])
			newsentencecount=len(Sentences1)
			sentencecount=sentencecount+newsentencecount
			count1=0
			for everysentence in Sentences1:
				if count1<len(Sentences1)and len(Sentences1)>0:
					newSentences1=word_tokenize(Sentences1[count1])
					count1=count1+1
					c=0
					for everyword in newSentences1:
						lowercaseCHAR=newSentences1[c].lower()
						wordLIST.append(lowercaseCHAR)
						c=c+1
			everyLINE=everyLINE+1
		POS_text =nltk.pos_tag(wordLIST)
		tagged = nltk.FreqDist(tag for (word, tag) in POS_text)
		Noun = tagged.get('NN', None)
		if Noun ==None:
			Noun=0
		Proper_Noun=tagged.get('NNP', None)
		if Proper_Noun ==None:
			Proper_Noun=0
		Plural_Noun=tagged.get('NNS', None)
		if Plural_Noun==None:
			Plural_Noun=0
		Plural_Proper_Noun=tagged.get('NNPS', None)
		if Plural_Proper_Noun==None:
			Plural_Proper_Noun=0
		Adj=tagged.get('JJ', None)
		if Adj==None:
			Adj=0
		Comp_Adj=tagged.get('JJR', None)
		if Comp_Adj==None:
			Comp_Adj=0
		Super_Adj=tagged.get('JJS', None)
		if Super_Adj==None:
			Super_Adj=0
		Personal_Pronoun=tagged.get('PRP', None)
		if Personal_Pronoun==None:
			Personal_Pronoun=0
		Possessive_Pronoun=tagged.get('PRP$', None)
		if Possessive_Pronoun==None:
			Possessive_Pronoun=0
		Wh_Pronoun=tagged.get('WP', None)
		if Wh_Pronoun==None:
			Wh_Pronoun=0
		Possesive_wh_Pronoun=tagged.get('WP$', None)
		if Possesive_wh_Pronoun==None:
			Possesive_wh_Pronoun=0
		Adverb=tagged.get('RB', None)
		if Adverb==None:
			Adverb=0
		Comp_Adverb=tagged.get('RBR', None)
		if Comp_Adverb==None:
			Comp_Adverb=0
		Super_Adverb=tagged.get('RBS', None)
		if Super_Adverb==None:
			Super_Adverb=0
		Wh_Adverb=tagged.get('WRB', None)
		if Wh_Adverb==None:
			Wh_Adverb=0
		Verb=tagged.get('VB', None)
		if Verb==None:
			Verb=0
		Past_Verb=tagged.get('VBD', None)
		if Past_Verb==None:
			Past_Verb=0
		Gerund_Verb=tagged.get('VBG', None)
		if Gerund_Verb==None:
			Gerund_Verb=0
		Past_Participle_Verb=tagged.get('VBN', None)
		if Past_Participle_Verb==None:
			Past_Participle_Verb=0
		Non3rd_Verb=tagged.get('VBP', None)
		if Non3rd_Verb==None:
			Non3rd_Verb=0
		thirdPerson_Verb=tagged.get('VPZ', None)
		if thirdPerson_Verb==None:
			thirdPerson_Verb=0
		Emotiveness_denominator=float(Plural_Proper_Noun+Plural_Noun+Proper_Noun+Noun+Verb+Past_Verb+Gerund_Verb+Past_Participle_Verb+Non3rd_Verb+thirdPerson_Verb)
		Modifiers=float(Adj+Comp_Adj+Super_Adj+Adverb+Comp_Adverb+Super_Adverb+Wh_Adverb)
		Emotiveness=float(Modifiers/Emotiveness_denominator)
		return Emotiveness

    def loadSwearing(self):
        self.swears = set()
        fk = open('swearing.txt', 'r')
        swears = fk.readlines()
        for x in xrange(len(swears)):
            self.swears.add(unicode(swears[x].rstrip().lower(), "utf-8"))
        print "Swear/emotive word count: ", len(self.swears)

    def isSwear(self, CHAR):
        if CHAR.lower() in self.swears:
            return True
        else:
            return False

    def getINFORMALITY(self, lineLIST):
		wordLIST=list()
		swearwordCOUNTER=0
		slangCOUNTER=0
		everyLINE=0
		paragraphcount=0
		sentencecount=0
		Sentences1=[]
		wordCount=0
		for everyPARAGRAPH in lineLIST:
			Sentences1=sent_tokenize(lineLIST[everyLINE])
			newsentencecount=len(Sentences1)
			sentencecount=sentencecount+newsentencecount
			count1=0
			for everysentence in Sentences1:
				if count1<len(Sentences1)and len(Sentences1)>0:
					newSentences1=word_tokenize(Sentences1[count1])
					count1=count1+1
					c=0
					for everyword in newSentences1:
						lowercaseCHAR=newSentences1[c].lower()
						wordLIST.append(lowercaseCHAR)
						c=c+1
						if lowercaseCHAR in slangARRAY:
						   slangCOUNTER=slangCOUNTER+1
						if self.isSwear(lowercaseCHAR):
						   swearwordCOUNTER=swearwordCOUNTER+1
			everyLINE=everyLINE+1
		totalINFORMAL=float(swearwordCOUNTER+slangCOUNTER)
		informality=float(totalINFORMAL/sentencecount)
		return informality

    def getAFFECT(self, lineLIST):
		wordLIST=list()
		positiveCOUNTER=0
		negativeCOUNTER=0
		everyLINE=0
		sentencecount=0
		Sentences1=[]
		for everyPARAGRAPH in lineLIST:
			Sentences1=sent_tokenize(lineLIST[everyLINE])
			newsentencecount=len(Sentences1)
			sentencecount=sentencecount+newsentencecount
			count1=0
			for everysentence in Sentences1:
				if count1<len(Sentences1)and len(Sentences1)>0:
					newSentences1=word_tokenize(Sentences1[count1])
					count1=count1+1
					c=0
					for everyword in newSentences1:
						lowercaseCHAR=newSentences1[c].lower()
						wordLIST.append(lowercaseCHAR)
						c=c+1
						if lowercaseCHAR in positiveARRAY:
						   positiveCOUNTER=positiveCOUNTER+1
						if lowercaseCHAR in negativeARRAY:
						   negativeCOUNTER=negativeCOUNTER+1
		totalAFFECT=float(negativeCOUNTER+positiveCOUNTER)
		Affect=float(totalAFFECT/sentencecount)
		return Affect

    def getPRONOUNcountperSENTENCE(self, lineLIST):
		wordLIST=list()
		everyLINE=0
		paragraphcount=0
		sentencecount=0
		Sentences1=[]
		wordCount=0
		for everyPARAGRAPH in lineLIST:
			Sentences1=sent_tokenize(lineLIST[everyLINE])
			newsentencecount=len(Sentences1)
			sentencecount=sentencecount+newsentencecount
			count1=0
			for everysentence in Sentences1:
				if count1<len(Sentences1)and len(Sentences1)>0:
					newSentences1=word_tokenize(Sentences1[count1])
					count1=count1+1
					c=0
					for everyword in newSentences1:
						lowercaseCHAR=newSentences1[c].lower()
						wordLIST.append(lowercaseCHAR)
						c=c+1
			everyLINE=everyLINE+1
		POS_text =nltk.pos_tag(wordLIST)
		tagged = nltk.FreqDist(tag for (word, tag) in POS_text)
		Personal_Pronoun=tagged.get('PRP', None)
		if Personal_Pronoun==None:
			Personal_Pronoun=0
		Possessive_Pronoun=tagged.get('PRP$', None)
		if Possessive_Pronoun==None:
			Possessive_Pronoun=0
		Wh_Pronoun=tagged.get('WP', None)
		if Wh_Pronoun==None:
			Wh_Pronoun=0
		Possesive_wh_Pronoun=tagged.get('WP$', None)
		if Possesive_wh_Pronoun==None:
			Possesive_wh_Pronoun=0
		Pronoun_Count=float(Possessive_Pronoun+Personal_Pronoun+Possesive_wh_Pronoun+Wh_Pronoun)
		Pronoun_CountperSENTENCE=float(Pronoun_Count/sentencecount)
		return Pronoun_CountperSENTENCE
