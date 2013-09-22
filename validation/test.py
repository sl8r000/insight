import argparse
import json
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC

from models.naive_bayes_body import NaiveBayesBody
from models.naive_bayes_title import NaiveBayesTitle
from models.tags_baseline import TagsBaseline
from models.sk_learn import SKLearnBagOfWords
from models.randomness_baseline import Randomness
from models.sk_learn_bagging import SKLearnTextBagging
from models.tagged_bayes_combo import TaggedBayesCombo


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file_name', help='path to the data file')
    parser.add_argument('-n', '--num_repetitions', help='number of times to run the tests', type=int)
    parser.add_argument('-s', '--split', help='number of results to train upon', type=int)
    parser.add_argument('-t', '--top', help='number of records to predict', type=int, default=10)
    args = parser.parse_args()

    with open(args.file_name) as stream:
        data = json.load(stream)

    data = dict((k, data[k]) for k in data.keys()[:3])

    bayes_results = []
    tags_results = []
    random_forest_results = []
    adaboost_results = []
    randomness_results = []
    bayes_title_results = []
    bagging_results = []
    combo_results = []
    for i in range(args.num_repetitions):
        print i
        training_data = dict()
        testing_data = dict()

        for user_id in data:
            records = data[user_id]
            random.shuffle(records)

            training_data[user_id] = records[:args.split]
            testing_data[user_id] = records[args.split:]

        # bagging = SKLearnTextBagging(classifier_class_list=[RandomForestClassifier, AdaBoostClassifier, SVC], text_source='title')
        # bagging.train(training_data)
        # these_bagging_results = bagging.test(testing_data, top_number=args.top)
        # bagging_results.append(these_bagging_results)

        # bayes_title = NaiveBayesTitle()
        # bayes_title.train(training_data)
        # these_bayes_title_results = bayes_title.test(testing_data, top_number=args.top)
        # bayes_title_results.append(these_bayes_title_results)

        # bayes = NaiveBayesBody()
        # bayes.train(training_data)
        # these_bayes_results = bayes.test(testing_data, top_number=args.top)
        # bayes_results.append(these_bayes_results)

        combo = TaggedBayesCombo()
        combo.train(training_data)
        these_combo_results = combo.test(testing_data, top_number=args.top)
        combo_results.append(these_combo_results)

        # tags = TagsBaseline()
        # tags.train(training_data)
        # these_tags_results = tags.test(testing_data, top_number=args.top)
        # tags_results.append(these_tags_results)

        # random_forest = SKLearnBagOfWords(RandomForestClassifier)
        # random_forest.train(training_data)
        # these_random_forest_results = random_forest.test(testing_data, top_number=args.top)
        # random_forest_results.append(these_random_forest_results)

        # adaboost = SKLearnBagOfWords(AdaBoostClassifier)
        # adaboost.train(training_data)
        # these_adaboost_results = adaboost.test(testing_data, top_number=args.top)
        # adaboost_results.append(these_adaboost_results)

        # randomness = Randomness()
        # randomness.train(training_data)
        # these_randomness_results = randomness.test(testing_data, top_number=args.top)
        # randomness_results.append(these_randomness_results)


# results = [bayes_results, tags_results, random_forest_results, adaboost_results, randomness_results, bayes_title_results, bagging_results]
# keys = ['bayes', 'tags', 'random_forest', 'adaboost', 'randomness', 'bayes_title', 'bagging']

# results = [bayes_results, bayes_title_results, tags_results, randomness_results]
# keys = ['bayes', 'bayes_title', 'tags', 'randomness']

results = [combo_results]
keys = ['combo']
individual_frames = [DataFrame(x) for x in results]
total_frame = pd.concat(individual_frames, axis=1, keys=keys)
total_frame = total_frame.swaplevel(0, 1, axis=1)

mean_matrix = total_frame.mean().unstack()
print mean_matrix
print ''
print mean_matrix.mean()

