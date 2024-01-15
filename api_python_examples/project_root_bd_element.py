from generating_token  import *  
from generating_token import get_token

'''
This method requires two input parameters repository and model names and returns the root breakdown element information in the project.

repository - "TruePLMprojectsRep” is a fixed value for all PLM projects and declared in plm_token_generation file 

'''





#####################  root_bd element infomration ######################
def get_root_breakdown_element(model,token,repository='TruePLMprojectsRep'):

    url_get_root_bd_info = PLM_URL + "/api/bkd/" + repository + "/" + model + "/" + token
    print("\nPerforming request: " + url_get_root_bd_info)
    try:
        response= requests.get(url_get_root_bd_info, timeout=2.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        print('Request failed {}\nError Message:  {}'.format(e, response.text))
        return None

# Input parameters

model = "Palfinger_Crane_Assembly"

token = get_token(getTokenData)

if token:
    root_bd = get_root_breakdown_element(model,token)
    print(root_bd)
    if root_bd:
        print('The root bd element of the project: {}, and instance_id is: {}'.format(
            root_bd['root_bkdn_elem']['name'],
            root_bd['root_bkdn_elem']['instance_id']
        ))