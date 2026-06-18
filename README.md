# Projek Praktikum UAS Analisis Algoritma
## Last-Mile Delivery Routing: Komparasi Algoritma Heuristik (Greedy) dan Eksak (DFS)

### Anggota Kelompok:
1. **140810240005 - Aulia Fadhila Mumtaza**  — *Algoritma Heuristik*
2. **140810240011 - Katrina Grace Kwok**  — *Algoritma Heuristik*
3. **140810240081 - Aliya Zahra Nurazizah**  — *Algoritma Eksak*
4. **140810240089 - Hosea Dave Andersen** — *Algoritma Eksak*

---

## 1. Cara Menjalankan Program

Program ini dikembangkan menggunakan **Python+**.

### Perintah Eksekusi CLI
Jalankan program dari direktori utama dengan memilih salah satu skenario ekonomi berikut:
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

Kami membandingkan 2 pendekatan algoritmik yang bertolak belakang untuk menganalisis trade-off antara efisiensi BBM dan biaya komputasi:

### A. Algoritma Heuristik Dasar: Greedy 
*   **Modul:** [src/programGreedy.py](/src/programGreedy.py)
* **Trade-off:** Dengan algoritma ini, kurir akan selalu memilih destinasi terdekat berikutnya dari lokasinya saat ini sehingga kecepatan eksekusi cepat, namun kemungkinan menghasilkan hasil yang tidak optimal.

### B. Algoritma Eksak: DFS Pruning
*   **Modul:** [src/programEksak.py](/src/programEksak.py)
*   **Trade-off:** Algoritma ini mengecek setiap kemungkinan kombinasi jalur sehingga dijamin pasti menemukan rute dengan konsumsi bensin paling murah secara absolut, tetapi kekurangannya yaitu waktu eksekusi yang sangat lambat. Meskipun sudah dibantu teknik pruning untuk memotong pengecekan pada cabang rute yang terbukti boros, eksekusinya tetap memakan biaya server yang paling mahal.

## 4. Analisis Kompleksitas (Big-O)

### A. Algoritma Greedy
1.  **Kompleksitas Waktu: O(N^2)**
    Memiliki satu *loop* utama untuk mengunjungi N-1 pelanggan. Di setiap iterasi, algoritma memeriksa N kandidat untuk mencari jarak terdekat. 
2.  **Kompleksitas Ruang: O(N)**
    Hanya mengalokasikan memori untuk variabel penanda `visited` dan *array* penyimpan `rute`.

### B. Algoritma DFS Pruning
1.  **Kompleksitas Waktu: O(N!) (Worst Case)**
    Meskipun *pruning* memotong banyak cabang pencarian secara signifikan, batas atas komputasi teoritisnya tetap faktorial karena mengevaluasi permutasi rute dari titik ke titik.
2.  **Kompleksitas Ruang: O(N)**
    Memori dialokasikan untuk memelihara tumpukan rekursi (*Call Stack*) sedalam N pelanggan.

---

## 5. Ringkasan Hasil Uji

Hasil pengujian eksekusi terminal CLI untuk kedua skenario tersimpan secara detail di folder docs:
..................

### Tabel Komparasi Utama ($N = 13$):

Tabel di bawah ini merupakan komparasi metrik finansial dan algoritmik (*N = 11*):

| Metrik | GREEDY (Heuristik) | DFS PRUNING (Eksak) |
| :--- | :---: | :---: | :---: |
| **Jarak Total (km)** | 46 km | 46 km |
| **Bensin Habis (Liter)** | 0.9982 L | 0.9982 L |
| **Waktu Running (ms)** | 0.0253 ms | 6.1015 ms |
| **Biaya Server (Rp 50/ms)**| Rp 1.27 | Rp 305.08 |
| **TCO Subsidi (BBM Rp5.000)**| Rp 4,992.17 | Rp 5,295.98 |
| **TCO Krisis (BBM Rp20.000)**| Rp 19,964.90 | Rp 20,268.71 |

*Catatan: Rumus rasio bensin dieksekusi secara dinamis di setiap pergerakan rute mengikuti formula:*
*Rasio = Rasio Kosong + ( (Rasio Penuh - Rasio Kosong) * (Beban Saat Ini / Beban Total) )*

---

## 6. Kesimpulan Keputusan Bisnis

Berdasarkan kalkulasi *Total Cost of Ownership* (TCO), rekomendasi arsitektur algoritma bagi manajemen logistik adalah sebagai berikut:

1.  **Skenario BBM Bersubsidi (Rp 5.000 / Liter):**
    Manajemen direkomendasikan untuk menggunakan **Greedy**. Pada tingkat harga BBM yang normal, algoritma Heuristik terbukti mampu menemukan rute optimal yang sama persis dengan hasil algoritma Eksak (keduanya menghabiskan 0.9982 Liter bensin). Karena kualitas rutenya seimbang, Greedy menang telak dari segi efisiensi komputasi karena mengeksekusi pencarian hanya dalam waktu 0.0253 ms, menekan tagihan *Cloud Server* hingga ke angka Rp 1.27.
2.  **Skenario Krisis BBM (Rp 20.000 / Liter):**
    Saat harga BBM melambung tinggi, perusahaan tetap direkomendasikan menggunakan **Greedy**. Secara logis, investasi pada algoritma Eksak yang mahal hanya masuk akal jika algoritma tersebut bisa memberikan sisa penghematan bensin yang lebih banyak. Pada kasus ini, algoritma DFS Pruning tidak memberikan tambahan pemotongan jarak atau bensin sama sekali. Memaksakan penggunaan DFS hanya akan membuang-buang anggaran server perusahaan sebesar Rp 305.08 per rute tanpa memberikan timbal balik penghematan (*Return on Investment*) di lapangan.
3.  **Analisis Titik Impas (Break-Even Point/BEP):**
    Untuk kasus dengan 11 titik lokasi ini, titik impas tidak akan pernah tercapai pada harga BBM berapapun. Syarat mutlak terjadinya *BEP* untuk perpindahan dari algoritma Heuristik ke Eksak adalah adanya selisih liter BBM yang dihemat. Tetapi di kasus ini, DFS dan Greedy menghasilkan rute dan konsumsi bensin yang sama persis. Karena tidak ada ekstra bensin yang berhasil dihemat oleh DFS, membayar tagihan server DFS yang jauh lebih mahal (selisih sekitar Rp 303) akan menjadi boros.

    Namun, jika kedepannya pesanan pelanggan bertambah sangat banyak dan peta jalan semakin rumit, algoritma Greedy berisiko mulai kewalahan dan keliru memilih rute karena sifatnya yang hanya melihat jarak terdekat sesaat. Saat skala datanya sudah membesar, algoritma DFS mungkin bisa lebih berpotensi, karena ia selalu teliti mengecek setiap kemungkinan jalur untuk menjamin bensin yang paling irit.
    
    *Titik Impas BBM = (Biaya Server DFS - Biaya Server Greedy) / (BBM Greedy (L) - BBM DFS (L))*
    *Titik Impas BBM = Rp [HASIL_HITUNGAN_MANUAL_ANDA] / Liter*
