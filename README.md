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
*   **Pelanggan (Indeks 1 - 12):** Daerah......

### Struktur File CSV 
* `data/berat_paket.csv`:
* `data/matriks_jarak.csv`:
* `data/skenario_ekonomi.csv`:

---

## 3. Pemilihan Algoritma 

Kami membandingkan dua pendekatan algoritmik yang bertolak belakang untuk menganalisis trade-off antara efisiensi BBM dan biaya komputasi:

### A. Algoritma Heuristik Dasar: Greedy (Nearest Neighbor)
*   **Modul:** [src/programGreedy.py](/src/programGreedy.py)
* **Alasan:** Pendekatan paling intuitif. Kurir selalu memilih destinasi terdekat berikutnya dari lokasinya saat ini.
* **Trade-off:** Kecepatan eksekusi sangat instan, namun mengorbankan kualitas rute. Sangat rentan terjebak pada kondisi sub-optimal karena menyisakan rute panjang di akhir perjalanan.

### B. Algoritma Metaheuristik: Ant Colony Optimization (ACO)
*   **Modul:** [src/programACO.py](/src/programACO.py)
*   **Alasan:** Mensimulasikan perilaku koloni semut menggunakan jejak feromon dan probabilitas (*Roulette Wheel Selection*) untuk mengeksplorasi ruang pencarian rute secara cerdas.
*   **Trade-off:** Mampu menghasilkan rute yang jauh lebih optimal dari Greedy, namun memerlukan waktu komputasi yang lebih lama karena mensimulasikan banyak semut dalam puluhan iterasi.

### C. Algoritma Eksak: DFS
*   **Modul:** [src/programEksak.py](/src/programEksak.py)
*   **Alasan:** Algoritma fundamental yang menjamin ditemukannya rute terpendek secara mutlak (*Global Optimum*).
*   **Trade-off:** Kompleksitas waktu yang sangat berat. Implementasi pemangkasan (*Pruning*) wajib diterapkan untuk menghentikan penelusuran cabang graf yang       biayanya sudah terbukti melebihi *best distance* sementara.

---

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
| **Jarak Total (km)** | [ISI_ANGKA] km | [ISI_ANGKA] km | [ISI_ANGKA] km |
| **Bensin Habis (Liter)** | [ISI_ANGKA] L | [ISI_ANGKA] L | [ISI_ANGKA] L |
| **Waktu Running (ms)** | [ISI_ANGKA] ms | [ISI_ANGKA] ms | [ISI_ANGKA] ms |
| **Biaya Server (Rp 50/ms)**| Rp [ISI_ANGKA] | Rp [ISI_ANGKA] | Rp [ISI_ANGKA] |
| **TCO Subsidi (BBM Rp5.000)**| Rp [ISI_ANGKA] | Rp [ISI_ANGKA] | Rp [ISI_ANGKA] |
| **TCO Krisis (BBM Rp20.000)**| Rp [ISI_ANGKA] | Rp [ISI_ANGKA] | Rp [ISI_ANGKA] |

*Catatan: Rumus rasio bensin dieksekusi secara dinamis di setiap pergerakan rute mengikuti formula:*
*Rasio = Rasio Kosong + ( (Rasio Penuh - Rasio Kosong) * (Beban Saat Ini / Beban Total) )*

---

## 6. Kesimpulan Keputusan Bisnis

Berdasarkan kalkulasi *Total Cost of Ownership* (TCO), rekomendasi arsitektur algoritma bagi manajemen logistik adalah sebagai berikut:

1.  **Skenario BBM Bersubsidi (Rp 5.000 / Liter):**
    Manajemen direkomendasikan untuk menggunakan **[PILIH_NAMA_ALGORITMA_DENGAN_TCO_TERENDAH]**. Pada harga BBM yang murah, penghematan bensin yang ditawarkan oleh algoritma Eksak tidak mampu menutupi melonjaknya tagihan sewa *Cloud Server* akibat tingginya waktu komputasi eksekusi rute.
2.  **Skenario Krisis BBM (Rp 20.000 / Liter):**
    Saat harga BBM melambung tinggi, perusahaan direkomendasikan beralih ke **[PILIH_NAMA_ALGORITMA_DENGAN_TCO_TERENDAH]**. Jika selisih tagihan komputasi server *DFS Pruning* atau *ACO* jauh lebih rendah dibandingkan potensi penghematan harga BBM harian, maka investasi pada waktu komputasi menjadi sangat masuk akal secara finansial.
3.  **Analisis Titik Impas (Break-Even Point):**
    Transisi *upgrade* arsitektur server ke algoritma DFS Pruning hanya akan menguntungkan apabila harga BBM menembus perhitungan berikut:
    
    *Titik Impas BBM = (Biaya Server DFS - Biaya Server Greedy) / (BBM Greedy (L) - BBM DFS (L))*
    *Titik Impas BBM = Rp [HASIL_HITUNGAN_MANUAL_ANDA] / Liter*