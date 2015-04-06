# -*- coding: utf-8 -*-

import time
import traceback

try:
    import console_colors
except ImportError:
    console_colors = None


class TerminalReporter(object):
    SUCCESS_TEMPLATE = "  ✓ {msg}"
    ERROR_TEMPLATE = "  ✗ {msg}"
    TESTS_FINISHED_TEMPLATE = ("\n{line}\nRan {test_count} tests in "
                               "{exec_time:.3f}s ({test_result})")

    def __init__(self):
        self._first_subject = True

    def on_new_subject(self, subject):
        if not self._first_subject:
            print("")
        self._first_subject = False
        print("{}".format(subject))

    def on_success(self, msg):
        print(self.SUCCESS_TEMPLATE.format(msg=msg))

    def on_error(self, msg):
        print(self.ERROR_TEMPLATE.format(msg=msg))

    def on_tests_finished(self, test_result):
        print(self.TESTS_FINISHED_TEMPLATE.format(
            line="―" * 80,
            test_count=len(test_result),
            exec_time=time.time() - test_result.start_time,
            test_result=test_result
        ))

    def on_exception(self, exc_type, exc_value, tb, stack, testable):
        header, trace = self._format_exception(exc_type, exc_value, stack,
                                               testable)
        print(header)
        print(trace)

    def _format_exception(self, exc_type, exc_value, stack, testable):
        yield "  \"{}\" raised a {}. Traceback:".format(str(testable),
                                                        exc_type.__name__)
        yield "  " + "\n  ".join("".join(
            traceback.format_list(stack) +
            traceback.format_exception_only(exc_type, exc_value)
        ).rstrip().splitlines())


if console_colors:
    class ColorTerminalReporter(TerminalReporter):
        SUCCESS_TEMPLATE = TerminalReporter.SUCCESS_TEMPLATE.replace(
            "✓", "{green}✓{reset}".format(
                green=console_colors.INTENSE_GREEN.fg,
                reset=console_colors.RESET))
        ERROR_TEMPLATE = TerminalReporter.ERROR_TEMPLATE.replace(
            "✗", "{green}✗{reset}".format(
                green=console_colors.INTENSE_RED.fg,
                reset=console_colors.RESET))
        TESTS_FINISHED_TEMPLATE = (
            "\n{line}\nRan {test_count} tests in {exec_time:.3f}s "
            "{color}({test_result}){reset}"
        )

        def on_tests_finished(self, test_result):
            if test_result.was_successful:
                color = console_colors.INTENSE_GREEN.fg
            else:
                color = console_colors.INTENSE_RED.fg
            print(self.TESTS_FINISHED_TEMPLATE.format(
                line="―" * 80,
                test_count=len(test_result),
                exec_time=time.time() - test_result.start_time,
                test_result=test_result,
                color=color,
                reset=console_colors.RESET
            ))

    class BlinkingColorTerminalReporter(ColorTerminalReporter):
        def on_error(self, msg):
            with console_colors.Blink():
                super(BlinkingColorTerminalReporter, self).on_error(msg)
