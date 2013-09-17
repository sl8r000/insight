PAGESIZE = 100
QUESTION_FILTER = '!.JEoc0rKopGMTGBW1K3m_MjFMiLgo'
ANSWER_FILTER = '!SrhU5Yqg3GWv2bQrOU'
DEFAULT_DB_NAME = 'tagged_questions'


def get_questions(stack_overflow_client, tag, limit):
    all_questions = []
    for index in range(0, limit, PAGESIZE):
        questions = stack_overflow_client.search.get(tagged=tag, pagesize=PAGESIZE, filter=QUESTION_FILTER)
        all_questions.extend(questions)

    return all_questions


def write_questions(database_client, questions, collection_name, db_name=DEFAULT_DB_NAME):
    database_client[db_name][collection_name].insert(questions)


def populate_database(stack_overflow_client, database_client, tag, limit):
    questions = get_questions(stack_overflow_client, tag, limit)
    write_questions(database_client, questions, str(tag))