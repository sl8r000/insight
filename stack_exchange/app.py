from flask import Flask, render_template, jsonify

import data_source as ds

app = Flask(__name__)


@app.route('/')
def show_index():
    return render_template('index.html')

@app.route('/recommended/<user_id>')
def give_recommendations(user_id):
    model = ds.NaiveBayesBody()
    data_source = ds.LiveSource.from_credentials(client_id=1962, key='IHEAzrM4kaVEBHGcLOP)tQ((')

    recommendations = model.recommend(data_source, user_id=user_id, number=5)
    return jsonify({'result': recommendations})

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

if __name__ == '__main__':
    app.run(port=8000, debug=True)