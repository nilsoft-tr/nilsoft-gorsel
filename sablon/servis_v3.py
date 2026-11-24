# -*- coding: utf-8 -*-
"""Servis Planlama kartı v3 — gerçek ekran haritası (servis_harita.png) + günlük liste kâğıdı, zümrüt gece."""
import os, sys
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, "out"); os.makedirs(OUT, exist_ok=True)
F = "/tmp/fonts2"

CSS = f"""
@font-face {{ font-family:"Brico"; src:url("file://{F}/Bricolage.ttf"); font-weight:200 800; font-stretch:75% 100%; }}
@font-face {{ font-family:"Plex"; src:url("file://{F}/PlexSans.ttf"); font-weight:100 700; font-stretch:85% 100%; }}
@font-face {{ font-family:"PlexMono"; src:url("file://{F}/PlexMono-SemiBold.ttf"); font-weight:600; }}
@font-face {{ font-family:"Kaushan"; src:url("file://{F}/KaushanScript.ttf"); }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
html,body {{ background:#000; }}
.cv {{ position:relative; overflow:hidden; width:1080px; font-family:"Plex",sans-serif; color:#fff;
  background:
   radial-gradient(900px 600px at 85% 8%, rgba(124,242,176,.20), transparent 60%),
   radial-gradient(700px 700px at 0% 100%, rgba(255,209,102,.12), transparent 60%),
   radial-gradient(rgba(255,255,255,.10) 1.3px, transparent 1.6px) 0 0/24px 24px,
   linear-gradient(165deg,#0E4A3B 0%,#0A3A2F 45%,#062720 100%); }}
.abs {{ position:absolute; }}
.hd {{ font-family:"Brico"; font-weight:800; font-stretch:75%; letter-spacing:-0.01em; line-height:.9; }}
.grad {{ background-image:linear-gradient(90deg,#8CF5C0 0%,#FFE08A 70%,#FFC857 100%); -webkit-background-clip:text; background-clip:text; color:transparent; padding-bottom:.06em; }}
.pill {{ display:inline-flex; align-items:center; gap:12px; border-radius:999px; font-weight:600; letter-spacing:.12em;
  background:rgba(140,245,192,.14); border:2px solid rgba(140,245,192,.5); color:#BFFADD; }}
.mapr {{ border-radius:22px; overflow:hidden; border:7px solid #fff; background:#fff;
  box-shadow:0 50px 90px rgba(0,0,0,.5), 0 0 120px rgba(124,242,176,.18); }}
.mapr img {{ display:block; width:100%; }}
.sheet {{ background:#fff; color:#13271F; border-radius:16px; overflow:hidden; box-shadow:0 36px 70px rgba(0,0,0,.5), 0 0 0 1px rgba(0,0,0,.06); }}
.sh-h {{ background:#0F8A5F; color:#fff; padding:16px 18px 14px; }}
.sh-h small {{ display:block; font-size:12px; letter-spacing:.14em; font-weight:700; opacity:.9; }}
.sh-h b {{ display:block; font-family:"Brico"; font-weight:800; font-size:25px; line-height:1.15; margin-top:3px; }}
.sh-h span {{ font-size:14px; opacity:.92; }}
.sr {{ display:flex; align-items:center; gap:11px; padding:9px 16px; border-bottom:1px solid #E6ECE7; }}
.sr i {{ flex:none; width:26px; height:26px; border-radius:50%; background:#C0264B; color:#fff; font-style:normal; font-family:"PlexMono"; font-size:13px; display:grid; place-items:center; }}
.sr b {{ font-size:15.5px; font-weight:600; white-space:nowrap; }}
.sr em {{ margin-left:auto; font-style:normal; font-size:11.5px; letter-spacing:.04em; color:#5B6B63; font-weight:600; }}
.sf {{ padding:11px 16px; font-size:14px; color:#3F5248; font-weight:600; background:#F2F6F3; }}
.sf .mono {{ font-family:"PlexMono"; color:#13271F; }}
.tag {{ background:#fff; color:#0D2A20; border-radius:18px; padding:13px 20px 13px 14px; display:flex; align-items:center; gap:13px; box-shadow:0 22px 44px rgba(0,0,0,.4); }}
.tag .ic {{ width:44px; height:44px; border-radius:50%; background:#E3F7EC; display:grid; place-items:center; flex:none; }}
.tag .ic svg {{ width:26px; height:26px; }}
.tag b {{ display:block; font-size:19px; line-height:1.2; }}
.tag span {{ font-size:15.5px; color:#4A5D53; font-weight:500; }}
.chips {{ display:flex; flex-wrap:wrap; gap:14px; }}
.chk {{ display:inline-flex; align-items:center; gap:11px; border-radius:999px; font-weight:600; white-space:nowrap;
  background:rgba(255,255,255,.08); border:2px solid rgba(255,255,255,.22); }}
.chk svg {{ width:24px; height:24px; flex:none; }}
.chk.hot {{ background:rgba(140,245,192,.16); border-color:rgba(140,245,192,.6); }}
.cta {{ border-radius:34px; background:linear-gradient(95deg,#8CF5C0 0%,#FFE08A 60%,#FFC857 100%); color:#062720; display:flex; align-items:center; justify-content:space-between; box-shadow:0 20px 50px rgba(255,200,87,.25); }}
.cta .t {{ font-family:"Brico"; font-weight:800; font-stretch:75%; line-height:1; }}
.cta .s {{ font-weight:600; }}
.cta .go {{ border-radius:50%; background:#062720; display:grid; place-items:center; flex:none; }}
"""

