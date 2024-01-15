from generating_token  import *  
from generating_token import get_token
from breakdown_quick_search import bd_quick_search


#####################  Updating element Property information  ###################### 


#####################  Updating breakdown element Property information  ###################### 

def update_breakdown_element_prop(model,node,upload_prop_data,token,repository="TruePLMprojectsRep"):

    update_prop_url = PLM_URL + "/api/bkd/prop/" + repository + "/" + model + "/" + node + "/"  + token
    print("\nPerforming request: " + update_prop_url)

    try:
        response = requests.post(update_prop_url,data = upload_prop_data, timeout=2.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        print('Request failed {}\nError Message:  {}'.format(e, response.text))
        return None   

model= 'Palfinger_Crane_Assembly'     # Project name 



# Breakdown element properties

upload_prop_data={
     'act_timestamp':'',
     'props': ["urn:rdl:Palfinger_Crane_Assembly:Manufacturer","urn:rdl:Palfinger_Crane_Assembly:Sensor_ID","urn:rdl:Palfinger_Crane_Assembly:Weight"],
     'ptypes': ['string','N','N'],
     'units':["","","Kg"],
     'vals': ['ABCD',1001,0.05]}


search_params={ "case_sens":"false",         
                "domains":"ID",         
                "folder_only":"true",  
                "node":"",              
                "page":"",              
                "page_size":"",        
                "pattern":"Accelerometer_Sensor",   # Required Breakdown element name 
                "props":""}                

token = get_token(getTokenData)
if token: 
    node=str(bd_quick_search(model,'q_search',search_params,token)[0]['bkdn_elem_info']['instance_id']) # Required node number
    print('The required breakdown element Instance Id:',node)
    if node:
        upload_result=update_breakdown_element_prop(model,node,upload_prop_data,token)
        if upload_result:
            pp.pprint(upload_result)      