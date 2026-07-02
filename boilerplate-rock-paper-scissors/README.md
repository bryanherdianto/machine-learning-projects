# Rock Paper Scissors — ML Player

## What this project does

You play 1000 games of Rock Paper Scissors against four different bots. Your job: write a player that **learns each opponent's pattern** and beats them at least 60% of the time.

Instead of hardcoding a different strategy for each bot, this project uses a single **Markov chain** machine-learning approach that **learns online** — it starts knowing nothing and gets smarter with every move played.

## The four opponent bots

All bots are defined in `RPS_game.py`. Each has a different strategy:

| Bot         | Strategy                    | How it decides                                                                    |
| ----------- | --------------------------- | --------------------------------------------------------------------------------- |
| **Quincy**  | Fixed cycle                 | Plays `R → R → P → P → S` on repeat, forever                                      |
| **Kris**    | React to your last move     | Always plays the counter to whatever you just played                              |
| **Mrugesh** | React to your recent habits | Plays the counter to your most frequent move in the last 10 turns                 |
| **Abbey**   | Predict your next move      | Builds a 2-gram Markov model of YOUR moves, predicts your next, plays the counter |

## How the ML player works

### The big idea: Markov chain

A **Markov chain** is a simple ML model that learns "what usually comes next?" from sequences. For example, if the opponent played `R, R, P, P, S, R, R, P, ...`, the model learns:

- After `RR` → the opponent usually plays `P`
- After `RP` → the opponent usually plays `P`
- After `PP` → the opponent usually plays `S`

Once the model can predict the opponent's next move, we play the **counter** (the move that beats it).

### Two models in parallel

Some bots (quincy) follow their own fixed pattern. Others (kris, mrugesh, abbey) react to _my_ moves. So the player runs two models simultaneously:

| Model                           | What it tracks                                                 | Catches                                       |
| ------------------------------- | -------------------------------------------------------------- | --------------------------------------------- |
| **Self-pattern** (`opp → opp`)  | "After the opponent's last _k_ moves, what do they play next?" | Quincy (fixed cycle)                          |
| **Cross-response** (`me → opp`) | "After my last _k_ moves, how does the opponent respond?"      | Kris, Mrugesh, Abbey (they react to my moves) |

Each turn, the player checks **both** models at orders 1, 2, and 3 (1-gram, 2-gram, 3-gram), and picks the prediction from the model with the highest **confidence** — measured with Laplace smoothing `(count + 1) / (total + 3)` so that a model with lots of data beats one that just got lucky once.

### Exponential decay

Opponents like Abbey are also learning — their strategy changes over time. To keep up, the model applies **0.95 exponential decay** to old counts on every update. This means recent games matter more than old ones, letting the player adapt when Abbey's behavior shifts.

### The timing trick

The opponent's move at turn _t_ is a response to my move at turn _t−1_ (not _t_ — I haven't played yet). So the model updates with the **2-turn-old** context (`my_history[-2]` → opponent's response) but predicts using the **1-turn-old** context (`my_history[-1]` → expected response next turn).

## Results

| Opponent | Win Rate | Status  |
| -------- | -------- | ------- |
| Quincy   | 99.7%    | ✅ Pass |
| Kris     | 99.9%    | ✅ Pass |
| Mrugesh  | 83.9%    | ✅ Pass |
| Abbey    | 65.8%    | ✅ Pass |

All four pass the ≥60% threshold.

## How to run

```bash
cd boilerplate-rock-paper-scissors
python main.py
```

This runs the 4 unit tests automatically. You should see:

```
Testing game against abbey...
Player 1 win rate: 65.76%
Testing game against kris...
Player 1 win rate: 99.90%
Testing game against mrugesh...
Player 1 win rate: 83.90%
Testing game against quincy...
Player 1 win rate: 99.70%

OK
```

To play interactively against a bot, uncomment the relevant lines in `main.py`.

## File structure

```
boilerplate-rock-paper-scissors/
├── README.md          ← you are here
├── RPS.py             ← the ML player (Markov chain) — the main deliverable
├── RPS_game.py        ← game engine + 4 opponent bots
├── test_module.py     ← unit tests (≥60% win rate vs each bot)
├── main.py            ← development entrypoint (runs tests)
└── requirements.txt   ← no external dependencies (Python stdlib only)
```

## Dependencies

**None!** This project uses only the Python standard library (`collections`, `random`, `unittest`). No TensorFlow, no NumPy, no external packages needed.
