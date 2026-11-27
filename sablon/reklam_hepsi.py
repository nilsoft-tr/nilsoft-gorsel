# -*- coding: utf-8 -*-
"""Sponsorlu reklam: "Hepsi tek bir PDKS'de — nilSOFT PDKS". Üç ayrı tasarım, her biri 4:5 ve 9:16.
  V1 Aurora (koyu, renkli ışıklar) : Patron Ekranı görüntüsü + aktarım hapları + modül ızgarası
  V2 Sarı-siyah                    : yalnız tipografi, hap bulutu
  V3 Açık zemin, merkez şeması     : tüm modüller ortadaki nilSOFT PDKS'ye bağlanır
Çalıştır: python3 reklam_hepsi.py [v1 v2 v3]"""
import os, sys, math
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, "out"); os.makedirs(OUT, exist_ok=True)
F = "/tmp/fonts2"

AKTARIM = ["Luca’ya aktarım", "Link’e online aktarım", "Workcube aktarım", "Logo’ya aktarım", "Netsis’e aktarım", "Mikro’ya aktarım"]
AKT_KISA = ["Luca", "Link (online)", "Workcube", "Logo", "Netsis", "Mikro"]
MODUL = ["Patron ekranı", "Vardiya planlama", "Servis aracı planlama",
         "Yıllık izin", "Yıllık izin planlama", "SGK raporu modülü",
         "Evrak takibi", "Eğitim takibi", "Zimmet takibi",
         "Yol yardımı", "Yemekhane", "Turnover",
         "Personel mobil", "Yönetici mobil", "Dinamik QR kod"]

BASE = f"""
@font-face {{ font-family:"Brico"; src:url("file://{F}/Bricolage.ttf"); font-weight:200 800; font-stretch:75% 100%; }}
@font-face {{ font-family:"Plex"; src:url("file://{F}/PlexSans.ttf"); font-weight:100 700; font-stretch:85% 100%; }}
@font-face {{ font-family:"PlexMono"; src:url("file://{F}/PlexMono-SemiBold.ttf"); font-weight:600; }}
@font-face {{ font-family:"Kaushan"; src:url("file://{F}/KaushanScript.ttf"); }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
html,body {{ background:#000; }}
.cv {{ position:relative; overflow:hidden; width:1080px; font-family:"Plex",sans-serif; }}
.abs {{ position:absolute; }}
.hd {{ font-family:"Brico"; font-weight:800; font-stretch:75%; letter-spacing:-0.01em; line-height:.9; white-space:nowrap; }}
.br {{ font-family:"Brico"; font-weight:800; font-stretch:75%; line-height:1; white-space:nowrap; }}
.kau {{ font-family:"Kaushan"; white-space:nowrap; }}
.pill {{ display:inline-flex; align-items:center; gap:12px; border-radius:999px; font-weight:600; letter-spacing:.12em; white-space:nowrap; }}
.chk {{ display:inline-flex; align-items:center; gap:10px; border-radius:999px; font-weight:600; white-space:nowrap; }}
.chk svg {{ flex:none; }}
.cta {{ display:flex; align-items:center; justify-content:space-between; }}
.more {{ display:flex; align-items:center; justify-content:center; gap:12px; border-radius:999px; font-weight:500; white-space:nowrap; border:2px dashed; }}
.more b {{ font-weight:700; }}
.cta .t {{ font-family:"Brico"; font-weight:800; font-stretch:75%; line-height:1; }}
.cta .s {{ font-weight:600; white-space:nowrap; }}
.cta .go {{ border-radius:50%; display:grid; place-items:center; flex:none; }}
"""

def CHECK(col, s=24):
    return f'<svg viewBox="0 0 24 24" width="{s}" height="{s}" fill="none" stroke="{col}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
def ARROW(col, s=40):
    return f'<svg viewBox="0 0 24 24" width="{s}" height="{s}" fill="none" stroke="{col}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v15M5.5 12.5 12 19l6.5-6.5"/></svg>'
def SWAP(col, s=22):
    return f'<svg viewBox="0 0 24 24" width="{s}" height="{s}" fill="none" stroke="{col}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 8h14M14 4l4 4-4 4M20 16H6M10 12l-4 4 4 4"/></svg>'
def SPARK(col, s=22):
    return f'<svg viewBox="0 0 24 24" width="{s}" height="{s}" aria-hidden="true"><path d="M12 1.5c.6 5.3 3.2 7.9 8.5 8.5-5.3.6-7.9 3.2-8.5 8.5-.6-5.3-3.2-7.9-8.5-8.5 5.3-.6 7.9-3.2 8.5-8.5z" fill="{col}"/></svg>'
