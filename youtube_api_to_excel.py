import requests
import pandas as pd
import time
import json
from pathlib import Path

# ---------------- Ayarlar ----------------
API_KEY = "AIzaSyDYRQB8jEn-BCtQsdIDK29StFrwzmlINv0"
VIDEO_ID = "Cr9B6yyLZSk"

OUTPUT_CSV = "youtube_all_comments2.csv"
OUTPUT_XLSX = "youtube_all_comments2.xlsx"
STATE_FILE = "yt_all_comments_state.json"

MAX_RESULTS = 100
SLEEP_TIME = 0.5     # request arası bekleme
MAX_RETRIES = 5      # hata olursa tekrar deneme
TIMEOUT = 15         # request timeout

# ---------------- Yardımcı Fonksiyonlar ----------------
def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def load_state():
    if not Path(STATE_FILE).exists():
        return {}
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def append_to_csv(rows, csv_path):
    # Sadece istediğimiz sütunları kaydediyoruz
    df = pd.DataFrame(rows, columns=["author", "text", "publishedAt"])
    if not Path(csv_path).exists():
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    else:
        df.to_csv(csv_path, mode="a", header=False, index=False, encoding="utf-8-sig")

def save_to_excel(csv_path, xlsx_path):
    df = pd.read_csv(csv_path)
    df.to_excel(xlsx_path, index=False, engine="openpyxl")
    print(f"Excel kaydedildi: {xlsx_path}")

# ---------------- API Fonksiyonları ----------------
session = requests.Session()

def fetch_json(url, params):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = session.get(url, params=params, timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            wait = 2 ** attempt
            print(f"Request hatası ({attempt}/{MAX_RETRIES}): {e}. {wait}s bekleniyor...")
            time.sleep(wait)
    print("Maximum retry sayısına ulaşıldı. Devam ediliyor...")
    return {}

def fetch_comment_threads(video_id, page_token=None):
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "key": API_KEY,
        "maxResults": MAX_RESULTS,
        "pageToken": page_token,
        "textFormat": "plainText"
    }
    return fetch_json(url, params)

def fetch_replies(parent_id, page_token=None):
    url = "https://www.googleapis.com/youtube/v3/comments"
    params = {
        "part": "snippet",
        "parentId": parent_id,
        "key": API_KEY,
        "maxResults": MAX_RESULTS,
        "pageToken": page_token,
        "textFormat": "plainText"
    }
    return fetch_json(url, params)

# ---------------- Ana Fonksiyon ----------------
def collect_all_comments(video_id):
    state = load_state()
    next_page_token = state.get("nextPageToken")
    total_fetched = state.get("total_fetched", 0)

    print("Başlıyor. Önceki kaydı yükledik:", bool(state))

    while True:
        data = fetch_comment_threads(video_id, next_page_token)
        items = data.get("items", [])
        if not items:
            print("Bu sayfada yorum yok.")
            break

        rows = []
        for item in items:
            top = item["snippet"]["topLevelComment"]["snippet"]
            row = {
                "author": top.get("authorDisplayName"),
                "text": top.get("textDisplay"),
                "publishedAt": top.get("publishedAt"),
            }
            rows.append(row)
            total_fetched += 1

            # Yanıtları çek
            parent_id = item["snippet"]["topLevelComment"]["id"]
            reply_token = None
            while True:
                reply_data = fetch_replies(parent_id, reply_token)
                reply_items = reply_data.get("items", [])
                if not reply_items:
                    break

                for r in reply_items:
                    rs = r["snippet"]
                    rrow = {
                        "author": rs.get("authorDisplayName"),
                        "text": rs.get("textDisplay"),
                        "publishedAt": rs.get("publishedAt"),
                    }
                    rows.append(rrow)
                    total_fetched += 1

                reply_token = reply_data.get("nextPageToken")
                if not reply_token:
                    break
                time.sleep(SLEEP_TIME)

        # CSV’ye ekle
        append_to_csv(rows, OUTPUT_CSV)
        print(f"{len(rows)} yorum kaydedildi. Toplam çekilen: {total_fetched}")

        # State kaydet
        next_page_token = data.get("nextPageToken")
        save_state({"nextPageToken": next_page_token, "total_fetched": total_fetched})

        if not next_page_token:
            print("Tüm sayfalar işlendi. İşlem tamam.")
            break

        time.sleep(SLEEP_TIME)

    save_to_excel(OUTPUT_CSV, OUTPUT_XLSX)
    print("Tüm yorumlar çekildi ve kaydedildi!")

# ---------------- Çalıştır ----------------
if __name__ == "__main__":
    collect_all_comments(VIDEO_ID)
