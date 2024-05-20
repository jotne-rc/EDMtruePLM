from generating_token import get_token, plm_info
import requests
import pprint

def create_new_bkd_element(node: str, model: str, data_param: dict, token: str, repository="TruePLMprojectsRep"):
    """
    Creates a new breakdown element in the EDMtruePLM system.

    :param node: Node ID under which the new element will be created.
    :param model: Project name.
    :param data_param: Dictionary containing data parameters for the new element.
    :param token: Authentication token.
    :param repository: Repository name, defaults to 'TruePLMprojectsRep'.
    :return: JSON response from the API or error message.
    """
    url = f"{plm_info['url']}/api/bkd/create/{repository}/{model}/{node}/{token}"
    print(f"\nPerforming request: {url}")

    try:
        response = requests.post(url, params=data_param, timeout=2.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.HTTPError as e:
        print(f'HTTP error occurred: {e.response.status_code} - {e.response.text}')
    except requests.exceptions.Timeout:
        print('Request timed out')
    except requests.exceptions.RequestException as e:
        print(f'General Request failed: {e}')
    return None

def main():
    """
    Main function to handle the process of creating a new breakdown element.
    """
    node = '201863467806'                    # Node ID - change this based on the required node
    model = 'Palfinger_Crane_Assembly'       # Project name - Chaneg this 
    parameters = {
        'act_timestamp': '',                 # Current time stamp
        'descr': 'stores sensors data',      # Required new Description of element
        'name': 'SENSORS',                   # Required new Element name
        'nodeType': 'urn:rdl:epm-std:Unit',  # Node type 
        'tmpl': ''                           # Template name
    }
    
    token = get_token()
    if token:
        new_element = create_new_bkd_element(node, model, parameters , token)
        if new_element:
            pp = pprint.PrettyPrinter()
            pp.pprint(new_element)
        else:
            print("Failed to create a new breakdown element.")
    else:
        print("Failed to retrieve token.")

if __name__ == '__main__':
    main()
