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
# Name:        clickbaitml.py
# Purpose:     detect clickbait
#
# Created:     03/06/2017
#
# Language and Information Technology Research Lab
# Faculty of Information and Media Studies (FIMS)
# University of Western Ontario, London, Canada
#-------------------------------------------------------------------------------

import nltk
import codecs
import numpy as np
import xlsxwriter
from collections import Counter
from nltk.corpus import brown
from pattern.en import parsetree, ngrams, modality, mood, sentiment, number, wordnet
from pattern.en.wordlist import TIME, ACADEMIC
from numpy import array
from html import HTML
from scipy import stats

from sklearn import grid_search
from sklearn import svm
from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, RobustScaler, normalize #.. normalize actually makes things worse
from sklearn.pipeline import Pipeline
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import mean_squared_error, precision_score, recall_score, f1_score
from traininghandler import TrainingHandler

#for precision-recall
from sklearn.metrics import average_precision_score
from sklearn.metrics import precision_recall_curve

class clickbaitDetector:

    def __init__(self, topWordsFeatureCount, topTrigramsFeatureCount, includeValidationSet=True, includeGangulySet=False, notClickbaitLowerbound=0.30, clickbaitUpperbound=0.60, buildBagOfWords=False, buildBagOfTrigrams=False, trainSize = 0.7):
        print "Initializing LITRL Clickbait Detector..."
        self.trainSize = trainSize
        print "Training size: ", self.trainSize
        print "Test size: ", 1.0-self.trainSize
        #use the top words as features (bag-of-words-ish...?)
        self.TOP_WORD_COUNT = topWordsFeatureCount
        #use the top trigrams as features (should detect common clickbait "Here's how", "These 10 things..." etc)
        self.TOP_TRIGRAM_COUNT = topTrigramsFeatureCount
        #not getting clickbait words or trigrams speeds things up, but decreases performance
        self.buildBagOfWords = buildBagOfWords
        self.buildBagOfTrigrams = buildBagOfTrigrams
        if buildBagOfTrigrams == False:
            self.TOP_TRIGRAM_COUNT = 0
        if buildBagOfWords == False:
            self.TOP_WORD_COUNT = 0
        #print out whole numpy arrays
        np.set_printoptions(threshold=np.nan)
        #setup the detector
        self.loadSwearing()
        self.notClickbaitLowerbound = notClickbaitLowerbound
        self.clickbaitUpperbound = clickbaitUpperbound
        self.th = TrainingHandler(True, notClickbaitLowerbound, clickbaitUpperbound, includeValidationSet, includeGangulySet)
        self.setupFeatureNameList()
        #used by the dist to NNP features
        self.tagsNNP = [u"NNP", u"NNPS", u"NNP-POS", u"NNP-PERS"]
        self.tagsNP  = [u"NN", u"NNS"]
        self.digits  = [u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0"]
        #some numbers we don't want to include for clickbait, need to be able to parse phone numbers
        self.numbersToAvoid = [u"911"]
        #for the classifier - big numbers really slow things down
        self.AMT_TINY = 25
        self.AMT_SMALL = 100
        self.AMT_MEDIUM = 1500
        self.AMT_LARGE = 5000
        self.AMT_XLARGE = 10000
        self.AMT_MASSIVE = 1000000
        self.AMT_TINY_CLASS = 10
        self.AMT_SMALL_CLASS = 20
        self.AMT_MEDIUM_CLASS = 30
        self.AMT_LARGE_CLASS = 40
        self.AMT_XLARGE_CLASS = 50
        self.AMT_MASSIVE_CLASS = 60

    #easiest way to print out information about features is to maintain a list of their names
    def setupFeatureNameList(self):
        self.featureNames = ["getWordCount", "getWord2GramsAvgLen", "getWord3GramsAvgLen", "getHashTagsAndRTs", "getQuestionMarks", "getAtMentions", "getNumbersSum", "minDistToNNP", "maxDistToNNP", "getNNPLOCCount", "getNNPPERSCount", "getSwearCount", "getAdjpCount", "getAdvpCount", "getNNPCount", "getVerbCount", "getNPsCount", "avgDistToNNP", "getCharLength", "getPronounCount", "getEmotiveness", "getTimeWordsCount", "getAcademicWordsCount", "getFirstNNPPos", "startsWithNumber", "maxDistFromNPToNNP", "NNPCountOverNPCount", "lenOfLongestWord", "maxDistToQuote", "containsOn", "minDistToOn", "containsTriggers", "npsPlusNNPsOverNumbersSum", "maxDistToHashTag", "maxDistToAt", "firstPartContainsColon", "determiners", "noun similarity"]
        self.featureNamesTopWord = []
        self.featureNamesTopTrigram = []
        if self.buildBagOfWords == True:
            for x in xrange(self.TOP_WORD_COUNT):
                self.featureNamesTopWord.append("TopWord: ")
        if self.buildBagOfTrigrams == True:
            for x in xrange(self.TOP_TRIGRAM_COUNT):
                self.featureNamesTopTrigram.append("TopTrigram: ")

    #this should be called after getting the list of top trigrams/words
    def buildFeatureNameList(self):
        self.featureNames = self.featureNames + self.featureNamesTopWord
        self.featureNames = self.featureNames + self.featureNamesTopTrigram

    #compute and assign the most commonly occuring words to self.topWords
    def buildTopWordList(self, setToProcess):
        if self.TOP_WORD_COUNT == 0:
            return
        self.topWords = Counter()
        for x in xrange(0, len(setToProcess)):
            strSentenceText = setToProcess[x]['text']
            patternParseTree = parsetree(setToProcess[x]['text'], tokenize=True, tags=True, chunks=True, relations=True, lemmata=True)
            for sentence in patternParseTree:
                for chunk in sentence.chunks:
                    for word in chunk.words:
                        self.topWords[word.string] = self.topWords[word.string] + 1
        #add this top word to the list of features so we can see it
        self.topWords = self.topWords.most_common(self.TOP_WORD_COUNT)
        print "Bag-of-WORDS: ", self.topWords
        for x in xrange(0, len(self.topWords)):
            self.featureNamesTopWord[x] = self.featureNamesTopWord[x] + self.topWords[x][0]

    #given a clickbait headline determine if it contains any top words
    def getTopWordCounts(self, lstSentWords):
        wordList = []
        features = []
        for tup in self.topWords:
            wordList.append(tup[0])
            features.append(0)
        for x in xrange(len(lstSentWords)):
            for y in xrange(len(wordList)):
                if (lstSentWords[x]== wordList[y]):
                    features[y] = features[y] + 1
                    break
        return features

    #compute and assign the top trigrams to self.topTrigrams
    def buildTopTrigramList(self, setToProcess):
        if self.TOP_TRIGRAM_COUNT == 0:
            return
        self.topTrigrams = Counter()
        for x in xrange(0, len(setToProcess)):
            strSentenceText = setToProcess[x]['text']
            patternParseTree = parsetree(setToProcess[x]['text'], tokenize=True, tags=True, chunks=True, relations=True, lemmata=True)
            for sentence in patternParseTree:
                lstSentenceWords = []
                for chunk in sentence.chunks:
                    for w in xrange(len(chunk.words)):
                        lstSentenceWords.append(chunk[w].string)
                for w in xrange(len(lstSentenceWords)):
                    trigram = []
                    if w + 3 < len(lstSentenceWords):
                        #build the trigram, forward only
                        for n in xrange(3):
                            trigram.append(lstSentenceWords[w + n].lower())
                        strTrigram = ','.join(trigram)
                        self.topTrigrams[strTrigram] = self.topTrigrams[strTrigram] + 1
        self.topTrigrams = self.topTrigrams.most_common(self.TOP_TRIGRAM_COUNT)
        print "Bag-of-TRIGRAMS: ", self.topTrigrams
        for x in xrange(0, len(self.topTrigrams)):
            self.featureNamesTopTrigram[x] = self.featureNamesTopTrigram[x] + self.topTrigrams[x][0]

    #compute trigrams for a headline and assign the most commonly occuring trigram features + 1 for each
    def getTopTrigramCounts(self, lstSentenceWords):
        trigramList = []
        features = []
        for tup in self.topTrigrams:
            trigramList.append(tup[0])
            features.append(0)
        for w in xrange(len(lstSentenceWords)):
            trigram = []
            if w + 3 < len(lstSentenceWords):
                #build the trigram, forward only
                for n in xrange(3):
                    trigram.append(lstSentenceWords[w + n].lower())
                strTrigram = ','.join(trigram)
                for t in xrange(len(trigramList)):
                    if trigramList[t] == strTrigram:
                        features[t] = features[t] + 100
        return features

    #main function to process items from our training handler
    #a web application could also use this method
    def processHeadlines(self, setToProcess, setAveragesTitle = "", verbose=True):
        sampleSet = []
        avgList = []

        for x in xrange(0, len(setToProcess)):
            strSentenceText = setToProcess[x]['text']
            truthMean = setToProcess[x]['truth-mean']
            patternParseTree = parsetree(setToProcess[x]['text'], tokenize=True, tags=True, chunks=True, relations=True, lemmata=True)
            lstSentPOS = []
            lstSentWords = []
            for sentence in patternParseTree:
                for chunk in sentence.chunks:
                    for word in chunk.words:
                        lstSentPOS.append(word.type)
                        lstSentWords.append(word.string)

            #f     - machine learning feature
            #lst   - list data structure
            #str   - character string
            #Sent  - sentence
            f0 = self.getWordCount(lstSentWords)
            f1 = self.getWord2GramsAvgLen(strSentenceText)
            f2 = self.getWord3GramsAvgLen(strSentenceText)
            f3 = self.getHashTagsAndRTs(strSentenceText, lstSentWords)
            f4 = self.getQuestionMarks(strSentenceText)
            f5 = self.getAtMentions(strSentenceText)
            f6 = self.getNumbersSum(lstSentWords) #will return 0 if skipGetNumbersSum is true
            f7 = self.minDistToNNP(lstSentPOS, lstSentWords)  #think this is OK now
            f8 = self.maxDistToNNP(lstSentPOS, lstSentWords) #think this is OK now
            f9 = self.getNNPLOCCount(lstSentPOS)
            f10 = self.getNNPPERSCount(lstSentPOS)
            f11 = self.getSwearCount(lstSentWords) #s
            f12 = self.getAdjpCount(lstSentPOS)
            f13 = self.getAdvpCount(lstSentPOS)
            f14 = self.getNNPCount(lstSentPOS)
            f15 = self.getVerbCount(lstSentPOS)
            f16 = self.getNPsCount(lstSentPOS)
            f17 = self.avgDistToNNP(lstSentPOS, lstSentWords) #think this is OK now
            f18 = self.getCharLength(strSentenceText)
            f19 = self.getPronounCount(lstSentPOS)
            f20 = self.getEmotiveness(f12, f13, f16, f15)
            f21 = self.getTimeWordsCount(lstSentWords)
            f22 = self.getAcademicWordsCount(lstSentWords)
            f23 = self.getFirstNNPPos(lstSentPOS)
            f24 = self.startsWithNumber(lstSentWords)
            f25 = self.maxDistFromNPToNNP(lstSentPOS) #self.getTrainingClickbaitSimilarity(strSentenceText)
            f26 = (f14 / f16) if f16 else 0
            f27 = self.lenOfLongestWord(lstSentWords)
            f28 = self.maxDistToQuote(strSentenceText)
            f29 = self.containsOn(strSentenceText)
            f30 = self.minDistToOn(strSentenceText)
            f31 = self.containsTriggers(strSentenceText)
            f32 = (f16 + f18) / f8 if f8 else 0 #NPs + NNPs / sum of the numbers found in headline
            f33 = self.maxDistToHashTag(strSentenceText)
            f34 = self.maxDistToAt(strSentenceText)
            f35 = self.firstPartContainsColon(strSentenceText)
            f36 = self.getDeterminers(lstSentPOS) # Uncommon, but much more prevalent in clickbait. A. Chakraborty, B. Paranjape, S.Kakarla, and N. Ganguly. 2016.
            f37 = self.maxSimilarityOfNNPsAndNPs(lstSentWords, lstSentPOS)

            sample = [f0,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19,f20,f21,f22,f23,f24,f25,f26,f27,f28,f29,f30,f31,f32,f33,f34,f35,f36,f37]

            if self.buildBagOfWords == True:
                #top words features: default 100
                fLastTopWordCount = self.getTopWordCounts(lstSentWords)
                sample = sample + fLastTopWordCount

            if self.buildBagOfTrigrams == True:
                #top trigrams features: default 50
                fLastTopTrigramsCount = self.getTopTrigramCounts(lstSentWords)
                sample = sample + fLastTopTrigramsCount

            #set up our list of features averages based on the size of our first sample
            if len(avgList) == 0:
                for c in xrange(len(sample)):
                    avgList.append(0)

            #sum everything to get an average later
            for x in xrange(len(sample)):
                avgList[x] = float(avgList[x]) + float(sample[x])

            #kind of poor fix to get the truth means for mean squared error in the train/test
            sample.append(truthMean)

            #kind of poor fix to print the text headline with the classifier prediction value
            sample.append(strSentenceText)
            sampleSet.append(sample)

        for x in xrange(len(sample) - 2):  #-2 for poor fix mentioned above
            avgList[x] = avgList[x] / float(len(sampleSet))

        if verbose == True:
            print setAveragesTitle

        formattedAverages = []

        #print averages with names of features (easiest way is to maintain an array of names)
        if verbose == True:
            print len(self.featureNames), len(avgList)

        for x in xrange(0, len(sample) - 2):  #-2 for poor fix mentioned above
            #twodecimals.append([self.featureNames[x], avgList[x]])
            formattedAverages.append(avgList[x])

        if verbose == True:
            print "AVG LIST:"
            print formattedAverages

        return sampleSet

    #process headlines for our clickbait and not clickbait training set
    def buildClickbaitSet(self):
        #th.trainingSetClickbait
        clickbaitAverageTitle = "CLICKBAIT FEATURE AVG"
        #only get top bag-of-words and trigrams JUST for clickbait, these should separate clickbait and not-clickbait
        if self.buildBagOfWords == True:
            self.buildTopWordList(self.th.trainingSetClickbait)
        if self.buildBagOfTrigrams == True:
            self.buildTopTrigramList(self.th.trainingSetClickbait)
        self.buildFeatureNameList()
        sampleSet = self.processHeadlines(self.th.trainingSetClickbait, clickbaitAverageTitle)
        return sampleSet

    def buildNonClickbaitSet(self):
        #th.trainingSetNoClickbait
        notClickbaitAverageTitle = "NONCLICKBAIT FEATURE AVG"
        sampleSet = self.processHeadlines(self.th.trainingSetNoClickbait, notClickbaitAverageTitle)
        return sampleSet

    def buildValidationClickbaitSet(self):
        clickbaitAverageTitle = "CLICKBAIT VALIDATION FEATURE AVG"
        #only get top bag-of-words and trigrams JUST for clickbait, these should separate clickbait and not-clickbait
        if self.buildBagOfWords == True:
            self.buildTopWordList(self.th.validationSetClickbait + self.th.gangulyClickbait)
        if self.buildBagOfTrigrams == True:
            self.buildTopTrigramList(self.th.validationSetClickbait + self.th.gangulyClickbait)
        self.buildFeatureNameList()
        sampleSet = self.processHeadlines(self.th.validationSetClickbait + self.th.gangulyClickbait, clickbaitAverageTitle)
        return sampleSet

    def buildValidationNonClickbaitSet(self):
        #th.trainingSetNoClickbait
        notClickbaitAverageTitle = "NONCLICKBAIT VALIDATION FEATURE AVG"
        sampleSet = self.processHeadlines(self.th.validationSetNoClickbait + self.th.gangulyNoClickbait, notClickbaitAverageTitle)
        return sampleSet

    def getWordCount(self, words):
        return len(words)

    #word 2-grams - AMOUNT of them... don't think this is very useful
    #Fixed: now is average LENGTH of the two grams
    def getWord2GramsAvgLen(self, sentence):
        twograms = ngrams(sentence, n=2)
        totalLen = 0
        for twogram in twograms:
            totalLen = totalLen + len(twogram[0])
            totalLen = totalLen + len(twogram[1])
        if len(twograms) > 0:
            return float(totalLen / len(twograms))
        else:
            return 0

    #word 3-grams - AMOUNT of them... don't think this is very useful
    #Fixed: now is average LENGTH of the three grams
    def getWord3GramsAvgLen(self, sentence):
        threegrams = ngrams(sentence, n=3)
        totalLen = 0
        for threegram in threegrams:
            totalLen = totalLen + len(threegram[0])
            totalLen = totalLen + len(threegram[1])
            totalLen = totalLen + len(threegram[2])
        if len(threegrams) > 0:
            return float(totalLen / len(threegrams))
        else:
            return 0

    #ganguly, 2016. DTs are normally not present in any headlines, but they do occur much more in clickbait
    #very similar to the NNP-PERS or NNP-LOC stuff
    def getDeterminers(self, lstSentPOS):
        count = 0
        for pos in lstSentPOS:
            if u"DT" in pos:
                count = count + 1
        return count

    #character 2 grams have been removed since the old code would just use the amount of char n-grams as a feature
    #this is incorrect. Using the most common 2-grams though may be useful.

    #hashtags
    def getHashTagsAndRTs(self, sentence, words):
        count = sentence.count(u"#")
        for word in words:
            if u"RT" in word:
                count = count + 1
        return count

    #question marks
    def getQuestionMarks(self, sentence):
        count = sentence.count(u"?")
        return count

    #@ mentions
    def getAtMentions(self, sentence):
        count = sentence.count(u"@")
        return count

    #sum the numbers in the headline. clickbait will have more, unit tests expect a float
    def getNumbersSum(self, words):
        #this is ALWAYS 10 for some reason... need to check it
        count = 0
        for x in xrange(len(words)):
            for digit in self.digits:
                if digit in words[x] and words[x] not in self.numbersToAvoid:
                    num = float(number(words[x]))
                    count = count + num

        #must classify numbers otherwise this really slows down performance
        #TODO: support for negative numbers?
        amountClass = 0
        if count < self.AMT_TINY:
            amountClass = self.AMT_TINY_CLASS
        elif count < self.AMT_SMALL:
            amountClass = self.AMT_SMALL_CLASS
        elif count < self.AMT_MEDIUM:
            amountClass = self.AMT_MEDIUM_CLASS
        elif count < self.AMT_LARGE:
            amountClass = self.AMT_LARGE_CLASS
        elif count < self.AMT_XLARGE:
            amountClass = self.AMT_XLARGE_CLASS
        elif count < self.AMT_MASSIVE:
            amountClass = self.AMT_MASSIVE_CLASS
        else:
            amountClass = self.AMT_MASSIVE_CLASS

        return float(amountClass)

    #list of numbers 1 2 3 4, 1st 2nd 3rd... TODO

    #time or month or year (AM PM in the afternoon)
    #TODO, numeric dates19XX, 20XX
    def getTimeWordsCount(self, words):
        timeWords = [w for w in words if w in TIME]
        return len(timeWords)

    #more academic words may suggest non-clickbait
    def getAcademicWordsCount(self, words):
        academicWords = [w for w in words if w in ACADEMIC]
        return len(academicWords)

    #adjective phrases over total parts of speech
    def getAdvpCount(self, partsOfSpeech):
        count = 0
        for pos in partsOfSpeech:
            if pos.count(u"RB") > 0:
                count = count + 1
        return count


    #adjp phrases over total parts of speech
    def getAdjpCount(self, partsOfSpeech):
        count = 0
        for pos in partsOfSpeech:
            if pos.count(u"JJ") > 0:
                count = count + 1
        return count

    #vb phrases over total parts of speech
    def getVerbCount(self, partsOfSpeech):
        count = 0
        for pos in partsOfSpeech:
            if pos.count(u"VB") > 0:
                count = count + 1
        return count

    #how many NNP's do we have? (less is indicative of clickbait). brogly
    def getNNPCount(self, partsOfSpeech):
        count = 0
        for pos in partsOfSpeech:
            if u"NNP" == pos and u"NNP-LOC" != pos and u"NNP-PERS" != pos:
                count = count + 1
        return count

    #how many pronouns (PRP, PRP$, WP, WP$) do we have? Vicki.
    def getPronounCount(self, partsOfSpeech):
        count = 0
        for pos in partsOfSpeech:
            if u"PRP" == pos or u"PRP$" == pos or u"WP" == pos or u"WP$" == pos:
                count = count + 1
        return count

    #nouns
    def getNPsCount(self, partsOfSpeech):
        npCount = 0
        for pos in partsOfSpeech:
            if u"NN" == pos :
                npCount = npCount + 1
            elif u"NNS" == pos:
                npCount = npCount + 1
        return npCount

    #load swears
    def loadSwearing(self):
        self.swears = set()
        fk = open('swearing.txt', 'r')
        swears = fk.readlines()
        for x in xrange(len(swears)):
            self.swears.add(unicode(swears[x].rstrip().lower(), "utf-8"))
        print "Swear/emotive word count: ", len(self.swears)

    #contains swear words
    #FIXME: only adding 1 if words are exactly equal and some lines in swears are phrases
    #Yimin
    def getSwearCount(self, sentWords):
        count = 0
        for word in sentWords:
            if word.lower() in self.swears:
                count = count + 10
        return float(count)

    #brogly
    def getFirstNNPPos(self, sentPOS):
        for x in xrange(0, len(sentPOS)):
            if sentPOS[x] == u"NNP":
                return x
        return 0

    #brogly. TODO: investigate adjectives/verbs
    def maxDistFromNPToNNP(self, sentPOS):
        firstNP = -1
        lastNNP = -1
        for x in xrange(0, len(sentPOS)):
            if sentPOS[x] in self.tagsNP:
                if firstNP == -1:
                    firstNP = x
            elif sentPOS[x] in self.tagsNNP:
                lastNNP = x
        if lastNNP > firstNP:
            return (lastNNP - firstNP)
        elif firstNP >= lastNNP:
            return (lastNNP - firstNP)
        elif lastNNP != -1:
            return -1
        elif firstNP != -1:
            return -2

    #max distance to an NNP
    #ie. for every NNP, pick the one with the most non-NNPs in front of it, call that max distance and use it
    #brogly. larger values indicative of clickbait.
    #TODO: bidirectional?
    def maxDistToNNP(self, sentPOS, sentWords):
        nnpDist = 0
        maxNNPDist = 0
        for x in xrange(0, len(sentPOS)):
            if sentPOS[x] not in self.tagsNNP:
                nnpDist = nnpDist + 1
            elif sentPOS[x] in self.tagsNNP:
                if nnpDist > maxNNPDist:
                    maxNNPDist = nnpDist
                nnpDist = 0
        return maxNNPDist

    #min dist to NNP - TODO: is this commutative with max dist for classifiers? Not sure
    #brogly
    def minDistToNNP(self, sentPOS, sentWords):
        nnpDist = 0
        allNNPDist = []
        for x in xrange(0, len(sentPOS)):
            if sentPOS[x] not in self.tagsNNP:
                nnpDist = nnpDist + 1
            elif sentPOS[x] in self.tagsNNP:
                allNNPDist.append(nnpDist)
                nnpDist = 0
        if len(allNNPDist) > 0:
            return min(allNNPDist)
        else:
            return 0

    #average distance to an NNP. unclear if average distance changes much.
    #brogly
    def avgDistToNNP(self, sentPOS, sentWords):
        nnpDist = 0
        nnpDists = []
        for x in xrange(0, len(sentPOS)):
            if sentPOS[x] not in self.tagsNNP:
                nnpDist = nnpDist + 1
            elif sentPOS[x] in self.tagsNNP:
                nnpDists.append(nnpDist)
                nnpDist = 0
        total = 0
        for x in xrange(0, len(nnpDists)):
            total = total + nnpDists[x]
        if len(nnpDists) > 0:
            return (float(total) / float(len(nnpDists))) * 10
        else:
            return 0

    #amt of NNP-LOCs
    #unfortunately this is usually low in clickbait and non-clickbait, but clickbait generally has less
    #brogly
    def getNNPLOCCount(self, poses):
        count = 0
        for pos in poses:
            if pos == u"NNP-LOC":
                count = count + 1
        return count

    #amt of NNP-PERS
    #unfortunately this is usually low in clickbait and non-clickbait, but clickbait generally has less
    #brogly
    def getNNPPERSCount(self, poses):
        count = 0
        for pos in poses:
            if pos == u"NNP-PERS":
                count = count + 1
        return count

    #overall character length of string. stein and potthast
    def getCharLength(self, strSentenceText):
        return len(strSentenceText)

    #emotiveness from paper. Nadia/Vicki/Yimin 2015.
    def getEmotiveness(self, totalAdjs, totalAdvps, totalNPs, totalVBs):
        if (float(totalNPs) + float(totalVBs)) > 0:
            return (float(totalAdjs) + float(totalAdvps)) / (float(totalNPs) + float(totalVBs))
        else:
            return 0

    #from stein, potthast et al; clickbait paper; this has 72% indiciation of clickbait
    def startsWithNumber(self, words):
        if len(words) == 0:
            return 0
        else:
            for digit in self.digits:
                if digit in words[0]:
                    if number(words[0]):
                        return 1
                    else:
                        return 0
            return 0

    #distance to quotations may be indicative of clickbait
    #use max char length to quote TODO: switch to words, quotes are stripped in pattern
    #brogly
    def maxDistToQuote(self, strSentenceText):
        quoteDist = 0
        maxQuoteDist = 0
        for x in xrange(0, len(strSentenceText)):
            if strSentenceText[x] == u"\"":
                if quoteDist > maxQuoteDist:
                    maxQuoteDist = quoteDist
                    quoteDist = 0
                else:
                    quoteDist = 0
            else:
                quoteDist = quoteDist + 1
        return maxQuoteDist

    #may be indicative of clickbait. Brogly.
    def maxDistToHashTag(self, strSentenceText):
        dist = 0
        maxDist = 0
        for x in xrange(0, len(strSentenceText)):
            if strSentenceText[x] == u"#":
                if dist > maxDist:
                    maxDist = dist
                    dist = 0
                else:
                    dist = 0
            else:
                dist = dist + 1
        return maxDist

    #may be indictative of clickbait. Brogly.
    def maxDistToAt(self, strSentenceText):
        atIndex = strSentenceText.rfind(u"@")
        if atIndex == -1:
            return 0
        else:
            return atIndex

    #Turner, 1975, cited by Mardh
    #there does not appear to be any significant difference between clickbait/non-clickbait when looking at words, but if this is found ANYWHERE in the sentence there is
    def containsOn(self, strSentenceText):
        if u"on" in strSentenceText or "on" in strSentenceText:
            return 1
        else:
            return 0

    #Turner, 1975, cited by Mardh
    #not entirely sure which is more helpful, max or min dist to on
    def minDistToOn(self, strSentenceText):
        pos = strSentenceText.find(u"on")
        if pos == -1:
            return 0
        else:
            return pos

    #real news never contains the following terms. Vicki/Sarah.
    def containsTriggers(self, strSentenceText):
        triggers = [u"there's", u"a", u"you", u"this", u"that", u"an", u"they", u"why", u"here", u"here's", u"heres",u"watch",u"video",u"ways",u"spot", u"people", u"how", u"meet", u"everything"]
        triggerCount = 0
        for trigger in triggers:
            if trigger in strSentenceText.lower():
                triggerCount = triggerCount + 100
        return triggerCount

    #return the length of the longest word, from potthast et al (not particularly effective)
    #from stein and potthast
    def lenOfLongestWord(self, words):
        wordLens = []
        for word in words:
            wordLens.append(len(word))
        #ODD BUG: wordLens can be zero?
        if len(wordLens) == 0:
            return 0
        return max(wordLens)

    #indicative of clickbait. Brogly.
    def firstPartContainsColon(self, strSentenceText):
        firstPart = ""
        if (len(strSentenceText) > 15):
            firstPart = strSentenceText[:15]
        else:
            firstPart = strSentenceText
        if u":" in firstPart:
            return 10
        else:
            return 0

    #a low max similarity is likely indicative of clickbait. Vicki.
    def maxSimilarityOfNNPsAndNPs(self, words, wordsPOS):
        nps = []
        result = 0

        for x in xrange(len(words)):
            if wordsPOS[x] in self.tagsNP:
                nps.append(words[x])
            elif wordsPOS[x] in self.tagsNNP:
                nps.append(words[x])

        #np-np
        if len(nps) == 0:
            #if no nps, there is no similarity
            result = 0
        else:
            for x in xrange(len(nps)):
                currentNPSynsets = wordnet.synsets(nps[x])
                if len(currentNPSynsets) > 0:
                    currentNP = currentNPSynsets[0]
                    for y in xrange(len(nps)):
                        if x != y:
                            otherNPSynsets = wordnet.synsets(nps[y])
                            if len(otherNPSynsets) > 0:
                                otherNP = otherNPSynsets[0]
                                sim = wordnet.similarity(currentNP, otherNP)
                                #if the similarity is higher, assign it for this feature
                                if sim > result:
                                    result = sim
        return result

    #write out graphs indicating feature comparisons, clickbait vs. non-clickbait
    def graphIndividualFeatures(self, clickbaitSamples, notClickbaitSamples, setname):
        clickbaitArray = np.array(clickbaitSamples)
        notClickbaitArray = np.array(notClickbaitSamples)

        h = HTML()
        h.h1(setname + " Report")
        h.br()
        h.a("",name = "topofpage")
        h.br()
        h.h2(self.classifierScore_SVM)
        h.br()
        h.h3(self.classifierScore_T1T2Good_CBCB)
        h.br()
        h.h3(self.classifierScore_T1T2Bad_LegitCB)
        h.br()
        h.h3(self.classifierScore_T1T2Bad_CBLegit)
        h.br()
        h.h3(self.classifierScore_T1T2Good_LegitLegit)
        h.br()

        #table of internal links for the report
        t = h.table(border='1')
        for x in xrange(len(self.featureNames) - self.TOP_TRIGRAM_COUNT - self.TOP_WORD_COUNT):
            r = t.tr
            r.td.a(self.featureNames[x], href=u"#" + self.featureNames[x])
            r.td('insert feature description here')
        h.br()

        means = []

        for x in xrange(len(self.featureNames) - self.TOP_TRIGRAM_COUNT - self.TOP_WORD_COUNT):
            h.a(name=self.featureNames[x]).h2(self.featureNames[x])

            clickbaitFeature = clickbaitArray[:,x]
            notClickbaitFeature = notClickbaitArray[:,x]

            #writing out data for publication formatting
            h.br()
            h.h2("Histogram Bins:")

            h.br()
            h.h2("Not Clickbait Scores - put these in excel")
            h.small(str(notClickbaitFeature))
            h.br()
            h.h2("Clickbait Scores - put these in excel")
            h.small(str(clickbaitFeature))
            h.br()

            means.append(abs(np.mean(clickbaitFeature) - np.mean(notClickbaitFeature)))

            h.br()
            h.h3(self.featureNames[x] + " Stats - NOT CLICKBAIT")
            h.br()
            l = h.ol

            l.li("Mean: " + str(np.mean(notClickbaitFeature)))
            l.li("Std Dev: " + str(np.std(notClickbaitFeature)))
            l.li("Variance: " + str(np.var(notClickbaitFeature)))
            l.li("Min: " + str(np.min(notClickbaitFeature)))
            l.li("Max: " + str(np.max(notClickbaitFeature)))

            #t-test
            l.li("(t-statistic, two-tailed p-val): " + str(stats.ttest_ind(notClickbaitFeature, clickbaitFeature, equal_var=False)))

            h.br()

            h.h3(self.featureNames[x] + " Stats - CLICKBAIT")
            h.br()
            l = h.ol
            l.li("Mean: " + str(np.mean(clickbaitFeature)))
            l.li("Std Dev: " + str(np.std(clickbaitFeature)))
            l.li("Variance: " + str(np.var(clickbaitFeature)))
            l.li("Min: " + str(np.min(clickbaitFeature)))
            l.li("Max: " + str(np.max(clickbaitFeature)))

            h.br()
            h.h4("Mean Difference: " + str(means[-1]))
            h.br()

            h.a("Back to Top", href="#topofpage")

        f = open("plots_features/" + setname + "_features_report.html", "w")
        f.write(unicode(h))
        f.close()

    #use a training and test set from the training set (2500 items)
    def trainSVMAndTestTrainingSet(self, allClassifiers=False, graphIndividualFeatures=False, statsPerFeature=False):
        self.clickbait = self.buildClickbaitSet()
        self.clickbaitTrain, self.clickbaitTest = train_test_split(self.clickbait, train_size = self.trainSize)
        self.notClickbait = self.buildNonClickbaitSet()
        self.notClickbaitTrain, self.notClickbaitTest = train_test_split(self.notClickbait, train_size = self.trainSize)

        #kind of poor fix to print the text headline with the classifier prediction value and get the truth mean
        #we basically just add it to the end of the feature scores list, then reorganize it here and delete it from the feature scores
        cbTestHeadlines = []
        notCbTestHeadlines = []
        for row in self.clickbaitTrain:
            del row[len(row) - 1]
            del row[len(row) - 1]
        for row in self.notClickbaitTrain:
            del row[len(row) - 1]
            del row[len(row) - 1]
        for row in self.clickbaitTest:
            cbTestHeadlines.append(row[len(row) - 1])
            del row[len(row) - 1]
            del row[len(row) - 1]
        for row in self.notClickbaitTest:
            notCbTestHeadlines.append(row[len(row) - 1])
            del row[len(row) - 1]
            del row[len(row) - 1]

        #added for type 1/2 errors - TODO: refactor
        self.testedHeadlines = cbTestHeadlines + notCbTestHeadlines

        fullSet = self.clickbaitTest + self.notClickbaitTest

        Xtrain = np.array(self.clickbaitTrain + self.notClickbaitTrain)
        Ytrain = []

        #y labels are the same length as sample and represent their class
        #0 - clickbait
        #1 - not clickbait
        for x in xrange(len(self.clickbaitTrain)):
            Ytrain.append(0)
        for x in xrange(len(self.notClickbaitTrain)):
            Ytrain.append(1)

        print "Feature count: ", len(self.featureNames)
        print "Trigram Bag: ", self.TOP_TRIGRAM_COUNT
        print "Word Bag: ", self.TOP_WORD_COUNT
        print "CB Training Len: ", len(self.clickbaitTrain)
        print "NCB Training Len: ", len(self.notClickbaitTrain)
        print "CB Test Len: ", len(self.clickbaitTest)
        print "NCB Test Len: ", len (self.notClickbaitTest)
        print "Validation Set: Not Clickbait used had a mean score < ", self.notClickbaitLowerbound
        print "Validation Set: Clickbait used had a mean score > ", self.clickbaitUpperbound

        Xtest = np.array(self.clickbaitTest + self.notClickbaitTest)
        Ytest = []
        for x in xrange(len(self.clickbaitTest)):
            Ytest.append(0)
        for x in xrange(len(self.notClickbaitTest)):
            Ytest.append(1)

        #NOTE: precision, recall, and F1 may report as 0 if predictions were poor. Lots of data and equal numbers in clickbait/not-clickbait are needed to avoid this.
        if statsPerFeature == True:
            self.writeStatsPerFeature(Xtrain, Xtest, Ytrain, Ytest, "training")
        else:
            #switched to LinearSVC instead of SVC due to poor performance
            linearclf = svm.LinearSVC(verbose=True)
            self.classifier_linear = CalibratedClassifierCV(linearclf)
            self.classifier_linear.fit(Xtrain, Ytrain)

            self.test_pred = self.classifier_linear.predict(Xtest)
            #print self.test_pred #NOTE: this prints out the classes for each headline. It is very big though.

            #print out predictions % for 0 - clickbait and 1 - not clickbait
            self.proba_pred = self.classifier_linear.predict_proba(Xtest)
            for x in xrange(1):
                print self.proba_pred[x], cbTestHeadlines[x]
                print self.clickbaitTest[x]
            for x in xrange(1):
                print self.proba_pred[x + len(self.clickbaitTest)], notCbTestHeadlines[x]
                print self.notClickbaitTest[x]

            #store the predictions
            self.npYtest = np.array(Ytest)

            self.classifierScore_SVM = "SVM Validation Test set score: {:.2f}".format(np.mean(self.test_pred == self.npYtest))
            print self.classifierScore_SVM

            self.precisionRecallScoreAndCurve("training_svm", self.npYtest, self.test_pred)

            self.errorsT1T2XLSX("t1t2errorstrainingSVM")

            if graphIndividualFeatures == True:
                self.graphIndividualFeatures(self.clickbaitTrain + self.clickbaitTest, self.notClickbaitTrain + self.notClickbaitTest, "training")

            if allClassifiers == True:
                self.createClassifiers("Training", Xtrain, Xtest, Ytrain)

    #get a min and max score for each feature to include these headlines in publications
    #the headline text is appended to the end of the row of preprocessed feature scores
    #hence the processedScoreRow[-1]. This needs to be refactored since it is messy.
    def getMinMaxPerFeature(self, headlines):
        self.featureExamplesMinHeadline = []
        self.featureExamplesMaxHeadline = []
        featureExamplesMin = []
        featureExamplesMax = []
        for x in xrange(len(self.featureNames) - self.TOP_TRIGRAM_COUNT - self.TOP_WORD_COUNT):
            featureExamplesMin.append(9999999999)
            featureExamplesMax.append(-9999999999)
            self.featureExamplesMinHeadline.append("")
            self.featureExamplesMaxHeadline.append("")
        for x in xrange(len(self.featureNames) - self.TOP_TRIGRAM_COUNT - self.TOP_WORD_COUNT):
            for processedScoreRow in headlines:
                #the min score for everything tends to go to the same short headline which gets 0 for all features
                #the and condition tries to use another one instead, a minimum that was not already used
                if processedScoreRow[x] < featureExamplesMin[x] and processedScoreRow[-1] + ", MinScore: " + str(processedScoreRow[x]) not in self.featureExamplesMinHeadline:
                    featureExamplesMin[x] = processedScoreRow[x]
                    self.featureExamplesMinHeadline[x] = processedScoreRow[-1] + ", MinScore: " + str(processedScoreRow[x])
                if processedScoreRow[x] > featureExamplesMax[x]:
                    featureExamplesMax[x] = processedScoreRow[x]
                    self.featureExamplesMaxHeadline[x] = processedScoreRow[-1] + ", MaxScore: " + str(processedScoreRow[x])

    #use a training and test set from the challenge validation set and optionally the large 30000 one
    def trainSVMAndTestValidationSet(self, allClassifiers=False, graphIndividualFeatures=False, statsPerFeature=False):
        print "Running VALIDATION set..."
        clickbaitValidation = self.buildValidationClickbaitSet()
        self.clickbaitValidationTrain, self.clickbaitValidationTest = train_test_split(clickbaitValidation, train_size = self.trainSize)
        notClickbaitValidation = self.buildValidationNonClickbaitSet()
        self.notClickbaitValidationTrain, self.notClickbaitValidationTest = train_test_split(notClickbaitValidation, train_size = self.trainSize)

        self.getMinMaxPerFeature(clickbaitValidation + notClickbaitValidation)

        #kind of poor fix to print the text headline with the classifier prediction value and get the truth mean
        #we basically just add it to the end of the feature scores list, then reorganize it here and delete it from the feature scores
        cbTestHeadlines = []
        notCbTestHeadlines = []
        cbTestTruthMeans = []
        notCbTestTruthMeans = []
        for row in self.clickbaitValidationTrain:
            del row[len(row) - 1]
            del row[len(row) - 1]
        for row in self.notClickbaitValidationTrain:
            del row[len(row) - 1]
            del row[len(row) - 1]
        for row in self.clickbaitValidationTest:
            cbTestHeadlines.append(row[len(row) - 1])
            cbTestTruthMeans.append(row[len(row) - 2])
            del row[len(row) - 1]
            del row[len(row) - 1]
        for row in self.notClickbaitValidationTest:
            notCbTestHeadlines.append(row[len(row) - 1])
            notCbTestTruthMeans.append(row[len(row) - 2])
            del row[len(row) - 1]
            del row[len(row) - 1]

        #added for type 1/2 errors - TODO: refactor
        self.testedHeadlines = cbTestHeadlines + notCbTestHeadlines

        XtestValidate = np.array(clickbaitValidation + notClickbaitValidation)
        YtestValidate = []

        for x in xrange(len(clickbaitValidation)):
            YtestValidate.append(0)
        for x in xrange(len(notClickbaitValidation)):
            YtestValidate.append(1)

        Xtrain = np.array(self.clickbaitValidationTrain + self.notClickbaitValidationTrain)
        Ytrain = []

        #y labels are the same length as sample and represent their class
        #0 - clickbait
        #1 - not clickbait
        for x in xrange(len(self.clickbaitValidationTrain)):
            Ytrain.append(0)
        for x in xrange(len(self.notClickbaitValidationTrain)):
            Ytrain.append(1)

        print "Feature count: ", len(self.featureNames)
        print "Trigram Bag: ", self.TOP_TRIGRAM_COUNT
        print "Word Bag: ", self.TOP_WORD_COUNT
        print "Validation Set: Not Clickbait used had a mean score < ", self.notClickbaitLowerbound
        print "Validation Set: Clickbait used had a mean score > ", self.clickbaitUpperbound
        print "CB Validation Training Len: ", len(self.clickbaitValidationTrain)
        print "NCB Validation Training Len: ", len(self.notClickbaitValidationTrain)
        print "CB Validation Test Len: ", len(self.clickbaitValidationTest)
        print "NCB Validation Test Len: ", len(self.notClickbaitValidationTest)

        Xtest = np.array(self.clickbaitValidationTest + self.notClickbaitValidationTest)
        Ytest = []
        for x in xrange(len(self.clickbaitValidationTest)):
            Ytest.append(0)
        for x in xrange(len(self.notClickbaitValidationTest)):
            Ytest.append(1)

        #NOTE: precision, recall, and F1 may report as 0 if predictions were poor. Lots of data and equal numbers in clickbait/not-clickbait are needed to avoid this.
        if statsPerFeature == True:
            self.writeStatsPerFeature(Xtrain, Xtest, Ytrain, Ytest, "validation")
        else:
            #not quite so sure why but the SVC is very slow now - switched to LinearSVC to improve speed/scale
            linearclf = svm.LinearSVC(class_weight=None,verbose=1,max_iter=2000)
            self.classifier_linear = CalibratedClassifierCV(linearclf)
            self.classifier_linear.fit(Xtrain, Ytrain)

            self.test_pred = self.classifier_linear.predict(Xtest)
            #print self.test_pred #NOTE: this prints out the classes for each headline - it is very big though.

            #print out predictions % for 0 - clickbait and 1 - not clickbait
            self.proba_pred = self.classifier_linear.predict_proba(Xtest)
            clickbaitScore = []
            for x in xrange(len(self.clickbaitValidationTest)):
                clickbaitScore.append(self.proba_pred[x].item(0))
            for x in xrange(len(self.notClickbaitValidationTest)):
                clickbaitScore.append(self.proba_pred[x + len(self.clickbaitValidationTest)].item(0))

            #compute the mean squared error (this simulates we were doing regression... may give a rough performance indicator compared to 2017 challenge entries)
            print "Simulated [and inaccurate] Test Set MEAN SQUARED ERROR (MSE): ", mean_squared_error(cbTestTruthMeans + notCbTestTruthMeans, clickbaitScore)

            #store the predictions
            self.npYtest = np.array(Ytest)

            self.classifierScore_SVM = "SVM Validation Test set score: {:.2f}".format(np.mean(self.test_pred == self.npYtest))
            print self.classifierScore_SVM

            self.precisionRecallScoreAndCurve("validation_svm", self.npYtest, self.test_pred)
            self.errorsT1T2XLSX("t1t2errorsvalidationSVM")

            self.testAllOfValidationSet()

            if graphIndividualFeatures == True:
                self.graphIndividualFeatures(self.clickbaitValidationTrain + self.clickbaitValidationTest, self.notClickbaitValidationTrain + self.notClickbaitValidationTest, "validation")

            if allClassifiers == True:
                self.createClassifiers("Validation", Xtrain, Xtest, Ytrain)

    def writeStatsPerFeature(self, Xtrain, Xtest, Ytrain, Ytest, setname):
        h = HTML()
        h.h1("Precision-Recall Table")
        h.h3("Note that for minimum feature score headlines the program tries to use a DIFFERENT minimum headline for each feature, otherwise the same one usually ends up as the minimum for all features.")
        h.br()
        #table of internal links for the report
        t = h.table(border='1')
        r = t.tr
        r.td("Feature Name")
        r.td("Precision Score")
        r.td("Recall Score")
        r.td("F1-Score")
        r.td("Average Correctly Classified (" + " number of headlines)")
        r.td("Minimum Scoring Headline")
        r.td("Maximum Scoring Headline")

        for x in xrange(len(self.featureNames) - self.TOP_TRIGRAM_COUNT - self.TOP_WORD_COUNT):
            linearclf = svm.LinearSVC(class_weight=None,verbose=0,max_iter=2000)
            self.classifier_linear = CalibratedClassifierCV(linearclf)
            trainFeatureScores = Xtrain[:,[x]]
            self.classifier_linear.fit(trainFeatureScores, Ytrain)
            testFeatureScores = Xtest[:,[x]]
            self.test_pred = self.classifier_linear.predict(testFeatureScores)
            #store the predictions
            self.npYtest = np.array(Ytest)
            self.classifierScore_SVM = self.featureNames[x] + " correct prediction mean: {:.4f}".format(np.mean(self.test_pred == self.npYtest))
            print self.classifierScore_SVM
            print self.featureNames[x] + " precision: ", precision_score(self.npYtest, self.test_pred)
            print self.featureNames[x] + " recall: ", recall_score(self.npYtest, self.test_pred)
            print self.featureNames[x] + " f1-score: ", f1_score(self.npYtest, self.test_pred)
            r = t.tr
            r.td(self.featureNames[x])
            r.td(str(round(precision_score(self.npYtest, self.test_pred), 4)))
            r.td(str(round(recall_score(self.npYtest, self.test_pred), 4)))
            r.td(str(round(f1_score(self.npYtest, self.test_pred), 4)))
            r.td(str(round(np.mean(self.test_pred == self.npYtest), 4)))
            r.td(self.featureExamplesMinHeadline[x].encode('ascii', 'ignore'))
            r.td(self.featureExamplesMaxHeadline[x].encode('ascii', 'ignore'))
            h.br()
        f = open("plots_features/" + setname + "_feature_stats.html", "w")
        f.write(unicode(h))
        f.close()

    #call this method and pass in a relevant file name for precision-recall information
    def precisionRecallScoreAndCurve(self, filename, test, score):
        #TODO
        return

    def createClassifiers(self, name, Xtr_r, Xte_r, Ytrain, randomForest=True, KNN=True, NB=True):
        if randomForest == True:
            self.classifierRndForest = RandomForestClassifier(verbose=True)
            self.classifierRndForest.fit(Xtr_r, Ytrain)
            otherClassifierTestPred = self.classifierRndForest.predict(Xte_r)
            print "Random Forest " + name + " Test set score: {:.2f}".format(np.mean(otherClassifierTestPred == self.npYtest))
            self.precisionRecallScoreAndCurve(name + "_randomforest", self.npYtest, otherClassifierTestPred)

        if KNN == True:
            self.classifierKNN = KNeighborsClassifier(n_neighbors=175)
            self.classifierKNN.fit(Xtr_r, Ytrain)
            otherClassifierTestPred = self.classifierKNN.predict(Xte_r)
            print "K-Nearest Neighbour " + name + " Test set score: {:.2f}".format(np.mean(otherClassifierTestPred == self.npYtest))
            self.precisionRecallScoreAndCurve(name + "_knn", self.npYtest, otherClassifierTestPred)

        if NB == True:
            self.classifierNaiveBayes = GaussianNB()
            self.classifierNaiveBayes.fit(Xtr_r, Ytrain)
            otherClassifierTestPred = self.classifierNaiveBayes.predict(Xte_r)
            print "Naive Bayes " + name + " Test set score: {:.2f}".format(np.mean(otherClassifierTestPred == self.npYtest))
            self.precisionRecallScoreAndCurve(name + "_naivebayes", self.npYtest, otherClassifierTestPred)

    #primarily for the ganguly set, for now, but you can use any headline
    #0 - clickbait, 1 - not clickbait
    def predictClass(self, headline):
        setToProcess = [{'text':headline, 'truth-mean': 0.0}]
        Xsamples = self.processHeadlines(setToProcess, verbose=False)
        #bad fix for keeping track of headline text and truth mean
        for row in Xsamples:
            del row[len(row) - 1]
            del row[len(row) - 1]
        prob = self.classifier_linear.predict(Xsamples)
        return prob[0].item() #numpy lingo

    #test accuracy on the ganguly set
    #TODO: refactor me
    def testGangulySet(self):
        amtClickbaitCorrect = 0
        amtClickbait = len(self.th.gangulyClickbait)
        amtNotClickbaitCorrect = 0
        amtNotClickbait = len(self.th.gangulyNoClickbait)

        for headline in self.th.gangulyClickbait:
            if self.predictClass(headline['text']) == 0:
                amtClickbaitCorrect = amtClickbaitCorrect + 1

        for headline in self.th.gangulyNoClickbait:
            if self.predictClass(headline['text']) == 1:
                amtNotClickbaitCorrect = amtNotClickbaitCorrect + 1

        cbAcc = float(amtClickbaitCorrect)/float(amtClickbait)
        ncbAcc = float(amtNotClickbaitCorrect)/float(amtNotClickbait)
        totalAcc = float(amtClickbaitCorrect + amtNotClickbaitCorrect) / float(amtClickbait + amtNotClickbait)

        print "Ganguly Clickbait Amt: ", amtClickbait
        print "Ganguly Not Clickbait Amt: ", amtNotClickbait
        print "Ganguly Clickbait Correct: ", amtClickbaitCorrect
        print "Ganguly Not Clickbait Correct: ", amtNotClickbaitCorrect
        print "Ganguly TOTAL: ", amtClickbait + amtNotClickbait
        print "Ganguly Clickbait Accuracy: ", cbAcc
        print "Ganguly Not Clickbait Accuracy: ", ncbAcc
        print "Ganguly Overall: ", totalAcc

    #Use the test set from the challenge with this function to get a better idea of MSE, still not sure about accuracy though
    def testAllOfValidationSet(self):
        amtClickbaitCorrect = 0
        amtClickbait = len(self.th.validationAllClickbait)
        amtNotClickbaitCorrect = 0
        amtNotClickbait = len(self.th.validationAllNotClickbait)

        print "Validation All Not Clickbait Amt: ", amtNotClickbait
        print "Validation All Clickbait Amt: ", amtClickbait
        print "Validation All TOTAL: ", amtClickbait + amtNotClickbait

        allTruthMeans = []
        predictedTruthMeans = []

        for h in self.th.validationAllClickbait:
            headline = h['text']
            truthMean = h['truth-mean']
            if self.predictClass(headline) == 0:
                amtClickbaitCorrect = amtClickbaitCorrect + 1
            allTruthMeans.append(truthMean)
            predictedTruthMeans.append(self.predict(headline, False, True))

        for h in self.th.validationAllNotClickbait:
            headline = h['text']
            truthMean = h['truth-mean']
            if self.predictClass(headline) == 1:
                amtNotClickbaitCorrect = amtNotClickbaitCorrect + 1
            allTruthMeans.append(truthMean)
            predictedTruthMeans.append(self.predict(headline, False, True))

        #compute the mean squared error (this simulates we were doing regression... may give a rough performance indicator compared to 2017 challenge entries)
        print "Simulated [and inaccurate] MEAN SQUARED ERROR (MSE) ALL VALIDATION: ", mean_squared_error(allTruthMeans, predictedTruthMeans)

        cbAcc = float(amtClickbaitCorrect)/float(amtClickbait)
        ncbAcc = float(amtNotClickbaitCorrect)/float(amtNotClickbait)
        totalAcc = float(amtClickbaitCorrect + amtNotClickbaitCorrect) / float(amtClickbait + amtNotClickbait)

        print "Validation All Clickbait Correct: ", amtClickbaitCorrect
        print "Validation All Not Clickbait Correct: ", amtNotClickbaitCorrect
        print "Validation All Clickbait Accuracy: ", cbAcc
        print "Validation All Not Clickbait Accuracy: ", ncbAcc
        print "Validation All Overall: ", totalAcc

    #TODO: refactor
    def predict(self, headline, verbose=True, quick=False):
        setToProcess = [{'text':headline, 'truth-mean':0.0}]
        Xsamples = self.processHeadlines(setToProcess, verbose=verbose)
        #bad fix for keeping track of headline text, truth-mean
        for row in Xsamples:
            del row[len(row) - 1]
            del row[len(row) - 1]
        prob = self.classifier_linear.predict_proba(Xsamples)

        if quick == True:
            return prob.item(0)

        #verbose should be false for the browser
        if verbose == False:
            betterString = str(prob[0])[1:-1]
            classValues = betterString.split(" ")
            classValues = filter(None, classValues) # fastest
            return ",".join(classValues) + "," + ",".join(str(featScore) for featScore in Xsamples[0][:38]) + "," + headline

        additionalMessage = "This link is "

        #details about clickbait score (class 0)
        if prob[0][0] > 0.90:
            additionalMessage = additionalMessage + "very likely to be direct clickbait "
        elif prob[0][0] > 0.65:
            additionalMessage = additionalMessage + "likely to be direct clickbait "
        elif prob[0][0] > 0.30:
            additionalMessage = additionalMessage + "moderately clickbaiting "
        elif prob[0][0] > 0.10:
            additionalMessage = additionalMessage + "marginally clickbaiting "
        else:
            additionalMessage = additionalMessage + " not clickbaiting "

        additionalMessage = additionalMessage + "and "

        if verbose == True:
            print type(prob[0][0])
            print type(prob[0][1])

        #details about legitimacy score (class 1)
        if prob[0][1] > 0.90:
            additionalMessage = additionalMessage + "accurately describes the article."
        elif prob[0][1] > 0.65:
            additionalMessage = additionalMessage + "mostly describes the article."
        elif prob[0][1] > 0.30:
            additionalMessage = additionalMessage + "marginally describes the article."
        elif prob[0][1] > 0.10:
            additionalMessage = additionalMessage + "does not or barely describes the article."
        else:
            additionalMessage = additionalMessage + "does not provide any information about the article."

        return str(prob[0]) + " " + additionalMessage

    #type 1/2 error grid
    def errorsT1T2XLSX(self, filename):
        Ytest = self.npYtest.tolist()
        lstTestPred = self.test_pred.tolist()
        list1 = []
        list2 = []
        list3 = []
        list4 = []

        for x in xrange(len(lstTestPred)):
            #square row1col1
            #clickbait, labelled clickbait (+, good)
            if lstTestPred[x] == 0 and Ytest[x] == 0:
                list1.append(self.testedHeadlines[x]  + " " +  str(self.proba_pred[x]))

            #square row1col2
            #legitimate headlines, labelled clickbait (-,bad)
            elif lstTestPred[x] == 0 and Ytest[x] == 1:
                list2.append(self.testedHeadlines[x]  + " " +  str(self.proba_pred[x]))

            #square row2col1
            #clickbait, labelled legitimate headlines (-,bad)
            elif lstTestPred[x] == 1 and Ytest[x] == 0:
                list3.append(self.testedHeadlines[x] + " " + str(self.proba_pred[x]))

            #square row2col2
            #legitimate headlines, labelled legitimate headlines (+, good)
            elif lstTestPred[x] == 1 and Ytest[x] == 1:
                list4.append(self.testedHeadlines[x]  + " " +  str(self.proba_pred[x]))

        workbook = xlsxwriter.Workbook(filename + ".xlsx")
        worksheet = workbook.add_worksheet()

        worksheet.set_column('A:D', 100)

        worksheet.write(0, 0, "clickbait, labelled clickbait (+, good)")
        for x in xrange(len(list1)):
            worksheet.write(x + 1, 0, list1[x])

        self.classifierScore_T1T2Good_CBCB = "length of clickbait identified as clickbait (+,good): " + str(len(list1)) + self.getPercent(len(list1), len(list1) + len(list3))
        print self.classifierScore_T1T2Good_CBCB

        worksheet.write(0, 1, "legitimate headlines, labelled clickbait (-,bad)")
        for x in xrange(len(list2)):
            worksheet.write(x + 1, 1, list2[x])

        self.classifierScore_T1T2Bad_LegitCB = "length of legit headlines identified as clickbait (-,bad): " + str(len(list2)) + self.getPercent(len(list2), len(list2) + len(list4))
        print self.classifierScore_T1T2Bad_LegitCB

        worksheet.write(0, 2, "clickbait, labelled legitimate headlines (-,bad)")
        for x in xrange(len(list3)):
            worksheet.write(x + 1, 2, list3[x])

        self.classifierScore_T1T2Bad_CBLegit = "length of clickbait identified as legit headlines (-,bad): " + str(len(list3)) + self.getPercent(len(list3), len(list1) + len(list3))
        print self.classifierScore_T1T2Bad_CBLegit

        worksheet.write(0, 3, "legitimate headlines, labelled legitimate headlines (+, good)")
        for x in xrange(len(list4)):
            worksheet.write(x + 1, 3, list4[x])

        self.classifierScore_T1T2Good_LegitLegit = "length of legit headlines identified as legit headlines (+,good): " + str(len(list4)) + self.getPercent(len(list4), len(list2) + len(list4))
        print self.classifierScore_T1T2Good_LegitLegit

    def getPercent(self, amt, totalAmt):
        result =  (float(amt) / float(totalAmt)) * 100
        return  " / " + str(totalAmt) + " (" + str(result) + "%)"