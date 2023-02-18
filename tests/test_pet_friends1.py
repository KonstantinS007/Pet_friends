from settings import valid_email, valid_password, no_valid_email, no_valid_password, valid_email2, valid_password2
import os
import requests
import pytest
from api1 import PetFriends
pf = PetFriends()
# import api
# pf = api.PetFriends()

@pytest.fixture(scope="class", autouse=True)
def get_key():
    # переменные email и password нужно заменить своими учетными данными
    response = requests.post(url='https://petfriends.skillfactory.ru/login',
                             data={"email": valid_email, "pass": valid_password})
    assert response.status_code == 200, 'Запрос выполнен неуспешно'
    assert 'Cookie' in response.request.headers, 'В запросе не передан ключ авторизации'
    return response.request.headers.get('Cookie')
    # s = requests.Session()
    # data = {"email": valid_email, "pass": valid_password}
    # url = "https://petfriends.skillfactory.ru/login"
    # response = s.post(url, data=data)
    # return response.request.headers.get('Cookie')


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    #  Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(get_key, filter='my_pets'):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    status, result = pf.get_list_of_pets(get_key, filter)

    assert status == 200
    assert len(result['pets']) > 0
    print(result['pets'])


def test_add_new_pet_with_valid_data(get_key, name='Васька', animal_type='Кот',
                                     age='1', pet_photo='images/Cat.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo

    # Добавляем питомца
    status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)
    _, my_pets = pf.get_list_of_pets(get_key, "my_pets")
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['age'] == age
    assert result['animal_type'] == animal_type
    assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']


def test_update_pet_info(get_key, name='Барсик', animal_type='Вислоух', age='5'):
    """Проверяем возможность изменения данных питомца"""

    _, my_pets = pf.get_list_of_pets(get_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(get_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Питомцы отсутствуют")


def test_successful_delete_self_pet(get_key):
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев

    _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Супер кот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(get_key, "my_pets")
    print(my_pets)    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(get_key, pet_id)
    print(my_pets)
    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(get_key, "my_pets")
    print(my_pets)
    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


# Новые тесты


def test_add_new_pet_with_valid_data_no_foto(get_key, name='Василий', animal_type='Котофей', age='3'):
    """Проверяем что можно добавить питомца с корректными данными без фото"""

    # Добавляем питомца
    status, result = pf.add_new_pet_no_foto(get_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['age'] == age
    assert result['animal_type'] == animal_type


def test_successful_update_self_pet_foto(get_key, pet_photo='images/Cat.jpg'):
    # pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    """Проверяем возможность добавления фото питомца"""

    _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Если список не пустой, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_foto(get_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(get_key, "")
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_successful_update_self_pet_foto_png(get_key, pet_photo='images/Cat1.png'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    """Проверяем возможность добавления фото питомца"""
    _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Если список не пустой, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_foto_png(get_key, my_pets['pets'][0]['id'], pet_photo)

        _, my_pets = pf.get_list_of_pets(get_key, "my_pets")
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# Группа тестов на получения ключа авторизации в разных вариантах валидных и не валидных значений почты и пароля.


def test_get_api_key_for_no_valid_user1(email=no_valid_email, password=no_valid_password):
    """ Проверяем что при невалидном значении почты и пароля нельзя получить ключ,
     запрос api ключа возвращает статус 403
     и в результате не содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert not'key' in result


def test_get_api_key_for_no_valid_user2(email=valid_email, password=no_valid_password):
    """ Проверяем что при невалидном пароле нельзя получить ключ,
     запрос api ключа возвращает статус 403
     и в результате не содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


def test_get_api_key_for_no_valid_user3(email=no_valid_email, password=valid_password):
    """ Проверяем что при невалидной почтой нельзя получить ключ,
     запрос api ключа возвращает статус 403
     и в результате не содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


def test_add_new_pet_with_no_valid_age(get_key, name='Василий', animal_type='Котофей', age='-1'):
    """Проверяем что нельзя добавить питомца с некорректными данными,
    с отрицательным значением возраста"""
    # Добавляем питомца
    status, result = pf.add_new_pet_no_foto(get_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    assert 'name' not in result


def test_successful_delete_self_pet_with_valid_key_stranger_id(get_key):
    """Проверяем возможность по-чужому id удаления питомца
    со своего аккаунта, полученного id непосредственно с чужого аккаунта"""

    # Получаем ключ auth_key и запрашиваем список питомцев 2 аккаунта
    _, auth_key2 = pf.get_api_key(valid_email2, valid_password2)
    _, my_pets = pf.get_list_of_pets1(auth_key2, "my_pets")
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet1(auth_key2, "Супер кот", "кот", "3", "images/Cat2.jpg")
        _, my_pets = pf.get_list_of_pets1(auth_key2, "my_pets")
    # получаем ключ первого аккаунта и через него авторизуемся для удаления

    # Берём id первого питомца из списка 2 аккаунта и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(get_key, pet_id)

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 403
    assert pet_id in my_pets.values()


# Либо что нельзя получить id питомца и его удалить

def test_successful_delete_self_pet_valid_key_stranger_id(get_key):
    """Проверяем возможность получение чужого id со своего аккаунта и с помощью его удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список питомцев 2 аккаунта

    _, my_pets = pf.get_list_of_pets(get_key, filter='my_pets')
    # получаем список животных и узнаем id последнего
    _, all_pets = pf.get_list_of_pets(get_key, filter='')
    n = True
    s = 1
    no_my_id = all_pets['pets'][len(all_pets['pets']) - s]['id']
    while n:  # Пока не найдется id не совпадающий с id авторизованного аккаунта
        if no_my_id not in my_pets.values():
            n = False
        else:
            s = s + 1
            n = True
    status, _ = pf.delete_pet(get_key, no_my_id)
    # Ещё раз запрашиваем список своих питомцев
    _, all_pets = pf.get_list_of_pets(get_key, "")

    # Проверяем что статус ответа неравен 200 и в списке питомцев не удалился по id чужой питомец
    assert status != 200
    assert no_my_id in all_pets.values()


def test_create_pet_simple_with_invalid_data(get_key, name='', animal_type='', age=''):
    """Проверяем что нельзя добавить питомца с пустыми данными (без фото)"""


    status, result = pf.add_new_pet_no_foto(get_key, name, animal_type, age)

    assert status != 200


def test_post_add_pet_no_valid_animal_type(get_key, name='Homa', animal_type='111', age='4'):
    """ Проверяем, что нельзя добавить нового питомца с указанием цифр вместо типа"""

    status, result = pf.add_new_pet_no_foto(get_key, name, animal_type, age)
    assert status != 200
    assert result['animal_type'] == animal_type


def test_post_add_pet_no_valid_age_max(get_key, name='Homa', animal_type='кот', age='999'):
    """ Проверяем, что нельзя добавить нового питомца с указанием слишком большого значения возраста"""

    status, result = pf.add_new_pet_no_foto(get_key, name, animal_type, age)
    assert status != 200
    assert result['age'] == age
