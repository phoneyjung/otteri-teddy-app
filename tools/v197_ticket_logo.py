#!/usr/bin/env python3
"""v197 — โลโก้หน้าหมีเส้นขาวดำ (ลายน้อย) ที่หัวใบงาน
ที่มา: เจ้าของ 3 พ.ย. 69 'ทำโลโก้ แบบลายละเอียดไม่เยอะได้มั้ย' → เลือกแบบ B หน้าหมีขยิบตา ใส่หัวใบงาน
ทำอะไร
  - TEDDY_TICKET_LOGO = PNG ขาวดำ 1 บิต 240 px (วาดใหม่จากโลโก้หมี Teddy · ต้นฉบับ SVG อยู่ใน shop-assets)
  - config.ticketLogo (Teddy 1/2 ใช้ร่วมกัน) → หัวใบงาน: โลโก้ซ้าย 120 px + ชื่อร้านตัวใหญ่ขึ้น + 'ใบรับฝากซัก-อบ-พับ'
  - ร้านที่ไม่มี ticketLogo (Otteri) = หัวใบแบบเดิม
usage: python3 tools/v197_ticket_logo.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


LOGO = 'data:image/png;base64,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'

rep("window.APP_VERSION = 'v196-2026-11-03';", "window.APP_VERSION = 'v197-2026-11-03';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v196';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v196';", "const CACHE_NAME = 'plp-laundry-v197';")

rep("""const TEDDY_CONFIG = {
""", "// 🐻 v197 โลโก้หน้าหมีเส้นขาวดำ (ลายน้อย) สำหรับหัวใบงานเครื่องพิมพ์ความร้อน · ต้นฉบับ SVG: shop-assets\nconst TEDDY_TICKET_LOGO = '" + LOGO + "';\n\nconst TEDDY_CONFIG = {\n", 'logo const')
rep("""  logo: TEDDY_LOGO,
""", """  logo: TEDDY_LOGO,
  ticketLogo: TEDDY_TICKET_LOGO, // 🐻 v197 หัวใบงาน
""", 'config ticketLogo')

rep("""              <div style={{ textAlign: 'center', borderBottom: '2px dashed #000', paddingBottom: '8px', marginBottom: '8px' }}>
                <div style={{ fontSize: '32px', fontWeight: 800, lineHeight: 1.1 }}>{config.name}</div>
                <div style={{ fontSize: '21px', fontWeight: 700 }}>ใบรับฝากซัก-อบ-พับ</div>
              </div>""", """              <div style={{ borderBottom: '2px dashed #000', paddingBottom: '8px', marginBottom: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '16px' }}>
                {config.ticketLogo && <img src={config.ticketLogo} alt="" data-ticket-logo style={{ width: '120px', height: 'auto', display: 'block', flex: 'none' }} />}
                <div style={{ textAlign: config.ticketLogo ? 'left' : 'center' }}>
                  <div style={{ fontSize: config.ticketLogo ? '40px' : '32px', fontWeight: 800, lineHeight: 1.1 }}>{config.name}</div>
                  <div style={{ fontSize: '21px', fontWeight: 700 }}>ใบรับฝากซัก-อบ-พับ</div>
                </div>
              </div>""", 'ticket header')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v197 applied')
