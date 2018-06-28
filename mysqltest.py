#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import time
import json

def connect_to_db():
	try:
		con = mdb.connect("localhost", "root", "password", "nhs")
	except mdb.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		return None
	return con

def run_query(sql):
	cur = con.cursor()
	cur.execute(sql)
	rows = cur.fetchall()
	return rows

tests = [ 
"""select sum(cost) from prescriptions;""",
"""select sum(cost) from prescriptions group by period;""",
"""select practice,sum(cost) as totalspend from prescriptions 
 group by practice
  order by totalspend desc 
  limit 10;""",
"""select practice,sum(cost/numpatients) as totalspend,avg(numpatients)
 from prescriptions,patientcounts 
 where prescriptions.practice=patientcounts.code
   group by practice 
   order by totalspend 
   desc limit 10;""",
"""select county,sum(totalcost) as spend,sum(patients) as patients,sum(totalcost)/sum(patients) as costperpatient
from
(select county,sum(cost) as totalcost, avg(numpatients) as patients
  from prescriptions,patientcounts,practices
  where prescriptions.practice=patientcounts.code 
  and   prescriptions.practice=practices.code
  group by county,practice) as byprac
  group by county
  having patients > 100000
  order by costperpatient desc limit 20;
""",
"""
select bnfcode,max(name),sum(nitems) as items 
from prescriptions
group by bnfcode
order by items desc
limit 10;
""",
"""
select bnfcode,max(name),sum(cost) as totalcost 
from prescriptions
group by bnfcode
order by totalcost desc
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

ver = run_query("select version()")
print "Database version : %s " % ver   

results = []

for test in tests:
	result = { 'query': test,'times':[]}
	print(test)
	for r in range(0,3):
		start = time.time()
		run_query(test)
		end = time.time()
		print("Took: " + str(end - start))
		result["times"].append(end-start)
	results.append(result)
	with open("mysql.json", "a") as outfile:
		json.dump(results, outfile)

if con:    
 	con.close()