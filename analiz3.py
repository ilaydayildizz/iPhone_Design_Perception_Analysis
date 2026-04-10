import pandas as pd
from collections import Counter
import re

# ==========================
# 1) DOSYAYI YÜKLE
# ==========================
df = pd.read_excel("only_design_hybrid.xlsx")

# Yorum metni olan kolon
TEXT_COL = "clean_text" if "clean_text" in df.columns else "temiz_yorum"

# Etiket kolonu
LABEL_COL = "sentiment_label"   # <-- senin dosyandaki isim


# ==========================
# 2) KELİMELERE AYIRMA
# ==========================
def kelimelere_ayir(text):
    if pd.isna(text): 
        return []
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9ğüşöçıöİĞÜŞÖÇ ]+", " ", text)  # noktalama-temizlik
    return [t for t in text.split() if len(t) > 2]          # tek harfleri at


# Basit gereksiz kelimeler
stopwords = {
    "ve","de","da","bu","şu","ama","çok","bir","en","gibi",
    "the","and","for","with","that","this","you","your","its","just",
    "ben","sen","o","i","it","is","was","are","to","of","in"
}

def en_cok_kelime(df_parca, adet=20):
    tum = []
    for txt in df_parca[TEXT_COL]:
        kelimeler = kelimelere_ayir(txt)
        kelimeler = [k for k in kelimeler if k not in stopwords]
        tum.extend(kelimeler)
    return Counter(tum).most_common(adet)


# ==========================
# 3) ANALİZ
# ==========================
for duygu in ["positive", "negative", "neutral"]:
    alt_df = df[df[LABEL_COL] == duygu]

    print("\n" + "#"*60)
    print(f"### {duygu.upper()} YORUMLARDA EN ÇOK GEÇEN KELİMELER")
    print("#"*60)
    print(f"Toplam yorum: {len(alt_df)}\n")

    for kelime, sayi in en_cok_kelime(alt_df):
        print(f"{kelime:<20} --> {sayi} kez geçmiş")
