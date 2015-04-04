import contextlib


class PassthroughReporter(object):
    class AssertionCtx(object):
        def success(self, msg):
            pass

    @contextlib.contextmanager
    def make_assertion(self):
        yield self.AssertionCtx()
