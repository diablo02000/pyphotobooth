"""
Handle photobooth configuration.
"""

import os
import sys
import logging
import yaml


class Configuration:
    """
    Create configuration object.
    """

    def __init__(self, file):
        self.logger = logging.getLogger(__name__)
        self.file = file
        self._get_config()

    def _get_config(self):
        """
        Try to extract configuration from YAML file
        """
        try:
            # Open configuration file and load YAML
            with open(self.file, 'r', encoding="utf-8") as f_cfg:
                self.logger.debug("Load %s configuration file.", self.file)
                config = yaml.load(f_cfg)

            # Set configuration attribute
            self.resolution = config['resolution']
            self.pictures_directory = os.path.expanduser(config['pictures_directory'])

            # Set meta for each language
            for lang in config['languages'].keys():
                logging.debug("Set lang [%s]", config['languages'])
                setattr(self, lang, config['languages'][lang])

        except KeyError as key_e:
            self.logger.error("Parameters missing in configuration file: %s.", key_e, exc_info=True)
            sys.exit(2)
        except (OSError, yaml.YAMLError):
            self.logger.error("Failed to parse configuration file", exc_info=True)
            sys.exit(2)
