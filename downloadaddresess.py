#!/usr/bin/python
import urllib
import os
from pprint import pprint

months = ['January','February','March','April','May','June','July',
          'August','September','October','November','December']

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

for year in range(2017,2012,-1):
	for month in range(12,0,-1):
		url = "http://datagov.ic.nhs.uk/presentation/{0:4d}_{1:02d}_{2:s}/T{0:4d}{1:02d}ADDR+BNFT.CSV".format(year,month,months[month-1])
		print("Downloading " + url)
		fname = "Practises_{:4d}{:02d}.csv".format(year,month)
		r = fetch_url(url,fname)
		if r == False:
			url = "http://datagov.ic.nhs.uk/presentation/{0:4d}_{1:02d}_{2:s}/T{0:4d}{1:02d}ADDR+BNFT.CSV".format(year,month,months[month-1].lower())
			print("Downloading alternative " + url)
			r = fetch_url(url,fname)
			if r == False:
				url = "http://datagov.ic.nhs.uk/presentation/{0:4d}_{1:02d}_{2:s}/T{0:4d}{1:02d}ADDR+BNFT.csv".format(year,month,months[month-1])
				print("Downloading alternative " + url)
				r = fetch_url(url,fname)
				if r == False:
					print("Not Available")
