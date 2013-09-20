import os
import pickle
import pymongo

from website import config, classifier

if __name__ == '__main__':
    mongo = pymongo.MongoClient(config.DATABASE_URL)
    user_ids = mongo.user_questions.collection_names()
    for user_id in user_ids:
        if 'index' in user_id:
            continue
        good = list(mongo.user_questions[user_id].find(limit=2000, fields=['body', 'tags', 'question_id']))
        user_tags = config.user_id_to_tags[int(user_id)]
        bad = []
        for tag in user_tags:
            if tag not in mongo.tagged_questions.collection_names():
                continue
            bad.extend(list(mongo.tagged_questions[tag].find(limit=1000, fields=['body', 'tags', 'question_id'])))

        clf = classifier.Classifier()
        clf.train(good, bad)
        if not os.path.exists(user_id):
            os.makedirs(user_id)
        with open('{}/classifier.pkl'.format(user_id), 'wb') as stream:
            pickle.dump(clf, stream)
        print user_id