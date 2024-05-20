import pprint
from generating_token import get_token, plm_info, headers
import requests


# Ensure PLM_URL is defined, assuming it's stored in `plm_info`
PLM_URL = plm_info['url']

def delete_breakdown_element(model: str, node: str, token: str,repository: str="TruePLMprojectsRep"):
    """
    Deletes a breakdown element by its node ID.

    Args:
    model (str): The name of the model.
    node (str): The node ID of the breakdown element to be deleted.
    token (str): Authentication token required for the API call.

    Returns:
    dict: JSON response from the server if deletion is successful, None otherwise.
    """
    del_bd_elem_url = f"{plm_info['url']}/api/bkd/{repository}/{model}/{node}/{token}"
    print(f"\nPerforming request: {del_bd_elem_url}")
    
    try:
        response = requests.delete(del_bd_elem_url, headers=headers, timeout=2.0)
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
    """
    Main function to execute the deletion process.
    """
    node = "201863476637"  # Instance ID of the breakdown element
    model = 'Palfinger_Crane_Assembly'
    token = get_token()

    if token:
        delete_result = delete_breakdown_element(model, node, token)
        if delete_result:
            pp = pprint.PrettyPrinter()
            pp.pprint(delete_result)
        else:
            print("Deletion failed or no response was received.")
    else:
        print("Failed to retrieve token.")

if __name__ == '__main__':
    main()
