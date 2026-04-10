# 📱 iPhone 17 Pro: Kullanıcı Yorumları ve Tasarım Algısı Analizi

Bu çalışma, YouTube üzerinde iPhone 17 Pro akıllı telefonu için yapılan izleyici geri bildirimlerini inceleyerek; cihazın dış görünümüne dair tüketici hissiyatını, görsel zafiyetleri ve bu unsurların marka prestijine olan etkilerini veri bilimi yöntemleriyle ortaya koymayı hedeflemektedir.

## 🎯 Araştırmanın Temel Amacı

Projenin ana gayesi, tüketicilerin cihaz dizaynı hakkındaki reaksiyonlarını yapay zeka araçlarıyla sayısallaştırmak ve Apple'ın görsel stratejisine dair bir avantaj-dezavantaj profili oluşturmaktır. Belirlenen alt hedefler şunlardır:

* Markanın tercih ettiği estetik dilin, hedef kitlenin gözündeki güncel konumunu saptamak.
* Tüketiciler tarafından takdir edilen tasarım detaylarının, marka sadakatine olan pozitif katkısını ölçmek.
* Yoğun eleştiri alan görsel kararların yaratabileceği potansiyel pazar risklerini belirlemek.
* Şirketin ileride atacağı ürün geliştirme adımlarına ve olası tasarım güncellemelerine veri tabanlı bir yol haritası sunmak.

## 🗂️ Veri Seti ve Kapsamı

İncelemeye konu olan veriler, tüketicilerin cihaz hakkındaki ilk izlenimlerini en doğal haliyle yansıtan YouTube yorumlarından derlenmiştir.
* Tamamen herkese açık olan iki büyük teknoloji inceleme videosunun altındaki metinler toplanmıştır.
* **Faydalanılan Kaynak Bağlantıları:**
    * 📍 `https://www.youtube.com/watch?v=s0EbxhQYeCA`
    * 📍 `https://www.youtube.com/watch?v=Cr9B6yyLZSk`

## ⚙️ Uygulanan Metodoloji

Çalışmada, klasik kural tabanlı yaklaşımlar (rule-based) ile modern büyük dil modellerinin (`meta-llama-3-8b-instruct`) harmanlandığı hibrit bir analiz yöntemi tercih edilmiştir.

### 🛠️ Teknik İşlem Adımları

1. **Veri Çekimi:** Otomasyon araçları ve YouTube API servisleri kullanılarak toplam 23.168 adet izleyici geri dönüşü elde edilmiştir.
2. **Dil Standardizasyonu:** Yabancı dildeki tüm metinler tespit edilerek yapay zeka aracılığıyla İngilizceye tercüme edilmiş ve analizde bütünlük sağlanmıştır.
3. **Metin Temizliği:** Linkler, emojiler, anlamsız bağlaçlar ve reklam içerikleri sistemden uzaklaştırılmış; geriye net 19.603 adet analiz edilebilir metin bırakılmıştır.
4. **Odak Filtrelemesi:** Sadece "kamera, çerçeve, estetik, incelik" gibi dış görünüşü niteleyen kavramlar süzülmüş, performans gibi teknik donanım kelimeleri dışarıda bırakılarak 4.245 adet tasarım odaklı yorum izole edilmiştir.
5. **Duygu Sınıflandırması:** Elde edilen odaklı veri seti; Olumlu, Olumsuz ve Tarafsız (Nötr) şeklinde üç gruba ayrılmış ve %85 – %90 bandında bir doğruluk oranına ulaşılmıştır.

## 📈 İstatistiksel Bulgular ve Kelime Analizi

Tasarım odaklı 4.245 metin üzerinde yapılan duygu sınıflandırması, kitlenin iPhone 17 Pro'nun görünümü konusunda tam anlamıyla ikiye bölündüğünü (kutuplaştığını) kanıtlamaktadır.

**Genel Duygu Dağılımı:**
* **Pozitif Yaklaşım:** 1.624 Metin
* **Negatif Yaklaşım:** 1.621 Metin
* **Nötr (Tarafsız):** 934 Metin

