import itertools


class ExceptionPassthrough(object):
    def __init__(self, testable):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class Testable(object):
    def __init__(self, subject, args=((), {}), name=None,
                 assertion_ctx=ExceptionPassthrough):
        self.__subject = subject
        self.__args, self.__kwargs = args
        self.__name = (name or getattr(subject, "__name__", None) or
                       repr(subject))  # TODO: Handle exception in repr
        self.__assertion_ctx = assertion_ctx
        self.__success_messages = []

    @property
    def value(self):
        if hasattr(self.__subject, "__call__"):
            return self.__subject(*self.__args, **self.__kwargs)
        else:
            return self.__subject

    def __getitem__(self, key):
        return Testable(self.value[key], name="{}[{!r}]".format(self, key),
                        assertion_ctx=self.__assertion_ctx)

    def __getattr__(self, name):
        value = getattr(self.value, name)
        return Testable(value, name="{}.{}".format(self, name),
                        assertion_ctx=self.__assertion_ctx)

    def __call__(self, *args, **kwargs):
        args_repr = itertools.chain(
            map(repr, args),
            ("{}={!r}".format(key, value) for key, value in kwargs.items())
        )
        return Testable(self.__subject,
                        args=(args, kwargs),
                        name="{}({})".format(self, ", ".join(args_repr)),
                        assertion_ctx=self.__assertion_ctx)

    def __str__(self):
        if self.__name:
            prefix = self.__name
        else:
            prefix = repr(self.value)

        if self.__success_messages:
            return "\n".join("{} {}".format(prefix, msg)
                             for msg in self.__success_messages)
        else:
            return prefix

    def __repr__(self):
        return "<Testable(subject={})>".format(self.__name)

    def should_equal(self, expected):
        error_msg = "{} doesn't equal {!r}".format(self, expected)
        with self.__assertion_ctx(self):
            assert self.value == expected, error_msg
            self.__success_messages.append("equals {!r}".format(expected))
            return self

    def should_raise(self, expected_exc):
        with self.__assertion_ctx(self):
            try:
                self.value
            except expected_exc:
                self.__success_messages.append(
                    "raises {}".format(expected_exc.__name__)
                )
                return self
            else:
                raise AssertionError(
                    "{} doesn't raise {}".format(self, expected_exc.__name__)
                )
