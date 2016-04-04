import importlib


class Strategy:
    def __init__(self, name, description, version, BaseClass, AntClass):
        self.name = name
        self.description = description
        self.version = version
        self.BaseClass = BaseClass
        self.AntClass = AntClass


class Loader:
    def __init__(self):
        pass

    def loadStrategy(self, strategyName):
        strategy_module = importlib.import_module('strategies.%s' % strategyName)
        manifest = strategy_module.MANIFEST

        if not isinstance(manifest, dict) or 'BaseClass' not in manifest or 'AntClass' not in manifest:
            raise ValueError('Incorrect strategy specified.')
        if 'description' not in manifest:
            manifest['description'] = '...'
        if 'version' not in manifest:
            manifest['version'] = '1.0'
        manifest['name'] = strategyName
        return Strategy(**manifest)

    def loadStrategies(self, strategyNames):
        return [self.loadStrategy(name) for name in strategyNames]
