# movbul — Movie Recommendation App (TMDb)

Basit bir film öneri uygulaması. Kullanıcı tercihlerini alır, TMDb API üzerinden öneriler ve popüler filmleri listeler.

## Özellikler
- Tür seçimi, arama kutusu
- Trend/popüler filmler
- Puan (vote_average), poster, yıl bilgisi
- Streamlit ile tek dosyada hızlı UI

## Kurulum
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # .env içine kendi TMDB v3 API anahtarını yaz
