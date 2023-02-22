Practice 19-21-22 <img src="https://media.giphy.com/media/M9gbBd9nbDrOTu1Mqx/giphy.gif" width="100"/>
requirements.txt зависимости они же библиотеки (команды запись и загрузка по списку)
pip freeze > requirements.txt  -генерирует файл  requirements.txt , записывая в файл все зависимости с их версиями
pip install -r requirements.txt - устанавливает все зависимости с файла.

report.log файл pytest, если сама библиотека забагует.

Testing_REST_api_PetFriends https://petfriends.skillfactory.ru.

По запросам SWAGGER PetFriends API v1 https://petfriends.skillfactory.ru/apidocs/#.

В файле settings.py расположенном в корневой директории содержится информация валидных и невалидных почте и паролях.

В файле app.py расположенном в корневой директории содержится библиотека к REST api веб сервису PetFriends.

В директории /tests располагается файл с тестами и /images лежат фотографии для теста.

Practice 19.7.2 test_pet_friends19.py; api.py; settings.py.
С классом тестов test_pet_friends_class19cokie.py(c фикстурой автокей и куки-кей conftest.py )

Practice 21 test_pet_friends_fixapi21.py с декораторами запросов составления логов из decorator.py в log.txt
также изменения оберткой апи запросов копии api21.py и запуск в терминале (pytest test_pet_friends_fixapi.py > myoutput.txt)
для записи лога тестирования, фикстурами conftest.py, маркерами pytest.ini (пример запуска pytest test_pet_friends_fixapi.py -v -m "auth" - авторизация тесты)

Practice_22
