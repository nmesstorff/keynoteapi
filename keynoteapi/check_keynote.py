#!/usr/bin/env python
"""
    Norman Messtorff <normes@normes.org>
    (c) 2014 - 2015
"""
import time
import logging
import argparse
import nagiosplugin
import keynoteapi
import keynotecli

_log = logging.getLogger('nagiosplugin')


class Keynote(nagiosplugin.Resource):
    """Basic usage of KeynoteApi for this Nagios check"""
    def __init__(self, apikey, measurement_slot):
        """collect configuration for KeynoteApi class"""
        # init KeynoteApi class
        self.starttime = time.time()
        self.kapi = keynoteapi.KeynoteApi(apikey)
        self.measurement_slot = measurement_slot
        self.timeranges = ['last_five_minute', 'last_fifteen_minute',
                           'last_one_hour', 'last_24_hours']

    def validateAvaildata(self, timerange):
        """
        check if the requested timerange is element of the given availabilities
        and verify if we get a valid percentage value.

        returns requested availabillity or raise exception on invalid data
        """
        _log.debug('timerange: %s', timerange)

        availabilities = self.kapi.get_avail_data(self.measurement_slot)
        if timerange in availabilities:
            avail_data = availabilities[timerange]
            try:
                avail_data = float(availabilities[timerange])
            except Exception as e:
                _log.debug(e)
                _log.warning(
                    "unable to convert %s/%s/avail_data='%s' to float",
                    self.measurement_slot, timerange, avail_data
                    )
                _log.debug('RETURN:: False')
                return False

            if 0 <= avail_data <= 100:
                _log.debug('RETURN:: %s', avail_data)
                return avail_data
            else:
                _log.warning('invalid avail_data=\'%s\'', avail_data)
        else:
            _log.debug('RETURN:: False')
            return False

    def validatePerfdata(self, timerange):
        """
        check if the requested responsetime is a valid value in seconds

        returns responsetime or raise exception on invalid data
        """
        _log.debug('timerange: %s', timerange)

        perf_data = self.kapi.get_perf_data(self.measurement_slot)
        if timerange in perf_data:
            perf_data = perf_data[timerange]
            try:
                perf_data = float(perf_data)
            except Exception as e:
                _log.debug(e)
                _log.warning("unable to convert %s/%s/perf_data='%s' to float",
                             self.measurement_slot, timerange, perf_data)
                _log.debug('RETURN:: False')
                return False

            if perf_data >= 0:
                _log.debug('RETURN:: %s', perf_data)
                return perf_data
            else:
                _log.warning('invalid perf_data=\'%s\'', perf_data)
        else:
            _log.debug('RETURN:: False')
            return False

    def probe(self):
        """
        Iterate all timeranges and collect metrics for this probe.

        returns one or more metrics
        """
        avail_counter = 0
        perf_counter = 0

        for timerange in self.timeranges:
            # get availabillity metrics
            avail_data = self.validateAvaildata(timerange)
            if avail_data:
                avail_counter += 1
                yield nagiosplugin.Metric(
                    "avail_%s" % self.kapi.timeranges[timerange],
                    avail_data, uom='%', min=0, max=100,
                    context='availabillity_%s' % timerange)

            # get performance metrics
            perf_data = self.validatePerfdata(timerange)
            if perf_data:
                perf_counter += 1
                yield nagiosplugin.Metric(
                    "response_%s" % self.kapi.timeranges[timerange],
                    perf_data, uom='s', min=0,
                    context='responsetime_%s' % timerange)

        # verify if we got any availabillity result
        _log.debug('avail_counter: %s', avail_counter)
        if avail_counter == 0:
            raise RuntimeError('No availabillity in timeranges! '
                               '(Keynote Error? %s API calls left this hour)'
                               % self.kapi.get_remaining_api_calls()[0],)

        # verify if we got any responsetime result
        _log.debug('perf_counter: %s', perf_counter)
        if perf_counter == 0:
            raise RuntimeError('No responsetimes in timeranges! '
                               '(Keynote Error? %s API calls left this hour)'
                               % self.kapi.get_remaining_api_calls()[0],)

        # monitor available API calls to Keynote
        yield nagiosplugin.Metric("remaining_api_calls_hour",
                                  self.kapi.get_remaining_api_calls()[0],
                                  min=0)
        yield nagiosplugin.Metric("remaining_api_calls_day",
                                  self.kapi.get_remaining_api_calls()[1],
                                  min=0)

        # Perfdata for runtime of this check
        yield nagiosplugin.Metric("script_runtime",
                                  time.time()-self.starttime, uom='s', min=0)


