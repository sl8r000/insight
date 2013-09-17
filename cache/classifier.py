from stack_exchange import text_processing as tp
import nltk


class TagSegmentedClassifier(object):
    def __init__(self):
        self.tag_classifiers = None
        self.untagged_classifier = None

    def train(self, questions_to_accept, questions_to_reject, tag_list):
        for tag in tag_list:
            tagged_accepts = [q for q in questions_to_accept if tag in q['tags']]
            tagged_rejects = [q for q in questions_to_reject if tag in q['tags']]

            tag_classifier = Classifier()
            tag_classifier.train(tagged_accepts, tagged_rejects)
            self.tag_classifiers[tag] = tag_classifier

        remaining_accepts = [q for q in questions_to_accept if set(q['tags']).isdisjoint(set(tag_list))]
        remaining_rejects = [q for q in questions_to_reject if set(q['tags']).isdisjoint(set(tag_list))]
        untagged_classifier = Classifier()
        untagged_classifier.train(remaining_accepts, remaining_rejects)
        self.untagged_classifier = untagged_classifier

    def get_recommendations(self, candidate_questions, number):
        tag_list = self.tag_classifiers.keys()
        tagged_rankings = dict((k, []) for k in tag_list)
        untagged_rankings = [] 

        for question in candidate_questions:
            question_body = Classifier.extract_body_words(question)
            if set(question['tags']).isdisjoint(set(tag_list)):
                score = self.untagged_classifier.prob_classify(question_body).prob(True)
                untagged_rankings.append((score, question))
            else:
                for tag in tag_list:
                    if tag in question['tags']:
                        score = self.tag_classifiers[tag].prob_classify(question_body).prob(True)
                    





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
            questions_and_ranks.append((score, question))

        questions_and_ranks.sort(key = lambda x: x[0], reverse=True)
        return questions_and_ranks[:number]

    @classmethod
    def extract_body_words(cls, question):
        if 'body' not in question:
            return dict()
        body = question['body']
        word_list = tp.pull_stop_words(tp.simplify(tp.strip_tags(body)))
        return dict((w,1) for w in word_list)