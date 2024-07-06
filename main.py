"""This module implements the functions and flask app for pushing data
to and from the post organizer."""
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

from postorganizer.controller.expiration import expire_posts
from postorganizer.controller import logging
from postorganizer.model.config import CONFIG
from postorganizer.router.app import FLASK_APP
from postorganizer.router.catchall import get, post # pylint: disable=unused-import

scheduler = BackgroundScheduler()
scheduler.add_job(expire_posts, 'cron', minute='*')

def on_shutdown():
    """This function is called at exit to stop the scheduler."""
    logging.info('shutting down scheduler')
    scheduler.shutdown()
    logging.info('scheduler shutdown')

atexit.register(on_shutdown)

if __name__ == '__main__':
    logging.info('starting posts organizer')
    logging.info(CONFIG)
    scheduler.start()
    logging.info('scheduler started')

    FLASK_APP.run(host=str(CONFIG.server.host), port=CONFIG.server.port)
