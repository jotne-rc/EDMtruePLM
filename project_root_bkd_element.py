from generating_headers import plm_info, headers
import requests



def get_root_breakdown_element(model: str, repository: str = 'TruePLMprojectsRep'):
    """
    Fetches the root breakdown element information from the project.

    :param model: Project name in EDMtruePLM.
    :param repository: Repository name, defaults to 'TruePLMprojectsRep'.
    :return: JSON data of the root breakdown element or None if an error occurs.
    """
    url_get_root_bd_info = f"{plm_info['url']}/api/bkd/{repository}/{model}"
    print(f"\nPerforming request: {url_get_root_bd_info}")

    try:
        response = requests.get(url_get_root_bd_info, headers=headers, timeout=2.0)
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
    Main function to execute API call.
    """
    model = "Palfinger_Crane_Assembly"  # change this to required project
    
    
    root_bd = get_root_breakdown_element(model)
    if root_bd:
        root_element_name = root_bd['root_bkdn_elem']['name']
        instance_id = root_bd['root_bkdn_elem']['instance_id']
        print(f'The root breakdown element of the project: {root_element_name}, '
                f'and instance_id is: {instance_id}')
    else:
        print('No root breakdown element information received.')
   

if __name__ == '__main__':
    main()
