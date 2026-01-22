import requests
from pathlib import Path
from generating_headers import plm_info, headers

PLM_URL = plm_info['url'] 

def download_document(doc_prop):
    source, title = doc_prop['source'], doc_prop['title']
    download_doc_url = f"{PLM_URL}/api/dat/file/data/{source}/{title}"
    print(f"\nPerforming request: {download_doc_url}")

    try:
        response = requests.get(download_doc_url, headers=headers, timeout=2.0)
        response.raise_for_status()
        return response.content if response.ok else None
    except requests.exceptions.Timeout:
        print (f"Request timed out")
    except requests.exceptions.HTTPError as e:
        print (f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
    except requests.exceptions.RequestException as e:
        print (f"Request failed: {e}")

def prepare_doc_for_download(data_param, model, repository="TruePLMprojectsRep"):
    url_download_file = f"{PLM_URL}/api/dat/doc/link/{repository}/{model}"
    try:
        response = requests.get(url_download_file, headers=headers, params=data_param, timeout=2.0)
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
    
    doc_data_param = {'id': '429496743751', 'ver': ''} # id is instance id of the document
    download_document_properties = prepare_doc_for_download(doc_data_param, "Palfinger_Crane_Assembly")
    print(download_document_properties)
    if download_document_properties:
        document_data = download_document(download_document_properties)
        if document_data:
            required_filename = Path('files/downloaded_sample.zip') 
            with required_filename.open('wb') as file:
                file.write(document_data)
            print('The Document has been downloaded successfully.')
        else:
            print('Failed to download document data.')
    else:
        print('Failed to retrieve document properties.')
    
if __name__ == '__main__':
    main()
