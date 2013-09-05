from data_source import DataSource

class DictSource(DataSource):

    def __init__(self, data):
        self.answers = data.answers
        self.questions = data.questions
        self.candidate_questions = data.candidate_questions

    def get_user_answers(self, user_id):
        return [a for a in self.answers if a['user_id'] == user_id]

    def get_questions(self, question_id_or_ids):
        id_set = set(question_id_or_ids) if isinstance(question_id_or_ids, list) else set([question_id_or_ids])
        return [q for q in self.questions if q['question_id'] in id_set]

    def get_candidate_questions(self, tags):
        tag_set = set(tags)
        return [q for q in self.candidate_questions if not set(q['tags']).isdisjoint(tag_set)]
