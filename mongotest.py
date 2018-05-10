//#!/usr/bin/python
# -*- coding: utf-8 -*-

from pymongo import MongoClient 
import sys
import time
import json
from pprint import pprint 

def connect_to_db():
	con = MongoClient()
	return con

def run_query(db,collection,query):
	coll = con[db][collection]
	
	rows = list(coll.aggregate(query,allowDiskUse=True))
	return rows

fulltests = [
 [{"$unwind":"$prescriptions"}, {"$group" : { "_id": True , "t" : {"$sum" : "$prescriptions.cost"}}}],
 [{ "$group" : { "_id": True , "t" : {"$sum" : {"$sum": "$prescriptions.cost"}}}}],
 [{"$unwind":"$prescriptions"}, {"$group" : { "_id": "$period" , "t" : {"$sum" : "$prescriptions.cost"}}}],
 [{ "$group" : { "_id": "$period" , "spend" : {"$sum" : {"$sum": "$prescriptions.cost"}}}}],
 [{ "$group" : { "_id": "$practice" , "spend" : {"$sum" : {"$sum": "$prescriptions.cost"}}}},{"$sort":{"spend":-1}},{"$limit":5}],
 [{ "$group" : { "_id": "$practice","perpatient": {"$sum": {"$divide": [{"$sum": "$prescriptions.cost"}, "$numpatients"]}}}},{"$sort":{"perpatient":-1}},{"$limit":5}],
 [{ "$group" : { "_id": { "county": "$address.county", "practice": "$practice"},"spend" : { "$sum" : {"$sum" : "$prescriptions.cost"}},"numpatients" : { "$avg" : "$numpatients"}}},{ "$group": { "_id" : "$_id.county", "spend" : { "$sum" : "$spend" },"numpatients" : {"$sum": "$numpatients"}}},{"$addFields" : { "costperpatient" : { "$divide" : ["$spend","$numpatients"] }}},{"$match" : { "numpatients" : { "$gt" : 100000}}},{"$sort" : { "costperpatient" : -1}},{"$limit":20} ],
[{"$unwind":"$prescriptions"},
  {"$group" : { "_id" : "$prescriptions.bnfcode",
"name" : { "$max":"$prescriptions.name"},
"items" : {"$sum" : "$prescriptions.nitems"}  }},
{"$sort" : { "items" : -1}},
{"$limit":10}]
 ]


tests = [
[{"$unwind":"$prescriptions"},
  {"$group" : { "_id" : "$prescriptions.bnfcode",
"name" : { "$max":"$prescriptions.name"},
"items" : {"$sum" : "$prescriptions.nitems"}  }},
{"$sort" : { "items" : -1}},
{"$limit":10}]
   ]

sqltests = [ 
"""select sum(cost) from prescriptions;""",
"""select sum(cost) from prescriptions group by period;""",
"""select practice,sum(cost) as totalspend from prescriptions 
 group by practice
  order by totalspend desc 
  limit 5;""",
"""select practice,sum(cost/numpatients) as totalspend,avg(numpatients)
 from prescriptions,patientcounts 
 where prescriptions.practice=patientcounts.code
   group by practice 
   order by totalspend 
   desc limit 5;""",
"""select county,sum(totalcost) as spend,sum(patients) as patients,sum(totalcost)/sum(patients) as costperpatient
from
(select county,sum(cost) as totalcost, avg(numpatients) as patients
  from prescriptions,patientcounts,practices
  where prescriptions.practice=patientcounts.code 
  and   prescriptions.practice=practices.code
  group by county,practice) as byprac
  group by county
  having patients > 100000
  order by costperpatient desc;
""",
"""
select bnfcode,max(name),sum(nitems) as items 
from prescriptions
group by bnfcode
order by items desc
limit 10;
""",
"""
select bnfcode,max(name),sum(cost) as cost 
from prescriptions
group by bnfcode
order by items desc
limit 10;
""",
"""
 select prescriptions.bnfcode,max(prescriptions.name),prescriptions.practice,max(practices.name),avg(nitems),
avg(patientcounts.numpatients),avg(aveperperson),avg((nitems/patientcounts.numpatients)/aveperperson) as ratio
from (select bnfcode, avg(nitems/numpatients) as aveperperson
  from prescriptions,patientcounts
  where prescriptions.practice=patientcounts.code 
  group by  bnfcode 
  ) as avgs 
left join prescriptions on avgs.bnfcode = prescriptions.bnfcode
left join patientcounts on prescriptions.practice=patientcounts.code
left join practices on practices.code=prescriptions.practice
where patientcounts.numpatients > 500
and aveperperson>0
and prescriptions.practice not in ("Y01924")
group by prescriptions.bnfcode,prescriptions.practice
order by ratio desc;
"""

]

con=connect_to_db()
if con == None:
	exit(1)


print "Database version : %s " % con.admin.command({"serverStatus":1})['version']


results = []
for test in tests:
	result = { 'query': test,'times':[]}
	print(test)
	for r in range(0,3):
		start = time.time()
		rval = run_query('nhs','prescriptions',test)
		end = time.time()
		pprint(rval)
		print("Took: " + str(end - start))
		result["times"].append(end-start)
	results.append(result)
	with open("mongodb.json", "a") as outfile:
		json.dump(results, outfile)