class KeynoteSummary(nagiosplugin.Summary):
    """
        Better statuslines on check output
    """
    def __init__(self, measurement_slot):
        self.measurement_slot = measurement_slot

    def ok(self, results):
        """Output on ok state"""
        _log.debug('results: %i in %s', len(results), results)

        output = "%s: " % self.measurement_slot
        for item in results:
            output += "%s %s; " % (item.metric.name, item.metric)
        _log.debug('RETURN:: %s', output)
        return output

    def problem(self, results):
        """Output on problem states"""
        _log.debug('results: %i in %s', len(results), results)

        output = "%s: " % self.measurement_slot
        for item in results:
            output += "%s %s %s; " % (item.metric.name,
                                      item.metric,
                                      item.state)
        _log.debug('RETURN:: %s', output)
        return output


@nagiosplugin.guarded
def main():
    """main function"""
    # parsing arguments
    argp = argparse.ArgumentParser()
    argp.add_argument('-v', '--verbose', action='count', default=0,
                      help='enable verbose logging up to 3 times. Default: 0')
    argp.add_argument('-t', '--timeout', type=int, default=10,
                      help='timeout for running this script. Default: 10')
    argp.add_argument('-k', '--apikey', type=str, required=False,
                      help='your personal API key from api.keynote.com')
    argp.add_argument('-l', '--list-measurement-slots', action='store_true',
                      help='list all available measurement slots and its'
                           ' current data values')
    argp.add_argument('-m', '--measurement-slot', type=str,
                      help='measurement of your keynote account to monitor')
    argp.add_argument('-a', '--avail-warning', metavar='RANGE', default='99:',
                      help='warning level for any timerange of availabillites'
                      '. Default: \'99:\'')
    argp.add_argument('-A', '--avail-critical', metavar='RANGE', default='80:',
                      help='critical level for any timerange of availabillites'
                      '. Default: \'80:\'')
    argp.add_argument('-r', '--response-warning', metavar='RANGE',
                      help='warning level for any timerange of responsetimes')
    argp.add_argument('-R', '--response-critical', metavar='RANGE',
                      help='critical level for any timerange of responsetimes')
    argp.add_argument('--apicalls-hour-warning', metavar='RANGE',
                      default='250:', help='warning level for any timerange of'
                      ' responsetimes. Default: \'250:\'')
    argp.add_argument('--apicalls-hour-critical', metavar='RANGE', default='',
                      help='critical level for any timerange of responsetimes')
    argp.add_argument('--apicalls-day-warning', metavar='RANGE',
                      default='6000:', help='warning level for any timerange '
                      'of responsetimes Default: \'6000:\'')
    argp.add_argument('--apicalls-day-critical', metavar='RANGE', default='',
                      help='critical level for any timerange of responsetimes')
    args = argp.parse_args()

    # to be solved by an own ArgumentParser.Action later #TODO
    if args.list_measurement_slots:
        kcli = keynotecli.KeynoteCli(args.apikey)
        kcli.listMeasurements()
        exit(0)

    check = nagiosplugin.Check(
        Keynote(args.apikey, args.measurement_slot),
        nagiosplugin.ScalarContext('availabillity_last_five_minute',
                                   args.avail_warning, args.avail_critical),
        nagiosplugin.ScalarContext('availabillity_last_fifteen_minute',
                                   args.avail_warning, args.avail_critical),
        nagiosplugin.ScalarContext('availabillity_last_one_hour',
                                   args.avail_warning, args.avail_critical),
        nagiosplugin.ScalarContext('availabillity_last_24_hours',
                                   args.avail_warning, args.avail_critical),
        nagiosplugin.ScalarContext('responsetime_last_five_minute',
                                   args.response_warning,
                                   args.response_critical),
        nagiosplugin.ScalarContext('responsetime_last_fifteen_minute',
                                   args.response_warning,
                                   args.response_critical),
        nagiosplugin.ScalarContext('responsetime_last_one_hour',
                                   args.response_warning,
                                   args.response_critical),
        nagiosplugin.ScalarContext('responsetime_last_24_hours',
                                   args.response_warning,
                                   args.response_critical),
        nagiosplugin.ScalarContext('remaining_api_calls_hour',
                                   args.apicalls_hour_warning,
                                   args.apicalls_hour_critical),
        nagiosplugin.ScalarContext('remaining_api_calls_day',
                                   args.apicalls_day_warning,
                                   args.apicalls_day_critical),
        nagiosplugin.ScalarContext('script_runtime', ':10'),
        KeynoteSummary(args.measurement_slot)
        )
    check.main(verbose=args.verbose, timeout=args.timeout)

if __name__ == '__main__':
    main()
