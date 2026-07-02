# Book Recommendation Engine using KNN

## What this project does

Have you ever seen "Customers who bought this also bought..." on Amazon? This project does exactly that — but for books.

Given a book title, the system finds **5 similar books** based on the reading patterns of thousands of users. The idea is simple: if many users who rated _Book A_ highly also rated _Book B_ highly, those books are probably similar in genre or appeal.

## The dataset

The **Book-Crossings dataset** contains:

| File                  | Contents                                   |
| --------------------- | ------------------------------------------ |
| `BX-Books.csv`        | Book metadata: ISBN, title, author         |
| `BX-Book-Ratings.csv` | User ratings: user ID, ISBN, rating (1–10) |

Overall: **1.1 million ratings** of **270,000 books** by **90,000 users**.

### Filtering for quality

Most books are rated by only a handful of users — not enough to draw reliable conclusions. So we filter:

- **Remove users** with fewer than 200 ratings (they don't have enough reading history to be useful)
- **Remove books** with fewer than 100 ratings (not enough consensus on them)

This ensures that the recommendations are based on statistically meaningful data.

## How it works (in simple terms)

### Step 1 — Create a book-user matrix

Imagine a giant spreadsheet where:

- Each **row** is a book
- Each **column** is a user
- Each **cell** contains that user's rating for that book (or 0 if they didn't rate it)

This is called a **pivot table**. Each row is a "rating fingerprint" for a book.

### Step 2 — Measure similarity with cosine distance

To find books similar to a given book, we compare its rating fingerprint to every other book's fingerprint. We use **cosine distance** — it measures the _angle_ between two vectors, ignoring their length.

If two books have similar rating patterns (the same users liked them), their fingerprints point in a similar direction, so the cosine distance is small.

### Step 3 — Find the 5 nearest neighbors

The **K-Nearest Neighbors (KNN)** algorithm finds the 6 closest books (by cosine distance), skips the book itself, and returns the remaining 5 as recommendations — sorted from most distant to closest, as the challenge expects.

## How to run it

### Option 1 — Google Colab (easiest)

1. Upload `notebook.ipynb` to [Google Colab](https://colab.research.google.com).
2. Click **Runtime → Run all** (`Ctrl + F9`).
3. The notebook downloads the data, builds the KNN model, and runs the test automatically.
4. If everything works, you'll see:

   > **You passed the challenge!**

Training takes about 1–2 minutes (CPU is fine — KNN has no training phase, just a lookup).

### Option 2 — Run on your own computer

1. Install **Python 3.10+**.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Open the notebook:
   ```
   jupyter notebook notebook.ipynb
   ```
4. Run each cell from top to bottom.

## What each cell does

| Cell                | What it does                                                  |
| ------------------- | ------------------------------------------------------------- |
| 1 (Imports)         | Load numpy, pandas, sklearn's NearestNeighbors                |
| 2 (Download)        | Download & unzip the Book-Crossings dataset                   |
| 3 (Load CSVs)       | Read `BX-Books.csv` and `BX-Book-Ratings.csv` into DataFrames |
| 4–7 (Inspect)       | Show `.head()` and `.info()` for both DataFrames              |
| 8 (Count users)     | Count how many ratings each user has                          |
| 9 (Count books)     | Count how many ratings each book has                          |
| 10 (Filter)         | Remove users with < 200 ratings and books with < 100 ratings  |
| 11 (Merge)          | Join books and ratings on ISBN                                |
| 12 (Pivot)          | Create the book × user matrix, fill missing with 0            |
| 13 (KNN)            | Fit NearestNeighbors with cosine distance                     |
| 14 (get_recommends) | Define the recommendation function                            |
| 15 (Test)           | **Official freeCodeCamp grader**                              |

## Dependencies

| Library        | What it's for                       |
| -------------- | ----------------------------------- |
| `pandas`       | Loading CSVs, merging, pivot tables |
| `numpy`        | Array operations for the KNN input  |
| `scikit-learn` | The `NearestNeighbors` algorithm    |

## Files in this project

```
book-recommendation/
├── README.md          ← you are here
├── notebook.ipynb     ← the notebook (open this!)
└── requirements.txt   ← Python dependencies
```
