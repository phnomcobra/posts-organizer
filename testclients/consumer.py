import logging
from random import randrange
from time import sleep
from urllib.request import urlopen, Request

logging.basicConfig(level=logging.DEBUG)

while True:
    try:
        i = randrange(0, 10)
        while True:
            f = urlopen(
                Request(
                    f'http://post-organizer:8080/{i}',
                    method='GET'
                )
            )
            logging.info(f.read())
    except Exception as e: # pylint: disable=broad-exception-caught
        logging.error(f'channel {i}: {e}') # pylint: disable=logging-fstring-interpolation
    finally:
        sleep(2)
