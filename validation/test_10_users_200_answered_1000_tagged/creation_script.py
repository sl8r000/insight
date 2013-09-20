import argparse
import json
import time

from stack_exchange.stack_exchange_client import StackExchangeClient
from website import util

def fetch_dataset(stack_overflow_client):
    users = stack_overflow_client.users.get(pagesize=10)
    user_ids = [int(user['user_id']) for user in users]

    user_question_lists = dict.fromkeys(user_ids)
    for user_id in user_ids:
        user_answers = []
        for i in range(2):
            user_answers.extend(stack_overflow_client.users.ids(user_id).answers.get(pagesize=100, page=i+1))

        user_question_ids = [a['question_id'] for a in user_answers]
        good_questions = []
        for i in range(2):
            these_questions = stack_overflow_client.questions.ids(user_question_ids[i*100:(i+1)*100]).get(filter='withbody', pagesize=100)
            good_questions.extend(these_questions)

        bad_questions = []
        for tag in util.lookup_user_tags(user_id):
            tagged_questions = []
            for i in range(3):
                these_tagged_questions = stack_overflow_client.questions.get(order='desc', sort='creation', tagged=tag, filter='withbody')
                tagged_questions.extend(these_tagged_questions)
            eligible_questions = [q for q in tagged_questions if q['question_id'] not in user_question_ids]
            eligible_questions = eligible_questions[:200]
            bad_questions.extend(eligible_questions)

        labeled_questions = []
        labeled_questions.extend([{'question': q, 'answer_accepted': True} for q in good_questions])
        labeled_questions.extend([{'question': q, 'answer_accepted': False} for q in bad_questions])
        user_question_lists[user_id] = labeled_questions

    return user_question_lists

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--client_id', help='Stack Overflow client_id', required=True)
    parser.add_argument('-k', '--key', help='Stack Overflow key', required=True)
    parser.add_argument('-f', '--file', help='JSON file destination', default=None)
    args = parser.parse_args()

    client = StackExchangeClient('stackoverflow', args.client_id, args.key)
    dataset = fetch_dataset(client)

    if args.file is not None:
        with open(args.file, 'w') as stream:
            json.dump(dataset, stream)
