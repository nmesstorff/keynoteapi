"""
    Testmodule for keynotcli
"""
import unittest
import keynoteapi.keynotecli


class KeynotecliTest(unittest.TestCase):
    """create a keynotecli object"""
    def setUp(self):
        self.keycli = keynoteapi.keynotecli.KeynoteCli('test-api-key')
        # self.keyapi.set_mockinput('tests/json/empty.json')

    def test_class_instance(self):
        """ test if we get the right class instance """
        result = keynoteapi.keynotecli.KeynoteCli('test-api-key')
        assert isinstance(result, keynoteapi.keynotecli.KeynoteCli) == True
