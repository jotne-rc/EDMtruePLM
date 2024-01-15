from generating_token  import *  
from generating_token import get_token


##################### Create new project ###################### 

# This method is used to create a new project by importing a STEP File . 


def create_new_project(data_param, file, token):
    create_new_proj = PLM_URL + "/api/adm_user/" + token

    print("\nPerforming request: " + create_new_proj)

    try:
        response = requests.post(create_new_proj, files=file, data=data_param, timeout=30.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        print('Request failed {}\nError Message:  {}'.format(e, response.text))
        return None


#Input parameters for the API method 

data_param={}

file = {'file': open("Palfinger_Crane_Assembly.stp",'r')} #  declaring the required step file path (.stp, .txt, .dex)

data_param={"descr":"Crane assembly",                     # description of the creating project
            "folder":"",                                  # Project folder for the new project placement
            "is_bkd_tmpl":"false",                        # Create new project as a breakdown template(true) or not(false)
            'is_tmpl':"false",                            # Create new project as a project template(true) or not(false)
            'name':"Palfinger_Crane_Assembly",            # User required Name of the Project
            'nodeType':"",                                # node type
            'src':"pdm",                                  # Type of the data file (pdm for STEP files)
            'tmpl':""}                                    # Project template model name for the new project initialization


token = get_token(getTokenData)
if token:
    new_project_information = create_new_project(data_param, file, token)
    if new_project_information:
        pp.pprint(new_project_information)