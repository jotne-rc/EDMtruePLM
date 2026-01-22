from generating_headers import plm_info, headers
import requests

def create_document(file_path, data_param, model, node, repository="TruePLMprojectsRep"):
    """
    Creates a document to the specified node in the model within the repository.
    Handles various file attachment types like excel, pdf, word, images.
    """
   
    url = f"{plm_info['url']}/api/dat/doc/{repository}/{model}/{node}"
    print(f"\nPerforming request: {url}")
    
    try:
        with open(file_path, "rb") as file_to_upload:
            response = requests.post(url, headers=headers, files={"file": file_to_upload}, data=data_param, timeout=25.0)
            print(response)
            response.raise_for_status()  # Will raise an exception for HTTP error responses
            return response.json()
    except requests.exceptions.HTTPError as e:
        print(f'HTTP error occurred: {e.response.status_code} - {e.response.reason}')
    except requests.exceptions.Timeout:
        print('Request timed out')
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
    return None
    

def add_file(file_path, data_param, model, doc, repository="TruePLMprojectsRep"):
    """
    Adds a file to an existing document in the specified document in the model within the repository.
    Handles various file attachment types like excel, pdf, word, images.
    """
   
    url = f"{plm_info['url']}/api/dat/file/{repository}/{model}/{doc}"
    print(f"\nPerforming request: {url}")
    
    try:
        with open(file_path, "rb") as file_to_upload:
            response = requests.post(url, headers=headers, files={"file": file_to_upload}, data=data_param, verify=False, timeout=25.0)
            print(response)
            response.raise_for_status()  # Will raise an exception for HTTP error responses
            return response.json()
    except requests.exceptions.HTTPError as e:
        print(f'HTTP error occurred: {e.response.status_code} - {e.response.reason}')
    except requests.exceptions.Timeout:
        print('Request timed out')
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
    return None    

def main():    
        
    # Input Parameters required for file upload 

    file_path = 'files/sample.pdf'                             # file path to upload, multiple files can be attached

    data_param={"descr":"maintenance information",                  # Description of the document
                "title":"Man",                                   # Title of the document 
                "source":"urn:rdl:epm-std:Unknown",                 # Source of the document
                "contentType":"urn:rdl:AP242:Domain:DigitalFile",   # Content type of the document
                "fileType":"urn:plcs:rdl:TruePLM:Binary",           # Binary file type
                "location":"urn:plcs:rdl:TruePLM:In_data_model",              
                "discipline":"urn:rdl:epm-std:Uncertain",        # Discipline of the document
                "projPhase":"urn:rdl:epm-std:0",                 # Project phase of the document
                "status":"urn:rdl:epm-std:Approved",             # Status of the document
                "editor":"jotne_rc",                             # Login of person, who edited the document
                "resp":"jotne_rc",                               # Login of person, who responsible for the document
                "rev":"jotne_rc",                                # Login of person, who reviewed the document
                "app":"jotne_rc",                                # Login of person, who approved the document
                "revMan":"jotne_rc"}                             # Login of person, who is the release manager for the document


    model="Palfinger_Crane_Assembly"     # Project name 
    node = "201863476589"                # Node instance where the document to be uploaded
    

    data=create_document(file_path,data_param,model,node)

    if (data):
       print(data)


    '''
        This section adds a file to an existing document instance. Ensure that the document instance ID is valid.
        Uncomment the below section to test adding a file to an existing document.
    '''

    # file_param={"title":"Added_file",          # Title of the file to be added
    #             "type":"urn:plcs:rdl:TruePLM:Binary",
    #             "location":"urn:plcs:rdl:TruePLM:In_data_model"}

    # doc_instance_id = "429496743751"   # Document instance id where the file to be added   
    # file_res =add_file(file_path,file_param,model,doc_instance_id) 
    # if (file_res):
    #    print(file_res)
    
if __name__ == "__main__":
    main()