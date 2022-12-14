"""This module exists to allow the Flask application to be imported
by entry point and router modules."""
from flask import Flask

FLASK_APP = Flask('post-organizer-api')
