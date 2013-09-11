import collections
import itertools

from model import Model

class TagsBaseline(Model):

    def train(self, dataset):
        self._most_common_tags = dict()
        for user_id in dataset:
            accepted_questions = [item['question'] for item in dataset[user_id] if item['answer_accepted']]
            tags = itertools.chain(*[question['tags'] for question in accepted_questions])
            tag_counts = collections.Counter(tags)
            self._most_common_tags[user_id] = set([count[0] for count in tag_counts.most_common(5)])

    def test(self, dataset, top_number):
        accuracy_per_user = dict()
        for user_id in dataset:
            triples = []
            for item in dataset[user_id]:
                question, label = item['question'], item['answer_accepted']
                tag_count = len(list(self._most_common_tags[user_id].intersection(set(question['tags']))))
                triples.append((tag_count, label, question['question_id']))

            triples.sort(key = lambda x: x[0], reverse=True)
            score = sum(1 for triple in triples[:top_number] if triple[1] == True)/float(top_number)
            accuracy_per_user[user_id] = score

        return accuracy_per_user
