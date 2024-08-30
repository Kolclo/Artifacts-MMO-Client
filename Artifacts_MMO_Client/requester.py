from credentials import api_token
import requests

url = "https://api.artifactsmmo.com/"
headers: str = {
    "Accept": "application/json",
    "Authorization": f"Bearer {api_token['token']}",
    "Content-Type": "application/json"
}


class APIRequester:
    def __init__(self, requests_module: requests = requests) -> None:
        self.requests_module: requests = requests_module

    def get(self, endpoint: str) -> dict[str, str]:
        response: requests.Response = self.requests_module.get(
            f"{url}{endpoint}", 
            headers=headers
            )
        
        return response.json()

    def post(self, endpoint: str, data: dict[str, str]) -> dict[str, str]:
        response: requests.Response = self.requests_module.post(
            f"{url}{endpoint}", 
            headers=headers, 
            json=data
            )
        
        return response.json()