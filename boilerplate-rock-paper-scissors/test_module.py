import unittest
from RPS_game import play, mrugesh, abbey, quincy, kris
from RPS import player_quincy, player_kris, player_abbey, player_mrugesh

class UnitTests(unittest.TestCase):
    print()
  
    def test_player_vs_quincy(self):
        print("Testing game against quincy...")
        actual = play(player_quincy, quincy, 1000) >= 60
        self.assertTrue(
            actual,
            'Expected player to defeat quincy at least 60% of the time.')

    def test_player_vs_abbey(self):
        print("Testing game against abbey...")
        actual = play(player_abbey, abbey, 1000) >= 60
        self.assertTrue(
            actual,
            'Expected player to defeat abbey at least 60% of the time.')

    def test_player_vs_kris(self):
        print("Testing game against kris...")
        actual = play(player_kris, kris, 1000) >= 60
        self.assertTrue(
            actual, 'Expected player to defeat kris at least 60% of the time.')

    def test_player_vs_mrugesh(self):
        print("Testing game against mrugesh...")
        actual = play(player_mrugesh, mrugesh, 1000) >= 60
        self.assertTrue(
            actual,
            'Expected player to defeat mrugesh at least 60% of the time.')


if __name__ == "__main__":
    unittest.main()
