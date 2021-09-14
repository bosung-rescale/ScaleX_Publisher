'''
ScaleX Publisher Tile
Author: Eric R Muir
Company: Rescale
Date: 11/6/2020

Modified by Bosung Lee for NEXTfoam BARAM
Date: 06/07/2021
'''

import requests
import json
import time
import textwrap

def create_persistent_cluster(api_token):

    cluster = requests.post(
        'https://kr.rescale.com/api/v3/clusters/',
        json = { 
            'hardware': {
                'coresPerSlot': 2, #Cores
                'coreType': { 'code': 'zinc' }, #Cluster should be used Zinc, Onyx which has not NVME disk
                'walltime': 2, #Walltime
            },
            'installedAnalyses': [ #Included installations
                {
                    'analysis': {
                        'code': 'user_included',
                        'version': 'multinode'
                    }
                }
            ]
            },
        headers={'Authorization': 'Token ' + api_token})

    return json.loads(cluster.text)

def start_persistent_cluster(cluster_id, api_token):

    start = requests.post(
        'https://kr.rescale.com/api/v3/clusters/' + cluster_id + '/start/',
        headers={'Authorization': 'Token ' + api_token})

    return 

def shutdown_persistent_cluster(cluster_id, api_token):

    shutdown = requests.post(
        'https://kr.rescale.com/api/v3/clusters/' + cluster_id + '/shutdown/',
        headers={'Authorization': 'Token ' + api_token})

    return 

def wait_cluster_start(cluster_id, api_token):

    #What for cluster status to become 'Started'
    while json.loads(requests.get(
        'https://kr.rescale.com/api/v3/clusters/' + cluster_id + '/statuses/',
        headers={'Authorization': 'Token ' + api_token}).text)['results'][0]['status'] != 'Started':

        time.sleep(5)

        print(json.loads(requests.get('https://kr.rescale.com/api/v3/clusters/' + cluster_id + '/statuses/',
              headers={'Authorization': 'Token ' + api_token}).text)['results'][0]['status'])

    return json.loads(requests.get(
            'https://kr.rescale.com/api/v3/clusters/' + cluster_id + '/statuses/',
            headers={'Authorization': 'Token ' + api_token}).text)

def wait_cluster_stop(cluster_id, api_token):

    #What for cluster status to become 'Stopped'
    while json.loads(requests.get(
        'https://kr.rescale.com/api/v3/clusters/' + cluster_id + '/statuses/',
        headers={'Authorization': 'Token ' + api_token}).text)['results'][0]['status'] != 'Stopped':

        time.sleep(5)

        print(json.loads(requests.get('https://kr.rescale.com/api/v3/clusters/' + cluster_id + '/statuses/',
              headers={'Authorization': 'Token ' + api_token}).text)['results'][0]['status'])

    return json.loads(requests.get(
            'https://kr.rescale.com/api/v3/clusters/' + cluster_id + '/statuses/',
            headers={'Authorization': 'Token ' + api_token}).text)

def run_installation(cluster_id, mount_point, api_token):

    installation = requests.post(
        'https://kr.rescale.com/api/v3/installations/',
        json = { 
            'name': 'IPhreeqcPy',
            'cluster_id': cluster_id,
            'mountPoint': mount_point,
            'volumeSize': 1, #Not sure the units, suspect GB
            'inputFiles': [
                {
                    'id': 'noCbdg', #Input file id already uploaded to user Rescale KR account
                    'name': 'iphreeqcpy_rescale.tar.gz' #Input file name already uploaded to user Rescale account
                }
            ],
            'command': textwrap.dedent(f'''\
                cd {mount_point}
                sudo tar zxf $HOME/work/iphreeqcpy_rescale.tar.gz
                ''') #Install commands
            },

        headers={'Authorization': 'Token ' + api_token})

    return json.loads(installation.text)

def wait_installation_finish(installation_id, api_token):

    #Wait for installation status to become 'COMPLETED'
    while json.loads(requests.get(
        'https://kr.rescale.com/api/v3/installations/' + installation_id + '/statuses/',
        headers={'Authorization': 'Token ' + api_token}).text)['results'][0]['status'] != 'COMPLETED':

        time.sleep(5)
        print(json.loads(requests.get('https://kr.rescale.com/api/v3/installations/' + installation_id + '/statuses/',
            headers={'Authorization': 'Token ' + api_token}).text)['results'][0]['status'])

    return json.loads(requests.get(
            'https://kr.rescale.com/api/v3/installations/' + installation_id + '/statuses/',
            headers={'Authorization': 'Token ' + api_token}).text)

