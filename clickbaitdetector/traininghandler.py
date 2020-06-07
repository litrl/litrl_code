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
# Name:        traininghandler.py
# Purpose:     class to load and access file data - clickbait challenge set, swearing, etc
#
# Created:     May 2017
#
# Language and Information Technology Research Lab
# Faculty of Information and Media Studies (FIMS)
# University of Western Ontario, London, Canada
#-------------------------------------------------------------------------------

import io
import codecs
import json_lines

#load the training set from the clickbait challenge
class TrainingHandler:

    def __init__(self):
        self.setupClickbaitCollections()
        self.loadGanguly()

    def __init__(self, validation, notClickbaitScoreUpperbound, clickbaitScoreLowerbound, includeValidationSet=True, includeGangulySet=False):
        self.notClickbaitScoreUpperbound = notClickbaitScoreUpperbound
        self.clickbaitScoreLowerbound = clickbaitScoreLowerbound
        self.setupClickbaitCollections()
        #added this flag to skip over the validation set
        if includeValidationSet == True:
            self.loadTruthJSONValidation("truth.jsonl")
            self.loadDetailsJSONValidation("instances.jsonl")
        if includeGangulySet == True:
            self.loadGanguly("./ganguly-stop-clickbait/clickbait_data", "./ganguly-stop-clickbait/non_clickbait_data")

    def setupClickbaitCollections(self):
        print("Loading training sets.")
        self.validationSet = {}
        self.validationSetNoClickbait = []
        self.validationSetClickbait = []
        self.validationAllClickbait = []
        self.validationAllNotClickbait = []
        self.gangulyClickbait = []
        self.gangulyNoClickbait = []

    def loadTruthJSONValidation(self, filename):
        print("Opening Clickbait Challenge 2017 VALIDATION truth file.")
        with open(filename, 'rb') as f:
            for item in json_lines.reader(f):
                self.validationSet[item['id']] = {'truth-mean': item['truthMean'], 'truth': item['truthClass'], 'text': '', 'id': item['id']}
        print("Finished reading truth file.")

    def loadDetailsJSONValidation(self, filename):
        print("Opening Clickbait Challenge 2017 VALIDATION details file.")
        with open(filename, 'rb') as f:
            i = 0
            for item in json_lines.reader(f):
                self.validationSet[item['id']]['text'] = item['postText'][0] #this is a list for some reason
                #use the truthmean here as the data in the middle (people weren't sure if this was or was not clickbait) causes issues
                #the values used here significantly affect the performance of the detector
                #see truth-means.txt for previously used values and results
                if float(self.validationSet[item['id']]['truth-mean']) < self.notClickbaitScoreUpperbound:
                    self.validationSetNoClickbait.append(self.validationSet[item['id']])
                elif float(self.validationSet[item['id']]['truth-mean']) > self.clickbaitScoreLowerbound:
                    self.validationSetClickbait.append(self.validationSet[item['id']])

                #the stuff in the middle (suspected that training with it is bad)
                #there is a method in clickbait.ml that will test with these headlines
                if float(self.validationSet[item['id']]['truth-mean']) < 0.50:
                    self.validationAllNotClickbait.append(self.validationSet[item['id']])
                elif float(self.validationSet[item['id']]['truth-mean']) > 0.50:
                    self.validationAllClickbait.append(self.validationSet[item['id']])

                i = i + 1

        print("Finished reading details file.")
        print("Attempting to use equal numbers of clickbait/not clickbait.")
        self.validationSetNoClickbait = self.validationSetNoClickbait[0:len(self.validationSetClickbait)]
        print("VALIDATION TRAIN/TEST CLICKBAIT LENGTH: ", len(self.validationSetClickbait))
        print("VALIDATION TRAIN/TEST NOT CLICKBAIT LENGTH: ", len(self.validationSetNoClickbait))
        print("VALIDATION ALL CLICKBAIT LENGTH: ", len(self.validationAllClickbait))
        print("VALIDATION ALL NOT CLICKBAIT LENGTH: ", len(self.validationAllNotClickbait))
        print("The Clickbait Challenge 2017 VALIDATION set (14000) includes truth-mean values in the range 0.0-1.0.")

    def loadGanguly(self, clickbaitFilename, noClickbaitFilename):
        print("Opening Ganguly (Large 300000) training set files.")
        with io.open(clickbaitFilename, 'r', encoding="utf-8") as cb:
            lines = (line.rstrip() for line in cb)
            gangulyClickbaitTmp = list(line for line in lines if line != "")
            for x in range(len(gangulyClickbaitTmp)):
                newGangulyHeadline = {}
                newGangulyHeadline['text'] = gangulyClickbaitTmp[x]
                newGangulyHeadline['truth-mean'] = 1.0 #in this set, you are either clickbait or you are not
                self.gangulyClickbait.append(newGangulyHeadline)
        with io.open(noClickbaitFilename, 'r', encoding="utf-8") as ncb:
            lines = (line.rstrip() for line in ncb)
            gangulyNoClickbaitTmp = list(line for line in lines if line != "")
            for x in range(len(gangulyNoClickbaitTmp)):
                newGangulyHeadline = {}
                newGangulyHeadline['text'] = gangulyNoClickbaitTmp[x]
                newGangulyHeadline['truth-mean'] = 0.0 #in this set, you are either clickbait or you are not
                self.gangulyNoClickbait.append(newGangulyHeadline)
        print("GANGULY CLICKBAIT LENGTH: ", len(self.gangulyClickbait))
        print("GANGULY NOTCLICKBAIT LENGTH: ", len(self.gangulyNoClickbait))
        print("The Ganguly (Large) set (30000) only includes binary classes (clickbait, or not clickbait).")
