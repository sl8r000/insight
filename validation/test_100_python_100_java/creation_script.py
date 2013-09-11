import argparse
import json
import time

from stack_exchange.stack_exchange_client import StackExchangeClient

def fetch_dataset(stack_overflow_client):
    ocaml_questions = stack_overflow_client.search.get(tagged='ocaml', filter='withbody')
    java_questions = stack_overflow_client.search.get(tagged='java', filter='withbody')

    labeled_python = [{'question': question, 'answer_accepted': True} for question in ocaml_questions]
    labeled_java = [{'question': question, 'answer_accepted': False} for question in java_questions]
    labeled_questions = labeled_python + labeled_java

    return {'fake_user': labeled_questions}

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
