#!/usr/bin/env python

import urllib
import urllib2
from optparse import OptionParser
import sys
import logging

#loging starts
logging.basicConfig(filename='/tmp/marketing.log', level=logging.DEBUG)


def parse_options():

    parser = OptionParser()

    parser.add_option('-e', '--email-address', dest='email', type="string", help='Set email address')
    parser.add_option('-b', '--business-phone', dest='phone', type="string", help='Set phone')
    parser.add_option('-f', '--first-name', dest='fname', type="string", help='Set first name')
    parser.add_option('-l', '--last-name', dest='lname', type="string", help='Set last name')
    parser.add_option('-r', '--job-role', dest='jobrole', type="string", help='Set job role')
    parser.add_option('-j', '--job-function', dest='jobfunction', type="string", help='Set job function')
    parser.add_option('-c', '--company', dest='company', type="string", help='Set company')

    (options, args) = parser.parse_args()

    if (options.email is None or options.phone is None or options.fname is None or options.lname is None or
        options.jobrole is None or options.jobfunction is None or options.company is None):
      logging.info("required parameter cannot be empty")
      sys.exit(1)
    return options

def postEulaInfo(firstName, lastName, emailAddress, company,jobRole, jobFunction, businessPhone):
    elqFormName='Cloudera_Azure_EULA'
    elqSiteID='1465054361'
    cid='70134000001PsLS'
    url = 'https://s1465054361.t.eloqua.com/e/f2'
    data = urllib.urlencode({'elqFormName': elqFormName,
                             'elqSiteID': elqSiteID,
                             'cid': cid,
                             'firstName': firstName,
                             'lastName': lastName,
                             'company': company,
                             'emailAddress': emailAddress,
                             'jobRole': jobRole,
                             'jobFunction': jobFunction,
                             'businessPhone': businessPhone
                            })
    results = urllib2.urlopen(url, data)
    logging.info(results.read())

def main():
    # Parse user options
    logging.info("parse_options")
    options = parse_options()
    postEulaInfo(options.fname, options.lname, options.email, options.company, options.jobrole, options.jobfunction,
                 options.phone)

if __name__ == "__main__":
    main()