"""
    Norman Messtorff <normes@normes.org>
    (c) 2014 - 2015

    Module to access the Keynote API from api.keynote.com
"""
from __future__ import print_function
try:
    import urllib.request as request
except ImportError:
    import urllib2 as request
import json
import os
import time


class KeynoteApi(object):
    """
        Class to access the Keynote API from api.keynote.com
    """
    timeranges = {'last_five_minute': '5min', 'last_fifteen_minute': '15min',
                  'last_one_hour': '1h', 'last_24_hours': '24h',
                  'last_one_week': '1week', 'last_one_month': '1month', }

    def __init__(self, api_key=None):
        if api_key:
            self.api_key = api_key
        else:
            try:
                self.api_key = os.environ['KEYNOTE_API_KEY']
            except KeyError as ex:
                print("KeynoteAPI key not known. Use environment variable \
'KEYNOTE_API_KEY' or pass api_key to class KeynoteApi\n")
                raise ex
        self.api_remaining_hour = None
        self.api_remaining_day = None
        self.dashboarddata = None
        self.products = None
        self.cache_usage = True
        self.cache_maxage = 60
        self.cache_filename = '/tmp/.cache_keynoteapi_response_'
        self.mockinput = None

    def set_mockinput(self, mockinput):
        """
            setter for mockinput which should only used for testing
        """
        self.mockinput = mockinput

    def check_cache_usable(self, filename):
        """
            check if the cache is still usable or not
            returns True if the cache is still warm enought
        """
        if os.path.isfile(filename):
            file_mtime = os.path.getmtime(filename)
        else:
            file_mtime = 0

        cache_maxage = time.time() - self.cache_maxage
        if file_mtime > cache_maxage:
            return True
        else:
            return False

    @staticmethod
    def gen_api_url(api_cmd,
                    api_key,
                    api_format,
                    api_base='https://api.keynote.com/keynote/api'):
        """ generate a url for keynote access including json/xml format """
        valid_formats = ('json', 'xml')
        if api_format not in valid_formats:
            raise ValueError
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
            request_cmd = request.urlopen(request_url)
            response = json.load(request_cmd)
            self.write_json_response(response, self.cache_filename + api_cmd)
            self.set_remaining_api_calls(response)
        return response

    @staticmethod
    def write_json_response(data, filename):
        """ write json data to local disc (used for caching)"""
        with open(filename, 'wb') as outfile:
            json.dump(data, outfile)

    def read_json_response_file(self, filename):
        """ read json data from local disc """
        with open(filename, 'rb') as infile:
            response = json.load(infile)
        self.set_remaining_api_calls(response)
        return response

    def set_remaining_api_calls(self, response):
        """ safe the remaining api calls to keep the budget """
        self.api_remaining_hour = \
            response['remaining_api_calls']['hour_call_remaining']
        self.api_remaining_day = \
            response['remaining_api_calls']['day_call_remaining']
        return self.get_remaining_api_calls()

    def get_remaining_api_calls(self):
        """ getter for remaining api calls. [0]=hourly, [1]=daily """
        return [self.api_remaining_hour, self.api_remaining_day]

    def get_dashboarddata(self):
        """ getter for processed dashboarddata """
        return self.get_api_response('getdashboarddata')

    def get_products(self):
        """
            process products / measurements from class local dashboarddata
            return: [ (product, id), (testprod, 4)]
        """
        products = {}
        for product in self.get_dashboarddata()['product']:
            for item in product['measurement']:
                products[item['alias']] = item['id']
        self.products = products
        return self.products

    def get_perf_data(self, product):
        """ getter for perf_data, the response times of your measurements """
        perf_data = {}
        for typ in self.get_dashboarddata()['product'][0]['measurement']:
            if typ['alias'] == product:
                for item in typ['perf_data']:
                    perf_data[item['name']] = item['value']
        return perf_data

    def get_avail_data(self, product):
        """ getter for avail_data, the availability of your measurements """
        avail_data = {}
        for typ in self.get_dashboarddata()['product'][0]['measurement']:
            if typ['alias'] == product:
                for item in typ['avail_data']:
                    avail_data[item['name']] = item['value']
        return avail_data
