import json
import random
import itertools

from models.naive_bayes_body import NaiveBayesBody

with open('data.json') as stream:
	data = json.load(stream)

classifier = NaiveBayesBody()
training_data = dict()
testing_data = dict()

for user_id in data:
	records = data[user_id]
	random.shuffle(records)

	training_data[user_id] = records[:70]
	testing_data[user_id] = records[70:]

classifier.train(testing_data)
print classifier.test(testing_data, top_number=10)
