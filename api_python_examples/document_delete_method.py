from generating_token  import *  
from generating_token import get_token
from breakdown_quick_search import bd_quick_search
from document_quick_search_method import doc_quick_search

'''
To find the necessary Breakdown element information, it is advised to use search functions. The alternate approach as 
demonstrated below, is to hardcode the instance id to the node variable. It is accessible through the GUI in the Figure. 
Instance id of the necessary breakdown element to delete, 

node="21478374906" 

'''

def doc_delete(ass_doc_instance_id,token,repository="TruePLMprojectsRep"):

    del_doc_url=PLM_URL+"/api/dat"+"/"+repository+"/"+model+"/"+ass_doc_instance_id+"/"+token
    print("\nPerforming request: "+del_doc_url)
    try:
        response=requests.delete(del_doc_url,timeout=2.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        print('Request failed {}\nError Message:  {}'.format(e, response.text))
        return None 
    
model="Palfinger_Crane_Assembly"     # Project name 


# parameters required for breakdown element quick search method     
node_search_params={ "case_sens":"false",         
                "domains":"ID",         
                "folder_only":"true",  
                "node":"",              
                "page":"",              
                "page_size":"",        
                "pattern":"Maintenance data",  # breakdown element where the file need to be searched ( Maintenance data element)
                "props":""}        


data_param={'case_sens':'no',    # Use case sensitive search or not
            'domains':'ID',      # CSV list of subjects for search, can include ID, DESCRIPTION, CLASS, PROPERTY
            'node':'',           # Breakdown element instance id - root of interesting branch
            'page':'',           # Start page of output
            'page_size':'',      # Page size of output
            'pattern':'test_file', # Search string pattern (for LIKE operations in EXPRESS)
            'props':''}            # CSV list of property names where to apply search pattern 

token=get_token(getTokenData) 
if token: 
    required_node=str(bd_quick_search(model,'q_search',node_search_params,token)[0]['bkdn_elem_info']['instance_id'])
    if required_node:
        data_param['node']= required_node
        doc_search_result=doc_quick_search(data_param,model,token)
    if doc_search_result:
        ass_doc_instance_id=str(doc_search_result[0]['doc_info']['ass_doc_instance_id'])  #Document ass_doc_instance_id obtained from q_search or a_search
        if ass_doc_instance_id:     
            doc_delete(ass_doc_instance_id,token)
            print('file has been deleted')