#!/usr/bin/env python2

import os.path
import sys
import urllib2
import json
import requests
from argparse import ArgumentParser

#
# Sample data
#
# data = {
#     "title":options.title,
#     "slashtag":options.slashtag,
#     "destination":options.url,
#     "domain": {
#         "id": "123456aaabbbcccd123456aaabbbcccd",
#         "ref": "/domains/123456aaabbbcccd123456aaabbbcccd"
#     }

def shorten_url(post_uri,api_token,data):

    headers = {
      'Content-Type': 'application/json',
      'apikey': api_token
    }

    r = requests.post(post_uri, data=json.dumps(data), headers=headers)

    if r.status_code == 200:
        print "Success!"
        reply = r.json()
        print 'Short url is:',reply['shortUrl']
    else:
        print "Oops: there was an error. Request exited with code:", r.status_code

def list_custom_domains(list_domains_uri,api_token):

    print "Listing custom domains in your account..."

    params = { 'orderBy':'createdAt','orderDir':'desc',
        'offset':'0','limit':100,'status':'active','type':'user'}
    headers = {'apikey': api_token}

    r = requests.get(list_domains_uri, params=params, headers=headers)

    if r.status_code == 200:
        reply = r.json()
        for x in reply:
            print x['fullName'],', ID:',x['id'],', DNS status:',x['status']['dns']
    else:
        print "Oops: there was an error! Request exited with code:", r.status_code

def main():

    post_uri = 'https://api.rebrandly.com/v1/links'
    list_domains_uri = 'https://api.rebrandly.com/v1/domains'

    # Load config
    path = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
    try:
        conf = open(os.path.join(path, 'config.json'), 'r')
        config = json.loads(conf.read())
    except IOError as e:
        print "Error: No config.json found."
        print "Exiting..."
        sys.exit()
    except:
        print "No file found"
        print "Exiting..."
        sys.exit()


    if len(sys.argv)>=2:
        data = {
            'destination':sys.argv[1]
        }
    else:
        print "Error: no URL to shorten specified. Please give one."
        print "Use -h or --help to know available options."
        print "Exiting..."
        sys.exit()

    # Parse command line options
    parser = ArgumentParser(description="Shroten URLs using Rebrandly service.")
    parser.add_argument('url',metavar='URL', nargs=1,
        help="URL to shorten")
    parser.add_argument("-l","--list-domains", action="store_true", dest="list_domains",
        help="list custom domains information (including IDs)")
    parser.add_argument("-t","--title", dest="title",
        help="Specify short link title in dashboard")
    parser.add_argument("-s","--slashtag", dest="slashtag",
        help="Use custom slashtag, e.g. 'mytag' so the shorten url is: domain/mytag")
    parser.add_argument("-c","--custom-domain", action="store_true", dest="custom_domain",
        help="Choose whether to shorten url using favorite custom domain set in config")
    args = parser.parse_args()

    if args.list_domains == True:
        list_custom_domains(list_domains_uri,config['api_token'])
        sys.exit()
    if args.title:
        data.update(title=args.title)
    if args.slashtag:
        data.update(slashtag=args.slashtag)
    if args.custom_domain == True:

        domain_details = {
            'id':config['favorite_custom_domain_id'],
            'ref':'/domains/'+config['favorite_custom_domain_id']
        }

        data.update(domain=domain_details)

    print data # debug
    shorten_url(post_uri,config['api_token'],data)

if __name__ == '__main__':
    main()