def underline(w, c1, c2, uid):
    return (f'<svg viewBox="0 0 {w} 40" width="{w}" height="40" aria-hidden="true"><defs><linearGradient id="{uid}" x1="0" x2="1">'
            f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>'
            f'<path d="M6,24 C{w*.25:.0f},12 {w*.6:.0f},8 {w-8},16" fill="none" stroke="url(#{uid})" stroke-width="9" stroke-linecap="round"/>'
            f'<path d="M{w*.12:.0f},33 C{w*.4:.0f},25 {w*.7:.0f},23 {w*.9:.0f},27" fill="none" stroke="url(#{uid})" stroke-width="5" stroke-linecap="round" opacity=".8"/></svg>')
MORE_TXT = "ve İK’nın işini kolaylaştıran <b>daha birçok özellik</b>"
def PLUS(col, s=26):
    return f'<svg viewBox="0 0 24 24" width="{s}" height="{s}" fill="none" stroke="{col}" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9.5"/><path d="M12 7.5v9M7.5 12h9"/></svg>'
def more(top, h, fs, col, extra=""):
    pos = f'position:absolute;left:56px;right:56px;top:{top}px;' if top is not None else ''
    return f'<div class="more" style="{pos}height:{h}px;font-size:{fs}px;{extra}">{PLUS(col)}<span>{MORE_TXT}</span></div>'
def page(css, body, H, cls=""):
    return f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><style>{BASE}{css}</style></head><body><div class="cv {cls}" style="height:{H}px">{body}</div></body></html>'
def cta(top, h, big, small, pad, btn, arrow_col, txt="Kendi verinizle canlı gösterim · 0 541 796 58 10 · Denizli"):
    return (f'<div class="abs cta" style="left:56px;right:56px;top:{top}px;height:{h}px;padding:{pad}">'
            f'<div><div class="t" style="font-size:{big}px">Ücretsiz demo</div><div class="s" style="font-size:{small}px;margin-top:4px">{txt}</div></div>'
            f'<div class="go" style="width:{btn}px;height:{btn}px">{ARROW(arrow_col)}</div></div>')

