import requests
import random
import sys
import time

# host_name = 'http://ec2-3-142-147-237.us-east-2.compute.amazonaws.com:8000'
host_name = 'http://localhost:8000'

class OthelloPlayer():

    def __init__(self, username):
        self.username = username


    def connect(self, session_name):
        response = requests.post(host_name+'/session/player/register?user_name='+self.username+'&session_name='+session_name)
        if response.status_code == 200:
            print(response.content)
            self.session_name = session_name

    def AI_MOVE(self, board):
        row = random.randint(0, 7)
        col = random.randint(0, 7)
        return (row, col)
        return (row, col)

    def play(self):
        while True:
            turn = requests.post(host_name + '/player/turn?session_name=' + self.session_name + '&player_id=' + self.username)
            if turn.status_code == 200:
                turn = turn.json()

                while not (turn['message'] == 'Game Over'):
                    if turn['turn']:
                        row, col = self.AI_MOVE(turn['board'])
                        move = requests.post(host_name + '/player/move?session_name=' + self.session_name + '&player_id=' + self.username + '&row=' + str(row) + '&column=' + str(col))
                        move = move.json()
                        print(move)
                    time.sleep(2)







print('Mucho gusto!')
# sys.argv[0] is the script name
script_name = sys.argv[0]
# The rest of the arguments start from sys.argv[1]
session_id = sys.argv[1]
player_id = sys.argv[2]

othello_player = OthelloPlayer(player_id)
othello_player.connect(session_id)
othello_player.play()
