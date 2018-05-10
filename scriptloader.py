#!/bin/python
#Load in Data
#Data is sorted by Practise so we can use that to make one record pre practise with all the data in
from pymongo import MongoClient
import os

client = MongoClient('localhost', 27017)
db = client.NHS
prescriptions = db.prescriptions
prescriptions.drop()

batch = []
batchsize = 100

def flush_batch():
	global batch
	prescriptions.insert_many(batch)
	batch=[]

def write_record(record):
	global batch
	if record.get('practice') == None:
		return
	batch.append(record)
	if len(batch) == batchsize:
		flush_batch()

postcodes = {}
def read_postcodes():
	print("Reading postcodes")
	with open("ukpostcodes.csv","r") as  infile:
		header = infile.readline()
		#print header
		for line in infile:

			parts = line.split(',')
			try:
				postcodes[parts[1]]=[float(parts[3].strip()),float(parts[2])]
			except Exception as e:
				pass

counts  = {}
def read_counts(year,month):
	print("Loading Count ",year,month)
	global counts
	counts={}
	fname = "Count_{:4d}{:02d}.csv".format(year,month)
	with open(fname,"r") as  infile:
		header = infile.readline()
		#print header
		for line in infile:
				#print line
				try:
					parts = line.split(",")
					record = { "type":parts[2].strip(),"patients":int(parts[9])}
					counts[parts[5]]=record
				except Exception as e:
					print(e)
					print("error parsing " + line)
	print("Done")


addresses = {}

def read_addresses(year,month):
	print("Loading Addresses ",year,month)
	global addresses
	addresses={}
	fname = "Practises_{:4d}{:02d}.csv".format(year,month)
	with open(fname,"r") as  infile:
		for line in infile:
				name = None
				try:
					when,praccode,name,add1,add2,town,county,postcode = line.split(",")
				except:
					try:
						when,praccode,name,add1,add2,town,county,postcode,dummy = line.split(",")	
					except Exception as e:
						print(e)
						print line
				if name != None:
					record = { "name ":name.strip(),"address1":add1.strip(),"address2":add2.strip(),
					"town":town.strip(),"county":county.strip(),"postcode":postcode.strip(),"location":postcodes.get(postcode.strip())}
					addresses[praccode]=record
			
	print("Done")

read_postcodes()

for year in range(2017,2011,-1):
	
	for month in range(12,0,-1):
		
		if year == 2017 and month > 10:
			continue
		#Read in the Practise list for adresses etc
		read_addresses(year,month)
		read_counts(year,month)
		print "Loading " + str(month)+" "+str(year)
		fname = "Prescriptions_{:4d}{:02d}.csv".format(year,month)
		if os.path.isfile(fname+".done") == False:
			record = {}
			with open(fname,"r") as  infile:
				line = infile.readline()
				for line in infile:
					code1,code2,practice,bnfcode,name,items,nicost,cost,quantity,period,null = line.split(",")
					if record.get('practice') != practice:
						write_record(record)
						record = {}
						record = { 'detail':counts.get(practice,{}),'practice':practice,'address':addresses.get(practice,{}),'period':int(period),'prescriptions':[]}
					record['prescriptions'].append({'b':bnfcode,'nm':name.strip(),'itm':int(items),'qty':int(quantity),'nic':float(nicost),'cst':float(cost)})

			with open(fname+".done","w") as donefile:
				donefile.close()

					
