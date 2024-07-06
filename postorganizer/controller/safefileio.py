"""This module implements functions for servicing hashed file paths and popping
files for the webserver to serve."""
from collections import namedtuple
import hashlib
import os
from threading import Lock
from typing import Tuple

from postorganizer.model.config import CONFIG

FILE_LOCK = Lock()
directory_lists = {}

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
    directory = os.path.join('/'.join([str(CONFIG.paths.boxes)] + safe_tokens[:-1]))
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

        if (safe_path.directory not in directory_lists or
            not directory_lists[safe_path.directory]
        ):
            directory_lists[safe_path.directory] = os.listdir(safe_path.fq_name)

        while directory_lists[safe_path.directory]:
            file_name = directory_lists[safe_path.directory].pop()
            fq_name = os.path.join(safe_path.fq_name, file_name)

            # refresh directory listing when a miss is encountered
            if not os.path.exists(fq_name):
                directory_lists[safe_path.directory] = os.listdir(safe_path.fq_name)
                continue

            if os.path.isfile(fq_name):
                create_time = os.path.getctime(fq_name)
                with open(fq_name, 'rb') as file:
                    data = file.read()
                    file.close()
                os.remove(fq_name)

        if data is None:
            # prune empty directory keys
            del directory_lists[safe_path.directory]
            raise IndexError
    finally:
        FILE_LOCK.release()
    return (data, create_time)
