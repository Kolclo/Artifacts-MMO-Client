# Artifacts MMO Python Client
This client can be used to play the [Artifacts MMO](https://artifactsmmo.com/).

## Usage
Requires `Python 3.10.11` (others may work but this is what I'm using)

### Clone the package
```git clone https://github.com/Kolclo/Artifacts-MMO-Client.git```

### Set up venv
`cd` into the package and use the following to create and activate the venv (Windows):

```bash
python -m venv .venv 
.venv\Scripts\activate
```

Then use ```pip3 install -r requirements.txt``` to get all the required packages

### Create credentials.py
Create a new file called `credentials.py` in `/Artifacts-MMO-Client/Artifacts_MMO_Client/` with the following inside:

```
api_token: dict[str, str] = {"token": "PUT TOKEN HERE"}
```

Sign up to [Artifacts MMO](https://artifactsmmo.com/) to get your API key, then paste it inside the credentials file

You're good to play!


## To-do

### Actions
Add support for more actions using APIs
- [ ] Display cooldown for actions on screen
- [ ] Move control ability to mapper instead of it's own window

#### Movement
- [x] Movement
- [x] Create corresponding API actions
- [ ] Improve efficiency - Add up all subsequent actions and send them all at once
- [x] Retry movement command after cooldown period instead of every 5 secs
- [ ] Error handling

#### Combat
- [ ] Combat
- [x] Create corresponding API actions
- [x] Sync location after combat is complete
- [ ] Error handling

#### Gathering
- [ ] Gathering
- [ ] Create corresponding API actions
- [ ] Error handling

#### Crafting
- [ ] Crafting
- [ ] Create corresponding API actions
- [ ] Error handling

### Equip/Unequip
- [ ] Equip items
- [ ] Unequip items
- [ ] Toggle feature - eg. 'W' will equip or unequip Weapon?
- [ ] Create corresponding API actions
- [ ] Error handles

(and more once these are done)

### Map
Render an interactive and dynamic map
- [x] Support for map rendering
- [x] Dynamic updates to map using API
- [ ] Support for map zooming?
- [x] Show character sprite on top of map
- [x] Show character sprite in correct server-side location + potential caching (half done)
- [x] Only move character sprite client-side if the character has moved server-side
- [x] Display correct character sprite depending on current character in use
- [ ] Ability to request new resources when they're not found locally
- [ ] Display name of the location you're hovering over in corner
- [ ] Display current location name in corner or near map
- [ ] Add pins to map?
- [ ] Save data from all_maps() to GameState and deprecate map() by using this data

### Controls - bugs
- [x] Button press should trigger movement/action
- [ ] Subsequent presses should be stored (for movement) 
- [ ] When cooldown has ended, add total subsequent presses and move that much. (eg. 4x up, 3x left, and 1x down would move the character to the tile that is 3 up and 3 left in one move)

### Inventory
Add support for inventory usage/management
- [ ] Access to inventory
- [ ] Inventory UI system

### Code Quality
Improve code consistency and efficiency
- [ ] Use typing for function parameters and return types
- [ ] Use more functions to make code more modular - in progress
- [x] Consistent naming conventions throughout the code
- [x] Remove hardcoded interactions with requester module and instead use api_actions

### Data
Improve data management via centralisation of data
- [ ] Move data into GameState class (in progress)
- [ ] Change all current code to use new GameState class

### Performance
Improve performance of client
- [ ] Multithreading?
- [ ] Option to play exclusively via terminal?


### Character Selection
Prompt user to select a character to control
- [x] Create custom background
- [x] Display background and animate it's movement
- [x] Create custom music
- [x] Get a list of characters from API
- [x] Display character list to user
- [x] Allow for character selection


make pygame module
separate gamestate from character and mapper
change name of Character inside Mapper.py
make controllers update stored data
make cooldown check into reusable function