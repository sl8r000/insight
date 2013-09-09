from data_source import DataSource
from stack_exchange.stack_exchange_client import StackExchangeClient


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
            questions.extend(self.client.search.advanced.get(tagged=tag, filter='withbody', accepted=False))

        return questions
