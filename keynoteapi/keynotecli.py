"""
    CLI tool for interacting with keynote.com services

    (c) 2015 Norman Messtorff <normes@normes.org>
"""
from __future__ import print_function
from keynoteapi import KeynoteApi


class KeynoteCli(object):

    def __init__(self, api_key, mockinput=None, proxies=None):
        self.kapi = KeynoteApi(api_key, proxies=proxies)
        self.kapi.set_mockinput(mockinput)

    def list_measurements(self):
        """List all available measurement slots and its data"""
        for measurement in self.kapi.get_measurement_slots():
            print("\n# '%s': " % measurement)

            print('  Availability data:')
            for timerange in self.kapi.get_avail_data(measurement):
                value = self.kapi.get_avail_data(measurement)[timerange]
                # do not print a percent sign unless we have an actual value
                print("    - %s:\t %s%s" % (timerange, value,
                                            "" if value in ["", "-"] else "%"))

            print('  Response times:')
            for timerange in self.kapi.get_perf_data(measurement):
                value = self.kapi.get_perf_data(measurement)[timerange]
                # do not print a unit symbol unless we have an actual value
                print("    - %s:\t %s%s" % (timerange, value,
                                            "" if value in ["", "-"] else "s"))

            thresholds = self.kapi.get_threshold_data(measurement)
            if len(thresholds.keys()) > 0:
                print('  Threshold data:')
                print("    - availability warning: %s" %
                      thresholds.get('availwarning', '-'))
                print("    - availability critical: %s" %
                      thresholds.get('availcritical', '-'))
                print("    - performance warning: %s" %
                      thresholds.get('perfwarning', '-'))
                print("    - performance critical: %s" %
                      thresholds.get('perfcritical', '-'))
