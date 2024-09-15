import concurrent.futures
from api_actions import Get, Post
from data.character import Character
from data.map import Map
from game_state import GameState
from controller import CharacterController, Vector2
import time
import signal

class Automation:
    def __init__(self, excluded_characters: list[str] = []):
        self.running = True
        self.get_request: Get = Get()
        self.characters: list[Character] = self.get_request.characters()
        self.excluded_characters: list[str] = excluded_characters
        self.controllers = []
        self.forge_location = Vector2(1, 5)
        self.copper_ore_location = Vector2(2,0)
        self.iron_ore_location = Vector2(1,7)
        self.exchange_location = Vector2(5, 1)

        for character in self.characters:
            if character.name not in self.excluded_characters:
                character_data = self.get_request.character(character.name)
                map_data_request: Map = self.get_request.map(character_data.x, character_data.y)
                game_data: GameState = GameState(character_data, map_data_request)
                post_request: Post = Post(game_data)
                controller: CharacterController = CharacterController(game_data)
                self.controllers.append(controller)
    
    def signal_handler(self, signum, frame):
        print("\nCtrl+C pressed. Stopping the program gracefully...")
        self.running = False

    def perform_actions(self, controller):
        try:
            controller.perform_action()
        except Exception as e:
            print(f"Error performing action for {controller.game_state.character_data.name}: {e}")

    def craft_copper(self, controller):
        craft_quantity = 4
        craft_delay = craft_quantity * 5
        try:
            print(f"Moving {controller.game_state.character_data.name} to Forge")
            controller.move_character(self.forge_location)
            time.sleep(30)
            controller.craft_item("copper", craft_quantity)
            time.sleep(craft_delay)
            print(f"Moving {controller.game_state.character_data.name} back to the Copper")
            controller.move_character(self.copper_ore_location)
            time.sleep(30)
        except Exception as e:
            print(f"Error in craft_copper for {controller.game_state.character_data.name}: {e}")
    
    def craft_iron(self, controller):
        craft_quantity = 6
        craft_delay = craft_quantity * 5
        try:
            print(f"Moving {controller.game_state.character_data.name} to Forge")
            controller.move_character(self.forge_location)
            time.sleep(10)
            controller.craft_item("iron", craft_quantity)
            time.sleep(craft_delay)
            print(f"Moving {controller.game_state.character_data.name} back to the Iron")
            controller.move_character(self.iron_ore_location)
            time.sleep(10)
        except Exception as e:
            print(f"Error in craft_iron for {controller.game_state.character_data.name}: {e}")

    def sell_copper_bars(self, controller):
        try:
            print(f"Moving {controller.game_state.character_data.name} to Exchange")
            controller.move_character(self.exchange_location)
            time.sleep(22)
            copper_stock_data = self.get_request.item_price("copper")
            copper_sell_price = copper_stock_data["sell_price"]
            print(f"{controller.game_state.character_data.name} is trying to sell copper at {copper_sell_price}")
            controller.sell_item("copper", copper_sell_price, 16)
            time.sleep(5)
            print(f"Moving {controller.game_state.character_data.name} back to the Copper")
            controller.move_character(self.copper_ore_location)
        except Exception as e:
            print(f"Error in sell_copper_bars for {controller.game_state.character_data.name}: {e}")
    
    def sell_iron_bars(self, controller):
        try:
            print(f"Moving {controller.game_state.character_data.name} to Exchange")
            controller.move_character(self.exchange_location)
            time.sleep(51)
            iron_stock_data = self.get_request.item_price("iron")
            iron_sell_price = iron_stock_data["sell_price"]
            print(f"{controller.game_state.character_data.name} is trying to sell iron at {iron_sell_price}")
            controller.sell_item("iron", iron_sell_price, 24)
            time.sleep(4)
            print(f"Moving {controller.game_state.character_data.name} back to the Iron")
            controller.move_character(self.iron_ore_location)
        except Exception as e:
            print(f"Error in sell_iron_bars for {controller.game_state.character_data.name}: {e}")

    def run(self):
        # Set up the signal handler
        signal.signal(signal.SIGINT, self.signal_handler)

        loops = 48
        x = 0

        second_loops = 0

        while self.running:
            print("Starting a new round of actions for all characters")

            # Perform actions loop
            while x < loops and self.running:
                print(f"Performing actions for all characters, loop {x + 1} of {loops}")
                with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.controllers)) as executor:
                    futures = [executor.submit(self.perform_actions, controller) for controller in self.controllers]
                    
                    for future in concurrent.futures.as_completed(futures):
                        if not self.running:
                            break
                        
                        try:
                            future.result()  # This will raise any exceptions that occurred in the thread
                        except Exception as e:
                            print(f"An error occurred: {e}")
                
                x += 1
                if self.running:
                    time.sleep(25)

            # Do something after completing the action loop
            if self.running:
                with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.controllers)) as executor:
                    futures = [executor.submit(self.craft_iron, controller) for controller in self.controllers]
                    
                    for future in concurrent.futures.as_completed(futures):
                        if not self.running:
                            break
                        try:
                            future.result()
                        except Exception as e:
                            print(f"An error occurred during craft_iron: {e}")
            x = 0
            second_loops += 1

            # Sell iron
            if (second_loops >= 4) and self.running:
                for controller in self.controllers:
                    if not self.running:
                        break
                    try:
                        self.sell_iron_bars(controller)
                    except Exception as e:
                        print(f"An error occurred during sell_iron_bars for {controller.game_state.character_data.name}: {e}")
                second_loops = 0
                time.sleep(50)



if __name__ == "__main__":
    excluded_characters = []
    # excluded_characters.append("Kieran")
    # excluded_characters.append("Shabazz")
    # excluded_characters.append("longnametest")
    # excluded_characters.append("Pog")
    # excluded_characters.append("ChadusRexus")
    automation = Automation(excluded_characters)
    try:
        automation.run()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting.")