#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import sys
from argparse import ArgumentParser

# Import Gui photobooth libs
try:
    sys.path.append('./libs/')
    from gui import Gui
except Exception as e:
    logging.error("Failed to import Gui from .libs folder: {}".format(e))


def set_logging(lvl=logging.INFO):
    """
    Set logging output.
    :param lvl: Log level.
    :type lvl: Int
    """
    log_format = '%(asctime)-15s - %(levelname)s - %(message)s'
    logging.basicConfig(level=lvl, format=log_format)


if __name__ == "__main__":
    # Create script arguments parser
    args_parse = ArgumentParser("Run photobooth.")
    args_parse.add_argument("--output", "-o", metavar="folder", help="directory to store pictures", required=True)

    params = args_parse.parse_args()

    # Check if output directory is writable.
    try:
        if os.path.isdir(params.output):
            open(os.path.join(params.output, "photobooth.txt"), 'a').close()

            # delete test file
            os.remove("{}/{}".format(params.output, "photobooth.txt"))

        else:
            raise os.error("Folder does not exists.")
    except os.error as e:
        logging.error("Failed to write in {}: {}".format(params.output, e))
        exit(2)

    # Run Photobooth Frame
    photobooth = Gui("My Photobooth", 800, 600)
    photobooth.run()
