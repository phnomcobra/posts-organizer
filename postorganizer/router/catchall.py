"""This module implements the endpoint functions for pushing data
to and from the post organizer."""
import os
import secrets

from flask import abort, request, Response

from postorganizer.controller import logging
from postorganizer.router.app import FLASK_APP
from postorganizer.service.safefileio import get_safe_path, pop_file

@FLASK_APP.route('/', defaults={'path': ''}, methods=['GET'])
@FLASK_APP.route('/<path:path>', methods=['GET'])
def get(path: str) -> Response:
    """This function registers a catch-all route for handling GET
    requests.

    Args:
        path:
            The path being requested.

    Returns:
        HTTP response.
    """
    try:
        data, create_time = pop_file(get_safe_path(path))
        response = Response(data)
        response.headers['CREATE_TIME'] = create_time
        logging.info(f'{len(data)} bytes from {path}')
        return response
    except (IndexError, OSError):
        logging.warning(f'{path} is empty')
        abort(404)
    except Exception as exception:
        logging.error(f'{path} raised {exception}')
        abort(500)

@FLASK_APP.route('/', defaults={'path': ''}, methods=['POST'])
@FLASK_APP.route('/<path:path>', methods=['POST'])
def post(path: str) -> Response:
    """This function registers a catch-all route for handling POST
    requests.

    Args:
        path:
            The path being requested.

    Returns:
        HTTP response.
    """
    try:
        safe_path = get_safe_path(path, file_name=secrets.token_hex(15))
        os.makedirs(safe_path.directory, exist_ok=True)
        file = open(safe_path.fq_name, 'wb')
        file.write(request.data)
        file.close()
        logging.info(f'{len(request.data)} bytes to {path}')
        return Response(request.data)
    except Exception as exception:
        logging.error(f'{path} raised {exception}')
        abort(500)
