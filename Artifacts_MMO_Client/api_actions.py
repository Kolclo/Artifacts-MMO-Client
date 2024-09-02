from requester import SendRequest
from data.monster import Monster
from data.resource import Resource
from data.character import Character
from data.map import Map
import time


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
        super().__init__(f"Failed to move character due to an error")

class FightError(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to fight due to an error")


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
        

    # Primary Actions
    def move_character(self, character_name: str, position_x: int, position_y: int):
        max_retries = 3
        retries = 0
        while retries < max_retries:
            try:
                data = {"x": position_x, "y": position_y}
                response: dict[str, dict[str, str | int | list[dict[str, str | int]]]] = self.send_request.post(f"/my/{character_name}/action/move", data)
                self.__error_handler(response, MoveCharacterError)
                character_data = response["data"]["character"]
                character: Character = Character(character_data)
                return character
            except MoveCharacterError as e:
                print(f"Error moving character: {e}")
                retries += 1
                # Wait for 5 seconds before trying to move again
                time.sleep(5)
        else:
            print("Failed to move character after {} retries".format(max_retries))
            raise MoveCharacterError
    
    def fight(self, character_name: str):
        response: dict[str, dict] = self.send_request.post(f"/my/{character_name}/action/fight")
        self.__error_handler(response, FightError)
        character_data = response["data"]["character"]
        character: Character = Character(character_data)
        return character

    def gather(self):
        # /my/{name}/action/gathering
        # Must be on a resource
        pass

    def craft(self):
        # /my/{name}/action/crafting
        # Must be on a workshop tile

        # {
        # "code": "string",
        # "quantity": 1
        # }

        pass

    def equip(self):
        # /my/{name}/action/equip

        # {
        # "code": "string",
        # "slot": "weapon",
        # "quantity": 1
        # }
        pass

    def unequip(self):
        # /my/{name}/action/unequip

        # {
        # "slot": "weapon",
        # "quantity": 1
        # }
        pass
    

    # Task-related
    def accept_task(self):
        # /my/{name}/action/task/new
        pass

    def complete_task(self):
        # /my/{name}/action/task/complete
        pass

    def cancel_task(self):
        # /my/{name}/action/task/cancel
        pass


    # Bank-related
    def deposit_item(self):
        # /my/{name}/action/bank/deposit

        # {
        # "code": "string",
        # "quantity": 1
        # }

        pass

    def deposit_gold(self):
        # /my/{name}/action/bank/deposit/gold

        # {
        # "quantity": 1
        # }
        pass

    def withdraw_item(self):
        # /my/{name}/action/bank/withdraw

        # {
        # "code": "string",
        # "quantity": 1
        # }
        pass

    def withdraw_money(self):
        # /my/{name}/action/bank/withdraw/gold

        # {
        # "quantity": 1
        # }
        pass

    def buy_expansion(self):
        # /my/{name}/action/bank/buy_expansion
        pass

    # Exchange-related
    def buy_item(self):
        # /my/{name}/action/ge/buy

        # {
        # "code": "string",
        # "quantity": 1,
        # "price": 1
        # }
        pass

    def sell_item(self):
        # /my/{name}/action/ge/buy

        # {
        # "code": "string",
        # "quantity": 1,
        # "price": 1
        # }
        pass



if __name__ == "__main__":
    character_name = "Kieran"
    send_post = Post()
    # send_post.move_character("Kieran", 1, 0)
    send_post.fight(character_name)