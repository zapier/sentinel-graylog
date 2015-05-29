import logging
import os
import sys
import time

import graypy
from redis.client import StrictRedis

SENTINEL_HOST = os.environ.get('SENTINEL_HOST', 'localhost')
SENTINEL_PORT = int(os.environ.get('SENTINEL_PORT', 26379))
GRAYLOG_HOST = os.environ.get('GRAYLOG_HOST', 'localhost')
LOGGING_HOSTNAME = os.environ.get('LOGGING_HOSTNAME')

VERBOSE = '-v' in sys.argv or os.environ.get('VERBOSE', '').lower() in ['true', 'yes']

logger = logging.getLogger('sentinel')

if GRAYLOG_HOST:
    handler = graypy.GELFHandler(GRAYLOG_HOST, 12201,
                                 localname=LOGGING_HOSTNAME)
    logger.setLevel(logging.INFO)

if not GRAYLOG_HOST or VERBOSE:
    handler = logging.StreamHandler()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s %(name)s %(levelname)s] %(message)s')
    handler.setFormatter(formatter)

logger.addHandler(handler)


def run_once():
    logger.debug('Connecting to Sentinel on {}:{}'.format(
        SENTINEL_HOST, SENTINEL_PORT))

    sentinel = StrictRedis(SENTINEL_HOST, SENTINEL_PORT)
    masters = sentinel.sentinel_masters()

    logger.debug('Sentinel reports {} monitored cluster(s)'.format(len(masters)))

    pubsub = sentinel.pubsub(ignore_subscribe_messages=True)
    pubsub.psubscribe('*')

    logger.debug('Subscribed and waiting for messages on all channels')

    for message in pubsub.listen():
        logger.info(u'{} {}'.format(message['channel'], message['data']))


def main():
    while True:
        try:
            run_once()
        except Exception as e:
            logger.exception(e)
            time.sleep(5)

if __name__ == '__main__':
    main()
