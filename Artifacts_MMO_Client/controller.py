from api_actions import Get, Post

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

class CharacterController:
    def __init__(self, character_name):
        self.character_name = character_name
        self.endpoint = f"my/{character_name}/action/move"
        self.character_location = None
        
        self.get_request = Get()
        self.post_request = Post()

        self.UP = Vector2(0, -1)
        self.DOWN = Vector2(0, 1)
        self.LEFT = Vector2(-1, 0)
        self.RIGHT = Vector2(1, 0)

    def move_character(self, location):
        response = self.post_request.move_character(self.character_name, location.x, location.y)
        new_location = Vector2(response.x, response.y)
        self.character_location = new_location
        print(f"Character moved to ({new_location.x}, {new_location.y})")
        return new_location

    def get_character_location(self):
        response = self.get_request.character(self.character_name)
        self.character_location = Vector2(response.x, response.y)
        return self.character_location

    def move_up(self):
        if self.character_location is None:
            self.character_location = self.get_character_location()
        new_location = self.move_character(self.character_location + self.UP)
        if new_location:
            self.character_location = new_location

    def move_down(self):
        if self.character_location is None:
            self.character_location = self.get_character_location()
        new_location = self.move_character(self.character_location + self.DOWN)
        if new_location:
            self.character_location = new_location

    def move_left(self):
        if self.character_location is None:
            self.character_location = self.get_character_location()
        new_location = self.move_character(self.character_location + self.LEFT)
        if new_location:
            self.character_location = new_location

    def move_right(self):
        if self.character_location is None:
            self.character_location = self.get_character_location()
        new_location = self.move_character(self.character_location + self.RIGHT)
        if new_location:
            self.character_location = new_location