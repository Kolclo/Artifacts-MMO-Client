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

#### Movement
- [ ] Movement
- [ ] Create corresponding API actions
- [ ] Error handling

#### Combat
- [ ] Combat
- [ ] Create corresponding API actions
- [ ] Error handling

#### Gathering
- [ ] Gathering
- [ ] Create corresponding API actions
- [ ] Error handling

#### Crafting
- [ ] Crafting
- [ ] Create corresponding API actions
- [ ] Error handling

(and more once these are done)

### Map
Render an interactive and dynamic map
- [x] Support for map rendering
- [x] Dynamic updates to map using API
- [ ] Support for map zooming?
- [x] Show character sprite on top of map
- [ ] Show character sprite in correct server-side location + potential caching
- [ ] Display correct character sprite depending on current character in use
- [ ] Ability to request new resources when they're not found locally
- [ ] Display name of the location you're hovering over in corner
- [ ] Display current location name in corner or near map
- [ ] Add pins to map?

### Inventory
Add support for inventory usage/management
- [ ] Access to inventory
- [ ] Inventory UI system

### Code Quality
Improve code consistency and efficiency
- [ ] Use typing for function parameters and return types
- [ ] Use more functions to make code more modular
- [ ] Consistent naming conventions throughout the code
- [ ] Remove hardcoded interactions with requester module and instead use api_actions

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
