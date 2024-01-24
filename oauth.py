import okta.client, okta.oauth, requests, csv

def main():
    client = okta.client.Client()
    # print(client)

    config = client.get_config()
    # print(config)

    params = {
        'grant_type': 'client_credentials',
        'scope': ' '.join(config['client']['scopes']),
        'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
        'client_assertion': okta.oauth.OAuth(client.get_request_executor(), config).get_JWT()
    }
    org_url = config['client']['orgUrl']
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(org_url + okta.oauth.OAuth.OAUTH_ENDPOINT, params=params, headers=headers)
    tokens = r.json()

    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + tokens['access_token']
    
    
    # print(f'userEmail,jobFamily,jobFamilyGroup,title,supervisoryOrg,organization,costCenter')
    # with open('dockersso.csv','r') as input_file:
    #    data = csv.DictReader(input_file)
    #    for row in data:
    #        userEmail = row["Email"]
    #     #    print(userEmail)
    #        r = s.get(org_url + '/api/v1/users/' + userEmail)
    #     #    print(r)
    #        user = r.json()
    #     #    print(user)
    #      #   status = r.json()['status']
    #     #    print(status)
    #        userId = r.json()['id']
    #        userType = r.json().get('profile').get('userType')
    #        jobFamily  = r.json().get('profile').get('jobFamily')
    #        jobFamilyGroup  = r.json().get('profile').get('jobFamilyGroup')
    #        title  = r.json().get('profile').get('title')
    #        supervisoryOrg  = r.json().get('profile').get('supervisoryOrg')
    #        organization = r.json().get('profile').get('organization')
    #        costCenter = r.json().get('profile').get('costCenter')
    #        print(f'{userEmail},{jobFamily},{jobFamilyGroup},{title},{supervisoryOrg},{organization},{costCenter}')
    #      #   employeeType = r.json().get('profile').get('employeeType')
    #     #    print(employeeType)
    #      #   print(f'{userEmail},{status},{userType},{employeeType}')


    '''
    list application starting with
    '''
    # print(org_url)
    # r = s.get(org_url+f'/api/v1/apps?q=genie&limit=50')
    # # print(r.json())
    # for i in r.json():
    #     print(i.get('label'))

    
    '''
    list group memberships
    '''
    # r = s.get(org_url+f'/api/v1/groups/{groupId}/users')
    # # print(r.json())
    # for i in r.json():
    #     print(i.get('profile').get('email'))
    #     # break


    '''
    removing user's group membership
    '''
    # groupId = '' #groupName
    # with open('users1.csv','r') as input_file:
    #     data = csv.DictReader(input_file)
    #     # next(groupNames_list)
    #     for row in data:
    #         user = row["emailAddress"]
    #         print(user)
    #         r = s.get(org_url + '/api/v1/users/' + user)
    #         user = r.json()
    #         # print(user['profile']['login'])
    #         userId = r.json()['id']
    #         # print(userId)
    #         r = s.delete(org_url + f'/api/v1/groups/{groupId}/users/{userId}')
    #         print(r)

    '''
    create new group
    '''
    # groups = [

    # ]
    
    # for groupName in groups:
    #     print(groupName)
    #     payload = {
    #       "profile": {
    #         "name": groupName
    #       }
    #     }
    #     r = s.post(org_url+'/api/v1/groups', json=payload)
    #     if r.status_code == 200:
    #         print(r ,r.text)
    
main()




