import pandas as pd

# ---------------- Müşteri Sadakati Sözlüğü (Tamamen Güncellenmiş) ----------------
LOYALTY_DICTIONARY = {

    "brand_transition": [
        "from iphone", "to iphone", "iphone to iphone", "going from iphone",
        "switched from iphone", "iphone upgrade", "iphone upgrading",
        "upgrading from iphone", "upgrade from iphone", "moving from iphone",
        "switching from iphone", "next iphone", "new iphone", "another iphone",
        "iphone again", "got iphone again", "my old phone was iphone",
        "didn't switch from iphone", "never left iphone", "stuck with iphone",
        "i don't plan to switch brands", "not switching brands", "brand loyalty",
        "the thought of changing brands doesn’t even cross my mind",
        "changing brands doesn't even cross my mind", "won't change brands",
        "always choose iphone", "loyal to apple", "stayed with apple",
        "keeping the same brand", "brand continuity", "next generation iphone",
        "followed iphone series",
        # Önceki ve Yeni Eklenen Sadakat Kelimeleri
        "not considering another brand",
        "suits me best",
        "can’t give up on apple",
        "my next phone would be an iphone",
        "don’t plan to switch brands", # Yeni eklendi: "iPhone is enough for me; I don’t plan to switch brands."
        "don’t plan to change", # Yeni eklendi: "iPhone is my favorite; I don’t plan to change."
        "don’t consider switching brands", # Yeni eklendi: "Apple products satisfy me; I don’t consider switching brands."
        "remain one",
        "won’t look at other brands",
        "will stay with it",
        "not really warm up to other brands",
        "won’t think otherwise",
        "remain loyal",
        "won’t switch to another brand",
        "will remain my preference",
    ],

    "repeat_purchase": [
        "another iphone", "buy iphone again", "new iphone again", "every new iphone",
        "keep buying iphone", "always buy iphone", "bought iphone again out of habit",
        "upgraded with iphone again", "repeat purchase", "purchase again",
        "next iphone model", "upgrade again", "keeping with series",
        "always upgrade", "continue upgrading",
        "third iphone in a row",
        "buy an iphone again",
        "always came back to iphone",
        "buy an iphone",
        "buy another iphone",
    ],

    "habitual_use": [
        "always iphone", "iphone is my default", "automatic choice", "natural choice",
        "hard to switch", "used to iphone", "keep using iphone", "continue using iphone",
        "been using iphone for years", "got used to using iphone now", "habit from iphone",
        "always used iphone", "default phone", "regularly use iphone",
        "routine use", "daily use", "cannot switch easily", "comfortable with iphone",
        "become a habit",
        "switching to another brand feels difficult",
        "choosing iphone each time comes naturally to me",
        "standard choice",
        "familiar to me",
        "gotten used to using an iphone",
        "part of my routine",
        "natural choice for me",
        # Yeni eklendi: "Choosing Apple is an easy decision for me."
        "easy decision for me" 
    ],

    "returning": [
        "came back to iphone", "returned to iphone", "went back to iphone", "always come back",
        "didn't give up iphone", "couldn't give up iphone", "back to iphone", "rejoined iphone",
        "come back again", "returning user", "repeat user", "back to apple",
        "ended up coming back to iphone",
    ],

    "long_term_use": [
        "using iphone for years", "long time iphone user", "been using iphone",
        "iphone user for years", "sticking with iphone", "always using iphone",
        "loyal to iphone", "remain with iphone", "using iphone since",
        "years of usage", "long term customer", "loyal customer",
        "brand continuity", "iPhone ecosystem",
        "apple ecosystem",
        "loyal to this brand",
        "loyal to this ecosystem",
        # Yeni eklendi: "I’m attached to the brand."
        "attached to the brand"
    ],

    "content_channel_loyalty": [
        "subscriber for years", "keep coming back", "always watch",
        "watch all your videos", "recommend this to all my friends",
        "can't wait for your next video", "always reliable",
        "best channel", "amazing content", "keep it up",
        "loyal viewer", "constant support", "followed for years",
        "repeat viewer", "faithful subscriber", "brand love",
        "expecting content", "trust this channel", "returning viewer",
        "always here", "never miss a video", "regular viewer"
    ],

    # ----------------------- İSTİSNA: Sadakat olmayan yorumlar -----------------------
    "non_loyalty": [
        "informative video", "production quality", "great lighting", "technical detail",
        "topic suggestion", "just wanted to say hi", "audio balance", "learned something new",
        "technical error", "feedback", "comment on topic", "single use content",
        "first time watching", "comment on quality", "one time watch", "random comment",
        "not related to brand", "neutral opinion", "video only"
    ],

    "general": [
        "again", "continue", "habit", "accustomed", "used", "satisfied", "trust",
        "preference", "stayed", "using", "upgraded", "ecosystem", "ios",
        "always", "same", "every", "repeat", "return", "keep", "default",
        "next", "followed", "long term", "years", "regularly", "loyal",
        "suits me",
        "happy with iphone",
        "fits me best",
        "confidence",
        "user experience",
        "performance",
        "reliable choice",
        "most suitable phone",
        "indispensable",
        # Yeni eklendi: "Apple products satisfy me"
        "satisfy me"
    ]
}


# ---------------- Fonksiyon: Sadakat Ataması ----------------
def loyalty_label(text):
    text_lower = str(text).lower()
    
    # Kategori bazlı kontrol yapılırken "non_loyalty" atlanır
    for category, keywords in LOYALTY_DICTIONARY.items():
        if category == "non_loyalty":
            continue
        
        for keyword in keywords:
            if keyword in text_lower:
                return 1  # Sadakat var
    
    # Sadakat kelimesi bulunamazsa, sadakat yok (0) döner.
    return 0  # Sadakat yok

# ---------------- Excel Dosyasını Oku ----------------
df = pd.read_excel("youtube_comments_translated_en.xlsx")

# ---------------- Müşteri Sadakati Sütununu Oluştur ----------------
# Yeni sözlükle etiketleme
df["Musteri_Sadakati"] = df["text_english"].apply(loyalty_label)

# ---------------- Sonuçları Kaydet ----------------
df.to_excel("youtube_comments_with_loyalty_final.xlsx", index=False)
print("✅ Müşteri sadakati sözlüğü başarıyla güncellendi. Yeni sonuçlar 'youtube_comments_with_loyalty_final.xlsx' dosyasına kaydedildi.")