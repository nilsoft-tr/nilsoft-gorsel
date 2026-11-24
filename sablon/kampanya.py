# -*- coding: utf-8 -*-
"""nilSOFT kampanya kartları v3 — her kart ayrı renk dünyası ve yerleşim.
A) Servis Planlama: zümrüt gece, haritalı 3B kolaj, telefon, yüzen etiketler
B) SGK Raporları: krem zemin, bordo-mercan, e-Vizite -> PDKS akış kolajı, el yazısı vurgu
"""
import os, sys
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, "out"); os.makedirs(OUT, exist_ok=True)
F = "/tmp/fonts2"

BASE = f"""
@font-face {{ font-family:"Brico"; src:url("file://{F}/Bricolage.ttf"); font-weight:200 800; font-stretch:75% 100%; }}
@font-face {{ font-family:"Plex"; src:url("file://{F}/PlexSans.ttf"); font-weight:100 700; font-stretch:85% 100%; }}
@font-face {{ font-family:"PlexMono"; src:url("file://{F}/PlexMono-SemiBold.ttf"); font-weight:600; }}
@font-face {{ font-family:"Kaushan"; src:url("file://{F}/KaushanScript.ttf"); }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
html,body {{ background:#000; }}
.cv {{ position:relative; overflow:hidden; width:1080px; font-family:"Plex",sans-serif; }}
.abs {{ position:absolute; }}
.hd {{ font-family:"Brico"; font-weight:800; font-stretch:75%; letter-spacing:-0.01em; line-height:.9; }}
.grad {{ -webkit-background-clip:text; background-clip:text; color:transparent; }}
.pill {{ display:inline-flex; align-items:center; gap:12px; border-radius:999px; font-weight:600; letter-spacing:.12em; }}
.chk {{ display:inline-flex; align-items:center; gap:12px; border-radius:999px; font-weight:600; white-space:nowrap; }}
.chk svg {{ width:24px; height:24px; flex:none; }}
.mono {{ font-family:"PlexMono"; font-weight:600; }}
"""

CHECK = lambda col: f'<svg viewBox="0 0 24 24" fill="none" stroke="{col}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
ARROW_DOWN = lambda col: f'<svg viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="{col}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v15M5.5 12.5 12 19l6.5-6.5"/></svg>'
SPARK = lambda col, s=28: f'<svg viewBox="0 0 24 24" width="{s}" height="{s}" aria-hidden="true"><path d="M12 1.5c.6 5.3 3.2 7.9 8.5 8.5-5.3.6-7.9 3.2-8.5 8.5-.6-5.3-3.2-7.9-8.5-8.5 5.3-.6 7.9-3.2 8.5-8.5z" fill="{col}"/></svg>'

def html(css, body, w, h):
    return f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><style>{BASE}{css}</style></head><body><div class="cv" style="height:{h}px">{body}</div></body></html>'

def underline(w, c1, c2, sw=9):
    return (f'<svg viewBox="0 0 {w} 40" width="{w}" height="40" aria-hidden="true"><defs><linearGradient id="ug" x1="0" x2="1">'
            f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>'
            f'<path d="M6,24 C{w*.25:.0f},12 {w*.6:.0f},8 {w-8},16" fill="none" stroke="url(#ug)" stroke-width="{sw}" stroke-linecap="round"/>'
            f'<path d="M{w*.12:.0f},33 C{w*.4:.0f},25 {w*.7:.0f},23 {w*.9:.0f},27" fill="none" stroke="url(#ug)" stroke-width="{sw*.55:.1f}" stroke-linecap="round" opacity=".8"/></svg>')

