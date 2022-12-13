"""This module implements the endpoint functions for pushing data
to and from the post organizer."""
import os
import secrets
from typing import NoReturn, Union

from flask import abort, request, Response

from postorganizer.controller import logging
from postorganizer.controller.safefileio import get_safe_path, pop_file
from postorganizer.router.app import FLASK_APP

@FLASK_APP.route('/', defaults={'path': ''}, methods=['GET'])
@FLASK_APP.route('/<path:path>', methods=['GET'])
def get(path: str) -> Union[Response, NoReturn]:
    """This function registers a catch-all route for handling GET
    requests.

    Args:
        path:
            The path being requested.

    Returns:
        HTTP response or no response.
    """
    try:
        data, create_time = pop_file(get_safe_path(path))
        response = Response(data)
        response.headers['CREATE_TIME'] = create_time
        logging.info(f'{len(data)} bytes from {path}')
        return response
    except (IndexError, OSError):
        logging.warning(f'{path} is empty')
        return abort(404)
    except Exception as exception: # pylint: disable=broad-except
        logging.error(f'{path} raised {exception}')
        return abort(500)

@FLASK_APP.route('/', defaults={'path': ''}, methods=['POST'])
@FLASK_APP.route('/<path:path>', methods=['POST'])
def post(path: str) -> Union[Response, NoReturn]:
    """This function registers a catch-all route for handling POST
    requests.

    Args:
        path:
            The path being requested.

    Returns:
        HTTP response or no response.
    """
    try:
        safe_path = get_safe_path(path, file_name=secrets.token_hex(15))
        os.makedirs(safe_path.directory, exist_ok=True)
        with open(safe_path.fq_name, 'wb') as file:
            file.write(request.data)
            file.close()
        logging.info(f'{len(request.data)} bytes to {path}')
        return Response(request.data)
    except Exception as exception: # pylint: disable=broad-except
        logging.error(f'{path} raised {exception}')
        return abort(500)
