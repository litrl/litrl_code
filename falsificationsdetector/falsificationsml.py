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
# Name:        falsificationml.py
# Purpose:     detect falsifications
#
# Created:     December 2018
#              This work is a combination of the original falsification detector
#              and the Falsification detector to attempt to improve accuracy.
#
# Language and Information Technology Research Lab
# Faculty of Information and Media Studies (FIMS)
# University of Western Ontario, London, Canada
#-------------------------------------------------------------------------------

import codecs
import warnings
import operator
import nltk
import math
import numpy as np
import sys
import csv
import json
import pandas as pd
import os
from io import BytesIO
from nltk import ne_chunk, pos_tag, word_tokenize, sent_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tree import Tree
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from numpy import array
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from nltk import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import KFold
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn import metrics
from pattern.en import ngrams, modality, mood, sentiment, number, wordnet
from pattern.vector import Document, Model
from os.path import isfile, join

from pattern.en import tag
from pattern.en import parsetree
from pattern.en import parse
from pattern.en import tokenize
from pattern.en import tree
from pattern.en import positive
from pattern.en.wordlist import PROFANITY
from pattern.en.wordlist import TIME

from nltk import ne_chunk, pos_tag, re, pprint, FreqDist
from pattern.en import sentiment

slangARRAY = ['OMG', 'LOL', 'Whoah', 'Wow', 'Whoa', 'Epic', 'aha', 'alas', 'woops', 'oops', 'jeez', 'uggh', 'gosh', 'hmmm', 'hmm', 'ha', 'haa', 'bravo']
generalizingARRAY = ['all', 'everyone', 'everywhere', 'everybody', 'everything', 'nobody', 'none', 'most', 'many', 'lot', 'always', 'entire', 'entirely', 'complete', 'completely', 'absolute', 'absolutely', 'total', 'totally', 'whole', 'wholly', 'utter', 'utterly', 'someone', 'somebody', 'somewhere', 'anyone', 'anywhere']
uncertainwordsARRAY = ['maybe', 'perhaps', 'peradventure', 'possibly', 'probably', 'perchance']
forwardRef = ['this', 'that', 'these', 'those', 'yon', 'yonder', 'she', 'her', 'he', 'him', 'it', 'I', 'me', 'you', 'we', 'us', 'they', 'them', 'my', 'hers', 'his', 'your', 'its', 'their', 'our']

