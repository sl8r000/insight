import pymongo
import time

from database_population import settings
from database_population.methods import user_answered_questions
from database_population.log import logger
from stack_exchange.stack_exchange_client import StackExchangeClient

USER_FILTER = '!bWWJdia*x26uv)'

if __name__ == '__main__':
    mongo_client = pymongo.MongoClient(settings.DATABASE_URL)
    stack_overflow_client = StackExchangeClient(site='stackoverflow', 
                                                                     client_id=settings.STACK_EXCHANGE_CLIENT_ID,
                                                                     key=settings.STACK_EXCHANGE_KEY)

    top_100_users = stack_overflow_client.users.get(pagesize=100, filter=USER_FILTER)
    top_100_users = top_100_users[47:50]
    logger.info('Getting questions for the users {}'.format(top_100_users))

    for user in top_100_users:
        start_time = time.time()
        user_id = user['user_id']
        answer_count = user['answer_count']

        user_answered_questions.populate_database(stack_overflow_client=stack_overflow_client,
                                                                           database_client=mongo_client, 
                                                                           user_id=user_id,
                                                                           limit=answer_count)
        end_time = time.time()
        print 'Finished with user {} in {} seconds'.format(user_id, end_time - start_time)
        time.sleep(2)
