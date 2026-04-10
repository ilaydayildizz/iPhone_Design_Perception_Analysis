import pandas as pd
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# sonuçlar her çalıştırmada aynı olsun
DetectorFactory.seed = 0

# Excel dosyanı oku
df = pd.read_excel("youtube_all_comments2.xlsx")

def detect_language(text):
    try:
        if pd.isna(text) or len(text.strip()) < 3:
            return "unknown"
        return detect(text)
    except LangDetectException:
        return "unknown"

# Yeni sütun ekle
df["language"] = df["text"].apply(detect_language)

# Yeni Excel dosyasına kaydet
df.to_excel("youtube_all_comments_with_language2.xlsx", index=False)

print("✅ Dil tespiti bitti. Yeni Excel oluşturuldu.")

