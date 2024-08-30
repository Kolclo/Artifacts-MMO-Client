from credentials import api_token
import requests


class APIRequester:
    def __init__(self, requests_module: requests = requests) -> None:
        self.requests_module: requests = requests_module
        self.url = "https://api.artifactsmmo.com/"
        self.headers: str = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_token['token']}",
            "Content-Type": "application/json"
}

    def get(self, endpoint: str, params: dict[str, str] = {}) -> dict[str, str]:
        response: requests.Response = self.requests_module.get(
            f"{self.url}{endpoint}",
            headers=self.headers,
            params=params
        )
        
        return response.json()

    def post(self, endpoint: str, data: dict[str, str]) -> dict[str, str]:
        response: requests.Response = self.requests_module.post(
            f"{self.url}{endpoint}", 
            headers=self.headers, 
            json=data
            )
        
        return response.json()