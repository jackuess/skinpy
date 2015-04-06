import time
import traceback

from .reporters import TerminalReporter
from .testable import Testable


class TestResult(object):
    def __init__(self, start_time):
        self.successful = 0
        self.failed = 0
        self.errors = 0
        self.start_time = start_time

    @property
    def was_successful(self):
        return not self.failed and not self.errors

    @property
    def has_failed(self):
        return not self.was_successful

    def __len__(self):
        return self.successful + self.failed + self.errors

    def __str__(self):
        return "successful={}, failed={}, errors={}".format(
            self.successful, self.failed, self.errors
        )

    def __repr__(self):
        return "<{self.__class__.__name__}({self})".format(self=self)

    def __add__(self, other):
        self.successful += other.successful
        self.failed += other.failed
        self.errors += other.errors
        return self


class AssertionCtx(object):
    def __init__(self, reporter, test_result, testable):
        self.reporter = reporter
        self.test_result = test_result
        self.testable = testable

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, tb):
        if not exc_type:
            self.test_result.successful += 1
            self.reporter.on_success(str(self.testable))
        elif exc_type is AssertionError:
            self.test_result.failed += 1
            self.reporter.on_error(exc_value.args[0])
        elif exc_value:
            self.test_result.errors += 1
            self.reporter.on_exception(exc_type, exc_value, tb,
                                       traceback.extract_stack()[:-2],
                                       self.testable)
        return True


class Description(object):
    reporter = None
    testable_cls = Testable

    def __init__(self):
        self.seen_subjects = set()

    def assertion_ctx(self, testable):
        return AssertionCtx(self.reporter, self.test_result, testable)

    def execute(self, reporter=TerminalReporter()):
        self.reporter = reporter

        self.test_result = TestResult(start_time=time.time())
        for testable in self.describe():
            pass

        return self.test_result

    def register_subject(self, subject):
        if subject not in self.seen_subjects:
            self.reporter.on_new_subject(subject.__name__)
            self.seen_subjects.add(subject)


class Fixture(object):
    def set_set_up(self, set_up_fn):
        self.set_up = set_up_fn

    def set_tear_down(self, tear_down_fn):
        self.tear_down = tear_down_fn
        return self

    def tear_down(self, obj):
        pass


class Subject(object):
    def __init__(self, getter):
        self.get = getter
        self.fixtures = []
        self.__name__ = getter.__name__

    def __get__(self, obj, objcls):
        if obj:
            obj.register_subject(self)
            self.do_set_up(obj)
            try:
                return obj.testable_cls(self.get(obj),
                                        assertion_ctx=obj.assertion_ctx)
            finally:
                self.do_tear_down(obj)
        else:
            return self

    def do_set_up(self, obj):
        for fixture in self.fixtures:
            fixture.set_up(obj)

    def do_tear_down(self, obj):
        for fixture in self.fixtures:
            fixture.tear_down(obj)

    def before(self, set_up_fn):
        fixture = Fixture()
        fixture.set_set_up(set_up_fn)
        self.fixtures.append(fixture)
        return fixture
