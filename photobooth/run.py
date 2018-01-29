#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import sys
from argparse import ArgumentParser

# Import Gui photobooth libs
try:
    # Get current directory
    root_directory = os.path.dirname(os.path.realpath(__file__))

    sys.path.append('{}/libs/'.format(root_directory))

    from gui import Gui
    from configuration import Configuration
except Exception as e:
    logging.error("Failed to import class from libs folder: {}".format(e))


def set_logging(lvl=logging.INFO):
    """
    Set logging output.
    :param lvl: Log level.
    :type lvl: Int
    """
    log_format = '%(asctime)-15s - %(levelname)s - %(message)s'
    logging.basicConfig(level=lvl, format=log_format)


def check_pictures_directory(pictures_directory):
    """
    Check if picture directory exist and is writable.
    :param pictures_directory: Path where to store pictures.
    """
    # Check if output directory is writable.
    try:
        if os.path.isdir(pictures_directory):
            open(os.path.join(pictures_directory, "photobooth.txt"), 'a').close()

            # delete test file
            os.remove("{}/{}".format(pictures_directory, "photobooth.txt"))

        else:
            raise os.error("Folder does not exists.")

    except os.error as e:
        raise os.error("Failed to write in {}: {}".format(pictures_directory, e))


if __name__ == "__main__":
    # Create script arguments parser
    args_parse = ArgumentParser("Run photobooth.")
    args_parse.add_argument("--config", "-c", metavar="file", help="Configuration file", required=True)
    args_parse.add_argument("--language", "-l", metavar="language", default="fr", help="choose application language.")

    params = args_parse.parse_args()

    # Extract config from configuration file.
    config = Configuration(params.config)

    # Check if output directory is writable.
    check_pictures_directory(config.pictures_directory)

    # Run Photobooth Frame
    try:
        photobooth = Gui(getattr(config, params.language)['title'], config.resolution['width'],
                         config.resolution['height'], getattr(config, params.language))
    except AttributeError:
        logging.error("Language {} not found.".format(params.language))
        exit(1)

    photobooth.run()
