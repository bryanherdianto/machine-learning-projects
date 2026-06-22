# Analisis Sentimen Pilpres 2024: Perbandingan RNN, LSTM, dan GRU

> Link Google Colab: https://colab.research.google.com/drive/1V5x3ueBjGmk7cdL-1xVj5UD8VzfwVGPA?usp=sharing  
> Link Demo: https://youtu.be/d7uHhrlRqZ8

Notebook ini membandingkan tiga arsitektur Recurrent Neural Network (RNN, LSTM, dan GRU) untuk mengklasifikasikan sentimen opini publik terkait Pemilihan Presiden Indonesia 2024.

## Anggota Kelompok (Selasa-10)

| Nama                      | NPM        |
| ------------------------- | ---------- |
| Muhammad Hilmi Al Muttaqi | 2306267082 |
| Reyhan Ahnaf Deannova     | 2306267100 |
| Bryan Herdianto           | 2306210885 |
| Adhikananda Wira Januar   | 2306267113 |

## Dataset

Dataset diambil dari Kaggle: [Indonesia Presidential Candidates Dataset 2024](https://www.kaggle.com/datasets/jocelyndumlao/indonesia-presidential-candidates-dataset-2024). Berisi tweet berlabel sentimen (Positive, Negative, Neutral) untuk tiga pasangan calon presiden.

## Arsitektur Model

| Model      | Layer Recurrent | Bidirectional | Unit |
| ---------- | --------------- | ------------- | ---- |
| Simple RNN | SimpleRNN       | Tidak         | 128  |
| LSTM       | LSTM            | Ya            | 128  |
| GRU        | GRU             | Ya            | 128  |

## Cara Menjalankan

1. Buka `notebook.ipynb` di Google Colab atau Jupyter Notebook
2. Install dependensi: `pip install kagglehub tensorflow scikit-learn matplotlib seaborn`
3. Jalankan semua cell secara berurutan

## Preprocessing

- Case folding (huruf kecil)
- Hapus URL, mention, hashtag
- Hapus tanda baca dan angka
- Tokenisasi + padding (max 10.000 kata, panjang 100 token)

## Metrik Evaluasi

Accuracy, Precision, Recall, F1-Score, dan Confusion Matrix
