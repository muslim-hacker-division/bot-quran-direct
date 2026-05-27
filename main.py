import math
import os
import requests
import datetime
import random
from playwright.sync_api import sync_playwright

# =========================================================
# CONFIG
# =========================================================
QURAN_API_RANDOM = (
    "https://api.alquran.cloud/v1/ayah/random/"
    "editions/quran-uthmani,id.indonesian"
)

OUTPUT_PREFIX = "slide"
WIDTH = 1280
HEIGHT = 1280
MAX_CHARS_PER_SLIDE = 380
WATERMARK = "Poster Pengingat"

# Telegram Config (Diambil dari GitHub Secrets)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# =========================================================
# API GET DATA (Dinamis: Hari Biasa vs Hari Jumat WIB)
# =========================================================
def get_ayah_data():
    # Deteksi hari berdasarkan waktu UTC GitHub + offset WIB (UTC+7)
    waktu_utc = datetime.datetime.now(datetime.timezone.utc)
    waktu_wib = waktu_utc + datetime.timedelta(hours=7)
    hari_ini = waktu_wib.weekday()  # 4 artinya hari Jumat

    if hari_ini == 4:
        print("🌙 [Mode Al-Kahfi Aktif] Hari Jumat WIB, mengambil ayat dari Surah Al-Kahfi...")
        # Mengambil ayat 1-10 Al-Kahfi secara acak untuk variasi pengingat
        ayat_pilihan = random.randint(1, 10)
        url = f"https://api.alquran.cloud/v1/ayah/18:{ayat_pilihan}/editions/quran-uthmani,id.indonesian"
    else:
        print("📖 [Mode Reguler] Hari biasa, mengambil ayat acak...")
        url = QURAN_API_RANDOM

    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()["data"]

    arabic = data[0]["text"]
    translation = data[1]["text"]
    surah_name = data[1]["surah"]["englishName"]
    ayah_number = data[1]["numberInSurah"]

    return arabic, translation, surah_name, ayah_number

# =========================================================
# SPLIT TEXT FOR SLIDES
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
# MODERN FUTURISTIC HTML TEMPLATE
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
    width: {WIDTH}px;
    height: {HEIGHT}px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #02080d;
    /* Efek Grid Labirin Teknologi + Gradasi Neon Cyberpunk */
    background-image: 
        linear-gradient(rgba(0, 242, 254, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 242, 254, 0.03) 1px, transparent 1px),
        radial-gradient(circle at 80% 20%, rgba(0, 242, 254, 0.15), transparent 45%),
        radial-gradient(circle at 15% 85%, rgba(79, 172, 254, 0.12), transparent 40%),
        linear-gradient(135deg, #020b14 0%, #051625 50%, #01060b 100%);
    background-size: 40px 40px, 40px 40px, 100% 100%, 100% 100%, 100% 100%;
    color: #e2f1f8;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
}}

/* Glassmorphic Cyber Container */
.container {{
    position: relative;
    width: {WIDTH - 120}px;
    height: {HEIGHT - 120}px;
    background: linear-gradient(135deg, rgba(5, 22, 37, 0.6) 0%, rgba(2, 10, 18, 0.8) 100%);
    border: 1px solid rgba(0, 242, 254, 0.25);
    border-radius: 20px;
    padding: 80px 70px;
    display: flex;
    flex-direction: column;
    align-items: center;
    box-shadow: 
        0 20px 50px rgba(0, 0, 0, 0.5),
        inset 0 0 30px rgba(0, 242, 254, 0.05);
}}

/* Tech HUD Corner Borders */
.container::before, .container::after {{
    content: '';
    position: absolute;
    width: 30px;
    height: 30px;
    border: 3px solid #00f2fe;
}}
.container::before {{ top: -1px; left: -1px; border-right: none; border-bottom: none; border-top-left-radius: 20px; }}
.container::after {{ bottom: -1px; right: -1px; border-left: none; border-top: none; border-bottom-right-radius: 20px; }}

/* Teks Arab dengan Glow Lembut */
.arabic {{
    font-family: 'Amiri', serif;
    font-size: 56px;
    line-height: 1.9;
    text-align: center;
    direction: rtl;
    max-width: 950px;
    margin-top: 10px;
    margin-bottom: 45px;
    color: #ffffff;
    text-shadow: 0 0 20px rgba(0, 242, 254, 0.2), 0 4px 10px rgba(0,0,0,0.7);
}}

/* Terjemahan Lebih Tebal dan Jelas */
.translation {{
    font-size: 34px;
    font-weight: 400;
    line-height: 1.75;
    text-align: center;
    max-width: 950px;
    margin: 0 auto;
    color: #b0c9d6;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}}

/* Referensi Surah bergaya HUD */
.reference {{
    margin-top: 40px;
    font-family: 'Orbitron', sans-serif;
    font-size: 24px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #00f2fe;
    text-shadow: 0 0 10px rgba(0, 242, 254, 0.5);
}}

.spacer {{ flex: 1; }}

/* Footer Info */
.footer-hud {{
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px dashed rgba(0, 242, 254, 0.15);
    padding-top: 25px;
}}
.watermark {{
    font-family: 'Orbitron', sans-serif;
    font-size: 18px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #4facfe;
}}
.page {{
    font-family: 'Orbitron', sans-serif;
    font-size: 18px;
    color: #00f2fe;
}}
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
# GENERATE ALL IMAGES (Optimized Browser Reuse)
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
# CAPTION CHANNEL TELEGRAM (DINAMIS & LENGKAP)
# =========================================================
def build_caption(arabic, translation, surah_name, ayah_number):
    # Cek hari lagi untuk menyesuaikan tema caption (Reguler vs Al-Kahfi)
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

    # Jika postingan terdiri dari beberapa slide (Multiple Images)
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
            "media": requests.utils.json.dumps(media)
        }
        
        response = requests.post(url, data=payload, files=files_payload, timeout=60)
        
        for f in files_payload.values():
            f.close()

    # Jika hanya 1 slide saja
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
        print("✅ Postingan gambar berhasil mendarat langsung di Telegram.")
    else:
        print(f"❌ Gagal kirim ke Telegram: {response.status_code} - {response.text}")

# =========================================================
# MAIN
# =========================================================
def main():
    print("🔄 Mengambil data ayat dinamis...")
    arabic, translation, surah_name, ayah_number = get_ayah_data()

    print(f"🎨 Membuat gambar slide untuk QS. {surah_name}: {ayah_number}...")
    files = generate_images(arabic, translation, surah_name, ayah_number)

    print("📝 Menyusun caption lengkap...")
    caption = build_caption(arabic, translation, surah_name, ayah_number)

    print("🚀 Mengirimkan langsung ke Telegram...")
    upload_to_telegram(files, caption)

if __name__ == "__main__":
    main()
