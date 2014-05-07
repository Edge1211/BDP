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

zid1 = 'X1-ZWz1b7g73ieivf_1zmzq'
zid2 = 'X1-ZWz1dt3t3sdxxn_31kch'

# get the xml raw data from Zillow, given a list of zipcodes/region id
def get_area_data_xml_raw(zipcodes, is_region_id = False):
    urlbase = 'http://www.zillow.com/webservice/GetDemographics.htm?'
    state = zipcodes[0]
    print 'Getting raw data for area: ' + state

    for zipcode in zipcodes[1:]:
        area_param = 'zip'
        if is_region_id:
            area_param = 'regionid'
        params = {'zws-id': zid2, \
                area_param: zipcode}
        url = urlbase + urllib.urlencode(params)
        path = state + '/'

        print 'Getting raw data for zip: ' + str(zipcode)
        if os.path.exists(path + str(zipcode)):
            print 'Data alreay got for zip: ' + str(zipcode)
            continue
        print url

        p = subprocess.Popen(['curl', url], stdout=subprocess.PIPE)
        result_xml = p.communicate()[0]
        root = ET.fromstring(result_xml)
        if root[1][0].text != 'Request successfully processed':
            print root[1][0].text
            break
        time.sleep(0.5)
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

# get area data given a list of zipcodes/region id, parse the xml raw data to get structured data
def get_area_data_by_zipcode(zipcodes):
    zip_datas = {}
    for zipcode in zipcodes[1:]:
        print 'Parsing xml for zip:' + str(zipcode)
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
                nations = attr.findall('./values/nation')
                if len(nations) == 2:
                    value = nations[0][0].text
                else:
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

def get_national_region_data():
    states = get_all_states()
    region_data = {}
    for state in states:
        region_data[state] = get_region_data_by_state(state)
    f = open('region_data.json', 'w')
    f.write(json.dumps(region_data, indent = 4))
    f.close()

