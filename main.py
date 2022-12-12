"""This module implements the functions and flask app for pushing data
to and from the post organizer."""
from postorganizer.controller import logging
from postorganizer.model.config import CONFIG
from postorganizer.router.app import FLASK_APP
from postorganizer.router.catchall import get, post

if __name__ == '__main__':
    logging.info('Starting posts organizer')
    logging.info(CONFIG)
    FLASK_APP.run(host=str(CONFIG.server.host), port=CONFIG.server.port)
