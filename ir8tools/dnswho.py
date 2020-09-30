#!/usr/bin/python3
import requests
import argparse
import json
import random
import string

VERSION = 1.01

def info():
    rand = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(32))
    try:
        res = requests.get('http://'+rand+'.edns.ip-api.com/json')
    except:
        print('Network connection failed.')
        return
    
    if(res.status_code != 200):
        print('HTTP error occurred. Code {}.'.format(res.status_code))
        return
    
    res = res.json()['dns']

    print('Server IP:',res['ip'])
    print('Server geolocation:',res['geo'])

def main():
    parser = argparse.ArgumentParser(description='Show info about the DNS server you are using.')
    parser.add_argument('-v','--version',help='Prints version information.',action='version',version= 'v'+str(VERSION))
    parser.parse_args()
    
    info()

if __name__ == "__main__":
    main()
