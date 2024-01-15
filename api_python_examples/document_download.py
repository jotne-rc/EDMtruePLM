from generating_token  import *  
from generating_token import get_token
from breakdown_quick_search import bd_quick_search
from document_quick_search_method import doc_quick_search

'''
The method is used for downloading file from a project 
/api/dat/file/link/{repository}/{model}/{token} Prepare the file of the document for download. 

The response which contains required file properties that are required download, and these are supplied to the below API method 
/api/dat/file/data/{src}/{name}/{token} Return file data for download
'''

def download_data(file_prop,token):   
    print(file_prop)
    
    download_data_url = PLM_URL+"/api/dat/file/data/"+file_prop['source']+"/"+file_prop['title']+"/"+token

    print("\nPerforming request:",download_data_url)

    try:
        response = requests.get(download_data_url, timeout=2.0)
        response.raise_for_status()
        return response if response.ok else None
    except requests.exceptions.RequestException as e:
        print('Request failed {}\nError Message:  {}'.format(e, response.text))
        return None 

def get_doc_file_prop(data_param,model,token,repository="TruePLMprojectsRep"):
    
    url_download_file=PLM_URL+"/api/dat/file/link"+"/"+repository + "/" + model+"/"+token
    try:
        response = requests.get(url_download_file,params=data_param,timeout=2.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        print('Request failed {}\nError Message:  {}'.format(e, response.text))
        return None 

model="Palfinger_Crane_Assembly"     # Project name
 
#parameters required for document quick search method  
data_param={'case_sens':'no',    # Use case sensitive search or not
            'domains':'ID',      # CSV list of subjects for search, can include ID, DESCRIPTION, CLASS, PROPERTY
            'node':'',           # Breakdown element instance id - root of interesting branch
            'page':'',           # Start page of output
            'page_size':'',      # Page size of output
            'pattern':'test_file', # Search string pattern (for LIKE operations in EXPRESS)
            'props':''}            # CSV list of property names where to apply search pattern 


# parameters required for breakdown element quick search method     
node_search_params={ "case_sens":"false",         
                "domains":"ID",         
                "folder_only":"true",  
                "node":"",              
                "page":"",              
                "page_size":"",        
                "pattern":"Maintenance data",  # breakdown element where the file need to be searched ( Maintenance data element)
                "props":""}        


doc_data_param={'name':'',  # required file name to dowload 
           'ver':''}         # instance id of document can be obtained from document (q_search or a_search)
      
token=get_token(getTokenData)

if token: 
    required_node=str(bd_quick_search(model,'q_search',node_search_params,token)[0]['bkdn_elem_info']['instance_id'])
    if required_node:
        data_param['node']= required_node
        doc_search_result=doc_quick_search(data_param,model,token)
    if doc_search_result:
        doc_data_param['name']=str(doc_search_result[0]['doc_info']['file_name'])
        doc_data_param['ver']=str(doc_search_result[0]['doc_info']['instance_id'])
        file_properties=get_doc_file_prop(doc_data_param,model,token) 
        if file_properties:
            file_data=download_data(file_properties,token)
            if file_data: 
                required_filename = Path('downloaded_test_file.pdf')
                required_filename.write_bytes(file_data.content)
                print('The file has downloaded')