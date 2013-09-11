from models.sk_learn import SKLearnBagOfWords

borat_train_text = ['MongoDB change name to MongoDB. Will take a few day before replica sets reflect change.',
                            'Data Science is statistics on a Mac.',
                            'Feel I get when I no bother to boost data before I apply training model',
                            'CEO friend say shift to treat data as most strategic asset very welcome change, he no longer need to pretend employee is important asset.',
                            'The unexamined data is not worth storing.']

borat_test_text = ['I quit consulting job for become VC Data Scientist in Residence. Job remain very similar, sell idea that no does work to large enterprise.',
                           'At BigDataBorat Lab backend engineer is call Data Scientist, frontend engineer is call Data Creationist']

lana_train_text = ['Looking forward to seeing you for the farewell project. I adore you and thank you for inspiring me. TROPICO ',
                           'I can\'t wait to see you at our premiers for Tropico at the Hollywood Forever Cemetery and in NYC.',
                           'TROPICO - a 30 minute film coming to a city near your. Premier dates coming soon. Lots of Love, Lana Del Rey',
                           'Pre-order The Great Gatsby soundtrack and get Young & Beautiful HERE:',
                           'of people in each territory with innovative ideas aimed at forwarding technology and improving sustainability.']

lana_test_text = ['GATSBY',
                         'The first photo from the Dreamland sessions by my sister and photographer']

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

clf = RandomForestClassifier()
vectorizer = TfidfVectorizer()
vectorized_train = vectorizer.fit_transform(borat_train_text + lana_train_text)

clf.fit(vectorized_train.toarray(), [1, 1, 1, 1 ,1, 0, 0, 0, 0, 0])

print 1, clf.predict(vectorizer.transform([borat_test_text[0]]).toarray()), clf.predict_proba(vectorizer.transform([borat_test_text[0]]).toarray()), borat_test_text[0]
print 1, clf.predict(vectorizer.transform([borat_test_text[1]]).toarray()), clf.predict_proba(vectorizer.transform([borat_test_text[1]]).toarray()), borat_test_text[1]
print 0, clf.predict(vectorizer.transform([lana_test_text[0]]).toarray()), clf.predict_proba(vectorizer.transform([lana_test_text[0]]).toarray()), lana_test_text[0]
print 0, clf.predict(vectorizer.transform([lana_test_text[1]]).toarray()), clf.predict_proba(vectorizer.transform([lana_test_text[1]]).toarray()), lana_test_text[1]


training_questions = []
for borat_line in borat_train_text:
    training_questions.append({'question': {'body': borat_line, 'question_id': borat_line}, 'answer_accepted': True})
for lana_line in lana_train_text:
    training_questions.append({'question': {'body': lana_line, 'question_id': lana_line}, 'answer_accepted': False})

testing_questions = []
for borat_line in borat_test_text:
    testing_questions.append({'question': {'body': borat_line, 'question_id': borat_line}, 'answer_accepted': True})
for lana_line in lana_test_text:
    testing_questions.append({'question': {'body': lana_line, 'question_id': lana_line}, 'answer_accepted': False})

model = SKLearnBagOfWords(RandomForestClassifier)

model.train({'123': training_questions})
model.test({'123': testing_questions}, top_number=2)
