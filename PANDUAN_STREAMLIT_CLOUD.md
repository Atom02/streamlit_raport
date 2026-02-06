# Panduan Deployment ke Streamlit Cloud (Gratis)

Ini adalah panduan langkah demi langkah untuk men-online-kan aplikasi Rapor Siswa Anda menggunakan layanan gratis **Streamlit Community Cloud**.

⚠️ **PENTING: Masalah Data Hilang**
Streamlit Cloud sifatnya "Ephemeral" (sementara). Artinya, setiap kali aplikasi restart (atau 'tidur' karena tidak dibuka), file lokal seperti database `report_card.db` akan **ter-reset** kembali ke kondisi awal yang ada di GitHub.

---

## Langkah 1: Siapkan GitHub dengan SSH Key

GitHub tidak lagi mendukung password biasa. Anda harus menggunakan **SSH Key** agar bisa meng-upload kode.

### 1. Cek / Buat SSH Key

Buka terminal di komputer Anda (laptop candra):

1.  **Cek apakah sudah punya key:**

    ```bash
    ls ~/.ssh/id_ed25519.pub
    ```

    Jika muncul file, lanjut ke langkah 2. Jika "No such file", buat baru:

    ```bash
    ssh-keygen -t ed25519 -C "email_anda@example.com"
    ```

    Tekan **Enter** terus sampai selesai (tidak perlu isi passphrase jika untuk belajar).

2.  **Ambil Public Key:**
    Tampilkan key yang akan dicopy ke GitHub:
    ```bash
    cat ~/.ssh/id_ed25519.pub
    ```
    Copy seluruh teks yang muncul (dimulai dengan `ssh-ed25519 ....`).

### 2. Masukkan ke GitHub

1.  Login ke [github.com](https://github.com).
2.  Kelik Foto Profil (pojok kanan atas) -> **Settings**.
3.  Pilih menu **SSH and GPG keys** (di menu kiri).
4.  Klik tombol **New SSH key**.
5.  **Title**: Isi "Laptop Candra" (bebas).
6.  **Key**: Paste kode yang tadi Anda copy.
7.  Klik **Add SSH key**.

### 3. Upload Kode

Sekarang Anda bisa upload kode tanpa password.

1.  **Buat Repository Baru di GitHub**:
    - Beri nama `aplikasi-rapor`.
    - Biarkan Public/Private.
    - **Jangan** centang "Add README".

2.  **Push dari Terminal**:
    Kembali ke folder proyek Anda:

    ```bash
    cd /home/candra/Projects/Personal/buatdede

    # Inisialisasi Git
    git init
    git add .
    git commit -m "Upload pertama"
    git branch -M main

    # PENTING: Gunakan format SSH (git@github.com:...) BUKAN https
    # Ganti USERNAME_GITHUB dengan username asli Anda
    git remote add origin git@github.com:USERNAME_GITHUB/aplikasi-rapor.git

    # Jika tadi sudah terlanjur add origin https, hapus dulu:
    # git remote remove origin
    # Lalu add ulang yang format git@...

    # Push
    git push -u origin main
    ```

    _Jika ditanya `Are you sure you want to continue connecting?`, ketik `yes` lalu Enter._

---

## Langkah 2: Deploy di Streamlit Cloud

1.  Buka [share.streamlit.io](https://share.streamlit.io) dan login dengan akun GitHub Anda.
2.  Klik tombol **New app**.
3.  Isi formulir:
    - **Repository**: Pilih repository yang baru Anda buat (`aplikasi-rapor`).
    - **Branch**: `main`.
    - **Main file path**: `app.py`.
4.  Klik **Deploy!**.

---

## Langkah 3: Konfigurasi Setelah Deploy

1.  Tunggu proses "Baking..." selesai.
2.  **Login ke Admin**: Password default: `dedePetot!`.
3.  **Setting URL Dasar**:
    - Di dashboard Admin, ganti "URL Dasar Aplikasi" dengan URL baru Anda (contoh: `https://aplikasi-rapor-anda.streamlit.app`).

---

## Tips Perawatan

- **Update Kode**: Cukup edit file di laptop, lalu:
  ```bash
  git add .
  git commit -m "Update baru"
  git push
  ```
  Streamlit akan otomatis update.
