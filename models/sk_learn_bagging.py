from sklearn.feature_extraction.text import TfidfVectorizer

from model import Model
from stack_exchange import text_processing as tp

class SKLearnTextBagging(Model):
    def __init__(self, classifier_class_list, text_source, include_accept_rate=False, vectorizer_class=None):
        self.classifier_class_list = classifier_class_list
        self.text_source = text_source
        self.include_accept_rate = include_accept_rate
        if vectorizer_class is None:
            vectorizer_class = TfidfVectorizer
        self.vectorizer_class = vectorizer_class

    @classmethod
    def clean_text(cls, messy_text):
        return tp.simplify(tp.strip_tags(messy_text))

    def train(self, dataset):
        self._user_model_lists = dict()
        self._user_vectorizers = dict()
        for user_id in dataset:
            texts = []
            for training_pair in dataset[user_id]:
                if self.text_source == 'body':
                    text = self.clean_text(training_pair['question']['body'])
                elif self.text_source == 'title':
                    text = self.clean_text(training_pair['question']['title'])
                texts.append(text)

            labels = [1 if pair['answer_accepted'] else 0 for pair in dataset[user_id]]

            vectorizer = self.vectorizer_class()
            vectorized_text = vectorizer.fit_transform(texts)
            self._user_vectorizers[user_id] = vectorizer

            classifiers = [classifier_class() for classifier_class in self.classifier_class_list]
            for classifier in classifiers:
                classifier.fit(vectorized_text.toarray(), labels)
            self._user_model_lists[user_id] = classifiers

    def test(self, dataset, top_number):
        accuracy_per_user = dict()
        for user_id in dataset:
            triples = []
            for pair in dataset[user_id]:
                question, label = pair['question'], pair['answer_accepted']

                if self.text_source == 'body':
                    text = self.clean_text(question['body'])
                elif self.text_source == 'title':
                    text = self.clean_text(question['title'])

                vectorized_text = self._user_vectorizers[user_id].transform([text])

                yes_votes = 0
                for model in self._user_model_lists[user_id]:
                    this_model_vote = model.predict(vectorized_text.toarray())
                    if this_model_vote == 1:
                        yes_votes += 1

                triples.append((yes_votes, label, question['question_id']))

            triples.sort(key = lambda x: x[0], reverse=True)
            score = sum(1 for triple in triples[:top_number] if triple[1] == 1)/float(top_number)
            accuracy_per_user[user_id] = score

        return accuracy_per_user
