from controller import CharacterController
import time
from game_state import GameState
from api_actions import Get
from data.options import Options
from data.map import Map

get_request: Get = Get()

character_data1 = get_request.character("Kieran")
character_data2 = get_request.character("Shabazz")
character_data3 = get_request.character("longnametest")
character_data4 = get_request.character("Pog")
character_data5 = get_request.character("ChadusRexus")

map_data_request1: Map = get_request.map(character_data1.x, character_data1.y)
map_data_request2: Map = get_request.map(character_data2.x, character_data2.y)
map_data_request3: Map = get_request.map(character_data3.x, character_data3.y)
map_data_request4: Map = get_request.map(character_data4.x, character_data4.y)
map_data_request5: Map = get_request.map(character_data5.x, character_data5.y)

game_data1: GameState = GameState(character_data1, map_data_request1)
game_data2: GameState = GameState(character_data2, map_data_request2)
game_data3: GameState = GameState(character_data3, map_data_request3)
game_data4: GameState = GameState(character_data4, map_data_request4)
game_data5: GameState = GameState(character_data5, map_data_request5)

controller1 = CharacterController(game_data1)
controller2 = CharacterController(game_data2)
controller3 = CharacterController(game_data3)
controller4 = CharacterController(game_data4)
controller5 = CharacterController(game_data5)

while True:
    controller1.perform_action()
    controller2.perform_action()
    controller3.perform_action()
    controller4.perform_action()
    controller5.perform_action()
    time.sleep(60)