import json
import os

import requests
key = 'ec167066-0fe8-46da-8aab-a372f2bfccab-9be191d-ff20-4f1e-a439-bc42cfe19e93'

def create(title:str, file_path:str):
    '''

    :param title:模型标题
    :param file_path: 本地文件zip（照片集）
    :return: tuple(upload_url,slug,response.text)
    upload_url:上传文件的url,
    slug:该模型的唯一标识符，用于确定模型，进行下载等操作
    response.text:返回response的内容，此时还没有重建成功，仅有一些基本的元数据，还没有下载链接。dict中的currentStage显示重建的阶段。
    '''
    capture_title = title
    auth_headers = {'Authorization': 'luma-api-key=ec167066-0fe8-46da-8aab-a372f2bfccab-9be191d-ff20-4f1e-a439-bc42cfe19e93'}

    response = requests.post("https://webapp.engineeringlumalabs.com/api/v2/capture",
                             headers=auth_headers,
                             data={'title': capture_title})
    capture_data = response.json()
    upload_url = capture_data['signedUrls']['from']
    slug = capture_data['capture']['slug']
    print(capture_data)
    print("Upload URL:", upload_url)
    print("Capture slug:", slug)


    # Save response.text as JSON file in temp folder
    response_data = json.loads(response.text)
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    with open(f"{temp_dir}/response.json", "w") as f:
        json.dump(response_data, f)

    # Upload  这里的response不返回任何东西
    with open(file_path, "rb") as f:
        payload = f.read()
    response = requests.put(upload_url, headers={'Content-Type': 'text/plain'}, data=payload)



    return (upload_url,slug,response)

def trigger(slug:str):
    '''

    :param slug:
    :return: response.text
    调用trigger后，开始处理模型，credit-1,若想查看上传模型的元数据（title、date等等），建议用Create产生的response
    '''
    # Trigger
    auth_headers = {'Authorization': 'luma-api-key=ec167066-0fe8-46da-8aab-a372f2bfccab-9be191d-ff20-4f1e-a439-bc42cfe19e93'}
    response = requests.post(f"https://webapp.engineeringlumalabs.com/api/v2/capture/{slug}",
                             headers=auth_headers)
    return response

