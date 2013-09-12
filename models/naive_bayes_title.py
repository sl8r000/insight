from model import Model
import nltk
from stack_exchange import text_processing as tp

class NaiveBayesTitle(Model):

    def train(self, dataset):
        self._user_models = dict()
        for user_id in dataset:
            training_data = []
            for training_pair in dataset[user_id]:
                question, label = training_pair['question'], training_pair['answer_accepted']
                training_data.append((self.extract_title_words(question), label))

            self._user_models[user_id] = nltk.NaiveBayesClassifier.train(training_data)

    def test(self, dataset, top_number=10):
        accuracy_per_user = dict()
        for user_id in dataset:
            question_bags = [self.extract_title_words(testing_pair['question']) for testing_pair in dataset[user_id]]
            probabilities = self._user_models[user_id].batch_prob_classify(question_bags)

            triples = []
            for index, testing_pair in enumerate(dataset[user_id]):
                question, label = testing_pair['question'], testing_pair['answer_accepted']
                probability = probabilities[index].prob(True)
                triples.append((probability, label, question['question_id']))

            triples.sort(key = lambda x: x[0], reverse=True)
            score = sum(1 for triple in triples[:top_number] if triple[1] == True)/float(top_number)
            accuracy_per_user[user_id] = score

        return accuracy_per_user

    def extract_title_words(self, question):
        title = question['title']
        word_list = tp.pull_stop_words(tp.simplify(tp.strip_tags(title)))
        return dict((w,1) for w in word_list)