# -*- coding: utf-8 -*-
"""nilSOFT Instagram kartlari v2 — HTML uret, Playwright ile PNG'ye isle."""
import os, re, random, sys
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, "out"); os.makedirs(OUT, exist_ok=True)
SEM = "/tmp/claude-0/-home-claude/f5e87bb3-b2d7-5f5f-a675-d292d69b61a0/scratchpad/artifact-files/562b167e-018f-4df2-8c62-f4d336e06b64/project"

CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
CHECK_W = CHECK.replace('currentColor', '#FFFFFF')
PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>'

def page(body, cls):
    return f'''<!doctype html><html lang="tr"><head><meta charset="utf-8">
<link rel="stylesheet" href="file://{D}/base.css"></head>
<body><div class="card {cls}">{body}</div></body></html>'''

HEAD = '''<div class="head"><div class="mark"><span>nil</span><b>SOFT</b></div>
<div class="tag">{tag}</div></div>'''

# ---------------- Aylik puantaj paneli ----------------
DAYS = list(range(1, 13))           # Kasim 2026: 1 ve 8 Pazar
HOL = {1, 8}
ROWS = [
    ("Ayşe Kaya",    "Dokuma · 1024", {},                       "75:00", "4:30"),
    ("Mehmet Demir", "Dokuma · 1031", {9: "y", 10: "y", 11: "y"}, "52:30", "2:00"),
    ("Fatma Şahin",  "Dokuma · 1047", {},                       "75:00", "6:30"),
    ("Hasan Çelik",  "Dokuma · 1052", {12: "y"},                "67:30", "3:00"),
    ("Elif Arslan",  "Dokuma · 1068", {},                       "75:00", "1:30"),
]
CODE = {"n": "N", "h": "HT", "y": "Yİ"}

def panel(rowpad=9):
    ths = "".join(f'<th class="{"hol" if d in HOL else ""}">{d}</th>' for d in DAYS)
    trs = ""
    for name, sub, special, nor, fm in ROWS:
        tds = ""
        for d in DAYS:
            k = "h" if d in HOL else special.get(d, "n")
            tds += f'<td><span class="c {k}">{CODE[k]}</span></td>'
        trs += (f'<tr><td class="who" style="padding-top:{rowpad}px;padding-bottom:{rowpad}px"><b>{name}</b><span>{sub}</span></td>'
                f'{tds}<td class="tot">{nor}</td><td class="tot fm" style="padding-right:64px">{fm}</td></tr>')
    return f'''<div class="panel">
<div class="pbar" style="padding-right:64px"><div class="ptitle">Aylık Puantaj <span>· Kasım 2026</span></div>
<div class="pctl"><span class="chip">Bölüm: Dokuma</span><span class="btn">Bordroya aktar</span></div></div>
<table class="pt"><thead><tr><th class="l">PERSONEL</th>{ths}<th>NORMAL</th><th style="padding-right:64px">FM</th></tr></thead>
<tbody>{trs}</tbody></table>
<div class="pfoot" style="padding-right:64px"><div class="okline">{CHECK}Puantaj hesaplandı, aktarıma hazır</div>
<div class="legend"><span><span class="c n">N</span>Normal</span><span><span class="c h">HT</span>Hafta tatili</span><span><span class="c y">Yİ</span>Yıllık izin</span></div></div>
</div>'''

def card_puantaj(story=False):
    h1 = 96 if story else 80
    lh = 104 if story else 86
    body = HEAD.format(tag="PERSONEL DEVAM KONTROL SİSTEMİ")
    body += f'<p class="kicker" style="margin-top:{60 if story else 44}px">Giriş-çıkıştan bordroya,</p>'
    body += f'<h1 class="h1" style="font-size:{h1}px;line-height:{lh}px">puantaj <em>kendiliğinden</em> hazır.</h1>'
    body += f'<div style="margin-top:{56 if story else 40}px;width:1040px;{"transform:scale(1.0);" if not story else ""}">{panel(14 if story else 9)}</div>'
    fs = 32 if story else 28
    body += f'''<div class="feats" style="margin-top:{56 if story else 40}px;gap:{16 if story else 12}px">
<div class="feat" style="font-size:{fs}px;line-height:{fs+10}px"><i></i><span>Kart ve parmak izi cihazlarından <strong>otomatik veri</strong></span></div>
<div class="feat" style="font-size:{fs}px;line-height:{fs+10}px"><i></i><span>Vardiya, fazla mesai ve izin <strong>tek ekranda</strong></span></div>
<div class="feat" style="font-size:{fs}px;line-height:{fs+10}px"><i></i><span><strong>Tüm bordro programlarına</strong> aktarım</span></div></div>'''
    body += '<div style="flex:1"></div>'
    body += '''<div class="band"><div class="big">Ücretsiz demo</div>
<div class="small">nilyazilim.com.tr<span>0 541 796 58 10</span></div></div>'''
    return page(body, "story" if story else "post")

# ---------------- Mobil ----------------
def qr_svg(seed=11, n=25):
    random.seed(seed)
    cells = []
    def finder(x, y):
        cells.append(f'<rect x="{x}" y="{y}" width="7" height="7" fill="#182133"/>')
        cells.append(f'<rect x="{x+1}" y="{y+1}" width="5" height="5" fill="#FFFFFF"/>')
        cells.append(f'<rect x="{x+2}" y="{y+2}" width="3" height="3" fill="#182133"/>')
    for i in range(n):
        for j in range(n):
            infinder = (i < 8 and j < 8) or (i > n-9 and j < 8) or (i < 8 and j > n-9)
            if not infinder and random.random() < 0.48:
                cells.append(f'<rect x="{i}" y="{j}" width="1" height="1" fill="#182133"/>')
    finder(0, 0); finder(n-7, 0); finder(0, n-7)
    return f'<svg viewBox="0 0 {n} {n}" shape-rendering="crispEdges" aria-hidden="true"><rect width="{n}" height="{n}" fill="#FFFFFF"/>{"".join(cells)}</svg>'

