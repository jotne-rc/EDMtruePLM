import requests
import json
import pprint
import json
pp=pprint.PrettyPrinter()

def load_config():
    with open('config.json') as config_file:
        return json.load(config_file)


plm_info = load_config()

def get_token():
    """
    This function retrieves a token using either the API token directly or user credentials.
    
    Use one of the following JSON structures as appropriate:
    
    For user credentials:
    {
        "group": "sdai-group",   # Default parameter for all users
        "user": "",              # PLM User name
        "pass": ""               # PLM Password
    }
    
    For direct API token access:
    """
    # Assuming `plm_info` contains the 'api_token' key with a valid token
    get_token_data = { 
        "api_token": plm_info["api_token"]
    }

    endpoint="/api/admin/token"  # API method 
    plm_url = plm_info['url']    # Change this to project specific URL
    get_token_url = plm_url + endpoint
    try:
        print("Performing request: " + get_token_url)
        response = requests.post(get_token_url, data=get_token_data, timeout=2.0)
        response.raise_for_status()
        token_data = response.json()
        return token_data.get("token", "Error: Token not found in the response.")
    except requests.exceptions.HTTPError as e:
        print(f'HTTP error occurred: {e.response.status_code} - {e.response.text}')
    except requests.exceptions.Timeout:
        print('Request timed out')
    except requests.exceptions.RequestException as e:
        print(f'General Request failed: {e}')
    return None


def main():
    token = get_token()
    if token and "Error" not in token:
        print("The token is:", token)
    else:
        print(token)

if __name__ == "__main__":
    main()