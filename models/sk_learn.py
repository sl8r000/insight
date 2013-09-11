import collections
from sklearn.feature_extraction.text import TfidfVectorizer

from model import Model
from stack_exchange import text_processing as tp

class SKLearnBagOfWords(Model):
    def __init__(self, classifier_class, vectorizer_class=None):
        self.classifier_class = classifier_class
        if vectorizer_class is None:
            vectorizer_class = TfidfVectorizer
        self.vectorizer_class = vectorizer_class

    @classmethod
    def extract_simple_body(cls, question):
        return tp.simplify(tp.strip_tags(question['body']))

    def train(self, dataset):
        self._user_vectorizers = dict()
        self._user_classifiers = dict()

        for user_id in dataset:
            question_texts = [SKLearnBagOfWords.extract_simple_body(training_pair['question']) 
                              for training_pair in dataset[user_id]]
            question_labels = [1 if training_pair['answer_accepted'] else 0 for training_pair in dataset[user_id]]

            vectorizer = self.vectorizer_class()
            vectorized_questions = vectorizer.fit_transform(question_texts)
            self._user_vectorizers[user_id] = vectorizer

            classifier = self.classifier_class()
            classifier.fit(vectorized_questions.toarray(), question_labels)
            self._user_classifiers[user_id] = classifier

    def test(self, dataset, top_number):
        accuracy_per_user = dict()
        for user_id in dataset:
            triples = []
            for testing_pair in dataset[user_id]:
                question, label = testing_pair['question'], testing_pair['answer_accepted']
                simple_body = SKLearnBagOfWords.extract_simple_body(question)
                vectorized_question = self._user_vectorizers[user_id].transform([simple_body])
                probability = self._user_classifiers[user_id].predict_proba(vectorized_question.toarray())[0][1]
                triples.append((probability, label, question['question_id']))

            triples.sort(key = lambda x: x[0], reverse=True)
            score = sum(1 for triple in triples[:top_number] if triple[1] == 1)/float(top_number)
            accuracy_per_user[user_id] = score

        return accuracy_per_user