CHECK = lambda col: f'<svg viewBox="0 0 24 24" fill="none" stroke="{col}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="#8CF5C0" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v15M5.5 12.5 12 19l6.5-6.5"/></svg>'
SPARK = '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M12 1.5c.6 5.3 3.2 7.9 8.5 8.5-5.3.6-7.9 3.2-8.5 8.5-.6-5.3-3.2-7.9-8.5-8.5 5.3-.6 7.9-3.2 8.5-8.5z" fill="#FFE08A"/></svg>'

def underline(w):
    return (f'<svg viewBox="0 0 {w} 40" width="{w}" height="40" aria-hidden="true"><defs><linearGradient id="ug" x1="0" x2="1">'
            f'<stop offset="0" stop-color="#8CF5C0"/><stop offset="1" stop-color="#FFC857"/></linearGradient></defs>'
            f'<path d="M6,24 C{w*.25:.0f},12 {w*.6:.0f},8 {w-8},16" fill="none" stroke="url(#ug)" stroke-width="9" stroke-linecap="round"/>'
            f'<path d="M{w*.12:.0f},33 C{w*.4:.0f},25 {w*.7:.0f},23 {w*.9:.0f},27" fill="none" stroke="url(#ug)" stroke-width="5" stroke-linecap="round" opacity=".8"/></svg>')

def sheet(w, n=5):
    rows = [("1", "Ali Kaplan", "DOKUMA"), ("2", "Yasin Bozkurt", "DOKUMA"), ("3", "Seda Ateş", "KONFEKSİYON"),
            ("4", "Recep Arslan", "KONFEKSİYON"), ("5", "Aslı Güler", "KONFEKSİYON")]
    r = "".join(f'<div class="sr"><i>{k}</i><b>{a}</b><em>{b}</em></div>' for k, a, b in rows[:n])
    return f'''<div class="sheet" style="width:{w}px"><div class="sh-h"><small>GÜNLÜK SERVİS LİSTESİ</small><b>İdari-Depo</b><span>Kemal Usta · 20 DT 105</span></div>
{r}<div class="sf">+{20-n} personel · <span class="mono">15,1 km</span> · <span class="mono">26 dk</span></div></div>'''

