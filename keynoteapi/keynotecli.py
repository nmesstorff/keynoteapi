"""
    CLI tool for interacting with keynote.com services

    (c) 2015 Norman Messtorff <normes@normes.org>
"""
from __future__ import print_function
from keynoteapi import KeynoteApi


class KeynoteCli(object):
    """docstring for KeynoteCli"""
    def __init__(self, apikey, mockinput=None):
        self.kapi = KeynoteApi(apikey)

    def listMeasurements(self):
        """List all available measurement slots and its data"""
        for measurement in self.kapi.get_products():
            print("\n# '%s': " % measurement)
            print('  Availability data:')
            for timerange in self.kapi.get_avail_data(measurement):
                print("    - %s:\t %s%%" % (
                    timerange,
                    self.kapi.get_avail_data(measurement)[timerange]
                    ))
            print('  Response times:')
            for timerange in self.kapi.get_perf_data(measurement):
                print("    - %s:\t %ss" % (
                    timerange,
                    self.kapi.get_perf_data(measurement)[timerange]
                    ))
        return True
