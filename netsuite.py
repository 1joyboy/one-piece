import csv, os, requests

secret = os.environ['TF_VAR_api_token_prod'] #update variable as needed
url = '' #update org value as needed
headers = {
    'Authorization': 'SSWS '+ secret,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}
session = requests.session()
session.headers.update(headers)

Company = "" #update as needed.
Netsuite_Production_SCIM = '' #update application id as needed
appId = Netsuite_Production_SCIM
count = 1

def get_user(username):
    r = (session.get(f'{url}/api/v1/users/{username}'))
    # print (r)
    return r.json()

def search_user(email):
    r = (session.get(f'{url}/api/v1/users/?search=profile.migratedUserId eq "{email}"'))
    return r.json()

def get_groupId(groupName):
    return session.get(f'{url}/api/v1/groups?q={groupName}').json()[0]['id']

def del_groupMembership(userId, groupId):
    return session.delete(f'{url}/api/v1/groups/{groupId}/users/{userId}')

def add_groupMembership(userId, groupId):
    return session.put(f'{url}/api/v1/groups/{groupId}/users/{userId}')

def create_group(groupName):
    payload = {
        "profile": {
            "name": f"{groupName}"
            }
        }
    return session.post(f'{url}/api/v1/groups', json=payload).status_code

def add_group_to_application(applicationId, groupId, extRole):

    payload = {
        "id":groupId,
        "profile":{
            "department":{
                "name":"-",
                "externalId":"EMPTY_DEPARTMENT"
            },
            "class":{
            },
            "location":{
                "name":"-",
                "externalId":"EMPTY_OBJECT"
            },
            "subsidiary":Company,
            "giveAccess":True,
            "roles": extRole
        }
    }
    return session.put(f'{url}/api/v1/apps/{applicationId}/groups/{groupId}', json = payload).status_code


with open('netsuite_rbac.csv','r') as input_file:
    data = csv.DictReader(input_file)
    # next(groupNames_list)
    for row in data:
        count +=1
        # print(row)
        role = (row['profile role name'])
        # print (role)
        mappings = (row['mapping'])
        # print (mappings)
        groupName = (row['Production group names in Opal'])
        if create_group(groupName) == 400:
            print (f'{groupName} already exist')
        groupId = get_groupId(groupName)
        print(groupId)
        # opalReviewer = (row['Approvers'])
        # print (opalReviewer)
        if not mappings: # if mappings == "":
            # print (role)
            oneRole = role.split(",0")
            # print (oneRole)
            print(add_group_to_application(appId, groupId, oneRole))
        else:
            # print(mappings)
            manyRoles = mappings.split(", ")
            # print(manyRoles) # is a list
            print(add_group_to_application(appId, groupId, manyRoles))
        # if count == 5:
            # break
        # break
        # userEmail = row['Databricks Email']
        # print(userEmail)
        # user = search_user(userEmail) 
        # print(user)
        