class falsificationDetector:

    def __init__(self):
        self.AMT_STORIES_FAKE = 138
        self.AMT_STORIES_LEGIT = 138
        print "Total Falsification stories (legit):  ", self.AMT_STORIES_LEGIT
        print "Total Falsification stories (fake): ", self.AMT_STORIES_FAKE
        print "Total Falsification stories: ", self.AMT_STORIES_FAKE + self.AMT_STORIES_LEGIT
        self.PATH_LEGIT = './Legit/story_'
        self.PATH_FAKE = './Fake/storyf_'
        self.loadSwearing()

    def v(self, verbose, text):
        if verbose:
            print "Verbose Output: ", text

    ######################## named entities  #########################

    def keywithmaxval(self, A):
         newA = dict(sorted(A.iteritems(), key=operator.itemgetter(1), reverse=True)[:3])
         return newA

    def get_continuous_chunks(self, s):
      #FIND A LIST OF NAMED ENTITES IN A STORY, INCLUDING LEAF NODES IN THE CASE OF TREES
      continuous_chunk = []
      chunked = ne_chunk(pos_tag(word_tokenize(s)))
      prev = None
      current_chunk = []
      for i in chunked:
         if type(i) == Tree:
              current_chunk.append(" ".join([token for token, pos in i.leaves()]))
         elif current_chunk:
              named_entity = " ".join(current_chunk)
              if named_entity not in continuous_chunk:
                 continuous_chunk.append(named_entity)
                 current_chunk = []
         else:
              continue
      return continuous_chunk

    #f - feature
    #f1: PRP + PRP$ (check)
    def getPronouns(self, partsOfSpeech, wordCount):
        count = 0
        for pos in partsOfSpeech:
            if u"PRP" in pos:
                count = count + 1
        return (float(count) / float(wordCount)) * 100

    #f2
    #PRP
    def getPersonalPronouns(self, partsOfSpeech, wordCount):
        count = 0
        for pos in partsOfSpeech:
            if u"PRP" == pos:
                count = count + 1
        return (float(count) / float(wordCount)) * 100

    #f3: PRP$ (pronouns, possessive. check)
    def getPossessivePronouns(self, partsOfSpeech, wordCount):
        count = 0
        for pos in partsOfSpeech:
            if u"PRP$" == pos:
                count = count + 1
        return (float(count) / float(wordCount)) * 100

    #f4: PP (prepositional phrase? check)
    def getPrepositionalPhrases(self, chunksOfSpeech, wordCount):
        count = 0
        for chunk in chunksOfSpeech:
            if u"PP" == chunk.type:
                count = count + 1
        return (float(count) / float(wordCount)) * 100

    #f5: VP
    def getVerbPhrases(self, chunksOfSpeech, wordCount):
        count = 0
        for chunk in chunksOfSpeech:
            if u"VP" == chunk.type:
                count = count + 1
        return (float(count) / float(wordCount)) * 100

    #f6: CC, IN
    def getConjunctions(self, partsOfSpeech, wordCount):
        count = 0
        for pos in partsOfSpeech:
            if u"CC" == pos:
                count = count + 1
            elif u"IN" == pos:
                count = count + 1
        return (float(count) / float(wordCount)) * 100

    #f7: ADVP
    def getAdverbPhrases(self, chunksOfSpeech, wordCount):
        count = 0
        for chunk in chunksOfSpeech:
            if u"ADVP" == chunk.type:
                count = count + 1
        return (float(count) / float(wordCount)) * 100

    #f8: ADJP
    def getAdjectivePhrases(self, chunksOfSpeech, wordCount):
        count = 0
        for chunk in chunksOfSpeech:
            if u"ADJP" == chunk.type:
                count = count + 1
        return (float(count) / float(wordCount)) * 100

    #f9: no equal for periods. write.
    def getPeriods(self, sentence):
        count = sentence.string.count(u".")
        return count

    #f10: ,
    def getCommas(self, sentence):
        count = sentence.string.count(u",")
        return count

    #f11:
    def getColon(self, sentence):
        count = sentence.string.count(u":")
        return count

    #f12: no equal for semicolon. write.
    def getSemicolon(self, sentence):
        count = sentence.string.count(u";")
        return count

    #f13: percent of sentences ending with a "?"
    def getQuestionMarks(self, sentence):
        count = sentence.string.count(u"?")
        return count

    #f14: no equal exclamations. write.
    def getExclamationMarks(self, sentence):
        count = sentence.string.count(u"!")
        return count

	#falsification add-ons
    def getText(self, filePath, storyNum):
        text = ""
        fileextension = '.txt'
        fullPath = filePath + str(storyNum) + fileextension
        with codecs.open(fullPath,"rU", encoding="utf-8", errors='ignore') as f:
			for line in f:
				line1 = line.encode('utf-8', errors='ignore')
				line2 = line1.decode('utf-8')
				text = text + line2
        return text

    def getParagraphs(self, story):
        lineLIST = story.splitlines()
        return lineLIST

	#f15
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

	#f16
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

	#f17
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

	#f18
    def getNoOfParagraphsPerNewsStory(self, lineLIST):
		paragraphcount=len(lineLIST)
		return paragraphcount

	#f19
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

	#f20
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

	#f21
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

	#f22
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

	#f23
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

	#f24
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
						if positive(lowercaseCHAR, threshold=0.5):
						   positiveCOUNTER=positiveCOUNTER+1
						else:
						   negativeCOUNTER=negativeCOUNTER+1
		totalAFFECT=float(negativeCOUNTER+positiveCOUNTER)
		Affect=float(totalAFFECT/sentencecount)
		return Affect

	#f25
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

    def getPercentage(self, count, divisor):
        return (float(count) / divisor) * 100

    def getAbsurdityScore(self, test_data):
        # COMPUTE ABSURDITY SCORE
        # FOR EVERY STORY, TOKENIZE THE STORY, GET A LIST OF THE NAMED ENTIES IN THE STORY ASIDE FROM LAST SENTENCE.
        # GET A LIST OF NAMED ENTITIES IN LAST SENTENCE. IF THERE IS NO OVERALAP THE RETURN 1  x
        absflag = 0
        sents = sent_tokenize(test_data.encode('ascii', 'ignore'))
        all = []
        for s in sents[0:-1]:
            ents = self.get_continuous_chunks(s)# get all the entities in all the story except the last sentence
            all.append(" ".join([t for t in ents]))
        if len(sents) > 0:
            last_ents = self.get_continuous_chunks(sents[-1])# get entities in the last sentence
            if last_ents:
              for l in last_ents:
                if l in all: #if an entity from the last is found in the rest then not absurd
                  absflag= 0
                else:
                  absflag=1
                  break;
            else:
                  absflag =0
        else:
            absflag = 0
        return absflag

    def trainTestSplit(self, train_percent=0.8):
        self.Falsification = []
        self.not_Falsification = []

		#append stories to correct lists
        for x in xrange(1, self.AMT_STORIES_FAKE):
            text = self.getText(self.PATH_FAKE, x)
            self.Falsification.append(text)
        for x in xrange(1, self.AMT_STORIES_LEGIT):
            text = self.getText(self.PATH_LEGIT, x)
            self.not_Falsification.append(text)

        self.notFalsificationTrain, self.notFalsificationTest = train_test_split(self.not_Falsification, train_size = train_percent)
        self.FalsificationTrain, self.FalsificationTest = train_test_split(self.Falsification, train_size = train_percent)

        Xtrain = np.array(self.notFalsificationTrain + self.FalsificationTrain)
        Ytrain = []

        for x in xrange(len(self.notFalsificationTrain)):
            Ytrain.append(0)
        for x in xrange(len(self.FalsificationTrain)):
            Ytrain.append(1)

        Xtest = np.array(self.notFalsificationTest + self.FalsificationTest)
        Ytest = []

        for x in xrange(len(self.notFalsificationTest)):
            Ytest.append(0)
        for x in xrange(len(self.FalsificationTest)):
            Ytest.append(1)

        print "Falsification Stories for Training: ", len(Xtrain)
        print "Falsification Stories for Testing: ", len(Xtest)

        self.train(Xtrain, Ytrain)

        correct_preds = 0

        for x in xrange(len(Ytest)):
            pred = self.classifier_linear.predict(self.getScores([Xtest[x]]))
            if pred == Ytest[x]:
                correct_preds = correct_preds + 1

        print "Correct classifications: ", correct_preds
        print "Total classifications:   ", len(Ytest)
        self.classifierScore_SVM = "SVM Test set score: ", correct_preds / float(len(Ytest))
        print self.classifierScore_SVM

    def train(self, train_data, Ytrain, allClassifiers=False, crossValidate=False):

        avgFalsification = []
        avgNotFalsification = []

        ######################## vectors construction and training ####################

        #BUILD THE TF-IDF VECTORS THAT INDEXES UNIGRAMS AND BIGRAMS AND REMOVES STOPWORDS

        self.vectorizer = TfidfVectorizer(min_df=2, ngram_range=(1,2), stop_words='english')
        train_tdfvectors = self.vectorizer.fit_transform(train_data)

        # CREATE A NUMPY ARRAY THAT READS THE LIWC VARIABLES THAT ARE BEING USED IN THE TRAINING AND APPENDS THEM TO THE TF-IDF VECTOR
        #the following list is from the old precomputed values, we have to re-calculate them here with the LIWC replacements
        #good_feat_list = ['pronoun','ppron','ipron','prep','verb','conj','adverb','adj','negemo','Period','Comma','Colon','SemiC','QMark','Exclam','Quote','Absurd','Humor']

        #feature scores for stories from the training set
        #cannot use the values in the training set because the LIWC features produce different values than the replacement code.
        train_feat = []
        train_count = 0

        for story in train_data:

            avgArrayName = ""
            if Ytrain[train_count] == 0:
                avgArrayName = "NotFalsification"
            else:
                avgArrayName = "Falsification"

            train_count = train_count + 1

            patternParseTree = parsetree(story, tokenize=True, tags=True, chunks=True, relations=True, lemmata=True)
            lstTextPOS = []
            lstTextWords = []
            lstTextChunks = []

            f9 = 0
            f10 = 0
            f11 = 0
            f12 = 0
            f13 = 0
            f14 = 0

            for sentence in patternParseTree:
				f9 = f9 + self.getPeriods(sentence)
				f10 = f10 + self.getCommas(sentence)
				f11 = f11 + self.getColon(sentence)
				f12 = f12 + self.getSemicolon(sentence)
				f13 = f13 + self.getQuestionMarks(sentence)
				f14 = f14 + self.getExclamationMarks(sentence)
				for chunk in sentence.chunks:
					lstTextChunks.append(chunk)
					for word in chunk.words:
						lstTextPOS.append(word.type)
						lstTextWords.append(word.string)

            divisorWordCount = float(len(lstTextWords))

			#f - feature
			#f1: PRP + PRP$ (check)
            f1 = self.getPronouns(lstTextPOS, len(lstTextWords))

			#f2: PRP
            f2 = self.getPersonalPronouns(lstTextPOS, len(lstTextWords))

            #f3: PRP$ (pronouns, possessive. check)
            f3 = self.getPossessivePronouns(lstTextPOS, len(lstTextWords))

            #f4: PP (prepositional phrase? check)
            f4 = self.getPrepositionalPhrases(lstTextChunks, len(lstTextWords))

            #f5: VP
            f5 = self.getVerbPhrases(lstTextChunks, len(lstTextWords))

            #f6: CC, IN
            f6 = self.getConjunctions(lstTextPOS, len(lstTextWords))

            #f7: ADVP
            f7 = self.getAdverbPhrases(lstTextChunks, len(lstTextWords))

            #f8: ADJP
            f8 = self.getAdjectivePhrases(lstTextChunks, len(lstTextWords))

            #f9-14 are all done during sentence processing

            #f9: periods, may not be the same as the LIWC functions
            f9 = self.getPercentage(f9, divisorWordCount)
            #f10: ,
            f10 = self.getPercentage(f10, divisorWordCount)
            #f11: :
            f11 = self.getPercentage(f11, divisorWordCount)
            #f12: semicolons
            f12 = self.getPercentage(f12, divisorWordCount)
            #f13: question marks
            f13 = self.getPercentage(f13, divisorWordCount)
            #f14: exclamations
            f14 = self.getPercentage(f14, divisorWordCount)

            #falsification add-on features
            lineLIST = self.getParagraphs(story)
            f15 = self.getNoOfParagraphsPerNewsStory(lineLIST)
            f16 = self.getAVGWordLength(lineLIST)     #NOTE: definitely a bug in this function, results are too low
            f17 = self.getAVGNoOfSentencesPerParagraph(lineLIST)
            f18 = self.getAVGNoOfWordsPerSentence(lineLIST)
            f19 = self.getAVGNoOfWordsPerParagraph(lineLIST)
            f20 = self.getPausality(lineLIST)
            f21 = self.getEMOTIVENESS(lineLIST)
            f22 = self.getPRONOUNcountperSENTENCE(lineLIST)
            f23 = self.getINFORMALITY(lineLIST)
            f24 = self.getLEXICALdiversity(lineLIST)
            f25 = self.getAFFECT(lineLIST)

            #print story
            absflag = self.getAbsurdityScore(story)

            story_features = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16, f17, f18, f19, f20, f21, f22, f23, f24, f25, absflag]

            if avgArrayName == "Falsification":
                #set up our list of features averages based on the size of our first sample
                if len(avgFalsification) == 0:
                    for c in xrange(len(story_features)):
                        avgFalsification.append(0)

                #sum everything to get an average later
                for x in xrange(len(story_features)):
                    avgFalsification[x] = float(avgFalsification[x]) + float(story_features[x])
            elif avgArrayName == "NotFalsification":
                #set up our list of features averages based on the size of our first sample
                if len(avgNotFalsification) == 0:
                    for c in xrange(len(story_features)):
                        avgNotFalsification.append(0)

                #sum everything to get an average later
                for x in xrange(len(story_features)):
                    avgNotFalsification[x] = float(avgNotFalsification[x]) + float(story_features[x])

            print train_count, story_features

            train_feat.append(story_features)

        Xtrain = np.hstack([train_tdfvectors.toarray(), train_feat])

        #divide to get avgs
        for x in xrange(len(avgFalsification)):
            avgFalsification[x] = avgFalsification[x] / float(len(avgFalsification))
        for x in xrange(len(avgNotFalsification)):
            avgNotFalsification[x] = avgNotFalsification[x] / float(len(avgNotFalsification))

        print "AVG Not Falsification Feature Scores"
        print avgFalsification

        print "AVG Falsification Feature Scores"
        print avgNotFalsification

        # Perform classification with SVM, kernel=linear
        self.classifier_linear = svm.SVC(kernel='linear', probability = True)
        self.classifier_linear.fit(Xtrain, Ytrain)

    def getScores(self, test_data, returnBoth = False):

        test_tdfvectors = self.vectorizer.transform(array(test_data))

        #disabled for now
        #print test_data[0]
        absflag = self.getAbsurdityScore(test_data[0])
        humflag = 0 #self.getHumorScore(test_data)

        #all liwc calls are replaced here with generally eqviliant calls to pattern
        #from what I understand "goodfeatures" holds numbers from liwc for the entire test set
        #test_data here is a single new story

        #liwc=receptiviti.get_liwc(name, [test_data])
        #goodfeatures = array([liwc['categories']['pronoun'],liwc['categories']['ppron'],liwc['categories']['ipron'],liwc['categories']['prep'],liwc['categories']['verb'],liwc['categories']['conj'],liwc['categories']['adverb'],liwc['categories']['adj'],liwc['categories']['negemo'],liwc['categories']['Period'],liwc['categories']['Comma'],liwc['categories']['Colon'],liwc['categories']['SemiC'], liwc['categories']['QMark'],liwc['categories']['Exclam'],liwc['categories']['Quote']])
        liwc_feat_list = ['Pronouns','Personal Pronouns ','Impersonal Pronouns','Prepositions','Verbs','Conjunctions','Adverbs','Adjectives','Negative Emotions','Periods','Commas','Colons','Semicolons','Question Marks','Exclamations','Quotes']

        patternParseTree = parsetree(test_data[0], tokenize=True, tags=True, chunks=True, relations=True, lemmata=True)
        lstTextPOS = []
        lstTextWords = []
        lstTextChunks = []

        f9 = 0
        f10 = 0
        f11 = 0
        f12 = 0
        f13 = 0
        f14 = 0

        for sentence in patternParseTree:
            f9 = f9 + self.getPeriods(sentence)
            f10 = f10 + self.getCommas(sentence)
            f11 = f11 + self.getColon(sentence)
            f12 = f12 + self.getSemicolon(sentence)
            f13 = f13 + self.getQuestionMarks(sentence)
            f14 = f14 + self.getExclamationMarks(sentence)
            for chunk in sentence.chunks:
                lstTextChunks.append(chunk)
                for word in chunk.words:
                    lstTextPOS.append(word.type)
                    lstTextWords.append(word.string)

        divisorWordCount = float(len(lstTextWords))

        #f - feature
        #f1: PRP + PRP$ (check)
        f1 = self.getPronouns(lstTextPOS, len(lstTextWords))

        #f2: PRP
        f2 = self.getPersonalPronouns(lstTextPOS, len(lstTextWords))

        #f3: PRP$ (pronouns, possessive. check)
        f3 = self.getPossessivePronouns(lstTextPOS, len(lstTextWords))

        #f4: PP (prepositional phrase? check)
        f4 = self.getPrepositionalPhrases(lstTextChunks, len(lstTextWords))

        #f5: VP
        f5 = self.getVerbPhrases(lstTextChunks, len(lstTextWords))

        #f6: CC, IN
        f6 = self.getConjunctions(lstTextPOS, len(lstTextWords))

        #f7: ADVP
        f7 = self.getAdverbPhrases(lstTextChunks, len(lstTextWords))

        #f8: ADJP
        f8 = self.getAdjectivePhrases(lstTextChunks, len(lstTextWords))

        #f9-14 are all done during sentence processing

        #f9: periods, may not be the same as the LIWC functions
        f9 = self.getPercentage(f9, divisorWordCount)
        #f10: ,
        f10 = self.getPercentage(f10, divisorWordCount)
        #f11: :
        f11 = self.getPercentage(f11, divisorWordCount)
        #f12: semicolons
        f12 = self.getPercentage(f12, divisorWordCount)
        #f13: question marks
        f13 = self.getPercentage(f13, divisorWordCount)
        #f14: exclamations
        f14 = self.getPercentage(f14, divisorWordCount)

		#falsification add-on features
        lineLIST = self.getParagraphs(test_data[0])
        f15 = self.getNoOfParagraphsPerNewsStory(lineLIST)
        f16 = self.getAVGWordLength(lineLIST)     #NOTE: definitely a bug in this function, results are too low
        f17 = self.getAVGNoOfSentencesPerParagraph(lineLIST)
        f18 = self.getAVGNoOfWordsPerSentence(lineLIST)
        f19 = self.getAVGNoOfWordsPerParagraph(lineLIST)
        f20 = self.getPausality(lineLIST)
        f21 = self.getEMOTIVENESS(lineLIST)
        f22 = self.getPRONOUNcountperSENTENCE(lineLIST)
        f23 = self.getINFORMALITY(lineLIST)
        f24 = self.getLEXICALdiversity(lineLIST)
        f25 = self.getAFFECT(lineLIST)

        featuresWithFlags = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16, f17, f18, f19, f20, f21, f22, f23, f24, f25, absflag]

        Xtest = np.append(test_tdfvectors.toarray(), featuresWithFlags)
        Xtest=Xtest.reshape(1,-1)

        if returnBoth == False:
            return Xtest
        else:
            return [featuresWithFlags, Xtest]

    def predict(self, text):
        test_dataF = text

        if test_dataF:
            test_dataF= test_dataF.replace("\n","")

        t = {'Full Text': [test_dataF]}
        test = pd.DataFrame(data=t)

        test_data = []
        for testitem in test['Full Text']:
            test_data.append(str(testitem).decode('utf-8',errors='ignore'))

        pairFeaturesXtest = self.getScores(test_data, True)
        features = pairFeaturesXtest[0]
        Xtest = pairFeaturesXtest[1]

        prediction_linear = self.classifier_linear.predict(Xtest)
        prediction_scores = self.classifier_linear.predict_proba(Xtest)

        betterString = str(prediction_scores[0])[1:-1]
        classValues = betterString.split(" ")
        classValues = filter(None, classValues)
        return ",".join(classValues) + "," + ",".join(str(featScore) for featScore in features)