from requester import SendRequest
from data.monster import Monster
from data.resource import Resource
from data.character import Character
from data.map import Map
from game_state import GameState
import sys


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

class GatherError(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to gather due to an error")

class UnequipError(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to unequip due to an error")

class AcceptTaskError(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to accept task due to an error")

class CompleteTaskError(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to complete task due to an error")

class CancelTaskError(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to cancel task due to an error")

# Bank-related
class BuyExpansionError(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to buy expansion due to an error")

# Get Actions
class Get:
    def __init__(self, request_client: SendRequest = SendRequest()) -> None:
        self.send_request: SendRequest = request_client

    def __error_handler(self, response: dict[str, str], exception_handler: Exception) -> None:
        if "error" in response:
            print(f"Failed to do action due to error: {response['error']['message']}")
            raise exception_handler()


    def server_status(self) -> dict[str, str | int]:
        """Get the server status.
        
        Returns:
            Server status (dict[str, str | int]): Server status data
        """
        status: dict[str, str | int] = self.send_request.get("/")
        try:
            print(status)
            if not status["data"]["status"] == "online":
                print("Server is offline. Please try again later.")
                sys.exit()
            print("Server is online! Continuing game initialisation.")
            return status
        except Exception as e:
            print(f"Failed to get server status.")
            sys.exit()
        
    
    def resource(self, resource_name: str) -> Resource:
        """Get details of a resource by name.
        
        Args:
            resource_name (str): Name of the resource to get
        
        Returns:
            Resource: Resource object with the given name and details
        """
        response: dict[str, str | int] = self.send_request.get(f"/resources/{resource_name}")
        self.__error_handler(response, GetResourceError)
        return Resource(response["data"])
    
    def monster(self, monster_name: str) -> Monster:
        """Get details of a monster by name.
        
        Args:
            monster_name (str): Name of the monster to get
        
        Returns:
            Monster: Monster object with the given name and details
        """
        response: dict[str, str | int] = self.send_request.get(f"/monsters/{monster_name}")
        self.__error_handler(response, GetMonsterError)
        return Monster(response["data"])

    def all_maps(self) -> list[dict[str, str | int]]:
        """Get all maps from the API.
        
        Returns:
            Data (list[dict[str, str | int]]): List of all map data
        """
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
        """Get map data from the API by position.
        
        Args:
            position_x (int): The x position of the map
            position_y (int): The y position of the map
        
        Returns:
            Map: Map object with the given position and details
        """
        response: dict[str, str | int] = self.send_request.get(f"/maps/{position_x}/{position_y}")
        self.__error_handler(response, GetMapError)
        return Map(response["data"])
    
    def event(self) -> list[dict[str, str | int]]:
        """Get all events from the API.
        
        Returns:
            Events (list[dict[str, str | int]]): List of all event data
        """
        response: dict[str, list[dict[str, str | int]]] = self.send_request.get("/events/")
        self.__error_handler(response, GetEventsError)
        return response["data"]
    
    def characters(self) -> list[Character]:
        """Get all available characters for the current user.
        
        Returns:
            Characters (list[Character]): List of all characters for the user
        """
        response: dict[str, list[dict[str, str | int]]] = self.send_request.get("/my/characters/")
        self.__error_handler(response, NoCharactersExistError)
        characters: list[Character] = [Character(character_data) for character_data in response["data"]]
        return characters
    
    def character(self, character_name: str) -> Character:
        """Get all details on a character by name.
        
        Args:
            character_name (str): The name of the character to get
        
        Returns:
            Character: The character object with the given name and details
        """
        response: dict[str, str | int | list[dict[str, str | int]]] = self.send_request.get(f"/characters/{character_name}", params={"name": {character_name}})
        self.__error_handler(response, NoCharactersExistError)
        return Character(response["data"])

class Post:
    def __init__(self, game_state, request_client: SendRequest = SendRequest()) -> None:
        self.send_request: SendRequest = request_client
        self.game_state: GameState = game_state

    def __error_handler(self, response: dict[str, str], exception_handler: Exception) -> None:
        """Checks if a response contains an error key and raises the given exception
        if it does.
        
        Args:
            response (dict[str, str]): The response to check for an error
            exception_handler (Exception): The exception to raise if the response contains an error
        """
        if "error" in response:
            print(f"Failed to do action due to error: {response['error']['message']}")
            raise exception_handler()
        

    # Primary Actions
    def move_character(self, character_name: str, position_x: int, position_y: int) -> Character:
        """Move the character to the given location.
        
        Args:
            character_name (str): The name of the character to move
            position_x (int): The x position of the location to move to
            position_y (int): The y position of the location to move to
        
        Returns:
            Character: The character object with updated data
        """
        data: dict[str, int] = {"x": position_x, "y": position_y}
        response: dict[str, dict[str, str | int | list[dict[str, str | int]]]] = self.send_request.post(f"/my/{character_name}/action/move", data)
        character_data: dict = response["data"]["character"]
        character: Character = Character(character_data)
        self.game_state.character_data = character
        return character
    
    def fight(self, character_name: str) -> Character:
        """Engage in combat with the current monster the character is at.
        
        Args:
            character_name (str): The name of the character to engage in combat
        
        Returns:
            Character: The character object with updated data
        """
        response: dict[str, dict] = self.send_request.post(f"/my/{character_name}/action/fight")
        self.__error_handler(response, FightError)
        character_data: dict = response["data"]["character"]
        character: Character = Character(character_data)
        return character

    def gather(self, character_name: str) -> Character:
        """Gather resources at the character's current location.
        
        Args:
            character_name (str): The name of the character to gather resources
        
        Returns:
            Character: The character object with updated data
        """
        response: dict[str, dict] = self.send_request.post(f"/my/{character_name}/action/gathering")
        self.__error_handler(response, GatherError)
        character_data: dict = response["data"]["character"]
        character: Character = Character(character_data)
        return character

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

    def unequip(self, character_name: str, data) -> Character:
        """Unequip an item from the given slot.
        
        Args:
            character_name (str): The name of the character to unequip an item from
            data (str): The name of the slot to unequip from
        Returns:
            Character: The character object with updated data
        """
        slot = {"slot": data}
        response: dict[str, dict] = self.send_request.post(f"/my/{character_name}/action/unequip", slot)
        self.__error_handler(response, UnequipError)
        character_data: dict = response["data"]["character"]
        character: Character = Character(character_data)
        return character
    

    # Task-related
    def accept_task(self):
        """Accept a task if one is available.
        
        If a task is available, this will accept the task and update the character's data.
        
        Returns:
            Character: The character object with updated data
        """
        response: dict[str, dict] = self.send_request.post(f"/my/{character_name}/action/task/new")
        self.__error_handler(response, AcceptTaskError)
        character_data: dict = response["data"]["character"]
        character: Character = Character(character_data)
        return character

    def complete_task(self):
        """Complete the current task if one is available.
        
        If a task is available, this will complete the task and update the character's data.
        
        Returns:
            Character: The character object with updated data
        """
        response: dict[str, dict] = self.send_request.post(f"/my/{character_name}/action/task/complete")
        self.__error_handler(response, CompleteTaskError)
        character_data: dict = response["data"]["character"]
        character: Character = Character(character_data)
        return character

    def cancel_task(self):
        """Cancel the current task if one is available.
        
        If a task is available, this will cancel the task and update the character's data.
        
        Returns:
            Character: The character object with updated data
        """
        response: dict[str, dict] = self.send_request.post(f"/my/{character_name}/action/task/cancel")
        self.__error_handler(response, CancelTaskError)
        character_data: dict = response["data"]["character"]
        character: Character = Character(character_data)
        return character


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
        """Buys an expansion in the bank.

        Returns:
            Character: The updated character object
        """
        response: dict[str, dict] = self.send_request.post(f"/my/{character_name}/action/bank/buy_expansion")
        self.__error_handler(response, BuyExpansionError)
        character_data: dict = response["data"]["character"]
        character: Character = Character(character_data)
        return character

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