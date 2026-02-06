# Panduan Deployment Aplikasi Rapor Siswa

Dokumen ini menjelaskan cara men-deploy aplikasi Streamlit ini ke server produksi. Karena aplikasi ini menggunakan database SQLite (`report_card.db`), strategi penyimpanan data (persistence) sangat penting agar data tidak hilang saat server restart.

---

## Opsi 1: Deploy di VPS (Disarankan)

Opsi ini paling stabil untuk aplikasi dengan database lokal SQLite.

### Prasyarat

- Server VPS dengan OS Linux (Ubuntu 20.04/22.04 disarankan).
- Python 3.8+ terinstal.

### Langkah-langkah

1.  **Clone atau Upload Kode ke Server**
    Simpan kode di folder, misal `/var/www/rapor-siswa`.

2.  **Siapkan Environment**

    ```bash
    cd /var/www/rapor-siswa
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Buat Service Systemd**
    Agar aplikasi jalan terus di background dan auto-start saat boot.
    Buat file: `sudo nano /etc/systemd/system/rapor.service`

    Isi dengan:

    ```ini
    [Unit]
    Description=Aplikasi Rapor Siswa Streamlit
    After=network.target

    [Service]
    User=www-data
    WorkingDirectory=/var/www/rapor-siswa
    ExecStart=/var/www/rapor-siswa/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```

4.  **Jalankan Service**

    ```bash
    sudo chown -R www-data:www-data /var/www/rapor-siswa
    sudo systemctl daemon-reload
    sudo systemctl start rapor
    sudo systemctl enable rapor
    ```

5.  **Akses Aplikasi**
    Buka `http://IP-SERVER-ANDA:8501`.

---

## Opsi 2: Deploy Menggunakan Docker

Kami telah menyediakan `Dockerfile` untuk kemudahan deployment.

1.  **Build Image**

    ```bash
    docker build -t rapor-app .
    ```

2.  **Jalankan Container (PENTING: Mounting Volume)**
    Anda **wajib** nge-mount file database agar data tidak hilang saat container dihapus/restart.

    ```bash
    docker run -d \
      -p 8501:8501 \
      -v $(pwd)/report_card.db:/app/report_card.db \
      --name rapor-container \
      rapor-app
    ```

    _Catatan: Pastikan file `report_card.db` sudah ada (kosong tidak apa-apa) sebelum menjalankan command ini, atau mount satu folder penuh._

    Cara lebih aman (mount folder):

    ```bash
    docker run -d \
      -p 8501:8501 \
      -v $(pwd):/app \
      --name rapor-container \
      rapor-app
    ```

---

## Opsi 3: Streamlit Community Cloud (Gratis)

Opsi ini paling mudah tapi **BERISIKO HILANG DATA** karena Streamlit Cloud bersifat "ephemeral" (sementara). File SQLite akan ter-reset jika aplikasi reboot (biasanya terjadi jika tidak ada yang akses dalam beberapa hari).

**Solusi:**
Untuk Streamlit Cloud, disarankan mengganti SQLite dengan database cloud seperti **Supabase** atau **Google Sheets** jika butuh data permanen. Namun, jika Anda rajin mem-backup CSV manual (download data), opsi ini bisa dipakai untuk jangka pendek.

1.  Push kode ke GitHub.
2.  Login ke [share.streamlit.io](https://share.streamlit.io).
3.  Deploy app dari repositori GitHub Anda.
4.  Aplikasi langsung aktif.

---

## Konfigurasi Tambahan

### Mengatur URL Dasar (Domain)

Setelah deploy, Anda akan mendapatkan IP atau Domain (misal `rapor.sekolah.com`).

1.  Login ke halaman Admin aplikasi.
2.  Di kolom **"URL Dasar Aplikasi"**, ganti `http://localhost:8501` dengan domain asli Anda, misal `https://rapor.sekolah.com`.
3.  Link yang digenerate akan otomatis menyesuaikan.

### Keamanan

- **Password**: Ganti password default di file `app.py` baris `if password == "dedePetot!":` dengan password yang lebih kuat.
- **HTTPS**: Jika menggunakan VPS, sangat disarankan menggunakan Nginx sebagai Reverse Proxy dan pasang SSL (gratis pakai Certbot).
