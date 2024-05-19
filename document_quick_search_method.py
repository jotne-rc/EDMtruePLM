import requests
from generating_token import get_token, plm_info

def doc_quick_search(data_param: dict, model: str, token: str, repository: str = "TruePLMprojectsRep") -> dict:
    """
    Perform a quick search for documents in a project using specific search parameters.

    Args:
    data_param (dict): Parameters for document search.
    model (str): Project name.
    token (str): Authentication token.
    repository (str): Repository name, defaults to 'TruePLMprojectsRep'.

    Returns:
    dict: JSON response from the server if the request is successful, None otherwise.
    """
    doc_search_url = f"{plm_info['url']}/api/dat/q_search/{repository}/{model}/{token}"
    print(f"\nPerforming request: {doc_search_url}")

    try:
        response = requests.get(doc_search_url, params=data_param, timeout=2.0)
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
    model = "Palfinger_Crane_Assembly"  # Project name
    data_param = {
        'case_sens': 'no',
        'domains': 'ID',
        'node': '',                     # Brekdown element instance id
        'page': '',
        'page_size': '',
        'pattern': 'sample',            # Required file name
        'props': ''
    }

    token = get_token()
    if token:
        search_result = doc_quick_search(data_param, model, token)
        if search_result:
            print(search_result)
        else:
            print("No results found or an error occurred.")
    else:
        print("Failed to retrieve token.")

if __name__ == '__main__':
    main()
