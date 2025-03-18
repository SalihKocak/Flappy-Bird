# Flappy Bird Oyunu
Bu proje, Python ve Pygame kullanılarak geliştirilmiş klasik Flappy Bird oyununun özelleştirilmiş bir versiyonudur. Birden fazla karakter, ses efektleri ve çeşitli oyun ekranları içerir.
Özellikler
5 farklı karakterle oynama imkanı (Phoenix, Shadow, Storm, Crystal, Dragon)
Ana menü, karakter seçim ekranı ve oyun sonu ekranı
Puan sistemi
Arkaplan müziği ve ses efektleri
Oyunu duraklatma özelliği
Modern ve kullanıcı dostu arayüz
Animasyonlu kuş karakterleri
Gereksinimler
Python 3.x
Pygame
Kurulum

1. Repoyu bilgisayarınıza klonlayın:
```
git clone https://github.com/kullaniciadi/flappy-bird.git
cd flappy-bird
```

2. Gerekli bağımlılıkları yükleyin:
```
pip install -r requirements.txt
```

3. Oyunu çalıştırın:
```
python Game.py
```

Oyun Kontrolleri
Boşluk Tuşu: Zıpla
Fare Tıklaması: Menülerde seçim yapma
Sağ Üst Köşedeki Pause Butonu: Oyunu duraklat/devam ettir

Proje Yapısı
```
flappy-bird/
├── Game.py          # Ana oyun dosyası
├── assets/          # Oyun içi grafik ve ses dosyaları
│   ├── background.png
│   ├── background.mp3
│   ├── bird.png     # Phoenix karakteri
│   ├── bird2.png    # Shadow karakteri
│   ├── bird3.png    # Storm karakteri
│   ├── bird4.png    # Crystal karakteri
│   ├── bird5.png    # Dragon karakteri
│   ├── pipe.png
│   ├── jump.mp3
│   ├── point.mp3
│   ├── hit.mp3
│   └── wing.mp3
├── README.md
└── requirements.txt
```

Not
Oyun çalıştırılmadan önce "assets" klasörünün mevcut olduğundan ve tüm resim ve ses dosyalarının bu klasörde bulunduğundan emin olun.

Ekran Görüntüleri
*Not: Projenize ekran görüntüleri ekleyerek README dosyanızı zenginleştirebilirsiniz.*

İyi oyunlar!

requirements.txt içeriği
