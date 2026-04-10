import requests
import pandas as pd

# LM Studio'da çalışan Llama 3 sunucunun adresi
LMSTUDIO_URL = "http://169.254.222.168:1234"

# ================================
# 1️⃣ Anahtar Kelime Filtreleri
# ================================
design_keywords = [
    # Genel tasarım / görünüş
    "design", "redesign", "looks", "look", "looking", "style", "styled",
    "aesthetic", "aesthetics", "appearance", "visual", "visually",
    "beautiful", "ugly", "sleek", "elegant", "minimal", "minimalist",
    "premium", "cheap looking", "cheap-looking", "toy-like",
    "futuristic", "boring", "outdated", "clean", "cluttered",

    # Renk / yüzey / kaplama
    "color", "colour", "colors", "colours",
    "matte", "glossy", "shiny", "finish", "coating",
    "black", "white", "silver", "blue", "orange", "gold", "sage",

    # Form / gövde
    "thin", "thickness", "thinner", "thick",
    "edges", "bezel", "bezels", "frame", "housing",
    "shape", "form factor", "camera bump", "camera island",
    "build quality", "build", "brick", "wallet", "chic",
]

not_design_noise = [
    # Performans / donanım
    "battery", "screen on time", "sot", "performance", "lag", "bug", "heat",
    "overheat", "overheating", "fps", "ram", "cpu", "gpu", "chip", "chipset",
    "benchmark", "geekbench", "antutu",

    # Fiyat / satın alma
    "price", "expensive", "cheap", "value", "deal", "discount",
    "buy", "bought", "purchase", "ordering", "order", "sell", "selling",

    # Depolama / özellikler
    "storage", "128gb", "256gb", "512gb", "1tb", "2tb",
    "features", "specs", "specifications",

    # Yazılım / sistem
    "software", "ios", "android", "update", "upgrade", "beta",
    "ios 18", "ios 19", "ios 26",

    # Kamera fonksiyonları (tasarım değil)
    "camera quality", "macro", "telephoto", "zoom", "video quality",
    "stabilization", "photo quality",

    # Kullanım / günlük deneyim
    "daily driver", "battery life", "charging", "charger", "fast charge",
]


# ================================
# 2️⃣ Llama 3 ile Hibrit Sınıflandırma
# ================================
def classify_with_llama3(text: str) -> str:
    """
    Metni Llama 3'e gönderir, sadece 'design' veya 'not_design' döndürmeye zorlar.
    """
    prompt = f"""
You are a strict classification model.

TASK:
Classify the following smartphone-related comment into exactly one of two labels:

- design  → if it mainly talks about appearance, aesthetics, how it looks, color, finish, camera bump, bezels, thinness, shape, frame, or overall visual style.
- not_design → if it mainly talks about battery, performance, price, storage, software, charging, camera specs, features, daily usage, bugs, heating, or purchasing decisions.

RULES:
- Focus on the MAIN topic of the comment.
- If both design and non-design topics appear, choose the dominant topic.
- If the topic is unclear or you are uncertain, choose "not_design".
- Your answer MUST be exactly one word: "design" or "not_design".
- Do NOT add explanations, punctuation, or extra text.

COMMENT:
\"\"\"{text}\"\"\"


Answer with exactly:
design
or
not_design
"""

    payload = {
        "prompt": prompt,
        "temperature": 0.0,   # deterministik
        "max_tokens": 5
    }

    try:
        response = requests.post(LMSTUDIO_URL, json=payload, timeout=30)
        response.raise_for_status()
        raw = response.json().get("response", "").strip().lower()
        if raw == "design":
            return "design"
        else:
            return "not_design"
    except Exception as e:
        # Model / bağlantı hatası varsa güvenli tarafta kal
        print(f"⚠️ Llama 3 isteğinde hata: {e}")
        return "not_design"


def hybrid_label(text: str) -> str:
    """
    1) Önce keyword'lerle hızlı karar
    2) Kararsızsa Llama 3'e sor
    """
    if not isinstance(text, str):
        text = "" if pd.isna(text) else str(text)

    lower = text.lower()

    # 1️⃣ Tasarım kelimeleri varsa ve teknik baskın değilse → design
    has_design = any(kw in lower for kw in design_keywords)
    has_noise = any(kw in lower for kw in not_design_noise)

    if has_design and not has_noise:
        return "design"

    if has_noise and not has_design:
        return "not_design"

    # 2️⃣ Karışık / belirsiz ise → Llama 3'e sor
    return classify_with_llama3(text)


# ================================
# 3️⃣ Excel'deki Yorumları Etiketle
# ================================
INPUT_FILE = "temizlenmis_yorumlar2.xlsx"
OUTPUT_FILE = "llama3_hibrit_etiketli2.xlsx"

print(f"📥 Excel yükleniyor: {INPUT_FILE}")
df = pd.read_excel(INPUT_FILE)

if "temiz_yorum" not in df.columns:
    raise ValueError("❌ 'temiz_yorum' adında bir sütun bulunamadı. Excel'deki sütun adını kontrol et.")

print("🧠 Llama 3 ile yorumlar etiketleniyor (hibrit yöntem)...")

labels = []
for i, text in enumerate(df["temiz_yorum"]):
    label = hybrid_label(text)
    labels.append(label)

    # Biraz ilerleme göstergesi
    if (i + 1) % 100 == 0:
        print(f"   ➜ {i+1} yorum etiketlendi...")

df["label"] = labels

df.to_excel(OUTPUT_FILE, index=False)
print(f"🎉 İşlem bitti! Etiketli dosya kaydedildi: {OUTPUT_FILE}")
