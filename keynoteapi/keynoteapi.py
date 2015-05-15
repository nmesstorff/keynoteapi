"""
    Norman Messtorff <normes@normes.org>
    (c) 2014 - 2015

    Module for accessing the Keynote API on api.keynote.com
"""
from __future__ import print_function

try:
    import urllib.request as request
except ImportError:
    import urllib2 as request
import json
import os
import time
import sys


class KeynoteApi(object):
    """
        Class to access the Keynote API from api.keynote.com
    """
    timeranges = {'last_five_minute': '5min', 'last_fifteen_minute': '15min',
                  'last_one_hour': '1h', 'last_24_hours': '24h',
                  'last_one_week': '1week', 'last_one_month': '1month', }

    def __init__(self, api_key=None, proxies=None):
        if api_key is not None:
            self.api_key = api_key
        else:
            self.api_key = os.getenv('KEYNOTE_API_KEY', None)

        if self.api_key is None:
            print("Unknown Keynote API key. Set via environment variable \
'KEYNOTE_API_KEY' or 'api_key' parameter in KeynoteApi instance\n")
            sys.exit(1)

        self.proxies = proxies
        self.api_remaining_hour = None
        self.api_remaining_day = None
        self.dashboarddata = None
        self.cache_usage = True
        self.cache_maxage = 60
        self.cache_filename = os.path.join('/tmp',
                                           '.cache_keynoteapi_response_')
        self.mockinput = None

    def set_mockinput(self, mockinput):
        """
            setter for mock input which should only be used for testing
        """
        self.mockinput = mockinput

    def check_cache_usable(self, filename):
        """
            check if the cache is still usable or not
            returns True if the cache is still warm enough
        """
        file_mtime = os.path.getmtime(filename) if os.path.isfile(filename) \
            else 0

        cache_maxage = time.time() - self.cache_maxage
        return file_mtime > cache_maxage

    @staticmethod
    def gen_api_url(api_cmd,
                    api_key,
                    api_format,
                    api_base='https://api.keynote.com/keynote/api'):
        """ generate a url for keynote access including json/xml format """
        valid_formats = ('json', 'xml')
        if api_format not in valid_formats:
            raise ValueError("%s not in valid formats %s" % (api_format,
                             ", ".join(valid_formats)))
        api_url = "%s/%s?api_key=%s&format=%s" % (api_base, api_cmd,
                                                  api_key, api_format)
        return api_url

    def get_api_response(self, api_cmd):
        """
            connect to the keynote api and consider the usage of a local cache
            to limit the needed requests (there is a hourly and daily limit).

            returns the response only as json at the moment
        """
        if self.mockinput:
            cache_filename = self.mockinput
            use_cache = False
        else:
            cache_filename = self.cache_filename + api_cmd
            use_cache = (
                self.cache_usage and self.check_cache_usable(cache_filename)
                )

        if use_cache or self.mockinput:
            response = self.read_json_response_file(cache_filename)
        else:
            request_url = self.gen_api_url(api_cmd, self.api_key, 'json')

            if self.proxies is not None and \
                    self.proxies.get('socks', None) is not None:

                try:
                    import requesocks
                except ImportError as err:
                    raise ImportError("Unable to use SOCKS proxy server: %s" %
                                      err)
                else:
                    session = requesocks.session()
                    session.proxies = {
                        'https': "socks5://%s" % self.proxies['socks']
                    }

                    try:
                        resp = session.get(request_url)
                    except Exception as ex:
                        raise Exception("Error accessing API URL: %s" % ex)

                    # TODO if resp.status_code < 300 ...
                    # using .content instead of .text because of
                    # binary (gzipped) response
                    response = json.loads(resp.content)
            else:
                if self.proxies is not None and \
                        self.proxies.get('https', None) is not None:

                    proxy = request.ProxyHandler({
                        'https': self.proxies['https']
                    })
                    opener = request.build_opener(proxy)
                    request.install_opener(opener)

                # _continue_ with... OR
                # _else_ open URL without proxy
                try:
                    request_cmd = request.urlopen(request_url)
                except request.URLError, ex:
                    raise Exception("Error accessing API URL: %s" % ex)

                # TODO if resp.status_code < 300 ...
                response = json.load(request_cmd)

            self.write_json_response(response, self.cache_filename + api_cmd)
            self.set_remaining_api_calls(response)
        return response

    @staticmethod
    def write_json_response(data, filename):
        """ write JSON data to local disk (used for caching)"""
        with open(filename, 'wb') as outfile:
            json.dump(data, outfile)

    def read_json_response_file(self, filename):
        """ read JSON data from local disk """
        with open(filename, 'rb') as infile:
            response = json.load(infile)
        self.set_remaining_api_calls(response)
        return response

    def set_remaining_api_calls(self, response):
        """ save the remaining API calls to keep the budget """

        if response is not None:
            try:
                self.api_remaining_hour = \
                    response['remaining_api_calls']['hour_call_remaining']
                self.api_remaining_day = \
                    response['remaining_api_calls']['day_call_remaining']
            except KeyError:
                pass

    def get_remaining_api_calls(self):
        """ getter for remaining API calls. [0]=hourly, [1]=daily """
        return [self.api_remaining_hour, self.api_remaining_day]

    def get_dashboarddata(self):
        """ getter for processed dashboarddata """
        return self.get_api_response('getdashboarddata')

    def get_measurement_slots(self):
        """
            process measurement slots from class-local dashboarddata
            return: [ (product, id), (testprod, 4)]
        """
        slots = {}
        for product in self.get_dashboarddata().get('product', []):
            for item in product.get('measurement', []):
                slots[item['alias']] = item['id']
        return slots

    def get_perf_data(self, measurement_slot):
        """ getter for perf_data, the response times of your measurements """
        return self.get_data(measurement_slot, data_type='perf_data')

    def get_avail_data(self, measurement_slot):
        """ getter for avail_data, the availability of your measurements """
        return self.get_data(measurement_slot, data_type='avail_data')

    def get_data(self, measurement_slot, data_type=None):
        """ getter for avail_data, perf_data """
        data = {}
        if data_type is not None:
            for product in self.get_dashboarddata().get('product', []):
                for type_ in product.get('measurement', []):
                    if type_['alias'] == measurement_slot:
                        for item in type_[data_type]:
                            data[item['name']] = item['value']
        return data
