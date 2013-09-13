from flask import Flask, render_template, jsonify
import os

from models.naive_bayes_body import NaiveBayesBody
from data_sources.live_source import LiveSource


app = Flask(__name__, template_folder='UI', static_folder='UI')


@app.route('/')
def show_index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    return error

@app.route('/recommended/<user_id>')
def give_recommendations(user_id):
    model = NaiveBayesBody()
    data_source = LiveSource.from_credentials(client_id=1962, key='IHEAzrM4kaVEBHGcLOP)tQ((')

    recommendations = model.recommend(data_source, user_id=22656, number=5)
    return jsonify({'result': recommendations})

if __name__ == '__main__':
    app.run(port=8000, debug=True)
