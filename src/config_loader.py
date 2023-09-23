import yaml
from functools import reduce


CONFIG_FILE = "./conf/config.yaml"

class ConfigLoader:
    _conf = {}

    @staticmethod
    def load_conf():
        with open(CONFIG_FILE, 'r') as f:
            ConfigLoader._conf = yaml.load(f, Loader=yaml.FullLoader)

    @staticmethod
    def get(*keys):
        if len(ConfigLoader._conf) == 0:
            ConfigLoader.load_conf()

        result = reduce(lambda d, key: d[key], keys, ConfigLoader._conf)

        return result