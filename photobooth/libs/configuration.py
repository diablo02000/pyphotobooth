import yaml
import os


class PhotoboothConfigurationException(Exception):
    pass


class PhotoboothConfigurationParameters(Exception):
    pass


class Configuration(object):
    """
    Create configuration object.
    """

    def __init__(self, file):
        self.file = file
        self._get_config()

    def _get_config(self):
        """
        Try to extract configuration from YAML file
        """
        try:
            # Open configuration file and load YAML
            with open(self.file, 'r') as f:
                config = yaml.load(f)

            # Set configuration attribute
            self.resolution = config['resolution']
            self.pictures_directory = os.path.expanduser(config['pictures_directory'])

            if 'log' in config.keys():
                self.log = os.path.expanduser(config['log'])

            # Set meta for each language
            for lang in config['languages'].keys():
                setattr(self, lang, config['languages'][lang])

        except KeyError as e:
            raise PhotoboothConfigurationParameters("Parameters missing in configuration file: {}.".format(e))
        except Exception as e:
            raise PhotoboothConfigurationException("Failed to parse configuration file: {}.".format(e))
