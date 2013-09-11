import argparse
import json
import time

from stack_exchange.stack_exchange_client import StackExchangeClient

def fetch_dataset(stack_overflow_client):
    users = stack_overflow_client.users.get(pagesize=10)
    user_ids = [int(user['user_id']) for user in users]

    user_question_lists = dict.fromkeys(user_ids)
    for user_id in user_ids:
        user_answers_1 = stack_overflow_client.users.ids(user_id).answers.get(pagesize=100, page=1)
        user_answers_2 = stack_overflow_client.users.ids(user_id).answers.get(pagesize=100, page=2)
        random_answers_1 = stack_overflow_client.answers.get(pagesize=100, page=1)
        random_answers_2 = stack_overflow_client.answers.get(pagesize=100, page=2)

        all_answers = user_answers_1 + user_answers_2 + random_answers_1 + random_answers_2

        question_ids = [answer['question_id'] for answer in all_answers]
        accepted_question_ids = [answer['question_id'] for answer in user_answers_1 + user_answers_2 if answer['is_accepted']]

        questions_1 = stack_overflow_client.questions.ids(question_ids[:100]).get(filter='withbody', pagesize=100)
        questions_2 = stack_overflow_client.questions.ids(question_ids[100:200]).get(filter='withbody', pagesize=100)
        questions_3 = stack_overflow_client.questions.ids(question_ids[200:300]).get(filter='withbody', pagesize=100)
        questions_4 = stack_overflow_client.questions.ids(question_ids[300:]).get(filter='withbody', pagesize=100)

        questions = questions_1 + questions_2 + questions_3 + questions_4

        labeled_questions = [{'question': question, 'answer_accepted': question['question_id'] in accepted_question_ids}
                             for question in questions]

        user_question_lists[user_id] = labeled_questions

        time.sleep(1)

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
