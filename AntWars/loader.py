import importlib
import os

class Strategy:
    def __init__(self, name, description, BaseClass, AntClass):
        self.name = name
        self.description = description
        self.BaseClass = BaseClass
        self.AntClass = AntClass


class Loader:
    def loadStrategy(self, path):
        normalized_name = os.path.split(path)[-1].split('.')[0]     # dir/name.py -> name
        strategy_module = importlib.import_module('strategies.%s' % normalized_name)
        manifest = strategy_module.MANIFEST

        if not isinstance(manifest, dict) or 'BaseClass' not in manifest or 'AntClass' not in manifest:
            raise ValueError('Incorrect strategy specified.')
        if 'description' not in manifest:
            manifest['description'] = '...'
        manifest['name'] = normalized_name
        return Strategy(**manifest)

    def loadStrategies(self, paths):
        return [self.loadStrategy(path) for path in paths]
