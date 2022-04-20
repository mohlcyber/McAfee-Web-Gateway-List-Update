#!/usr/bin/env python

import sys
import xml.etree.ElementTree as xml

import requests
from requests.structures import CaseInsensitiveDict


MWG_URL = "https://1.1.1.1"  # url of the web gateway
MWG_PORT = "4712"  # port of the web gateway
MWG_USER = "user"  # username
MWG_PWD = "password"  # password
VERIFY = False  # https verification

def login(headers):
    auth = {'userName': MWG_USER,
            'pass'    : MWG_PWD}
    requests.packages.urllib3.disable_warnings()

    res = requests.post(MWG_URL + ':' + MWG_PORT + '/Konfigurator/REST/login', headers=headers, params=auth, verify=VERIFY)

    if res.status_code == 200:
        print('Successfull logged in')
    else:
        print('Something went wrong')
        sys.exit(1)

    return res.cookies['JSESSIONID']


def create_backup(headers, cookies):
    res = requests.post(MWG_URL + ':' + MWG_PORT + '/Konfigurator/REST/backup', cookies=cookies, headers=headers, verify=VERIFY)
    with open('backup.txt', 'w') as f:
        f.writelines(res.text)


def get_list_id(headers, cookies, list):
    params = {'name': list}
    try:
        res = requests.get(MWG_URL + ':' + MWG_PORT + '/Konfigurator/REST/list', cookies=cookies, params=params, headers=headers, verify=VERIFY)

        if res.status_code == 200:
            res_parse = xml.fromstring(res.text).find('entry/id')
            print('The ID for the list {0} is: {1}'.format(list, res_parse.text))
            # com.scur.type.regex.4518
        else:
            print('Get_list_id: Something went wrong')
            sys.exit(1)
    except:
        pass

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

    try:
        res = requests.post(MWG_URL + ':' + MWG_PORT + '/Konfigurator/REST/list/' + list_id + '/entry/0/insert', \
                            headers=headers, cookies=cookies, data=data, verify=VERIFY)

        if res.status_code == 200:
            print('Successfull added the IP/Domain {0} to the list {1}'.format(value, list))
        else:
            print(res.content, 'Something Went Wrong')
    except:
        pass
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

    list = 'Blocked Clients'  # list to edit
    value = sys.argv[1]
    headers = CaseInsensitiveDict()
    headers = {'Content-Type': 'application/xml'}

    try:
        cookie = login(headers)
        cookies = {'JSESSIONID': cookie}
        # create_backup(headers, cookies)
        list_id = get_list_id(headers, cookies, list)

        insert = insert_list(headers, cookies, list, list_id, str(value))
        commit = commit(headers, cookies)

        logout = logout(headers, cookies)
    except:
        print("Exit with errors")
        logout = logout(headers, cookies)
        exit(1)
