# 📖 Bot Auto-Posting Quran Direct

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Playwright-Headless-green?style=for-the-badge&logo=playwright&logoColor=white" alt="Playwright">
  <img src="https://img.shields.io/badge/Telegram-API%20Direct-blue?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  <img src="https://img.shields.io/badge/Platform-GitHub%20Actions-black?style=for-the-badge&logo=githubactions&logoColor=white" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

---

## 🛠️ Tentang Proyek
Bot otomatisasi generasi baru untuk menyiarkan ayat-ayat Al-Qur'an dan terjemahannya langsung ke Channel Telegram tanpa pihak ketiga (**No Make.com / Zapier**). 

Proyek ini menggunakan **Playwright Headless Browser** untuk merender template HTML interaktif berseragam **Modern Futuristic Cyberpunk Glow** menjadi gambar beresolusi tinggi ($1280 \times 1280\text{ px}$), lalu mengirimkannya sebagai album multimedia ke Telegram lengkap dengan teks Arab dan terjemahan di bagian *caption*.

### ✨ Fitur Unggulan
* **Direct Integration:** Memotong jalur *webhook* pihak ketiga, langsung menembak API Telegram menggunakan library `requests`. Lebih cepat, stabil, dan 100% gratis tanpa kuota limit.
* **Mode Jumat Dinamis (Al-Kahfi):** Script otomatis mendeteksi Waktu Indonesia Barat (WIB). Setiap hari Jumat, bot akan mengunci otomatis ke **Surah Al-Kahfi (Ayat 1-10)** dengan tag khusus `#alkahfi`, dan kembali ke mode ayat acak pada hari biasa.
* **Smart Slide Multi-Page:** Jika terjemahan terlalu panjang, teks otomatis dipotong per slide secara rapi dan dikirim sebagai **Media Group (Album)** di Telegram.
* **UI Cyberpunk Modern:** Desain background menggunakan efek grid labirin teknologi dengan pendaran neon cyan dan border bertema HUD fiksi ilmiah.

---

## 🚀 Struktur Repositori
* `.github/workflows/main.yml` — Konfigurasi jadwal otomatisasi (*Cron Job*) via GitHub Actions.
* `main.py` — Logika inti bot (Fetch API Quran, Render Playwright, & Direct Sender Telegram).
* `requirements.txt` — Daftar dependensi ringan (`requests` & `playwright`).

---

## 📅 Jadwal Otomatisasi (Cron Job WIB)
Bot ini dikonfigurasi untuk berjalan secara otomatis dua kali sehari mengikuti zona waktu Asia/Jakarta:
1. **Pagi Hari:** Jam `09:17 WIB` (`17 2 * * *` UTC)
2. **Sore Hari:** Jam `16:43 WIB` (`43 9 * * *` UTC)

---

## 📜 Lisensi
Proyek ini dilindungi di bawah lisensi **MIT**. Anda bebas menyalin, memodifikasi, dan mendistribusikan ulang proyek ini dengan tetap menyertakan atribusi hak cipta asli.

---
<p align="center">
  Developed with ⚡ by <b>Muslim Hacker Division</b><br>
  <i>"Code for Deen, Automate for Iman"</i>
</p>