# get region data from Zillow
def get_region_data_by_state(state):
    urlbase = 'http://www.zillow.com/webservice/GetRegionChildren.htm?'
    params = {'zws-id': zid2, \
                'state':state}
    url = urlbase + urllib.urlencode(params)

    print 'Getting region data of state: ' + state
    p = subprocess.Popen(['curl', url], stdout=subprocess.PIPE)
    result_xml = p.communicate()[0]
    # result_xml = '''<?xml version="1.0" encoding="utf-8"?><RegionChildren:regionchildren xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.zillow.com/static/xsd/RegionChildren.xsd http://www.zillowstatic.com/vstatic/d7b385b/static/xsd/RegionChildren.xsd" xmlns:RegionChildren="http://www.zillow.com/static/xsd/RegionChildren.xsd"><request><state>NY</state></request><message><text>Request successfully processed</text><code>0</code></message><response><region><id>43</id><latitude>42.754496</latitude><longitude>-75.809189</longitude></region><subregiontype>county</subregiontype><list><count>62</count><region><id>581</id><name>Kings</name><zindex currency="USD">571700</zindex><latitude>40.651781</latitude><longitude>-73.94545</longitude></region><region><id>1347</id><name>Queens</name><zindex currency="USD">474000</zindex><latitude>40.677704</latitude><longitude>-73.831405</longitude></region><region><id>2452</id><name>New York</name><zindex currency="USD">1166600</zindex><latitude>40.780651</latitude><longitude>-73.971286</longitude></region><region><id>2046</id><name>Suffolk</name><zindex currency="USD">341600</zindex><latitude>40.884668</latitude><longitude>-72.676567</longitude></region><region><id>401</id><name>Bronx</name><zindex currency="USD">312900</zindex><latitude>40.851601</latitude><longitude>-73.856998</longitude></region><region><id>1252</id><name>Nassau</name><zindex currency="USD">434900</zindex><latitude>40.752674</latitude><longitude>-73.601799</longitude></region><region><id>3148</id><name>Westchester</name><zindex currency="USD">509800</zindex><latitude>41.122733</latitude><longitude>-73.733074</longitude></region><region><id>157</id><name>Erie</name><latitude>42.768354</latitude><longitude>-78.800282</longitude></region><region><id>1223</id><name>Monroe</name><zindex currency="USD">125100</zindex><latitude>43.153767</latitude><longitude>-77.684551</longitude></region><region><id>2511</id><name>Richmond</name><zindex currency="USD">389100</zindex><latitude>40.572243</latitude><longitude>-74.151077</longitude></region><region><id>2465</id><name>Onondaga</name><latitude>43.021362</latitude><longitude>-76.198051</longitude></region><region><id>1290</id><name>Orange</name><zindex currency="USD">200900</zindex><latitude>41.387728</latitude><longitude>-74.354961</longitude></region><region><id>2255</id><name>Dutchess</name><zindex currency="USD">230200</zindex><latitude>41.759861</latitude><longitude>-73.74414</longitude></region><region><id>823</id><name>Albany</name><zindex currency="USD">188100</zindex><latitude>42.614773</latitude><longitude>-73.971241</longitude></region><region><id>2515</id><name>Rockland</name><zindex currency="USD">375400</zindex><latitude>41.160851</latitude><longitude>-74.06139</longitude></region><region><id>1283</id><name>Oneida</name><latitude>43.239206</latitude><longitude>-75.47834</longitude></region><region><id>2529</id><name>Saratoga</name><zindex currency="USD">230600</zindex><latitude>43.086609</latitude><longitude>-73.867153</longitude></region><region><id>1946</id><name>Niagara</name><zindex currency="USD">108200</zindex><latitude>43.195911</latitude><longitude>-78.768135</longitude></region><region><id>895</id><name>Broome</name><zindex currency="USD">128000</zindex><latitude>42.206671</latitude><longitude>-75.745247</longitude></region><region><id>1448</id><name>Ulster</name><zindex currency="USD">189400</zindex><latitude>41.87871</latitude><longitude>-74.346092</longitude></region><region><id>3004</id><name>Rensselaer</name><zindex currency="USD">168500</zindex><latitude>42.711363</latitude><longitude>-73.525695</longitude></region><region><id>3137</id><name>Schenectady</name><zindex currency="USD">152500</zindex><latitude>42.833186</latitude><longitude>-74.058448</longitude></region><region><id>2900</id><name>Chautauqua</name><latitude>42.284292</latitude><longitude>-79.410805</longitude></region><region><id>1296</id><name>Oswego</name><zindex currency="USD">95400</zindex><latitude>43.431244</latitude><longitude>-76.186829</longitude></region><region><id>2748</id><name>Jefferson</name><zindex currency="USD">131500</zindex><latitude>44.035649</latitude><longitude>-75.909012</longitude></region><region><id>3249</id><name>Saint Lawrence</name><zindex currency="USD">74300</zindex><latitude>44.53307</latitude><longitude>-75.193218</longitude></region><region><id>1952</id><name>Ontario</name><latitude>42.808064</latitude><longitude>-77.287922</longitude></region><region><id>1343</id><name>Putnam</name><zindex currency="USD">293600</zindex><latitude>41.424351</latitude><longitude>-73.756748</longitude></region><region><id>2578</id><name>Tompkins</name><zindex currency="USD">183500</zindex><latitude>42.445006</latitude><longitude>-76.467567</longitude></region><region><id>2039</id><name>Steuben</name><latitude>42.289486</latitude><longitude>-77.35778</longitude></region><region><id>796</id><name>Wayne</name><latitude>43.177903</latitude><longitude>-77.038818</longitude></region><region><id>1610</id><name>Chemung</name><latitude>42.146881</latitude><longitude>-76.75106</longitude></region><region><id>1630</id><name>Clinton</name><zindex currency="USD">113500</zindex><latitude>44.720226</latitude><longitude>-73.680832</longitude></region><region><id>3088</id><name>Cattaraugus</name><zindex currency="USD">74500</zindex><latitude>42.270309</latitude><longitude>-78.684944</longitude></region><region><id>929</id><name>Cayuga</name><zindex currency="USD">106600</zindex><latitude>43.017945</latitude><longitude>-76.503162</longitude></region><region><id>2567</id><name>Sullivan</name><latitude>41.719138</latitude><longitude>-74.755828</longitude></region><region><id>1909</id><name>Madison</name><zindex currency="USD">123100</zindex><latitude>42.954476</latitude><longitude>-75.617027</longitude></region><region><id>1479</id><name>Warren</name><zindex currency="USD">196000</zindex><latitude>43.512839</latitude><longitude>-73.826175</longitude></region><region><id>2961</id><name>Livingston</name><latitude>42.729724</latitude><longitude>-77.774166</longitude></region><region><id>2214</id><name>Columbia</name><latitude>42.243902</latitude><longitude>-73.64151</longitude></region><region><id>1298</id><name>Otsego</name><zindex currency="USD">110500</zindex><latitude>42.611182</latitude><longitude>-75.023368</longitude></region><region><id>2340</id><name>Herkimer</name><latitude>43.460884</latitude><longitude>-74.957531</longitude></region><region><id>3066</id><name>Washington</name><zindex currency="USD">122400</zindex><latitude>43.374774</latitude><longitude>-73.439484</longitude></region><region><id>1722</id><name>Genesee</name><latitude>42.997992</latitude><longitude>-78.185074</longitude></region><region><id>1024</id><name>Fulton</name><zindex currency="USD">113100</zindex><latitude>43.135899</latitude><longitude>-74.436249</longitude></region><region><id>2186</id><name>Chenango</name><zindex currency="USD">88300</zindex><latitude>42.470152</latitude><longitude>-75.591759</longitude></region><region><id>748</id><name>Tioga</name><zindex currency="USD">106900</zindex><latitude>42.204476</latitude><longitude>-76.322456</longitude></region><region><id>2287</id><name>Franklin</name><zindex currency="USD">85300</zindex><latitude>44.552676</latitude><longitude>-74.318348</longitude></region><region><id>1060</id><name>Greene</name><latitude>42.280327</latitude><longitude>-74.155906</longitude></region><region><id>2119</id><name>Allegany</name><zindex currency="USD">60300</zindex><latitude>42.259826</latitude><longitude>-78.016174</longitude></region><region><id>2979</id><name>Montgomery</name><latitude>42.910133</latitude><longitude>-74.424022</longitude></region><region><id>2224</id><name>Cortland</name><zindex currency="USD">104900</zindex><latitude>42.599197</latitude><longitude>-76.069698</longitude></region><region><id>2248</id><name>Delaware</name><latitude>42.182982</latitude><longitude>-74.925377</longitude></region><region><id>1954</id><name>Orleans</name><latitude>43.252182</latitude><longitude>-78.231373</longitude></region><region><id>2105</id><name>Wyoming</name><zindex currency="USD">98400</zindex><latitude>42.694657</latitude><longitude>-78.221824</longitude></region><region><id>505</id><name>Essex</name><zindex currency="USD">133800</zindex><latitude>44.145623</latitude><longitude>-73.815693</longitude></region><region><id>1373</id><name>Seneca</name><latitude>42.782742</latitude><longitude>-76.783993</longitude></region><region><id>2843</id><name>Schoharie</name><latitude>42.592209</latitude><longitude>-74.438545</longitude></region><region><id>599</id><name>Lewis</name><latitude>43.81864</latitude><longitude>-75.480716</longitude></region><region><id>816</id><name>Yates</name><latitude>42.611697</latitude><longitude>-77.13113</longitude></region><region><id>2533</id><name>Schuyler</name><latitude>42.390141</latitude><longitude>-76.863601</longitude></region><region><id>2321</id><name>Hamilton</name><latitude>43.667551</latitude><longitude>-74.457336</longitude></region></list></response></RegionChildren:regionchildren><!-- H:003  T:221ms  S:6661  R:Mon May 05 09:18:24 PDT 2014  B:4.0.34-release_2014-04-30.baa36eb-RELEASE_CANDIDATE-6768304-20140429.235718.baa36eb402e969a980e3ef3d26db55c7adff3b1c.20140430133516219-origin/release/2014-04-30 -->'''
    root = ET.fromstring(result_xml)
    msg = root.findall('./message/code')[0].text
    if msg != '0':
        print 'Error:' + msg
        return {}
    state_rid = root.findall('./response/region/id')[0].text
    
    ids = root.findall('./response/list/region/id')
    subids = []
    for sid in ids:
        subids.append(sid.text)
    
    state_rdata = {}
    state_rdata['rid'] = state_rid
    state_rdata['subids'] =subids

    return state_rdata





# get data for major metro areas
def get_metro_area_data():
    for metro_area in metro_areas:
        get_area_data_xml_raw(metro_area)
        zipdatas = get_area_data_by_zipcode(metro_area)
        f = open(metro_area[0] + '-stat.json', 'w')
        f.write(json.dumps(zipdatas, indent = 4))
        f.close()

def get_state_data_by_rid():
    states = get_all_states()
    f = open('region_data.json')
    region_data = json.loads(f.read())
    state_stat = {}
    for state in states:
        if state not in region_data:
            continue
        if 'rid' not in region_data[state]:
            continue
        rid = region_data[state]['rid']
        param = [state] + [rid]
        get_area_data_xml_raw(param, True)
        data = get_area_data_by_zipcode(param)

        state_stat[state] = data

    f = open('state-stat.json', 'w')
    f.write(json.dumps(state_stat, indent = 4))
    f.close()




def main():
    # get all states and get area data of every zipcode
    states = get_all_states()
    for state in states:
        #get raw data first
        get_area_data_by_state_raw(state)
        #parse the raw data and extract useful information
        get_area_data_by_state(state)
        #get data for major metro areas
        get_metro_area_data()
        # get national region data
        get_national_region_data()



if __name__ == '__main__':
    main()
    