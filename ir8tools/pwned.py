#!/usr/bin/python3
import hashlib, requests, argparse

VERSION = 1.0

def do(passwd):
    sha1 = hashlib.sha1(passwd.encode()).hexdigest().upper()
    try:
        res = requests.get('https://api.pwnedpasswords.com/range/' + sha1[:5]).iter_lines()
    except:
        print('Request failed. Check your network.')
        return

    for i in res:
        j = i.decode().upper().split(':')
        if(sha1[5:] == j[0]):
            print('Oh no! Pwned. Your password has been listed password dictionaries.\nYou should change this password immediately.\n')
            print(sha1.lower(),':', j[1],'time(s)')
            return    
    print('Password can not be found in password dictionaries.')

def main():
    parser = argparse.ArgumentParser(description='Check if your password is on password dictionaries.')
    parser.add_argument('-v','--version',help='Prints version information.',action='version',version= 'v'+str(VERSION))
    parser.add_argument(metavar='PASSWORD', dest='passwd', help='Your password which will be checked.')
    args = parser.parse_args()
    do(args.passwd)

if __name__ == '__main__':
    main()
