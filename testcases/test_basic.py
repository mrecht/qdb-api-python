# pylint: disable=C0103,C0111,C0302,W0212
import datetime
import os
import sys
import unittest
import settings

from settings import quasardb

class QuasardbBasic(unittest.TestCase):
    def test_build(self):
        build = quasardb.build()
        self.assertGreater(len(build), 0)

    def test_version(self):
        version = quasardb.version()
        self.assertGreater(len(version), 0)

    def test_purge_all_throws_exception__when_disabled_by_default(self):
        self.assertRaises(quasardb.Error,
                          settings.cluster.purge_all, datetime.timedelta(minutes=1))


if __name__ == '__main__':
    if settings.get_lock_status() is False:
        settings.init()
        test_directory = os.getcwd()
        test_report_directory = os.path.join(os.path.split(
            __file__)[0], '..', 'build', 'test', 'test-reports')
        import xmlrunner
        unittest.main(testRunner=xmlrunner.XMLTestRunner(  # pylint: disable=E1102
            output=test_report_directory), exit=False)
        settings.terminate()
