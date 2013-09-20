from flask import Flask, render_template, jsonify
import pickle

import config
from stack_exchange.stack_exchange_client import StackExchangeClient
import util

app = Flask(__name__, template_folder='UI', static_folder='UI')

@app.route('/')
def show_index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    return error

@app.route('/recommended/<user_id>')
def give_recommendations(user_id):
    user_id = util.lookup_user_id(user_id)

    user_classifier_path = '../cache/{}/classifier.pkl'.format(user_id)
    with open(user_classifier_path) as stream:
        classifier = pickle.load(stream)

    user_tags = util.lookup_user_tags(user_id)

    client = StackExchangeClient(site='stackoverflow', client_id=config.STACK_EXCHANGE_KEY, key=config.STACK_EXCHANGE_KEY)
    candidate_questions = []
    for tag in user_tags:
        candidate_questions.extend(client.questions.get(order='desc', sort='creation', tagged=tag, filter='withbody'))

    recommendations = classifier.get_recommendations(candidate_questions, 5)
    return jsonify({'result': recommendations})

if __name__ == '__main__':
    app.run(port=8000, debug=True)
