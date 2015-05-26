import logging
import os
import sys
import time

import graypy
from redis.client import StrictRedis

GRAYLOG_ADDRESS = os.environ.get('GRAYLOG_ADDRESS')
SENTINEL_ADDRESS = os.environ.get('SENTINEL_ADDRESS')
SENTINEL_PORT = os.environ.get('SENTINEL_PORT')

VERBOSE = '-v' in sys.argv or os.environ.get('VERBOSE', '').lower() in ['true', 'yes']

logger = logging.getLogger('sentinel')

if GRAYLOG_ADDRESS:
    handler = graypy.GELFHandler(GRAYLOG_ADDRESS, 12201)
    logger.setLevel(logging.INFO)

if not GRAYLOG_ADDRESS or VERBOSE:
    handler = logging.StreamHandler()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s %(name)s %(levelname)s] %(message)s')
    handler.setFormatter(formatter)

logger.addHandler(handler)


def main():
    if not (SENTINEL_ADDRESS and SENTINEL_PORT):
        logger.error(
            'Both SENTINEL_ADDRESS and SENTINEL_PORT environment variables '
            'must be provided.')
        sys.exit(-1)

    logger.debug('Connecting to Sentinel on {}:{}'.format(
        SENTINEL_ADDRESS, SENTINEL_PORT))

    sentinel = StrictRedis(SENTINEL_ADDRESS, SENTINEL_PORT)
    masters = sentinel.sentinel_masters()

    logger.debug('Sentinel reports {} monitored cluster(s)'.format(len(masters)))

    pubsub = sentinel.pubsub(ignore_subscribe_messages=True)
    pubsub.psubscribe('*')

    logger.debug('Subscribed and waiting for messages on all channels')

    for message in pubsub.listen():
        logger.info(u'{} {}'.format(message['channel'], message['data']))

if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            logger.exception(e)
            time.sleep(5)
