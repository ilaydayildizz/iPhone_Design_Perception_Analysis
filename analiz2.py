import pandas as pd
import requests
from collections import Counter
import re

LM_URL = "http://localhost:1234/v1/chat/completions"
MODEL = "lmstudio"

df = pd.read_excel("only_design.xlsx")
df['clean_text'] = df['temiz_yorum'].fillna("").astype(str)

# ==============================
# 1) Kelime Listeleri (Geliştirilmiş)
# ==============================
positive_words = [
    "good","great","love","amazing","nice","beautiful","premium","sleek","like",
    "perfect","cool","clean","modern","high quality","stylish","color","finish",
    "camera","frame","thin","premium look","solid","well built","matte","glossy"
]

negative_words = [
    "bad","ugly","hate","cheap","terrible","worst","disappoint","outdated","boring",
    "overpriced","awful","problem","issue","regret","trash","poor quality","toy-like",
    "looks cheap","not good","not impressed","weird camera","heavy","bulky"
]

# ==============================
# 2) Kelime Puanlama (Hızlı Karar)
# ==============================
def rule_label(text):
    t = text.lower()
    pos = sum(w in t for w in positive_words)
    neg = sum(w in t for w in negative_words)
    
    if pos > neg + 1: return "positive"
    if neg > pos + 1: return "negative"
    return "check"  # kararsız → LLM'e gönder


# ==============================
# 3) LLM ile Karar Destek
# ==============================
def lm_decide(text):
    prompt = f"""
Classify the comment strictly as: positive, negative or neutral.
Return ONE WORD ONLY.

COMMENT: "{text}"
"""
    try:
        r = requests.post(LM_URL, json={
            "model": MODEL,
            "messages":[{"role":"user","content":prompt}],
            "temperature":0.0,
            "max_tokens":5
        })
        return r.json()['choices'][0]['message']['content'].strip().lower()
    except:
        return "neutral"


# ==============================
# 4) Hibrit Etiketleme
# ==============================
labels = []
total = len(df)

for i, text in enumerate(df['clean_text'], start=1):
    first = rule_label(text)
    if first == "check":
        label = lm_decide(text)
    else:
        label = first
        
    labels.append(label)
    print(f"🔄 Etiketleniyor: {i}/{total} (%{(i/total)*100:.1f})", end="\r")

df["sentiment_label"] = labels
print("\n\n✨ Hibrit etiketleme tamamlandı!")
df.to_excel("only_design_hybrid.xlsx", index=False)
print("📁 Kaydedildi: only_design_hybrid.xlsx\n")


# ==============================
# 5) Sayısal Özet
# ==============================
pos = (df.sentiment_label=="positive").sum()
neg = (df.sentiment_label=="negative").sum()
neu = (df.sentiment_label=="neutral").sum()

print("========== 📌 SONUÇLAR ==========")
print("Toplam yorum:", total)
print("👍 Positive :", pos)
print("👎 Negative :", neg)
print("😐 Neutral  :", neu)
print("=================================\n")


# ==============================
# 6) EN ÇOK ÖVÜLEN / ELEŞTİRİLEN NOKTALAR
# ==============================
def get_topics(texts, keywords):
    words = []
    for t in texts:
        t = t.lower()
        for w in keywords:
            if w in t:
                words.append(w)
    return Counter(words).most_common(10)

pos_texts = df[df.sentiment_label=="positive"]["clean_text"]
neg_texts = df[df.sentiment_label=="negative"]["clean_text"]
neu_texts = df[df.sentiment_label=="neutral"]["clean_text"]

print("✨ Olumlu yorumlarda en çok övülenler:")
print(get_topics(pos_texts, positive_words), "\n")

print("💢 Olumsuz yorumlarda en çok eleştirilenler:")
print(get_topics(neg_texts, negative_words), "\n")

print("😶 Nötr yorumlarda kararsız kalınan noktalar:")
print(get_topics(neu_texts, positive_words + negative_words), "\n")
