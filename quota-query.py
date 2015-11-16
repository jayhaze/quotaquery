# This is a query tool, not a creation tool. Could do with better usage instructions to cover what options need to be used in any query.

# Import some of the important things...must install requests, because it makes things (getting around SSL verification) sooo much easier.
import requests, json
import base64
import string
import sys
import traceback
import argparse

# To make it so our breaking of SSL security doesn't yell at us...
import urllib3
urllib3.disable_warnings()

# This is the way we take our arguments...

parser = argparse.ArgumentParser(description='Get things to do')
parser.add_argument('--summary', '-s', help='Print Quota Usage Summary', action='store_true')
parser.add_argument('--all', '-a', help='Get all quota information', action='store_true')
parser.add_argument('--user', '-u', help='Specify user to lookup', type=str, nargs="?")
parser.add_argument('--group', '-g', help='Specify group to lookup', type=str, nargs="?")
parser.add_argument('--directory', '-d', help='Specify directory to lookup', nargs="?")
parser.add_argument('--type', '-t', help='Specify the type of quota', nargs="?")
parser.add_argument('--duser', '-du', help='Lookup default user quota for named directory', action='store_true')
parser.add_argument('--dgroup', '-dg', help='Lookup default group quota for named directory', action='store_true')

args = parser.parse_args()
print args

# Set up the session.  Using API "1" as my current test cluster is pre-Riptide.
HOST = 'https://10.245.108.21:8080/platform'
USER = 'root'
PASSWORD = 'a'
API_VERSION = '1'

# my base URI construct to query quota and other things that are helpful to build here...
QUOTAS_URI = HOST + '/' + API_VERSION + '/quota'

# What do we want to accomplish here?
# We want to know: 
# (1) What is my overall user quota and utilization? 
# (2) What is the quota governance on the directory I am curious about?

# Create a session to do shit.
from requests import Request, Session

s = requests.Session()
s.auth = (USER, PASSWORD)

if args.type == 'user':
	USERNAME = 'USER:' + args.user

	payload = {'path': args.directory, 'persona': USERNAME, 'type': args.type}
	r = s.get(QUOTAS_URI+"/quotas", params=payload, verify=False)
	print(r.url)
	print(r.text)
	
if args.type == 'group':
	GROUPNAME = 'GROUP:' + args.group


	payload = {'path': args.directory, 'persona': GROUPNAME, 'type': args.type}
	r = s.get(QUOTAS_URI+"/quotas", params=payload, verify=False)
	print(r.url)
	print(r.text)
	
if args.type == 'directory':

	payload = {'path': args.directory, 'type': args.type}
	r = s.get(QUOTAS_URI+"/quotas", params=payload, verify=False)
	print(r.url)
	print(r.text)

if args.duser:

	payload = {'path': args.directory, 'type': 'default-user'}
	r = s.get(QUOTAS_URI+"/quotas", params=payload, verify=False)
	print(r.url)
	print(r.text)
	
if args.dgroup:

	payload = {'path': args.directory, 'type': 'default-group'}
	r = s.get(QUOTAS_URI+"/quotas", params=payload, verify=False)
	print(r.url)
	print(r.text)

if args.summary:

	r = s.get(QUOTAS_URI+"/quotas-summary", verify=False)
	print(r.text)

if args.all:

	r = s.get(QUOTAS_URI+"/quotas", verify=False)
	print(r.text)

quit()