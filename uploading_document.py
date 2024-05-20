from generating_token import get_token,plm_info
import requests

def upload_file(file_path, data_param, model, node, repository="TruePLMprojectsRep"):
    """
    Uploads a file to the specified node in the model within the repository.
    Handles various file types like excel, pdf, word, images.
    """
    token = get_token()
    if not token:
        print("Failed to retrieve token.")
        return None

    url = f"{plm_info['url']}/api/dat/{repository}/{model}/{node}/{token}"
    print(f"\nPerforming request: {url}")
    
    try:
        with open(file_path, "rb") as file_to_upload:
            response = requests.post(url, files={"file": file_to_upload}, data=data_param, timeout=25.0)
            response.raise_for_status()  # Will raise an exception for HTTP error responses
            return response.json()
    except requests.exceptions.HTTPError as e:
        print(f'HTTP error occurred: {e.response.status_code} - {e.response.text}')
    except requests.exceptions.Timeout:
        print('Request timed out')
    except requests.exceptions.RequestException as e:
        print(f'General Request failed: {e}')
    return None

def main():    
        
    # Input Parameters required for file upload 

    file_path = 'files/sample.pdf'                             # file path to upload 

    data_param={'descr':"maintenance information",              # Description of the document
                'title':"sample",                                # Title of the document
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
    node = "201863476589"
        
    data=upload_file(file_path,data_param,model,node)

    if (data):
        print(data)
           

if __name__ == "__main__":
    main()