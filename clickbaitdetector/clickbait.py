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
# Name:        clickbait
# Purpose:     main program for clickbait
#              can run this if you are working on the clickbait detector to test
#              additionally you need to run this module to generate the detector
#              pickle file, which is used by the browser for clickbait detection
#
# Created:     02/07/2017
#
# Language and Information Technology Research Lab
# Faculty of Information and Media Studies (FIMS)
# University of Western Ontario, London, Canada
#-------------------------------------------------------------------------------

import dill
import cProfile, pstats, io
from clickbaitml import clickbaitDetector

#interestingly, even though the detector performs OK on a training/test set
#it is not in-line with one of our own validation sets. Results get MUCH better if we add the large 30000 set.
def testYiminSet(detector):
    cbHeadlineFile = open("CB_Headlines.sta", "r")
    notCbHeadlineFile = open("Not_CB_Headlines.sta", "r")
    cbHeadlines = cbHeadlineFile.readlines()
    notCbHeadlines = notCbHeadlineFile.readlines()

    #type 1 type 2 errors
    goodCB = 0
    badCB = 0
    goodNotCB = 0
    badNotCB = 0

    resultsFile = open("yimin_results.csv", "w")
    for x in range(len(cbHeadlines)):
        ranking = detector.predict(str(cbHeadlines[x], errors='ignore'), verbose=False)
        group = detector.predictClass(str(cbHeadlines[x], errors='ignore'))
        if group == 0:
            goodCB = goodCB + 1
        else:
            badCB = badCB + 1
        resultsFile.write(ranking)
    for x in range(len(notCbHeadlines)):
        ranking = detector.predict(str(notCbHeadlines[x], errors='ignore'), verbose=False)
        group = detector.predictClass(str(notCbHeadlines[x], errors='ignore'))
        if group == 1:
            goodNotCB = goodNotCB + 1
        else:
            badNotCB = badNotCB + 1
        resultsFile.write(ranking)
    cbHeadlineFile.close()
    notCbHeadlineFile.close()
    resultsFile.close()
    print("Yimin Study - Clickbait identified as clickbait (+,good): ", goodCB)
    print("Yimin Study - Clickbait identified as legitimate (-,bad): ", badCB)
    print("Yimin Study - Clickbait TOTAL: ", len(cbHeadlines))
    print("Yimin Study - Legit identified as Legit (+,good): ", goodNotCB)
    print("Yimin Study - Legit identified as clickbait (-,bad): ", badNotCB)
    print("Yimin Study - Legit TOTAL: ", len(notCbHeadlines))
    print("Yimin Study - Accuracy: ", float(goodCB + goodNotCB) / float(goodCB + badCB + goodNotCB + badNotCB))

def main():
    #set to 0 to prevent using most common word list as features
    topWordsFeatureCount = 125
    #set to 0 to prvent using most common word trigrams as features
    topWordTrigramFeatureCount = 75

    pr = cProfile.Profile()
    pr.enable()

    #set featureStats = True to get individual feature performance
    featureStats = False

    #create an instance of our clickbait detector
    #the last two parameters are regarding the challenge training set truth-mean scores
    #any score below the first parameter is clickbait and any score above the second parameter is not clickbait
    #we can change these values to alter how we train our SVM
    #challenge training set: using only < 0.10 for clickbait and above 0.6 for not clickbait
    #challenge validation set: < 0.10 for clickbait, > 0.60 for not-clickbait, with bags of things, gets high accuracy.
    #ganguly set is just binary classification
    #leads to good classification results, but poor results compared to our qualitative study.
    detector = clickbaitDetector(topWordsFeatureCount, topWordTrigramFeatureCount, includeValidationSet=True, includeGangulySet=True, notClickbaitLowerbound=0.10, clickbaitUpperbound=0.6, buildBagOfWords=True, buildBagOfTrigrams=True, trainSize = 0.7)

    #NOTE: only TRAIN with ONE challenge set, then test or predict as much as you want
    #set GraphIndividualFeatures=False to speed things up (but you won't get a performance report)
    #set allClassifiers=False to only use LinearSVM not the KNN, Random Forest, or Naive Bayes. This speeds things up.
    #detector.trainSVMAndTestTrainingSet(graphIndividualFeatures=False, allClassifiers=False, statsPerFeature=featureStats)
    detector.trainSVMAndTestValidationSet(graphIndividualFeatures=True, allClassifiers=False, statsPerFeature=featureStats)
    #detector.testGangulySet()
    #detector.testMiddleOfValidationSet()  #this only works if your not clickbait scores are below 0.5 and clickbait scores are above 0.5
    #detector.predictClass("The top 10 ways to download crap")
    #detector.predict("The top 10 ways to download crap")

    if featureStats == False:
        #testYiminSet(detector) #uncomment this line to get comparative results for the qualitative study
        #dump (serialize) the detector object so we don't have to retrain every time
        #use a dump of the detector that has the highest observed accuracy
        detectorDUMP = open('pickles/clickbait_detector.dill', 'wb')
        dill.dump(detector, detectorDUMP)
        detectorDUMP.close()
        pr.disable()

    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(30)
    print(s.getvalue())

if __name__ == '__main__':
    main()
