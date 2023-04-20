import requests
from config import API_URL, API_KEY

class ExtractFromAPI:
    def __init__(self, key, list_id):
        self.key = key
        self.list_id = list_id

    def api_request_get_clickup(self):
        self.response = requests.get(API_URL.format(list_id=self.list_id), headers={'Authorization': API_KEY})

    def data_obtained(self):
        data = self.response.json()
        return data
