import json
import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import AdaBoostClassifier

from models.naive_bayes_body import NaiveBayesBody
from models.tags_baseline import TagsBaseline
from models.sk_learn import SKLearnBagOfWords

class Randomness(object):
    def train(self, dataset):
        pass

    def test(self, dataset, top_number):
        accuracy_per_user = dict()
        for user_id in dataset:
            records = dataset[user_id]
            triples = [(0.5, record['answer_accepted'], record['question']['question_id']) for record in records]

            random.shuffle(triples)
            score = sum(1 for triple in triples[:top_number] if triple[1] == True)/float(top_number)
            accuracy_per_user[user_id] = score

        return sum(accuracy_per_user.values()) / len(accuracy_per_user)


with open('data.json') as stream:
    data = json.load(stream)

bayes_results = []
tags_results = []
random_forest_results = []
sgd_results = []
randomness_results = []

for i in range(20):
    bayes = NaiveBayesBody()
    tags = TagsBaseline()
    random_forest = SKLearnBagOfWords(RandomForestClassifier)
    sgd = SKLearnBagOfWords(AdaBoostClassifier)
    randomness = Randomness()
    training_data = dict()
    testing_data = dict()
    
    for user_id in data:
        records = data[user_id]
        random.shuffle(records)
    
        training_data[user_id] = records[:70]
        testing_data[user_id] = records[70:]

    randomness.train(testing_data)
    randomness_test = randomness.test(testing_data, top_number=10)
    randomness_results.append(randomness_test)
    
    bayes.train(training_data)
    bayes_test = bayes.test(testing_data, top_number=10)
    bayes_results.append(bayes_test)
    
    tags.train(training_data)
    tags_test = tags.test(testing_data, top_number=10)
    tags_results.append(tags_test)

    random_forest.train(training_data)
    random_forest_test = random_forest.test(testing_data, top_number=10)
    random_forest_results.append(random_forest_test)

    sgd.train(training_data)
    sgd_test = sgd.test(testing_data, top_number=10)
    sgd_results.append(sgd_test)


print 'Bayes', np.mean(bayes_results)
print 'Tags', np.mean(tags_results)
print 'Random Forest', np.mean(random_forest_results)
print 'SGD', np.mean(sgd_results)
print 'Random', np.mean(randomness_results)
