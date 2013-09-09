import itertools
import collections

from model import Model
import nltk
from stack_exchange import text_processing as tp

class NaiveBayesBody(Model):

    def recommend(self, data_source, user_id, number):
        answers =  data_source.get_user_answers(user_id)
        accepted_answer_ids = set(a['question_id'] for a in answers if a['is_accepted'])

        questions = data_source.get_questions([a['question_id'] for a in answers])
        training_data = [(self.extract_body_words(q), q['question_id'] in accepted_answer_ids)
                         for q in questions]

        classifier = nltk.NaiveBayesClassifier.train(training_data)

        tags = itertools.chain(*[q['tags'] for q in questions])
        top_tags = [x[0] for x in collections.Counter(tags).most_common(5)]

        candidate_questions = data_source.get_candidate_questions(top_tags)
        candidate_questions.sort(key = lambda q: q['question_id'])
        candidate_questions = ([candidate_questions[0]] + 
            [q for i,q in enumerate(candidate_questions) if q['question_id'] != candidate_questions[i-1]['question_id']])


        working_double = [(q, self.extract_body_words(q)) for q in candidate_questions]
        scores = [(x[0], classifier.prob_classify(x[1]).prob(True)) for x in working_double]
        scores.sort(key = lambda x: x[1], reverse=True)

        return scores[:5]

    def extract_body_words(self, question):
        body = question['body']
        word_list = tp.pull_stop_words(tp.simplify(tp.strip_tags(body)))
        return dict((w,1) for w in word_list)