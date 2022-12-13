"""This module implements the functions for expiring post files
and child directories."""
import os
import time

from postorganizer.controller import logging
from postorganizer.model.config import CONFIG

def expire_posts():
    """This function removes any post file whos age has exceeded
    the server's retention period. Additionally, any directory
    that has no files and no child directories is removed."""
    logging.info('expiring posts')

    # Walk the "boxes" directory and remove expiring files and
    # accumulate a list of empty directories to delete.
    num_files_removed = 0
    directories_to_remove = []
    for path, _current_directory, files in os.walk(CONFIG.paths.boxes):
        if len(os.listdir(path)) == 0 and len(files) == 0:
            directories_to_remove.append(path)

        for file in files:
            try:
                full_filename = os.path.join(path, file)
                removal_time = (
                    os.path.getctime(full_filename) + CONFIG.server.retention_seconds
                )
                if time.time() > removal_time:
                    os.remove(full_filename)
                    num_files_removed += 1
            except Exception as exception: # pylint: disable=broad-except
                logging.error(exception)

    num_directories_removed = 0
    for directory in directories_to_remove:
        try:
            os.rmdir(directory)
            num_directories_removed += 1
        except Exception as exception: # pylint: disable=broad-except
            logging.error(exception)

    if num_files_removed > 0:
        logging.warning(f'removed {num_files_removed} files')

    if num_directories_removed > 0:
        logging.warning(f'removed {num_directories_removed} directories')
