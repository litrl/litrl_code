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
# Name:        satireml.py
# Purpose:     detect satire
#
# Created:     Browser version - December 2017
#
# Language and Information Technology Research Lab
# Faculty of Information and Media Studies (FIMS)
# University of Western Ontario, London, Canada
#-------------------------------------------------------------------------------

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
#from sklearn.cross_validation import KFold
#from sklearn.cross_validation import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn import metrics
from pattern.en import parsetree, ngrams, modality, mood, sentiment, number, wordnet
from pattern.vector import Document, Model
from os.path import isfile, join

# Parameters to the algorithm.
ALPHA = 0.2
BETA = 0.45
ETA = 0.4
PHI = 0.2
DELTA = 0.85
N = 0

class satireDetector:

    def v(self, verbose, text):
        if verbose:
            print("Verbose Output: ", text)

    ######################## named entities  #########################

    def keywithmaxval(self, A):
         newA = dict(sorted(iter(A.items()), key=operator.itemgetter(1), reverse=True)[:3])
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


    ######################### word similarity ##########################

    def get_best_synset_pair(self, word_1, word_2):
        #GIVEN TWO WORDS, FIND THEIR SET OF SYNONYMS. RETURN THE PAIR OF SYNONYMS FROM ALL THE SYNONYMS PAIRS THAT HAVE THE HIGHEST SIMILARITY (SHORTEST PATH)
        """
        Choose the pair with highest path similarity among all pairs.
        Mimics pattern-seeking behavior of humans.
        """
        max_sim = -1.0
        synsets_1 = wn.synsets(word_1)
        synsets_2 = wn.synsets(word_2)
        if len(synsets_1) == 0 or len(synsets_2) == 0:
            return None, None
        else:
            max_sim = -1.0
            best_pair = None, None
            #huge slowdown because of the for loop and wn.path_similarity
            for synset_1 in synsets_1:
                for synset_2 in synsets_2:
                   sim = wn.path_similarity(synset_1, synset_2)
                   if sim > max_sim:
                       max_sim = sim
                       best_pair = synset_1, synset_2
            return best_pair

    def length_dist(self, synset_1, synset_2):
        #GIVEN TWO SETS OF SYNONYMS RETURN THE LENGTH AS THE SHORTEST DISTANCE IF THERE IS NO WORD OVERLAP
        """
        Return a measure of the length of the shortest path in the semantic
        ontology between two
        synsets.
        """
        l_dist = sys.maxsize
        if synset_1 is None or synset_2 is None:
            return 0.0
        if synset_1 == synset_2:
            # if synset_1 and synset_2 are the same synset return 0
            l_dist = 0.0
        else:
            wset_1 = set([str(x.name()) for x in synset_1.lemmas()])
            wset_2 = set([str(x.name()) for x in synset_2.lemmas()])
            if len(wset_1.intersection(wset_2)) > 0:
                # if synset_1 != synset_2 but there is word overlap, return 1.0
                l_dist = 1.0
            else:
                # just compute the shortest path between the two
                l_dist = synset_1.shortest_path_distance(synset_2)
                if l_dist is None:
                    l_dist = 0.0
        # normalize path length to the range [0,1]
        return math.exp(-ALPHA * l_dist)

    def hierarchy_dist(self, synset_1, synset_2):
        #GIVEN TO SETS OF SYNONYMS RETURN A MEASURE OF THE DEPTH OF THE ONTOLOGY

        """
        Return a measure of depth in the ontology to model the fact that
        nodes closer to the root are broader and have less semantic similarity
        than nodes further away from the root.
        """
        h_dist = sys.maxsize
        if synset_1 is None or synset_2 is None:
            return h_dist
        if synset_1 == synset_2:
            # return the depth of one of synset_1 or synset_2
            h_dist = max([x[1] for x in synset_1.hypernym_distances()])
        else:
            # find the max depth of least common subsumer
            hypernyms_1 = {x[0]:x[1] for x in synset_1.hypernym_distances()}
            hypernyms_2 = {x[0]:x[1] for x in synset_2.hypernym_distances()}
            lcs_candidates = set(hypernyms_1.keys()).intersection(
                set(hypernyms_2.keys()))
            if len(lcs_candidates) > 0:
                lcs_dists = []
                for lcs_candidate in lcs_candidates:
                    lcs_d1 = 0
                    if lcs_candidate in hypernyms_1:
                        lcs_d1 = hypernyms_1[lcs_candidate]
                    lcs_d2 = 0
                    if lcs_candidate in hypernyms_2:
                        lcs_d2 = hypernyms_2[lcs_candidate]
                    lcs_dists.append(max([lcs_d1, lcs_d2]))
                h_dist = max(lcs_dists)
            else:
                h_dist = 0
        return ((math.exp(BETA * h_dist) - math.exp(-BETA * h_dist)) /
            (math.exp(BETA * h_dist) + math.exp(-BETA * h_dist)))

    def word_similarity(self, word_1, word_2):
        # GIVEN TWO WORDS, GET THE BEST SYSNONYM SET PAIR FOR BOTH WORDS.  RETURN THEIR SIMILARITY WHICH IS LENGTH_DIST x HIERARCHY DISTANCE

        synset_pair = self.get_best_synset_pair(word_1, word_2)
        return (self.length_dist(synset_pair[0], synset_pair[1]) *
            self.hierarchy_dist(synset_pair[0], synset_pair[1]))


    ######################### sentence similarity ##########################

    def most_similar_word(self, word, word_set):

        #GIVEN A SINGLE WORD AND A SET OF WORDS, RETURN THE WORD IN THE SET THAT IS MOST SIMILAR BY CALLING WORD_SIMILARITY ROUTINE. ALSO RETURN THE SIMIARITY SCORE

        """
        Find the word in the joint word set that is most similar to the word
        passed in. We use the algorithm above to compute word similarity between
        the word and each word in the joint word set, and return the most similar
        word and the actual similarity value.
        """
        max_sim = -1.0
        sim_word = ""
        for ref_word in word_set:
          sim = self.word_similarity(word, ref_word)
          if sim > max_sim:
              max_sim = sim
              sim_word = ref_word
        return sim_word, max_sim


    def semantic_vector(self, words, joint_words):
        # GIVEN A SENTENCE AS A SET OF WORDS, AND A LIST OF WORDS IN BOTH SENTENCES RETURN A VECTOR OF VALUES

        """
        Computes the semantic vector of a sentence. The sentence is passed in as
        a collection of words. The size of the semantic vector is the same as the
        size of the joint word set. The elements are 1 if a word in the sentence
        already exists in the joint word set, or the similarity of the word to the
        most similar word in the joint word set if it doesn't.
        """
        sent_set = set(words)
        semvec = np.zeros(len(joint_words))
        i = 0
        for joint_word in joint_words:
            if joint_word in sent_set:
                # if word in union exists in the sentence, semantic vector(i) = 1 (unnormalized)
                semvec[i] = 1.0
            else:
                # find the most similar word in the joint set and set the sim value
                sim_word, max_sim = self.most_similar_word(joint_word, sent_set)
                semvec[i] = PHI if max_sim > PHI else 0.0
            i = i + 1
        return semvec

    def semantic_similarity(self, sentence_1, sentence_2):
        #GIVEN TWO SENTENCES, CALL THEIR SEMANTIC VECTOR VALUES, AND COMPUTE THEIR COSINE SIMILARITY.COSINE IS DOT PRODUCT DIVIDED BY MULTIPLIED VECTOR LENGTHS

        """
        Computes the semantic similarity between two sentences as the cosine
        similarity between the semantic vectors computed for each sentence.
        """
        words_1 = nltk.word_tokenize(sentence_1)
        words_2 = nltk.word_tokenize(sentence_2)
        joint_words = set(words_1).union(set(words_2))
        vec_1 = self.semantic_vector(words_1, joint_words)
        vec_2 = self.semantic_vector(words_2, joint_words)
        return np.dot(vec_1, vec_2.T) / (np.linalg.norm(vec_1) * np.linalg.norm(vec_2))

    ######################### word order similarity ##########################

    def word_order_vector(self, words, joint_words, windex):

        # GIVEN A SENTENCE AS A SET OF WORDS AND A JOINT SET RETURN THE WORD ORDER VECTOR.
        # The elements of the word order  vector are the position mapping (from the windex dictionary) of the word in the joint set if the word exists in the sentence.
        # If the word does not exist in the sentence, then the value of the element is the  position of the most similar word in the sentence as long as the similarity is above the threshold ETA.

        wovec = np.zeros(len(joint_words))
        i = 0
        wordset = set(words)
        for joint_word in joint_words:
            if joint_word in wordset:
                # word in joint_words found in sentence, just populate the index
                wovec[i] = windex[joint_word]
            else:
                # word not in joint_words, find most similar word and populate
                # word_vector with the thresholded similarity
                sim_word, max_sim = self.most_similar_word(joint_word, wordset)
                if max_sim > ETA:
                    wovec[i] = windex[sim_word]
                else:
                    wovec[i] = 0
            i = i + 1
        return wovec

    def word_order_similarity(self, sentence_1, sentence_2):
        # GIVEN TWO SENTENCES, RETURN THEIR ORDER SIMILARITY.  1-Vector Norm (v1-v2)/ Vector norm (v1 +v2); v1 is word order vector of s1, v2 is word order vector of s2)

        """
        Computes the word-order similarity between two sentences as the normalized
        difference of word order between the two sentences.
        """
        words_1 = nltk.word_tokenize(sentence_1)
        words_2 = nltk.word_tokenize(sentence_2)
        joint_words = list(set(words_1).union(set(words_2)))
        windex = {x[1]: x[0] for x in enumerate(joint_words)}
        r1 = self.word_order_vector(words_1, joint_words, windex)
        r2 = self.word_order_vector(words_2, joint_words, windex)
        return 1.0 - (np.linalg.norm(r1 - r2) / np.linalg.norm(r1 + r2))



    ######################### overall similarity #################################

    def similarity(self, sentence_1, sentence_2):

        # GIVEN TWO SENTENCES, RETURN THEIR SIMIALRITY WHICH IS A COMBINATION OF SEMANTIC SIMILARITY AND WORD ORDER SMILARITY AS A NORMALIZED SCORE

        """
        Calculate the semantic similarity between two sentences.
        """
        return DELTA * self.semantic_similarity(sentence_1, sentence_2) + \
            (1.0 - DELTA) * self.word_order_similarity(sentence_1, sentence_2)

    #LIWC ALTERNATIVES (some of these are copied directly from the clickbait detector. It would be good to refactor these into a parent class)
    #LIWC normally returns results as a % of the total text. The numbers from these functions may not be the exact same.
    #EXCEPT, word count, words per sentence, sentences ending with a "?" mark

    #f - feature
    #f1: PRP + PRP$ (check)
    def getPronouns(self, partsOfSpeech, wordCount):
        count = 0
        for pos in partsOfSpeech:
            if "PRP" in pos:
                count = count + 1
        return (float(count) / float(wordCount)) * 100

    #f2
    #PRP
    def getPersonalPronouns(self, partsOfSpeech, wordCount):
        count = 0
        for pos in partsOfSpeech:
            if "PRP" == pos:
                count = count + 1
        return (float(count) / float(wordCount)) * 100

    #f3: PRP$ (pronouns, possessive. check)
    def getPossessivePronouns(self, partsOfSpeech, wordCount):
        count = 0
        for pos in partsOfSpeech:
            if "PRP$" == pos:
                count = count + 1
        return (float(count) / float(wordCount)) * 100

    #f4: PP (prepositional phrase? check)
    def getPrepositionalPhrases(self, chunksOfSpeech, wordCount):
        count = 0
        for chunk in chunksOfSpeech:
            if "PP" == chunk.type:
                count = count + 1
        return (float(count) / float(wordCount)) * 100

    #f5: VP
    def getVerbPhrases(self, chunksOfSpeech, wordCount):
        count = 0
        for chunk in chunksOfSpeech:
            if "VP" == chunk.type:
                count = count + 1
        return (float(count) / float(wordCount)) * 100

    #f6: CC, IN
    def getConjunctions(self, partsOfSpeech, wordCount):
        count = 0
        for pos in partsOfSpeech:
            if "CC" == pos:
                count = count + 1
            elif "IN" == pos:
                count = count + 1
        return (float(count) / float(wordCount)) * 100

    #f7: ADVP
    def getAdverbPhrases(self, chunksOfSpeech, wordCount):
        count = 0
        for chunk in chunksOfSpeech:
            if "ADVP" == chunk.type:
                count = count + 1
        return (float(count) / float(wordCount)) * 100

    #f8: ADJP
    def getAdjectivePhrases(self, chunksOfSpeech, wordCount):
        count = 0
        for chunk in chunksOfSpeech:
            if "ADJP" == chunk.type:
                count = count + 1
        return (float(count) / float(wordCount)) * 100

    #f9: no equal for negative emotions
    #TODO

    #f10: no equal for periods. write.
    def getPeriods(self, sentence):
        count = sentence.string.count(".")
        return count

    #f11: ,
    def getCommas(self, sentence):
        count = sentence.string.count(",")
        return count

    #f12: :
    def getColon(self, sentence):
        count = sentence.string.count(":")
        return count

    #f13: no equal for semicolon. write.
    def getSemicolon(self, sentence):
        count = sentence.string.count(";")
        return count

    #percent of sentences ending with a "?"
    def getQuestionMarks(self, sentence):
        count = sentence.string.count("?")
        return count

    #f15: no equal exclamations. write.
    def getExclamationMarks(self, sentence):
        count = sentence.string.count("!")
        return count

    #f16: no equal for quotes. write.
    #TODO

    def getPercentage(self, count, divisor):
        return (float(count) / divisor) * 100

    def getAbsurdityScore(self, test_data):
        # COMPUTE ABSURDITY SCORE
        # FOR EVERY STORY, TOKENIZE THE STORY, GET A LIST OF THE NAMED ENTIES IN THE STORY ASIDE FROM LAST SENTENCE.
        # GET A LIST OF NAMED ENTITIES IN LAST SENTENCE. IF THERE IS NO OVERALAP THE RETURN 1  x
        absflag = 0
        sents = sent_tokenize(test_data)
        all = []
        for s in sents[0:-1]:
            ents = self.get_continuous_chunks(s)# get all the entities in all the story except the last sentence
            all.append(" ".join([t for t in ents]))
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
        return absflag

    def getHumorScore(self, test_data):
        # COMPUTE HUMOR SCORE
        # for all sentences in the story apart from the first sentence, create a list of the similarities. If the similarity between the first and the last is lower than the similarities in the list, return humorous
        d_sim =[]
        sents = sent_tokenize(test_data.encode('ascii', 'ignore'))
        humflag = 0 # set humor to zero default
        firstAndLastSentSim = self.similarity(sents[0], sents[-1])
        for s in sents[1:-1]:
            d_sim.append(self.similarity(sents[0], s))
            if min(d_sim) > firstAndLastSentSim:
              humflag=1
              break;
            else: humflag=0
        return humflag

    def trainTestSplit(self, train_percent=0.8):
        #THE TRAINING SET USED IN THE MODEL IS RETRIEVED HERE#
        train = pd.read_csv("./data/All_Data_475_no_newlines.csv", header=0, sep=",", error_bad_lines=False)

        self.satire = []
        self.not_satire = []

        i = 0
        for i in range(0, len(train['Full Text'])):
            if train['Satire Flag'][i] == 0:
                self.not_satire.append(train['Full Text'][i])
            else:
                self.satire.append(train['Full Text'][i])
            i = i + 1

        self.notSatireTrain, self.notSatireTest = train_test_split(self.not_satire, train_size = train_percent)
        self.satireTrain, self.satireTest = train_test_split(self.satire, train_size = train_percent)

        Xtrain = np.array(self.notSatireTrain + self.satireTrain)
        Ytrain = []

        for x in range(len(self.notSatireTrain)):
            Ytrain.append(0)
        for x in range(len(self.satireTrain)):
            Ytrain.append(1)

        Xtest = np.array(self.notSatireTest + self.satireTest)
        Ytest = []

        for x in range(len(self.notSatireTest)):
            Ytest.append(0)
        for x in range(len(self.satireTest)):
            Ytest.append(1)

        print("Satire Stories for Training: ", len(Xtrain))
        print("Satire Stories for Testing: ", len(Xtest))

        self.train(Xtrain, Ytrain)

        correct_preds = 0

        for x in range(len(Ytest)):
            pred = self.classifier_linear.predict(self.getScores([Xtest[x]]))
            if pred == Ytest[x]:
                correct_preds = correct_preds + 1

        print("Correct classifications: ", correct_preds)
        print("Total classifications:   ", len(Ytest))
        self.classifierScore_SVM = "SVM Test set score: ", correct_preds / float(len(Ytest))
        print(self.classifierScore_SVM)

    def train(self, train_data, Ytrain, allClassifiers=False, crossValidate=False):

        avgSatire = []
        avgNotSatire = []

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
                avgArrayName = "NotSatire"
            else:
                avgArrayName = "Satire"

            train_count = train_count + 1

            patternParseTree = parsetree(story, tokenize=True, tags=True, chunks=True, relations=True, lemmata=True)
            lstTextPOS = []
            lstTextWords = []
            lstTextChunks = []

            #for feature 14
            f10 = 0
            f11 = 0
            f12 = 0
            f13 = 0
            f14 = 0
            f15 = 0

            for sentence in patternParseTree:
                f10 = f10 + self.getPeriods(sentence)
                f11 = f11 + self.getCommas(sentence)
                f12 = f12 + self.getColon(sentence)
                f13 = f13 + self.getSemicolon(sentence)
                f14 = f14 + self.getQuestionMarks(sentence)
                f15 = f15 + self.getExclamationMarks(sentence)
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

            #f9: no equal for negative emotions
            #TODO
            f9 = 0

            #f10-15 are all done during sentence processing

            #f10: no equal for periods. write.

            f10 = self.getPercentage(f10, divisorWordCount)
            #f11: ,
            f11 = self.getPercentage(f11, divisorWordCount)
            #f12: :
            f12 = self.getPercentage(f12, divisorWordCount)
            #f13: no equal for semicolon. write.
            f13 = self.getPercentage(f13, divisorWordCount)
            #f14: no equal for question mark. write.
            f14 = self.getPercentage(f14, divisorWordCount)
            #f15: no equal exclamations. write.
            f15 = self.getPercentage(f15, divisorWordCount)

            #f16: no equal for quotes. write.
            #TODO
            f16 = 0

            absflag = self.getAbsurdityScore(story)
            #humScore = self.getHumorScore(story)

            story_features = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16, absflag]

            if avgArrayName == "Satire":
                #set up our list of features averages based on the size of our first sample
                if len(avgSatire) == 0:
                    for c in range(len(story_features)):
                        avgSatire.append(0)

                #sum everything to get an average later
                for x in range(len(story_features)):
                    avgSatire[x] = float(avgSatire[x]) + float(story_features[x])
            elif avgArrayName == "NotSatire":
                #set up our list of features averages based on the size of our first sample
                if len(avgNotSatire) == 0:
                    for c in range(len(story_features)):
                        avgNotSatire.append(0)

                #sum everything to get an average later
                for x in range(len(story_features)):
                    avgNotSatire[x] = float(avgNotSatire[x]) + float(story_features[x])

            print(train_count, story_features)

            train_feat.append(story_features)

        Xtrain = np.hstack([train_tdfvectors.toarray(), train_feat])

        #divide to get avgs
        for x in range(len(avgSatire)):
            avgSatire[x] = avgSatire[x] / float(len(avgSatire))
        for x in range(len(avgNotSatire)):
            avgNotSatire[x] = avgNotSatire[x] / float(len(avgNotSatire))

        print("AVG Not Satire Feature Scores")
        print(avgSatire)

        print("AVG Satire Feature Scores")
        print(avgNotSatire)

        # Perform classification with SVM, kernel=linear
        self.classifier_linear = svm.SVC(kernel='linear', probability = True)
        self.classifier_linear.fit(Xtrain, Ytrain)

        #print train_data[169]
        #print Xtrain[169]
        #pred = self.classifier_linear.predict_proba(Xtrain[169])
        #print pred

        if allClassifiers == True:
            #TRAIN AND TEST THE MODEL USING FIT AND PREDICT FUNCTIONS FROM SCIKIT LEARN - NAIVE BAYES CLASSIFIER
            t0 = time.time()
            self.classifier_NB = MultinomialNB(alpha=1, fit_prior=True)
            self.classifier_NB.fit(Xtrain, Ytrain)
            time_nb_train = t1-t0

            #TRAIN AND TEST THE MODEL - RBF KERNEL
            self.classifier_rbf = svm.SVC( kernel='rbf')
            t0 = time.time()
            self.classifier_rbf.fit(Xtrain, Ytrain)
            t1 = time.time()
            time_rbf_train = t1-t0

            # Perform classification with SVM, kernel=linear
            self.classifier_liblinear = svm.LinearSVC()
            t0 = time.time()
            self.classifier_liblinear.fit(Xtrain, Ytrain)
            t1 = time.time()
            time_liblinear_train = t1-t0

        if crossValidate == True:
            #PERFORM 10-fold Cross Validation for Accuracy Score
            scores = cross_val_score(self.classifier_linear,Xtrain, Ytrain, cv=10, scoring='accuracy')

    def getScores(self, test_data, returnBoth = False):

        test_tdfvectors = self.vectorizer.transform(array(test_data))

        #disabled for now
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

        #for feature 14
        f10 = 0
        f11 = 0
        f12 = 0
        f13 = 0
        f14 = 0
        f15 = 0

        for sentence in patternParseTree:
            f10 = f10 + self.getPeriods(sentence)
            f11 = f11 + self.getCommas(sentence)
            f12 = f12 + self.getColon(sentence)
            f13 = f13 + self.getSemicolon(sentence)
            f14 = f14 + self.getQuestionMarks(sentence)
            f15 = f15 + self.getExclamationMarks(sentence)
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

        #f9: no equal for negative emotions
        #TODO
        f9 = 0

        #f10-15 are all done during sentence processing

        #f10: periods, may not be the same as the LIWC functions
        f10 = self.getPercentage(f10, divisorWordCount)
        #f11: ,
        f11 = self.getPercentage(f11, divisorWordCount)
        #f12: :
        f12 = self.getPercentage(f12, divisorWordCount)
        #f13: semicolons
        f13 = self.getPercentage(f13, divisorWordCount)
        #f14: question marks
        f14 = self.getPercentage(f14, divisorWordCount)
        #f15: exclamations
        f15 = self.getPercentage(f15, divisorWordCount)

        #f16: no equal for quotes. write.
        #TODO
        f16 = 0

        features = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16]

        featuresWithFlags = features + [absflag]

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
            test_data.append(testitem)

        pairFeaturesXtest = self.getScores(test_data, True)
        features = pairFeaturesXtest[0]
        Xtest = pairFeaturesXtest[1]

        prediction_linear = self.classifier_linear.predict(Xtest)
        prediction_scores = self.classifier_linear.predict_proba(Xtest)

        betterString = str(prediction_scores[0])[1:-1]
        classValues = betterString.split(" ")
        classValues = [_f for _f in classValues if _f]
        return ",".join(classValues) + "," + ",".join(str(featScore) for featScore in features)
