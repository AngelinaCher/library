import json
import requests


class LibraryAPI:
    """ Получение данные из API """
    BASE_URL = 'https://json.medrocket.ru/library'

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def get_data(self) -> json:
        url = f'{self.BASE_URL}/{self.endpoint}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_message = {
                "error": f"Ошибка при запросе к {url}",
                "details": str(e)
            }
            return json.dumps(error_message)
