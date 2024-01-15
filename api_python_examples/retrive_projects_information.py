from generating_token  import *  
from generating_token import get_token
'''
This method is used to obtain an overview of projects created by the PLM user. 
This call returns information such as project name, project guid, project creation, and end dates.
'''
##################### project information ###################### 
def get_current_projects_info(token):
    
    url_get_proj_info=PLM_URL+'/'+'api/adm_user/all_user_proj'+'/'+token   # URL for getting the projects info
    print("\nPerforming request: " +  url_get_proj_info)

    try:
        response = requests.get(url_get_proj_info, timeout=2.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        print('Request failed {}\nError Message:  {}'.format(e, response.text))
        return None

token = get_token(getTokenData)
if token:
    projects_information = get_current_projects_info(token)
    if projects_information:
        for project_info in projects_information:
            project_name = project_info['in_project']['name']
            project_guid = project_info['in_project']['guid']
            print('\nProject name: {}, guid: {}'.format(project_name, project_guid))