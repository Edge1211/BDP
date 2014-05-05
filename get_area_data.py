# -*- coding: utf-8 -*-
import urllib
import subprocess
import json
import time
import re
import os
import csv
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from data import *

# get the xml raw data from Zillow, given a list of zipcodes
def get_area_data_xml_raw(zipcodes):
    urlbase = 'http://www.zillow.com/webservice/GetDemographics.htm?'
    state = zipcodes[0]
    print 'Getting raw data for area: ' + state

    for zipcode in zipcodes[1:]:
        zid1 = 'X1-ZWz1b7g73ieivf_1zmzq'
        zid2 = 'X1-ZWz1dt3t3sdxxn_31kch'
        params = {'zws-id': zid2, \
                'zip':zipcode}
        url = urlbase + urllib.urlencode(params)
        print url
        print 'Getting raw data for zip: ' + str(zipcode)

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

# get the xml raw data from Zillow, given a state
def get_area_data_by_state_raw(state):
    zipcodes = get_zipcodes_by_state(state)

    zipcodes = [state] + zipcodes
    
    get_area_data_xml_raw(zipcodes)


# get area data given a state
def get_area_data_by_state(state):
    
    zipcodes = get_zipcodes_by_state(state)

    zipcodes = [state] + zipcodes
    data = get_area_data_by_zipcode(zipcodes)

    f = open('../stat/' + state, 'w')
    f.write(json.dumps(data, indent = 4))
    f.close()

# get area data given a list of zipcodes, parse the xml raw data to get structured data
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

# get zip codes by state through zipcode database
def get_zipcodes_by_state(state):
    zipcodes = []
    f = open('zip_code_database.csv')
    lines = [line for line in f]
    f.close()

    for line in lines[1:]:
        ls = line.split(',')
        if ls[0] == state:
            zipcodes.append(ls[1])
    return zipcodes

# get all states in u.s. through zipcode database
def get_all_states():
    f = open('zip_code_database.csv')
    
    lines = [line for line in f]
    f.close()
    states = set()
    for line in lines[1:]:

        ls = line.split(',')
        states.add(ls[0])
    return states

# get data for major metro areas
def get_metro_area_data():
    for metro_area in metro_areas:
        get_area_data_xml_raw(metro_area)




def main():
    # get all states and get area data of every zipcode
    states = get_all_states()
    for state in states:
        #get raw data first
        get_area_data_by_state_raw(state)
        #parse the raw data and extract useful information
        get_area_data_by_state(state)


if __name__ == '__main__':
    #main()
    get_metro_area_data()
