# This entrypoint file to be used in development. Start by reading README.md
from RPS_game import play, mrugesh, abbey, quincy, kris, human, random_player
from RPS import player_quincy, player_kris, player_abbey, player_mrugesh
from unittest import main

# print('Abbey:')
# play(player_abbey, abbey, 1000)
# print('\nQuincy:')
# play(player_quincy, quincy, 1000)
# print('\nKris:')
# play(player_kris, kris, 1000)
# print('\nMrugesh:')
# play(player_mrugesh, mrugesh, 1000)

# Uncomment line below to play interactively against a bot:
# play(human, abbey, 20, verbose=True)

# Uncomment line below to play against a bot that plays randomly:
# play(human, random_player, 1000)

# Uncomment line below to run unit tests automatically
main(module='test_module', exit=False)