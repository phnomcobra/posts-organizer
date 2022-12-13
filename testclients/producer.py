import logging
from random import randrange
from time import sleep
from urllib.request import urlopen, Request

logging.basicConfig(level=logging.DEBUG)

# Flask won't read any bytes in the payload without a content type.
headers = {
    'content-type': 'text/plain'
}

while True:
    try:
        i = randrange(0, 10)
        f = urlopen(
            Request(
                f'http://post-organizer:8080/{i}',
                data=f'Channel {i} data'.encode(),
                method='POST',
                headers=headers
            )
        )
    except Exception as e:
        logging.error(f'channel {i}: {e}')
    finally:
        sleep(1)
