import json
import numpy as np
import requests

DROPBOX_KEY = '' #leave empty
DROPBOX_APP_KEY = '' #hide
DROPBOX_SECRET = '' #hide

NOTION_SECRET='' #hide

def get_dropbox_token():
    print(f'Go to this website and get the key: https://www.dropbox.com/oauth2/authorize?client_id={DROPBOX_APP_KEY}&response_type=code&token_access_type=offline')
    key = input('Paste the key: ')
    print(key)
    url = "https://api.dropboxapi.com/2/auth/token/from_oauth1"
    data = {
        'code': key,
        'grant_type': 'authorization_code',
    }

    response = requests.post('https://api.dropbox.com/oauth2/token', data=data, auth=(DROPBOX_APP_KEY, DROPBOX_SECRET))
    r = response.json()
    print(r)
    return(r['access_token'])


def get_database():
    url = "https://api.notion.com/v1/databases/d38aec3936034f85890193f22cc287c4"

    headers = {
        'authorization': f'Bearer {NOTION_SECRET}',
        "accept": "application/json",
        "Notion-Version": "2022-06-28"
    }

    response = requests.get(url, headers=headers)

    print('Retrieved database: ' + response.text)

    return response

def create_page(link, tag, name):
    print("CREATING THE PAGE")
    url = "https://api.notion.com/v1/pages"
    database_id = 'd38aec3936034f85890193f22cc287c4'
    print("Sending url: " + link)

    payload = {
        "parent": {
            "database_id": database_id
        },
        "properties": {
            "Name": {
                "title": [
                            {
                            "text": {
                                "content": name
                            }
                        }
                    ]
            },
            "Tags":{
                "multi_select":[
                    {
                    "name": tag
                    }
                ]
            },
            "URL": {
                "url": link
            }
    }}

    headers = {
        'authorization': f'Bearer {NOTION_SECRET}',
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    print(response.text)


def list_folder():
    print("LISTING FOLDERS")
    url = "https://api.dropboxapi.com/2/files/list_folder"

    headers = {
        "Authorization": f"Bearer {DROPBOX_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "path": "/ReMarkable",
        "recursive": True
    }
    r = requests.post(url, headers=headers, data=json.dumps(data))
    return r

def check_for_tag(path):
    
    url = "https://api.dropboxapi.com/2/files/tags/get"

    headers = {
        "Authorization": f"Bearer {DROPBOX_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "paths": [path]
    }

    r = requests.post(url, headers=headers, data=json.dumps(data))
    
    _r = r.json()
    print(_r)
    if(len(_r['paths_to_tags'][0]['tags']) > 0):
        if(_r['paths_to_tags'][0]['tags'][0]['tag_text'] == 'synced'):
            return False
    return True


def not_already_synced(file):
    path = file['path_lower']
    return check_for_tag(path)

def should_sync(folder_content):
    print("FINDING NOT SYNCED PAGES")
    pages_to_sync = []
    print(f'Retrieved folder {folder_content}')
    for i in range(len(folder_content['entries'])):
        if(folder_content['entries'][i]['.tag'] == 'file'):
            if(not_already_synced(folder_content['entries'][i]) == True):
                pages_to_sync.append(folder_content['entries'][i])
    return pages_to_sync

def where_to_sync(file):
    print("FINDING THE TAG")
    path = file['path_lower']
    split_path = path.split('/')
    return split_path[2], split_path[3]

def get_link_to_share(extra_path):
    print("GETTING THE LINK FOR THE PAGE")

    url = "https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings"

    headers = {
        "Authorization": f"Bearer {DROPBOX_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "path": f"/remarkable/{extra_path}"
    }

    r = requests.post(url, headers=headers, data=json.dumps(data))
    file = r.json()
    if("error" in file):
        return(file['error']['shared_link_already_exists']['metadata']['url'])
    else:
        return(file['url'])

#def read_file():
#    text_file = open("refresh_key.txt", "r")
#    text = text_file.read()
#    text_file.close()
#    return text

#def save_in_file(text):
#    text_file = open("refresh_key.txt", "w")
#    n = text_file.write(text)
#    text_file.close()

def update_key():
    key = get_dropbox_token()
    return key

def mark_synced(path):
    url = "https://api.dropboxapi.com/2/files/tags/add"

    headers = {
        "Authorization": f"Bearer {DROPBOX_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "path": f"/remarkable/{path}",
        "tag_text": "synced"
    }

    r = requests.post(url, headers=headers, data=json.dumps(data))
    print(r.text)

def sync_all(files):
    print("STARTING SYNC")
    for i in range(len(files)):
        place_to_sync, file_name = where_to_sync(files[i])
        _name = file_name
        _name = _name.replace('.pdf', '')
        file_path = f"{place_to_sync}/{file_name}"
        share_link = get_link_to_share(file_path)
        mark_synced(file_path)
        create_page(share_link, place_to_sync, _name)


DROPBOX_KEY = update_key()

folder_content = list_folder().json()

files_to_sync = should_sync(folder_content)
if(len(files_to_sync) > 0):
    sync_all(files_to_sync)
else:
    print("No files to sync")


