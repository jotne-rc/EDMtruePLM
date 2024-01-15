from generating_token  import *  
from generating_token import get_token
from breakdown_quick_search import bd_quick_search

'''
To find the necessary Breakdown element information, it is advised to use search functions. The alternate approach as 
demonstrated below, is to hardcode the instance id to the node variable. It is accessible through the GUI in the Figure. 
Instance id of the necessary breakdown element to delete, 

node="21478374906" 

'''

def delete_breakdown_element(model,repository,node,token):

    del_bd_elem_url=PLM_URL+"/api/bkd"+"/"+repository + "/" + model + "/" + node + "/"+token

    print("\nPerforming request: " + del_bd_elem_url)
    try:
        response = requests.delete(del_bd_elem_url,timeout=2.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        print('Request failed {}\nError Message:  {}'.format(e, response.text))
        return None   
    
# Input parameters  

model= 'Palfinger_Crane_Assembly'           # Project name 

repository="TruePLMprojectsRep"             # Project repo

# Modifiy the search paramaters to find required breakdown element node 
search_params={"case_sens":"false",         # Use case sensitive search or not
                    "domains":"ID",         # CSV list of subjects for search, can include ID, DESCRIPTION, CLASS, PROPERY
                    "folder_only":"true",   # Return only direct children of parent folder
                    "node":"",              # Breakdown element instance id - root of interesting branch
                    "page":"",              # Start page of output
                    "page_size":"",         # Page size of output
                    "pattern":"SENSORS 2",  # Search string pattern (for LIKE operations in EXPRESS)
                    "props":""}             # CSV list of property names where to apply search pattern (when PROPERTY is listed)    

token = get_token(getTokenData)
if token: 
    node=str(bd_quick_search(model,'q_search',search_params,token)[0]['bkdn_elem_info']['instance_id'])
    print('The required breakdown element Instance Id:',node)
    if node:
        delete_result=delete_breakdown_element(model,repository,node,token)
        if delete_result:
            pp.pprint(delete_result)   