# -*- coding: utf-8 -*-
"""Yıllık İzin Planlama kartı v3 — mor gece + güneş sarısı. Yıl çizelgesi (Haz–Eyl 2027 yakınlaştırması, çizim)
ve Uyarılar kartı. Gerçek ekran görüntüsü gelince .gp bloğu yerine ekran/ altındaki kırpım konur."""
import os, datetime as dt
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, "out"); os.makedirs(OUT, exist_ok=True)
F = "/tmp/fonts2"

YEAR = 2027
T0 = dt.date(YEAR, 6, 1)          # çizelgenin ilk günü
T1 = dt.date(YEAR, 9, 30)         # son günü
DAYS = (T1 - T0).days + 1         # 122
PX = 6                            # gün başına piksel
W = DAYS * PX                     # 732
L = 250                           # sol sütun

def x(m, d):
    return (dt.date(YEAR, m, d) - T0).days * PX

def span(m1, d1, m2, d2):
    a, b = dt.date(YEAR, m1, d1), dt.date(YEAR, m2, d2)
    assert a.weekday() == 0 and b.weekday() == 4, (a, b, "Pzt–Cum olmalı")
    return x(m1, d1), ((b - a).days + 1) * PX

CSS = f"""
@font-face {{ font-family:"Brico"; src:url("file://{F}/Bricolage.ttf"); font-weight:200 800; font-stretch:75% 100%; }}
@font-face {{ font-family:"Plex"; src:url("file://{F}/PlexSans.ttf"); font-weight:100 700; font-stretch:85% 100%; }}
@font-face {{ font-family:"PlexMono"; src:url("file://{F}/PlexMono-SemiBold.ttf"); font-weight:600; }}
@font-face {{ font-family:"Kaushan"; src:url("file://{F}/KaushanScript.ttf"); }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
html,body {{ background:#000; }}
.cv {{ position:relative; overflow:hidden; width:1080px; font-family:"Plex",sans-serif; color:#fff;
  background:
   radial-gradient(820px 560px at 92% 4%, rgba(255,214,90,.26), transparent 62%),
   radial-gradient(760px 700px at 0% 100%, rgba(255,110,160,.20), transparent 60%),
   radial-gradient(rgba(255,255,255,.10) 1.3px, transparent 1.6px) 0 0/24px 24px,
   linear-gradient(160deg,#4A2296 0%,#32166E 45%,#1C0B42 100%); }}
.abs {{ position:absolute; }}
.hd {{ font-family:"Brico"; font-weight:800; font-stretch:75%; letter-spacing:-0.01em; line-height:.9; }}
.grad {{ background-image:linear-gradient(90deg,#FFE566 0%,#FFB648 55%,#FF86A6 100%); -webkit-background-clip:text; background-clip:text; color:transparent; padding-bottom:.06em; }}
.pill {{ display:inline-flex; align-items:center; gap:12px; border-radius:999px; font-weight:600; letter-spacing:.12em;
  background:rgba(255,229,102,.13); border:2px solid rgba(255,229,102,.55); color:#FFF1B0; }}
.sub {{ color:#DCCFFB; font-weight:500; line-height:1.32; }}
.sub b {{ color:#fff; font-weight:600; }}

/* ---- yıl çizelgesi ---- */
.gp {{ background:#fff; color:#21143F; border-radius:20px; overflow:hidden; border:6px solid #fff;
  box-shadow:0 50px 90px rgba(8,2,30,.6), 0 0 120px rgba(255,214,90,.16); }}
.gbar {{ display:flex; align-items:center; justify-content:space-between; padding:0 16px 0 18px; height:58px; background:#F6F3FC; border-bottom:1px solid #E2DAF3; }}
.gbar .t {{ font-size:19px; font-weight:700; white-space:nowrap; }}
.gbar .t span {{ display:inline-block; margin-left:10px; font-family:"PlexMono"; font-size:13px; color:#5B4B8A; background:#E9E1FA; border-radius:6px; padding:3px 9px; vertical-align:2px; }}
.gbtn {{ display:flex; gap:8px; }}
.gbtn span {{ font-size:14px; font-weight:600; border-radius:7px; padding:7px 12px; background:#fff; border:1px solid #D6CCEC; color:#3D2C6E; white-space:nowrap; }}
.gbtn span.p {{ background:#6D38E0; border-color:#6D38E0; color:#fff; }}
.gr {{ display:flex; border-bottom:1px solid #EDE8F7; }}
.gl {{ flex:none; width:{L}px; display:flex; align-items:center; justify-content:space-between; gap:8px; padding:0 12px 0 18px; border-right:1px solid #E2DAF3; }}
.tl {{ position:relative; flex:none; width:{W}px;
  background:
    linear-gradient(#D9D0EE,#D9D0EE) {x(7,1)}px 0/1px 100% no-repeat,
    linear-gradient(#D9D0EE,#D9D0EE) {x(8,1)}px 0/1px 100% no-repeat,
    linear-gradient(#D9D0EE,#D9D0EE) {x(9,1)}px 0/1px 100% no-repeat,
    linear-gradient(#FFDDE3,#FFDDE3) {x(7,15)}px 0/{PX}px 100% no-repeat,
    linear-gradient(#FFDDE3,#FFDDE3) {x(8,30)}px 0/{PX}px 100% no-repeat,
    repeating-linear-gradient(90deg, transparent 0 {4*PX}px, #F3EFFA {4*PX}px {6*PX}px, transparent {6*PX}px {7*PX}px); }}
.mh {{ height:30px; background:#FBFAFE; }}
.mh .gl {{ font-size:11.5px; letter-spacing:.12em; font-weight:700; color:#7A6BA6; }}
.mh .tl {{ background:none; }}
.mh .tl b {{ position:absolute; top:0; height:30px; line-height:30px; font-size:12.5px; letter-spacing:.14em; font-weight:700; color:#4B3A80; padding-left:10px; border-left:1px solid #D9D0EE; }}
.dh {{ height:22px; background:#FBFAFE; }}
.dh .tl i {{ position:absolute; top:3px; font-style:normal; font-family:"PlexMono"; font-size:11px; color:#8B7DB3; width:{5*PX}px; text-align:center; }}
.dep {{ height:38px; background:#F1ECFB; }}
.dep .gl b {{ font-size:13.5px; letter-spacing:.1em; font-weight:700; color:#3D2C6E; }}
.dep .gl span {{ font-size:12px; color:#6A5B96; font-weight:600; white-space:nowrap; }}
.dep .tl {{ background:
    linear-gradient(#D9D0EE,#D9D0EE) {x(7,1)}px 0/1px 100% no-repeat,
    linear-gradient(#D9D0EE,#D9D0EE) {x(8,1)}px 0/1px 100% no-repeat,
    linear-gradient(#D9D0EE,#D9D0EE) {x(9,1)}px 0/1px 100% no-repeat; }}
.dn {{ position:absolute; top:8px; height:22px; border-radius:6px; font-family:"PlexMono"; font-size:12.5px; line-height:22px; text-align:center; color:#4B3A80; }}
.dn.c1 {{ background:#E6DDF9; }} .dn.c2 {{ background:#D3C4F5; }} .dn.c3 {{ background:#BBA5EF; color:#2A1A57; }}
.dn.c4 {{ background:#9F82E8; color:#fff; }}
.dn.over {{ background:#E5484D; color:#fff; box-shadow:0 0 0 3px rgba(229,72,77,.25); }}
.dn.top {{ background:#FFD84D; color:#5B4300; font-family:"Plex"; font-weight:700; font-size:11px; letter-spacing:.1em; }}
.pr {{ height:46px; }}
.pr .gl b {{ font-size:16px; font-weight:600; white-space:nowrap; }}
.bd {{ font-size:11.5px; font-weight:700; border-radius:999px; padding:3px 9px; background:#EFE9FB; color:#5B4B8A; white-space:nowrap; }}
.bd.neg {{ background:#FDE3E4; color:#C22B31; }}
.bd.ok {{ background:#DDF5EA; color:#12805C; }}
.bar {{ position:absolute; top:10px; height:26px; border-radius:7px; }}
.bar.t {{ background:repeating-linear-gradient(135deg,#EDE4FF 0 6px,#DCCBFF 6px 12px); border:1.5px dashed #8B5CF6; }}
.bar.o {{ background:#6D38E0; }}
.bar.k {{ background:#12A07A; }}
.bar.y {{ background:repeating-linear-gradient(135deg,#FFE88A 0 6px,#FFD84D 6px 12px); border:1.5px solid #E0A800; }}
.lg {{ display:flex; align-items:center; gap:18px; height:38px; padding:0 18px; background:#F6F3FC; font-size:13px; font-weight:600; color:#4B3A80; }}
.lg span {{ display:inline-flex; align-items:center; gap:7px; white-space:nowrap; }}
.lg i {{ position:static; display:inline-block; width:22px; height:13px; border-radius:4px; }}

/* ---- uyarılar kartı ---- */
.wn {{ background:#fff; color:#21143F; border-radius:18px; overflow:hidden; box-shadow:0 36px 70px rgba(8,2,30,.6), 0 0 0 1px rgba(0,0,0,.05); }}
.wn-h {{ display:flex; align-items:center; justify-content:space-between; padding:13px 18px 11px; background:#21143F; color:#fff; }}
.wn-h b {{ font-size:14px; letter-spacing:.16em; font-weight:700; }}
.wn-h span {{ font-family:"PlexMono"; font-size:13px; background:#FFD84D; color:#3A2A00; border-radius:999px; padding:1px 10px; }}
.wr {{ display:flex; align-items:center; gap:13px; padding:11px 18px; border-bottom:1px solid #EEE9F7; }}
.wr:last-child {{ border-bottom:0; }}
.wr .ic {{ flex:none; width:34px; height:34px; border-radius:50%; display:grid; place-items:center; font-family:"Brico"; font-weight:800; font-size:21px; color:#fff; background:#F59E0B; }}
.wr.r .ic {{ background:#E5484D; }}
.wr b {{ display:block; font-size:17px; line-height:1.2; font-weight:700; white-space:nowrap; }}
.wr span {{ display:block; font-size:14.5px; color:#5E5182; font-weight:500; white-space:nowrap; }}

.chips {{ display:flex; flex-wrap:wrap; gap:14px; }}
.chk {{ display:inline-flex; align-items:center; gap:11px; border-radius:999px; font-weight:600; white-space:nowrap;
  background:rgba(255,255,255,.09); border:2px solid rgba(255,255,255,.24); }}
.chk svg {{ width:24px; height:24px; flex:none; }}
.chk.hot {{ background:rgba(255,229,102,.15); border-color:rgba(255,229,102,.62); }}
.cta {{ border-radius:34px; background:linear-gradient(95deg,#FFE566 0%,#FFB648 58%,#FF8FAE 100%); color:#1C0B42; display:flex; align-items:center; justify-content:space-between; box-shadow:0 20px 50px rgba(255,170,90,.28); }}
.cta .t {{ font-family:"Brico"; font-weight:800; font-stretch:75%; line-height:1; }}
.cta .s {{ font-weight:600; }}
.cta .go {{ border-radius:50%; background:#1C0B42; display:grid; place-items:center; flex:none; }}
"""

