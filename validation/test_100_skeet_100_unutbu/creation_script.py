import argparse
import json

from stack_exchange.stack_exchange_client import StackExchangeClient

def fetch_dataset(stack_overflow_client):
    user_ids = [22656, 190597]

    user_question_lists = dict.fromkeys(user_ids)
    for user_id in user_ids:
        other_user_id = 22656 if user_id == 190597 else 190597
        
        user_answers = stack_overflow_client.users.ids(user_id).answers.get(pagesize=100)
        other_user_answers = stack_overflow_client.users.ids(other_user_id).answers.get(pagesize=100)

        user_question_ids = [answer['question_id'] for answer in user_answers]
        other_user_question_ids = [answer['question_id'] for answer in other_user_answers]
        accepted_question_ids = [answer['question_id'] for answer in user_answers if answer['is_accepted']]

        user_questions = stack_overflow_client.questions.ids(user_question_ids).get(filter='withbody', pagesize=100)
        # user_questions = [question for question in user_questions if question['question_id'] in accepted_question_ids]
        other_user_questions = stack_overflow_client.questions.ids(other_user_question_ids).get(filter='withbody', pagesize=100)
        questions = user_questions + other_user_questions

        labeled_questions = [{'question': question, 'answer_accepted': question['question_id'] in accepted_question_ids}
                             for question in questions]

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