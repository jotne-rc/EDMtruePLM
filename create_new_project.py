from generating_headers import plm_info, headers
import requests
import pprint


def create_new_project(data_param, file_path):
    """Create a new project by uploading a STEP file."""

    url = f"{plm_info['url']}/api/adm_user"
    print(f"\nPerforming request: {url}")

    with open(file_path, 'rb') as file:
        files = {'file': file}
        try:
            response = requests.post(url, files=files, headers=headers, data=data_param, timeout=30.0)
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

    parameters = {
        "descr": "Crane assembly",
        "folder": "",
        "is_bkd_tmpl": "false",
        "is_tmpl": "false",
        "name": "Palfinger_Crane_Assembly",
        "src": "pdm", # pdm, bsl, ap242, zip_sys
        "tmpl": ""
    }
    
    file_path = r'files/Palfinger_Crane_Assembly_pdm.zip'


    new_project_information = create_new_project(parameters , file_path)
    if new_project_information:
        pp = pprint.PrettyPrinter()
        pp.pprint(new_project_information)
    else:
        print("Failed to create new project")
    


if __name__ == '__main__':
    main()
