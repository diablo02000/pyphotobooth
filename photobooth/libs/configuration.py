import yaml
import os
import logging


class Configuration(object):
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
            with open(self.file, 'r') as f:
                self.logger.debug("Load {} configuration file.".format(self.file))
                config = yaml.load(f)

            # Set configuration attribute
            self.resolution = config['resolution']
            self.pictures_directory = os.path.expanduser(config['pictures_directory'])

            # Set meta for each language
            for lang in config['languages'].keys():
                logging.debug("Set lang [{}]".format(config['languages']))
                setattr(self, lang, config['languages'][lang])

        except KeyError as e:
            self.logger.error("Parameters missing in configuration file: {}.".format(e), exc_info=True)
            exit(2)
        except Exception as e:
            self.logger.error("Failed to parse configuration file", exc_info=True)
            exit(2)