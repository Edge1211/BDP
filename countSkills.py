#!/usr/bin/python


import sys, os
import operator


def mymap():
    for eachline in sys.stdin:
        elements = eachline.strip().split("\t")
        """

"skills": "NOT FOUND",
 "jobTitle": "Database Design Engineer 4", 
 "company": "NORTHROP GRUMMAN",
  "detailUrl": "http://www.dice.com/job/result/ngitbot/14003579?src=19",
   "location": "San Diego, CA", 
   "date": "2014-04-15"},

        """
        skills = elements[0].strip()
        tokens = skills.strip().split(",")

        job = elements[1].strip()
        for s in range(0, len(tokens)):
            print "%s\t%s" % (job, tokens[s])


def myreduce():
    dic={}
    for eachline in sys.stdin:
        elements = eachline.strip().split("\t")
        job = elements[0].strip()
        # require = elements[1].strip()
        # print "%s\t%s" % (job,require)
        # 
        # print "%s\t%s" % (job, require)
    #     if require in dic:
    #         dic[require] = dic[require] + 1
    #     else:
    #         dic[require] = 1

    # sorted_dic = sorted(dic.iteritems(), key=operator.itemgetter(1), reverse=True)
    # for key in range(0,len(sorted_dic)):
    #     print "%s\t%s" % (sorted_dic[key])

if sys.argv[1] == "Map":
    mymap()
else:
    myreduce()
