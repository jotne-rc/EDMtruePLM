from generating_token  import *  
from generating_token import get_token
from breakdown_quick_search import bd_quick_search

'''
These methods are used for searching documents in a project.

/api/dat/q_search/{repository}/{model}/{token} quick Search for the documents

'''

def doc_quick_search(data_param,model,token,repository="TruePLMprojectsRep"):

    doc_search_url=PLM_URL+"/api/dat/q_search"+"/"+repository + "/" + model + "/"+token
    print("\nPerforming request: " + doc_search_url)

    try:
        response = requests.get(doc_search_url,params=data_param,timeout=2.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        print('Request failed {}\nError Message:  {}'.format(e, response.text))
        return None  
    
# parameters required for breakdown element quick search method     
node_search_params={ "case_sens":"false",         
                "domains":"ID",         
                "folder_only":"true",  
                "node":"",              
                "page":"",              
                "page_size":"",        
                "pattern":"Maintenance data",  # breakdown element where the file need to be searched ( Maintenance data element)
                "props":""}        
    
# parameters required for document quick search method 

data_param={'case_sens':'no',    # Use case sensitive search or not
            'domains':'ID',      # CSV list of subjects for search, can include ID, DESCRIPTION, CLASS, PROPERTY
            'node':'',           # Breakdown element instance id - root of interesting branch
            'page':'',           # Start page of output
            'page_size':'',      # Page size of output
            'pattern':'test_file', # Search string pattern (for LIKE operations in EXPRESS)
            'props':''}            # CSV list of property names where to apply search pattern 

model="Palfinger_Crane_Assembly"     # Project name   
    
token = get_token(getTokenData)

if token: 
    required_node=str(bd_quick_search(model,'q_search',node_search_params,token)[0]['bkdn_elem_info']['instance_id'])
    if required_node:
        data_param['node']= required_node
        search_result=doc_quick_search(data_param,model,token)
        if search_result:
            pp.pprint(search_result)  
