from settings import valid_email, valid_password, no_valid_email, no_valid_password
from api import PetFriends

#    pytest test_get_pet22.py


class TestClassPetsGetAPI:
    def setup(self):
        self.pf = PetFriends
        self.base_url = "https://petfriends.skillfactory.ru/"

    def test_get_api_key_for_valid_user(self, email=valid_email, password=valid_password):
        """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = self.pf.get_api_key(self, email, password)
        #  Сверяем полученные данные с нашими ожиданиями
        assert status == 200
        assert 'key' in result

    def test_get_api_key_for_no_valid_user1(self, email=no_valid_email, password=no_valid_password):
        """ Проверяем что при невалидном значении почты и пароля нельзя получить ключ,
         запрос api ключа возвращает статус 403
         и в результате не содержится слово key"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = self.pf.get_api_key(self, email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403
        assert not'key' in result

    def test_get_all_pets_with_valid_key(self, get_key, filter='my_pets'):
        """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """

        status, result = self.pf.get_list_of_pets_cookie(self, get_key, filter)

        assert status == 200
        assert len(result['pets']) > 0
        print(result['pets'])

    def test_get_all_pets_with_valid_key(self, auth_key, filter='my_pets'):
        """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """

        status, result = self.pf.get_list_of_pets(self, auth_key, filter)

        assert status == 200
        assert len(result['pets']) > 0
        print(result['pets'])

