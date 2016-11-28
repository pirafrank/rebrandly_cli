#!/usr/bin/env python2

import os.path
import sys
import urllib2
import json
import requests
from optparse import OptionParser

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
        print r.json()
    else:
        print "Oops: there was an error. Request exited with code:", r.status_code

def list_custom_domains(list_domains_uri,api_token):

    print "Custom domains in your account"

    params = { 'orderBy':'createdAt','orderDir':'desc',
        'offset':'0','limit':100,'status':'active','type':'user'}
    headers = {'apikey': api_token}

    r = requests.get(list_domains_uri, params=params, headers=headers)

    if r.status_code == 200:
        print r.json()
    else:
        print "Oops: there was an error. Request exited with code:", r.status_code

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

    if sys.argv[1]:
        data = {
            'destination':sys.argv[1]
        }
    else:
        print "Error: no url to shorten specified. Please give one."
        print "Use -h or --help to know available options."
        print "Exiting..."
        sys.exit()

    parser = OptionParser()
    parser.add_option("-l","--list-domains", dest="list_domains", default=False,
        help="list custom domains information (including IDs)")
    parser.add_option("-t","--title", dest="title",
        help="specify short link title in dashboard")
    parser.add_option("-s","--slashtag", dest="slashtag",
        help="use custom slashtag, e.g. /mytag")
    parser.add_option("-c","--custom-domain", dest="custom_domain", default=False,
        help="shorten url using set custom domain")
    (options, args) = parser.parse_args()

    if options.list_domains == True: # @todo this should be doable without url
        list_custom_domains(list_domains_uri,config['api_token'])
    elif options.title:
        data.update(title=options.title)
    elif options.slashtag:
        data.update(slashtag=options.slashtag)
    elif options.custom_domain:

        domain_details = {
            'id':favorite_custom_domain_id,
            'ref':'/domains/'+config['favorite_custom_domain_id']
        }

        data.update(domain=domain_details)
    shorten_url(post_uri,config['api_token'],data)

if __name__ == '__main__':
    main()