# ======================================================================= V1 — Aurora
CSS1 = """
.cv { color:#fff; background:
   radial-gradient(900px 720px at 104% -4%, rgba(255,122,61,.62), transparent 60%),
   radial-gradient(900px 860px at -8% 34%, rgba(168,64,255,.58), transparent 62%),
   radial-gradient(1000px 820px at 86% 104%, rgba(34,120,255,.55), transparent 60%),
   radial-gradient(rgba(255,255,255,.10) 1.3px, transparent 1.6px) 0 0/24px 24px,
   linear-gradient(180deg,#150B3A 0%,#0B0724 100%); }
.grad { background-image:linear-gradient(90deg,#FFC46B 0%,#FF7EB0 55%,#B79CFF 100%); -webkit-background-clip:text; background-clip:text; color:transparent; padding-bottom:.06em; display:inline-block; }
.pill { background:rgba(255,255,255,.10); border:2px solid rgba(255,255,255,.38); color:#FFE9D2; }
.rule { height:2px; background:linear-gradient(90deg,rgba(255,196,107,.9),rgba(255,126,176,0)); }
.hero { border-radius:20px; overflow:hidden; border:5px solid rgba(255,255,255,.22); background:#0B1230;
  box-shadow:0 44px 90px rgba(4,0,24,.65), 0 0 110px rgba(255,126,176,.30); }
.hero img { display:block; width:100%; }
.ak-t { font-size:15px; letter-spacing:.16em; font-weight:700; color:#FFD9A8; white-space:nowrap; display:flex; align-items:center; gap:9px; }
.ak { display:inline-flex; align-items:center; gap:9px; border-radius:14px; font-weight:700; white-space:nowrap; color:#1B0E3F;
  background:linear-gradient(95deg,#FFD08A,#FF9EC0); box-shadow:0 10px 24px rgba(255,126,176,.25); }
.chk { background:rgba(255,255,255,.10); border:2px solid rgba(255,255,255,.26); font-stretch:92%; }
.grid { display:grid; grid-template-columns:repeat(3,1fr); }
.cta { border-radius:34px; background:linear-gradient(95deg,#FFC46B 0%,#FF7EB0 58%,#B79CFF 100%); color:#150B3A; box-shadow:0 20px 50px rgba(255,126,176,.30); }
.cta .go { background:#150B3A; }
.more { border-color:rgba(255,196,107,.65); color:#F3E9FF; background:rgba(255,196,107,.07); }
.more b { color:#FFD08A; }
"""
def v1(story):
    H = 1920 if story else 1350
    top = 196 if story else 64
    hs = 132 if story else 118
    b = f'<div class="abs" style="right:64px;top:{top-6}px"><img src="file://{D}/logo_white.png" style="width:{150 if story else 136}px"></div>'
    b += f'<div class="abs pill" style="left:64px;top:{top+10}px;padding:10px 20px;font-size:{20 if story else 18}px">{SPARK("#FFC46B")}PUANTAJ · AKTARIM · İK · MOBİL</div>'
    ty = top + (96 if story else 84)
    b += f'<div class="abs hd" style="left:60px;top:{ty}px;font-size:{hs}px"><div>Hepsi tek bir</div><div class="grad">PDKS’de.</div></div>'
    by = ty + int(hs * 1.8) + (34 if story else 22)
    bs = 78 if story else 68
    b += (f'<div class="abs" style="left:60px;right:56px;top:{by}px;display:flex;align-items:center;gap:22px">'
          f'<span class="br" style="font-size:{bs}px">nilSOFT PDKS</span>'
          f'<span class="kau" style="font-size:{int(bs*.66)}px;color:#FFC46B;transform:rotate(-4deg) translateY(-4px)">hepsi içinde!</span>'
          f'<span class="rule" style="flex:1"></span></div>')
    chips = lambda fs, py, px: "".join(f'<span class="chk" style="padding:{py}px {px}px;font-size:{fs}px">{CHECK("#FFC46B", 22)}{t}</span>' for t in MODUL)
    if not story:
        hy = by + 100
        b += f'<div class="abs hero" style="left:76px;top:{hy}px;width:520px;transform:perspective(1600px) rotateY(9deg) rotateX(2deg);transform-origin:right center"><img src="file://{D}/patron_ekrani.png"></div>'
        ak = "".join(f'<span class="ak" style="padding:11px 16px;font-size:23px">{SWAP("#1B0E3F")}{t}</span>' for t in AKT_KISA)
        b += f'<div class="abs" style="left:632px;top:{hy+4}px;width:400px"><div class="ak-t">{SPARK("#FFC46B",16)}PUANTAJ AKTARIMI</div><div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:14px">{ak}</div></div>'
        b += f'<div class="abs grid" style="left:56px;right:56px;top:{hy+318}px;gap:11px 14px">{chips(22, 12, 15)}</div>'
        b += more(1142, 48, 23, "#FFC46B")
        b += cta(1206, 104, 50, 19, "0 18px 0 34px", 68, "#FFC46B")
    else:
        hy = by + 100
        b += f'<div class="abs hero" style="left:255px;top:{hy}px;width:570px;transform:perspective(1800px) rotateX(6deg);transform-origin:center bottom"><img src="file://{D}/patron_ekrani.png"></div>'
        ak = "".join(f'<span class="ak" style="padding:10px 15px;font-size:22px">{SWAP("#1B0E3F", 20)}{t}</span>' for t in AKT_KISA)
        ay = hy + 340
        b += f'<div class="abs" style="left:56px;right:56px;top:{ay}px"><div class="ak-t">{SPARK("#FFC46B",16)}PUANTAJ AKTARIMI</div><div style="display:flex;gap:11px;margin-top:12px;justify-content:space-between">{ak}</div></div>'
        b += f'<div class="abs grid" style="left:56px;right:56px;top:{ay+102}px;gap:9px 14px">{chips(23, 10, 15)}</div>'
        b += more(1422, 48, 24, "#FFC46B")
        b += cta(1482, 104, 54, 21, "0 20px 0 38px", 74, "#FFC46B")
    return page(CSS1, b, H)

