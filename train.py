import requests
import os
import json
from engine.create_upload_triger import create,trigger
from engine.check_download import check,download

# 获得最近获得的文件
def get_most_recently_uploaded_file(directory):
    # Get a list of files in the directory
    files = [
        f for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]
    if not files:
        return None

    # Find the most recently uploaded file by comparing modification times
    most_recent_file = max(
        files, key=lambda f: os.path.getmtime(os.path.join(directory, f)))
    return most_recent_file


def train(title:str,file_path:str):
    '''
    
    :param title: 
    :param file_path: 
    :return:
    models文件夹中出现新的模型文件夹，名为title。
    '''
    upload_url, slug, response_create = create(title,file_path)
    response_trigger = trigger(slug)

    import time

    # 循环直到状态变为 'finished'
    while True:
        status = check(slug)
        if status == 'finished':
            print("已完成")
            break
        else:
            print("等待中...")
            time.sleep(30)  # 暂停 10 秒再检查

    # 继续操作，下载文件，以title为文件名，放置在models文件夹下。
    download(slug)

