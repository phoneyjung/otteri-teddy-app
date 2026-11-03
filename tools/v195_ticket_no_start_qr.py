#!/usr/bin/env python3
"""v195 — ใบงานไม่ต้องมีกรอบ 'สแกนเริ่มเครื่อง' แล้ว
ที่มา: เจ้าของ 3 พ.ย. 69 'สแกนเครื่องไม่ต้องมีแล้ว เพราะ ตอนนี้แม่บ้านถนัดกดผ่าน แอปไปแล้ว'
ทำอะไร
  - ซ่อนกรอบ QR เริ่มเครื่อง (v145) บนใบงานที่ปริ้น ทุกร้าน
    (เปิดคืนได้ด้วย config.ticketStartQr: true · ปุ่ม 📷 สแกนใบงานในแอปยังอยู่ ใบเก่าที่มี QR ยังสแกนได้)
  - ใบงานสั้นลง · QR บนใบเหลืออันเดียว = QR แอดไลน์ของลูกค้า (ไม่สับสน)
usage: python3 tools/v195_ticket_no_start_qr.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v194-2026-11-03';", "window.APP_VERSION = 'v195-2026-11-03';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v194';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v194';", "const CACHE_NAME = 'plp-laundry-v195';")

rep("""              {/* 📷 QR เริ่มเครื่อง — แม่บ้านสแกนแล้วเข้าหน้าเลือกเครื่องของงานนี้ (v145) */}
              {pulseOn(config) && order.id && creditForOrder(order, config) > 0 && (() => {""",
    """              {/* 📷 QR เริ่มเครื่อง — แม่บ้านสแกนแล้วเข้าหน้าเลือกเครื่องของงานนี้ (v145) · v195 ปิด (แม่บ้านกดผ่านแอปแล้ว) เปิดคืน = config.ticketStartQr */}
              {config.ticketStartQr && pulseOn(config) && order.id && creditForOrder(order, config) > 0 && (() => {""", 'hide start QR')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v195 applied')
