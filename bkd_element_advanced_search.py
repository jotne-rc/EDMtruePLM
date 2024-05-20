from generating_token import get_token, plm_info, headers
import requests
import pprint

# Advanced search for the breakdown element in the project
def bkd_advanced_search(model: str, search_params: dict, token: str,repository: str="TruePLMprojectsRep") -> dict:
    """
    Performs an advanced search for breakdown elements based on various attributes.
    
    Parameters:
    - model: Project model name.
    - repository: Repository to search within.
    - search_params: Dictionary containing search parameters.
    - token: Authorization token.

    Returns:
    - Dictionary containing search results or None if an error occurs.
    """
    # Construct the search URL
    search_url = f"{plm_info['url']}/api/bkd/a_search/{repository}/{model}/{token}"
    print(f"\nPerforming request: {search_url}")

    
    try:
        response = requests.get(search_url, headers=headers, params=search_params, timeout=2.0)
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        return response.json() if response.ok else None
    except requests.exceptions.HTTPError as e:
        print(f'HTTP error occurred: {e.response.status_code} - {e.response.reason}')
    except requests.exceptions.Timeout:
        print('Request timed out')
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
    return None

def main():
    # Define search parameters
    search_params = {
        "createAfter": "",    # Search for elements created after a specific date
        "createBefore": "",   # Search for elements created before a specific date
        "createUser": "",     # Search for elements created by a specific user
        "descr": "",          # Description pattern to search for
        "editAfter": "",      # Search for elements edited after a specific date
        "editBefore": "",     # Search for elements edited before a specific date
        "editUser": "",       # Search for elements edited by a specific user
        "limit": "",          # Limit the number of results returned
        "nodeID": "",         # Instance ID of the root element to start the search
        "nodeVer": "",        # Version number to search within
        "pPhase": "",         # Project phase to include in search
        "pattern": "SENSORS", # Search pattern for element name
        "propName": [],       # Property names to search
        "propVal": [],        # Property values to match
        "type": ""            # Type pattern to search for
    }

    # Obtain token
    token = get_token()
    if token:
        search_result = bkd_advanced_search("Palfinger_Crane_Assembly", search_params, token)
        if search_result:
            pp = pprint.PrettyPrinter()
            pp.pprint(search_result)
        else:
            print("No results found or an error occurred.")
    else:
        print("Failed to retrieve token.")

if __name__ == '__main__':
    main()
