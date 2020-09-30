#!/usr/bin/python3
import requests
import argparse
import json

VERSION = 1.01
data_list = [('IP address','query'),('Latitude','lat'),('Longitude','lon'),('District','district'),('City','city'),('Zip code','zip'),('Region/state','regionName'),('Region/state code','region'),('Country','country'),('Country code','countryCode'),('Time zone','timezone'),('Currency','currency'),('Continent','continent'),('Continent code','continentCode'),('ISP','isp'),('Organization','org'),('AS','as'),('AS name','asname'),('Hosting','hosting'),('Proxy','proxy')]

def info(ips):
    if(len(ips)==0):
        url = 'http://ip-api.com/json?fields=status,message'
    else:
        url = 'http://ip-api.com/batch?fields=status,message'
    
    for d in data_list:
        url += ','+d[1]
    
    try:
        res = requests.post(url,data=json.dumps(ips))
    except:
        print('Network connection failed.')
        return
    
    if(res.status_code != 200):
        print('HTTP error occurred. Code {}.'.format(res.status_code))
        return
    
    res = res.json()
    res = [res] if(not isinstance(res,list)) else res

    for r in res:
        if(r['status'] != 'success'):
            print('Query failed for IP:',r['query'],'\nReason:',r['message'])
        else:
            for d in data_list:
                print(d[0]+':',r[d[1]])
        
        print()

def main():
    parser = argparse.ArgumentParser(description='Show info about an IP. Pass no argument to view info about this machine\'s IP.',add_help=False)
    parser.add_argument(type=str,dest='ips',nargs='*',metavar='IP')
    parser.add_argument('-v','--version',help='Prints version information.',action='version',version= 'v'+str(VERSION))
    parser.add_argument('-h','--help', help='Show this help message and exit.',action='help')
    args = parser.parse_args()
    info(args.ips)

if __name__ == "__main__":
    main()
