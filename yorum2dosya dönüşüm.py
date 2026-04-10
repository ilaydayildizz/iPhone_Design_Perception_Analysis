import pandas as pd

# CSV dosya adınızı buraya yazın
csv_file = "youtube_all_comments2.csv"
excel_file = "youtube_all_comments2.xlsx"

# CSV'yi oku
df = pd.read_csv(csv_file, encoding="utf-8")

# Excel'e kaydet
df.to_excel(excel_file, index=False)

print("✔ Dönüştürme tamamlandı!")
print(f"📁 Oluşturulan dosya: {excel_file}")
