import time

import streamlit as st
import pandas as pd
import random
import numpy as np
import time
import requests

host = 'http://localhost:8000'
# host = 'http://ec2-18-224-173-144.us-east-2.compute.amazonaws.com:8000'

st.session_state.game_id = st.session_state.get('game_id', '')
st.session_state.game_status = st.session_state.get('game_id', 'new')
st.session_state.session_status = st.session_state.get('session_status', 'open')
st.session_state.classification = st.session_state.get('classification', [])
st.session_state.matches = st.session_state.get('matches', [])

def start_game(game_id):

    if _game_id == '':

        st.toast('Empty text input', icon="⚠️")

    else :
        st.session_state.game_id = _game_id
        game_info = requests.post(host + '/game/game_info?session_name=' + _game_id).json()

        if game_info['status'] == 501:
            st.session_state.game_status = 'New Game'
            new_game = requests.post(host + '/game/new_game?session_name=' + _game_id).json()

        response = requests.post(host + '/game/classification?session_name=' + _game_id).json()

        if 'data' in response:
            st.session_state.classification = response['data']
        else:
            st.session_state.classification = []

def refresh_classif(game_id):
    response = requests.post(host + '/game/classification?session_name=' + _game_id).json()
    if 'data' in response:
        st.session_state.classification = response['data']
    else:
        st.session_state.classification = []
#
# def refresh_matches():
#     pass
#
# def close_session():
#
#     if st.session_state.session_status == 'open':
#         st.session_state.session_status = 'close'
#         close_session = requests.post(host + '/game/close_registration?session_name=' + st.session_state.game_id)
#     # else:
#     #     st.session_state.session_status = 'open'
#     #     close_session = requests.post(host + '/game/open_registration?session_name=' + st.session_state.game_id)
#
#
#
# def pair_players():
#     pair = requests.post(host+ '/game/pair_players?session_name=' + st.session_state.game_id)

_game_id = st.text_input('Enter game id')

start_button =  st.button('Start game', on_click=start_game(_game_id))

st.title(f'{st.session_state.game_id}')

col1, col2,col3 = st.columns([4,10,2])

with col1:
    st.subheader('Classification')
with col3:
    if st.button('Refresh', key = 'classif_refresh'):
        response = requests.post(host + '/game/classification?session_name=' + st.session_state.game_id)
        if response.status_code == 200:
            response = response.json()
            if 'data' in response:
                st.session_state.classification = response['data']
            else:
                st.session_state.classification = []


st.dataframe(
    pd.DataFrame(st.session_state.classification)
    , column_config={
            "name" : "Player"
            , "played" : st.column_config.NumberColumn('Played')
            , "wins" : st.column_config.NumberColumn('Won 🥇', format = '%d')
            , "draws" : st.column_config.NumberColumn('Drawn 🤝', format = '%d')
            , "losses" : st.column_config.NumberColumn('Lost 😿', format = '%d')
            , "points" : st.column_config.NumberColumn('Points 🏆')
        }
        , use_container_width=True
        , hide_index=True
)

st.subheader('Matches')

col1, col2, col3= st.columns([4,10,2])


with col1:
    # pair_button = st.button('Pair', key = 'pairing', type = 'primary',  on_click = pair_players())
    if st.button('Pair', key = 'pairing', type = 'primary'):
        if st.session_state.game_id ==  '':
            st.toast('Invalid Game ID', icon="⚠️")
        else:
            pair = requests.post(host + '/game/pair_players?session_name=' + st.session_state.game_id)
            response = requests.post(host + '/game/current_matches?session_name=' + st.session_state.game_id).json()
            st.session_state.matches = response['data']

with col3:
    if st.button('Refresh', key = 'matches_refresh'):
        if st.session_state.game_id ==  '':
            st.toast('Invalid Game ID', icon="⚠️")
        else:
            response = requests.post(host + '/game/current_matches?session_name=' + st.session_state.game_id).json()
            st.session_state.matches = response['data']

st.dataframe(
    pd.DataFrame(st.session_state.matches)
    , column_config={
            "name" : "Player"
            , "played" : st.column_config.NumberColumn('Played')
            , "wins" : st.column_config.NumberColumn('Won 🥇', format = '%d')
            , "draws" : st.column_config.NumberColumn('Drawn 🤝', format = '%d')
            , "losses" : st.column_config.NumberColumn('Lost 😿', format = '%d')
            , "points" : st.column_config.NumberColumn('Points 🏆')
        }
    , use_container_width=True
    , hide_index=True
)