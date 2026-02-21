import os
import time
import threading
import requests
import random
from flask import Flask

# --- FLASK SUNUCUSU (Render'ın kapanmaması için) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot aktif ve calisiyor!"

def run_flask():
    # Render varsayılan olarak 10000 portunu kullanır
    port = int(os.environ.get("PORT", 10000))
    app.run(host=\'0.0.0.0\', port=port)

# --- DISCORD BOT MANTIĞI ---
TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_IDS = os.environ.get("CHANNEL_IDS", "").split(",")
MESSAGE_TEXT = os.environ.get("MESSAGE_TEXT", "Otomatik Mesaj")
IMAGE_URL = os.environ.get("IMAGE_URL") # Fotoğraf için internet linki kullanacağız

def send_discord_message():
    while True:
        if not TOKEN or not CHANNEL_IDS[0]:
            print("Hata: Token veya Kanal ID bulunamadi!")
            time.sleep(60)
            continue

        for channel_id in CHANNEL_IDS:
            url = f"https://discord.com/api/v9/channels/{channel_id.strip()}/messages"
            headers = {"Authorization": TOKEN}
            
            data = {"content": MESSAGE_TEXT}
            
            # Fotoğraf gönderimi (Link olarak veya dosya olarak)
            # Render'da dosya yönetimi zor olduğu için IMAGE_URL kullanmak en sağlıklısıdır
            if IMAGE_URL:
                data["content"] = f"{MESSAGE_TEXT}\n{IMAGE_URL}"

            try:
                response = requests.post(url, headers=headers, json=data)
                if response.status_code == 200:
                    print(f"Mesaj gonderildi: {channel_id}")
                else:
                    print(f"Hata ({response.status_code}): {response.text}")
            except Exception as e:
                print(f"Baglanti hatasi: {e}")

        # 15-20 dakika arası bekleme
        wait_time = random.randint(15 * 60, 20 * 60)
        print(f"Bekleme suresi: {wait_time // 60} dakika.")
        time.sleep(wait_time)

# --- BAŞLATMA ---
if __name__ == "__main__":
    # Botu arka planda çalıştır
    bot_thread = threading.Thread(target=send_discord_message)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Flask sunucusunu ana işlemde çalıştır
    run_flask()
