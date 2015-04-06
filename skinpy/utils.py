class CallProxy(object):
    def __init__(self):
        self._reporters = {}

    def register(self, name):
        def _register(reporter):
            self._reporters[name] = reporter
            return reporter
        return _register

    def __call__(self, name, *args, **kwargs):
        return self._reporters[name](*args, **kwargs)
