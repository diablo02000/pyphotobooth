#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import sys
from argparse import ArgumentParser
from pprint import pprint

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

# Define logger
log4py = logging.getLogger('photobooth')

def set_logging(lvl, log_path=None):
    """
    Set logging module
    :param lvl: Log level.
    :type lvl: Int
    """
    # define format
    log_format = '%(asctime)-15s - %(levelname)s - %(message)s'
    log_date_format = "%Y-%m-%d %H:%M:%S"
    log_formatter = logging.Formatter(log_format, log_date_format)

    # Create file handler if log path define
    if log_path:
        f_handler = logging.FileHandler(log_path)
        f_handler.setFormatter(log_formatter)
        log4py.addHandler(f_handler)
    else:
        # Create streamHandler
        s_handler = logging.StreamHandler(sys.stdout)
        s_handler.setFormatter(log_formatter)
        log4py.addHandler(s_handler)

    log4py.setLevel(lvl)

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

def run(cfg, verbose):
    """
        Run Photobooth application.
    """
    # Init configuration
    configuration = Configuration(cfg)

    # Check output directory
    check_output_directory(configuration.pictures_directory)

    # Enable verbose log
    if verbose:
        log_lvl = logging.DEBUG
    else:
        log_lvl = logging.INFO

    try:
        set_logging(log_path=configuration.log, lvl=log_lvl)
    except Exception:
        set_logging(lvl=log_lvl)

    log4py.info("Photobooth apps running ...")
    log4py.debug("ok")

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
    args_parse.add_argument("--verbose", "-V", action="store_true")

    params = args_parse.parse_args()

    run(cfg=params.config, verbose=params.verbose)
