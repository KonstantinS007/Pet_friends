from settings import valid_email, valid_password
import requests
import json
import os
import pytest
from api0 import PetFriends
from datetime import datetime
from requests_toolbelt.multipart.encoder import MultipartEncoder
@pytest.fixture(autouse=True)
def get_key():
    # переменные email и password нужно заменить своими учетными данными
    # response = requests.post(url='https://petfriends.skillfactory.ru/login',
    #                          data={"email": valid_email, "pass": valid_password})
    # assert response.status_code == 200, 'Запрос выполнен неуспешно'
    # assert 'Cookie' in response.request.headers, 'В запросе не передан ключ авторизации'
    # return response.request.headers.get('Cookie')
    s = requests.Session()
    data = {"email": valid_email, "pass": valid_password}
    url = "https://petfriends.skillfactory.ru/login"
    r = s.post(url, data=data)
    return r.request.headers.get('Cookie')


def test_get(get_key):
    data = MultipartEncoder(
                 fields={
                         'name': 'name',
                          'animal_type': 'animal_type',
                          'age': 'age'
                         })
    headers = {"Cookie": get_key, 'Content-Type': data.content_type}
    base_url = "https://petfriends.skillfactory.ru/"
    res = requests.post(base_url + 'api/create_pet_simple', headers=headers, data=data)
    status = res.status_code
    result = ""
    try:
        result = res.json()
    except json.decoder.JSONDecodeError:
        result = res.text
    print(result)
    print(status)
