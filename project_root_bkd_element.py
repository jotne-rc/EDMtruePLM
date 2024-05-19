from generating_token import get_token, plm_info
import requests



def get_root_breakdown_element(model: str, token: str, repository: str = 'TruePLMprojectsRep'):
    """
    Fetches the root breakdown element information from the project.

    :param model: Project name in EDMtruePLM.
    :param token: Auth token for API access.
    :param repository: Repository name, defaults to 'TruePLMprojectsRep'.
    :return: JSON data of the root breakdown element or None if an error occurs.
    """
    url_get_root_bd_info = f"{plm_info['url']}/api/bkd/{repository}/{model}/{token}"
    print(f"\nPerforming request: {url_get_root_bd_info}")

    try:
        response = requests.get(url_get_root_bd_info, timeout=2.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.Timeout:
            return "Request timed out"
    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

def main():
    """
    Main function to execute API call.
    """
    model = "Palfinger_Crane_Assembly"  # change this to required project
    token = get_token()

    if token:
        root_bd = get_root_breakdown_element(model, token)
        if root_bd:
            root_element_name = root_bd['root_bkdn_elem']['name']
            instance_id = root_bd['root_bkdn_elem']['instance_id']
            print(f'The root breakdown element of the project: {root_element_name}, '
                  f'and instance_id is: {instance_id}')
        else:
            print('No root breakdown element information received.')
    else:
        print('Failed to retrieve token')

if __name__ == '__main__':
    main()
