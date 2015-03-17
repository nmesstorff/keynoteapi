#Keynote API
keynoteapi is a Python module to access the Keynote Systems API (api.keynote.com) with your personal API token.

*This module runs only with Python 2.6 and above. Compatibility for Python 3 is in progress!*

[![Travis CI Build Status](https://travis-ci.org/nmesstorff/keynoteapi.png)](https://travis-ci.org/nmesstorff/keynoteapi)
[![Coverage Status](https://coveralls.io/repos/nmesstorff/keynoteapi/badge.png)](https://coveralls.io/r/nmesstorff/)

##Features
 - access dashboarddata
 - cached requests to minimize API usage (Keynote Systems has a limit per hour and day)
 - Nagios check to integrate the measurements into your regular monitoring system

##Requirements
You need a API token to use the keynote API: http://api.keynote.com/apiconsole/apikeygen.aspx

Install all needed python modules via pip:
`pip install -r requirements.txt`

##Examples / How to start
 - Every command will print you a small help when starting with the '-h' or '--help' argument.
    `./keynoteCli.py -h`
    `./keynoteCli.py --help`
    `./check_keynote.py -h`

 - List measurements
    `./keynoteCli.py -k YOUR_TOKEN -l`

 - Nagios check one of your measurement slots
    `./check_keynote.py -k YOUR_TOKEN -m MEASUREMENT`

 - Use an environment variable for your API token

    `export KEYNOTE_API_KEY=the-keynote-api-token-goeas-here`
 
    `./keynoteCli.py -l`

##Running tests
To run the tests and create a coverage report:

    python setup.py nosetests

##Version numbers
Releases are versioned via 'Semantic Versioning' - see http://semver.org.
Which meens in short:

Example Version 2.1.4-rc1 as MAJOR.MINOR.PATCH-EXTENSION
 - MAJOR: expect breaking API changes
 - MINOR: compatible new features and improvements
 - PATCH: compatible bugfixes
 - (optional) EXTENSION: label for special releases like 'rc' for release candidates.


##Support
For questions or bugs [create an issue on GitHub](https://github.com/nmesstorff/keynoteapi/issues/new).

##Contribute
I'm happy to receive pull requests from you! But please clean all flake8 errors *and* warnings before.
If i ask you to change something: `git commit --amend`

##License
See LICENSE file.
The content of tests/json and tests/xml are based on the examples from Keynote Systems: http://api.keynote.com/apiconsole/apistatus.aspx?page=docs

##Contact
Norman Meßtorff
eMail: normes at normes dot org
