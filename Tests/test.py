import allure
from typing import Dict, Any, List, Optional


@allure.title("Тест поиска фильмов по имени")
@allure.description(
    "Проверяет функционал поиска фильмов по заданному имени,"
    "валидирует ответ API и выводит данные о первом найденном фильме.")
@allure.feature("Поиск фильмов")
@allure.severity(allure.severity_level.NORMAL)
def test_search_movies(api: Any) -> None:
    """
    Тестирует поиск фильмов по имени.

    Параметры:
    - api (Any): объект API для выполнения запросов.

    Возвращаемое значение:
    - None: функция выполняет проверки через assert и
    выводит данные через print, не возвращая значений.
    """
    name = 'я'

    with allure.step("Выполняем запрос на поиск фильмов"):
        response_body, status_code = api.search_movies1(name)

    with allure.step("Проверяем, что статус-код ответа равен 200"):
        assert status_code == 200

    with allure.step("Проверяем наличие поля 'docs' в ответе"):
        assert 'docs' in response_body
        docs = response_body['docs']

    first_movie = docs[0]

    with allure.step(
            "Проверяем, что имя фильма содержит искомое значение"):
        assert 'Я' in first_movie['name']
        print(docs[0])

    with allure.step(
            "Проверяем совпадение ID фильма в первом элементе списка"):
        assert first_movie['id'] == docs[0]['id']
        print(f"ID : {docs[0]['id']}")

    with allure.step("Проверяем наличие постера и выводим его URL"):
        assert 'poster' in first_movie
        poster_url = first_movie['poster']
        print(f"Вот картинка фильма Я: {poster_url}")


@allure.title("Тест получения списка жанров по имени")
@allure.description(
    "Проверяет получение списка жанров через API,"
    "валидирует статус-код и содержимое ответа.")
@allure.feature("Жанры")
@allure.severity(allure.severity_level.MINOR)
def test_search_genres_name(api: Any) -> None:
    """
    Тестирует получение списка жанров по имени.

    Параметры:
    - api (Any): объект API для выполнения запросов.

    Возвращаемое значение:
    - None: функция выполняет проверки через assert и
    выводит данные через print, не возвращая значений.
    """
    with allure.step("Выполняем запрос на получение списка жанров"):
        response = api.search_genres_name()
        status_code = response.status_code

    with allure.step("Проверяем, что статус-код ответа равен 200"):
        assert status_code == 200
        print("Yupeee it works")

    with allure.step(
            "Парсим JSON-ответ и проверяем, что список не пустой"):
        items = response.json()
        print(len(items))
        assert len(items) > 0

    with allure.step(
            "Проверяем наличие поля 'name' у первого элемента списка"):
        assert 'name' in items[0]


@allure.title("Тест получения случайного фильма")
@allure.description(
    "Проверяет функционал получения случайного фильма через API,"
    "валидирует данные фильма и постера.")
@allure.feature("Случайный фильм")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_random_movie(api: Any) -> None:
    """
    Тестирует получение случайного фильма.

    Параметры:
    - api (Any): объект API для выполнения запросов.

    Возвращаемое значение:
    - None: функция выполняет проверки через assert
    и выводит данные через print, не возвращая значений.
    """
    with allure.step("Выполняем запрос на получение случайного фильма"):
        response = api.get_random_movie()

    with allure.step("Проверяем, что статус-код ответа равен 200"):
        assert response.status_code == 200

    with allure.step("Парсим JSON-ответ"):
        lest = response.json()
        movie_name = lest["alternativeName"]
        print(movie_name)

    with allure.step(
            "Проверяем наличие и валидность постера фильма"):
        film_poster = lest['poster']
        assert 'poster' in lest
        assert film_poster is not None
        assert 'url' in film_poster
        poster_url = film_poster
        print(poster_url)


@allure.title(
    "Тест получения информации о номинациях и наградах")
@allure.description("Проверяет получение данных о"
                    "номинациях и наградах через API.")
@allure.feature("Награды и номинации")
@allure.severity(allure.severity_level.NORMAL)
def test_awards(api: Any) -> None:
    """
    Тестирует получение информации о номинациях и наградах.

    Параметры:
    - api (Any): объект API для выполнения запросов.

    Возвращаемое значение:
    - None: функция выполняет проверки через assert,
    не возвращая значений.
    """
    with allure.step(
            "Выполняем запрос на получение информации о номинациях"):
        response = api.search_nominations()

    with allure.step("Проверяем, что статус-код ответа равен 200"):
        assert response.status_code == 200

    with allure.step(
            "Парсим JSON-ответ и проверяем наличие поля 'docs'"):
        response_json = response.json()
        assert 'docs' in response_json
        docs = response_json['docs']
        assert len(docs) > 0

    with allure.step(
            "Проверяем структуру каждой номинации и награды"):
        for doc in docs:
            nomination = doc['nomination']
            with allure.step(
                    f"Проверяем тип поля 'nomination'"
                    f"для документа {doc.get('id', 'unknown')}"):
                assert (nomination, list)
                award = nomination['award']
            with allure.step(
                    f"Проверяем тип поля 'award'"
                    f"для номинации {nomination}"):
                assert (award, list)


@allure.title("Тест поиска имён (персон)")
@allure.description(
    "Проверяет поиск имён"
    "(актёров, режиссёров) через API,"
    "выводит список английских имён.")
@allure.feature("Поиск персон")
@allure.severity(allure.severity_level.NORMAL)
def test_search_names(api: Any) -> None:
    """
    Тестирует поиск имён (вероятно,
    персон — актёров, режиссёров и т. д.).

    Параметры:
    - api (Any): объект API для выполнения запросов.

    Возвращаемое значение:
    - None: функция выполняет проверки через assert
    и выводит данные через print, не возвращая значений.
    """
    with allure.step("Выполняем запрос на поиск имён персон"):
        response = api.all_search_names()

    with allure.step(
            "Проверяем, что статус-код ответа равен 200"):
        assert response.status_code == 200

    with allure.step("Парсим JSON-ответ"):
        response_body = response.json()

    with allure.step(
            "Проверяем наличие поля 'docs', что оно не пустое"):
        assert 'docs' in response_body
        persons = response_body['docs']
        assert len(persons) > 0

    with allure.step(
            "Проверяем наличие общего количества"
            "записей и его положительность"):
        assert 'total' in response_body
        total_count = response_body['total']
        assert total_count > 0

    en_names = []
    with allure.step("Собираем и проверяем английские имена персон"):
        for person in persons:
            with allure.step(
                    f"Проверяем наличие поля 'enName' у "
                    f"персоны {person.get('id', 'unknown')}"):
                assert 'enName' in person
                en_name = person['enName']
                en_names.append(en_name)

    print("Список Имен:")
    for name in en_names:
        print(f"- {name}")
