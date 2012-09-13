import csv
import urllib2
import json
import re

def findID(str):
	# extracts the status ID from teh following string example:
	# "http://twitter.com/IBPTravels/statuses/75907873892339712"
	matchObj = re.match('(.)+statuses\/(\d+)', str, re.I)
	return matchObj.group(2)

def findURL(str):
	# input string is a link in the following format: <a href="X" rel="X">link text </a>
	# this regex extracts the link text, if input is a link, otherwise returns the same string 
	# (sometimes twitter source is just 'web')
	
	matchObj = re.match('.+>(.+)<\/a>', str, re.I)
	
	if matchObj:
	   return matchObj.group(1)
	else:
	   #print "No match"
	   return str


reader = csv.reader(open('in.csv', 'rU'), delimiter=',', quotechar='"')
writer = csv.writer(open('out.csv', 'wb'), delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)

rowcount = 0

for row in reader:
  # write the header line first, no transformations or lookups needed
  if rowcount ==  0:  
       writer.writerow(row)
  else: 
   
	  if rowcount > 0:
		#print row[1]
		if row[2] == "TWITTER":
		
			id = findID(row[1])
			
			url = 'https://api.twitter.com/1/statuses/show.json?id=' + id
			#print url
			
			# insert try here because sometimes repsponse codes are 403 (forbidden) or 404 (not found)
			try:
				req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
				data = urllib2.urlopen(url)
				source = data.read()
				
				obj = json.loads(source) 
				#print obj["source"]
				
				cleanstr  = findURL(obj["source"]).replace(u'\xa0', u' ')
				cleanstr = cleanstr.replace(u'\xae', u' ')
				
				row[3] = cleanstr
				#print row
			
			except urllib2.HTTPError, e:
				print e.fp.read()
				row[3] = 'not authorized'
		
	  else:
	  	row[3] = 'n/a'
		
	  writer.writerow(row)
  rowcount += 1
     