def create_package(installation_id, api_token):

    package = requests.post(
        'https://kr.rescale.com/api/v3/packages/',
        json = { 
            'installationId': installation_id,
            'tags': {
                'Name': 'IPhreeqcPy', #Package Name
                'Industries': 'Geochemical' #Package industry
                }
            },
        headers={'Authorization': 'Token ' + api_token})

    return json.loads(package.text)

def wait_package_finish(package_id, api_token):

    #Wait for package installation status to become 'COMPLETED'
    while json.loads(requests.get(
        'https://kr.rescale.com/api/v3/packages/' + package_id + '/statuses/',
        headers={'Authorization': 'Token ' + api_token}).text)['results'][0]['status'] != 'COMPLETED':
        time.sleep(5)
        print(json.loads(requests.get('https://kr.rescale.com/api/v3/packages/'+package_id+'/statuses/',
            headers={'Authorization': 'Token ' + api_token}).text)['results'][0]['status'])

    return json.loads(requests.get(
            'https://kr.rescale.com/api/v3/packages/' + package_id + '/statuses/',
            headers={'Authorization': 'Token ' + api_token}).text)

def create_analysis(api_token):

    analysis = requests.post(
        'https://kr.rescale.com/api/v3/developer-analyses/',
        json = { 
            'code': 'iphreeqcpy-1', #Analysis code (internal)
            'name': 'IPhreeqcPy' #Analysis name
            },
        headers={'Authorization': 'Token ' + api_token})

    return json.loads(analysis.text)

def create_analysis_version(analysis_id, mount_point, api_token):

    version = requests.post(
        'https://kr.rescale.com/api/v3/developer-analyses/' + analysis_id + '/versions/',
        json = { 
            'mountBase': mount_point,
            'version': '1.0.2',
            'versionCode': '1.0.2',
            'stdCommand': textwrap.dedent(f'''\
                # 
                '''), #Template command
            'mpiCommand': textwrap.dedent(f'''\
                # 
                '''), #To enable multinodes, mpiCommand field should not be empty
        },
        headers={'Authorization': 'Token ' + api_token})

    return json.loads(version.text)

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

#def put_environment_variables(api_token,version_id):
#
#    environment = requests.get(
#        'https://kr.rescale.com/api/v3/developer-analysis-versions/'+version_id+'/environment-variables/',
#        headers={'Authorization': 'Token ' + api_token})
#
#    print(environment.text)
#
#    environment = requests.put(
#        'https://kr.rescale.com/api/v3/developer-analysis-versions/'+version_id+'/environment-variables/',
#        json = [{'name':'ACTIVATE_USER_ENV','value': '";source ${PROGRAM_PATH}/baram.sh"','sortGroup':1 }],
#        headers={'Authorization': 'Token ' + api_token})
#
#    return 

if __name__ == "__main__":

    #Paste your API token here
    api_token = ''  # KR bosung@rescale.com API

    #Select program mount point
    mount_point = '/program/iphreeqcpy'

    #Create persistent cluster - you change change coretype, number of cores, walltime, and installed analyses
    cluster_data = create_persistent_cluster(api_token)
    print('create persistent cluster')

    #Start persistent cluster
    cluster_start = start_persistent_cluster(cluster_data['id'], api_token)
    print('start persistent cluster')

    #Wait for cluster to start
    cluster_status = wait_cluster_start(cluster_data['id'], api_token)
    print('persistent cluster started')

    #Run installation - Install commands go in 'commands' section.  You also can include files that are required
    installation_data = run_installation(cluster_data['id'], mount_point, api_token)
    print('installation started')

    #Wait for installation to finish
    print('Installation ID : ', installation_data['id'])
    installation_status = wait_installation_finish(installation_data['id'], api_token)
    print('Waiting for 180 seconds for sync installation')
    time.sleep(180) # Sufficient time should be required to installation finish
    print('installation finished')

    #Create package of installation - You can specify name and industry here.  Maybe also thumbnail?
    package_data = create_package(installation_data['id'], api_token)
    print('create package started')

    #Wait for package to finish
    print('Package ID : ', package_data['id'])
    package_status = wait_package_finish(package_data['id'], api_token)
    print('package created')

    #Create analysis
    analysis_data = create_analysis(api_token)
    print('create analysis')
    print(analysis_data)

    #Create analysis version - this is where you specify the template command
    version_data = create_analysis_version(analysis_data['id'], mount_point, api_token)
    print(version_data)
    print('create analysis version')
    
    #Stop Cluster
    cluster_shutdown = shutdown_persistent_cluster(cluster_data['id'], api_token)
    print('shutdown persistent cluster')

    #Wait for cluster to stop
    cluster_status = wait_cluster_stop(cluster_data['id'], api_token)
    print('persistent cluster stopped')
