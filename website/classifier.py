from stack_exchange import text_processing as tp
import nltk

class Classifier(object):
    def __init__(self):
        self.classifier = None

    def train(self, questions_to_accept, questions_to_reject):
        training_data = [(self.extract_body_words(question), True) for question in questions_to_accept]
        training_data.extend([(self.extract_body_words(question), False) for question in questions_to_reject])

        self.classifier = nltk.NaiveBayesClassifier.train(training_data)

    def get_recommendations(self, candidate_questions, number):
        questions_and_ranks = []
        for question in candidate_questions:
            question_body = Classifier.extract_body_words(question)
            score = self.classifier.prob_classify(question_body).prob(True)
            questions_and_ranks.append((question, score))

        questions_and_ranks.sort(key = lambda x: x[1], reverse=True)
        print [x[0]['question_id'] for x in questions_and_ranks[-number:]]
        return questions_and_ranks[:number]

    @classmethod
    def extract_body_words(cls, question):
        if 'body' not in question:
            return dict()
        body = question['body']
        word_list = tp.pull_stop_words(tp.simplify(tp.strip_tags(body)))
        return dict((w,1) for w in word_list)
