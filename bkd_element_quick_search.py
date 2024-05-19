from generating_token import get_token, plm_info
import requests

PLM_URL = plm_info['url']  # Ensure this is defined in your generating_token module or config

def bkd_quick_search(model: str, search_type: str, search_params: dict, token: str, repository="TruePLMprojectsRep"):
    """
    Conducts a quick search or an extended quick search on breakdown elements based on the provided parameters.

    :param model: Project name.
    :param search_type: Type of search ('q_search' or 'q_search_ext').
    :param search_params: Dictionary of parameters for the search.
    :param token: Authentication token.
    :param repository: Repository name, defaults to 'TruePLMprojectsRep'.
    :return: JSON response from the API or None if an error occurs.
    """
    if search_type not in ["q_search", "q_search_ext"]:
        print('Invalid search type')
        return None

    search_url = f"{PLM_URL}/api/bkd/{search_type}/{repository}/{model}/{token}"
    print(f"\nPerforming request: {search_url}")

    try:
        response = requests.get(search_url, params=search_params, timeout=2.0)
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
    token = get_token()  
    if token:
        search_params = {
            "case_sens": "false",
            "domains": "ID",
            "folder_only": "true",
            "pattern": "SENSORS",
            "node"   : "201863467806"
        }
        result = bkd_quick_search('Palfinger_Crane_Assembly', 'q_search', search_params, token)
        if result:
            print(result)
        else:
            print("No results returned or an error occurred.")
    else:
        print("Failed to retrieve token.")

if __name__ == '__main__':
    main()
