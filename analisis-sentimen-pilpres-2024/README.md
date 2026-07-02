# Analisis Sentimen Pilpres 2024: Perbandingan RNN, LSTM, dan GRU

## Apa yang dilakukan proyek ini?

Bayangkan Anda membaca ribuan tweet tentang Pilpres 2024. Sebagian tweet positif ("Mantap, semoga menang!"), sebagian negatif ("Saya kecewa dengan debat tadi malam."). Proyek ini melatih **tiga jenis neural network** untuk membaca tweet dan menebak apakah sentimennya **positif** atau **negatif** secara otomatis.

Tiga model yang dibandingkan:

| Model          | Singkatannya             | Analogi                                                                                               |
| -------------- | ------------------------ | ----------------------------------------------------------------------------------------------------- |
| **Simple RNN** | Recurrent Neural Network | Seperti membaca kalimat kata per kata, hanya mengingat kata terakhir                                  |
| **LSTM**       | Long Short-Term Memory   | Seperti membaca dengan buku catatan — bisa mengingat informasi penting dari awal kalimat sampai akhir |
| **GRU**        | Gated Recurrent Unit     | Versi lebih ringan dari LSTM — catatannya lebih kecil tapi cepat                                      |

LSTM dan GRU menggunakan **Bidirectional** (membaca dari kiri ke kanan _dan_ kanan ke kiri), sehingga model bisa menangkap konteks dari kedua arah.

## Dataset