def phone(scale=1.0):
    return f'''<div class="phone" style="transform:scale({scale});transform-origin:top left">
<div class="screen"><div class="notch"></div>
<div class="ahead"><div class="brand"><b>nil</b>SOFT PDKS</div><h3>Günaydın, Ayşe</h3><p>Merkez Fabrika · Dokuma</p></div>
<div class="scan"><div class="qrbox"><i class="corner tl"></i><i class="corner tr"></i><i class="corner bl"></i><i class="corner br"></i>{qr_svg()}</div>
<small>Lokasyon QR kodunu okutun</small></div>
<div class="loc">{PIN}Konum doğrulandı</div>
<div class="rec"><div><span>Giriş</span><b>07:58</b></div><div><span>Çıkış</span><b class="muted">—</b></div></div>
</div></div>'''

TOAST = f'''<div class="toast" style="{{pos}}"><div class="ic">{CHECK_W}</div>
<div><b>Giriş kaydedildi</b><span><span class="t">07:58</span> · Merkez Fabrika</span></div></div>'''

def card_mobil(story=False):
    body = HEAD.format(tag="PDKS MOBİL")
    if not story:
        body += '''<div style="max-width:520px"><p class="kicker">Saha, şantiye, şube…</p>
<h1 class="h1">giriş-çıkış<br>artık<br><em>telefonda.</em></h1></div>'''
        body += '''<div class="feats" style="margin-top:40px;max-width:480px">
<div class="feat"><i></i><span><strong>QR kod</strong> ile giriş-çıkış</span></div>
<div class="feat"><i></i><span><strong>GPS</strong> ile konum doğrulama</span></div>
<div class="feat"><i></i><span>Kayıtlar anında <strong>puantaja</strong> düşer</span></div></div>
<div class="pills" style="margin-top:40px;max-width:480px"><span class="pill">APP STORE</span><span class="pill">GOOGLE PLAY</span></div>'''
        body += f'<div style="position:absolute;right:70px;top:190px;width:426px;height:874px">{phone(1.12)}</div>'
        body += TOAST.replace("{pos}", "left:330px;top:790px")
        body += '<div style="flex:1"></div>'
        body += '''<div class="band"><div class="big">Ücretsiz demo</div>
<div class="small">nilyazilim.com.tr<span>0 541 796 58 10</span></div></div>'''
    else:
        body += '''<p class="kicker" style="margin-top:60px">Saha, şantiye, şube…</p>
<h1 class="h1" style="font-size:96px;line-height:104px">giriş-çıkış artık <em>telefonda.</em></h1>'''
        body += f'<div style="position:relative;margin:56px auto 0;width:380px;height:780px">{phone(1.0)}</div>'
        body += TOAST.replace("{pos}", "left:110px;top:1170px")
        body += '<div style="flex:1"></div>'
        body += '''<div class="pills" style="margin-bottom:28px"><span class="pill">QR KOD</span><span class="pill">GPS DOĞRULAMA</span><span class="pill">APP STORE</span><span class="pill">GOOGLE PLAY</span></div>
<div class="band"><div class="big">Ücretsiz demo</div>
<div class="small">nilyazilim.com.tr<span>0 541 796 58 10</span></div></div>'''
    return page(body, "story" if story else "post")

# ---------------- Seminer (mevcut tasarim, oldugu gibi) ----------------
def seminer(fname, w, h):
    src = open(os.path.join(SEM, fname), encoding="utf-8").read()
    inner = re.search(r"<x-dc>(.*)</x-dc>", src, re.S).group(1)
    inner = re.sub(r"<helmet>.*?</helmet>", "", inner, flags=re.S)
    inner = inner.replace("{{lacivert}}", "#0E1B3D").replace("{{vurgu}}", "#F2B33D")
    return f'''<!doctype html><html lang="tr"><head><meta charset="utf-8">
<link rel="stylesheet" href="file://{D}/base.css"><style>body{{margin:0}}</style></head>
<body><div class="sem" style="width:{w}px;height:{h}px">{inner}</div></body></html>'''

JOBS = [
    ("01_puantaj_post",  card_puantaj(False), 1080, 1350),
    ("01_puantaj_story", card_puantaj(True),  1080, 1920),
    ("02_mobil_post",    card_mobil(False),   1080, 1350),
    ("02_mobil_story",   card_mobil(True),    1080, 1920),
    ("03_seminer_post",  seminer("Instagram_Gonderi.dc.html", 1080, 1350), 1080, 1350),
    ("03_seminer_story", seminer("Instagram_Hikaye.dc.html", 1080, 1920), 1080, 1920),
]

only = set(sys.argv[1:])
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(device_scale_factor=1)
    for name, html, w, h in JOBS:
        if only and name not in only:
            continue
        path = os.path.join(D, name + ".html")
        open(path, "w", encoding="utf-8").write(html)
        pg.set_viewport_size({"width": w, "height": h})
        pg.goto("file://" + path)
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(150)
        fams = pg.evaluate("[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family+':'+f.weight)")
        pg.screenshot(path=os.path.join(OUT, name + ".png"), clip={"x": 0, "y": 0, "width": w, "height": h})
        print(name, "ok", sorted(set(fams)))
    b.close()
