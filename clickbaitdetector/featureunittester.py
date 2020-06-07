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
# Name:        feature unit tester
# Purpose:     verify that feature preprocessing functions actually work
#              This has been unused since early in the project but would be good
#              to update.
#
# Created:     20/06/2017
#
# Language and Information Technology Research Lab
# Faculty of Information and Media Studies (FIMS)
# University of Western Ontario, London, Canada
#-------------------------------------------------------------------------------

import sys
import traceback
from clickbaitml import clickbaitDetector
from pattern.en import parsetree, ngrams, modality, mood, sentiment

class featureUnitTester:

    def __init__(self):
        #create an instance of our clickbait detector
        #skipGetNumbersSum will prevent getNumbersSum from summing anything that could be a number in english, sometimes slow
        skipGetNumbersSum = False

        #set to 0 to prevent using most common word list as features
        topWordsFeatureCount = 100
        #set to 0 to prvent using most common word trigrams as features
        topWordTrigramFeatureCount = 50
        self.clickbaitDetector = clickbaitDetector(skipGetNumbersSum, topWordsFeatureCount, topWordTrigramFeatureCount)

        #TODO: include a wide range of headlines, including some less vulgar
        #for the unit tests, we need headlines and manually determined correct values for each feature
        testCase = "RT The world's 10 most \"advanced sex\" dolls will soon be able to think and talk"
        #"getNumbersSum" : 10.0 #this is excluded since getNumbersSum may be disabled
        testValues = {
            "getWordCount" : 15,
            "getHashTagsAndRTs" : 1,
            "getQuestionMarks": 0,
            "getAtMentions" : 0,
            "getCharLength" : len(testCase),
            "getNNPLOCCount" : 0,
            "getNNPPERSCount" : 0,
            "getSwearCount" : 2,
            "maxDistToQuote" : 31,
            "maxDistToNNP": 0,
            "getNumbersSum" : 0.0
        }

        patternParseTree = parsetree(testCase, tokenize=True, tags=True, chunks=True, relations=True, lemmata=True)
        strSentenceText = testCase
        lstSentPOS = []
        lstSentWords = []
        for sentence in patternParseTree:
            for chunk in sentence.chunks:
                for word in chunk.words:
                    lstSentPOS.append(word.type)
                    lstSentWords.append(word.string)

        #call unit tests here
        try:
            self.assertMaxDistToNNP(lstSentPOS, lstSentWords, testValues)
            self.assertMaxDistToQuote(strSentenceText, testValues)
            self.assertGetWordCount(lstSentWords, testValues)
            self.assertGetHashTagsAndRTs(strSentenceText, lstSentWords, testValues)
            self.assertGetQuestionMarks(strSentenceText, testValues)
            self.assertGetAtMentions(strSentenceText, testValues)
            self.assertGetNumbersSum(lstSentWords, testValues)
            self.assertGetNNPPERSCount(lstSentPOS, testValues)
            self.assertGetSwearCount(lstSentWords, testValues)
            self.assertGetNNPLOCCount(lstSentPOS, testValues)
            self.assertGetCharLength(strSentenceText, testValues)
            print("Clickbait detector has passed all Unit Tests!")
        except AssertionError as e:
            print(e.args) #print the "args" part of assertionError, showing expected values
            exit(1)

    #self.getWordCount(lstSentWords)
    def assertGetWordCount(self, lstSentWords, testValues):
        testName = "getWordCount"
        result = self.clickbaitDetector.getWordCount(lstSentWords)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.getWord2Grams(strSentenceText)
    def assertGetWord2Grams(self, strSentenceText, testValues):
        testName = "getWord2Grams"
        result = self.clickbaitDetector.getWord2Grams(strSentenceText)
        assert result is type(testValues[testName])
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.getWord3Grams(strSentenceText)
    def assertGetWord3Grams(self, strSentenceText, testValues):
        testName = "getWord3Grams"
        result = self.clickbaitDetector.getWord3Grams(strSentenceText)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.getChar2Grams(lstSentWords)
    def assertGetChar2Grams(self, lstSentWords, testValues):
        testName = "getWord2Grams"
        result = self.clickbaitDetector.getWord2Grams(lstSentWords)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.getChar3Grams(lstSentWords)
    def assertGetChar3Grams(self, lstSentWords, testValues):
        testName = "getWord3Grams"
        result = self.clickbaitDetector.getWord3Grams(lstSentWords)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.getHashTagsAndRTs(strSentenceText, lstSentWords)
    def assertGetHashTagsAndRTs(self, strSentenceText, lstSentWords, testValues):
        testName = "getHashTagsAndRTs"
        result = self.clickbaitDetector.getHashTagsAndRTs(strSentenceText,lstSentWords)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.getQuestionMarks(strSentenceText)
    def assertGetQuestionMarks(self, strSentenceText, testValues):
        testName = "getQuestionMarks"
        result = self.clickbaitDetector.getQuestionMarks(strSentenceText)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.getAtMentions(strSentenceText)
    def assertGetAtMentions(self, strSentenceText, testValues):
        testName = "getAtMentions"
        result = self.clickbaitDetector.getAtMentions(strSentenceText)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.getNumbersSum(lstSentWords)
    def assertGetNumbersSum(self, lstSentWords, testValues):
        testName = "getNumbersSum"
        result = self.clickbaitDetector.getNumbersSum(lstSentWords)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.minDistToNNP(lstSentPOS, lstSentWords)
    def assertMinDistToNNP(self, lstSentPOS, lstSentWords, testValues):
        testName = "minDistToNNP"
        result = self.clickbaitDetector.minDistToNNP(lstSentPOS, lstSentWords)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName]

    #self.maxDistToNNP(lstSentPOS, lstSentWords) #s
    def assertMaxDistToNNP(self, lstSentPOS, lstSentWords, testValues):
        testName = "maxDistToNNP"
        result = self.clickbaitDetector.maxDistToNNP(lstSentPOS, lstSentWords)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.getNNPLOCCount(lstSentPOS)
    def assertGetNNPLOCCount(self, lstSentPOS, testValues):
        testName = "getNNPLOCCount"
        result = self.clickbaitDetector.getNNPLOCCount(lstSentPOS)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.getNNPPERSCount(lstSentPOS)
    def assertGetNNPPERSCount(self, lstSentPOS, testValues):
        testName = "getNNPPERSCount"
        result = self.clickbaitDetector.getNNPPERSCount(lstSentPOS)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.getSwearCount(lstSentWords) #s
    def assertGetSwearCount(self, lstSentWords, testValues):
        testName = "getSwearCount"
        result = self.clickbaitDetector.getSwearCount(lstSentWords)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.getAdjpCount(lstSentPOS)
    def assertGetAdjpCount(self, lstSentPOS, testValues):
        testName = "getAdjpCount"
        result = self.clickbaitDetector.getAdjpCount(lstSentPOS)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.getAdvpCount(lstSentPOS)
    def assertGetAdvpCount(self, lstSentPOS, testValues):
        testName = "getAdvpCount"
        result = self.clickbaitDetector.getAdvpCount(lstSentPOS)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.getNNPCount(lstSentPOS)
    def assertGetNNPCount(self, lstSentPOS, testValues):
        testName = "getNNPCount"
        result = self.clickbaitDetector.getNNPCount(lstSentPOS)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.getVerbCount(lstSentPOS)
    def assertGetVerbCount(self, lstSentPOS, testValues):
        testName = "getVerbCount"
        result = self.clickbaitDetector.getVerbCount(lstSentPOS)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.getNPs(lstSentPOS)
    def assertGetNPCount(self, lstSentPOS, testValues):
        testName = "getNPCount"
        result = self.clickbaitDetector.getNPCount(lstSentPOS)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.avgDistToNNP(lstSentPOS, lstSentWords)
    def assertAvgDistToNNP(self, lstSentPOS, lstSentWords, testValues):
        testName = "avgDistToNNP"
        result = self.clickbaitDetector.getNPCount(lstSentPOS, lstSentWords)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.getCharLength(strSentenceText)
    def assertGetCharLength(self, strSentenceText, testValues):
        testName = "getCharLength"
        result = detector.getCharLength(strSentenceText)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.getPronounCount(lstSentPOS)
    def assertGetNPCount(self, lstSentPOS, testValues):
        testName = "getPronounCount"
        result = self.clickbaitDetector.getPronounCount(lstSentPOS)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.getModality(strSentenceText)            #TODO.

    #self.getEmotiveness(f12, f13, f16, f15)      #Emotiveness - TODO. Not sure if these is easy to test. Probably have to round the result.

    #self.getTimeWordsCount(lstSentWords)         #This should be fine.
    #self.getAcademicWordsCount(lstSentWords)     #This should be fine.

    #self.getFirstNNPPos(lstSentPOS)
    def assertGetFirstNNPPos(self, lstSentPOS, testValues):
        testName = "getFirstNNPPos"
        result = self.clickbaitDetector.getFirstNNPPos(lstSentPOS)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.startsWithNumber(lstSentWords)
    def assertStartsWithNumber(self, lstSentWords, testValues):
        testName = "startsWithNumber"
        result = self.clickbaitDetector.startsWithNumber(lstSentWords)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.assertMaxDistToQuote
    def assertMaxDistToQuote(self, lstSentWords, testValues):
        testName = "maxDistToQuote"
        result = self.clickbaitDetector.maxDistToQuote(lstSentWords)
        assert type(result) is type(testValues[testName]), {"ResultType: " : type(result), "ExpectedType: " : type(testValues[testName])}
        assert result == testValues[testName], {"Result: " : result, "Expected: " : testValues[testName]}

    #self.getTrainingClickbaitSimilarity(strSentenceText) #TODO. This one needs some work so test later.

tester = featureUnitTester()