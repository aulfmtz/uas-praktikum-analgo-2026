# Projek Praktikum UAS Analisis Algoritma
## Last-Mile Delivery Routing: Komparasi Algoritma Heuristik (Greedy, ACO) dan Eksak (DFS)

### Anggota Kelompok:
1. **140810240005 - Aulia Fadhila Mumtaza**  — *Pembagian Tugas*
2. **140810240011 - Katrina Grace Kwok**  —
3. **140810240081 - Aliya Zahra Nurazizah**  —
4. **140810240089 - Hosea Dave Andersen** — 

---

## 1. Cara Menjalankan Program

Program ini dikembangkan menggunakan **Python+**.

### Perintah Eksekusi CLI
Jalankan program dari direktori utama dengan memilih salah satu skenario ekonomi berikut:

1.  **Menjalankan Skenario Subsidi BBM (Harga BBM Rp 5.000 / Liter):**
    ```bash
    python src/program.py 
    ```

---

## 2. Deskripsi Data & Model Input

Bagian ini memodelkan data geografis dan berat logistik pengiriman barang secara dinamis dari file CSV.

### Skenario Geografis:
Dataset memodelkan rute pengantaran kurir di daerah perkotaan Bandung yang terdiri atas **1 Gudang Pusat (Hub)** dan **10 Pelanggan** (Total 11 Titik).
*   **Hub (Indeks 0):** Gudang Pusat (Awal & Akhir rute).
*   **Customer (Indeks 1 - 12)** 

### Struktur File CSV 
* `data/berat_paket.csv`:
* `data/matriks_jarak.csv`:
* `data/skenario_ekonomi.csv`:

---

## 3. Pemilihan Algoritma 

Kami membandingkan tiga pendekatan algoritmik (2 heuristik dan 1 eksak) yang bertolak belakang untuk menganalisis trade-off antara efisiensi BBM dan biaya komputasi:

### A. Algoritma Heuristik Dasar: Greedy 
*   **Modul:** [src/programGreedy.py](/src/programGreedy.py)
* **Trade-off:** Dengan algoritma ini, kurir akan selalu memilih destinasi terdekat berikutnya dari lokasinya saat ini sehingga kecepatan eksekusi cepat, namun kemungkinan menghasilkan hasil yang tidak optimal.

### B. Algoritma Metaheuristik: Ant Colony Optimization (ACO)
*   **Modul:** [src/programACO.py](/src/programACO.py)
*   **Trade-off:** Algoritma ini lebih pintar dari Greedy karena ikut mempertimbangkan jejak rute yang sukses di masa lalu (seperti semut) untuk mencari konsumsi bensin paling hemat. Hasil akhirnya jauh lebih optimal, tapi waktu komputasinya menjadi sedikit lebih lambat karena program harus mensimulasikan pergerakan puluhan semut virtual secara berulang.

### C. Algoritma Eksak: DFS Pruning
*   **Modul:** [src/programEksak.py](/src/programEksak.py)
*   **Trade-off:** Algoritma ini mengecek setiap kemungkinan kombinasi jalur sehingga dijamin pasti menemukan rute dengan konsumsi bensin paling murah secara absolut, tetapi kekurangannya yaitu waktu eksekusi yang sangat lambat. Meskipun sudah dibantu teknik pruning untuk memotong pengecekan pada cabang rute yang terbukti boros, eksekusinya tetap memakan biaya server yang paling mahal.

## 4. Analisis Kompleksitas (Big-O)

### A. Algoritma Greedy
1.  **Kompleksitas Waktu: O(N^2)**
    Memiliki satu *loop* utama untuk mengunjungi $N - 1$ pelanggan. Di setiap iterasi, algoritma memeriksa $N$ kandidat untuk mencari jarak terdekat. 
2.  **Kompleksitas Ruang: O(N)**
    Hanya mengalokasikan memori untuk variabel penanda `visited` dan *array* penyimpan `rute`.

