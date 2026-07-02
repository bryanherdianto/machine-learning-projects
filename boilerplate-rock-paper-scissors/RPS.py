"""
Rock Paper Scissors — ML Player (Markov Chain)

Uses a variable-order Markov chain to learn each opponent's patterns
during play. Two models run in parallel:

1. Opponent self-pattern (opp -> opp):
   "after the opponent's last k moves, what do they play next?"
   Captures bots with fixed cycles (e.g., quincy's RRPPS loop).

2. Cross-response (me -> opp):
   "after my last k moves, how does the opponent respond?"
   Captures bots that react to my moves (kris, mrugesh, abbey).

Each turn: update both models with the opponent's latest move,
predict the opponent's next move, and play the counter.

Model selection uses Laplace-smoothed confidence to pick the most
reliable predictor, and exponential decay (0.95) lets the model
track opponents that change strategy over time (e.g., abbey).
"""

from collections import defaultdict


class MarkovPlayer:
    """Variable-order Markov chain that learns opponent patterns online."""

    def __init__(self, max_order=3, decay=0.95):
        self.max_order = max_order
        self.decay = decay
        self.my_history = []
        self.opp_history = []
        self.opp_model = defaultdict(lambda: defaultdict(float))
        self.me_model = defaultdict(lambda: defaultdict(float))

    def _update(self, prev_play):
        """Update both models with the opponent's latest move."""
        for k in range(1, min(self.max_order, len(self.opp_history) - 1) + 1):
            ctx = "".join(self.opp_history[-(k + 1) : -1])
            if ctx:
                for move in self.opp_model[ctx]:
                    self.opp_model[ctx][move] *= self.decay
                self.opp_model[ctx][prev_play] += 1

        for k in range(1, min(self.max_order, len(self.my_history) - 1) + 1):
            ctx = "".join(self.my_history[-(k + 1) : -1])
            if ctx:
                for move in self.me_model[ctx]:
                    self.me_model[ctx][move] *= self.decay
                self.me_model[ctx][prev_play] += 1

    def _predict(self):
        """Predict the opponent's next move using the most reliable model."""
        best_pred = None
        best_score = 0.0

        for k in range(1, min(self.max_order, len(self.my_history)) + 1):
            ctx = "".join(self.my_history[-k:])
            counts = self.me_model.get(ctx)
            if counts:
                total = sum(counts.values())
                if total > 0:
                    top_move = max(counts, key=counts.get)
                    score = (counts[top_move] + 1) / (total + 3)
                    if score > best_score:
                        best_score = score
                        best_pred = top_move

        for k in range(1, min(self.max_order, len(self.opp_history)) + 1):
            ctx = "".join(self.opp_history[-k:])
            counts = self.opp_model.get(ctx)
            if counts:
                total = sum(counts.values())
                if total > 0:
                    top_move = max(counts, key=counts.get)
                    score = (counts[top_move] + 1) / (total + 3)
                    if score > best_score:
                        best_score = score
                        best_pred = top_move

        if best_pred:
            return best_pred

        if self.opp_history:
            freq = {"R": 0, "P": 0, "S": 0}
            for m in self.opp_history:
                if m in freq:
                    freq[m] += 1
            return max(freq, key=freq.get)

        return "R"

    def play(self, prev_play):
        ideal_response = {"R": "P", "P": "S", "S": "R"}

        if prev_play != "":
            self.opp_history.append(prev_play)
            self._update(prev_play)

        prediction = self._predict()
        my_move = ideal_response[prediction]
        self.my_history.append(my_move)
        return my_move


class Player:
    """Wraps MarkovPlayer as a callable matching the game's player interface."""

    def __init__(self):
        self.model = MarkovPlayer(max_order=3, decay=0.95)

    def __call__(self, prev_play):
        return self.model.play(prev_play)


player_quincy = Player()
player_kris = Player()
player_mrugesh = Player()
player_abbey = Player()
