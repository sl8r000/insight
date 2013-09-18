from flask import Flask, render_template, jsonify

import config
from data_sources.live_source import LiveSource
from models.naive_bayes_body import NaiveBayesBody
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

    model = NaiveBayesBody()
    data_source = LiveSource.from_credentials(client_id=config.STACK_EXCHANGE_CLIENT_ID, 
                                                                   key=config.STACK_EXCHANGE_KEY)

    recommendations = model.recommend(data_source, user_id=user_id, number=5)
    return jsonify({'result': recommendations})

if __name__ == '__main__':
    app.run(port=8000, debug=True)
