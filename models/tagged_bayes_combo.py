import collections
import itertools

from model import Model
import nltk
from stack_exchange import text_processing as tp

class TaggedBayesCombo(Model):

    def train(self, dataset):
        self._user_models = dict()
        self._user_top_tags = dict()
        for user_id in dataset:
            training_data = []
            top_tag = self.get_top_tags([training_pair['question'] for training_pair in dataset[user_id] if training_pair['answer_accepted']])[1]
            print top_tag
            # top_tag = 'c#'
            top_tag_training_data = []
            for training_pair in dataset[user_id]:
                question, label = training_pair['question'], training_pair['answer_accepted']
                training_data.append((self.extract_body_words(question), label))

                if top_tag in training_pair['question']['tags']:
                    top_tag_training_data.append((self.extract_body_words(question), label))

            self._user_models[user_id] = nltk.NaiveBayesClassifier.train(training_data)
            self._user_top_tags[user_id] = top_tag
            self._user_models['__' + user_id] = nltk.NaiveBayesClassifier.train(top_tag_training_data)

    def test(self, dataset, top_number=10):
        accuracy_per_user = dict()
        for user_id in dataset: 
            question_bags = [self.extract_body_words(testing_pair['question']) for testing_pair in dataset[user_id]]
            probabilities = self._user_models[user_id].batch_prob_classify(question_bags)
            tag_probabilities = self._user_models['__' + user_id].batch_prob_classify(question_bags)

            triples = []
            top_tag = self._user_top_tags[user_id]
            # top_tag = self.get_top_tags([training_pair['question'] for training_pair in dataset[user_id]])[1]
            print top_tag
            # top_tag = 'c#'
            for index, testing_pair in enumerate(dataset[user_id]):
                question, label = testing_pair['question'], testing_pair['answer_accepted']
                probability = probabilities[index].prob(True)
                tag_probability = tag_probabilities[index].prob(True)
                if top_tag in testing_pair['question']['tags'] and tag_probability < probability:
                    probability = tag_probability
                triples.append((probability, label, question['question_id']))

            triples.sort(key = lambda x: x[0], reverse=True)
            score = sum(1 for triple in triples[:top_number] if triple[1] == True)/float(top_number)
            accuracy_per_user[user_id] = score

        return accuracy_per_user

    def get_top_tags(self, questions, number_of_tags=5):
        tag_lists = [q['tags'] for q in questions]
        all_tags = itertools.chain(*tag_lists)
        counts = collections.Counter(all_tags)
        most_common = [x[0] for x in counts.most_common(number_of_tags)]
        return most_common

    def extract_body_words(self, question):
        if 'body' not in question:
            return {}
        body = question['body']
        word_list = tp.pull_stop_words(tp.simplify(tp.strip_tags(body)))
        return dict((w,1) for w in word_list)