import json
import requests
from typing import Dict


class APIHandler:

    def get(self, url: str, params: Dict | None = None, headers: Dict | None = None):
        try:
            response = requests.get(url=url, params=params, headers=headers)
            if response.status_code >= 300:
                raise Exception(response.text)
            else:
                return response.json()

        except Exception as e:
            raise e

    def post(self, url: str, body: Dict, params: Dict | None = None, headers: Dict | None = None):
        try:
            body = json.dumps(body)  # to convert the dict from one quote into 2 quotes
            response = requests.post(url=url, data=body, params=params, headers=headers)
            if response.status_code >= 300:
                raise Exception(response.text)
            else:
                return response.json()

        except Exception as e:
            raise e

    def put(self, url: str, body: Dict, params: Dict | None = None, headers: Dict | None = None):
        pass

    def delete(self, url: str, body: Dict, params: Dict | None = None, headers: Dict | None = None):
        pass
