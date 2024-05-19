import requests
from generating_token import get_token, plm_info

def doc_delete(ass_doc_instance_id: str, model:str,token: str,repository:str="TruePLMprojectsRep") -> dict:
    """
    Deletes a document from the project based on the document's instance ID.

    Parameters:
    - ass_doc_instance_id (str): The instance ID of the document to delete.
    - token (str): Authentication token.

    Returns:
    - dict: JSON response from the server if the deletion is successful, None otherwise.
    """
    del_doc_url = f"{plm_info['url']}/api/dat/{repository}/{model}/{ass_doc_instance_id}/{token}"
    print(f"\nPerforming request: {del_doc_url}")
    try:
        response = requests.delete(del_doc_url, timeout=2.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.HTTPError as e:
        print(f'HTTP error occurred: {e.response.status_code} - {e.response.text}')
    except requests.exceptions.Timeout:
        print('Request timed out')
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e.response.text}')
    return None

def main():
    token = get_token()
    model = "Palfinger_Crane_Assembly"
    if token:
        ass_doc_instance_id = "201863484089"  # Document instance ID obtained from search
        result = doc_delete(ass_doc_instance_id, model, token)
        if result:
            print("Document deleted successfully:", result)
        else:
            print("Failed to delete document.")
    else:
        print("Failed to retrieve token.")

if __name__ == '__main__':
    main()
