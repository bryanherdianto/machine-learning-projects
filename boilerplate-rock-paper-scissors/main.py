# This entrypoint file to be used in development. Start by reading README.md
from RPS_game import play, mrugesh, abbey, quincy, kris
from RPS import player_quincy, player_kris, player_abbey, player_mrugesh
from unittest import main

# Uncomment lines below to watch each ML player compete:
# play(player_abbey, abbey, 1000)
# play(player_quincy, quincy, 1000)
# play(player_kris, kris, 1000)
# play(player_mrugesh, mrugesh, 1000)

# Uncomment to play interactively against a bot:
# from RPS_game import human
# play(human, abbey, 20, verbose=True)

# Uncomment to play against a random bot:
# from RPS_game import random_player
# play(human, random_player, 1000)

# Run unit tests:
main(module="test_module", exit=False)
