#!/usr/bin/env python

import sys
import requests
import json
import xml.etree.ElementTree as xml

MWG_URL = 'http://1.1.1.1' #url of the web gateway
MWG_PORT = '4711' #port of the web gateway
MWG_USER = 'admin' #username
MWG_PWD = 'password' #password
VERIFY = False #https verification

def login(headers):
    auth = {'userName': MWG_USER,
            'pass': MWG_PWD}

    res = requests.post(MWG_URL + ':' + MWG_PORT + '/Konfigurator/REST/login', headers=headers, params=auth, verify=VERIFY)

    if res.status_code == 200:
        print('Successfull logged in')
    else:
        print('Something went wrong')
        sys.exit(1)

    return res.cookies['JSESSIONID']

def get_list_id(headers, cookies, list):
    params = {'name': list}
    res = requests.get(MWG_URL + ':' + MWG_PORT + '/Konfigurator/REST/list', headers=headers, cookies=cookies, params=params, verify=VERIFY)
    res_parse = xml.fromstring(res.content).find('entry/id')

    if res.status_code == 200:
        print('The ID for the list {0} is: {1}'.format(list, res_parse.text))
    else:
        print('Something went wrong')
        sys.exit(1)

    return res_parse.text

def insert_list(headers, cookies, list, list_id, value):
    data = '''
            <entry xmlns="http://www.w3org/2011/Atom">
                <content type="application/xml">
                    <listEntry>
                        <entry>{}</entry>
                        <description></description>
                    </listEntry>
                </content>
            </entry>
            '''
    data = data.format(value)

    res = requests.post(MWG_URL + ':' + MWG_PORT + '/Konfigurator/REST/list/' + list_id + '/entry/0/insert', \
            headers=headers, cookies=cookies, data=data, verify=VERIFY)

    if res.status_code == 200:
        print('Successfull added the IP/Domain {0} to the list {1}'.format(value, list))
    else:
        print res.content
        print('Something Went Wrong')
    return res

def commit(headers, cookies):
    res = requests.post(MWG_URL + ':' + MWG_PORT + '/Konfigurator/REST/commit', headers=headers, cookies=cookies, verify=VERIFY)
    return res.content

def logout(headers, cookies):
    res = requests.post(MWG_URL + ':' + MWG_PORT + '/Konfigurator/REST/logout', headers=headers, cookies=cookies, verify=VERIFY)

    if res.status_code == 200:
        print('Successfull Logged Out')
    else:
        print('Something Went Wrong')
    return res

if __name__ == "__main__":

    list = 'Global Block: Sites' #list to edit
    value = sys.argv[1]

    headers = {'Content-Type': 'application/xml'}

    cookie = login(headers)
    cookies = {'JSESSIONID': cookie}

    list_id = get_list_id(headers, cookies, list)

    insert = insert_list(headers, cookies, list, list_id, value)
    commit = commit(headers, cookies)

    logout = logout(headers, cookies)
