from generating_token  import *  
from generating_token import get_token
#####################  BD search element ###################### 

'''
GET /api/bkd/a_search/{repository}/{model}/{token}, Advanced search for the breakdown element

This method is used to look for breakdown elements and obtain information about it. Based on the query parameters, the output of this function offers information on the attributes of the required breakdown element.

The nodeID parameter defines the precise route within the tree to find the needed Break down element. Otherwise, the response contains all Breakdown elements that satisfy the query criteria.
'''

def bd_advanced_search(model,repository,search_params,token):

    break_down_search_url = PLM_URL + "/api/bkd/a_search/" + repository + "/" + model + "/" + token

    print("\nPerforming request: " + break_down_search_url)

    try:
        response = requests.get(break_down_search_url,params=search_params,timeout=2.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        print('Request failed {}\nError Message:  {}'.format(e, response.text))
        return None

    

search_params={
                    "createAfter":'',  # Search for the breakdown element created after the specified date
                    "createBefore":'', # Search for the breakdown element created before the specified date
                    "createUser":'',   # Search value for the breakdown element creator person
                    "descr":'',        # Search pattern for the breakdown element description
                    "editAfter":'',    # Search for the breakdown element edited after the specified date
                    "editBefore":'',   # Search for the breakdown element edited before the specified date
                    "editUser":'',     # Search value for the breakdown element editor person
                    "limit":'',        # Limit for the number of search result 
                    "nodeID":'',       # Root element’s instance ID of the branch to search within
                    "nodeVer":'',      # Version number of the element to search within
                    "pPhase":'',       # Project phase to search within
                    "pattern":"SENSORS",    # Search pattern for the breakdown element name
                    "propName":[],          # List of the breakdown element property names to search for
                    "propVal":[],           # List of the breakdown element property values to search for
                    "type":''}              # Search pattern for the breakdown element type (urn:rdl:epm-std:Unit)    


token = get_token(getTokenData)
if token: 
    search_result=bd_advanced_search(model,repository,search_params,token)
    if search_result:
        pp.pprint(search_result)   
                                 