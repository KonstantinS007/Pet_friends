from settings import valid_email, valid_password
import requests
import os
import pytest
from api0 import PetFriends
from datetime import datetime
# import api
# pf = api.PetFriends()


@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    print(f"\nТест шел: {end_time - start_time}")


@pytest.fixture(scope="class", autouse=True)
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
    response = s.post(url, data=data)
    return response.request.headers.get('Cookie')


class TestClassPets:
    def setup(self):
        self.pf = PetFriends
        self.base_url = "https://petfriends.skillfactory.ru/"

    # def test_get_api_key_for_valid_user(self, email=valid_email, password=valid_password):
    #     """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    #
    #     # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    #     status, result = self.pf.get_api_key(self, email, password)
    #     #  Сверяем полученные данные с нашими ожиданиями
    #     assert status == 200
    #     assert 'key' in result

    def test_get_all_pets_with_valid_key(self, get_key, filter='my_pets'):
        """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """

        status, result = self.pf.get_list_of_pets(self, get_key, filter)

        assert status == 200
        assert len(result['pets']) > 0
        print(result['pets'])

    def test_add_new_pet_with_valid_data(self, get_key, name='Васька', animal_type='Кот',
                                         age='1', pet_photo='images/Cat.jpg'):
        """Проверяем что можно добавить питомца с корректными данными"""
        # pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Добавляем питомца
        status, result = self.pf.add_new_pet(self, get_key, name, animal_type, age, pet_photo)
        _, my_pets = self.pf.get_list_of_pets(self, get_key, "my_pets")
        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
        assert result['age'] == age
        assert result['animal_type'] == animal_type
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']


    def test_update_pet_info(self, get_key, name='Барсик', animal_type='Вислоух', age='5'):
        """Проверяем возможность изменения данных питомца"""
        _, my_pets = self.pf.get_list_of_pets(self, get_key, 'my_pets')

        if len(my_pets['pets']) > 0:
            status, result = self.pf.update_pet_info(self, get_key, my_pets['pets'][0]['id'], name, animal_type, age)
            assert status == 200
            assert result['name'] == name
        else:
            raise Exception("Питомцы отсутствуют")
#
#
#     def test_successful_delete_self_pet(self, get_key):
#         """Проверяем возможность удаления питомца"""
#
#         # Получаем ключ auth_key и запрашиваем список своих питомцев
#         _, my_pets = self.pf.get_list_of_pets(self, get_key, "my_pets")
#
#         # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
#         if len(my_pets['pets']) == 0:
#             self.pf.add_new_pet(self, get_key, "Супер кот", "кот", "3", "images/cat1.jpg")
#             _, my_pets = self.pf.get_list_of_pets(self, get_key, "my_pets")
#         print(my_pets)    # Берём id первого питомца из списка и отправляем запрос на удаление
#         pet_id = my_pets['pets'][0]['id']
#         status, _ = self.pf.delete_pet(self, get_key, pet_id)
#         print(my_pets)
#         # Ещё раз запрашиваем список своих питомцев
#         _, my_pets = self.pf.get_list_of_pets(self, get_key, "my_pets")
#         print(my_pets)
#         # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
#         assert status == 200
#         assert pet_id not in my_pets.values()
#
#
# # Новые тесты
#
#
    def test_add_new_pet_with_valid_data_no_foto(self, get_key, name='Василий', animal_type='Котофей', age='3'):
        """Проверяем что можно добавить питомца с корректными данными без фото"""

        # Добавляем питомца
        status, result = self.pf.add_new_pet_no_foto(self, get_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
        assert result['age'] == age
        assert result['animal_type'] == animal_type
#
#
#     def test_successful_update_self_pet_foto(self, get_key, pet_photo='images/Cat.jpg'):
#         pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
#         """Проверяем возможность добавления фото питомца"""
#         _, my_pets = self.pf.get_list_of_pets(self, get_key, "my_pets")
#
#         # Если список не пустой, то пробуем добавить фото
#         if len(my_pets['pets']) > 0:
#             status, result = self.pf.update_pet_foto(self, get_key, my_pets['pets'][0]['id'], pet_photo)
#             _, my_pets = self.pf.get_list_of_pets(self, get_key, "my_pets")
#             # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
#             assert status == 200
#             assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
#         else:
#             # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
#             raise Exception("There is no my pets")
#
#
#     def test_successful_update_self_pet_foto_png(self, get_key, pet_photo='images/Cat1.png'):
#         pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
#         """Проверяем возможность добавления фото питомца"""
#         # Получаем ключ auth_key и список своих питомцев
#         _, auth_key = self.pf.get_api_key(self, valid_email, valid_password)
#         _, my_pets = self.pf.get_list_of_pets(self, get_key, "my_pets")
#
#         # Если список не пустой, то пробуем добавить фото
#         if len(my_pets['pets']) > 0:
#             status, result = self.pf.update_pet_foto_png(self, get_key, my_pets['pets'][0]['id'], pet_photo)
#
#             _, my_pets = self.pf.get_list_of_pets(self, get_key, "my_pets")
#             # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
#             assert status == 200
#             assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
#         else:
#             # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
#             raise Exception("There is no my pets")
#
#
#     def test_add_new_pet_with_no_valid_age(self, get_key, name='Василий', animal_type='Котофей', age='-1'):
#         """Проверяем что нельзя добавить питомца с некорректными данными,
#         с отрицательным значением возраста"""
#         # Добавляем питомца
#         status, result = self.pf.add_new_pet_no_foto(self, get_key, name, animal_type, age)
#
#         # Сверяем полученный ответ с ожидаемым результатом
#         assert status == 200
#         assert 'name' not in result
#
#
#     def test_create_pet_simple_with_invalid_data(self, get_key, name='', animal_type='', age=''):
#         """Проверяем что нельзя добавить питомца с пустыми данными (без фото)"""
#
#         _, auth_key = self.pf.get_api_key(self, valid_email, valid_password)
#         status, result = self.pf.add_new_pet_no_foto(self, get_key, name, animal_type, age)
#
#         assert status == 200
#
#
#     def test_post_add_pet_no_valid_animal_type(self, get_key, name='Homa', animal_type='111', age='4'):
#         """ Проверяем, что нельзя добавить нового питомца с указанием цифр вместо типа"""
#         status, result = self.pf.add_new_pet_no_foto(self, get_key, name, animal_type, age)
#         assert status == 200
#         assert result['animal_type'] == animal_type
#
#
#     def test_post_add_pet_no_valid_age_max(self, get_key, name='Homa', animal_type='кот', age='999'):
#         """ Проверяем, что нельзя добавить нового питомца с указанием слишком большого значения возраста"""
#         status, result = self.pf.add_new_pet_no_foto(self, get_key, name, animal_type, age)
#         assert status == 200
#         assert result['age'] == age
