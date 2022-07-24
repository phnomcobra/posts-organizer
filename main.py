"""This module implements the functions and flask app for pushing data
to and from the post organizer."""
from collections import namedtuple
import hashlib
import os
import secrets
from threading import Lock
from typing import Tuple

from flask import abort, Flask, request, Response

ROOT_BOXES_DIRECTORY = './boxes'
HOST = '0.0.0.0'
PORT = 8080
FILE_LOCK = Lock()
FLASK_APP = Flask(__name__)

SafePath = namedtuple('SafePath', ['directory', 'file_name', 'fq_name'])

def hash_token(token: str) -> str:
    """This function computes a SHA256 hash from a string.

    Args:
        token:
            String being encoded and hashed.

    Returns:
        A hex digest as a string."""
    sha256 = hashlib.sha256()
    sha256.update(token.encode())
    return sha256.hexdigest()

def get_safe_path(path_str: str, file_name: str = None) -> SafePath:
    """This function generates a safe path from a path string and an optional
    file name. The path is tokenized. The tokens themselves are hashed to prevent
    enumeration of the file system. A path is built by a path join using a combination
    a base directory, and the hashed tokens.

    Args:
        path_str:
            Path string to be tokenized and hashed.

        file_name:
            Optional file_name that is used as an additional token to be hashed and
            joined.

    Returns:
        A named tuple of consisting of the directory, file name, and fully qualified
        name.
    """
    safe_tokens = [hash_token(x) for x in path_str.split('/')]
    if file_name is not None:
        safe_tokens.append(hash_token(file_name))
    directory = os.path.join('/'.join([ROOT_BOXES_DIRECTORY] + safe_tokens[:-1]))
    file_name = safe_tokens[-1]
    fq_name = os.path.join('/'.join([directory, file_name]))
    return SafePath(directory=directory, file_name=file_name, fq_name=fq_name)

def pop_file(safe_path: SafePath) -> Tuple[bytes, float]:
    """This function "pops" a file by reading it from a directory specified
    by the safe path into a binary, deleting the file, and returning it. The
    first file encountered in the directory's listing is the file that's
    read.

    Args:
        safe_path:
            The SafePath tuple of the directory to read from.

    Returns:
        A tuple of file contents as bytes and creation time."""
    try:
        FILE_LOCK.acquire()
        data = None
        create_time = None

        for file_name in os.listdir(safe_path.fq_name):
            fq_name = os.path.join(safe_path.fq_name, file_name)
            if os.path.isfile(fq_name):
                create_time = os.path.getctime(fq_name)
                file = open(fq_name, 'rb')
                data = file.read()
                file.close()
                os.remove(fq_name)
                break

        if data is None:
            raise IndexError
    finally:
        FILE_LOCK.release()
    return (data, create_time)

@FLASK_APP.route('/', defaults={'path': ''}, methods=['GET'])
@FLASK_APP.route('/<path:path>', methods=['GET'])
def catch_all_gets(path: str) -> Response:
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
        return response
    except (IndexError, OSError):
        abort(404)

@FLASK_APP.route('/', defaults={'path': ''}, methods=['POST'])
@FLASK_APP.route('/<path:path>', methods=['POST'])
def catch_all_posts(path: str) -> Response:
    """This function registers a catch-all route for handling POST
    requests.

    Args:
        path:
            The path being requested.

    Returns:
        HTTP response.
    """
    safe_path = get_safe_path(path, file_name=secrets.token_hex(15))
    os.makedirs(safe_path.directory, exist_ok=True)
    file = open(safe_path.fq_name, 'wb')
    file.write(request.data)
    file.close()
    return Response(request.data)

if __name__ == '__main__':
    FLASK_APP.run(host=HOST, port=PORT)
