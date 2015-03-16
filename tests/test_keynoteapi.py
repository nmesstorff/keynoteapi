"""
    Testmodule for keynoteapi
"""
import unittest
import os
import json
import keynoteapi
import keynoteapi.keynoteapi


class KeynoteapiTest(unittest.TestCase):
    """create a keynoteapi object and set a dummy api key"""
    def setUp(self):
        self.keyapi = keynoteapi.keynoteapi.KeynoteApi('test-api-key')
        self.keyapi.set_mockinput('tests/json/empty.json')

    def test_version(self):
        assert keynoteapi.__version__ >= '0.1.0'

    def test_class_instance(self):
        result = keynoteapi.keynoteapi.KeynoteApi('test-api-key')
        assert isinstance(result, keynoteapi.keynoteapi.KeynoteApi) == True
        assert self.keyapi.api_key == 'test-api-key'

    def test_apikey_from_environment(self):
        current_environment_value = os.environ.get('KEYNOTE_API_KEY')
        os.environ['KEYNOTE_API_KEY'] = 'environment-api-key'
        result = keynoteapi.keynoteapi.KeynoteApi()
        os.environ['KEYNOTE_API_KEY'] = current_environment_value
        assert isinstance(result, keynoteapi.keynoteapi.KeynoteApi) == True
        assert result.api_key == 'environment-api-key'

    def test_missing_apikey(self):
        current_environment_value = os.environ.get('KEYNOTE_API_KEY')
        del os.environ['KEYNOTE_API_KEY']
        self.assertRaises(KeyError, keynoteapi.keynoteapi.KeynoteApi)
        os.environ['KEYNOTE_API_KEY'] = current_environment_value

    def test_class_timeranges_type(self):
        assert type(self.keyapi.timeranges) == dict

    def test_class_timeranges_items(self):
        assert len(self.keyapi.timeranges) == 6

    def test_read_json_response_file(self):
        """
        test read_json_response_file() and check if it sets
        api_remaining_* values
        """
        try:
            result = self.keyapi.read_json_response_file(
                'tests/json/getdashboarddata_list.json')
            assert len(result) > 0
        except Exception:
            assert False

    def test_cachable_filename_not_existing(self):
        """
        test check_cachable_usable() if we get False on non existing cachefiles
        """
        result = self.keyapi.check_cache_usable(
            '/tmp/not-existing-testfile-for-keynoteapi')
        assert result == False

    def test_cachable_filename_used(self):
        """
        test check_cachable_usable() if we get True on usable cache files
        """
        testfilename = 'testfile-test_cachable_filename_used'
        testfile = open(testfilename, 'w')
        testfile.close()
        result = self.keyapi.check_cache_usable(testfilename)
        os.remove(testfilename)
        assert result == True

    def test_write_json_response(self):
        testfilename = 'testfile-test_write_json_response'
        self.keyapi.write_json_response('{ "test": "true"}', testfilename)
        testfile = open(testfilename)
        firstline = testfile.readline()
        testfile.close()
        result = json.loads(firstline)
        os.remove(testfilename)
        assert type(result) == unicode

    def test_read_json_response_file_is_dict(self):
        """
        test read_json_response_file() and check if it sets
        api_remaining_* values
        """
        result = self.keyapi.read_json_response_file(
            'tests/json/getdashboarddata_list.json')
        assert type(result) == dict

    def test_read_json_response_file_data_link(self):
        result = self.keyapi.read_json_response_file(
            'tests/json/getdashboarddata_list.json')
        link = result['link']
        assert 'http://api.keynote.com/keynote/api/getslotmetadata?api_key=0'\
            in link['href']
        assert link['type'] == 'application/json'
        assert link['rel'] == 'slotmetadata'

    def test_read_json_response_file_data_link_is_dict(self):
        result = self.keyapi.read_json_response_file(
            'tests/json/getdashboarddata_list.json')
        link = result['link']
        assert type(link) == dict

    def test_read_json_response_file_data_link_has_three_elements(self):
        result = self.keyapi.read_json_response_file(
            'tests/json/getdashboarddata_list.json')
        link = result['link']
        assert len(link) == 3

    def test_read_json_response_file_data_product(self):
        result = self.keyapi.read_json_response_file(
            'tests/json/getdashboarddata_list.json')
        product = result['product']
        assert product[0]['id'] == "TxP"
        assert product[0]['name'] == "TxP"

    def test_read_json_response_file_data_product_is_list(self):
        result = self.keyapi.read_json_response_file(
            'tests/json/getdashboarddata_list.json')
        product = result['product']
        assert type(product) == list

    def test_read_json_response_file_data_product_has_one_element(self):
        result = self.keyapi.read_json_response_file(
            'tests/json/getdashboarddata_list.json')
        product = result['product']
        assert len(product) == 1

    def test_read_json_response_file_data_avail_data_is_list(self):
        result = self.keyapi.read_json_response_file(
            'tests/json/getdashboarddata_list.json')
        avail_data = result['product'][0]['measurement'][0]['avail_data']
        assert type(avail_data) == list

    def test_read_json_response_file_data_measurement(self):
        result = self.keyapi.read_json_response_file(
            'tests/json/getdashboarddata_list.json')
        measurement = result['product'][0]['measurement']
        # assert type(measurement[0]['alias']) == str
        assert measurement[0]['threshold_data'][0]['duration'] == ""
        assert measurement[0]['threshold_data'][0]['unit'] == "seconds"
        assert measurement[0]['threshold_data'][0]['name'] == "perfwarning"
        assert measurement[0]['threshold_data'][0]['value'] == "-1.0"

    def test_read_json_response_file_data_measurement_threshold_data_is_list(self):
        result = self.keyapi.read_json_response_file(
            'tests/json/getdashboarddata_list.json')
        measurement = result['product'][0]['measurement']
        assert type(measurement[0]['threshold_data']) == list

    def test_read_json_response_file_data_measurement_threshold_data_has_dict(self):
        result = self.keyapi.read_json_response_file(
            'tests/json/getdashboarddata_list.json')
        measurement = result['product'][0]['measurement']
        assert type(measurement[0]['threshold_data'][0]) == dict

    def test_read_json_response_file_data_measurement_is_list(self):
        result = self.keyapi.read_json_response_file(
            'tests/json/getdashboarddata_list.json')
        measurement = result['product'][0]['measurement']
        assert type(measurement) == list

    def test_read_json_response_file_data_measurement_list_has_dict(self):
        result = self.keyapi.read_json_response_file(
            'tests/json/getdashboarddata_list.json')
        measurement = result['product'][0]['measurement']
        assert type(measurement[0]) == dict

    def test_read_json_response_file_data_remaining_api_calls(self):
        result = self.keyapi.read_json_response_file(
            'tests/json/getdashboarddata_list.json')
        assert result['remaining_api_calls']['hour_call_remaining'] == 3596
        assert result['remaining_api_calls']['day_call_remaining'] == 21596

    def test_read_json_response_file_data_remaining_api_calls_eq_clasvariables(self):
        result = self.keyapi.read_json_response_file(
            'tests/json/getdashboarddata_list.json')
        assert result['remaining_api_calls']['hour_call_remaining'] ==\
            self.keyapi.api_remaining_hour
        assert result['remaining_api_calls']['day_call_remaining'] ==\
            self.keyapi.api_remaining_day

    def test_read_json_response_file_data_remaining_api_calls_has_two_elements(self):
        result = self.keyapi.read_json_response_file(
            'tests/json/getdashboarddata_list.json')
        assert len(result['remaining_api_calls']) == 2

    def test_read_json_response_file_data_remaining_api_calls_is_dict(self):
        result = self.keyapi.read_json_response_file(
            'tests/json/getdashboarddata_list.json')
        assert type(result['remaining_api_calls']) == dict

    def test_gen_api_url_json_format(self):
        """
        test if we generate a valid URL for keynote access from gen_api_url()
        and get a url with format=json
        """
        ret = self.keyapi.gen_api_url(api_cmd='test-api-cmd',
                                      api_key=self.keyapi.api_key,
                                      api_format='json')
        assert ret == 'https://api.keynote.com/keynote/api/test-api-cmd?api_key\
=test-api-key&format=json'

    def test_gen_api_url_xml_format(self):
        """
        test if we generate a valid URL for keynote access from gen_api_url()
        and get a url with format=xml
        """
        ret = self.keyapi.gen_api_url(api_cmd='test-api-cmd',
                                      api_key=self.keyapi.api_key,
                                      api_format='xml')
        assert ret == 'https://api.keynote.com/keynote/api/test-api-cmd?api_key\
=test-api-key&format=xml'

    def test_gen_api_url_invalid_format(self):
        """
        test if we get a ValueError exception on invalid requested format
        """
        try:
            self.keyapi.gen_api_url(api_cmd='test-api-cmd',
                                    api_key=self.keyapi.api_key,
                                    api_format='invalid')
            assert False
        except ValueError:
            assert True

    def test_get_api_response(self):
        """
        test if we get a valid response from get_api_response()
        """
        pass

    def test_set_remaining_api_calls_hour(self):
        """test if set_remaining_api_calls sets correct values"""
        self.keyapi.read_json_response_file(
            'tests/json/getdashboarddata_list.json')
        assert self.keyapi.api_remaining_hour >= 1
        assert self.keyapi.api_remaining_hour ==\
            self.keyapi.get_remaining_api_calls()[0]

    def test_set_remaining_api_calls_day(self):
        """test if set_remaining_api_calls sets correct values"""
        self.keyapi.read_json_response_file(
            'tests/json/getdashboarddata_list.json')
        assert self.keyapi.api_remaining_day >= 0
        assert self.keyapi.api_remaining_day ==\
            self.keyapi.get_remaining_api_calls()[1]

    def test_get_remaining_api_calls_is_list1(self):
        """
        test if get_remaining_api_calls() returns an list
        """
        assert type(self.keyapi.get_remaining_api_calls()) == list

    def test_get_remaining_api_calls_is_list2(self):
        """
        test if get_remaining_api_calls() returns an list
        """
        self.keyapi.read_json_response_file(
            'tests/json/getdashboarddata_list.json')
        assert type(self.keyapi.get_remaining_api_calls()) == list

    def test_get_remaining_api_calls_has_two_elements(self):
        """
        test if get_remaining_api_calls() returns an object with two elements
        """
        assert len(self.keyapi.get_remaining_api_calls()) == 2

    def test_get_dashboarddata_eq_data(self):
        """
        test if the getter of dashboarddata is working and returns valid data
        """
        self.keyapi.set_mockinput('tests/json/getdashboarddata_list.json')
        response = self.keyapi.read_json_response_file(
            'tests/json/getdashboarddata_list.json')
        assert len(response) > 0
        assert self.keyapi.get_dashboarddata() != None

    def test_get_dashboarddata_is_dict(self):
        """
        test if the getter of dashboarddata is working and returns valid data
        """
        self.keyapi.set_mockinput('tests/json/getdashboarddata_list.json')
        assert type(self.keyapi.get_dashboarddata()) == dict

    def test_get_dashboarddata_has_three_elements(self):
        """
        test if the getter of dashboarddata is working and returns valid data
        """
        self.keyapi.set_mockinput('tests/json/getdashboarddata_list.json')
        assert len(self.keyapi.get_dashboarddata()) == 3

    def test_get_products_eq_data(self):
        """
        test if the getter of products is working
        """
        self.keyapi.set_mockinput(
            'tests/json/getdashboarddata_list.json')
        assert self.keyapi.get_products() != None
        assert self.keyapi.get_products() == self.keyapi.products

    def test_get_products_is_dict(self):
        """
        test if the getter of products is working
        """
        self.keyapi.set_mockinput('tests/json/getdashboarddata_list.json')
        assert type(self.keyapi.get_products()) == dict

    def test_get_products_has_one_element(self):
        """
        test if the getter of products is working
        """
        self.keyapi.set_mockinput('tests/json/getdashboarddata_list.json')
        assert len(self.keyapi.get_products()) == 1

    def test_get_perf_data(self):
        """
        test if get_perfdata gets useful performance data
        """
        self.keyapi.set_mockinput('tests/json/getdashboarddata_list.json')
        assert self.keyapi.get_perf_data('WPT_Ford')\
            ['last_five_minute'] == '16.726'
        assert self.keyapi.get_perf_data('WPT_Ford')\
            ['last_fifteen_minute'] == '16.726'
        assert self.keyapi.get_perf_data('WPT_Ford')\
            ['last_one_hour'] == '28.465'
        assert self.keyapi.get_perf_data('WPT_Ford')\
            ['last_24_hours'] == '28.783'

    def test_get_perf_data_is_dict(self):
        """
        test if get_perfdata gets useful performance data
        """
        self.keyapi.set_mockinput('tests/json/getdashboarddata_list.json')
        assert type(self.keyapi.get_perf_data('WPT_Ford')) == dict

    def test_get_perf_data_has_four_elements(self):
        """
        test if get_perfdata gets useful performance data
        """
        self.keyapi.set_mockinput('tests/json/getdashboarddata_list.json')
        assert len(self.keyapi.get_perf_data('WPT_Ford')) == 4

    def test_get_perf_data_invalid_is_dict(self):
        """
        test if get_perfdata gets useful performance data
        """
        self.keyapi.set_mockinput('tests/json/getdashboarddata_list.json')
        assert type(self.keyapi.get_perf_data('invalid product')) == dict

    def test_get_perf_data_invalid_has_zero_elements(self):
        """
        test if get_perfdata gets useful performance data
        """
        self.keyapi.set_mockinput('tests/json/getdashboarddata_list.json')
        assert len(self.keyapi.get_perf_data('invalid product')) == 0

    def test_avail_data(self):
        """docstring for test_avail_data"""
        self.keyapi.set_mockinput('tests/json/getdashboarddata_list.json')
        assert self.keyapi.get_avail_data('WPT_Ford')\
            ['last_five_minute'] == '100'
        assert self.keyapi.get_avail_data('WPT_Ford')\
            ['last_fifteen_minute'] == '98.059'
        assert self.keyapi.get_avail_data('WPT_Ford')\
            ['last_one_hour'] == '98.193'
        assert self.keyapi.get_avail_data('WPT_Ford')\
            ['last_24_hours'] == '97.658'

    def test_avail_data_is_dict(self):
        """docstring for test_avail_data"""
        self.keyapi.set_mockinput('tests/json/getdashboarddata_list.json')
        assert type(self.keyapi.get_avail_data('WPT_Ford')) == dict

    def test_avail_data_has_four_elements(self):
        """docstring for test_avail_data"""
        self.keyapi.set_mockinput('tests/json/getdashboarddata_list.json')
        assert len(self.keyapi.get_avail_data('WPT_Ford')) == 4

    def test_avail_data_invalid_is_dict(self):
        """docstring for test_avail_data"""
        self.keyapi.set_mockinput('tests/json/getdashboarddata_list.json')
        assert type(self.keyapi.get_avail_data('invalid product')) == dict

    def test_avail_data_invalid_has_zero_elements(self):
        """docstring for test_avail_data"""
        self.keyapi.set_mockinput('tests/json/getdashboarddata_list.json')
        assert len(self.keyapi.get_avail_data('invalid product')) == 0