# =====================================================================
# A) SERVİS PLANLAMA — zümrüt gece
# =====================================================================
A_CSS = """
.zA { background:
   radial-gradient(900px 600px at 85% 8%, rgba(124,242,176,.20), transparent 60%),
   radial-gradient(700px 700px at 0% 100%, rgba(255,209,102,.12), transparent 60%),
   radial-gradient(rgba(255,255,255,.10) 1.3px, transparent 1.6px) 0 0/24px 24px,
   linear-gradient(165deg,#0E4A3B 0%,#0A3A2F 45%,#062720 100%); color:#fff; }
.zA .gA { background-image:linear-gradient(90deg,#8CF5C0 0%,#FFE08A 70%,#FFC857 100%); }
.mapc { border-radius:22px; overflow:hidden; background:#F4F7F3; box-shadow: 0 50px 90px rgba(0,0,0,.5), 0 0 0 1px rgba(255,255,255,.18), 0 0 120px rgba(124,242,176,.18); }
.mapbar { display:flex; justify-content:space-between; align-items:center; padding:16px 22px; background:#fff; border-bottom:1px solid #DDE5DF; color:#13271F; }
.mapbar b { font-size:20px; } .mapbar span { color:#5B6B63; font-size:17px; }
.mbtn { background:#0F8A5F; color:#fff; font-weight:600; font-size:16px; padding:7px 14px; border-radius:8px; }
.phone { border-radius:46px; background:#04120E; padding:12px; box-shadow:0 40px 80px rgba(0,0,0,.55), 0 0 0 2px rgba(255,255,255,.12) inset; }
.scr { border-radius:36px; background:#F4F7F3; overflow:hidden; height:100%; color:#13271F; position:relative; }
.notch { position:absolute; top:10px; left:50%; transform:translateX(-50%); width:96px; height:26px; border-radius:14px; background:#04120E; }
.ph { background:#0F8A5F; color:#fff; padding:52px 22px 18px; }
.ph small { font-size:14px; opacity:.85; letter-spacing:.08em; font-weight:600; }
.ph b { display:block; font-size:24px; margin-top:4px; font-family:"Brico"; font-weight:800; }
.ph span { font-size:15px; opacity:.9; }
.stop { display:flex; align-items:center; gap:14px; padding:13px 20px; border-bottom:1px solid #E1E8E3; font-size:17px; }
.stop i { flex:none; width:30px; height:30px; border-radius:50%; border:3px solid #0F8A5F; color:#0F8A5F; font-style:normal; font-family:"PlexMono"; font-weight:600; font-size:14px; display:grid; place-items:center; background:#fff; }
.stop b { font-weight:600; } .stop em { margin-left:auto; font-style:normal; color:#5B6B63; font-size:15px; }
.stop.f i { background:#FFC857; border-color:#FFC857; color:#2A1F00; }
.tag { background:#fff; color:#0D2A20; border-radius:16px; padding:14px 18px; display:flex; align-items:center; gap:12px; box-shadow:0 20px 40px rgba(0,0,0,.35); font-weight:600; }
.tag .ic { width:38px; height:38px; border-radius:50%; display:grid; place-items:center; flex:none; }
.ctaA { border-radius:34px; background:linear-gradient(95deg,#8CF5C0 0%,#FFE08A 60%,#FFC857 100%); color:#062720; display:flex; align-items:center; justify-content:space-between; box-shadow:0 20px 50px rgba(255,200,87,.25); }
.ctaA .t { font-family:"Brico"; font-weight:800; font-stretch:75%; line-height:1; }
.ctaA .s { font-weight:600; }
.ctaA .go { border-radius:50%; background:#062720; display:grid; place-items:center; flex:none; }
.chkA { background:rgba(255,255,255,.08); border:2px solid rgba(255,255,255,.22); color:#fff; }
"""

