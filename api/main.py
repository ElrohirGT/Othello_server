from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import string
import random
import json
import os
import pickle
from othello_game import OthelloGame


def player_exists(username: str) -> bool:
    file_path = 'players.json'

    with open(file_path, 'r') as file:
        data = json.load(file)

    return username in data['current_players']

def player_create(username: str) -> bool:
    file_path = 'players.json'

    with open(file_path, 'r') as file:
        data = json.load(file)

    data['current_players'].append(username)

    with open(file_path, 'w') as file:
        json.dump(data, file)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[""]
)


@app.get("/root")
def read_root():
    return {"Hello": "World"}

@app.post("/session/new")
def new_session(session_name : str):
    # Specify the path of the directory
    directory_path = '../sessions/' + session_name

    # Create the directory
    # Check if the directory was created
    if os.path.exists(directory_path):
        message = f"Session ID: '{directory_path}' already exists."
    else:
        os.makedirs(directory_path, exist_ok=True)
        if os.path.exists(directory_path):
            session_variables = {}
            session_variables['players'] = []
            session_variables['scores'] = {}
            session_variables['active'] = True
            session_variables['open'] = True

            file_path = directory_path + '/session_variables.json'
            with open(file_path, 'w') as file:
                json.dump(session_variables, file)

            os.makedirs(directory_path + '/games', exist_ok=True)

            message = f"Session ID: '{directory_path}' successfully created."
        else:
            message = f"Failed to create Session ID: '{directory_path}'."

    return ({
        "message": message
    })

@app.get("/session/active")
def list_sessions():
    existing_sessions = os.listdir('/sessions')
    active_sessions = []
    for _existing_session in existing_sessions:

        file_path = '../sessions/' + _existing_session + '/session_variables.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                try:
                    if data['active'] :
                        active_sessions.append(_existing_session)
                except:
                    pass

    return {"sessions": active_sessions}

@app.post("/session/player/register")
def register_player(user_name : str, session_name : str):
    directory_path = '../sessions/' + session_name
    if os.path.exists(directory_path):
        file_path =  directory_path + '/session_variables.json'
        with open(file_path, 'r') as file:
            data = json.load(file)
        if data['open']:
            if user_name in data['players']:
                return {"message": "User already exists. Please select another ID."}

            else:
                data['players'].append(user_name)
                with open(file_path, 'w') as file:
                    json.dump(data, file)

                return {"message": "USER '" + user_name + "' succesfully created."}
        else:
            return {"message": "Session already closed"}

    else:
        return {"message": "Session ID '" + session_name + "' does not exist."}


@app.post("/session/close")
def session_close(session_name : str):
    directory_path = '../sessions/' + session_name
    if os.path.exists(directory_path):

        file_path = directory_path + '/session_variables.json'

        with open(file_path, 'r') as file:
            data = json.load(file)

        if data['open']:
            data['open'] = False
            with open(file_path, 'w') as file:
                json.dump(data, file)

            return {"message": "Session closed"}
        else:
            return {"message": "Session already closed"}


    else:
        return {"message": "Session ID '" + session_name + "' does not exist."}


def random_pair(items):

    _random_items = random.sample(items, len(items))
    pairs = []
    for i in range(0, len(_random_items) - 1, 2):
        pairs.append([_random_items[i], _random_items[i+1]])
    if len(_random_items) % 2 != 0:
        pairs.append([_random_items[-1],])
    return pairs

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@app.post("/session/pair")
def pair_players(session_name : str):
    directory_path = '../sessions/' + session_name
    if os.path.exists(directory_path):

        file_path = directory_path + '/session_variables.json'

        with open(file_path, 'r') as file:
            data = json.load(file)

        if data['open']:
            return {"message": "Please close the session before pairing the players."}
        else:
            _players = data['players']
            matches = random_pair(_players)
            current_matches = []
            for match in matches:
                if len(match) > 1:
                    match_id = generate_random_string(6)
                    current_matches.append({
                        'whites': match[0]
                        , 'blacks': match[1]
                        , 'match_id': match_id
                    })

                    match_game = OthelloGame(match_id)

                    with open(directory_path + '/games/' + match_id+'.pkl', 'wb') as f:
                        # Serialize and save the object to the file
                        pickle.dump(match_game, f)

            data['current_matches'] = current_matches
            with open(file_path, 'w') as file:
                json.dump(data, file)

            return {"message": "Pairs done"}
    else:
        return {"message": "Session ID '" + session_name + "' does not exist."}