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

## v3 — Kampanya tarzı (24.11.2026'dan itibaren ASIL ŞABLON budur)
Mustafa'nın geri bildirimi: "renkler vs hepsi birbirinin aynısı, senden çıktığı belli oluyor; farklı farklı ve alımlı yap."
Referans: `ornekler/` klasöründeki kendi hikâye reklamları. Örnek kod: `sablon/kampanya.py` (A = zümrüt gece, B = krem-bordo).

Kurallar:
- **Her gönderi ayrı renk dünyası.** Arka arkaya iki gönderide aynı palet olmaz. Palet havuzu: zümrüt gece (yeşil + nane→sarı), krem + bordo/mercan, gece mavisi + turuncu, mor + sarı, petrol + mercan, antrasit + neon yeşil, bordo + altın. Lacivert-amber "kurumsal" kart yalnız arada bir.
- **Yerleşim de değişir.** Arketipler: 3B eğik ekran + telefon kolajı; "önce → sonra" akışı (iki kart + kesik ok); dev rakam / istatistik; tek telefon kahraman; çip ızgarası + büyük ürün ekranı.
- Başlık: Bricolage Grotesque 800, `font-stretch:75%` (dar), 110–136 px, 2–3 satır; bir satır degrade dolgulu; altına el çizimi çift çizgi.
- El yazısı vurgu (Kaushan Script) bir kısa ifade için: "rota hazır!", "e-Vizite'ye girmeden!", "daha ötesi".
- Noktalı doku (24 px ızgara) + köşelerde yumuşak ışık.
- Gerçek logo: `sablon/logo_white.png` (koyu zemin), `sablon/logo_navy.png` (açık zemin), sağ üst.
- Yüzen beyaz etiketler (ikonlu), "YENİ MODÜL" hapı, özellik çipleri (tik işaretli hap), en altta büyük degrade "Ücretsiz demo" bandı + yuvarlak ok butonu; alt satır: "Kendi verinizle canlı gösterim · 0 541 796 58 10".
- Mümkünse `ekran/` klasöründeki gerçek ekran görüntülerini kullan (eğik, gölgeli). Çizim panel sadece gerçek görüntü yoksa.
- Yerel detay: Denizli semt adları (Sırakapılar, Bağbaşı, Gerzele, Kınıklı, Çamlaraltı), tekstil bölümleri (Dokuma, Konfeksiyon, Boyahane).
- Fontlar: yukarıdakilere ek `curl -sfL -o /tmp/fonts2/KaushanScript.ttf "$B/kaushanscript/KaushanScript-Regular.ttf"`.

## Gerçek ekran görüntüsü kullanımı (24.11.2026)
`ekran/` klasöründe Mustafa'nın gönderdiği gerçek ekranlardan kesilmiş görseller durur (ör. `ekran/servis_planlama_harita.png`).
Örnek kullanım: `sablon/servis_v3.py` (eğik, beyaz çerçeveli gerçek harita + günlük liste kâğıdı + yüzen etiket).
Kesim kuralı: personel adresi, telefon, TC gibi kişisel alanlar görselde kalmaz; harita kullanılıyorsa "© OpenStreetMap katkıcıları" yazısı görünür kalır.
Mustafa'nın vurgulanmasını istediği ifadeler (Servis Planlama): "Otomatik personel ataması", "Haritada otomatik güzergâh".
