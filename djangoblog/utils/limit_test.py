import time

from django import test


class SlowTestException(Exception):
    """SlowTestException."""


class LimitTestCaseMixing:
    def _callTestMethod(self, method):
        start = time.time()

        result = super()._callTestMethod(method)

        LIMIT_SECONDS = 10
        time_taken = time.time() - start
        if time_taken > LIMIT_SECONDS:
            raise SlowTestException(
                f"This test took {time_taken:.2f}s, more than the limit of {LIMIT_SECONDS}s.",
            )

        return result


class TestCase(LimitTestCaseMixing, test.TestCase):
    fixtures = ["test"]

    pass


class TransactionTestCase(LimitTestCaseMixing, test.TransactionTestCase):
    pass


class SimpleTestCase(LimitTestCaseMixing, test.TestCase):
    pass
