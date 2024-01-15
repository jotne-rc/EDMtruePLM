from generating_token  import *  
from generating_token import get_token
from breakdown_quick_search import bd_quick_search

'''
This method is used for searching documents in a project.

/api/dat/a_search/{repository}/{model}/{token} Advanced search for the documents 
'''

def document_advanced_search(data_param,model,token,repository="TruePLMprojectsRep"):

    doc_search_url=PLM_URL+"/api/dat/a_search"+"/"+repository + "/" + model + "/"+token

    print("\nPerforming request: " + doc_search_url)

    try:
        response = requests.get(doc_search_url,params=data_param,timeout=2.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        print('Request failed {}\nError Message:  {}'.format(e, response.text))
        return None  
        
        
model="Palfinger_Crane_Assembly"     # Project name     

# parameters required for node quick search method     
node_search_params={ "case_sens":"false",         
                "domains":"ID",         
                "folder_only":"true",  
                "node":"",              
                "page":"",              
                "page_size":"",        
                "pattern":"Maintenance data",  # breakdown element where the file need to be searched ( Maintenance data element)
                "props":""}       

# parameters required for doduemnt search 

data_param={ 'approver':'',         # Search value for the document approver person
            'checkOutUser':'',      # Search for the documents checked out by the specified person
            'createAfter':'',       # Search for the document created after the specified date
            'createBefore':'',      # Search for the document created before the specified date
            'createUser':'',        # Search for the documents created by the specified person
            'dataType':'',          # Search value for the document data type
            'descipline':'',        # Search value for the document discipline
            'descr':'maintenance information',             # Search pattern for the document description
            'docSource':'',         # Search value for the document source
            'docStatus':'',         # Search value for the document status
            'docType':'',           # Search value for the document type
            'editAfter':'',         # Search for the document edited after the specified date
            'editBefore':'',        # Search for the document edited before the specified date
            'editUser':'',          # Search for the documents edited by the specified person
            'editor':'',            # Search value for the document editor person
            'extVer':'',            # Search value for the document external version
            'limit':'',             # Limit for the number of search result
            'nodeID':'',            # Root element’s instance ID of the branch to search within
            'nodeVer':'',           # Version number of the element to search within
            'onlyCheckOut':'false', # Search for the checked out documents only
            'onlyRedFlag':'false',  # Search for the documents with the read flag only
            'onlyStickyNote':'false', # Search for the documents with the sticky notes only
            'pPhase':'',              # Search value for the document project phase
            'propName':'',            # List of the document property names to search for
            'propVal':'',             # List of the document property values to search for
            'rManager':'',            # Search value for the document release manager person
            'responsible':'',         # Search value for the document responsible person
            'reviewer':'',            # Search value for the document reviewer person
            'rid':'',                 # Search value for the document RID
            'submitAfter':'',         # Search for the document submitted after the specified date
            'submitBefore':'',        # Search for the document submitted before the specified date
            'title':'test_file'    }           # Search pattern for the document title
    
token = get_token(getTokenData)
if token: 
    required_node=str(bd_quick_search(model,'q_search',node_search_params,token)[0]['bkdn_elem_info']['instance_id'])
    if required_node:
        data_param['nodeID']= required_node             
        search_result=document_advanced_search(data_param,model,token)
        if search_result:
            print(search_result)  
