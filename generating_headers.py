import requests
import json
import pprint
import json
pp=pprint.PrettyPrinter()

def load_config():
    with open('config.json') as config_file:
        return json.load(config_file)

plm_info = load_config()

headers = {
    'Authorization': plm_info['api_token']  # Ensure this value is set to a valid api_token
}

def get_authorization_header():
    """
    Retrieves the Authorization token from the configuration.
    Returns the headers dictionary if the Authorization token is present and non-empty.
    Otherwise, returns an error message.
    """
    if headers.get('Authorization'):
        return headers
    else:
        return "Error: Authorization token is missing from the headers."

def main():
    res = get_authorization_header()
    
    if isinstance(res, dict) and res.get('Authorization'):
        print("Authorization token is set in the header.")
    else:
        print(res)

# Example usage
if __name__ == "__main__":
    main()