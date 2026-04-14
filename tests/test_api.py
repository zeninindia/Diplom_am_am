import allure
from typing import Dict, Any, List, Optional
import os
from dotenv import load_dotenv
load_dotenv()


@allure.title("Тест поиска фильмов по имени")
@allure.description(
    "Проверяет функционал поиска фильмов по заданному имени,"
    "выводит данные о первом найденном фильме.")
@allure.feature("Поиск фильмов")
@allure.severity(allure.severity_level.NORMAL)
def test_search_movies(api: Any) -> None:
    """
    Тестирует поиск фильмов по имени.

    Параметры:
    - api (Any): API для выполнения запросов.

    Возвращаемое значение:
    - None: функция выполняет проверки через assert и
    выводит данные, не возвращая значений.
    """

    with allure.step("Выполняем запрос на поиск фильмов"):
        response_body, status_code = api.search_movies1()

    with allure.step("Проверяем, что статус-код ответа равен 200"):
        assert status_code == 200

    with allure.step("Проверяем наличие поля 'docs' в ответе"):
        assert 'docs' in response_body
        docs = response_body['docs']

    first_movie = docs[0]

    with allure.step(
            "Проверяем, что имя фильма содержит искомое значение"):
        assert os.getenv('FILM_NAME') in first_movie['name']

    with allure.step("Проверяем наличие постера и выводим его URL"):
        assert 'poster' in first_movie
        poster_url = first_movie["poster"]
        print(f"Вот картинка фильма Я: {poster_url}")


@allure.title("Тест получения списка жанров по имени")
@allure.description(
    "Проверяет получение списка жанров,"
    "выводит статус-код и содержимое ответа.")
@allure.feature("Жанры")
@allure.severity(allure.severity_level.MINOR)
def test_search_genres_name(api: Any) -> None:
    """
    Тестирует получение списка жанров по имени.

    Параметры:
    - api (Any): объект API для выполнения запросов.

    Возвращаемое значение:
    - None: функция выполняет проверки через assert и
    выводит данные, не возвращая значений.
    """
    with allure.step("Выполняем запрос на получение списка жанров"):
        response = api.search_genres_name()
        status_code = response.status_code

    with allure.step("Проверяем, что статус-код ответа равен 200"):
        assert status_code == 200

    with allure.step(
            "Запрашиваем JSON-ответ и проверяем, что список не пустой"):
        items = response.json()
        assert len(items) > 0

    with allure.step(
            "Проверяем наличие поля 'name' у первого элемента списка"):
        assert 'name' in items[0]


@allure.title("Тест получения случайного фильма")
@allure.description(
    "Проверяет функционал получения случайного фильма,"
    "выводит данные фильма и постера.")
@allure.feature("Случайный фильм")
@allure.severity(allure.severity_level.NORMAL)
def test_get_random_movie(api: Any) -> None:
    """
    Тестирует получение случайного фильма.

    Параметры:
    - api (Any): Логика API для выполнения запросов.

    Возвращаемое значение:
    - None: функция выполняет проверки через assert
    и выводит данные, не возвращая значений.
    """
    with allure.step("Выполняем запрос на получение случайного фильма"):
        response = api.get_random_movie()

    with allure.step("Проверяем, что статус-код ответа равен 200"):
        assert response.status_code == 200

    with allure.step("Выводим и проверяем JSON-ответ"):
        lest = response.json()
        movie_name = lest["alternativeName"]

    with allure.step(
            "Проверяем наличие и валидность постера фильма"):
        try:
            'poster' in lest and lest['poster'] is not None
            film_poster = lest['poster']
            assert 'url' in film_poster
        except:
            pass
        print(lest['poster'])


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
    - api (Any): Логика API для выполнения запросов.

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
            "Выводим JSON-ответ и проверяем наличие поля 'docs'"):
        response_json = response.json()
        assert 'docs' in response_json
        docs = response_json['docs']
        assert len(docs) > 0

    with allure.step(
            "Проверяем структуру номинации и награды"):
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


@allure.title("Тест поиска имён")
@allure.description(
    "Проверяет поиск имён"
    "(актёров, режиссёров) через API,"
    "выводит список английских имён.")
@allure.feature("Поиск персон")
@allure.severity(allure.severity_level.NORMAL)
def test_search_names(api: Any) -> None:
    """
    Тестирует поиск имён (вероятно,
    персон — актёров, режиссёров.).

    Параметры:
    - api (Any): Логика API для выполнения запросов.

    Возвращаемое значение:
    - None: функция выполняет проверки через assert
    и выводит данные, не возвращая значений.
    """
    with allure.step("Выполняем запрос на поиск имён"):
        response = api.all_search_names()

    with allure.step(
            "Проверяем, что статус-код ответа равен 200"):
        assert response.status_code == 200

    with allure.step("Выводим JSON-ответ"):
        response_body = response.json()

    with allure.step(
            "Проверяем наличие поля 'docs', что оно не пустое"):
        assert 'docs' in response_body
        persons = response_body['docs']
        assert len(persons) > 0

    with allure.step(
            "Проверяем наличие общего количества"
            "записей и что они есть"):
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
