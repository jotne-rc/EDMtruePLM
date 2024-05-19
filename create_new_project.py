from generating_token import get_token, plm_info
import requests
import pprint


def create_new_project(data_param, file_path, token):
    """Create a new project by uploading a STEP file."""

    url = f"{plm_info['url']}/api/adm_user/{token}"
    print(f"\nPerforming request: {url}")
    
    with open(file_path, 'rb') as file:
        files = {'file': file}
        try:
            response = requests.post(url, files=files, data=data_param, timeout=30.0)
            response.raise_for_status()
            return response.json() if response.ok else None
        except requests.exceptions.Timeout:
            return "Request timed out"
        except requests.exceptions.HTTPError as e:
            return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
        except requests.exceptions.RequestException as e:
            return f"Request failed: {e}"


def main():

    parameters = {
        "descr": "Crane assembly",
        "folder": "",
        "is_bkd_tmpl": "false",
        "is_tmpl": "false",
        "name": "Palfinger_Crane_Assembly",
        "nodeType": "",
        "src": "pdm",
        "tmpl": ""
    }
    
    file_path = r'files/Palfinger_Crane_Assembly_pdm.zip'

    token = get_token()   # generating token

    if token:
        new_project_information = create_new_project(parameters , file_path, token)
        if new_project_information:
            pp = pprint.PrettyPrinter()
            pp.pprint(new_project_information)
        else:
            print("Failed to create new project")
    else:
        print("Failed to retrieve token")


if __name__ == '__main__':
    main()
