import json
import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import AdaBoostClassifier

from models.naive_bayes_body import NaiveBayesBody
from models.tags_baseline import TagsBaseline
from models.sk_learn import SKLearnBagOfWords

with open('data.json') as stream:
    data = json.load(stream)


bayes_results = []
tags_results = []
random_forest_results = []
sgd_results = []
for i in range(10):
    bayes = NaiveBayesBody()
    tags = TagsBaseline()
    random_forest = SKLearnBagOfWords(RandomForestClassifier)
    sgd = SKLearnBagOfWords(AdaBoostClassifier)
    training_data = dict()
    testing_data = dict()
    
    for user_id in data:
        records = data[user_id]
        random.shuffle(records)
    
        training_data[user_id] = records[:70]
        testing_data[user_id] = records[70:]
    
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