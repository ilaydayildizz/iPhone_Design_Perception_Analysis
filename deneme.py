import pandas as pd

df = pd.read_excel("youtube_comments_translated_en.xlsx")


buy_list = []
for i in df["text_english"].tolist():
    try:
        if "buy" in i.lower():
            print(i)
            buy_list.append(i)
    except:
        pass

print(len(buy_list))

import nltk
import re
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)  # özel karakterleri sil
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return " ".join(words)

cleaned_comments = [clean_text(c) for c in buy_list]


from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(
    max_df=0.9,
    min_df=2,
    ngram_range=(1, 2)
)

X = vectorizer.fit_transform(cleaned_comments)

from sklearn.decomposition import LatentDirichletAllocation

num_topics = 10  # konu sayısı (tasarım, kamera, batarya gibi)

lda = LatentDirichletAllocation(
    n_components=num_topics,
    random_state=42
)

lda.fit(X)

feature_names = vectorizer.get_feature_names_out()

def print_topics(model, feature_names, top_n=6):
    for idx, topic in enumerate(model.components_):
        print(f"\n🟢 Topic {idx + 1}")
        print(" ".join(
            feature_names[i]
            for i in topic.argsort()[:-top_n - 1:-1]
        ))

print_topics(lda, feature_names)