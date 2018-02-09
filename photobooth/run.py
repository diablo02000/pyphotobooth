#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import sys
from argparse import ArgumentParser

"""
    Try to import Photobooth apps libs.
"""
try:
    # Get current directory
    libs_directory = "{}/libs/".format(os.path.dirname(os.path.realpath(__file__)))

    sys.path.append(libs_directory)

    from gui import Gui
    from configuration import Configuration
except Exception as e:
    logging.error("Failed to import class from libs folder: {}".format(e))
    exit(2)


def set_logging(lvl=logging.INFO):
    """
    Set logging output.
    :param lvl: Log level.
    :type lvl: Int
    """
    log_format = '%(asctime)-15s - %(levelname)s - %(message)s'
    logging.basicConfig(level=lvl, format=log_format)


def check_output_directory(directory):
    """
    Check if output directory exist and is writable.
    :param directory: Path where to store pictures.
    """
    try:
        testing_file = os.path.join(directory, "photobooth_apps.txt")
        open(testing_file, 'a').close()

        os.remove(testing_file)
    except NotADirectoryError:
        logging.error("{} not a valide directory.".format(directory))
        exit(2)
    except Exception as e:
        logging.error("Unexpected error: {}".format(e))

def run(cfg):
    """
        Run Photobooth application.
    """
    # Init configuration
    configuration = Configuration(cfg)

    # Check output directory
    check_output_directory(configuration.pictures_directory)

    print(configuration.__dict__)

    """
        # Run Photobooth Frame
        try:
            photobooth = Gui(getattr(config, params.language)['title'], config.resolution['width'],
                             config.resolution['height'], getattr(config, params.language))
        except AttributeError:
            logging.error("Language {} not found.".format(params.language))
            exit(1)

        photobooth.run()
    """



if __name__ == "__main__":
    # Create script arguments parser
    args_parse = ArgumentParser("Run photobooth.")
    args_parse.add_argument("--config", "-c", metavar="file", help="Configuration file", required=True)
    args_parse.add_argument("--language", "-l", metavar="language", default="fr", help="choose application language.")

    params = args_parse.parse_args()

    run(cfg=params.config)
