import requests
import json
import sys
import csv

with open('test.csv','r') as csv_file:
    _csv=csv.reader(csv_file)
    next(_csv)
# https://careerkarma.com/blog/python-valueerror-io-operation-on-closed-file/
    for line in _csv:
        _email=line[1]
        print(_email)

        url="https://{{url}}/api/v1/users/{}".format(line[1])
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'SSWS '+sys.argv[1] 
        }
        response = requests.request("GET", url, headers=headers)
        _object=response.json()
        _id=_object.get('id')
        #print(_id)
        if url != None:
            _url="{{url}}/api/v1/groups/00g6a80xcrf9Pr42u4x7/users/{}".format(_id)
            headers = {
                'Authorization': 'SSWS '+sys.argv[1]
            }
            _response=requests.request("PUT", _url, headers=headers)
            #print(_response)
            print(_response.status_code)
            print(_response.text)
        else:
            print("FAILED")