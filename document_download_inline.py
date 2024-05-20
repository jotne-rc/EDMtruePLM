import requests
from pathlib import Path
from generating_token import get_token, plm_info, headers

PLM_URL = plm_info['url']

def file_for_download(data_param, model, token, repository="TruePLMprojectsRep"):
    """
    Fetches a file from the server based on provided parameters. 
    Handles the response differently based on 'use_inline' parameter in data_param.
    """
    download_url = f"{PLM_URL}/api/dat/file/body/{repository}/{model}/{token}"
    print(f"Making request to: {download_url}")

    try:
        response = requests.get(download_url, headers=headers, params=data_param, timeout=2.0)
        response.raise_for_status()

        # Check if we are expected to handle the file inline or as a downloadable file
        if data_param.get('use_inline', 'true').lower() == 'false':
            return response.content  # Return binary content for file download
        else:
            return "the file will be rendered in browser"
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    return None

def main():
    token = get_token()
    if token:
        doc_data_param = {'name': 'sample', 'ver': '201863484150', 'use_inline': 'true'}
        file_data = file_for_download(doc_data_param, "Palfinger_Crane_Assembly", token)
        if file_data:
            # Save the file if 'use_inline' is 'false'
            if doc_data_param.get('use_inline', 'true').lower() == 'false':
                file_path = Path('files/downloaded_file.webm')  # Adjust the extension based on your file type
                file_path.write_bytes(file_data)
                print(f"The file has been downloaded and saved to {file_path}")
            else:
                print(file_data)
        else:
            print("Failed to download or fetch file data.")
    else:
        print("Failed to retrieve token.")

if __name__ == '__main__':
    main()
