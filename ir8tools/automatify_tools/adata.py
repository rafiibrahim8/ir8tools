import requests
import json
from base64 import b64encode, b64decode
from argparse import ArgumentParser
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import os
import time

VERSION = '0.1'
ADMIN=False

def push_impl(type_, field=None, data=None, settings=None):
    body = {
        'time': int(time.time()),
        'type': type_,
        'field': field,
        'data': data,
        'random': b64encode(os.urandom(15)).decode('utf-8')
    }

    body = b64encode(json.dumps(body).encode('utf-8')).decode('utf-8')
    digest = SHA256.new(body.encode('utf-8'))
    private_key = RSA.import_key(b64decode(settings['keep']))
    signer = PKCS1_v1_5.new(private_key)
    signature = b64encode(signer.sign(digest)).decode()

    json_data = {'body':body,'sig':signature,'user': settings['user'],'admin': ADMIN}

    res = requests.post(settings['server'] + '/update',json=json_data)
    return res.status_code

def show_data():
    body = {
        'time': int(time.time()),
        'service':'adata',
        'random': b64encode(os.urandom(15)).decode('utf-8')
    }
    body = b64encode(json.dumps(body).encode('utf-8')).decode('utf-8')
    digest = SHA256.new(body.encode('utf-8'))
    with open(os.path.expanduser('~/.config/ir8tools/adata.conf'),'r') as f:
        settings = json.load(f)
    private_key=RSA.importKey(b64decode(settings['keep']))
    signer = PKCS1_v1_5.new(private_key)
    signature = b64encode(signer.sign(digest)).decode()

    json_data = {'body':body,'sig':signature,'user': settings['user'],'admin': ADMIN}

    res = requests.post(settings['server'] + '/info',json=json_data)
    print(res.text)

def custom_input(prompt, required=False):
    i = input(prompt).strip()
    while(not i and required):
        print('This field is required.')
        i = input(prompt).strip()
    return i if(i) else None

def setup():
    server = custom_input('Enter Server URL(*): ',True).strip('/')
    user = custom_input('Enter username(*): ',True)
    private_key = custom_input('Enter private key (Ask admin if you don\'t have one):', False)
    fbid = custom_input('Enter FB message id (Ask admin if you don\'t have one):', False)
    airtel_fb_graph_id = custom_input('Enter FB key (Ask admin if you don\'t have one)(*):', True)

    pri_key = RSA.importKey(b64decode(private_key))
    pub_key = pri_key.publickey()
    pub_key = b64encode(pub_key.exportKey(format='PEM')).decode('utf-8')

    settings = {
        'server':server,
        'key':pub_key,
        'keep': private_key,
        'fbid' : fbid,
        'user': user,
        'airtel_fb_graph_id': airtel_fb_graph_id
    }
    dir = os.path.expanduser('~/.config/ir8tools')
    os.makedirs(dir,exist_ok=True)
    conf_file = os.path.join(dir,'adata.conf')
    with open(conf_file,'w') as f:
        json.dump(settings,f)

def push():
    with open(os.path.expanduser('~/.config/ir8tools/adata.conf'),'r') as f:
        settings = json.load(f)
    to_push = ['fbid','airtel_fb_graph_id']
    for i in to_push:
        if(push_impl('field',i,settings[i],settings)!=200):
            print('Failed to push {}'.format(i))
    if(push_impl('key',None,settings['key'],settings)!=200):
        print('Failed to push key')

def main():
    parser = ArgumentParser(description='Show airtel (Bangladesh) data balance from command line.')
    parser.add_argument('-v','--version',help='Prints version information.',action='version',version= 'v'+str(VERSION))
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-S','--setup',action='store_true',help='Setup interactively.')
    group.add_argument('-P','--push',action='store_true',help='Push configuration to server.')
    args = parser.parse_args()

    if(args.setup):
        setup()
    elif(args.push):
        push()
    else:
        show_data()

if __name__ == "__main__":
    main()
