from database_population.log import logger

PAGESIZE = 100
QUESTION_FILTER = '!.JEoc0rKopGMTGBW1K3m_MjFMiLgo'
ANSWER_FILTER = '!SrhU5Yqg3GWv2bQrOU'
DEFAULT_DB_NAME = 'user_questions'


def get_questions(stack_overflow_client, user_id, limit):
    logger.info('Getting questions for user {}'.format(user_id))

    all_question_ids = []
    last_page = limit/PAGESIZE + 1
    for page in range(1, last_page):
        raw_answers = stack_overflow_client.users.ids(user_id).answers.get(pagesize=PAGESIZE, page=page, filter=ANSWER_FILTER)
        question_ids = [answer['question_id'] for answer in raw_answers]
        all_question_ids.extend(question_ids)
        logger.debug('Getting Answers: Finished with page {} out of {} total'.format(page, last_page))

    questions = []
    for index in range(0, len(all_question_ids), PAGESIZE):
        chunk_start, chunk_end = index, index + PAGESIZE
        chunk = all_question_ids[chunk_start:chunk_end]

        questions.extend(stack_overflow_client.questions.ids(chunk).get(pagesize=PAGESIZE, filter=QUESTION_FILTER))
        logger.debug('Getting Questions: Finished with chunk [{}:{}]'.format(chunk_start, chunk_end))

    return questions


def write_questions(database_client, questions, collection_name, db_name=DEFAULT_DB_NAME):

    for index in range(0, len(questions), 1000):
        these_questions = questions[index:index+1000]
        database_client[db_name][collection_name].insert(these_questions)


def populate_database(stack_overflow_client, database_client, user_id, limit):
    questions = get_questions(stack_overflow_client, user_id, limit)
    write_questions(database_client, questions, str(user_id))
