# -*- coding: utf-8 -*-
"""nilSOFT yeni modül kartları (Servis Planlama, SGK Raporları) — base.css ile, Playwright'la işlenir."""
import os, sys
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, "out"); os.makedirs(OUT, exist_ok=True)

CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'

EXTRA = """
<style>
.tagnew { display:inline-flex; align-items:center; gap:12px; }
.tagnew b { background: var(--amber); color: var(--lac); font-size: 17px; line-height: 22px; letter-spacing: .14em; padding: 3px 10px; font-weight: 700; }
/* servis listesi */
.svc { display:grid; grid-template-columns: 300px minmax(0,1fr); }
.svl { border-right:1px solid var(--line); background: var(--white); }
.svi { display:flex; gap:14px; align-items:flex-start; padding:16px 20px; border-bottom:1px solid #E8EBF0; }
.svi.on { background: var(--blue-soft); box-shadow: inset 4px 0 0 var(--blue); }
.svi .no { flex:none; width:34px; height:34px; border-radius:8px; background: var(--hol); color: var(--slate); font-family: var(--mono); font-weight:600; font-size:16px; display:grid; place-items:center; }
.svi.on .no { background: var(--blue); color: var(--white); }
.svi b { display:block; font-size:18px; line-height:22px; }
.svi span { font-size:15px; color: var(--slate); }
.map { position:relative; background:#EAF0F7; }
.map svg { display:block; width:100%; height:100%; }
/* sgk tablosu */
.sg td, .sg th { text-align:left; }
.sg th { font-family: var(--body); letter-spacing:.06em; padding-left: 0; }
.sg th:first-child, .sg td:first-child { padding-left: 24px; }
.sg td { padding: 13px 0; font-size: 17px; }
.vk { display:inline-block; font-size:14px; font-weight:600; padding:3px 9px; border-radius:5px; background: var(--hol); color:#4B556B; }
.vk.kaza { background:#FDE8D7; color:#8A4300; }
.dt { font-family: var(--mono); font-weight:600; font-size:16px; }
.st-ok { display:inline-flex; align-items:center; gap:6px; color: var(--ok); font-weight:600; font-size:16px; }
.st-ok svg { width:18px; height:18px; }
.st-btn { display:inline-block; background: var(--blue); color:#fff; font-size:15px; font-weight:600; padding:6px 12px; border-radius:6px; }
</style>"""

def page(body, cls):
    return f'''<!doctype html><html lang="tr"><head><meta charset="utf-8">
<link rel="stylesheet" href="file://{D}/base.css">{EXTRA}</head>
<body><div class="card {cls}">{body}</div></body></html>'''

def head(mod):
    return f'''<div class="head"><div class="mark"><span>nil</span><b>SOFT</b></div>
<div class="tag tagnew"><b>YENİ</b>{mod}</div></div>'''

BAND = '''<div class="band"><div class="big">Ücretsiz demo</div>
<div class="small">nilyazilim.com.tr<span>0 541 796 58 10</span></div></div>'''

def feats(items, story):
    fs = 32 if story else 28
    rows = "".join(f'<div class="feat" style="font-size:{fs}px;line-height:{fs+10}px"><i></i><span>{t}</span></div>' for t in items)
    return f'<div class="feats" style="margin-top:{52 if story else 36}px;gap:{16 if story else 12}px">{rows}</div>'

def title(kicker, h1, story):
    return (f'<p class="kicker" style="margin-top:{60 if story else 44}px">{kicker}</p>'
            f'<h1 class="h1" style="font-size:{96 if story else 80}px;line-height:{104 if story else 86}px">{h1}</h1>')

