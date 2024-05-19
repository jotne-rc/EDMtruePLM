import requests
from pathlib import Path
from generating_token import get_token, plm_info

PLM_URL = plm_info['url'] 

def download_file(file_prop, token):
    source, title = file_prop['source'], file_prop['title']
    download_data_url = f"{PLM_URL}/api/dat/file/data/{source}/{title}/{token}"
    print(f"\nPerforming request: {download_data_url}")

    try:
        response = requests.get(download_data_url, timeout=2.0)
        response.raise_for_status()
        return response.content if response.ok else None
    except requests.exceptions.Timeout:
        return "Request timed out"
    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

def prepare_file_for_download(data_param, model, token, repository="TruePLMprojectsRep"):
    url_download_file = f"{PLM_URL}/api/dat/file/link/{repository}/{model}/{token}"
    try:
        response = requests.get(url_download_file, params=data_param, timeout=2.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.Timeout:
        return "Request timed out"
    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

def main():
    token = get_token()
    if token:
        doc_data_param = {'name': 'sample', 'ver': '201863484150'}
        file_properties = prepare_file_for_download(doc_data_param, "Palfinger_Crane_Assembly", token)
        print(file_properties)
        if file_properties:
            file_data = download_file(file_properties, token)
            if file_data:
                required_filename = Path('files/downloaded_sample.pdf')
                with required_filename.open('wb') as file:
                    file.write(file_data)
                print('The file has been downloaded successfully.')
            else:
                print('Failed to download file data.')
        else:
            print('Failed to retrieve file properties.')
    else:
        print('Failed to retrieve token.')

if __name__ == '__main__':
    main()
