import requests
import json
import time
import textwrap

def get_analysis(api_token):

    analysis = requests.get(
        'https://kr.rescale.com/api/v3/developer-analyses/',
        headers={'Authorization': 'Token ' + api_token})

    return json.loads(analysis.text)

def get_analysis_version(api_token,active_id):

    version = requests.get(
        'https://kr.rescale.com/api/v3/developer-analyses/'+active_id+'/versions/',
        headers={'Authorization': 'Token ' + api_token})

    return json.loads(version.text)

def put_environment_variables(api_token,version_id):

    environment = requests.get(
        'https://kr.rescale.com/api/v3/developer-analysis-versions/'+version_id+'/environment-variables/',
        headers={'Authorization': 'Token ' + api_token})

    print(environment.text)

    environment = requests.put(
        'https://kr.rescale.com/api/v3/developer-analysis-versions/'+version_id+'/environment-variables/',
        json = [{'name':'ACTIVATE_USER_ENV','value': '";source ${PROGRAM_PATH}/baram.sh"','sortGroup':1 }],
        headers={'Authorization': 'Token ' + api_token})

    return 

if __name__ == "__main__":

    #Paste your API token here
    api_token = '' # API

    analysis_data = get_analysis(api_token)
    active_id = ''
    for i in range(analysis_data['count']) :
        print(analysis_data['results'][i]['id'], analysis_data['results'][i]['isActive'], analysis_data['results'][i]['name'])
        if (analysis_data['results'][i]['isActive'] == True) :
            active_id = analysis_data['results'][i]['id']

    version_data = get_analysis_version(api_token, active_id)
    print('Before setup Environment-variables', version_data)

    version_id = version_data['results'][0]['id']
    print('Version ID : ', version_id)

    put_environment_variables(api_token, version_id)
