from generating_token import get_token,plm_info
import requests
import pprint

def get_breakdown_element_prop(model: str, node: str, get_prop_data: dict, token: str, repository: str = "TruePLMprojectsRep") -> dict:
    """
    get properties of a breakdown element in the PLM system.

    Args:
    model (str): The name of the model.
    node (str): The instance ID of the breakdown element.
    get_prop_data (dict): Properties to upload.
    token (str): Authentication token.
    repository (str): Repository name, default is 'TruePLMprojectsRep'.

    Returns:
    dict: The server response if the request is successful, None otherwise.
    """
    get_prop_url = f"{plm_info['url']}/api/bkd/{repository}/{model}/{node}/{token}"
    print(f"\nPerforming request: {get_prop_url}")

    try:
        response = requests.get(get_prop_url, data=get_prop_data, timeout=2.0)
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
        # Modify this based on the required property data
        get_prop_data = {
            "count":100        }
        model = "Palfinger_Crane_Assembly"
        node = "201863476589"
        upload_result = get_breakdown_element_prop(model, node, get_prop_data, token)
        if upload_result:
            pp = pprint.PrettyPrinter()
            pp.pprint(upload_result)
        else:
            print("No response or an error occurred.")
    else:
        print("Failed to retrieve token.")

if __name__ == '__main__':
    main()
