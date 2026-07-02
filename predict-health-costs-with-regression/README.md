# Predict Health Costs with Regression

## What this project does

Imagine you work for an insurance company. You have data about thousands of customers — their age, gender, BMI, number of children, whether they smoke, and where they live. You also know how much each person costs in healthcare expenses.

Your goal: **build a model that reads a person's info and predicts their healthcare costs.**

This is called **regression** — predicting a number (the cost in dollars) from input features. It's different from **classification** (like the SMS spam project), where you predict a category (ham/spam).

To pass the challenge, the model's predictions must be within **$3,500** of the actual cost (on average).

## The dataset

We use the **Insurance dataset**, provided by freeCodeCamp. It's a CSV file with 1,338 rows and 7 columns:

| Column     | Type     | Example values              | Description                                         |
| ---------- | -------- | --------------------------- | --------------------------------------------------- |
| `age`      | Number   | 18, 21, 50, 61              | The person's age                                    |
| `sex`      | Category | `male`, `female`            | Biological sex                                      |
| `bmi`      | Number   | 25.8, 31.0, 36.9            | Body Mass Index (a health metric)                   |
| `children` | Number   | 0, 1, 2, 3                  | Number of children covered by insurance             |
| `smoker`   | Category | `yes`, `no`                 | Whether the person smokes                           |
| `region`   | Category | `southwest`, `northeast`... | Where the person lives (4 regions)                  |
| `expenses` | Number   | 1629.83, 29141.36           | **Annual healthcare costs** (the target to predict) |

The notebook downloads this file automatically from `cdn.freecodecamp.org`.

## How the model works (in simple terms)

### Step 1 — Convert categories to numbers

Neural networks only understand numbers, so we convert text categories:

- **Binary features** (`sex`, `smoker`): These have only 2 values, so we map them to 0/1. For example, `smoker`: `no` → 0, `yes` → 1.
- **Multi-valued feature** (`region`): This has 4 values (`southwest`, `southeast`, `northwest`, `northeast`). If we mapped them to 0/1/2/3, the model would think `northeast` (3) is "more" than `southwest` (0) — which makes no sense! So instead we use **one-hot encoding**: create 4 new yes/no columns (one per region). Only one column is "1" for each person.

### Step 2 — Normalize the numbers

The features have very different scales: `age` ranges from 18–64, `bmi` from 15–53, `children` from 0–5. If we feed these raw numbers to the model, it struggles — the large numbers (`age`) dominate the small ones (`children`), and the model takes forever to learn.

**Normalization** fixes this: for each feature, subtract the average and divide by the spread (standard deviation). After normalization, every feature has an average of 0 and a spread of 1. The model can learn much faster and more fairly.

We use a Keras `Normalization` layer that learns the averages from the **training data only** (so we don't accidentally cheat by looking at the test data).

### Step 3 — Build the neural network

A simple **feed-forward neural network** with 4 layers:

| Layer                | What it does                                                     |
| -------------------- | ---------------------------------------------------------------- |
| **Normalization**    | Subtracts the average and divides by the spread for each feature |
| **Dense (64, ReLU)** | 64 "neurons" that learn patterns from the normalized input       |
| **Dense (64, ReLU)** | Another 64 neurons that learn deeper patterns                    |
| **Dense (1)**        | A single output neuron — the predicted cost in dollars           |

The output layer has **no activation function** (called "linear"), which is standard for regression. This lets the model predict any positive number.

### Step 4 — Train with early stopping

We split the data: 80% for **training** (the model learns from this) and 20% for **testing** (we check the model on data it has never seen).

During training, we also hold out 20% of the training data as a **validation set** to monitor performance. **Early stopping** watches the validation error — if it stops improving for 20 epochs in a row, training halts automatically. This saves time and prevents **overfitting** (memorizing the training data instead of learning general patterns).

The model uses **MSE** (Mean Squared Error) as its loss function — it penalizes large errors more than small ones. We also track **MAE** (Mean Absolute Error) because the challenge checks MAE < 3500.

## How to run it

### Option 1 — Google Colab (easiest, no setup needed)

1. Upload `fcc_predict_health_costs_with_regression.ipynb` to [Google Colab](https://colab.research.google.com).
2. Click **Runtime → Run all** (or press `Ctrl + F9`).
3. The notebook downloads the data, trains the model, and runs the test automatically.
4. If everything works, you'll see:

   > **You passed the challenge. Great job!**

   A scatter plot will also appear showing predicted vs. actual costs.

Training takes about 1–3 minutes on a free Colab instance.

### Option 2 — Run on your own computer

1. Install **Python 3.10 or newer** from [python.org](https://www.python.org).
2. Open a terminal in this folder and install the dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Start Jupyter and open the notebook:

   ```
   jupyter notebook fcc_predict_health_costs_with_regression.ipynb
   ```

4. Run each cell from top to bottom (press `Shift + Enter`).

## What each cell in the notebook does

| Cell             | What it does                                                           |
| ---------------- | ---------------------------------------------------------------------- |
| **1** (Imports)  | Load Python libraries and set random seeds for reproducibility         |
| **2** (Download) | Download `insurance.csv` from freeCodeCamp's server                    |
| **3** (Inspect)  | Show dataset info and unique category values                           |
| **4** (Encode)   | Convert categories to numbers (ordinal for binary, one-hot for region) |
| **5** (Verify)   | Show the encoded dataset to confirm the conversion                     |
| **6** (Split)    | 80/20 train/test split + convert to NumPy arrays                       |
| **7** (Model)    | Build the neural network with a Normalization layer                    |
| **8** (Train)    | Train with EarlyStopping and a validation split                        |
| **9** (Test)     | **Grader for model's performance**                                     |
| **10** (Predict) | Make predictions on a sample data point                                |

## Dependencies

| Library      | What it's for                                                              |
| ------------ | -------------------------------------------------------------------------- |
| `tensorflow` | The neural network framework (Dense layers, Normalization, Adam optimizer) |
| `pandas`     | Loading and manipulating the CSV data                                      |
| `numpy`      | Numerical operations (arrays, statistics)                                  |
| `matplotlib` | Plotting predicted vs. actual costs                                        |

All four come pre-installed on Google Colab. If running locally, use `requirements.txt`.

## Files in this project

```
predict-health-costs-with-regression/
├── README.md                                      ← you are here
├── fcc_predict_health_costs_with_regression.ipynb  ← the notebook (open this!)
└── requirements.txt                               ← Python dependencies (for local use)
```
