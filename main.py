import math
import os
import requests
import datetime
import random
import json 
from playwright.sync_api import sync_playwright

# =========================================================
# CONFIG
# =========================================================
OUTPUT_PREFIX = "slide"
WIDTH = 1280
HEIGHT = 1280
MAX_CHARS_PER_SLIDE = 380
WATERMARK = "Poster Pengingat"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# =========================================================
# API GET DATA (Dinamis: Hari Biasa vs Hari Jumat WIB)
# =========================================================
def get_ayah_data():
    waktu_utc = datetime.datetime.now(datetime.timezone.utc)
    waktu_wib = waktu_utc + datetime.timedelta(hours=7)
    hari_ini = waktu_wib.weekday() 

    if hari_ini == 4:
        print("🌙 [Mode Al-Kahfi Aktif] Hari Jumat WIB...")
        ayat_pilihan = random.randint(1, 110)
        url = f"https://api.alquran.cloud/v1/ayah/18/{ayat_pilihan}/editions/quran-uthmani,id.indonesian"
    else:
        surah_acak = random.randint(1, 114)
        url = "https://api.alquran.cloud/v1/ayah/random/editions/quran-uthmani,id.indonesian"
        print(f"📖 [Mode Reguler] Mengambil ayat acak dari API...")

    response = requests.get(url, timeout=30)
    response.raise_for_status()
    
    data = response.json()["data"]

    arabic = data[0]["text"]
    translation = data[1]["text"]
    surah_name = data[1]["surah"]["englishName"]
    ayah_number = data[1]["numberInSurah"]

    print(f"✅ Berhasil mendapatkan: QS. {surah_name} Ayat {ayah_number}")
    return arabic, translation, surah_name, ayah_number

# =========================================================
# HITUNG MUNDUR RAMADHAN
# =========================================================
def calculate_ramadan_countdown():
    # Sesuaikan estimasi tanggal 1 Ramadhan (Contoh: 8 Februari 2027)
    ramadan_date = datetime.date(2027, 2, 8)
    waktu_utc = datetime.datetime.now(datetime.timezone.utc)
    waktu_wib = waktu_utc + datetime.timedelta(hours=7)
    today = waktu_wib.date()
    
    delta = ramadan_date - today
    days_left = delta.days
    return max(0, days_left)

# =========================================================
# Pecah Teksnya untuk Slide
# =========================================================
def split_translation(text, max_chars=MAX_CHARS_PER_SLIDE):
    words = text.split()
    pages = []
    current = ""

    for word in words:
        test = current + (" " if current else "") + word
        if len(test) <= max_chars:
            current = test
        else:
            if current:
                pages.append(current)
            current = word

    if current:
        pages.append(current)

    return pages

# =========================================================
# Template HTML Modern & Futuristik (Ayat Quran)
# =========================================================
def build_html(arabic, translation, reference, page_num, total_pages):
    arabic_block = ""
    if page_num == 1:
        arabic_block = f'<div class="arabic">{arabic}</div>'

    page_indicator = ""
    if total_pages > 1:
        page_indicator = f'<div class="page">{page_num} // {total_pages}</div>'

    html = f'''
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Amiri:wght@700&family=Orbitron:wght@500;700&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
    width: {WIDTH}px; height: {HEIGHT}px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #02080d;
    background-image: 
        linear-gradient(rgba(0, 242, 254, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 242, 254, 0.03) 1px, transparent 1px),
        radial-gradient(circle at 80% 20%, rgba(0, 242, 254, 0.15), transparent 45%),
        radial-gradient(circle at 15% 85%, rgba(79, 172, 254, 0.12), transparent 40%),
        linear-gradient(135deg, #020b14 0%, #051625 50%, #01060b 100%);
    background-size: 40px 40px, 40px 40px, 100% 100%, 100% 100%, 100% 100%;
    color: #e2f1f8; overflow: hidden; display: flex; justify-content: center; align-items: center;
}}
.container {{
    position: relative; width: {WIDTH - 120}px; height: {HEIGHT - 120}px;
    background: linear-gradient(135deg, rgba(5, 22, 37, 0.6) 0%, rgba(2, 10, 18, 0.8) 100%);
    border: 1px solid rgba(0, 242, 254, 0.25); border-radius: 20px; padding: 80px 70px;
    display: flex; flex-direction: column; align-items: center;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), inset 0 0 30px rgba(0, 242, 254, 0.05);
}}
.container::before, .container::after {{
    content: ''; position: absolute; width: 30px; height: 30px; border: 3px solid #00f2fe;
}}
.container::before {{ top: -1px; left: -1px; border-right: none; border-bottom: none; border-top-left-radius: 20px; }}
.container::after {{ bottom: -1px; right: -1px; border-left: none; border-top: none; border-bottom-right-radius: 20px; }}
.arabic {{
    font-family: 'Amiri', serif; font-size: 56px; line-height: 1.9; text-align: center; direction: rtl;
    max-width: 950px; margin-top: 10px; margin-bottom: 45px; color: #ffffff;
    text-shadow: 0 0 20px rgba(0, 242, 254, 0.2), 0 4px 10px rgba(0,0,0,0.7);
}}
.translation {{
    font-size: 34px; font-weight: 400; line-height: 1.75; text-align: center; max-width: 950px; margin: 0 auto; color: #b0c9d6;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}}
.reference {{
    margin-top: 40px; font-family: 'Orbitron', sans-serif; font-size: 24px; font-weight: 700; letter-spacing: 2px; color: #00f2fe;
    text-shadow: 0 0 10px rgba(0, 242, 254, 0.5);
}}
.spacer {{ flex: 1; }}
.footer-hud {{
    width: 100%; display: flex; justify-content: space-between; align-items: center;
    border-top: 1px dashed rgba(0, 242, 254, 0.15); padding-top: 25px;
}}
.watermark {{ font-family: 'Orbitron', sans-serif; font-size: 18px; letter-spacing: 3px; text-transform: uppercase; color: #4facfe; }}
.page {{ font-family: 'Orbitron', sans-serif; font-size: 18px; color: #00f2fe; }}
</style>
</head>
<body>
<div class="container">
    {arabic_block}
    <div class="translation">“{translation}”</div>
    <div class="reference">// QS. {reference}</div>
    <div class="spacer"></div>
    <div class="footer-hud">
        <div class="watermark">SYS: {WATERMARK}</div>
        {page_indicator}
    </div>
</div>
</body>
</html>
'''
    return html

