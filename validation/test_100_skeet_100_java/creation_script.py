import argparse
import json

from stack_exchange.stack_exchange_client import StackExchangeClient

def fetch_dataset(stack_overflow_client):
    jon_skeet_id = 22656

    answers = []
    for i in range(1, 4):
        answers.extend(stack_overflow_client.users.ids(jon_skeet_id).answers.get(pagesize=100, page=i))

    question_ids = [answer['question_id'] for answer in answers]
    skeet_questions = []
    for i in range(1, 10):
        skeet_questions.extend(stack_overflow_client.questions.ids(question_ids[(i-1)*100:i*100]).get(filter='withbody', pagesize=100))

    java_questions = []
    for i in range(1, 21):
        java_questions.extend(stack_overflow_client.search.get(tagged='java', order='desc', sort='creation', filter='withbody', pagesize=100, page=i))

    labeled_questions = [{'question': question, 'answer_accepted': True} for question in skeet_questions]
    labeled_questions.extend([{'question': question, 'answer_accepted': False} for question in java_questions])

    return {jon_skeet_id: labeled_questions}

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