# ---------------- Servis Planlama ----------------
def map_svg():
    roads = [
        "M0,80 C180,70 360,100 700,85", "M0,200 C200,190 420,215 700,198", "M0,320 C200,310 420,335 700,318",
        "M110,0 C120,140 95,280 125,420", "M330,0 C318,150 345,280 332,420", "M540,0 C528,140 555,280 545,420",
    ]
    r = "".join(f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="16" stroke-linecap="round"/>' for d in roads)
    r += "".join(f'<path d="{d}" fill="none" stroke="#D9E1EC" stroke-width="1.5"/>' for d in roads)
    stops = [(110, 84), (114, 196), (222, 202), (332, 205), (336, 316), (440, 322)]
    path = "M" + " L".join(f"{x},{y}" for x, y in stops) + " L545,320 L545,345"
    pins = "".join(
        f'<circle cx="{x}" cy="{y}" r="16" fill="#FFFFFF" stroke="#2456C8" stroke-width="4"/>'
        f'<text x="{x}" y="{y+0.5}" text-anchor="middle" dominant-baseline="central" font-family="IBM Plex Mono" font-weight="600" font-size="16" fill="#2456C8">{i+1}</text>'
        for i, (x, y) in enumerate(stops))
    fab = ('<rect x="495" y="345" width="100" height="42" rx="8" fill="#F2B33D"/>'
           '<text x="545" y="366.5" text-anchor="middle" dominant-baseline="central" font-family="IBM Plex Sans" font-weight="700" font-size="15" fill="#0E1B3D" letter-spacing="1">FABRİKA</text>')
    return (f'<svg viewBox="0 0 700 420" preserveAspectRatio="xMinYMid slice" aria-hidden="true">'
            f'<rect width="700" height="420" fill="#EAF0F7"/>{r}'
            f'<path d="{path}" fill="none" stroke="#2456C8" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" opacity=".9"/>'
            f'{pins}{fab}</svg>')

def servis_panel(h):
    items = [("1", "Servis 1 · Dokuma", "12 kişi · 6 durak", True),
             ("2", "Servis 2 · Konfeksiyon", "9 kişi · 5 durak", False),
             ("3", "Servis 3 · Boyahane", "11 kişi · 7 durak", False),
             ("4", "Servis 4 · Paketleme", "8 kişi · 4 durak", False)]
    lst = "".join(f'<div class="svi{" on" if on else ""}"><div class="no">{n}</div><div><b>{a}</b><span>{b}</span></div></div>'
                  for n, a, b, on in items)
    return f'''<div class="panel" style="width:1040px">
<div class="pbar" style="padding-right:64px"><div class="ptitle">Servis Planlama <span>· Sabah vardiyası</span></div>
<div class="pctl"><span class="chip">Güzergâh: 18,4 km</span><span class="btn">Şoför listesi</span></div></div>
<div class="svc" style="height:{h}px"><div class="svl">{lst}</div><div class="map">{map_svg()}</div></div></div>'''

def card_servis(story=False):
    b = head("SERVİS PLANLAMA")
    b += title("Servis listeleri Excel'de dağılmasın.", "Servisler artık <em>haritada.</em>", story)
    b += f'<div style="margin-top:{56 if story else 40}px">{servis_panel(420)}</div>'
    b += feats(["Personeli servislere atayın, <strong>durak sırasını</strong> belirleyin",
                "Güzergâhı <strong>haritada</strong> görün",
                "Şoför listesini <strong>tek tıkla</strong> yazdırın"], story)
    b += '<div style="flex:1"></div>' + BAND
    return page(b, "story" if story else "post")

# ---------------- SGK Raporları ----------------
def sgk_panel(pad):
    rows = [("Ayşe Kaya", "Dokuma", "Hastalık", "", "03.11 – 05.11", True),
            ("Mehmet Demir", "Konfeksiyon", "İş kazası", "kaza", "10.11 – 14.11", True),
            ("Fatma Şahin", "Dokuma", "Hastalık", "", "18.11 – 19.11", False),
            ("Hasan Çelik", "Boyahane", "Hastalık", "", "20.11 – 22.11", False)]
    trs = ""
    for n, bol, vk, vc, dt, ok in rows:
        st = (f'<span class="st-ok">{CHECK}Aktarıldı</span>' if ok else '<span class="st-btn">İzne aktar</span>')
        trs += (f'<tr><td class="who" style="padding-top:{pad}px;padding-bottom:{pad}px"><b>{n}</b><span>{bol}</span></td>'
                f'<td><span class="vk {vc}">{vk}</span></td><td class="dt">{dt}</td><td style="padding-right:64px">{st}</td></tr>')
    return f'''<div class="panel" style="width:1040px">
<div class="pbar" style="padding-right:64px"><div class="ptitle">SGK Raporları <span>· Kasım 2026</span></div>
<div class="pctl"><span class="btn">e-Vizite'den indir</span></div></div>
<table class="pt sg"><thead><tr><th>PERSONEL</th><th>VAKA</th><th>RAPOR DÖNEMİ</th><th style="padding-right:64px">DURUM</th></tr></thead>
<tbody>{trs}</tbody></table>
<div class="pfoot" style="padding-right:64px"><div class="okline">{CHECK}2 rapor izne aktarıldı</div><div>2 rapor bekliyor</div></div></div>'''

def card_sgk(story=False):
    b = head("SGK RAPORLARI")
    b += title("e-Vizite'ye girip tek tek bakmayın.", "SGK raporları <em>tek tıkla</em> izne.", story)
    b += f'<div style="margin-top:{56 if story else 40}px">{sgk_panel(16 if story else 11)}</div>'
    b += feats(["Raporlar SGK e-Vizite'den <strong>program içinden</strong> gelir",
                "Personel <strong>TC kimlik no</strong> ile eşleşir",
                "Aynı rapor <strong>iki kez aktarılmaz</strong>"], story)
    b += '<div style="flex:1"></div>' + BAND
    return page(b, "story" if story else "post")

JOBS = [("04_servis_post", card_servis(False), 1080, 1350), ("04_servis_story", card_servis(True), 1080, 1920),
        ("05_sgk_post", card_sgk(False), 1080, 1350), ("05_sgk_story", card_sgk(True), 1080, 1920)]

only = set(sys.argv[1:])
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(device_scale_factor=1)
    for name, html, w, h in JOBS:
        if only and name not in only: continue
        path = os.path.join(D, name + ".html"); open(path, "w", encoding="utf-8").write(html)
        pg.set_viewport_size({"width": w, "height": h}); pg.goto("file://" + path)
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(150)
        over = pg.evaluate("(()=>{const c=document.querySelector('.card');return [...c.children].some(e=>e.getBoundingClientRect().bottom>c.getBoundingClientRect().bottom+1)})()")
        pg.screenshot(path=os.path.join(OUT, name + ".png"), clip={"x": 0, "y": 0, "width": w, "height": h})
        print(name, "ok", "TASMA!" if over else "")
    br.close()
