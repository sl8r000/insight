import collections
import itertools

from model import Model
import nltk
from stack_exchange import text_processing as tp


class TitleBodyBayes(object):
    def __init__(self):
        self.title_model = None
        self.body_model = None

    def train(self, labeled_questions):
        title_training_data = []
        body_training_data = []
        for labeled_question in labeled_questions:
            question, label = labeled_question['question'], labeled_question['answer_accepted']
            body_training_data.append((TaggedBayesCombo.extract_body_words(question), label))
            title_training_data.append((TaggedBayesCombo.extract_title_words(question), label))

        self.title_model = nltk.NaiveBayesClassifier.train(title_training_data)
        self.body_model = nltk.NaiveBayesClassifier.train(body_training_data)

    def score(self, question):
        title_score = self.title_model.prob_classify(TaggedBayesCombo.extract_title_words(question)).prob(True)
        body_score = self.body_model.prob_classify(TaggedBayesCombo.extract_body_words(question)).prob(True)

        # print TaggedBayesCombo.extract_body_words(question)
        return body_score

class TaggedBayesCombo(Model):
    NUMBER_OF_TAGS = 3

    def train(self, dataset):
        self._user_models = dict()
        for user_id in dataset:
            tag_lists = [training_pair['question']['tags'] for training_pair in dataset[user_id]]
            all_tags = itertools.chain(*tag_lists)
            tag_counts = collections.Counter(all_tags)
            top_tags = set([count[0] for count in tag_counts.most_common(self.NUMBER_OF_TAGS)])
            tagged_training_data = collections.defaultdict(lambda: [])
            for training_pair in dataset[user_id]:
                if top_tags.isdisjoint(set(training_pair['question']['tags'])):
                    tagged_training_data['__default'].append(training_pair)
                    continue
                else:
                    for tag in top_tags:
                        if tag in training_pair['question']['tags']:
                            tagged_training_data[tag].append(training_pair)

            self._user_models[user_id] = dict()
            for tag in tagged_training_data:
                model = TitleBodyBayes()
                model.train(tagged_training_data[tag])
                self._user_models[user_id][tag] = model

    def test(self, dataset, top_number=10):
        accuracy_per_user = dict()
        for user_id in dataset:
            tagged_models = self._user_models[user_id]
            scored_questions = []
            for testing_pair in dataset[user_id]:
                tag_scores = dict()
                if set(testing_pair['question']['tags']).isdisjoint(tagged_models.keys()):
                    default_score = tagged_models['__default'].score(testing_pair['question'])
                    tag_scores['__default'] = default_score
                else:
                    for tag in tagged_models:
                        if tag in testing_pair['question']['tags']:
                            tag_score = tagged_models[tag].score(testing_pair['question'])
                            tag_scores[tag] = tag_score
                print tag_scores, testing_pair['answer_accepted']
                score = min(tag_scores.values())
                scored_questions.append((score, testing_pair['answer_accepted'], testing_pair['question']['question_id']))

            scored_questions.sort(key=lambda x: x[0], reverse=True)
            score = sum(1 for record in scored_questions[:top_number] if record[1] == True) / float(top_number)
            accuracy_per_user[user_id] = score

        return accuracy_per_user

    @classmethod
    def extract_title_words(self, question):
        title = question['title']
        word_list = tp.pull_stop_words(tp.simplify(tp.strip_tags(title)))
        return dict((w,1) for w in word_list)

    @classmethod
    def extract_body_words(self, question):
        if 'body' not in question:
            return {}
        body = question['body']
        word_list = tp.pull_stop_words(tp.simplify(tp.strip_tags(body)))
        return dict((w,1) for w in word_list)