import requests
import csv
from datetime import datetime
import sys
import time

session = requests.session()
payload = {}
headers = {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': 'SSWS '+ sys.argv[1]
          }

user_store = []
application_store = []

with open('{{file_path.csv}}', 'r') as the_file:
    report = csv.reader(the_file)
    next(report)

    for row in report:
        uid = row[0]
        url = f"https://{{url}}/api/v1/apps?filter=user.id+eq+\"{uid}\""
        
        response = session.get(url, headers=headers, data=payload)
        user_apps = response.json()

        limit = int(response.headers['x-rate-limit-limit'])
        remaining = int(response.headers['x-rate-limit-remaining'])
        reset = datetime.utcfromtimestamp(int(response.headers['x-rate-limit-reset']))

        print("totol active apps counted " + str(len(application_store)) + " from last user")
        application_store.clear()
        print("application store is expected to be blank"+ str(application_store))

        #print("count of users app assignment : "+ str(len(user_apps)))
        #print(row[1])
        #print(response)
        #print(response.headers)
        print('x-rate-limit-limit : '+ str(limit))
        print('x-rate-limit-remaining : '+ str(remaining))
        print("x-rate-limit-reset : "+ str(reset))
        #print(row[0])
        
    
        limit_remaining = 5
        now = datetime.utcnow()
        if remaining < limit_remaining:
            [print("sleeping....")]
            while reset > now: 
                time.sleep(2)
                now = datetime.utcnow() 
                print(now)

        for app in user_apps:
            if app['status'] == 'ACTIVE':
                application_store.append(app)

        print(str(len(application_store)) + " of the " + str(len(user_apps)) + " apps assigned to user is active")
        
        if len(application_store) >= 1:
            user_store.append(row[0])
            print(str(len(user_store)) + " total authorized users appended to list")

    print(user_store)


    with open('users.csv','w', newline='') as csvfile:
        headers=['number', 'userid']
        csvwriter = csv.DictWriter(csvfile, fieldnames=headers)
        
        csvwriter.writeheader()
    
        for user in userlist:
            usercount += 1
            csvwriter.writerow({'number':usercount,'userid':user})