from Artifacts_MMO_Client.requester import APIRequester


class MockResponse:
    @staticmethod
    def json() -> dict[str, str]:
        return {"data": {"name": "Mock Character"}}
    

class MockRequests:
    @staticmethod
    def get(url: str, headers: dict[str, str]) -> MockResponse:
        return MockResponse()
    
    @staticmethod
    def post(url: str, headers: dict[str, str], json: dict[str, str]) -> MockResponse:
        return MockResponse()
    

def test_get() -> None:
    api_requester: APIRequester = APIRequester(MockRequests())

    response: dict[str, str] = api_requester.get("/test/endpoint")

    assert response == {"data": {"name": "Mock Character"}}


def test_post() -> None:
    api_requester: APIRequester = APIRequester(MockRequests())
    mock_data: dict[str, str] = {"speed": "fast"}

    response: dict[str, str] = api_requester.post("/test/endpoint", mock_data)

    assert response == {"data": {"name": "Mock Character"}}