Dataset diambil dari Kaggle: [Indonesia Presidential Candidates Dataset 2024](https://www.kaggle.com/datasets/jocelyndumlao/indonesia-presidential-candidates-dataset-2024).

Dataset berisi tweet tentang tiga pasangan calon presiden:

| File CSV               | Kandidat         |
| ---------------------- | ---------------- |
| `Anies Baswedan.csv`   | Anies Baswedan   |
| `Ganjar Pranowo.csv`   | Ganjar Pranowo   |
| `Prabowo Subianto.csv` | Prabowo Subianto |

Setelah pembersihan (menghapus baris kosong), total ada **29.728 tweet** dengan 2 kelas sentimen:

| Sentimen     | Jumlah Tweet | Persentase |
| ------------ | ------------ | ---------- |
| **Positive** | 21.654       | 72,8%      |
| **Negative** | 8.074        | 27,2%      |

> **Catatan:** Hanya ada 2 kelas (Positive dan Negative). Tidak ada kelas "Neutral" di dataset ini.

Karena data tidak seimbang (jauh lebih banyak Positive daripada Negative), kita menggunakan **class weight** — teknik yang memberi bobot lebih besar pada kelas minoritas (Negative) agar model tidak hanya belajar menebak "Positive" untuk semua tweet.

## Bagaimana modelnya bekerja (penjelasan sederhana)

### Langkah 1 — Membersihkan teks (Preprocessing)

Tweet biasanya berantakan: ada URL, mention (`@username`), hashtag (`#tag`), tanda baca, dan angka. Semua itu dibersihkan agar model fokus pada kata-kata yang penting:

- **Case folding**: semua huruf diubah jadi huruf kecil
- **Hapus URL**: link seperti `https://...` dihilangkan
- **Hapus mention & hashtag**: `@username` dan `#` dihilangkan
- **Hapus tanda baca & angka**: hanya menyisakan huruf dan spasi

### Langkah 2 — Mengubah kata jadi angka (Tokenisasi)

Model hanya bisa membaca angka, bukan teks. Jadi setiap kata diberi ID unik (seperti nomor induk siswa):

- Membangun kamus dari **10.000 kata** paling sering muncul
- Kata di luar kamus diganti dengan `<OOV>` (Out-of-Vocabulary)
- Semua kalimat dipotong/disihi menjadi panjang **100 kata** (padding)

### Langkah 3 — Membangun neural network

Ketiga model punya struktur yang sama, hanya beda di layer recurrent-nya:

```
Embedding (128 dimensi)
    ↓
[SimpleRNN / Bidirectional LSTM / Bidirectional GRU] — 128 unit
    ↓
Dense (64 neuron, ReLU) + Dropout 0.3
    ↓
Dense (softmax) — output: probabilitas per kelas
```

| Komponen            | Fungsinya                                                                                       |
| ------------------- | ----------------------------------------------------------------------------------------------- |
| **Embedding**       | Mengubah kata (angka) menjadi vektor 128 dimensi yang merepresentasikan "makna" kata            |
| **Recurrent Layer** | Membaca urutan kata dan mengingat konteks. RNN = ingatan pendek, LSTM/GRU = ingatan panjang     |
| **Dense (ReLU)**    | Layer tersembunyi yang menggabungkan fitur yang dipelajari                                      |
| **Dropout**         | Mematikan 30% neuron secara acak saat training untuk mencegah overfitting (hafal data training) |
| **Dense (softmax)** | Output: probabilitas untuk setiap kelas (Positive/Negative)                                     |

### Langkah 4 — Training

- **Epoch** = 10 (maksimal), dengan **EarlyStopping** patience=2 (berhenti otomatis jika tidak membaik)
- **Batch size** = 64 (proses 64 tweet sekaligus)
- **Validation split** = 10% dari data training untuk memantau performa
- **Class weight** diterapkan agar model adil terhadap kelas minoritas

## Hasil Perbandingan

| Model          | Accuracy | Precision | Recall | F1-Score | Waktu Training |
| -------------- | -------- | --------- | ------ | -------- | -------------- |
| **Simple RNN** | 72,84%   | 53,06%    | 72,84% | 61,39%   | 21,8 detik     |
| **LSTM**       | 88,88%   | 89,44%    | 88,88% | 89,06%   | 980,3 detik    |
| **GRU**        | 87,12%   | 87,81%    | 87,12% | 87,35%   | 414,7 detik    |

**Kesimpulan:**

- **LSTM** memiliki akurasi tertinggi (88,88%) dan F1-Score terbaik (89,06%), tapi paling lambat (980 detik)
- **GRU** hampir sebagus LSTM (87,12%) tapi lebih cepat (415 detik) — pilihan terbaik untuk rasio performa/kecepatan
- **Simple RNN** jauh tertinggal (72,84%) karena tidak bisa mengingat konteks jangka panjang, walau paling cepat

## Analisis Etika & Keterbatasan

Notebook ini juga menganalisis potensi bias dan keterbatasan model:

### Bias per Kandidat

Distribusi sentimen tidak merata antar kandidat:

- Anies: 65% Positive, 35% Negative
- Ganjar: 79% Positive, 21% Negative
- Prabowo: 74% Positive, 26% Negative

Ini berarti model mungkin belajar bias politik tertentu dari data.

### Keterbatasan

- **Sarkasme/ironi** sulit dideteksi oleh model RNN/LSTM standar
- **Slang & typo** tidak ada di kamus (jadi `<OOV>`)
- **Teks sangat pendek** (1-2 kata) kurang konteks untuk klasifikasi
- **Akun bot/spam** bisa mencemari data dengan opini tidak asli

### Implikasi Etis

- Model tidak boleh digunakan untuk keputusan individual tanpa validasi manual
- Penggunaan untuk profiling individu tanpa persetujuan bermasalah secara etika
- Kesalahan klasifikasi bisa merugikan reputasi seseorang

**Rekomendasi:** Gunakan model hanya untuk analisis agregat (tren besar), bukan untuk keputusan per individu.

## Cara Menjalankan

### Opsi 1 — Google Colab (paling mudah)

1. Buka [Google Colab](https://colab.research.google.com) dan upload `notebook.ipynb`.
2. Setup Kaggle API key (diperlukan untuk mengunduh dataset):
   - Buat akun di [kaggle.com](https://www.kaggle.com) (gratis)
   - Buka **Settings → API → Create New Token** → unduh `kaggle.json`
   - Upload `kaggle.json` ke Colab dengan menjalankan:
     ```python
     from google.colab import files
     files.upload()  # pilih kaggle.json
     !mkdir -p ~/.kaggle && cp kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json
     ```
3. Set runtime ke **GPU**: **Runtime → Change runtime type → T4 GPU**
4. Klik **Runtime → Run all** (`Ctrl + F9`)
5. Training ketiga model selesai dalam ~25 menit (dengan GPU T4)

### Opsi 2 — Jalankan di komputer sendiri

1. Install **Python 3.10+**.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Setup Kaggle API key:
   - Letakkan `kaggle.json` di `~/.kaggle/` (Linux/Mac) atau `C:\Users\<nama>\.kaggle\` (Windows)
4. Buka notebook:
   ```
   jupyter notebook notebook.ipynb
   ```
5. Jalankan setiap cell dari atas ke bawah.

## Struktur Cell dalam Notebook

| Cell                          | Apa yang dilakukan                                              |
| ----------------------------- | --------------------------------------------------------------- |
| **1** (Imports)               | Memuat library dan modul yang dibutuhkan                        |
| **2** (Load Dataset)          | Mengunduh dataset dari Kaggle via `kagglehub`                   |
| **3** (Load CSV)              | Membaca 3 file CSV, menggabungkan, membersihkan baris kosong    |
| **4** (Preprocessing)         | Membersihkan teks (lowercase, hapus URL/mention/tanda baca)     |
| **5** (Tokenisasi)            | Mengubah teks jadi angka, padding, label encoding, class weight |
| **6** (Split)                 | Membagi data 80% training / 20% testing                         |
| **7** (Build Model)           | Membuat fungsi `build_model()` untuk RNN/LSTM/GRU               |
| **8** (Training)              | Melatih ketiga model dengan EarlyStopping                       |
| **9** (Tabel Perbandingan)    | Menampilkan tabel metrik kinerja                                |
| **10** (Visualisasi)          | Grafik akurasi & loss per epoch                                 |
| **11** (Confusion Matrix)     | Visualisasi matriks kebingungan untuk setiap model              |
| **12** (Bias per Kandidat)    | Analisis distribusi sentimen per kandidat                       |
| **13** (Edge Cases)           | Identifikasi contoh prediksi yang salah                         |
| **14** (Error per Kelas)      | Classification report & error rate per kelas                    |
| **15** (Etika & Keterbatasan) | Analisis etika, bias, dan keterbatasan model                    |
| **16** (Ringkasan)            | Ringkasan distribusi kelas dan metrik                           |

## Dependencies

| Library        | Untuk apa                                                 |
| -------------- | --------------------------------------------------------- |
| `tensorflow`   | Framework neural network (RNN, LSTM, GRU, Embedding)      |
| `pandas`       | Manipulasi data (membaca CSV, menggabungkan dataframe)    |
| `numpy`        | Operasi numerik (array, argmax)                           |
| `matplotlib`   | Membuat grafik (akurasi/loss per epoch)                   |
| `seaborn`      | Membuat heatmap (confusion matrix)                        |
| `scikit-learn` | Split data, label encoding, metrik evaluasi, class weight |
| `kagglehub`    | Mengunduh dataset dari Kaggle                             |

## File dalam Proyek Ini

```
analisis-sentimen-pilpres-2024/
├── README.md          ← Anda di sini
├── notebook.ipynb     ← Notebook utama (buka ini!)
└── requirements.txt   ← Dependencies Python (untuk lokal)
```
