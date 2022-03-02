import requests
import json
import sys
import csv




with open('test.csv','r') as csv_file:
    _csv=csv.reader(csv_file)
    next(_csv)

    for line in _csv:
        _email=line[1]
        _firstName=line[2]
        _lastName=line[3]

        _urlScope = "https://api.sendgrid.com/v3/teammates/{}".format(line[0])
        #payload={}
        headers = {
            'Authorization': 'Bearer '+sys.argv[1]
            }
        response = requests.request("GET", _urlScope, headers=headers) #, data=payload)

        _object=response.json()
        _scopes=_object.get('scopes')
        # _scope=json.dumps(_scopes)
        # print(_firstName)
        # print(_lastName)
        print(_email)
        # print(_scopes)
        # print(_scope)
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
        print("LOADING...")

        _urlSSO = "https://api.sendgrid.com/v3/sso/teammates"
        headers = {
            'Authorization': 'Bearer '+sys.argv[1]
            }
        payload=json.dumps({"first_name": _firstName,
                 "last_name": _lastName,
                 "email": _email,
                 "scopes": _scopes
                })
        # print(payload)
        response2 = requests.request("POST", _urlSSO, headers=headers, data=payload)
        print(response2.status_code)
        print(response2.text)
        print("NEXT")
        
        
