# -*- coding: utf-8 -*-
import urllib
import subprocess
import json
import time
import re
import os
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


def get_area_data_xml_raw(zipcodes):
    urlbase = 'http://www.zillow.com/webservice/GetDemographics.htm?'
    state = zipcodes[0]

    for zipcode in zipcodes[1:]:
        zid1 = 'X1-ZWz1b7g73ieivf_1zmzq'
        zid2 = 'X1-ZWz1dt3t3sdxxn_31kch'
        params = {'zws-id': zid2, \
                'zip':zipcode}
        url = urlbase + urllib.urlencode(params)
        print url
        p = subprocess.Popen(['curl', url], stdout=subprocess.PIPE)
        result_xml = p.communicate()[0]
        root = ET.fromstring(result_xml)
        if root[1][0].text != 'Request successfully processed':
            print root[1][0].text
            break
        time.sleep(0.5)
        path = state + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(path + str(zipcode), 'w+')
        f.write(result_xml)
        f.close()

def get_area_data_by_state_raw(state):
    f = open('../' + state + '.txt')
    zipcodes = f.read().split('\n')

    idx = zipcodes.index('14750')
    zipcodes = zipcodes[idx+1:]

    zipcodes = [state] + zipcodes
    zipcodes = zipcodes[0:-1]
    get_area_data_xml_raw(zipcodes)

def get_area_data_by_state(state):
    f = open('../' + state + '.txt')
    zipcodes = f.read().split('\n')

    zipcodes = [state] + zipcodes
    zipcodes = zipcodes[0:-1]

    data = get_area_data_by_zipcode(zipcodes)

    f = open('../stat/' + state, 'w')
    f.write(json.dumps(data, indent = 4))
    f.close()


def get_area_data_by_zipcode(zipcodes):
    zip_datas = {}
    for zipcode in zipcodes[1:]:
        print zipcode
        try:
            f = open(zipcodes[0] + '/' + str(zipcode))
        except Exception, e:
            print e
            continue
        root = ET.fromstring(f.read())
        if root[1][0].text != 'Request successfully processed':
            print root[1][0].text
            break

        zip_data = {}
        zip_data['zipcode'] = zipcode
        zip_data['state'] = root.findall('./response/region/state')[0].text
        # zip_data['city'] = root.findall('./response/region/city')[0].text
        zip_data['lat'] = root.findall('./response/region/latitude')[0].text
        zip_data['lot'] = root.findall('./response/region/longitude')[0].text

        pages = root.findall('./response/pages/page')
        aff_page = pages[0]
        attrs = aff_page.findall('./tables/table/data/attribute')
        for attr in attrs:
            name = attr.findall('./name')[0].text
            l = attr.findall('./values/zip')
            if len(l) == 0:
                value = 0
            else:
                value = l[0][0].text
            zip_data[name] = value


        zip_datas[zipcode] = zip_data
    return zip_datas

get_area_data_by_state_raw('NY')