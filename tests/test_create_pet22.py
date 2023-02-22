import os
from api import PetFriends
import pytest
#    pytest test_create_pet22.py


def generate_string(num):
   return "x" * num


def russian_chars():
   return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
# Здесь мы взяли 20 популярных китайских иероглифов


def chinese_chars():
   return '的一是不了人我在有他这为之大来以个中上们'


def special_chars():
   return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'

@pytest.mark.parametrize("name"
   , [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
      special_chars(), '123']
   , ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("animal_type"
   , [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
      special_chars(), '123']
   , ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("age", ['1'], ids=['min'])
class TestClassPetsApi:
    def setup(self):
        self.pf = PetFriends
        self.base_url = "https://petfriends.skillfactory.ru/"

    def test_add_new_pet_with_valid_data(self, auth_key, name='Васька', animal_type='Кот',
                                         age='1', pet_photo='images/Cat.jpg'):
        """Проверяем что можно добавить питомца с корректными данными"""
        # pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Добавляем питомца
        status, result = self.pf.add_new_pet(self, auth_key, name, animal_type, age, pet_photo)
        _, my_pets = self.pf.get_list_of_pets(self, auth_key, "my_pets")
        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
        assert result['age'] == age
        assert result['animal_type'] == animal_type
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']

    def test_update_pet_info1(self, auth_key, name='Барсик', animal_type='Вислоух', age='5'):
        """Проверяем возможность изменения данных питомца"""
        _, my_pets = self.pf.get_list_of_pets(self, auth_key, 'my_pets')

        if len(my_pets['pets']) > 0:
            status, result = self.pf.update_pet_info(self, auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
            assert status == 200
            assert result['name'] == name
        else:
            raise Exception("Питомцы отсутствуют")

    def test_successful_delete_self_pet(self, auth_key):
        """Проверяем возможность удаления питомца"""

        # Получаем ключ auth_key и запрашиваем список своих питомцев
        _, my_pets = self.pf.get_list_of_pets(self, auth_key, "my_pets")

        # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            self.pf.add_new_pet(self, auth_key, "Супер кот", "кот", "3", "images/cat1.jpg")
            _, my_pets = self.pf.get_list_of_pets(self, auth_key, "my_pets")
        print(my_pets)    # Берём id первого питомца из списка и отправляем запрос на удаление
        pet_id = my_pets['pets'][0]['id']
        status, _ = self.pf.delete_pet(self, auth_key, pet_id)
        print(my_pets)
        # Ещё раз запрашиваем список своих питомцев
        _, my_pets = self.pf.get_list_of_pets(self, auth_key, "my_pets")
        print(my_pets)
        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert status == 200
        assert pet_id not in my_pets.values()

    def test_add_new_pet_with_valid_data_no_foto(self, auth_key, name='Василий', animal_type='Котофей', age='3'):
        """Проверяем что можно добавить питомца с корректными данными без фото"""

        # Добавляем питомца
        status, result = self.pf.add_new_pet_no_foto(self, auth_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
        assert result['age'] == age
        assert result['animal_type'] == animal_type

    def test_successful_update_self_pet_foto(self, auth_key, pet_photo='images/Cat.jpg'):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        """Проверяем возможность добавления фото питомца"""
        _, my_pets = self.pf.get_list_of_pets(self, auth_key, "my_pets")

        # Если список не пустой, то пробуем добавить фото
        if len(my_pets['pets']) > 0:
            status, result = self.pf.update_pet_foto(self, auth_key, my_pets['pets'][0]['id'], pet_photo)
            _, my_pets = self.pf.get_list_of_pets(self, auth_key, "my_pets")
            # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
            assert status == 200
            assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
        else:
            # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
            raise Exception("There is no my pets")

    def test_add_new_pet_with_no_valid_age(self, auth_key, name='Василий', animal_type='Котофей', age='-1'):
        """Проверяем что нельзя добавить питомца с некорректными данными,
        с отрицательным значением возраста"""
        # Добавляем питомца
        status, result = self.pf.add_new_pet_no_foto(self, auth_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 403
        assert 'name' not in result
