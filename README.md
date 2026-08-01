# KiwiBypass - DPI Bypass Proxy (Kivy/KivyMD)

Python + KivyMD ile şık, Android uyumlu DPI bypass proxy uygulaması.
GoodbyeDPI benzeri paket parçalama + DNS çözümleme yöntemiyle engelli
siteleri (Discord, YouTube, Telegram vb.) açar.

## Özellikler

- **DNS + Fragmentation** modu (GoodbyeDPI mantığı)
- SNI split tekniği: TLS ClientHello'yu bölerek DPI'ı şaşırtır
- DNS çözümleme: Cloudflare, Google, Quad9, OpenDNS, AdGuard
- Engelli domain listesi: Discord, YouTube, Telegram ve daha fazlası
- Şık Material Design arayüz (karanlık tema)
- Canlı durum göstergesi ve log ekranı
- Ayarların kaydedilmesi
- HTTP + HTTPS (CONNECT) proxy desteği

## Windows'ta Çalıştırma (Test)

```powershell
pip install -r requirements.txt
python windows_test.py
```

> KivyMD 2.0.1 PyPI'de yok, `master.zip`'ten kurulur.
> Windows testi için: `pip install "kivymd==https://github.com/kivymd/KivyMD/archive/master.zip"`

## Android APK Derleme

### Yöntem 1: GitHub Actions (EN KOLAY - ÖNERİLEN)

Windows'ta hiçbir şey kurmadan:

1. Projeyi GitHub'a yükle (`.github/workflows/build-apk.yml` hazır)
2. GitHub'da **Actions** sekmesine git → **Build APK** → **Run workflow**
3. Bittiğinde **Artifacts**'tan APK'yı indir

Build 20-30 dk sürer, sadece ilk seferde. Sonraki buildler daha hızlı.

### Yöntem 2: WSL (Ubuntu)

Buildozer Windows'ta çalışmaz, WSL gerekir:

```powershell
# PowerShell (Yönetici):
wsl --install -d Ubuntu
```

Ubuntu içinde:
```bash
sudo apt update
sudo apt install -y python3-pip build-essential git unzip zlib1g-dev libjpeg-dev libpng-dev openjdk-17-jdk-headless python3-virtualenv
pip3 install --user --upgrade buildozer cython virtualenv

cd /mnt/c/Users/linuxunkaderi/Documents/'Default Project'/KiwiBypass
buildozer android debug
```

APK: `bin/KiwiBypass-*-arm64-v8a-debug.apk`

### Yöntem 3: Google Colab

Buildozer'ı Colab'da çalıştırabilirsin:
- Colab'e projeyi yükle → buildozer komutlarını çalıştır → APK'yı indir.

## Kullanım

1. **BASLAT** butonuna bas → proxy 8888 portunda çalışır
2. Engelli bir siteye girmeye çalış (Discord, YouTube vb.)
3. Proxy, engelli domain'leri algılayıp paketleri parçalar
4. Log ekranından ne olduğunu izle

## Nasıl Çalışır?

- **SNI Split**: DPI, TLS el sıkışmasındaki SNI (site adı) alanına bakarak
  engelliyor. KiwiBypass ClientHello'yu SNI'in tam ortasından ikiye bölüp
  ayrı TCP segmenti olarak gönderir → DPI deseni göremez.
- **DNS**: Yerel DNS yerine Cloudflare/Google gibi temiz DNS kullanarak
  DNS kayıtlarının engellenmesini aşar.
- **Proxy**: Uygulamalar bu yerel proxy'yi (8888) kullandığında trafik
  kontrol edilip sadece el sıkışma paketi parçalanır, gerisi hızlı akar.
  Ping düşük kalır.

## Modlar

| Mod | Ne yapar |
|-----|----------|
| DNS + Frag | DNS + SNI parçalama (tavsiye edilen) |
| Sadece DNS | Sadece DNS çözümleme |
| Sadece Frag | Sadece SNI parçalama (en düşük gecikme) |
| Tumu | Her ikisi + en agresif |

## Telefonda kullanım

- APK'yı kur
- **BASLAT**'a bas
- Uygulama ayarlarından DNS/port ayarlarını değiştir (veya ayarları bırak)
- Discord/YouTube vb. uygulamaları dene
