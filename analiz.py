import pandas as pd
import requests

# ================================
# 1) DOSYALARI BİRLEŞTİR
# ================================
file1 = "llama3_hibrit_etiketli.xlsx"
file2 = "llama3_hibrit_etiketli2.xlsx"

df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)

df = pd.concat([df1, df2], ignore_index=True)
df['label'] = df['label'].str.lower().str.strip()

df.to_excel("merged_all.xlsx", index=False)
print("📌 Toplam yorum:", len(df))


# ================================
# 2) SADECE DESIGN YORUMLARI
# ================================
design_df = df[df['label'] == "design"].copy()
design_df.to_excel("only_design.xlsx", index=False)
print("🎨 Design yorum sayısı:", len(design_df))


# ================================
# 3) SENTIMENT ANALYSIS (text sütunu ile)
# ================================

LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"

def sentiment_predict(text):
    prompt = f"""
You analyze product design sentiment.
Classify opinions about the *design* of a product.

Return only:
positive
negative

================= 100 EXAMPLES =================
"Beautiful, sleek, premium design" → positive
"I hate this cheap looking frame" → negative
"Color and finish look elegant" → positive
"Ugly camera bump ruins everything" → negative
"Outdated design, looks like 2016" → negative
"Premium materials and modern look" → positive
"Cheap plastic body feels low-quality" → negative
"Matte finish looks amazing" → positive
"Terrible proportions and ugly bezels" → negative
"Clean design with a minimalist feel" → positive
"Awful design, looks like a toy" → negative
"Elegant curves and premium build" → positive
"Heavy, bulky and outdated" → negative
"Modern, futuristic vibe" → positive
"Terrible camera bump and weird angles" → negative
"Smooth edges and nice form factor" → positive
"Ugly layout, looks unfinished" → negative
"Stylish and visually impressive" → positive
"Low effort, cheap design" → negative
"Refined, thin bezels look great" → positive
"Chunky design ruins the experience" → negative
"Premium colors and aesthetic choices" → positive
"Plastic shiny body looks terrible" → negative
"Modern camera housing looks attractive" → positive
"Unbalanced layout, not visually pleasing" → negative
"Solid metal frame feels premium" → positive
"Design language looks inconsistent" → negative
"Iconic design, instantly recognizable" → positive
"Horrible texture and cheap vibe" → negative
"Minimalist and classy" → positive
"Looks old and boring" → negative
"Fresh, exciting redesign" → positive
"Why does it look like a kids toy?" → negative
"High-end look and luxury feel" → positive
"Disappointing design for the price" → negative
"Professional and mature aesthetic" → positive
"Bezels are too big and ugly" → negative
"Classy and polished exterior" → positive
"The worst camera bump I’ve seen" → negative
"Sleek and perfectly executed" → positive
"Very bad choices in shape" → negative
"Stunning materials and finish" → positive
"Unappealing and clumsy" → negative
"Looks like a flagship device" → positive
"Feels like a budget toy" → negative
"Design is inspiring" → positive
"I can’t stand how this looks" → negative
"Elegant and futuristic lines" → positive
"Outdated and messy structure" → negative
"Delightful matte texture" → positive
"Messy, off-balance camera island" → negative
"Visually impressive and clean" → positive
"Poorly executed design" → negative
"Thoughtful, detail-focused" → positive
"Unrefined and inconsistent" → negative
"Smart, well-proportioned layout" → positive
"Design looks rushed and lazy" → negative
"Stunning craftsmanship" → positive
"Zero creativity, boring" → negative
"Impressive and modern build" → positive
"Looks like last decade hardware" → negative
"Beautifully engineered" → positive
"Clunky and ugly" → negative
"Perfect color harmony" → positive
"Disgusting camera placement" → negative
"Looks truly premium" → positive
"Terrible aesthetic decisions" → negative
"Very elegant!" → positive
"Such an eyesore" → negative
"Super clean!" → positive
"It’s so ugly" → negative
"Smart finish and modern identity" → positive
"Feels awkward and badly shaped" → negative
"Perfect minimalist look" → positive
"Terrible material choice" → negative
"High-end aesthetic" → positive
"Trashy build" → negative
"Professional and refined" → positive
"Design is horrible" → negative
"Love the finish" → positive
"I hate how it looks" → negative
"Immaculate craftsmanship" → positive
"Very disappointing look" → negative
"Perfectly balanced and premium" → positive
"Design mistakes everywhere" → negative
"Looks so good!" → positive
"So ugly!" → negative
"Absolutely beautiful finish" → positive
"Poor taste design" → negative
"Stunning!" → positive
"Horrible!" → negative
=================================================

Now classify:
"{text}"

Answer only:
positive or negative
"""
    response = requests.post(
        LMSTUDIO_URL,
        json={
            "model":"Llama-3",
            "messages":[{"role":"user","content":prompt}],
            "temperature":0,
            "max_tokens":3
        }
    )
    try:
        return response.json()['choices'][0]['message']['content'].strip().lower()
    except:
        return "unknown"


# ================================
# 4) DESIGN YORUMLARINI ETİKETLE (text sütunu)
# ================================
sentiments = []
for i, text in enumerate(design_df['text'], start=1):
    sentiments.append(sentiment_predict(text))
    if i % 100 == 0:
        print(f"{i} yorum sınıflandırıldı...")

design_df['sentiment'] = sentiments
design_df.to_excel("design_sentiment.xlsx", index=False)
print("📁 Kaydedildi → design_sentiment.xlsx")


# ================================
# 5) ANALİZ – NE BEĞENİLMİŞ / NE ELEŞTİRİLMİŞ?
# ================================
positive_words = ["premium","sleek","beautiful","elegant","color","matte","thin","bezel","aesthetic","camera","finish"]
negative_words = ["ugly","cheap","outdated","boring","thick","heavy","plastic","worse","bad","camera bump"]

pos_df = design_df[design_df['sentiment']=="positive"]
neg_df = design_df[design_df['sentiment']=="negative"]

pos_result = {w: pos_df['text'].str.contains(w, case=False).sum() for w in positive_words}
neg_result = {w: neg_df['text'].str.contains(w, case=False).sum() for w in negative_words}

print("\n💖 EN ÇOK ÖVÜLENLER:")
for k,v in sorted(pos_result.items(), key=lambda x:x[1], reverse=True):
    print(f"{k:15} → {v}")

print("\n💔 EN ÇOK ELEŞTİRİLENLER:")
for k,v in sorted(neg_result.items(), key=lambda x:x[1], reverse=True):
    print(f"{k:15} → {v}")