CHECK = lambda col: f'<svg viewBox="0 0 24 24" fill="none" stroke="{col}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="#FFE566" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v15M5.5 12.5 12 19l6.5-6.5"/></svg>'
SPARK = '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M12 1.5c.6 5.3 3.2 7.9 8.5 8.5-5.3.6-7.9 3.2-8.5 8.5-.6-5.3-3.2-7.9-8.5-8.5 5.3-.6 7.9-3.2 8.5-8.5z" fill="#FFE566"/></svg>'

def underline(w):
    return (f'<svg viewBox="0 0 {w} 40" width="{w}" height="40" aria-hidden="true"><defs><linearGradient id="ug" x1="0" x2="1">'
            f'<stop offset="0" stop-color="#FFE566"/><stop offset="1" stop-color="#FF86A6"/></linearGradient></defs>'
            f'<path d="M6,24 C{w*.25:.0f},12 {w*.6:.0f},8 {w-8},16" fill="none" stroke="url(#ug)" stroke-width="9" stroke-linecap="round"/>'
            f'<path d="M{w*.12:.0f},33 C{w*.4:.0f},25 {w*.7:.0f},23 {w*.9:.0f},27" fill="none" stroke="url(#ug)" stroke-width="5" stroke-linecap="round" opacity=".8"/></svg>')

