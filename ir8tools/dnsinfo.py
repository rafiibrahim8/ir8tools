#!/usr/bin/python3
import dns.resolver as resolver
import dns.exception
import dns.rdatatype
import argparse

VERSION = 1.0
types = ['A', 'AAAA', 'AFSDB', 'ALIAS', 'ATMA', 'CAA', 'CERT', 'CNAME', 'DHCID', 'DNAME', 'DNSKEY', 'DS', 'HINFO', 'ISDN', 'LOC', 'MB', ' MG', ' MINFO', ' MR', 'MX', 'NAPTR', 'NS', 'NSAP', 'NSEC', 'NSEC3', 'NSEC3PARAM', 'PTR', 'RP', 'RRSIG', 'RT', 'SOA', 'SRV', 'TLSA', 'TXT', 'X25']

def info(domain, query_type):
    try:
        answers = resolver.query(domain, query_type)
    except resolver.NXDOMAIN:
        print('The domain', "'"+domain+"'", 'does not exist.')
        return
    except resolver.NoAnswer:
        print('There is no record for:', query_type)
        return
    except resolver.NoNameservers:
        print('Nameservers not found for domain:', domain)
        return
    except dns.rdatatype.UnknownRdatatype:
        print('Unknown query type:',query_type)
        return
    except dns.exception.Timeout as timeout:
        print(timeout)
        return
    
    for answer in answers:
        print(answer)

def main():
    parser = argparse.ArgumentParser(description='Show dns records (i.e.: NS, MX, A, AAAA) of a domain.')
    parser.add_argument('-v','--version',help='Prints version information.',action='version',version= 'v'+str(VERSION))
    parser.add_argument(metavar='TYPE', dest='query_type', help='Type of record (i.e.: NS, MX, A, AAAA). Pass ALL for query all records.')
    parser.add_argument(metavar='DOMAIN', dest='domain', help='The domain to run query.')
    args = parser.parse_args()

    if(args.query_type.upper() == 'ALL'):
        for t in types:
            print(t+' >')
            info(args.domain, t)
            print()
    else:
        info(args.domain, args.query_type.upper())

if __name__ == "__main__":
    main()
