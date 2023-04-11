import functools


def edit_data(json):  # Укорачивает запись значений в лог
    try:
        list_of_pets = json["pets"]
    except KeyError:
        list_of_pets = [json]
    for i in list_of_pets:
        if len(i["pet_photo"]) > 5:
            i["pet_photo"] = i["pet_photo"][:5]
        if len(i["age"]) > 4:
            i['age'] = i['age'][:4]
        if len(i["animal_type"]) > 10:
            i['animal_type'] = i['animal_type'][:10]
        if len(i["name"]) > 10:
            i['name'] = i['name'][:10]
    return json


def post_api_log(func):
    def wrapper(*args, **kwargs):
        with open('log.txt', 'a', encoding="UTF-8") as f:
            print("Request--------------------------------", file=f)
            print(f"Doing POST request to {args[0]}", file=f)
            try:
                print(f"Path parameters: {kwargs['params']}", file=f)
            except KeyError:
                print(f"No path parameters")
            print(f"Headers of request: {kwargs['headers']}", file=f)
            data_repr = repr(kwargs['data'])
            print(f"Request body: {data_repr}", file=f)
            value = func(*args, **kwargs)
            print("Response---------------------------------", file=f)
            response_code = repr(value)[10:-1]
            print(f"Code of answer to response - {response_code}", file=f)
            if value.status_code != 200:
                print(f"Response body: {value.text}")
            else:
                try:
                    print(f"Response body: {edit_data(value.json())}", file=f)
                except KeyError:
                    print(f"Response body: {value.json()}", file=f)

            return value
    print("  ")
    print("  ")
    return wrapper


def get_api_log(func):
    def wrapper(*args, **kwargs):
        with open('log.txt', 'a', encoding="UTF-8") as f:
            print("Request--------------------------", file=f)
            print(f"Запрос GET {args[0]}", file=f)
            try:
                print(f"Parameters of path: {kwargs['params']}", file=f)
            except KeyError:
                print(f"Query parameter is not provided.", file=f)
            print(f"Headers of request: {kwargs['headers']}", file=f)
            value = func(*args, **kwargs)
            print("Response------------------------------", file=f)
            response_code = repr(value)
            print(f"Код ответа - {response_code}", file=f)
            if value.status_code != 200:
                print(f"Ответ body: {value.text}", file=f)
            else:
                try:
                    print(f"Ответ body: {edit_data(value.json())}", file=f)
                except KeyError:
                    print(f"Ответ body: {value.json()}", file=f)
            return value
    print("  ")
    print("  ")
    return wrapper


def put_api_log(func, path='/some_default_path'):
    def wrapper(*args, **kwargs):
        with open('log.txt', 'a', encoding="UTF-8") as f:
            print("Request---------------------------------", file=f)
            print(f"Что изменили {args[0]}", file=f)
            print(f"Headers of request: {kwargs['headers']}", file=f)
            print(f"Parameters of request path pet_id: {kwargs['path']}", file=f)
            data_repr = repr(kwargs['data'])
            print(f"Ответ body: {data_repr}", file=f)
            value = func(*args, **kwargs)
            print(value)
            print("Response--------------------------------------", file=f)
            response_code = repr(value)
            print(f"Код ответа - {response_code}", file=f)
            if value.status_code != 200:
                print(f"Ответ body: {value.text}", file=f)
            else:
                try:
                    print(f"Ответ body: {edit_data(value.json())}", file=f)
                except KeyError:
                    print(f"Ответ body: {edit_data(value.json())}", file=f)

            return value
    print("  ")
    print("  ")
    return wrapper


def delete_api_log(func, path='/some_default_path'):
    def wrapper(*args, **kwargs):
        with open('log.txt', 'a', encoding="Windows-1251") as f:
            print("Request-----------------------------------------")
            print(f"Что удаленно {args[0]}", file=f)
            print(f"Headers: {kwargs['headers']}", file=f)
            print(f"Parameter of path request pet_id: {kwargs['path']}", file=f)
            value = func(*args, **kwargs)  # *args, **kwargs
            print("Response-------------------------------------------")
            response_code = repr(value)
            print(f"Код ответа- {response_code}", file=f)
            return value
    print("  ")
    return wrapper


def log_api(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        status = str(value[0])
        result = str(value[1])
        request = str(value[2:4])
        responce_headers = str(value[4:])
        with open('log.txt', 'a', encoding='utf8') as f:
            f.write(f'''Информация запроса:
------------------
Статус запроса:
{status}
Параметры запроса:
{request}
Информация ответа:
------------------
Тело ответа:
{result}
Заголовок ответа:
{responce_headers}''')

    print("  ")
    print("  ")
    return wrapper


def generate_string(n):
   return "x" * n

def russian_chars():
   return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def chinese_chars():
   return '的一是不了人我在有他这为之大来以个中上们'


def special_chars():
   return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'
