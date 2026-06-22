# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

import ast
import json

def player_kris(prev_play, opponent_history=[]):
  ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}

  if prev_play == '':
    prev_play = "R"

  guess = ideal_response[ideal_response[prev_play]]

  return guess

def player_quincy(prev_play, opponent_history=[]):
  opponent_history.append(prev_play)

  guess = "P"

  if len(opponent_history) > 2:
    guess = opponent_history[-3]

  return guess

def player_mrugesh(prev_play):
  player_history = []
  ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}

  if prev_play == '':
    prev_play = 'S'
    
  player_history.append(ideal_response[ideal_response[prev_play]])
  last_ten = player_history[-10:]
  most_frequent = max(set(last_ten), key=last_ten.count)

  return ideal_response[ideal_response[most_frequent]]

def player_abbey(prev_play, opponent_history=[]):
  ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
  prediction = 'P'
  play_order = {
      "RR": 0,
      "RP": 0,
      "RS": 0,
      "PR": 0,
      "PP": 0,
      "PS": 0,
      "SR": 0,
      "SP": 0,
      "SS": 0,
  }
  
  if not prev_play:
    prev_play = 'R'
    opponent_history.append(str(play_order))
    opponent_history.append(prev_play)
  else:
    opponent_history.append(ideal_response[prev_play])

  play_order = ast.literal_eval(opponent_history[0])
  
  if len(opponent_history) >= 3:
    last_two = "".join(opponent_history[-2:])
    if len(last_two) == 2:
      play_order[last_two] += 1
      opponent_history[0] = json.dumps(play_order)

  potential_plays = [
    ideal_response[prev_play] + "R",
    ideal_response[prev_play] + "P",
    ideal_response[prev_play] + "S",
  ]
  
  sub_order = {
    k: play_order[k]
    for k in potential_plays if k in play_order
  }

  if len(opponent_history) <= 3:
    return 'S'

  for key, value in sub_order.items():
    if value == min(sub_order.values()):
      prediction = key[1]
      
  return prediction