def sun(s):
    import math
    rays = ""
    for i in range(12):
        a = math.radians(i * 30 + 8)
        r1, r2 = 33, (47 if i % 2 == 0 else 42)
        rays += f'<line x1="{50+r1*math.cos(a):.1f}" y1="{50+r1*math.sin(a):.1f}" x2="{50+r2*math.cos(a):.1f}" y2="{50+r2*math.sin(a):.1f}"/>'
    return (f'<svg viewBox="0 0 100 100" width="{s}" height="{s}" aria-hidden="true"><defs><linearGradient id="sg" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="#FFE566"/><stop offset="1" stop-color="#FFB648"/></linearGradient></defs>'
            f'<g stroke="#FFD84D" stroke-width="5" stroke-linecap="round">{rays}</g><circle cx="50" cy="50" r="24" fill="url(#sg)"/></svg>')

MONTHS = [(6, "HAZİRAN"), (7, "TEMMUZ"), (8, "AĞUSTOS"), (9, "EYLÜL")]
TOPLU = (8, 2, 8, 13)   # yaz kapanışı (toplu plan)

def bars(items):
    h = ""
    for kind, m1, d1, m2, d2 in items:
        l, w = span(m1, d1, m2, d2)
        h += f'<div class="bar {kind}" style="left:{l+1}px;width:{w-2}px"></div>'
    l, w = span(*TOPLU)
    return h + f'<div class="bar y" style="left:{l+1}px;width:{w-2}px"></div>'

