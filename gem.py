import requests
import json
import xml.etree.ElementTree as ET

BASE_URL = 'http://api.worldbank.org/'


def fetch_data(params=None,payload=None):
	url = BASE_URL + '/'.join(params) if params else BASE_URL
	# payload = {'format':'json'}
	r = requests.get(url,payload)
	data = None
	if r.status_code == 200:
		data = r.text
		if data:
			return data
	return None

def unpack_list_of_dicts_into_dict(dct,lst):
	for item in lst:
		dct[item['id']] = item['name']
	return dct

def fetch_indicators(params=None,payload=None,loop=True):
	params = ['sources','15','indicators']
	payload = {'format':'json','page':'1'}
	data = fetch_data(params,payload)
	fetched = {}
	if data:
		info = data[0]
		fetched = unpack_list_of_dicts_into_dict(fetched,data[1])
		if loop:
			curr = data[0]['page']
			total = data[0]['pages']
			while curr <= total:
				payload['page']=str(curr+1)
				curr +=1
				data = fetch_data(params,payload)
				if data:
					fetched = unpack_list_of_dicts_into_dict(fetched,data[1])
					

	return fetched.keys()


def fetch_by_indicator(params=None,indicator=None):
	if not indicator:
		return
	else:
		params = ['countries','all','indicators',str(indicator)]
		data = fetch_data(params)
		root = ET.fromstring(data.encode('utf-8'))
		return root

def parse_xml_returned(data):
	pass