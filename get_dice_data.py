# -*- coding: utf-8 -*-
import urllib
import subprocess
import json
import time
import re
import os
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


#  Get raw json from dice api given parameters 
def get_json_from_dice(text = '', skill = '', state = '', page = ''):
    params = {'text': text, 
              'skill': skill,
              'state': state,
              'page': page}
    urlbase = 'http://service.dice.com/api/rest/jobsearch/v1/simple.json?'
    url = urlbase + urllib.urlencode(params)
    print url
    p = subprocess.Popen(['curl', url], stdout=subprocess.PIPE)
    return p.communicate()[0]

# Use map reduce to extract job details like(skills needed, degree, job location)
# number of openings, how long the job has been posted

def get_jobs_from_dice(text = '' , skill = '', state = '', output_path = ''):
    jobs_json = json.loads(get_json_from_dice(text, skill, state, 1))
    page_num = jobs_json['count'] / 50
    print page_num
    jobs = []
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # print jobs_json['resultItemList']
    for i in range(2, page_num + 1):
        jj = json.loads(get_json_from_dice(text, skill, state, i))
        jobs = jobs + jj['resultItemList']
        factor = 50
        if (i / factor > 0 and i % factor == 0) or (i == page_num):
            
            f = open(output_path + '/' + str(i/factor), 'w')
            f.write(json.dumps(jobs))
            f.close()
            jobs = []
        time.sleep(0.5)
    

def extract_jobskill_from_dice(detail_url):
    p = subprocess.Popen(['curl', detail_url], stdout=subprocess.PIPE)
    result = p.communicate()[0]
    if 'Moved Temporarily' in result:
        soup = BeautifulSoup(result)
        redirect_url = soup.a['href']
        p = subprocess.Popen(['curl', redirect_url], stdout=subprocess.PIPE)
        result = p.communicate()[0]

    soup = BeautifulSoup(result)
    
    dl_set = soup.find_all('dl')
    for dl in dl_set:
        if dl == None or dl.dt == None:
            continue
        if dl.dt.string == 'Skills:':
            if dl.dd == None or dl.dd.string == None:
                continue
            skills = dl.dd.string

            return skills.encode('utf-8')
    return 'NOT FOUND'    
            
            


#  Get raw json of articles from New York Times api given keyword
def get_json_from_nyt(title, begin_date, end_date):
    params = {'title': title,
              'begin_date': begin_date,
              'end_date': end_date,
              'api-key': 'ae38bd69490377413c6cd3d71490d9a6:14:69168845'}
    urlbase = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?'
    url = urlbase + urllib.urlencode(params)
    p = subprocess.Popen(['curl', url], stdout=subprocess.PIPE)
    return p.communicate()[0]


occupations = ['Nurse']
for ocpt in occupations:
    #get raw json data
    print '------------------ Getting raw data for ' + ocpt
    get_jobs_from_dice(text = ocpt, output_path = ocpt)
    
    #get job detail
    print '------------------ Extracting skill data for ' + ocpt
    raw_files = os.listdir(ocpt + '/')
    for raw_file in raw_files:
        f = open(ocpt + '/' + raw_file)
        jobs = json.loads(f.read())
        for job in jobs:
            job['skills'] = extract_jobskill_from_dice(job['detailUrl'])
        f.close()
        
        f = open(ocpt + '/' + raw_file + '_post.json', 'w')
        f.write(json.dumps(jobs, indent = 4))
        f.close()


# # print get_json_from_nyt("obama", '20130101', '20140409')

# #get_jobs_from_dice(title = 'Software')
# f = open('2')
# jobs = json.loads(f.read())
# for job in jobs:
#     job['skills'] = extract_jobskill_from_dice(job['detailUrl'])
# f.close()
# f = open('2-s', 'w')
# f.write(json.dumps(jobs))
# f.close()