def card(story):
    H = 1920 if story else 1350
    top = 190 if story else 64
    hs = 136 if story else 118
    b = f'<div class="abs" style="right:64px;top:{top-6}px"><img src="file://{D}/logo_white.png" style="width:{150 if story else 136}px"></div>'
    b += f'<div class="abs pill" style="left:64px;top:{top+10}px;padding:10px 20px;font-size:{20 if story else 18}px">{SPARK}YENİ MODÜL · SERVİS PLANLAMA</div>'
    ty = top + (96 if story else 84)
    b += f'<div class="abs hd" style="left:60px;top:{ty}px;font-size:{hs}px"><div>Personel servisi</div><div class="grad">artık haritada.</div></div>'
    b += f'<div class="abs" style="left:70px;top:{ty + int(hs*1.82)}px">{underline(560 if story else 500)}</div>'
    tag = f'<div class="tag"><span class="ic">{CHECK("#0F8A5F")}</span><div><b>Otomatik dağıtıldı</b><span>83 personel · 5 servis</span></div></div>'
    if not story:
        b += f'<div class="abs mapr" style="left:286px;top:414px;width:736px;transform:perspective(1800px) rotateY(-9deg) rotateX(3deg);transform-origin:left center"><img src="file://{D}/servis_harita.png"></div>'
        b += f'<div class="abs" style="left:40px;top:694px;transform:rotate(-4deg)">{sheet(300, 4)}</div>'
        b += f'<div class="abs" style="left:470px;top:884px">{tag}</div>'
        b += '<div class="abs" style="left:770px;top:962px;font-family:Kaushan;font-size:46px;color:#FFE08A;transform:rotate(-5deg);white-space:nowrap">rota hazır!</div>'
        chips = [("Otomatik personel ataması", 1), ("Haritada otomatik güzergâh", 1), ("Sefer raporu", 0)]
        c = "".join(f'<span class="chk{" hot" if h else ""}" style="padding:12px 20px;font-size:22px">{CHECK("#8CF5C0")}{t}</span>' for t, h in chips)
        b += f'<div class="abs chips" style="left:56px;right:40px;top:1106px">{c}</div>'
        b += f'''<div class="abs cta" style="left:56px;right:56px;top:1210px;height:100px;padding:0 18px 0 34px">
<div><div class="t" style="font-size:50px">Ücretsiz demo</div><div class="s" style="font-size:19px;margin-top:4px">Kendi verinizle canlı gösterim · 0 541 796 58 10</div></div>
<div class="go" style="width:68px;height:68px">{ARROW}</div></div>'''
    else:
        b += f'<div class="abs mapr" style="left:240px;top:630px;width:764px;transform:perspective(1800px) rotateY(-9deg) rotateX(3deg);transform-origin:left center"><img src="file://{D}/servis_harita.png"></div>'
        b += f'<div class="abs" style="left:40px;top:916px;transform:rotate(-4deg)">{sheet(330)}</div>'
        b += f'<div class="abs" style="left:480px;top:1128px">{tag}</div>'
        b += '<div class="abs" style="left:770px;top:1212px;font-family:Kaushan;font-size:52px;color:#FFE08A;transform:rotate(-5deg);white-space:nowrap">rota hazır!</div>'
        chips = [("Otomatik personel ataması", 1), ("Haritada otomatik güzergâh", 1), ("Günlük servis listesi", 0), ("Sefer raporu", 0)]
        c = "".join(f'<span class="chk{" hot" if h else ""}" style="padding:13px 22px;font-size:24px">{CHECK("#8CF5C0")}{t}</span>' for t, h in chips)
        b += f'<div class="abs chips" style="left:56px;right:40px;top:1346px">{c}</div>'
        b += f'''<div class="abs cta" style="left:56px;right:56px;top:1514px;height:110px;padding:0 20px 0 38px">
<div><div class="t" style="font-size:54px">Ücretsiz demo</div><div class="s" style="font-size:21px;margin-top:4px">Kendi verinizle canlı gösterim · 0 541 796 58 10</div></div>
<div class="go" style="width:74px;height:74px">{ARROW}</div></div>'''
    return f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="cv" style="height:{H}px">{b}</div></body></html>'

JOBS = [("A_servis_post_v3", card(False), 1350), ("A_servis_story_v3", card(True), 1920)]
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(device_scale_factor=1)
    for name, h, H in JOBS:
        path = os.path.join(D, name + ".html"); open(path, "w", encoding="utf-8").write(h)
        pg.set_viewport_size({"width": 1080, "height": H}); pg.goto("file://" + path)
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        info = pg.evaluate("""(()=>{const r=e=>{const b=e.getBoundingClientRect();return [Math.round(b.left),Math.round(b.top),Math.round(b.right),Math.round(b.bottom)]};
          return {chips:[...document.querySelectorAll('.chk')].map(r), cta:r(document.querySelector('.cta')), map:r(document.querySelector('.mapr')), sheet:r(document.querySelector('.sheet')), tag:r(document.querySelector('.tag'))}})()""")
        pg.screenshot(path=os.path.join(OUT, name + ".png"), clip={"x": 0, "y": 0, "width": 1080, "height": H})
        print(name, info)
    br.close()
