# SMS Text Classification — Ham or Spam?

## What this project does

Have you ever gotten a text message like _"CONGRATULATIONS! You've won $1,000,000!"_? That's **spam** — an unwanted ad or scam. A normal text from a friend like _"Hey, are we still on for Friday?"_ is **ham** (not spam).

This project trains an **artificial brain** (a neural network) to read a text message and guess whether it's ham or spam. It's like building a spam filter for your phone.

At the end, you get a function called `predict_message()` that takes any message and returns:

```python
predict_message("you have won £1000 cash! call to claim your prize.")
# -> [0.987, "spam"]

predict_message("hey, are you free for lunch tomorrow?")
# -> [0.012, "ham"]
```

- The **first number** is the model's confidence that the message is spam (0 = definitely ham, 1 = definitely spam).
- The **second word** is the final label: `"ham"` or `"spam"`. If the confidence is 0.5 or higher, it's spam; otherwise, it's ham.

## How to run it

### Option 1 — Google Colab (easiest, no setup needed)

1. Go to [colab.research.google.com](https://colab.research.google.com).
2. Upload the file `fcc_sms_text_classification.ipynb`.
3. Click **Runtime → Run all** (or press `Ctrl + F9`).
4. The notebook downloads the data, trains the model, and runs the test automatically.
5. If everything works, you'll see this at the bottom:

   > **You passed the challenge. Great job!**

Training takes about 2–5 minutes on a free Colab instance.

### Option 2 — Run on your own computer

1. Install **Python 3.10 or newer** from [python.org](https://www.python.org).
2. Open a terminal in this folder and install the dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Start Jupyter and open the notebook:

   ```
   jupyter notebook fcc_sms_text_classification.ipynb
   ```

4. Run each cell from top to bottom (click the ▶ button or press `Shift + Enter`).

## The dataset

We use the **SMS Spam Collection** dataset, provided by freeCodeCamp. It contains thousands of real SMS messages, each labeled as `ham` or `spam`.

The data comes in two files that the notebook downloads automatically:

| File             | Purpose                     | Approx. size    |
| ---------------- | --------------------------- | --------------- |
| `train-data.tsv` | Used to **train** the model | ~4,200 messages |
| `valid-data.tsv` | Used to **test** the model  | ~1,400 messages |

Each file is a **TSV** (tab-separated values) spreadsheet with two columns:

| type | message                                        |
| ---- | ---------------------------------------------- |
| ham  | Hey are you free for lunch tomorrow?           |
| spam | WINNER!! You have won a £1000 prize. Call now! |

## How the model works (in simple terms)

### Step 1 — Load the messages

We load thousands of real text messages that are already labeled as "ham" or "spam" into a table (a pandas DataFrame).

### Step 2 — Clean the text

We convert everything to lowercase, remove HTML tags, and strip punctuation. This way the model focuses on the _words_ themselves, not on capitalization or symbols.

### Step 3 — Turn words into numbers

Neural networks can't read words — they only understand numbers. So we give each unique word its own integer ID (like a student ID number). For example:

```
"free"    -> 42
"winner"  -> 1337
"hello"   -> 5
```

A layer called `TextVectorization` handles this automatically.

### Step 4 — Learn word meanings with an Embedding

Each word ID gets turned into a list of 64 numbers (a **vector**). These numbers start random, but during training the model adjusts them so that words with similar meanings end up with similar numbers. This is called an **embedding** — the model is "learning what each word means."

### Step 5 — Read the message with a Bidirectional LSTM

An **LSTM** (Long Short-Term Memory) is a type of neural network that reads words _in order_ and remembers context. For example, it can learn that "you have won" followed by "call to claim" is probably spam, even if no single word is suspicious on its own.

We use a **Bidirectional** LSTM, which reads the message both **forward and backward**. This helps it catch patterns that might be clearer from either direction.

### Step 6 — Handle the ham/spam imbalance

The dataset has way more ham messages than spam messages (about 87% ham, 13% spam). Without fixing this, the model would just guess "ham" for everything and still be 87% accurate — but it would catch zero spam.

We fix this with **class weights**. Think of it like a teacher saying _"pay extra attention when you see a spam example."_ This forces the model to learn both types fairly, not just the majority.

### Step 7 — Output a confidence score

The final layer outputs a single number between 0 and 1 (a **sigmoid** function squashes the output into this range):

- Close to **0** → the model thinks it's ham
- Close to **1** → the model thinks it's spam
- **0.5** is the decision boundary: anything ≥ 0.5 is labeled spam

## What each cell in the notebook does

| Cell                | What it does                                                                       |
| ------------------- | ---------------------------------------------------------------------------------- |
| **1** (Imports)     | Load the Python libraries we need and set random seeds so results are reproducible |
| **2** (Download)    | Download the dataset from freeCodeCamp's server (skips if already downloaded)      |
| **3** (Load data)   | Read the TSV files into pandas DataFrames                                          |
| **4** (Labels)      | Convert "ham"/"spam" text labels to 0/1 numbers                                    |
| **5** (Vectorize)   | Clean text + convert words to integer IDs                                          |
| **6** (Build model) | Create the neural network (Embedding → Bidirectional LSTM → Dense)                 |
| **7** (Train)       | Train the model with class weights and early stopping                              |
| **8** (Evaluate)    | Test the trained model on the held-out test set                                    |
| **9** (Predict)     | Define `predict_message()` and try it on example messages                          |
| **10** (Grader)     | **Official freeCodeCamp test cell**                                                |

## Dependencies

| Library      | What it's for                                                  |
| ------------ | -------------------------------------------------------------- |
| `tensorflow` | The neural network framework (LSTM, Embedding, training, etc.) |
| `pandas`     | Loading and manipulating the TSV data files                    |
| `numpy`      | Numerical operations (arrays, class weight computation)        |

All three come pre-installed on Google Colab. If running locally, use `requirements.txt`.

## Files in this project

```
sms-text-classification/
├── README.md                              ← you are here
├── fcc_sms_text_classification.ipynb      ← the notebook (open this!)
└── requirements.txt                       ← Python dependencies (for local use)
```
