import os
import yaml

# The purpose of this file is to load the yaml file in memory and pass it
# around to other module around.

# TODO setup app settings
config_path = os.environ.get('APP_SETTINGS')
if config_path is None:
    config = yaml.load(open('settings.yaml'))
else:
    config = yaml.load(open(config_path))
