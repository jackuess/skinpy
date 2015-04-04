import itertools

from .reporters import PassthroughReporter


class Testable(object):
    def __init__(self, subject, args=((), {}), name=None,
                 reporter=PassthroughReporter()):
        self.__subject = subject
        self.__args, self.__kwargs = args
        self.__name = name
        self.__reporter = reporter

    @property
    def value(self):
        try:
            return self.__subject(*self.__args, **self.__kwargs)
        except TypeError:
            return self.__subject

    def __getitem__(self, key):
        return Testable(self.value[key], name="{}[{!r}]".format(self, key),
                        reporter=self.__reporter)

    def __getattr__(self, name):
        value = getattr(self.value, name)
        return Testable(value, name="{}.{}".format(self, name),
                        reporter=self.__reporter)

    def __call__(self, *args, **kwargs):
        args_repr = itertools.chain(
            map(repr, args),
            ("{}={!r}".format(key, value) for key, value in kwargs.items())
        )
        return Testable(self.__subject,
                        args=(args, kwargs),
                        name="{}({})".format(self.__subject.__name__,
                                             ", ".join(args_repr)),
                        reporter=self.__reporter)

    def __str__(self):
        if self.__name:
            return "{}: {!r}".format(self.__name, self.value)
        return str(self.value)

    def should_equal(self, expected):
        with self.__reporter.make_assertion() as assertion:
            error_msg = "{} doesn't equal {!r}".format(self, expected)
            assert self.value == expected, error_msg
            assertion.success("{} equals {!r}".format(self, expected))

    def should_raise(self, expected_exc):
        subject_name = self.__subject.__name__
        with self.__reporter.make_assertion() as assertion:
            try:
                self.value
            except expected_exc:
                assertion.success("{} raises {!r}".format(subject_name,
                                                          expected_exc))
            except Exception as exc:
                raise AssertionError(
                    "{} doesn't raise {!r}, it raises {!r}".format(
                        subject_name,
                        expected_exc,
                        exc
                    )
                )
            else:
                raise AssertionError(
                    "{} doesn't raise {!r}".format(subject_name, expected_exc)
                )