def dens(items):
    h = ""
    for m, d, n, cls in items:
        assert dt.date(YEAR, m, d).weekday() == 0
        h += f'<div class="dn {cls}" style="left:{x(m,d)}px;width:{5*PX}px">{n}</div>'
    l, w = span(*TOPLU)
    return h + f'<div class="dn top" style="left:{l}px;width:{w}px">TOPLU</div>'

def person(name, badge, bcls, items):
    return (f'<div class="gr pr"><div class="gl"><b>{name}</b><span class="bd {bcls}">{badge}</span></div>'
            f'<div class="tl">{bars(items)}</div></div>')

def dept(name, info, items):
    return (f'<div class="gr dep"><div class="gl"><b>{name}</b><span>{info}</span></div>'
            f'<div class="tl">{dens(items)}</div></div>')

def gantt(n_konf=2):
    mh = "".join(f'<b style="left:{x(m,1)}px">{t}</b>' for m, t in MONTHS)
    dh, d = "", T0
    while d <= T1:
        if d.weekday() == 0:
            dh += f'<i style="left:{(d-T0).days*PX}px">{d.day}</i>'
        d += dt.timedelta(days=1)
    dokuma = [
        person("Ayşe K.", "plansız 4", "", [("o", 7, 5, 7, 16)]),
        person("Mehmet D.", "plansız −2", "neg", [("o", 7, 12, 7, 23), ("t", 9, 6, 9, 17)]),
        person("Fatma Ş.", "plansız 0", "ok", [("t", 7, 12, 7, 30)]),
        person("Hasan Ç.", "plansız 6", "", [("k", 6, 14, 6, 25), ("t", 9, 13, 9, 17)]),
    ]
    konf = [
        person("Zeynep A.", "plansız 2", "", [("k", 6, 7, 6, 18), ("o", 7, 5, 7, 9)]),
        person("Emre T.", "plansız 8", "", [("t", 6, 28, 7, 2), ("t", 7, 19, 7, 23)]),
        person("Elif Y.", "plansız 5", "", [("o", 6, 28, 7, 9)]),
    ][:n_konf]
    d1 = dept("DOKUMA", "42 kişi · sınır 4", [
        (6, 7, 1, "c1"), (6, 14, 2, "c2"), (6, 21, 2, "c2"), (6, 28, 2, "c2"), (7, 5, 3, "c3"),
        (7, 12, 5, "over"), (7, 19, 4, "c4"), (7, 26, 3, "c3"), (8, 16, 2, "c2"), (8, 23, 2, "c2"),
        (9, 6, 2, "c2"), (9, 13, 3, "c3")])
    d2 = dept("KONFEKSİYON", "30 kişi · sınır 3", [
        (6, 7, 2, "c2"), (6, 14, 2, "c2"), (6, 28, 2, "c2"), (7, 5, 2, "c2"), (7, 19, 3, "c4"), (7, 26, 2, "c2"),
        (8, 16, 2, "c2"), (8, 23, 1, "c1"), (9, 20, 1, "c1")])
    lg = ('<div class="lg"><span><i class="bar t"></i>Taslak</span><span><i class="bar o"></i>Onaylı</span>'
          '<span><i class="bar k"></i>İzne çevrildi</span><span><i class="bar y"></i>Toplu plan</span>'
          '<span><i style="background:#E5484D"></i>Sınır aşıldı</span></div>')
    return f'''<div class="gp" style="width:{L+W+12}px">
<div class="gbar"><div class="t">Yıllık İzin Planlama<span>2027 · Haz–Eyl</span></div>
<div class="gbtn"><span>Toplu plan</span><span>Onayla</span><span class="p">İzne çevir</span><span>Çizelge</span></div></div>
<div class="gr mh"><div class="gl">PERSONEL</div><div class="tl">{mh}</div></div>
<div class="gr dh"><div class="gl"></div><div class="tl">{dh}</div></div>
{d1}{"".join(dokuma)}{d2}{"".join(konf)}{lg}</div>'''

