import collections
import itertools
import nltk

from stack_exchange_client import StackExchangeClient
import text_processing as tp

EXCEPTION_FORMATTER = ('Method {method_name} not implemented!'
                       '{class_name} is an abstract class meant only to guarantee a consistent'
                       'interface across different data sources.')


class DataSource(object):

    # Return all the answers submitted by User user_id.
    def get_user_answers(self, user_id):
        raise NotImplementedError(
            EXCEPTION_FORMATTER.format(method_name='get_user_answers', class_name='DataSource'))

    # Return all questions with the given id or ids
    def get_questions(self, question_id_or_ids):
        raise NotImplementedError(
            EXCEPTION_FORMATTER.format(method_name='get_questions', class_name='DataSource'))

    # Return a list of candidate questions to classify
    def get_candidate_questions(self, tags):
        raise NotImplementedError(
            EXCEPTION_FORMATTER.format(method_name='get_candidate_questions', class_name='DataSource'))

class LiveSource(DataSource):

    def __init__(self, stack_overflow_client):
        self.client = stack_overflow_client

    @classmethod
    def from_credentials(cls, client_id, key):
        client = StackExchangeClient(site='stackoverflow', client_id=client_id, key=key)
        return cls(client)

    def get_user_answers(self, user_id):
        return self.client.users.ids(user_id).answers.get(filter='withbody')

    def get_questions(self, question_id_or_ids):
        throttle_limit = 100

        id_chunks = [question_id_or_ids[i:i+throttle_limit] 
                     for i in xrange(0, len(question_id_or_ids), throttle_limit)]

        questions = []
        for chunk in id_chunks:
            questions.extend(self.client.questions.ids(chunk).get(filter='withbody'))

        return questions

    def get_candidate_questions(self, tags):
        questions = []
        for tag in tags:
            questions.extend(self.client.search.get(tagged=tag, filter='withbody'))

        return questions


class Model(object):
    
    def train(self, data_source, feature_extractor):
        raise NotImplementedError(
            EXCEPTION_FORMATTER.format(method_name='train', class_name='Model'))

    def recommend(self, data_source, user_id, number):
        raise NotImplementedError(
            EXCEPTION_FORMATTER.format(method_name='recommend', class_name='Model'))

    def test(self, data_source, feature_extractor, truth_function):
        raise NotImplementedError(
            EXCEPTION_FORMATTER.format(method_name='recommend', class_name='Model'))


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

        working_double = [(q, self.extract_body_words(q)) for q in candidate_questions]
        scores = [(x[0], classifier.prob_classify(x[1]).prob(True)) for x in working_double]
        scores.sort(key = lambda x: x[1], reverse=True)

        return scores[:5]

    def extract_body_words(self, question):
        body = question['body']
        word_list = tp.pull_stop_words(tp.simplify(tp.strip_tags(body)))
        return dict((w,1) for w in word_list)

if __name__ == '__main__':
    model = NaiveBayesBody()
    data_source = LiveSource.from_credentials(client_id=1962, key='IHEAzrM4kaVEBHGcLOP)tQ((')

    recommendations = model.recommend(data_source, user_id=1144035, number=5)




