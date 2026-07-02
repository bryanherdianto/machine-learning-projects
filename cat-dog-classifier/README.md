# Cat and Dog Image Classifier

## What this project does

This project builds a **Convolutional Neural Network (CNN)** that looks at a photo and decides: is it a **cat** or a **dog**?

CNNs are specialized neural networks for images. Instead of looking at raw pixels one by one, they use **filters** that scan across the image and detect visual patterns — first simple edges, then textures, then complex shapes like ears or snouts.

The model must correctly identify at least **63%** of 50 test images to pass the challenge.

## The dataset

The dataset contains RGB images of cats and dogs, organized in folders:

| Split          | Images | Purpose                                        |
| -------------- | ------ | ---------------------------------------------- |
| **Training**   | 2,000  | The model learns from these                    |
| **Validation** | 1,000  | Used to monitor training (prevent overfitting) |
| **Test**       | 50     | Final check — the model has never seen these   |

All images are resized to **150×150 pixels**.

## How it works (in simple terms)

### Step 1 — Load & rescale images

Images are loaded from disk in batches and **rescaled** from 0–255 (raw pixel values) to 0–1 (normalized). This helps the neural network learn faster.

### Step 2 — Data augmentation

With only 2,000 training images, the model might **overfit** — memorize the training photos instead of learning what "cat-ness" and "dog-ness" look like in general.

**Data augmentation** fixes this by creating "new" training examples on the fly. Each image is randomly:

- **Rotated** up to 20°
- **Flipped** horizontally
- **Sheared** (slightly skewed)
- **Zoomed** in randomly

This effectively multiplies the training data and forces the model to learn patterns that work regardless of orientation or position.

### Step 3 — Build the CNN

| Layer                        | What it does                                                                                   |
| ---------------------------- | ---------------------------------------------------------------------------------------------- |
| **Conv2D (32 filters, 3×3)** | Scans the image with 32 small 3×3 windows, each detecting a different pattern (edges, corners) |
| **MaxPooling (2×2)**         | Shrinks the image by half, keeping only the strongest signals                                  |
| **Conv2D (64 filters, 3×3)** | Detects 64 more complex patterns (textures, shapes)                                            |
| **MaxPooling (2×2)**         | Shrinks again                                                                                  |
| **Conv2D (64 filters, 3×3)** | Detects 64 even higher-level features                                                          |
| **Flatten**                  | Converts the 2D grid of features into a 1D list                                                |
| **Dense (64, ReLU)**         | A fully-connected layer that combines all features into a decision                             |
| **Dense (1, sigmoid)**       | Outputs a single number: 0 = cat, 1 = dog                                                      |

### Step 4 — Train for 15 epochs

The model sees the training images 15 times (15 **epochs**). After each epoch, it checks its accuracy on the validation set. The `adam` optimizer adjusts the filters automatically to reduce errors.

### Step 5 — Predict on test images

After training, the model predicts a probability (0 to 1) for each of the 50 test images. Values above 0.5 → dog, below 0.5 → cat.

## How to run it

### Option 1 — Google Colab (recommended)

1. Upload `notebook.ipynb` to [Google Colab](https://colab.research.google.com).
2. Set runtime to **GPU**: **Runtime → Change runtime type → T4 GPU** (speeds up training significantly).
3. Click **Runtime → Run all** (`Ctrl + F9`).
4. The notebook downloads the data, trains the CNN, and runs the test automatically.
5. Training takes about 5–15 minutes with GPU (longer on CPU).

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
4. Run each cell from top to bottom. Training on CPU may take 10–30 minutes.

## What each cell does

| Cell                  | What it does                                                  |
| --------------------- | ------------------------------------------------------------- |
| 1 (Imports)           | Load TensorFlow, Keras, matplotlib; set random seeds          |
| 2 (Download)          | Download & unzip the cat/dog dataset; count images            |
| 3 (Generators)        | Create `ImageDataGenerator` for train/val/test with rescaling |
| 4 (plotImages)        | Helper function to display images + sample training images    |
| 5 (Augmentation)      | Create augmented image generator with random transformations  |
| 6 (Augmented samples) | Show 5 augmented versions of one image                        |
| 7 (Model)             | Build the CNN (3× Conv2D+MaxPool → Dense)                     |
| 8 (Train)             | Train for 15 epochs with `steps_per_epoch` using `np.ceil`    |
| 9 (Visualize)         | Plot training vs. validation accuracy and loss                |
| 10 (Predict)          | Grab test images, predict probabilities, display results      |
| 11 (Test)             | **Official freeCodeCamp grader**                              |

## Dependencies

| Library      | What it's for                                              |
| ------------ | ---------------------------------------------------------- |
| `tensorflow` | The CNN framework (Conv2D, MaxPooling, ImageDataGenerator) |
| `numpy`      | Array operations (ceil, flatten, round)                    |
| `matplotlib` | Plotting training curves and test image predictions        |

## Files in this project

```
cat-dog-classifier/
├── README.md          ← you are here
├── notebook.ipynb     ← the notebook (open this!)
└── requirements.txt   ← Python dependencies
```