# ======================================================================= V2 — Sarı-siyah
CSS2 = """
.cv { color:#111; background:
   radial-gradient(720px 620px at 100% 0%, rgba(255,255,255,.55), transparent 62%),
   radial-gradient(760px 700px at 0% 100%, rgba(255,150,0,.34), transparent 62%),
   radial-gradient(rgba(0,0,0,.10) 1.3px, transparent 1.6px) 0 0/24px 24px,
   #FFD21F; }
.pill { background:#111; color:#FFD21F; }
.box { display:inline-block; background:#111; color:#FFD21F; border-radius:22px; transform:rotate(-2.2deg); }
.rule { height:4px; background:#111; border-radius:2px; }
.cloud { display:flex; flex-wrap:wrap; justify-content:center; }
.chk.k { background:#111; color:#fff; }
.chk.w { background:#fff; color:#111; box-shadow:0 8px 18px rgba(120,80,0,.18); }
.cta { border-radius:34px; background:#111; color:#fff; box-shadow:0 22px 50px rgba(90,60,0,.35); }
.cta .t { color:#FFD21F; }
.cta .go { background:#FFD21F; }
.more { border-color:#111; border-width:2.5px; color:#111; }
"""
def v2(story):
    H = 1920 if story else 1350
    top = 196 if story else 64
    hs = 168 if story else 148
    b = f'<div class="abs" style="right:64px;top:{top-6}px"><img src="file://{D}/logo_navy.png" style="width:{150 if story else 136}px;filter:brightness(0)"></div>'
    b += f'<div class="abs pill" style="left:64px;top:{top+10}px;padding:12px 22px;font-size:{20 if story else 18}px">{SPARK("#FFD21F")}PUANTAJ · AKTARIM · İK · MOBİL</div>'
    ty = top + (104 if story else 90)
    b += (f'<div class="abs hd" style="left:58px;top:{ty}px;font-size:{hs}px"><div>Hepsi tek bir</div>'
          f'<div class="box" style="padding:.06em .16em .1em;margin-top:.06em;margin-left:-6px">PDKS’de.</div></div>')
    by = ty + int(hs * 2.02) + (40 if story else 26)
    bs = 82 if story else 70
    b += (f'<div class="abs" style="left:60px;right:56px;top:{by}px;display:flex;align-items:center;gap:22px">'
          f'<span class="br" style="font-size:{bs}px">nilSOFT PDKS</span><span class="rule" style="flex:1"></span>'
          f'<span class="kau" style="font-size:{int(bs*.66)}px;transform:rotate(-4deg) translateY(-4px)">hepsi içinde!</span></div>')
    fs, py, px, gap, rg = (28, 14, 21, 13, 16) if story else (27, 12, 20, 13, 13)
    order = [("k", t) for t in AKTARIM] + [("w", t) for t in MODUL]
    rows = [order[i:i+3] for i in range(0, len(order), 3)]
    c = "".join('<div class="cloud" style="gap:%dpx">' % gap + "".join(
        f'<span class="chk {k}" style="padding:{py}px {px}px;font-size:{fs}px">{CHECK("#FFD21F" if k=="k" else "#111", 24)}{t}</span>' for k, t in row) + '</div>' for row in rows)
    c += '<div class="cloud">' + more(None, 58 if story else 54, 26 if story else 25, "#111", "padding:0 26px;") + '</div>'
    b += f'<div class="abs" style="left:40px;right:40px;top:{by + (130 if story else 104)}px;display:flex;flex-direction:column;gap:{rg}px">{c}</div>'
    if not story: b += cta(1198, 104, 50, 19, "0 18px 0 34px", 68, "#111")
    else:         b += cta(1474, 108, 54, 21, "0 20px 0 38px", 74, "#111")
    return page(CSS2, b, H)

# ======================================================================= V3 — Açık zemin, merkez şeması
BLUE, PINK, AMBER, VIOLET, GREEN, ORANGE = "#2563EB", "#DB2777", "#D97706", "#7C3AED", "#059669", "#EA580C"
SOL = [("PUANTAJ AKTARIMI", BLUE, AKTARIM), ("YÖNETİM", PINK, ["Patron ekranı", "Turnover"]), ("YAN HAKLAR", AMBER, ["Yemekhane", "Yol yardımı"])]
SAG = [("PLANLAMA", VIOLET, ["Vardiya planlama", "Yıllık izin planlama", "Servis aracı planlama"]),
       ("ÖZLÜK", GREEN, ["Yıllık izin", "SGK raporu modülü", "Evrak takibi", "Eğitim takibi", "Zimmet takibi"]),
       ("MOBİL", ORANGE, ["Personel mobil", "Yönetici mobil", "Dinamik QR kod"])]
