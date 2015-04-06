# -*- coding: utf-8 -*-

import time
import traceback

try:
    import console_colors
except ImportError:
    pass


class TerminalReporter(object):
    def __init__(self):
        self._first_subject = True

    def on_new_subject(self, subject):
        if not self._first_subject:
            print("―" * 80)
            print("")
        self._first_subject = False
        print("{}".format(subject))
        self._print_horizontal_line()

    def on_success(self, msg):
        print("{} ✓".format(msg))

    def on_error(self, msg):
        print("{} ✗".format(msg))

    def on_tests_finished(self, test_result):
        self._print_horizontal_line()
        print("")
        self._print_summary(test_result)

    def on_exception(self, exc_type, exc_value, tb, stack, testable):
        header, trace = self._format_exception(exc_type, exc_value, stack,
                                               testable)
        print(header)
        print(trace)

    def _print_horizontal_line(self):
        print("―" * 80)

    def _print_summary(self, test_result):
        print("Ran {} tests in {:.3f}s ({})".format(
            len(test_result),
            time.time() - test_result.start_time,
            test_result
        ))

    def _format_exception(self, exc_type, exc_value, stack, testable):
        yield "\"{}\" raised a {}. Traceback:".format(str(testable),
                                                      exc_type.__name__)
        yield "".join(
            traceback.format_list(stack) +
            traceback.format_exception_only(exc_type, exc_value)
        ).rstrip()


class ColorTerminalReporter(TerminalReporter):
    def on_success(self, msg):
        with console_colors.Foreground(console_colors.INTENSE_GREEN):
            super(ColorTerminalReporter, self).on_success(msg)

    def on_error(self, msg):
        with console_colors.Foreground(console_colors.INTENSE_RED):
            super(ColorTerminalReporter, self).on_error(msg)

    def on_exception(self, exc_type, exc_value, tb, stack, testable):
        header, trace = self._format_exception(exc_type, exc_value, stack,
                                               testable)
        with console_colors.Foreground(console_colors.INTENSE_RED):
            print(header)
        print(trace)

    def on_tests_finished(self, test_result):
        self._print_horizontal_line()
        with console_colors.Foreground(
                console_colors.INTENSE_GREEN if test_result.was_successful
                else console_colors.INTENSE_RED):
            print()
            self._print_summary(test_result)


class BlinkingColorTerminalReporter(ColorTerminalReporter):
    def on_error(self, msg):
        with console_colors.Blink():
            super(BlinkingColorTerminalReporter, self).on_error(msg)
