# Panduan Deployment ke Streamlit Cloud (Gratis)

Ini adalah panduan langkah demi langkah untuk men-online-kan aplikasi Rapor Siswa Anda menggunakan layanan gratis **Streamlit Community Cloud**.

⚠️ **PENTING: Masalah Data Hilang**
Streamlit Cloud sifatnya "Ephemeral" (sementara). Artinya, setiap kali aplikasi restart (atau 'tidur' karena tidak dibuka), file lokal seperti database `report_card.db` akan **ter-reset** kembali ke kondisi awal yang ada di GitHub.
**Solusi:**

- Untuk penggunaan jangka pendek/demo: Tidak masalah, tapi Anda harus rajin **Upload Ulang CSV** setiap kali membuka aplikasi jika datanya hilang.
- Jika link siswa harus permanen: Anda perlu menggunakan database eksternal (seperti Google Sheets atau Supabase) di masa depan. Untuk sekarang, ikuti panduan ini untuk demo/testing.

---

## Langkah 1: Siapkan GitHub

Karena Streamlit Cloud mengambil kode dari GitHub, Anda harus meng-upload kode Anda ke sana.

1.  **Buat Akun GitHub**: Jika belum punya, daftar di [github.com](https://github.com).
2.  **Buat Repository Baru**:
    - Login ke GitHub.
    - Klik tombol `New` (warna hijau) atau tanda `+` di pojok kanan atas -> `New repository`.
    - Beri nama, misal `aplikasi-rapor`.
    - Pilih **Public** (agar mudah) atau **Private**.
    - Klik `Create repository`.

3.  **Upload Kode Anda**:
    Jika Anda sudah familiar dengan Git di terminal:

    ```bash
    git init
    git add .
    git commit -m "Upload pertama"
    git branch -M main
    git remote add origin https://github.com/USERNAME_ANDA/aplikasi-rapor.git
    git push -u origin main
    ```

    **Cara Manual (Upload Files):**
    - Di halaman repository GitHub yang baru dibuat, klik **uploading an existing file**.
    - Drag & Drop semua file dari folder proyek Anda (`app.py`, `data_processor.py`, `utils.py`, `requirements.txt`).
    - **PENTING**: Jangan lupa upload file `requirements.txt` agar Streamlit tahu library apa yang harus diinstal.
    - Klik `Commit changes`.

---

## Langkah 2: Deploy di Streamlit Cloud

1.  Buka [share.streamlit.io](https://share.streamlit.io) dan login dengan akun GitHub Anda.
2.  Klik tombol **New app**.
3.  Isi formulir:
    - **Repository**: Pilih repository yang baru Anda buat (`aplikasi-rapor`).
    - **Branch**: Biasanya `main` atau `master`.
    - **Main file path**: `app.py`.
4.  Klik **Deploy!**.

---

## Langkah 3: Konfigurasi Setelah Deploy

1.  Tunggu proses "Baking..." selesai. Ini akan menginstal library python.
2.  Setelah selesai, aplikasi akan terbuka di domain seperti `https://aplikasi-rapor-anda.streamlit.app`.
3.  **Login ke Admin**:
    - Gunakan password default: `dedePetot!` (sesuai kode terakhir Anda).
4.  **Setting URL Dasar**:
    - Di dashboard Admin, ganti "URL Dasar Aplikasi" dengan URL baru Anda (contoh: `https://aplikasi-rapor-anda.streamlit.app`).
    - Ini agar tombol copy link menghasilkan link yang benar.

---

## Tips Perawatan

- **Agar Aplikasi Tidak Tidur**: Streamlit Cloud akan "menidurkan" aplikasi jika tidak ada trafik selama beberapa hari. Anda cukup membukanya kembali dan menekan tombol "Wake Up" jika itu terjadi. ingat, database akan kosong kembali saat bangun.
- **Update Kode**: Jika Anda ingin mengubah kode, cukup edit/upload file baru ke GitHub. Streamlit Cloud akan otomatis mendeteksi perubahan dan me-restart aplikasi.