### B. Algoritma Ant Colony Optimization (ACO)
1.  **Kompleksitas Waktu: O(I * A * N^2)**
    Beban komputasi sangat dipengaruhi oleh jumlah Iterasi ($I$), jumlah Semut ($A$), dan proses pemilihan tujuan (`probs`) yang mengevaluasi $N$ lokasi.
2.  **Kompleksitas Ruang: O(N^2)**
    Membutuhkan alokasi memori matriks 2 dimensi berukuran $N \times N$ untuk menyimpan dan memperbarui matriks feromon di setiap iterasinya.

### C. Algoritma DFS Pruning
1.  **Kompleksitas Waktu: O(N!) (Worst Case)**
    Meskipun *pruning* memotong banyak cabang pencarian secara signifikan (memperbaiki *Average Case*), batas atas komputasi teoritisnya tetap faktorial karena mengevaluasi permutasi rute dari titik ke titik.
2.  **Kompleksitas Ruang: O(N)**
    Memori dialokasikan untuk memelihara tumpukan rekursi (*Call Stack*) sedalam jumlah pelanggan $N$.

---

## 5. Ringkasan Hasil Uji

Hasil pengujian eksekusi terminal CLI untuk kedua skenario tersimpan secara detail di folder docs:
..................

### Tabel Komparasi Utama ($N = 13$):

Tabel di bawah ini merupakan komparasi metrik finansial dan algoritmik (*N = 11*):

| Metrik | GREEDY (Heuristik) | ACO (Metaheuristik) | DFS PRUNING (Eksak) |
| :--- | :---: | :---: | :---: |
| **Jarak Total (km)** | 46 km | 46 km | 46 km |
| **Bensin Habis (Liter)** | 0.9982 L | 0.9982 L | 0.9982 L |
| **Waktu Running (ms)** | 0.0314 ms | 18.9548 ms | 6.4638 ms |
| **Biaya Server (Rp 50/ms)**| Rp 1.57 | Rp 947.74| Rp 323.19 |
| **TCO Subsidi (BBM Rp5.000)**| Rp 4,993.48 | Rp 5,938.65 | Rp 5,314.10 |
| **TCO Krisis (BBM Rp20.000)**| Rp 19,965.21 | Rp 20,911.38 | Rp 20,286.83 |

*Catatan: Rumus rasio bensin dieksekusi secara dinamis di setiap pergerakan rute mengikuti formula:*
*Rasio = Rasio Kosong + ( (Rasio Penuh - Rasio Kosong) * (Beban Saat Ini / Beban Total) )*

---

## 6. Kesimpulan Keputusan Bisnis

Berdasarkan kalkulasi *Total Cost of Ownership* (TCO), rekomendasi arsitektur algoritma bagi manajemen logistik adalah sebagai berikut:

1.  **Skenario BBM Bersubsidi (Rp 5.000 / Liter):**
    Manajemen direkomendasikan untuk menggunakan **ACO**. Pada harga BBM yang murah, penghematan bensin yang ditawarkan oleh algoritma Eksak tidak mampu menutupi melonjaknya tagihan sewa *Cloud Server* akibat tingginya waktu komputasi eksekusi rute.
2.  **Skenario Krisis BBM (Rp 20.000 / Liter):**
    Saat harga BBM melambung tinggi, perusahaan direkomendasikan beralih ke **ACO**. Jika selisih tagihan komputasi server *DFS Pruning* atau *ACO* jauh lebih rendah dibandingkan potensi penghematan harga BBM harian, maka investasi pada waktu komputasi menjadi sangat masuk akal secara finansial.
3.  **Analisis Titik Impas (Break-Even Point):**
    Transisi *upgrade* arsitektur server ke algoritma DFS Pruning hanya akan menguntungkan apabila harga BBM menembus perhitungan berikut:
    
    *Titik Impas BBM = (Biaya Server DFS - Biaya Server Greedy) / (BBM Greedy (L) - BBM DFS (L))*
    *Titik Impas BBM = Rp [HASIL_HITUNGAN_MANUAL_ANDA] / Liter*