CSS3 = """
.cv { color:#0E1B3D; background:
   radial-gradient(760px 640px at 100% 0%, rgba(124,58,237,.16), transparent 62%),
   radial-gradient(760px 700px at 0% 42%, rgba(37,99,235,.14), transparent 62%),
   radial-gradient(820px 700px at 90% 100%, rgba(234,88,12,.14), transparent 62%),
   radial-gradient(rgba(14,27,61,.09) 1.3px, transparent 1.6px) 0 0/24px 24px,
   #F5F7FD; }
.grad { background-image:linear-gradient(90deg,#2563EB 0%,#7C3AED 55%,#DB2777 100%); -webkit-background-clip:text; background-clip:text; color:transparent; padding-bottom:.06em; display:inline-block; }
.pill { background:#0E1B3D; color:#fff; }
.lab { background:#0E1B3D; color:#fff; border-radius:18px; display:inline-block; }
.hc { position:absolute; display:flex; align-items:center; gap:10px; background:#fff; border-radius:999px; font-weight:600; white-space:nowrap; color:#0E1B3D;
  box-shadow:0 8px 20px rgba(14,27,61,.10); border:2px solid; }
.hc i { flex:none; width:12px; height:12px; border-radius:50%; }
.gl { position:absolute; font-size:13.5px; font-weight:700; letter-spacing:.16em; white-space:nowrap; }
.med { position:absolute; border-radius:50%; background:conic-gradient(#2563EB,#7C3AED,#DB2777,#EA580C,#D97706,#059669,#2563EB); display:grid; place-items:center;
  box-shadow:0 30px 70px rgba(37,99,235,.30), 0 0 0 14px rgba(255,255,255,.75); }
.med > div { border-radius:50%; background:#fff; display:flex; flex-direction:column; align-items:center; justify-content:center; }
.med b { font-family:"Brico"; font-weight:800; font-stretch:75%; letter-spacing:.04em; color:#0E1B3D; line-height:1; }
.cta { border-radius:34px; background:linear-gradient(95deg,#2563EB 0%,#7C3AED 58%,#DB2777 100%); color:#fff; box-shadow:0 20px 50px rgba(76,60,220,.30); }
.cta .go { background:#fff; }
.more { border-color:rgba(124,58,237,.55); color:#0E1B3D; background:rgba(255,255,255,.6); }
.more b { color:#6D28D9; }
"""
def hub(cy, ch, cg, lh, fs, R=112):
    cx, xl, xr = 540, 366, 714           # sol sütunun sağ kenarı, sağ sütunun sol kenarı
    def col(groups, side):
        n = sum(len(g[2]) for g in groups)
        total = n * ch + (n - 1) * cg + len(groups) * lh + (len(groups) - 1) * 10
        y = cy - total / 2
        html, lines, k, N = "", "", 0, n
        for gi, (name, colr, items) in enumerate(groups):
            if gi: y += 10
            pos = f'right:{1080-xl}px' if side == "L" else f'left:{xr}px'
            html += f'<div class="gl" style="{pos};top:{y+lh-24:.0f}px;color:{colr}">{name}</div>'
            y += lh
            for t in items:
                yc = y + ch / 2
                dot = f'<i style="background:{colr}"></i>'
                inner = (t + dot) if side == "L" else (dot + t)
                pad = f'0 12px 0 20px' if side == "L" else f'0 20px 0 12px'
                html += f'<div class="hc" style="{pos};top:{y:.0f}px;height:{ch}px;padding:{pad};font-size:{fs}px;border-color:{colr}55">{inner}</div>'
                th = math.radians(-62 + 124 * (k / (N - 1)))          # merkeze giriş açısı
                if side == "L":
                    x0, ex, ey = xl + 4, cx - (R + 18) * math.cos(th), cy + (R + 18) * math.sin(th)
                    k2 = (ex - x0) * .55; d = f'M{x0},{yc:.1f} C{x0+k2:.1f},{yc:.1f} {ex-k2:.1f},{ey:.1f} {ex:.1f},{ey:.1f}'
                else:
                    x0, ex, ey = xr - 4, cx + (R + 18) * math.cos(th), cy + (R + 18) * math.sin(th)
                    k2 = (x0 - ex) * .55; d = f'M{x0},{yc:.1f} C{x0-k2:.1f},{yc:.1f} {ex+k2:.1f},{ey:.1f} {ex:.1f},{ey:.1f}'
                lines += f'<path d="{d}" fill="none" stroke="{colr}" stroke-width="2.6" stroke-linecap="round" opacity=".75"/><circle cx="{ex:.1f}" cy="{ey:.1f}" r="4.5" fill="{colr}"/>'
                y += ch + cg; k += 1
            y -= cg
        return html, lines, total
    hl, ll, tl = col(SOL, "L"); hr, lr, tr = col(SAG, "R")
    svg = f'<svg class="abs" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true">{ll}{lr}</svg>'
    med = (f'<div class="med" style="left:{cx-R}px;top:{cy-R}px;width:{2*R}px;height:{2*R}px"><div style="width:{2*R-16}px;height:{2*R-16}px">'
           f'<img src="file://{D}/logo_navy.png" style="width:{int(R*.98)}px;margin-top:-4px"><b style="font-size:{int(R*.36)}px;margin-top:4px">PDKS</b></div></div>')
    return svg + hl + hr + med, max(tl, tr)

