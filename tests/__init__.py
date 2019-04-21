from tests import config
import unittest


def run():
    for test in config.tests:
        print(test().get_desc())
        suite = unittest.TestLoader().loadTestsFromTestCase(test)
        unittest.TextTestRunner(verbosity=2).run(suite)
