#!/usr/bin/env python3
"""v214: printed job ticket (and every html2canvas image) — text drawn too low.
Case (owner, 12 Nov 2026, photo of Teddy 2 ticket คิว 5): letters sit low — 'ซัก อบ พับ ฟรี!' falls out of the black bar,
the pill text is cut by its border, 'แม่บ้าน' is crossed by the line above the total.
Root cause: html2canvas measures each font's baseline with a hidden 1x1 <img> that must sit inline next to sample text.
Tailwind's preflight makes every <img> display:block → that img drops to the next line → baseline = whole line height
→ every text run is painted ~0.45 em lower than on screen (22px text: 11px · 56px queue number: 26px).
Fix: keep html2canvas's measuring img inline (matched by its exact data URI) → raster = what the screen shows.
Usage: python3 tools/v214_ticket_text_baseline.py index.html sw.js"""
import sys
idx, sw = sys.argv[1], sys.argv[2]
s = open(idx, encoding='utf-8').read()

def rep(old, new):
    global s
    assert s.count(old) == 1, ('count', s.count(old), old[:90])
    s = s.replace(old, new)

GIF = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'  # html2canvas 1.4.1 SMALL_IMAGE
rep("""  input, textarea { font-family: inherit; }
""", """  input, textarea { font-family: inherit; }
  /* 🖨️ v214 ตัวอักษรในใบงาน/รูปใบเสร็จตกลงล่าง: html2canvas วัดเส้นฐานตัวอักษรด้วยรูป 1px ที่ต้องอยู่บรรทัดเดียวกับข้อความ
     แต่ Tailwind ตั้งรูปทุกรูปเป็น block → รูปหล่นไปบรรทัดใหม่ → วัดผิด ตัวอักษรถูกวาดต่ำกว่าจอ ~ครึ่งตัว · บรรทัดนี้คืนรูปวัดให้อยู่ในบรรทัด */
  img[src="%s"] { display: inline !important; }
""" % GIF)
rep("window.APP_VERSION = 'v213-2026-11-12';", "window.APP_VERSION = 'v214-2026-11-12';")
open(idx, 'w', encoding='utf-8').write(s)
w = open(sw, encoding='utf-8').read()
assert w.count("const CACHE_NAME = 'plp-laundry-v213';") == 1
open(sw, 'w', encoding='utf-8').write(w.replace("const CACHE_NAME = 'plp-laundry-v213';", "const CACHE_NAME = 'plp-laundry-v214';"))
print('v214 patched')
