import requests
from generating_token import get_token, plm_info


def document_advanced_search(data_param,model,token,repository="TruePLMprojectsRep"):

    """
    Performs an advanced search for documents within a project.

    Args:
    data_param (dict): Parameters for document search.
    model (str): The project model name.
    token (str): Authentication token.
    repository (str): Repository name, defaults to 'TruePLMprojectsRep'.

    Returns:
    dict: JSON response from the API if the request is successful, None otherwise.
    """
    doc_search_url = f"{plm_info['url']}/api/dat/a_search/{repository}/{model}/{token}"
    print(f"\nPerforming request: {doc_search_url}")

    try:
        response = requests.get(doc_search_url,params=data_param,timeout=2.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.HTTPError as e:
        print(f'HTTP error occurred: {e.response.status_code} - {e.response.reason}')
    except requests.exceptions.Timeout:
        print('Request timed out')
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
    return None
        
   
def main():
    token = get_token()
    if token:
        model="Palfinger_Crane_Assembly"     # Project name  
        # parameters required for document search 
        data_param={ 'approver':'',         # Search value for the document approver person
                    'checkOutUser':'',      # Search for the documents checked out by the specified person
                    'createAfter':'',       # Search for the document created after the specified date
                    'createBefore':'',      # Search for the document created before the specified date
                    'createUser':'',        # Search for the documents created by the specified person
                    'dataType':'',          # Search value for the document data type
                    'descipline':'',        # Search value for the document discipline
                    'descr':'test',             # Search pattern for the document description
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
                    'title':'sample'    }           # Search pattern for the document title
        
        search_result = document_advanced_search(data_param, model, token)

        print(search_result)

        if search_result:
            print(search_result)
        else:
            print("No results found or an error occurred.")
    else:
        print("Failed to retrieve token.")

if __name__ == '__main__':
    main()