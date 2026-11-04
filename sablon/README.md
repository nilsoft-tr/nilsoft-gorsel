# nilSOFT Instagram tasarım şablonu

Seminer davetiyesiyle aynı görsel dil: lacivert `#0E1B3D` zemin, amber `#F2B33D` vurgu,
Bricolage Grotesque (başlık) + IBM Plex Sans (gövde) + IBM Plex Mono (saat/rakam).
Ürün panelleri programın açık temasından: mürekkep `#182133`, gri-mavi `#556075`, çizgi `#D3D9E3`, ürün mavisi `#2456C8`.

- Gönderi: 1080x1350 (4:5), `.card.post`
- Hikâye: 1080x1920 (9:16), `.card.story` — üst 190 px ve alt 280 px Instagram arayüzü için boş kalır
- Ürün kartlarının alt bandı: "Ücretsiz demo" + nilyazilim.com.tr / 0 541 796 58 10

## Çalıştırma
```
mkdir -p /tmp/fonts2 && cd /tmp/fonts2
B=https://raw.githubusercontent.com/google/fonts/main/ofl
curl -sfL -o Bricolage.ttf "$B/bricolagegrotesque/BricolageGrotesque%5Bopsz,wdth,wght%5D.ttf"
curl -sfL -o PlexSans.ttf "$B/ibmplexsans/IBMPlexSans%5Bwdth,wght%5D.ttf"
curl -sfL -o PlexMono-Medium.ttf "$B/ibmplexmono/IBMPlexMono-Medium.ttf"
curl -sfL -o PlexMono-SemiBold.ttf "$B/ibmplexmono/IBMPlexMono-SemiBold.ttf"
```
Sonra `build.py` içindeki kart fonksiyonlarını örnek alıp yeni kart yaz; Playwright (Python) ile işle.
`build.py` içindeki seminer işleri, başka bir tasarım tuvalinden okunan dosyalara bağlı; yeni kartlarda o kısım gerekmez.
Kartı yayına koymadan önce PNG'yi açıp taşma, çakışma ve font yüklenmesini kontrol et.