def v3(story):
    H = 1920 if story else 1350
    top = 196 if story else 64
    b = f'<div class="abs" style="right:64px;top:{top-6}px"><img src="file://{D}/logo_navy.png" style="width:{150 if story else 136}px"></div>'
    b += f'<div class="abs pill" style="left:64px;top:{top+10}px;padding:12px 22px;font-size:{20 if story else 18}px">{SPARK("#FFD21F")}PUANTAJ · AKTARIM · İK · MOBİL</div>'
    if story:
        ty, hs = top + 100, 132
        b += f'<div class="abs hd" style="left:60px;top:{ty}px;font-size:{hs}px"><div>Hepsi tek bir</div><div class="grad">PDKS’de.</div></div>'
        ly = ty + int(hs * 1.8) + 34
        b += f'<div class="abs" style="left:60px;top:{ly}px;display:flex;align-items:center;gap:22px"><span class="lab br" style="font-size:64px;padding:12px 26px 14px">nilSOFT PDKS</span><span class="kau" style="font-size:50px;color:#7C3AED;transform:rotate(-4deg)">hepsi içinde!</span></div>'
        h, tot = hub(1046, 50, 9, 34, 24)
        b += h
        b += more(1422, 48, 24, "#7C3AED")
        b += cta(1482, 104, 54, 21, "0 20px 0 38px", 74, "#2563EB")
    else:
        ty, hs = top + 84, 104
        b += f'<div class="abs hd" style="left:60px;top:{ty}px;font-size:{hs}px">Hepsi tek bir <span class="grad">PDKS’de.</span></div>'
        ly = ty + int(hs * .9) + 24
        b += f'<div class="abs" style="left:60px;top:{ly}px;display:flex;align-items:center;gap:20px"><span class="lab br" style="font-size:54px;padding:10px 22px 12px">nilSOFT PDKS</span><span class="kau" style="font-size:44px;color:#7C3AED;transform:rotate(-4deg)">hepsi içinde!</span></div>'
        h, tot = hub(770, 48, 9, 32, 23, R=108)
        b += h
        b += more(1140, 48, 23, "#7C3AED")
        b += cta(1206, 100, 48, 19, "0 18px 0 34px", 66, "#2563EB")
    return page(CSS3, b, H)

JOBS = {"v1": [("R1_aurora_post", v1(False), 1350), ("R1_aurora_story", v1(True), 1920)],
        "v2": [("R2_sari_post", v2(False), 1350), ("R2_sari_story", v2(True), 1920)],
        "v3": [("R3_merkez_post", v3(False), 1350), ("R3_merkez_story", v3(True), 1920)]}
only = sys.argv[1:] or list(JOBS)
JS = """(()=>{const r=e=>{const b=e.getBoundingClientRect();return [Math.round(b.left),Math.round(b.top),Math.round(b.right),Math.round(b.bottom)]};
 const all=[...document.querySelectorAll('.chk,.hc,.ak,.gl')].map(r);
 return {hd:[...document.querySelectorAll('.hd')].map(r), minL:Math.min(...all.map(a=>a[0])), maxR:Math.max(...all.map(a=>a[2])), minT:Math.min(...all.map(a=>a[1])), maxB:Math.max(...all.map(a=>a[3])),
  cta:r(document.querySelector('.cta')), ctaS:r(document.querySelector('.cta .s')), hero:document.querySelector('.hero')?r(document.querySelector('.hero')):null, more:r(document.querySelector('.more')), n:all.length}})()"""
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(device_scale_factor=1)
    for key in only:
        for name, h, H in JOBS[key]:
            path = os.path.join(D, name + ".html"); open(path, "w", encoding="utf-8").write(h)
            pg.set_viewport_size({"width": 1080, "height": H}); pg.goto("file://" + path)
            pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
            print(name, pg.evaluate(JS))
            pg.screenshot(path=os.path.join(OUT, name + ".png"), clip={"x": 0, "y": 0, "width": 1080, "height": H})
    br.close()
