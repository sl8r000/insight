import collections
from stack_exchange_client import StackExchangeClient
import text_processing as tp

def _extract_body_words(question):
    body = question['body']

    word_list = tp.pull_stop_words(tp.simplify(tp.strip_tags(body)))

    return collections.defaultdict(lambda x: 0, dict((w, 1) for w in word_list))


def recommend(client, user_id):
    user_answers = client.users.ids(user_id).answers.get()
    answered_questions_ids = [a['question_id'] for a in user_answers]
    accepted_ids = set(a['question_id'] for a in user_answers if a['is_accepted'])
    answered_questions = client.questions.ids(answered_questions_ids).get(filter='withbody')

    tags_lists = [q['tags'] for q in answered_questions if q['question_id'] in accepted_ids]
    tags = itertools.chain(*tags_lists)
    top_tags = [x[0] for x in collections.Counter(tags).most_common(3)]
    tag_matches_lists = [client.search.get(tagged=tag, filter='withbody') for tag in top_tags]
    candidate_questions = list(itertools.chain(*tag_matches_lists))

    training_data = []
    for q in answered_questions:
        data_point = (_extract_body_words(q), q['question_id'] in accepted_ids)
        training_data.append(data_point)

    classifier = nltk.NaiveBayesClassifier.train(training_data)

    scores = [(q, classifier.prob_classify(_extract_body_words(q))) for q in candidate_questions]

    return scores