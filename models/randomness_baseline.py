import random

from models.model import Model

class Randomness(Model):
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

        return accuracy_per_user