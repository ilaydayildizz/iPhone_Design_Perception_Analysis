import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import emoji

# Gerekli dil paketlerini indir
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def on_isleme(metin):
    if pd.isna(metin):
        return ""
    
    metin = str(metin)

    # 1️⃣ Emojileri kaldır
    metin = emoji.replace_emoji(metin, replace=" ")

    # 2️⃣ URL, mention, hashtag temizleme
    metin = re.sub(r"http\S+|www\.\S+", " ", metin)
    metin = re.sub(r"[@#]\w+", " ", metin)

    # 3️⃣ küçük harfe çevir
    metin = metin.lower()

    # 4️⃣ noktalama, sembol, sayı temizleme
    metin = re.sub(r'[^\w\s]', ' ', metin)
    metin = re.sub(r'\d+', ' ', metin)

    # 5️⃣ ASCII dışı her şeyi sil (emoji artıkları dahil)
    metin = metin.encode("utf-8", "ignore").decode("ascii", "ignore")

    # 6️⃣ stopword temizleme
    kelimeler = metin.split()
    temiz_kelimeler = [w for w in kelimeler if w not in stop_words]
    metin = " ".join(temiz_kelimeler)

    # 7️⃣ Boşlukları düzenle
    metin = re.sub(r'\s+', ' ', metin).strip()

    return metin


# ===================================================
#                ANA İŞLEM BÖLÜMÜ
# ===================================================
print("📥 Excel yükleniyor...")
df = pd.read_excel('youtube_comments_translated_en2.xlsx')

print("🧹 Metinler temizleniyor...")
df['temiz_yorum'] = df['text_english'].apply(on_isleme)

# 8️⃣ Tek kelimeli yorumları sil
print("🚮 Tek kelimeli yorumlar temizleniyor...")
df = df[df['temiz_yorum'].str.split().str.len() > 1]  # ✨ burası eklendi

# Sonuçları kaydet
print("💾 Kaydediliyor...")
df.to_excel('temizlenmis_yorumlar2.xlsx', index=False)

print("🎉 İşlem tamamlandı! 'temizlenmis_yorumlar2.xlsx' dosyası hazır.")
