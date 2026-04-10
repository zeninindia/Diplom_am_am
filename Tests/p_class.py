import requests

class ApiPage:
    def __init__(self):
        self.url = "https://api.poiskkino.dev/"
        self.key = 'GH99NQ5-Y6W49WP-QF0T6RT-FRH4YP9'


    def search_movies1(self, name):
        pen = f"{self.url}v1.4/movie/search"
        params = {
            'page': 1,
            'limit': 10,
            'query': name
        }

        headers = {
            'accept': 'application/json',
            'X-API-KEY': self.key
        }

        response = requests.get(pen, params=params, headers=headers)
        response_body = response.json()
        status_code = response.status_code
        return response_body, status_code