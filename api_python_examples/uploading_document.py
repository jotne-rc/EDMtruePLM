from generating_token  import *  
from generating_token import get_token
from breakdown_quick_search import bd_quick_search
'''
The method is used for uploading a file in breakdown element /api/dat/{repository}/{model}/{node}/{token} 

This method can be used to upload any file like (excel, pdf, word, images).
'''

def upload_file(data_param,file_to_upload,model,node,token,repository="TruePLMprojectsRep"):

    url_upload_file=PLM_URL+"/api/dat"+"/"+repository + "/" + model + "/" + node + "/"+token

    print("\nPerforming request: " + url_upload_file)

    try:
        response = requests.post(url_upload_file,files= {"file" : file_to_upload },data=data_param,timeout=5.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        print('Request failed {}\nError Message:  {}'.format(e, response.text))
        return None  
        
# Input Parameters required for file upload 

file_path = "test_file.pdf"                                 # file path to upload 
file_to_upload = open(file_path, "rb") 

data_param={'descr':"maintenance information",              # Description of the document
           'title':"test_file",                             # Title of the document
           'source':"urn:rdl:epm-std:Unknown",              # Source of the document
           'contentType':'urn:rdl:epm-std:Miscellaneous',   # Content type of the document
           'discipline':'urn:rdl:epm-std:Uncertain',        # Discipline of the document
           'projPhase':'urn:rdl:epm-std:0',                 # Project phase of the document
           'status':'urn:rdl:epm-std:Approved',             # Status of the document
           'editor':'jotne_rc',                             # Login of person, who edited the document
           'resp':'jotne_rc',                               # Login of person, who responsible for the document
           'rev':'jotne_rc',                                # Login of person, who reviewed the document
           'app':'jotne_rc',                                # Login of person, who approved the document
           'revMan':'jotne_rc'}                             # Login of person, who is the release manager for the document


model="Palfinger_Crane_Assembly"     # Project name 
    
search_params={ "case_sens":"false",         
                "domains":"ID",         
                "folder_only":"true",  
                "node":"",              
                "page":"",              
                "page_size":"",        
                "pattern":"Maintenance data",    # breakdown element where the file need to be uploaded ( Maintenance data element)
                "props":""}        

token = get_token(getTokenData)
if token: 
    node=str(bd_quick_search(model,'q_search',search_params,token)[0]['bkdn_elem_info']['instance_id']) # Required node number
    print('The required breakdown element Instance Id:',node)
    if node:        
        data=upload_file(data_param,file_to_upload,model,node,token)
        if data:
            print(data)  