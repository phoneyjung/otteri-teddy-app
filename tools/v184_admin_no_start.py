#!/usr/bin/env python3
"""v184 — หน้าแอดมิน (ร้าน SOL) ไม่มีการ์ด 🧺 เริ่มเครื่อง / 📷 สแกนใบงาน แล้ว
ที่มา: เจ้าของ 2 พ.ย. 69 (รูปหน้าแอดมิน Otteri) 'ทำไมยังมี เริ่มเครื่อง' — v183 ติ๊กเริ่มใน SOL ให้ตอนบันทึกแล้ว
ร้านที่ปุ่มเริ่มเครื่องสั่งเครื่องจริง (EC) ยังมีการ์ดเหมือนเดิม
usage: python3 tools/v184_admin_no_start.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v183-2026-11-02';", "window.APP_VERSION = 'v184-2026-11-02';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v183';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v183';", "const CACHE_NAME = 'plp-laundry-v184';")
rep("""      {pulseOn(config) && <HomePulseStartCard config={config} orders={freeOrders} />}""",
    """      {pulseOn(config) && !isSol(config) && <HomePulseStartCard config={config} orders={freeOrders} />}{/* v184 SOL: บันทึกแล้วติ๊กเริ่มให้เอง (v183) — ไม่ต้องมีการ์ดเริ่มเครื่อง */}""", 'admin no start card')
open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v184 applied')
