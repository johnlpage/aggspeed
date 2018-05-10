#!/usr/bin/python
import urllib
import os.path
from pprint import pprint

def fetch_url(url,fname):
	if os.path.isfile(fname) == False:
			try:
				rval = urllib.urlretrieve (url, fname )
			except Exception as a:
				pprint(a)
				return False
	statinfo=os.stat(fname)
	if statinfo.st_size < 2000:
		print("File is only "+str(statinfo.st_size)+" bytes")
		#Error so remove it
		os.remove(fname)
		return False
	return True
#http://digital.nhs.uk/media/33804/Patients-Registered-at-a-GP-Practice-November-2017-Totals-GP-practice-all-persons-/default/gp-reg-pat-prac-all-nov-17

months = ['January','February','March','April','May','June','July',
          'August','September','October','November','December']
short=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']

for year in range(2017,2012,-1):
	for month in range(12,0,-1):
		url = "http://digital.nhs.uk/media/33804/Patients-Registered-at-a-GP-Practice-{0:s}-{1:4d}-Totals-GP-practice-all-persons-/default/gp-reg-pat-prac-all-{2:s}-{3:2d}".format(months[month-1],year,short[month-1],year-2000)
		print(url)
		fname = "Count_{:4d}{:02d}.csv".format(year,month)
		if os.path.isfile(fname) == False:
			if fetch_url(url,fname) == False:
				print("Not Available")