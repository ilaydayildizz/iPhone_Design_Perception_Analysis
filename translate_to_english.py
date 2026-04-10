import pandas as pd
import time
from deep_translator import GoogleTranslator

# Excel dosyasını oku
df = pd.read_excel("youtube_all_comments_with_language2.xlsx")

translator = GoogleTranslator(source="auto", target="en")

total = len(df)
start_time = time.time()

def translate_if_needed(text, language):
    try:
        if pd.isna(text) or len(text.strip()) < 2:
            return ""

        # Zaten İngilizceyse çevirme
        if language == "en":
            return text

        # Dil tespit edilemediyse (emoji vs.)
        if language == "unknown":
            return ""

        # İngilizce olmayanları çevir
        return translator.translate(text)

    except Exception:
        return ""

translated_texts = []

for i, row in enumerate(df.itertuples(index=False), start=1):
    translated_texts.append(
        translate_if_needed(row.text, row.language)
    )

    # ---- İLERLEME ÇIKTISI ----
    elapsed = time.time() - start_time
    avg_per_item = elapsed / i
    remaining = avg_per_item * (total - i)
    percent = (i / total) * 100

    print(
        f"\r🔄 {i}/{total} (%{percent:.2f}) | "
        f"Geçen: {elapsed/60:.1f} dk | "
        f"Kalan: {remaining/60:.1f} dk",
        end=""
    )

    # Google ban riskine karşı yavaşlat (sadece çevrilecekler sayılır)
    if row.language != "en" and i % 20 == 0:
        time.sleep(1)

print()  # satır atlat

df["text_english"] = translated_texts

# Yeni dosyaya kaydet
df.to_excel("youtube_comments_translated_en2.xlsx", index=False)

print("✅ İngilizce dışındaki tüm yorumlar İngilizceye çevrildi.")