### 🟢 Olumlu İzlenimler: Zarafet ve Modern Çizgiler
Beğenilerin odak noktasında cihazın premium hissiyatı, inceliği ve yeni sunulan renk skalası yer almaktadır. Yeni gövde formu, ürünün teknolojik kimliğini başarıyla desteklemektedir.
* **Öne Çıkan Kavramlar:** *like / love* (Duygusal beğeni - 648 Frekans), *looks* (Modern duruş - 268 Frekans), *color / orange / blue* (Renk geçişi memnuniyeti), *thin* (Zarif ve hafif yapı).

### 🔴 Olumsuz İzlenimler: Orantısızlık ve Beklenti Kırıklığı
Şikayetlerin merkezi; arka modülün estetik olmayan çıkıntısı, orantı sorunları ve önceki modellere göre tasarımsal bir sıçrama yaşanmamasıdır. Kullanıcılar devrimsel bir yenilik görememekten şikayetçidir.
* **Öne Çıkan Kavramlar:** *ugly* (Görsel uyumsuzluk ve çirkinlik - 204 Frekans), *nothing / changed* (İnovasyon noksanlığı - 280 Frekans toplamı), *camera bump* (Rahatsız edici kamera adası).

### ⚪ Nötr İzlenimler: İkna Edilemeyen Kitle
Bu gruptakiler cihazın görsel bir potansiyeli olduğuna inansa da ilk bakışta tam olarak tatmin olmamıştır. Fiziksel kullanım tecrübesinin nihai kararı belirleyeceği vurgulanmaktadır.
* **Öne Çıkan Kavramlar:** *samsung* (Rakiplerle yapılan kıyaslamalar), *look* (Kararsız ilk bakış).

## ⚠️ Marka İmajını Bekleyen Riskler

Analiz sonucunda, Apple'ın mevcut tasarım stratejisinde acilen çözülmesi gereken üç temel zafiyet tespit edilmiştir:

1. **Optik Modül Orantısızlığı:** Kamera adasının gövdenin geri kalanından bağımsız ve aşırı büyük durması, estetik bütünlüğü ciddi şekilde bozmaktadır.
2. **Kısır Döngü Algısı:** Tüketiciler, tasarımsal olarak heyecan verici bir yenilik görememekte ve "hep aynı tasarım" eleştirisi markaya zarar vermektedir.
3. **Görsel Kalınlık Yanılsaması:** Cihaz kağıt üzerinde çok ince planlanmış olsa da, detaylardaki mühendislik kararları kullanıcılara cihazın kalın ve hantal olduğu izlenimini vermektedir.

## 💡 Gelecek İçin Stratejik Çıkarımlar

Sonuçlar incelendiğinde; iPhone 17 Pro'nun dış görünümü aslında sağlam temellere dayanmaktadır ancak bu vizyon tüketiciye doğru yansıtılamamıştır. Yani sorun doğrudan tasarımın kendisinde değil, markanın izlediği iletişim stratejisindedir. Bu durumu düzeltmek için şu adımlar tavsiye edilmektedir:

* **Geometrik Dengeleme:** Arka kamera modülünün fiziksel yapısı veya konumlandırması, gözü daha az yoracak ve daha dengeli hissettirecek şekilde revize edilmelidir.
* **Şeffaf İletişim Stratejisi:** Marka, cihazın "neden bu formda tasarlandığını" tüketiciye dürüstçe açıklamalı, mühendislik kararlarının arkasındaki faydayı anlatarak oluşabilecek önyargıları kırmalıdır.
* **Kişiselleştirilmiş Yaklaşım:** Sektördeki "tek bir kalıp herkese uyar" anlayışı artık terk edilmelidir. Farklı beklentilere yanıt veren özel kaplama seçenekleri ve sınırlı koleksiyonlar üretilmelidir.
* **Somut Deneyim Odaklı Tanıtım:** İkna olmakta zorlanan kitleler için; soyut ve fütüristik reklamlar yerine, insanların cihazın ergonomisini doğrudan ellerinde hissedecekleri somut tanıtım materyalleri kullanılmalıdır.
