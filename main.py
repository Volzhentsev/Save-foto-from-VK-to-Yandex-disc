import json
import requests
import time
from tqdm import tqdm
from pprint import pprint

class VKUser:
    url = 'https://api.vk.com/method/'
    def __init__(self, vk_token, version):
        self.params = {
            'access_token': vk_token,
            'v': version
        }

    def get_foto(self, user_id):
        foto_url = self.url + 'photos.get'
        foto_params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': 'likes',
            'photo_sizes': 1,
            'count': 10
        }
        req = requests.get(foto_url, params={**self.params, **foto_params}).json()
        foto = {}
        req = req['response']['items']
        print('Фотографии скачены с VK:')
        for el in tqdm(req):
            time.sleep(1)
            if str(el['likes']['count']) in foto:
                foto[str(el['likes']['count']) +'-' + str(el['date'])] = str(el['sizes'][-1]['url']), str(el['sizes'][-1]['type'])
            else:
                foto[str(el['likes']['count'])] = str(el['sizes'][-1]['url']), str(el['sizes'][-1]['type'])
        return foto

def get_info_file(dict):
    info_file = []
    for k, v in tqdm(dict.items()):
        time.sleep(1)
        info_file.append({'file_name': k, 'size': v[1]})
    print(info_file)
    with open('info.json', 'w') as f:
        json.dump(info_file, f, ensure_ascii=False, indent=2)
    print('\nЗагружена информация по фотографиям в файл info.json с результатами')

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def create_folder(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {
            'path': 'course_py46_1'
        }
        requests.put(url=url, headers=self.get_headers(), params=params)
        print('\nСоздана папка course_py46_1 на Yandex.disk')

    def upload(self, foto_dict):
        for k, v in tqdm(foto_dict.items()):
            time.sleep(1)
            url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
            headers = self.get_headers()
            params = {"path": "/course_py46_1/" + k + ".jpg",
                      "url": v[0],
                      "overwrite": "true"}
            response = requests.post(url=url, headers=headers, params=params)
            res = response.json()
            if response.status_code != 202:
                print(f'Ошибка. Код ошибки: {response.status_code}')
        print(res)
        print('\nФотографии загружены на Yandex.disk')

if __name__ == '__main__':
    user_id = input('Введите id пользователя VK: ')
    ya_token = input('Введите token полигона Yandex: ')
    vk_client_photo = VKUser('958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008', '5.131')
    i = vk_client_photo.get_foto(user_id)
    pprint(i)
    get_info_file(i)
    uploader = YaUploader(ya_token)
    uploader.create_folder()
    uploader.upload(i)
