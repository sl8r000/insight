import argparse
import json

from stack_exchange.stack_exchange_client import StackExchangeClient

def fetch_dataset(stack_overflow_client):
    users = stack_overflow_client.users.get(pagesize=10)
    user_ids = [int(user['user_id']) for user in users]

    bad_questions = []
    for i in range(20):
        these_questions = stack_overflow_client.questions.get(order='desc', sort='creation', filter='withbody')
        bad_questions.extend(these_questions)

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
