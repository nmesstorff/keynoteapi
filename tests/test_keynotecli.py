"""
    Testmodule for keynotcli
"""
import unittest
import keynoteapi.keynotecli


class KeynotecliTest(unittest.TestCase):
    """create a keynotecli object"""
    def setUp(self):
        self.keycli = keynoteapi.keynotecli.KeynoteCli('test-api-key')

    def test_class_instance(self):
        """ test if we get the right class instance """
        result = keynoteapi.keynotecli.KeynoteCli('test-api-key')
        assert isinstance(result, keynoteapi.keynotecli.KeynoteCli)

    def test_list_measurements(self):
        """ test output of list_measurements """
        import sys
        from StringIO import StringIO

        kcli = keynoteapi.keynotecli.KeynoteCli('test-api-key', mockinput='tests/json/getdashboarddata_list.json')
        assert kcli.kapi is not None
        assert "WPT_Ford" in kcli.kapi.get_measurement_slots()
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            kcli.list_measurements()
            output = out.getvalue().strip()
            assert "Availability data" in output
            assert "Response times" in output
            assert "- last_24_hours:\t 97.658%" in output
            assert "- last_24_hours:\t 28.783s" in output
        finally:
            sys.stdout = saved_stdout
