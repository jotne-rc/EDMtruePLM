from generating_token  import *  
from generating_token import get_token

#####################  Creating new BD element ###################### 
'''
This method is used in the project to create a new breakdown element.

Post /api/bkd/create/{repository}/{model}/{node}/{token} 

In this method user need to specify the path in form of node id such that the required new breakdown element will 
be created under this path.

Note:   For demonstration purposes, the node id (instance id) in these examples is assigned explicitly.
        Nevertheless, it is usually advised against using the node numbers directly by the user. 
        Instead, they must employ element search techniques to find the node id (which is the instance id of the element). 
        Use this as the input for the API requests thereafter.
'''

def create_new_bd_element(node,model,data_param,token,repository="TruePLMprojectsRep"):

    create_new_bd_ele_url=PLM_URL+"/api/bkd/create"+"/"+repository + "/" + model + "/" + node + "/"+token
    print("\nPerforming request: " + create_new_bd_ele_url)
    try:
        response = requests.post(create_new_bd_ele_url,params=data_param,timeout=2.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        print('Request failed {}\nError Message:  {}'.format(e, response.text))
        return None
    
# Required input parameters

node= '214748369406'                                           # provide required node path 

model= 'Palfinger_Crane_Assembly'                              # Project name 


data_param={'act_timestamp':'',                                # Current time stamp
           'descr':'stores sensors data',                      # Description of element  
           'name':'SENSORS',                                   # Required Breakdown element name
           'nodeType':'urn:rdl:epm-std:Unit',                  # Node type
           'tmpl':''}                                          # Name of the breakdown template

token = get_token(getTokenData)
if token:
    new_element=create_new_bd_element(node,model,data_param,token)   
    if new_element:
        pp.pprint(new_element)