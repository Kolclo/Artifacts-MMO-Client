from requester import SendRequest
from data.monster import Monster
from data.resource import Resource
from data.character import Character
from data.map import Map


# Custom Errors
# World Related
class GetMapError(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to get map due to an error")

class GetMonsterError(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to get monster due to an error")

class GetResourceError(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to get resource due to an error")

class GetEventsError(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to get events due to an error")

# Character Related
class NoCharactersExistError(Exception):
    def __init__(self) -> None:
        super().__init__("No characters currently exist")

class MoveCharacterError(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to move character due to an error")


# Get Actions
class Get:
    def __init__(self, request_client: SendRequest = SendRequest()) -> None:
        self.send_request: SendRequest = request_client

    def __error_handler(self, response: dict[str, str], exception_handler: Exception) -> None:
        if "error" in response:
            print(f"Failed to do action due to error {response['error']['message']}")
            raise exception_handler()


    def server_status(self) -> dict[str, str | int]:
        response: dict[str, str | int] = self.send_request.get("/")
        return response["data"]
    
    def resource(self, resource_name: str) -> Resource:
        response: dict[str, str | int] = self.send_request.get(f"/resources/{resource_name}")
        self.__error_handler(response, GetResourceError)
        return Resource(response["data"])
    
    def monster(self, monster_name: str) -> Monster:
        response: dict[str, str | int] = self.send_request.get(f"/resources/{monster_name}")
        self.__error_handler(response, GetMonsterError)
        return Monster(response["data"])

    def all_maps(self):
        data = []
        page = 1
        while True:
            response = self.send_request.get("maps", params={"size": 100, "page": page})
            if not response["data"]:
                break
            data.extend(response["data"])
            page += 1
        return data
    
    def map(self, position_x: int, position_y: int) -> Map:
        response: dict[str, str | int] = self.send_request.get(f"/maps/{position_x}/{position_y}")
        self.__error_handler(response, GetMapError)
        return Map(response["data"])
    
    def event(self) -> list[dict[str, str | int]]:
        response: dict[str, list[dict[str, str | int]]] = self.send_request.get("/events/")
        self.__error_handler(response, GetEventsError)
        return response["data"]
    
    def characters(self) -> list[Character]:
        response: dict[str, list[dict[str, str | int]]] = self.send_request.get("/my/characters/")
        self.__error_handler(response, NoCharactersExistError)
        characters: list[Character] = [Character(character_data) for character_data in response["data"]]
        return characters
    
    def character(self, character_name: str) -> Character:
        response: dict[str, str | int | list[dict[str, str | int]]] = self.send_request.get(f"/characters/{character_name}", params={"name": {character_name}})
        self.__error_handler(response, NoCharactersExistError)
        return Character(response["data"])

class Post:
    def __init__(self, request_client: SendRequest = SendRequest()) -> None:
        self.send_request: SendRequest = request_client

    def __error_handler(self, response: dict[str, str], exception_handler: Exception) -> None:
        if "error" in response:
            print(f"Failed to do action due to error {response['error']['message']}")
            raise exception_handler()
        
    
    def move_character(self, character_name: str, position_x: int, position_y: int):
        data = {"x": position_x, "y": position_y}
        response: dict[str, dict[str, str | int | list[dict[str, str | int]]]] = self.send_request.post(f"/my/{character_name}/action/move", data)
        self.__error_handler(response, MoveCharacterError)
        character_data = response["data"]["character"]
        character: Character = Character(character_data)
        return character


if __name__ == "__main__":
    character_name = "Kieran"
    send_post = Post()
    send_post.move_character("Kieran", 1, 0)