# =========================================================
# Template HTML Khusus Countdown Ramadhan (DIUPDATE DENGAN HADIS)
# =========================================================
def build_countdown_html(days_left):
    return f'''
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
    width: {WIDTH}px; height: {HEIGHT}px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #02080d;
    background-image: 
        linear-gradient(rgba(0, 242, 254, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 242, 254, 0.03) 1px, transparent 1px),
        radial-gradient(circle at 50% 50%, rgba(0, 242, 254, 0.12), transparent 70%);
    background-size: 40px 40px, 40px 40px, 100% 100%;
    color: #e2f1f8; display: flex; justify-content: center; align-items: center; overflow: hidden;
}}
.container {{
    position: relative; width: {WIDTH - 120}px; height: {HEIGHT - 120}px;
    background: linear-gradient(135deg, rgba(5, 22, 37, 0.8) 0%, rgba(2, 10, 18, 0.9) 100%);
    border: 1px solid rgba(0, 242, 254, 0.4); border-radius: 20px; padding: 50px 60px;
    display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;
    box-shadow: 0 0 40px rgba(0, 242, 254, 0.2), inset 0 0 30px rgba(0, 242, 254, 0.05);
}}
.container::before, .container::after {{
    content: ''; position: absolute; width: 30px; height: 30px; border: 3px solid #00f2fe;
}}
.container::before {{ top: -1px; left: -1px; border-right: none; border-bottom: none; border-top-left-radius: 20px; }}
.container::after {{ bottom: -1px; right: -1px; border-left: none; border-top: none; border-bottom-right-radius: 20px; }}
.title {{ font-family: 'Orbitron', sans-serif; font-size: 22px; color: #4facfe; letter-spacing: 4px; margin-bottom: 15px; }}
.days-number {{ font-family: 'Orbitron', sans-serif; font-size: 110px; font-weight: 900; color: #ffffff; text-shadow: 0 0 30px rgba(0, 242, 254, 0.6); line-height: 1; margin-bottom: 10px; }}
.label {{ font-family: 'Orbitron', sans-serif; font-size: 20px; color: #00f2fe; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 25px; }}
.quote {{ font-size: 21px; color: #b0c9d6; font-style: italic; max-width: 900px; line-height: 1.5; margin-bottom: 12px; }}
.quote-ref {{ font-family: 'Orbitron', sans-serif; font-size: 16px; color: #00f2fe; letter-spacing: 2px; }}
.footer {{ position: absolute; bottom: 30px; font-family: 'Orbitron', sans-serif; font-size: 15px; color: #4facfe; letter-spacing: 2px; }}
</style>
</head>
<body>
<div class="container">
    <div class="title">// SYSTEM COUNTDOWN //</div>
    <div class="days-number">{days_left}</div>
    <div class="label">Hari Menuju Bulan Ramadhan</div>
    <div class="quote">“Telah datang kepadamu bulan Ramadan, bulan yang diberkahi. Allah mewajibkan kepadamu puasa di dalamnya; pada bulan ini pintu-pintu surga dibuka, pintu-pintu neraka ditutup dan para setan diikat...”</div>
    <div class="quote-ref">// (HR. Ahmad & An-Nasa'i)</div>
    <div class="footer">SYS: RUNTIME IMAN // RAMADHAN PREP</div>
</div>
</body>
</html>
'''
    return html

