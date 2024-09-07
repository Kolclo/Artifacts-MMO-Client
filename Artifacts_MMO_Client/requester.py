from credentials import api_token
import requests
from requests.exceptions import JSONDecodeError


class SendRequest:
    def __init__(self, requests_module: requests = requests) -> None:
        """
        Initialises a new instance of the SendRequest class.

        Args:
            requests_module: The requests module to use for making API requests.

        Attributes:
            requests_module: The requests module used for making API requests.
            url: The base URL of the API.
            headers: The headers to include with every API request.
        """
        self.requests_module: requests = requests_module
        self.url: str = "https://api.artifactsmmo.com/"
        self.headers: str = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_token['token']}",
            "Content-Type": "application/json"
            }

    def get(self, endpoint: str, params: dict[str, str] = {}) -> dict[str, str]:
        """Makes a GET request to the given endpoint.

        Args:
            endpoint (str): The endpoint to request.
            params (dict[str, str], optional): The query parameters to send. Defaults to {}.

        Returns:
            response (dict[str, str]): The parsed JSON response.
        """
        response: requests.Response = self.requests_module.get(
            f"{self.url}{endpoint}",
            headers=self.headers,
            params=params
        )

        try:
            json_response = response.json()
            return json_response
        except JSONDecodeError:
            return response

    def post(self, endpoint: str, data: dict[str, str] = {}) -> dict[str, str]:
        """Makes a POST request to the given endpoint.

        Args:
            endpoint (str): The endpoint to request.
            data (dict[str, str], optional): The JSON data to send. Defaults to {}.

        Returns:
            response (dict[str, str]): The parsed JSON response.
        """
        response: requests.Response = self.requests_module.post(
            f"{self.url}{endpoint}", 
            headers=self.headers, 
            json=data
            )
        
        return response.json()