def a_map(w, h):
    roads = ["M-20,90 C200,70 420,120 {W},100", "M-20,250 C230,230 470,270 {W},250", "M-20,400 C230,380 470,425 {W},405",
             "M120,-20 C135,140 100,300 140,{H}", "M360,-20 C345,160 380,320 365,{H}", "M610,-20 C595,150 630,300 615,{H}"]
    roads = [r.replace("{W}", str(w + 20)).replace("{H}", str(h + 20)) for r in roads]
    parks = '<ellipse cx="250" cy="170" rx="70" ry="42" fill="#DCEFD9"/><ellipse cx="520" cy="330" rx="80" ry="40" fill="#DCEFD9"/>'
    rd = "".join(f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="20" stroke-linecap="round"/>' for d in roads)
    rd += "".join(f'<path d="{d}" fill="none" stroke="#D3DCD5" stroke-width="1.5"/>' for d in roads)
    st = [(125, 96), (128, 244), (240, 252), (362, 258), (366, 398), (488, 404)]
    path = "M" + " L".join(f"{x},{y}" for x, y in st) + " L560,404"
    pins = "".join(f'<circle cx="{x}" cy="{y}" r="17" fill="#fff" stroke="#0F8A5F" stroke-width="5"/>'
                   f'<text x="{x}" y="{y+1}" text-anchor="middle" dominant-baseline="central" font-family="PlexMono" font-weight="600" font-size="16" fill="#0F8A5F">{i+1}</text>'
                   for i, (x, y) in enumerate(st))
    fab = ('<g transform="translate(560,404)"><rect x="0" y="-22" width="118" height="44" rx="10" fill="#FFC857"/>'
           '<text x="59" y="1" text-anchor="middle" dominant-baseline="central" font-family="Plex" font-weight="700" font-size="16" fill="#2A1F00" letter-spacing="1.5">FABRİKA</text></g>')
    bus = ('<g transform="translate(125,96)"><circle r="30" fill="#0F8A5F" opacity=".18"/></g>')
    return (f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true"><rect width="{w}" height="{h}" fill="#EEF3EE"/>{parks}{rd}{bus}'
            f'<path d="{path}" fill="none" stroke="#fff" stroke-width="14" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="{path}" fill="none" stroke="#0F8A5F" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>{pins}{fab}</svg>')

def a_phone():
    rows = [("1", "Sırakapılar", "3 kişi"), ("2", "Bağbaşı", "2 kişi"), ("3", "Gerzele", "3 kişi"),
            ("4", "Kınıklı", "2 kişi"), ("5", "Çamlaraltı", "2 kişi")]
    r = "".join(f'<div class="stop"><i>{n}</i><b>{a}</b><em>{b}</em></div>' for n, a, b in rows)
    r += '<div class="stop f"><i>F</i><b>Fabrika</b><em>12 kişi</em></div>'
    r += '<div style="margin:18px 20px 0;border:2px solid #0F8A5F;color:#0F8A5F;border-radius:12px;padding:12px;text-align:center;font-weight:700;font-size:16px">Şoför listesini yazdır</div>'
    return f'''<div class="phone" style="width:330px;height:660px"><div class="scr"><div class="notch"></div>
<div class="ph"><small>SERVİS 1 · DOKUMA</small><b>Sabah servisi</b><span>6 durak · 12 personel</span></div>{r}</div></div>'''

def a_map_card(w, h):
    return f'''<div class="mapc" style="width:{w}px">
<div class="mapbar"><div><b>Servis Planlama</b> <span>· Sabah vardiyası</span></div></div>
{a_map(w, h)}</div>'''

def card_A(story):
    W, H = 1080, (1920 if story else 1350)
    top = 190 if story else 64
    hs = 136 if story else 118
    b = f'<div class="abs" style="right:64px;top:{top-6}px"><img src="file://{D}/logo_white.png" style="width:{150 if story else 136}px"></div>'
    b += f'<div class="abs pill" style="left:64px;top:{top+10}px;padding:10px 20px;background:rgba(140,245,192,.14);border:2px solid rgba(140,245,192,.5);color:#BFFADD;font-size:{20 if story else 18}px">{SPARK("#FFE08A",22)}YENİ MODÜL · SERVİS PLANLAMA</div>'
    ty = top + (96 if story else 84)
    b += f'''<div class="abs hd" style="left:60px;top:{ty}px;font-size:{hs}px">
<div>Personel servisi</div><div class="gA grad" style="padding-bottom:.06em">artık haritada.</div></div>'''
    b += f'<div class="abs" style="left:70px;top:{ty + int(hs*1.82)}px">{underline(560 if story else 500, "#8CF5C0", "#FFC857")}</div>'
    if not story:
        b += f'<div class="abs" style="left:300px;top:404px;transform:perspective(1600px) rotateY(-14deg) rotateX(5deg);transform-origin:left center">{a_map_card(690, 470)}</div>'
        b += f'<div class="abs" style="left:56px;top:470px;transform:rotate(-4deg)">{a_phone()}</div>'
        b += f'''<div class="abs tag" style="right:52px;top:430px;font-size:19px"><span class="ic" style="background:#E3F7EC">{CHECK("#0F8A5F")}</span><span>Şoför listesi hazır</span></div>'''
        b += '<div class="abs" style="left:610px;top:1000px;font-family:Kaushan;font-size:46px;color:#FFE08A;transform:rotate(-5deg)">rota hazır!</div>'
        chips = [("Personel ataması", 268), ("Durak sırası", 210), ("Haritada güzergâh", 290)]
        cx, cy = 64, 1146
        out = ""
        for t, w in chips:
            out += f'<div class="abs chk chkA" style="left:{cx}px;top:{cy}px;padding:12px 20px;font-size:22px">{CHECK("#8CF5C0")}{t}</div>'
            cx += w + 16
        b += out
        b += f'''<div class="abs ctaA" style="left:56px;right:56px;top:1226px;height:96px;padding:0 18px 0 34px">
<div><div class="t" style="font-size:48px">Ücretsiz demo</div><div class="s" style="font-size:19px;margin-top:4px">Kendi verinizle canlı gösterim · 0 541 796 58 10</div></div>
<div class="go" style="width:66px;height:66px">{ARROW_DOWN("#8CF5C0")}</div></div>'''
    else:
        b += f'<div class="abs" style="left:250px;top:640px;transform:perspective(1600px) rotateY(-14deg) rotateX(5deg);transform-origin:left center">{a_map_card(760, 520)}</div>'
        b += f'<div class="abs" style="left:52px;top:720px;transform:rotate(-4deg) scale(1.06);transform-origin:top left">{a_phone()}</div>'
        b += f'''<div class="abs tag" style="right:56px;top:600px;font-size:21px"><span class="ic" style="background:#E3F7EC">{CHECK("#0F8A5F")}</span><span>Şoför listesi hazır</span></div>'''
        b += '<div class="abs" style="left:520px;top:1300px;font-family:Kaushan;font-size:54px;color:#FFE08A;transform:rotate(-5deg)">rota hazır!</div>'
        rows = [[("Personel ataması", 290), ("Durak sırası", 228)], [("Haritada güzergâh", 314), ("Şoför listesi", 236)]]
        y = 1420
        for row in rows:
            x = 64
            for t, w in row:
                b += f'<div class="abs chk chkA" style="left:{x}px;top:{y}px;padding:13px 22px;font-size:24px">{CHECK("#8CF5C0")}{t}</div>'
                x += w + 18
            y += 74
        b += f'''<div class="abs ctaA" style="left:56px;right:56px;top:1576px;height:110px;padding:0 20px 0 38px">
<div><div class="t" style="font-size:54px">Ücretsiz demo</div><div class="s" style="font-size:21px;margin-top:4px">Kendi verinizle canlı gösterim · 0 541 796 58 10</div></div>
<div class="go" style="width:74px;height:74px">{ARROW_DOWN("#8CF5C0")}</div></div>'''
    return html(A_CSS, f'<div class="zA" style="position:absolute;inset:0">{b}</div>', W, H)

# =====================================================================
# B) SGK RAPORLARI — krem + bordo/mercan
# =====================================================================
B_CSS = """
.kB { background:
   radial-gradient(800px 500px at 100% 0%, rgba(242,107,91,.16), transparent 60%),
   radial-gradient(700px 600px at 0% 100%, rgba(142,31,58,.10), transparent 60%),
   radial-gradient(rgba(90,30,40,.13) 1.3px, transparent 1.6px) 0 0/24px 24px,
   linear-gradient(180deg,#FBF6EF 0%,#F4EADF 100%); color:#2A1220; }
.kB .gB { background-image:linear-gradient(90deg,#8E1F3A 0%,#D2384A 55%,#F26B5B 100%); }
.cardx { background:#fff; border-radius:20px; box-shadow:0 30px 60px rgba(70,20,30,.18), 0 0 0 1px rgba(70,20,30,.07); overflow:hidden; color:#2A1220; }
.cx-h { display:flex; align-items:center; justify-content:space-between; padding:16px 20px; border-bottom:1px solid #EFE3DA; }
.cx-h b { font-size:19px; } .cx-h span { font-size:14px; color:#7A6470; letter-spacing:.06em; font-weight:600; }
.vz .row { display:grid; grid-template-columns:1fr auto; gap:6px 12px; padding:13px 20px; border-bottom:1px solid #F3EAE3; }
.vz .row .n { font-weight:600; font-size:17px; } .vz .row .tc { font-family:"PlexMono"; font-size:14px; color:#8A7480; }
.vz .row .v { justify-self:end; font-size:13px; font-weight:600; padding:3px 9px; border-radius:6px; background:#F3ECE7; color:#6B5560; }
.vz .row .d { justify-self:end; font-family:"PlexMono"; font-size:14px; color:#4A3440; }
.vz .row.sel { background:#FFF4EE; box-shadow: inset 4px 0 0 #F26B5B; }
.iz .fld { padding:12px 22px; border-bottom:1px solid #F3EAE3; }
.iz .fld small { display:block; font-size:13px; letter-spacing:.08em; font-weight:600; color:#8A7480; }
.iz .fld b { font-size:20px; font-weight:600; } .iz .fld .mono { font-size:19px; }
.iz .ok { display:flex; align-items:center; gap:10px; padding:16px 22px; background:#EAF6EF; color:#1E7A50; font-weight:700; font-size:18px; }
.iz .ok svg { width:24px; height:24px; }
.badgeB { display:inline-block; background:#8E1F3A; color:#fff; font-size:14px; font-weight:700; letter-spacing:.1em; padding:4px 10px; border-radius:6px; }
.sticker { border-radius:50%; background:#F26B5B; color:#fff; display:grid; place-items:center; text-align:center; font-family:"Brico"; font-weight:800; font-stretch:75%; line-height:.95; box-shadow:0 18px 36px rgba(242,107,91,.4); border:5px dashed rgba(255,255,255,.55); }
.chkB { background:#fff; border:2px solid #EAD9CF; color:#2A1220; box-shadow:0 6px 14px rgba(70,20,30,.06); }
.ctaB { border-radius:34px; background:linear-gradient(100deg,#7A1730 0%,#A8263F 60%,#C93246 100%); color:#fff; display:flex; align-items:center; justify-content:space-between; box-shadow:0 22px 50px rgba(142,31,58,.35); }
.ctaB .t { font-family:"Brico"; font-weight:800; font-stretch:75%; line-height:1; }
.ctaB .s { font-weight:500; opacity:.95; }
.ctaB .go { border-radius:50%; background:#fff; display:grid; place-items:center; flex:none; }
"""

def b_vizite(w):
    rows = [("Ayşe Kaya", "1234*****78", "Hastalık", "03.11–05.11", False),
            ("Fatma Şahin", "2871*****14", "Hastalık", "18.11–19.11", True),
            ("Hasan Çelik", "5560*****02", "İş kazası", "20.11–22.11", False)]
    r = "".join(f'<div class="row{" sel" if s else ""}"><div class="n">{n}</div><div class="v">{v}</div>'
                f'<div class="tc">TC {tc}</div><div class="d">{d}</div></div>' for n, tc, v, d, s in rows)
    return f'''<div class="cardx vz" style="width:{w}px"><div class="cx-h"><b>SGK e-Vizite</b><span>RAPOR LİSTESİ</span></div>{r}</div>'''

def b_izin(w):
    return f'''<div class="cardx iz" style="width:{w}px"><div class="cx-h"><b>nilSOFT PDKS · İzin girişi</b><span class="badgeB">SGK</span></div>
<div class="fld"><small>PERSONEL</small><b>Fatma Şahin</b> <span style="color:#8A7480;font-size:16px">· Dokuma</span></div>
<div class="fld"><small>İZİN TÜRÜ</small><b>Raporlu (hastalık)</b></div>
<div class="fld"><small>TARİH</small><span class="mono">18.11.2026 – 19.11.2026</span></div>
<div class="ok">{CHECK("#1E7A50")}Kaydedildi · puantaja işlendi</div></div>'''

def flow_arrow(w, h, vertical=False):
    if vertical:
        d = f"M{w*.35:.0f},6 C{w*.15:.0f},{h*.45:.0f} {w*.75:.0f},{h*.55:.0f} {w*.6:.0f},{h-14}"
        hx, hy = w*.6, h-14
        head = f'<path d="M{hx-16:.0f},{hy-20:.0f} L{hx:.0f},{hy:.0f} L{hx+18:.0f},{hy-16:.0f}" fill="none" stroke="#8E1F3A" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
    else:
        d = f"M8,{h*.25:.0f} C{w*.4:.0f},{h*.05:.0f} {w*.65:.0f},{h*.9:.0f} {w-14},{h*.7:.0f}"
        hx, hy = w-14, h*.7
        head = f'<path d="M{hx-22:.0f},{hy-14:.0f} L{hx:.0f},{hy:.0f} L{hx-14:.0f},{hy+20:.0f}" fill="none" stroke="#8E1F3A" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true"><path d="{d}" fill="none" stroke="#8E1F3A" stroke-width="5" stroke-dasharray="2 12" stroke-linecap="round"/>{head}</svg>'

def card_B(story):
    W, H = 1080, (1920 if story else 1350)
    top = 190 if story else 64
    hs = 128 if story else 112
    b = f'<div class="abs" style="right:64px;top:{top-6}px"><img src="file://{D}/logo_navy.png" style="width:{150 if story else 136}px"></div>'
    b += f'<div class="abs pill" style="left:64px;top:{top+10}px;padding:10px 20px;background:#8E1F3A;color:#fff;font-size:{20 if story else 18}px">{SPARK("#FFD3C4",22)}YENİ MODÜL · SGK RAPORLARI</div>'
    ty = top + (96 if story else 84)
    b += f'''<div class="abs hd" style="left:60px;top:{ty}px;font-size:{hs}px">
<div>SGK raporları</div><div class="gB grad" style="padding-bottom:.06em">tek tıkla</div><div>izne aktarılsın.</div></div>'''
    sy = ty + int(hs * 2.72)
    b += f'<div class="abs" style="left:{440 if story else 410}px;top:{ty + int(hs*(1.05 if story else 1.08))}px;font-family:Kaushan;font-size:{54 if story else 46}px;color:#D2384A;transform:rotate(-6deg);white-space:nowrap">e-Vizite\'ye girmeden!</div>'
    if not story:
        b += f'<div class="abs" style="left:40px;top:530px;transform:rotate(-3deg)">{b_vizite(450)}</div>'
        b += f'<div class="abs" style="left:474px;top:640px">{flow_arrow(120, 110)}</div>'
        b += f'<div class="abs" style="right:40px;top:612px;transform:rotate(2.5deg)">{b_izin(450)}</div>'
        b += '<div class="abs sticker" style="left:330px;top:862px;width:150px;height:150px;font-size:38px;transform:rotate(-12deg)">TEK<br>TIK</div>'
        chips = [("TC ile eşleşme", 250), ("Mükerrer aktarım yok", 322), ("Vakaya göre izin", 268)]
        x = 64
        for t, w in chips:
            b += f'<div class="abs chk chkB" style="left:{x}px;top:1066px;padding:12px 20px;font-size:21px">{CHECK("#D2384A")}{t}</div>'
            x += w + 14
        b += f'''<div class="abs ctaB" style="left:56px;right:56px;top:1170px;height:100px;padding:0 18px 0 34px">
<div><div class="t" style="font-size:50px">Ücretsiz demo</div><div class="s" style="font-size:19px;margin-top:4px">Kendi verinizle canlı gösterim · 0 541 796 58 10</div></div>
<div class="go" style="width:68px;height:68px">{ARROW_DOWN("#8E1F3A")}</div></div>'''
    else:
        b += f'<div class="abs" style="left:60px;top:720px;transform:rotate(-3deg)">{b_vizite(600)}</div>'
        b += f'<div class="abs" style="left:300px;top:1010px">{flow_arrow(260, 150, vertical=True)}</div>'
        b += f'<div class="abs" style="right:60px;top:1110px;transform:rotate(2.5deg)">{b_izin(600)}</div>'
        b += '<div class="abs sticker" style="left:70px;top:1150px;width:170px;height:170px;font-size:44px;transform:rotate(-12deg)">TEK<br>TIK</div>'
        rows = [[("TC ile eşleşme", 266), ("Mükerrer aktarım yok", 342)], [("Vakaya göre izin türü", 342)]]
        y = 1458
        for row in rows:
            x = 64
            for t, w in row:
                b += f'<div class="abs chk chkB" style="left:{x}px;top:{y}px;padding:12px 20px;font-size:23px">{CHECK("#D2384A")}{t}</div>'
                x += w + 16
            y += 0 if False else 0
            break
        x = 64 + 266 + 16 + 342 + 16
        b += f'<div class="abs chk chkB" style="left:64px;top:1530px;padding:12px 20px;font-size:23px">{CHECK("#D2384A")}Vakaya göre izin türü</div>'
        b += f'''<div class="abs ctaB" style="left:56px;right:56px;top:1610px;height:108px;padding:0 20px 0 38px">
<div><div class="t" style="font-size:54px">Ücretsiz demo</div><div class="s" style="font-size:21px;margin-top:4px">Kendi verinizle canlı gösterim · 0 541 796 58 10</div></div>
<div class="go" style="width:74px;height:74px">{ARROW_DOWN("#8E1F3A")}</div></div>'''
    return html(B_CSS, f'<div class="kB" style="position:absolute;inset:0">{b}</div>', W, H)

JOBS = [("A_servis_post", card_A(False), 1350), ("A_servis_story", card_A(True), 1920),
        ("B_sgk_post", card_B(False), 1350), ("B_sgk_story", card_B(True), 1920)]

only = set(sys.argv[1:])
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(device_scale_factor=1)
    for name, h, H in JOBS:
        if only and name not in only: continue
        path = os.path.join(D, name + ".html"); open(path, "w", encoding="utf-8").write(h)
        pg.set_viewport_size({"width": 1080, "height": H}); pg.goto("file://" + path)
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(250)
        fams = pg.evaluate("[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family)")
        pg.screenshot(path=os.path.join(OUT, name + ".png"), clip={"x": 0, "y": 0, "width": 1080, "height": H})
        print(name, sorted(set(fams)))
    br.close()
