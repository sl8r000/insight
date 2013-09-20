import pymongo
import time

from website import config
from database_population import settings
from database_population.methods import tagged_questions
from database_population.log import logger
from stack_exchange.stack_exchange_client import StackExchangeClient

USER_FILTER = '!bWWJdia*x26uv)'

if __name__ == '__main__':
    mongo_client = pymongo.MongoClient(settings.DATABASE_URL)
    stack_overflow_client = StackExchangeClient(site='stackoverflow', 
                                                                     client_id=settings.STACK_EXCHANGE_CLIENT_ID,
                                                                     key=settings.STACK_EXCHANGE_KEY)

    extant_tags = set(mongo_client.tagged_questions.collection_names())
    all_tags = set(sum(config.user_id_to_tags.values(), []))
    top_100_tags = list(all_tags - extant_tags)

    logger.info('Getting questions for the tags {}'.format(top_100_tags))

    for tag in top_100_tags:
        start_time = time.time()

        tagged_questions.populate_database(stack_overflow_client=stack_overflow_client,
                                                          database_client=mongo_client, 
                                                          tag=tag,
                                                          limit=1000)
        end_time = time.time()
        print 'Finished with tag {} in {} seconds'.format(tag, end_time - start_time)
        time.sleep(2)