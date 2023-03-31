slug = 'affluence-piety-5i-260509'
slug2 = 'risk-free-colorful-7b-261021'
import requests

def check(slug:str):
    '''

    :param slug: 任务的唯一标识符
    :return: status:str 当前状态
    查看slug对应任务的状态，若是 ’finished‘，则训练完成，可以下载了
    '''
    # slug from Capture step
    auth_headers = {
        'Authorization': 'luma-api-key=ec167066-0fe8-46da-8aab-a372f2bfccab-9be191d-ff20-4f1e-a439-bc42cfe19e93'}
    response = requests.get(f"https://webapp.engineeringlumalabs.com/api/v2/capture/{slug}",
                            headers=auth_headers)

    # 将response.text写入data.json文件中
    import json
    with open('temp/response.json', 'w') as f:
        json.dump(response.text, f)

    # 解析json数据，获取obj文件的status
    data = json.loads(response.text)
    status = data['latestRun']['status']
    print(f'the status is :{status}')
    return status



def download(slug:str):
    '''

    :param slug:
    :return:None
    以title为文件名，放置在models文件夹下。
    '''
    # slug from Capture step
    auth_headers = {
        'Authorization': 'luma-api-key=ec167066-0fe8-46da-8aab-a372f2bfccab-9be191d-ff20-4f1e-a439-bc42cfe19e93'}
    response = requests.get(f"https://webapp.engineeringlumalabs.com/api/v2/capture/{slug}",
                            headers=auth_headers)
    print(f'response.text:\n{response.text}')

    # 将response.text写入data.json文件中
    import json
    with open('data.json', 'w') as f:
        json.dump(response.text, f)

    # 解析json数据，获取obj文件的URL
    obj_url = None
    data = json.loads(response.text)
    for artifact in data['latestRun']['artifacts']:
        if artifact['type'] == 'textured_mesh_obj' and artifact['url'].endswith('.zip'):
            obj_url = artifact['url']
            break
    if obj_url is None:
        print('No obj file found.')
        return
    print(obj_url)


    # 下载zip文件
    response = requests.get(obj_url)
    with open('model.zip', 'wb') as f:
        f.write(response.content)

    # 解压zip文件到models文件夹中
    import zipfile
    import os

    title = data.get('title', 'unknown')  # 获取title，如果没有则使用'unknown'作为默认值
    dir_path = "../static/models/"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with zipfile.ZipFile('model.zip', 'r') as zip_ref:
        zip_ref.extractall(f'{dir_path}/{title}')


