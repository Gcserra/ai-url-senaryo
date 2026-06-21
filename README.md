# 🧪 Test Senaryosu Üretici Yapay Zeka Aracı (PoC)

Bu proje, bir web sayfası ya da ekran görüntüsünü analiz ederek yazılım test ekipleri için otomatik test senaryosu başlıkları ve adımları üreten bir yapay zeka uygulamasıdır. 

## 🚀 Özellikler

- 🌐 Web sayfası URL’sini analiz eder
- 🖼️ Ekran görüntüsünden OCR ile metin çıkartır
- 🧠 OpenAI GPT ile kullanıcı hikayesine uygun test senaryoları üretir
- 📄 Senaryoları `.txt` veya `.pdf` olarak dışa aktarır
- 🌍 Çok dilli çıktı (Türkçe / İngilizce)
- 📊 Analiz başarı oranı gösterimi

## 🛠️ Kullanılan Teknolojiler

- `Streamlit`: Web arayüzü
- `requests`, `beautifulsoup4`: Web sayfası içeriği çekme
- `openai`: GPT-3.5 veya GPT-4 API kullanımı
- `pytesseract`: OCR (Ekran görüntüsü analizi)
- `fpdf`: PDF çıktısı oluşturma
- `python-dotenv`: API anahtarı yönetimi

