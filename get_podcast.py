import xmltodict, requests, re, os, urllib, os.path
from StringIO import StringIO
from urlparse import urlparse
from sys import argv

script, rss_feed = argv
storage_dir = 'podcasts'

###############
###FUNCTIONS###
###############

def get_xml(xml):
	r = requests.get(xml)
	xml_data = StringIO(r.content)
	parsed_xml_data = xmltodict.parse(xml_data.read(),xml_attribs=True)
	return parsed_xml_data

def download(url, fname):
	urllib.urlretrieve (url, fname)

##########
###CODE###
##########

#set working dir (script location)
working_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(working_dir)
#create dir for podcast downloads
if not os.path.exists(storage_dir):
	os.mkdir(storage_dir)
os.chdir(storage_dir) # switch to podcast dir

print 'Getting links....'
xml = get_xml(rss_feed) # go fetch rss feed

for entry in xml['rss']['channel']['item']:
	podcast_url = entry['enclosure']['@url']
	base = urlparse(podcast_url)[1]
	clean_path = urlparse(podcast_url)[2]
	path, fname = os.path.split(clean_path)
	if "http" not in base:
		podcast_url = 'http://'+str(base)+str(clean_path)
	else:
		podcast_url = str(base)+str(clean_path)
	if not os.path.isfile(fname):
		print 'Downloading: '+clean_path
		download(podcast_url, fname)

print 'All caught up.'