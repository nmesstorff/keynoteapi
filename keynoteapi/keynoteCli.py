#!/usr/bin/env python
"""
    CLI tool for interacting with keynote.com services

    (c) 2015 Norman Messtorff <normes@normes.org>
"""

import argparse
import keynotecli


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
    args = argp.parse_args()

    keycli = keynotecli.KeynoteCli(args.apikey)
    # to be solved by an own ArgumentParser.Action later #TODO
    if args.list_measurement_slots:
        keycli.listMeasurements()
        exit(0)

if __name__ == '__main__':
    main()