# =========================================================
# HASILKAN SEMUA GAMBAR (Ayat Reguler)
# =========================================================
def generate_images(arabic, translation, surah_name, ayah_number):
    pages = split_translation(translation)
    reference = f"{surah_name.upper()}: {ayah_number}"
    files = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT})

        for i, page_text in enumerate(pages, start=1):
            html = build_html(
                arabic=arabic,
                translation=page_text,
                reference=reference,
                page_num=i,
                total_pages=len(pages),
            )
            filename = f"{OUTPUT_PREFIX}_{i}.png"
            page.set_content(html, wait_until="networkidle")
            page.screenshot(path=filename)
            files.append(filename)
            
        browser.close()
    return files

# =========================================================
# POST CHANNEL TELEGRAM (Caption Ayat Reguler)
# =========================================================
def build_caption(arabic, translation, surah_name, ayah_number):
    waktu_utc = datetime.datetime.now(datetime.timezone.utc)
    waktu_wib = waktu_utc + datetime.timedelta(hours=7)
    hari_ini = waktu_wib.weekday()

    if hari_ini == 4:
        header = "✨ *[RUNTIME IMAN - JUMAT AL-KAHFI]*"
        hashtags = "#alkahfi #jumatberkah #alquran #selfreminder #runtimeiman #MHDWarrior"
    else:
        header = "📖 *[RUNTIME IMAN DAILY QURAN]*"
        hashtags = "#alquran #selfreminder #runtimeiman #MHDWarrior"

    return f"""{header}

{arabic}

“_{translation}_”

📌 *QS. {surah_name}: {ayah_number}*

_Semoga ayat ini menjadi pengingat dan penyejuk hati kita hari ini._

{hashtags}"""

# =========================================================
# UPLOAD TO TELEGRAM
# =========================================================
def upload_to_telegram(files, caption):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Error: Secrets TELEGRAM_BOT_TOKEN atau TELEGRAM_CHAT_ID belum diisi di GitHub!")
        return

    if len(files) > 1:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMediaGroup"
        media = []
        files_payload = {}
        
        for i, file_path in enumerate(files):
            file_key = f"photo_{i}"
            files_payload[file_key] = open(file_path, "rb")
            
            media_item = {
                "type": "photo",
                "media": f"attach://{file_key}"
            }
            if i == 0:
                media_item["caption"] = caption
                media_item["parse_mode"] = "Markdown"
            media.append(media_item)

        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "media": json.dumps(media)
        }
        response = requests.post(url, data=payload, files=files_payload, timeout=60)
        for f in files_payload.values():
            f.close()
    else:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        with open(files[0], "rb") as photo_file:
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "caption": caption,
                "parse_mode": "Markdown"
            }
            files_payload = {"photo": photo_file}
            response = requests.post(url, data=payload, files=files_payload, timeout=60)

    if response.status_code == 200:
        print("✅ OKE! Postingan gambar berhasil mendarat langsung di Telegram.")
    else:
        print(f"❌ Gagal kirim ke Telegram: {response.status_code} - {response.text}")

# =========================================================
# MAIN (DENGAN SAKLAR MODE)
# =========================================================
def main():
    post_mode = os.getenv("POST_MODE", "ayah")

    if post_mode == "countdown":
        print("🌙 Menjalankan Mode Hitung Mundur Ramadhan...")
        days_left = calculate_ramadan_countdown()

        # Render gambar khusus countdown dengan hadis baru
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT})
            html = build_countdown_html(days_left)
            filename = "countdown_slide.png"
            page.set_content(html, wait_until="networkidle")
            page.screenshot(path=filename)
            browser.close()

        files = [filename]
        caption = f"⏳ *[RAMADHAN COUNTDOWN]*\n\nHitung mundur menuju bulan suci: *{days_left} Hari Lagi*.\n\n_“Telah datang kepadamu bulan Ramadan, bulan yang diberkahi. Allah mewajibkan kepadamu puasa di dalamnya; pada bulan ini pintu-pintu surga dibuka, pintu-pintu neraka ditutup dan para setan diikat...”_\n\n📌 *(HR. Ahmad dan An-Nasa'i)*\n\n#Ramadhan #CountdownRamadhan #RuntimeIman #MHDWarrior"

        print("🚀 Mengirimkan poster countdown ke Telegram...")
        upload_to_telegram(files, caption)

        if os.path.exists(filename):
            os.remove(filename)

    else:
        print("🔄 Mengambil data ayat dinamis (Mode Reguler/Al-Kahfi)...")
        arabic, translation, surah_name, ayah_number = get_ayah_data()

        print(f"🎨 Membuat gambar slide untuk QS. {surah_name}: {ayah_number}...")
        files = generate_images(arabic, translation, surah_name, ayah_number)

        print("📝 Menyusun caption lengkap...")
        caption = build_caption(arabic, translation, surah_name, ayah_number)

        print("🚀 Mengirimkan ayat ke Telegram...")
        upload_to_telegram(files, caption)

if __name__ == "__main__":
    main()
