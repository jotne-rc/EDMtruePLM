from generating_token  import *  
from generating_token import get_token
######################## q_search method ######################


def bd_quick_search(model,search_type,search_params,token,repository="TruePLMprojectsRep"):

    if search_type == "q_search":
        break_down_search_url = PLM_URL + "/api/bkd/q_search/" + repository + "/" + model + "/" + token
    elif search_type == "q_search_ext":
        break_down_search_url = PLM_URL + "/api/bkd/q_search_ext/" + repository + "/" + model + "/" + token
    else:
        print('Invalid search type')
        return None
    print("\nPerforming request: " + break_down_search_url)
    try:
        response = requests.get(break_down_search_url,params=search_params,timeout=2.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        print('Request failed {}\nError Message:  {}'.format(e, response.text))
        return None
    
model= 'Palfinger_Crane_Assembly'           # Project name 

search_params={"case_sens":"false",         # Use case sensitive search or not
                    "domains":"ID",         # CSV list of subjects for search, can include ID, DESCRIPTION, CLASS, PROPERY
                    "folder_only":"true",   # Return only direct children of parent folder
                    "node":"",              # Breakdown element instance id - root of interesting branch
                    "page":"",              # Start page of output
                    "page_size":"",         # Page size of output
                    "pattern":"SENSORS",    # Search string pattern (for LIKE operations in EXPRESS)
                    "props":""}             # CSV list of property names where to apply search pattern (when PROPERTY is listed)    
    

token = get_token(getTokenData)
if token: 
    print(bd_quick_search(model,'q_search',search_params,token))