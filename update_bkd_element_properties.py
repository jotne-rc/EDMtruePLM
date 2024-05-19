from generating_token import get_token, plm_info
import requests
import pprint

def update_breakdown_element_prop(model: str, node: str, upload_prop_data: dict, token: str, repository: str = "TruePLMprojectsRep") -> dict:
    """
    Updates properties of a breakdown element in the PLM system.

    Args:
    model (str): The name of the model.
    node (str): The instance ID of the breakdown element.
    upload_prop_data (dict): Properties to upload.
    token (str): Authentication token.
    repository (str): Repository name, default is 'TruePLMprojectsRep'.

    Returns:
    dict: The server response if the request is successful, None otherwise.
    """
    update_prop_url = f"{plm_info['url']}/api/bkd/prop/{repository}/{model}/{node}/{token}"
    print(f"\nPerforming request: {update_prop_url}")

    try:
        response = requests.post(update_prop_url, data=upload_prop_data, timeout=2.0)
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
        upload_prop_data = {
            'act_timestamp': '',
            'props': [
                "urn:rdl:Palfinger_Crane_Assembly:Manufacturer",
                "urn:rdl:Palfinger_Crane_Assembly:Serial Number"
            ],
            'ptypes': ['string', 'N'],
            'units': ["", ""],
            'vals': ['ABCD', 1001]
        }
        model = "Palfinger_Crane_Assembly"
        node = "201863476589"
        upload_result = update_breakdown_element_prop(model, node, upload_prop_data, token)
        if upload_result:
            pp = pprint.PrettyPrinter()
            pp.pprint(upload_result)
        else:
            print("No response or an error occurred.")
    else:
        print("Failed to retrieve token.")

if __name__ == '__main__':
    main()
