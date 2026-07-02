# Artificial Neural Network from Scratch

## What this project does

This notebook builds a **neural network from scratch** — using only **NumPy** (no TensorFlow, no PyTorch, no Keras). The network learns to classify points in a spiral pattern into **3 classes**.

### What does "from scratch" mean?

When you use a framework like TensorFlow, you write something like `model.fit(x, y)` and it handles everything — the math, the gradients, the weight updates. In this notebook, **we write all that math ourselves**:

- **Matrix multiplication** (`np.dot`) for the forward pass
- **Gradient computation** (derivatives) for the backward pass (backpropagation)
- **Weight updates** (SGD optimizer) by hand

This is the best way to truly understand how neural networks work under the hood.

## The dataset

We use the **spiral dataset** from the [`nnfs`](https://pypi.org/project/nnfs/) (Neural Networks From Scratch) package. It generates 600 data points arranged in 3 spiral arms:

| Property      | Value                         |
| ------------- | ----------------------------- |
| Total samples | 600 (200 per class)           |
| Features      | 2 (x, y coordinates)          |
| Classes       | 3 (one per spiral arm)        |
| Difficulty    | Hard — not linearly separable |

A spiral is a challenging pattern because the classes intertwine — you can't just draw a straight line to separate them. The neural network has to learn a **non-linear** decision boundary.

## The architecture

```
Input (2 features)
    ↓
Dense layer (2 → 64 neurons)    — learns patterns from the 2D coordinates
    ↓
ReLU activation                 — introduces non-linearity (lets the network learn curves, not just lines)
    ↓
Dense layer (64 → 3 neurons)    — outputs 3 scores (one per class)
    ↓
Softmax + Cross-Entropy Loss    — converts scores to probabilities + measures error
```

### Classes implemented in the notebook

| Class                     | What it does                                                                                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `Dense`                   | A fully-connected layer: `output = dot(input, weights) + biases`. Has `forward()` and `backward()` methods.                          |
| `ReLU`                    | Activation function: `max(0, x)`. Turns negative values to zero, keeping positives.                                                  |
| `LeakyRelu`               | Like ReLU but allows a small negative slope (0.05x) — prevents "dying ReLU" problem.                                                 |
| `Sigmoid`                 | Activation that squashes values to 0–1 range: `1 / (1 + e^(-x))`.                                                                    |
| `Linear`                  | Pass-through (no activation) — output = input.                                                                                       |
| `Tanh`                    | Activation that squashes to -1 to 1 range.                                                                                           |
| `Softmax`                 | Converts raw scores to probabilities (all sum to 1). Used for the output layer.                                                      |
| `CategoricalCrossEntropy` | Loss function: measures how far predictions are from true labels.                                                                    |
| `CalcSoftmaxLossGrad`     | Fused Softmax + Loss backward — combines both for a simpler, more stable gradient.                                                   |
| `Optimizer_SGD`           | Stochastic Gradient Descent: updates weights using `weights -= learning_rate * gradient`. Supports momentum and learning-rate decay. |

## Training

- **Optimizer**: SGD with learning rate = 0.2, decay = 0.001, momentum = 0.9
- **Epochs**: 10,000 (full passes over the data)
- **Loss function**: Categorical Cross-Entropy
- **Early in training**: loss starts high (~1.0), accuracy near 33% (random guessing for 3 classes)
- **After 10,000 epochs**: **Loss: 0.229, Accuracy: 91%**

The notebook also plots the loss and accuracy curves over all 10,000 epochs, so you can see how the network gradually learns.

## How to run it

### Option 1 — Google Colab (easiest)

1. Upload `notebook.ipynb` to [Google Colab](https://colab.research.google.com).
2. Click **Runtime → Run all** (`Ctrl + F9`).
3. The first cell installs `nnfs` automatically.
4. Training takes about 10–30 seconds (CPU is fine — no GPU needed since it's pure NumPy).

### Option 2 — Run on your own computer

1. Install **Python 3.10+** from [python.org](https://www.python.org).
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Open the notebook:
   ```
   jupyter notebook notebook.ipynb
   ```
4. Run each cell from top to bottom (`Shift + Enter`).

## What each cell does

| Cell  | What it does                                                                                                            |
| ----- | ----------------------------------------------------------------------------------------------------------------------- |
| 1     | Install the `nnfs` package                                                                                              |
| 2     | Import NumPy, `nnfs.datasets.spiral_data`, and matplotlib                                                               |
| 3     | Define all ANN classes (Dense, ReLU, Sigmoid, Softmax, Loss, CrossEntropy, SGD optimizer, etc.)                         |
| 4     | Demo: `np.exp(100)` overflow warning (motivates numerical stability)                                                    |
| 5–13  | **Testing with simple input**: manual forward pass through 2 Dense layers + ReLU + Softmax to verify shapes and outputs |
| 14–15 | **Load the spiral dataset**: 200 samples × 3 classes, plot the scatter                                                  |
| 16–20 | Inspect data shapes and visualize the spiral                                                                            |
| 21    | Initialize layers, activation, loss, and optimizer                                                                      |
| 22    | **Training loop**: 10,000 epochs of forward + backward propagation + weight updates                                     |
| 23    | Plot loss and accuracy curves over training                                                                             |
| 24–28 | **Test the trained model**: define `get_y_pred()`, predict on a dummy input `[0.1, 0.2]`                                |

## Dependencies

| Library      | What it's for                                                  |
| ------------ | -------------------------------------------------------------- |
| `numpy`      | All math operations (matrix multiplication, gradients, arrays) |
| `nnfs`       | Provides the spiral dataset used for training                  |
| `matplotlib` | Plotting the dataset, loss curve, and accuracy curve           |

All three are lightweight — no deep learning framework needed!

## Files in this project

```
artificial-neural-network/
├── README.md          ← you are here
├── notebook.ipynb     ← the notebook (open this!)
└── requirements.txt   ← Python dependencies
```
