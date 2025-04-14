from generating_headers import plm_info, headers
import requests
import pprint

def create_new_bkd_element(node: str, model: str, data_param: dict, repository="TruePLMprojectsRep"):
    """
    Creates a new breakdown element in the EDMtruePLM system.

    :param node: Node ID under which the new element will be created.
    :param model: Project name.
    :param data_param: Dictionary containing data parameters for the new element.
    :param token: Authentication token.
    :param repository: Repository name, defaults to 'TruePLMprojectsRep'.
    :return: JSON response from the API or error message.
    """
    url = f"{plm_info['url']}/api/bkd/create/{repository}/{model}/{node}"
    print(f"\nPerforming request: {url}")

    try:
        response = requests.post(url, headers=headers, params=data_param, timeout=2.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.Timeout:
        print (f"Request timed out")
    except requests.exceptions.HTTPError as e:
        print (f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
    except requests.exceptions.RequestException as e:
        print (f"Request failed: {e}")
    return None

def main():
    """
    Main function to handle the process of creating a new breakdown element.
    """
    node = '201863469170'#'201863467806'                    # Node ID - change this based on the required node
    model = 'Palfinger_Crane_Assembly'       # Project name - Chaneg this 
    parameters = {
        'act_timestamp': '',                 # Current time stamp
        'descr': 'stores sensors data',      # Required new Description of element
        'name': 'SENSORS',                   # Required new Element name
        'nodeType': 'urn:rdl:epm-std:Unit',  # Node type 
        'tmpl': ''                           # Template name
    }
    
    
    
    new_element = create_new_bkd_element(node, model, parameters)
    if new_element:
        pp = pprint.PrettyPrinter()
        pp.pprint(new_element)
    else:
        print("Failed to create a new breakdown element.")
    

if __name__ == '__main__':
    main()