def warn(w):
    rows = [("r", "Dokuma · 12–16 Tem", "Bölüm sınırı aşıldı: 5 / 4 kişi"),
            ("", "Mehmet D.", "Hakkından 2 gün fazla plan"),
            ("", "Emre T.", "10 gün kuralı · İş K. md. 56")]
    r = "".join(f'<div class="wr {c}"><span class="ic">!</span><div><b>{a}</b><span>{b}</span></div></div>' for c, a, b in rows)
    return f'<div class="wn" style="width:{w}px"><div class="wn-h"><b>UYARILAR</b><span>3</span></div>{r}</div>'

def card(story):
    H = 1920 if story else 1350
    top = 190 if story else 64
    hs = 136 if story else 118
    b = f'<div class="abs" style="right:64px;top:{top-6}px"><img src="file://{D}/logo_white.png" style="width:{150 if story else 136}px"></div>'
    b += f'<div class="abs pill" style="left:64px;top:{top+10}px;padding:10px 20px;font-size:{20 if story else 18}px">{SPARK}YENİ MODÜL · YILLIK İZİN PLANLAMA</div>'
    ty = top + (96 if story else 84)
    b += f'<div class="abs hd" style="left:60px;top:{ty}px;font-size:{hs}px"><div>2027 izin planınız</div><div class="grad" style="display:inline-block">hazır mı?</div></div>'
    b += f'<div class="abs" style="left:70px;top:{ty + int(hs*1.82)}px">{underline(430 if story else 380)}</div>'
    if not story:
        b += f'<div class="abs" style="left:500px;top:{ty+118}px;transform:rotate(12deg)">{sun(112)}</div>'
        b += f'<div class="abs sub" style="left:640px;top:{ty+140}px;width:400px;font-size:22px;white-space:nowrap">Kim ne zaman izinde, hangi bölümde<br>kaç kişi eksik?<br><b>Yıl başlamadan görün.</b></div>'
        b += f'<div class="abs" style="left:38px;top:452px;transform:rotate(-2.2deg);transform-origin:left top">{gantt(2)}</div>'
        b += f'<div class="abs" style="left:660px;top:818px;transform:rotate(3deg)">{warn(372)}</div>'
        b += '<div class="abs" style="left:86px;top:984px;font-family:Kaushan;font-size:46px;color:#FFE566;transform:rotate(-5deg);white-space:nowrap">yaz şimdiden belli!</div>'
        chips = [("Bölüm sınırı uyarısı", 1), ("Toplu yaz / bayram planı", 1), ("Tek tıkla izne çevir", 0)]
        c = "".join(f'<span class="chk{" hot" if h else ""}" style="padding:12px 20px;font-size:22px">{CHECK("#FFE566")}{t}</span>' for t, h in chips)
        b += f'<div class="abs chips" style="left:56px;right:56px;top:1106px;justify-content:space-between">{c}</div>'
        b += f'''<div class="abs cta" style="left:56px;right:56px;top:1210px;height:100px;padding:0 18px 0 34px">
<div><div class="t" style="font-size:50px">Ücretsiz demo</div><div class="s" style="font-size:19px;margin-top:4px">Kendi verinizle canlı gösterim · 0 541 796 58 10</div></div>
<div class="go" style="width:68px;height:68px">{ARROW}</div></div>'''
    else:
        b += f'<div class="abs" style="left:560px;top:{ty+134}px;transform:rotate(12deg)">{sun(128)}</div>'
        b += f'<div class="abs sub" style="left:716px;top:{ty+136}px;width:330px;font-size:24px;white-space:nowrap">Kim ne zaman izinde,<br>hangi bölümde<br>kaç kişi eksik?<br><b>Yıl başlamadan görün.</b></div>'
        b += f'<div class="abs" style="left:38px;top:664px;transform:rotate(-2.2deg);transform-origin:left top">{gantt(3)}</div>'
        b += f'<div class="abs" style="left:640px;top:1066px;transform:rotate(3deg)">{warn(392)}</div>'
        b += '<div class="abs" style="left:86px;top:1228px;font-family:Kaushan;font-size:52px;color:#FFE566;transform:rotate(-5deg);white-space:nowrap">yaz şimdiden belli!</div>'
        chips = [("Bölüm sınırı uyarısı", 1), ("Toplu yaz / bayram planı", 1), ("Tek tıkla izne çevir", 0), ("İzin kurulu çizelgesi (Excel)", 0)]
        c = "".join(f'<span class="chk{" hot" if h else ""}" style="padding:13px 22px;font-size:24px">{CHECK("#FFE566")}{t}</span>' for t, h in chips)
        b += f'<div class="abs chips" style="left:56px;right:40px;top:1354px">{c}</div>'
        b += f'''<div class="abs cta" style="left:56px;right:56px;top:1524px;height:110px;padding:0 20px 0 38px">
<div><div class="t" style="font-size:54px">Ücretsiz demo</div><div class="s" style="font-size:21px;margin-top:4px">Kendi verinizle canlı gösterim · 0 541 796 58 10</div></div>
<div class="go" style="width:74px;height:74px">{ARROW}</div></div>'''
    return f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="cv" style="height:{H}px">{b}</div></body></html>'

JOBS = [("C_izin_post", card(False), 1350), ("C_izin_story", card(True), 1920)]
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(device_scale_factor=1)
    for name, h, H in JOBS:
        path = os.path.join(D, name + ".html"); open(path, "w", encoding="utf-8").write(h)
        pg.set_viewport_size({"width": 1080, "height": H}); pg.goto("file://" + path)
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        info = pg.evaluate("""(()=>{const r=e=>{const b=e.getBoundingClientRect();return [Math.round(b.left),Math.round(b.top),Math.round(b.right),Math.round(b.bottom)]};
          return {hd:[...document.querySelectorAll('.hd > div')].map(r), chips:[...document.querySelectorAll('.chk')].map(r), cta:r(document.querySelector('.cta')), gp:r(document.querySelector('.gp')), wn:r(document.querySelector('.wn')), sub:r(document.querySelector('.sub'))}})()""")
        pg.screenshot(path=os.path.join(OUT, name + ".png"), clip={"x": 0, "y": 0, "width": 1080, "height": H})
        print(name, info)
    br.close()
