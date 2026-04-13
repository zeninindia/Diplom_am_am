import requests
import os
from dotenv import load_dotenv
import allure

load_dotenv()


class ApiPage:
    """
    Класс для взаимодействия с API киносервиса.
    Предоставляет методы для поиска фильмов,
    получения жанров, случайных фильмов,
    номинаций и персон (актёров, режиссёров и т. д.).
    """

    def __init__(self, url: str | None) -> None:
        """
        Инициализация экземпляра класса ApiPage.

        Параметры:
        - url (str | None): базовый URL API. Если None,
        берётся из переменной окружения URL.

        Атрибуты экземпляра:
        - self.url (str): базовый URL API;
        - self.key (str | None): API‑ключ из переменной окружения KEY;
        - self.headers (dict): заголовки для запросов, включая API‑ключ.
        """
        self.url = url or os.getenv("URL")
        self.key = os.getenv("KEY")
        self.headers = {
            'accept': 'application/json',
            'X-API-KEY': self.key
        }

    @allure.step("Поиск фильмов по названию")
    def search_movies1(self) -> tuple[dict, int]:
        """
        Поиск фильмов по названию.

        Параметры:
        - name (str): название фильма для поиска
        (в текущей реализации не используется —
          вместо него берётся значение из переменной окружения FILM_NAME).

        Возвращает:
        - tuple[dict, int]: кортеж из:
          - тела ответа в формате JSON (dict);
          - кода статуса HTTP‑ответа (int).
        """
        with allure.step(f"Формирование URL для поиска фильмов:"
                         f"{self.url}v1.4/movie/search"):
            pen = f"{self.url}v1.4/movie/search"

        with allure.step("Подготовка параметров запроса"):
            params = {
                'page': 1,
                'limit': 10,
                'query': os.getenv("FILM_NAME")
            }

        with allure.step("Отправка GET‑запроса для поиска фильмов"):
            response = requests.get(pen, params=params, headers=self.headers)

        with allure.step("Парсинг ответа и получение статуса"):
            response_body = response.json()
            status_code = response.status_code

        return response_body, status_code

    @allure.step("Получение возможных значений для поля 'genres.name'")
    def search_genres_name(self) -> requests.Response:
        """
        Получение списка возможных значений для поля genres.name
        (жанры фильмов).

        Параметры: отсутствуют.

        Возвращает:
        - requests.Response: объект ответа от сервера
        (без предварительной обработки).
        """
        with allure.step("Установка URL для запроса жанров"):
            pen_url = f"{self.url}/v1/movie/possible-values-by-field"

        with allure.step(
                "Подготовка параметра запроса:"
                "field='genres.name'"):
            params = {
                'field': 'genres.name'
            }

        with allure.step("Отправка GET‑запроса для получения жанров"):
            response = requests.get(
                pen_url, headers=self.headers, params=params)

        return response

    @allure.step("Получение случайного фильма")
    def get_random_movie(self) -> requests.Response:
        """
        Получение данных о случайном фильме из базы.

        Параметры: отсутствуют.

        Возвращает:
        - requests.Response:
        объект ответа от сервера с данными о фильме.
        """
        with allure.step(
                f"Формирование URL для получения случайного фильма:"
                f"{self.url}v1.4/movie/random"):
            pen = f"{self.url}v1.4/movie/random"

        with allure.step(
                "Отправка GET‑запроса для получения случайного фильма"):
            response = requests.get(pen, headers=self.headers)

        return response

    @allure.step("Поиск номинаций и наград")
    def search_nominations(self) -> requests.Response:
        """
        Поиск информации о номинациях и наградах фильмов.

        Параметры: отсутствуют.

        Возвращает:
        - requests.Response:
        объект ответа от сервера с информацией о номинациях.
        """
        with allure.step(
                f"Формирование URL для поиска номинаций:"
                f"{self.url}v1.4/movie/awards"):
            pen = f"{self.url}v1.4/movie/awards"

        with allure.step("Отправка GET‑запроса для получения номинаций"):
            response = requests.get(pen, headers=self.headers)

        return response

    @allure.step("Поиск персон (актёров, режиссёров и т. д.)")
    def all_search_names(self) -> requests.Response:
        """
        Поиск персон: актёров, режиссёров,
        сценаристов и других участников кинопроизводства.

        Параметры: отсутствуют.

        Возвращает:
        - requests.Response:
        объект ответа от сервера с результатами поиска персон.
        """
        with allure.step(
                f"Формирование URL для поиска персон:"
                f"{self.url}v1.4/person/search"):
            pen = f"{self.url}v1.4/person/search"

        with allure.step("Отправка GET‑запроса для поиска персон"):
            response = requests.get(pen, headers=self.headers)
            return response
