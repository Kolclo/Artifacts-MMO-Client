from api_actions import Get, Post
from data.character import Character
from game_state import GameState
from data.map import Map

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    def __eq__(self, other):
        """Checks if two Vector2s are equal.

        Compares the x and y attributes of the two Vector2s to see if they are equal.

        Args:
            other: The Vector2 to compare to.

        Returns:
            bool: True if the two Vector2s are equal, False otherwise.
        """
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        """Returns a new Vector2 that is the sum of this and the other given Vector2.

        Args:
            other: The Vector2 to add to this one.

        Returns:
            Vector2: A new Vector2 that is the sum of this and the other given Vector2.
        """
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Returns a new Vector2 that is the difference of this and the other given Vector2.

        Args:
            other: The Vector2 to subtract from this one.

        Returns:
            Vector2: A new Vector2 that is the difference of this and the other given Vector2.
        """
        return Vector2(self.x - other.x, self.y - other.y)

class CharacterController:
    def __init__(self, game_state):
        self.game_state: GameState = game_state
        self.character_name: str = self.game_state.character_data.name
        self.endpoint: str = f"my/{self.character_name}/action/move"
        self.character_location = None
        self.tile_data: Map = self.game_state.tile_data
        
        self.get_request: Get = Get()
        self.post_request: Post = Post(game_state)

        self.UP: Vector2 = Vector2(0, -1)
        self.DOWN: Vector2 = Vector2(0, 1)
        self.LEFT: Vector2 = Vector2(-1, 0)
        self.RIGHT: Vector2 = Vector2(1, 0)

    def move_character(self, location: Vector2) -> Vector2:
        """Move the character to the given location.

        Args:
            location (Vector2): The location to move the character to, eg. (1, -2)

        Returns:
            new_location (Vector2): The new location of the character
        """
        response = self.post_request.move_character(self.character_name, location.x, location.y)
        if response:
            new_location = Vector2(response.x, response.y)
            self.character_location = new_location
            print(f"Character moved to ({new_location.x}, {new_location.y})")
            return new_location
        else:
            return False
    
    def out_of_bounds_check(self, location: Vector2) -> Vector2:
        """Check if the given location is out of bounds.

        Args:
            location (Vector2): The location to check

        Returns:
            new_location (Vector2): The new location of the character
        """
        if location.x < -5 or location.x > 12 and location.y < 5 or location.y > 16:
            return True
        else:
            return False

    def get_character_location(self) -> Vector2:
        """Get the current location of the character.

        Returns:
            character_location (Vector2): The current location of the character
        """
        response = self.get_request.character(self.character_name)
        self.character_location = Vector2(response.x, response.y)
        return self.character_location

    def move_up(self) -> None:
        """Move the character up by one tile.

        If the character's current location is not known, it will be retrieved.
        The character will then be moved up by one tile and the new location will be stored.
        """
        if self.character_location is None:
            self.character_location = self.get_character_location()
        desired_location = self.character_location + self.UP
        if self.out_of_bounds_check(desired_location):
            print("You cannot move outside of the map.")
        else:
            new_location = self.move_character(desired_location)
            if new_location:
                self.character_location = new_location

    def move_down(self) -> None:
        """Move the character down by one tile.

        If the character's current location is not known, it will be retrieved.
        The character will then be moved down by one tile and the new location will be stored.
        """
        if self.character_location is None:
            self.character_location = self.get_character_location()
        desired_location = self.character_location + self.DOWN
        if self.out_of_bounds_check(desired_location):
            print("You cannot move outside of the map.")
        else:
            new_location = self.move_character(desired_location)
            if new_location:
                self.character_location = new_location

    def move_left(self) -> None:
        """Move the character left by one tile.

        If the character's current location is not known, it will be retrieved.
        The character will then be moved left by one tile and the new location will be stored.
        """
        if self.character_location is None:
            self.character_location = self.get_character_location()
        desired_location = self.character_location + self.LEFT
        if self.out_of_bounds_check(desired_location):
            print("You cannot move outside of the map.")
        else:
            new_location = self.move_character(desired_location)
            if new_location:
                self.character_location = new_location

    def move_right(self) -> None:
        """Move the character right by one tile.

        If the character's current location is not known, it will be retrieved.
        The character will then be moved right by one tile and the new location will be stored.
        """
        if self.character_location is None:
            self.character_location = self.get_character_location()
        desired_location = self.character_location + self.RIGHT
        if self.out_of_bounds_check(desired_location):
            print("You cannot move outside of the map.")
        else:
            new_location = self.move_character(desired_location)
            if new_location:
                self.character_location = new_location
    
    def perform_action(self) -> Character:
        """Check the current tile that the character is on and perform an action on it if appropriate.

        If the character is on a monster, they will attack it. If they are on a resource, they will gather it.
        The character's updated tile data is stored in the game state.

        Returns:
            response (Character): The updated character object
        """
        updated_tile_data = self.get_request.map(self.game_state.character_data.x, self.game_state.character_data.y)
        self.game_state.tile_data = updated_tile_data
        tile_type = self.game_state.tile_data.content.type
        if tile_type == "monster":
            response = self.post_request.fight(self.character_name)
            print(f"{self.character_name} attacked monster")
            self.game_state.character_data = response
            return response
        elif tile_type == "resource":
            response = self.post_request.gather(self.character_name)
            print(f"{self.character_name} gathered resource")
            self.game_state.character_data = response
            return response
    
    def unequip(self, slot: str):
        response = self.post_request.unequip(self.character_name, slot)
        print(f"{self.character_name} unequipped {slot}")
        return response
    
    def craft_item(self, item_code: str, quantity: int = 1):
        response = self.post_request.craft(self.character_name, item_code, quantity)
        print(f"{self.character_name} crafted {item_code}")
        return response
    
    def sell_item(self, item_code: str, price: int, quantity: int = 1):
        response = self.post_request.sell_item(self.character_name, item_code, price, quantity)
        print(f"{self.character_name} sold {item_code}")
        return response