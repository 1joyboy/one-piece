import csv, os, requests

opal_secret = os.environ['opal'] 
okta_secret = os.environ['TF_VAR_api_token_prod'] 
okta_url = '' #your_org_url
opal_url = 'https://api.opal.dev/v1' 

okta_prod = '1dcd991a-fa20-4182-b96f-abd1308fcadc' #app_source_id

def list_owners():
    headers = {
    'Authorization': f'Bearer {opal_secret}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
    }
    session = requests.session()
    session.headers.update(headers)
    response = session.get(f'{opal_url}/owners?page_size=1000')
    return response

def import_group(groupName, groupId):
    print('runing import_group function..')
    headers = {
    'Authorization': f'Bearer {opal_secret}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
    }
    session = requests.session()
    session.headers.update(headers)
    payload = {
        "group_type": "OKTA_GROUP",
        "remote_info": { 
            "okta_group": { 
                "group_id": f"{groupId}" 
            } 
        },
        "app_id": f"{okta_prod}",
        "name": f"{groupName}"
    }
    response = session.post(f'{opal_url}/groups', json=payload)
    # print(response.status_code)
    return response

def patch_reviewers(opalGroupId, ownersId):
    print('runing patch_reviewers function..')
    headers = {
        'Authorization': f'Bearer {opal_secret}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    session = requests.session()
    session.headers.update(headers)
    payload = { "stages": [ {
        "require_manager_approval": False,
        "operator": "AND",
        "owner_ids": [f"{ownersId}"]
        } ] 
    }
    response = session.put(f'{opal_url}/groups/{opalGroupId}/reviewer-stages', json = payload)
    print(response.status_code)
    return response

def put_owners(ownersList,ownerId):
    print('running put_owners function..')
    headers = {
        'Authorization': f'Bearer {opal_secret}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    session = requests.session()
    session.headers.update(headers)
    payload = {
        "user_ids": ownersList
    }
    response = session.put(f'{opal_url}/owners/{ownerId}/users', json = payload)
    return response    

def create_owners(ownerList,oktaGroupName):
    print('running create_owners funtion..')
    headers = {
        'Authorization': f'Bearer {opal_secret}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    session = requests.session()
    session.headers.update(headers)
    payload = {
        "name": f"opal.rev.{oktaGroupName}",
        "user_ids": ownerList
    }
    response = session.post(f'{opal_url}/owners', json = payload)
    return response

def get_opalUser(userEmail):
    headers = {
        'Authorization': f'Bearer {opal_secret}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    session = requests.session()
    session.headers.update(headers)
    response = session.get(f'{opal_url}/user?email={userEmail}')
    return response.json()['user_id']

def get_oktaGroupId(oktaGroupName):
    headers = {
        'Authorization': f'SSWS {okta_secret}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    session = requests.session()
    session.headers.update(headers)
    response = session.get(f'{okta_url}/api/v1/groups?q={oktaGroupName}')
    return response.json()[0]['id']


owners = {}
allOwners = list_owners().json()['results']
for owner in allOwners:
        for key, value in owner.items():
            if key == 'name':
                name = value
            if key == "owner_id":
                owner_id = value
        owners[name] = owner_id
        # print(len(owners))
# for key, value in owners.items():
#         print(f'{key}: {value}')
        # print(f'{key} : {value}')
# exit()


with open('netsuite_rbac.csv','r') as input_file: #your CSV file
    dataset = csv.DictReader(input_file)
    for item in dataset:
        ownersList = []
        approver = item["Approvers"]
        oktaGroupName = item["Production group names in Opal"]
        oktaGroupId = get_oktaGroupId(oktaGroupName)
        # print(f'{oktaGroupName}: {oktaGroupId}')
        
        if approver != "": 
            userEmailList = approver.split(",")
            for userEmail in userEmailList: 
                opalUserId = get_opalUser(userEmail)
                ownersList.append(opalUserId)        
            created_owners = create_owners(ownersList,oktaGroupName)
            if created_owners.status_code == 400:
                print(f'opal.rev.{oktaGroupName} already exist')
                ownerId = owners[f'opal.rev.{oktaGroupName}']
                updatedOwners = put_owners(ownersList,ownerId)
                print(f'put_owners: {updatedOwners.status_code}')
            else:
                print(f'created_owners: {created_owners.status_code}')     
                ownerId = created_owners.json()['owner_id']
            importedGroup = import_group(oktaGroupName,oktaGroupId)
            print(importedGroup.status_code)
            opalGroupId = importedGroup.json()['group_id']
            patchedReviewers = patch_reviewers(opalGroupId,ownerId)
        break
