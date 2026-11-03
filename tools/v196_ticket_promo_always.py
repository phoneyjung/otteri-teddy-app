#!/usr/bin/env python3
"""v196 — ป้าย 'แอดไลน์ครั้งแรก ลดค่าซัก 50฿' ขึ้นทุกใบงาน
ที่มา: เจ้าของ 3 พ.ย. 69 'หมายถึง เปลี่ยนที่โปรแกรมนะ จะได้ปริ้นออกมาได้งานอื่น เอาแบบ แอดไลลด 50 ด้วย'
ทำอะไร
  - เดิม (v193/v194) ซ่อนป้ายโปรถ้าใบนั้นใช้โปรแอดไลน์แล้ว → ตอนนี้ขึ้นทุกใบ (คนอื่นเห็นใบแล้วสแกนแอดไลน์รับส่วนลด)
  - ร้านที่ไม่ได้เปิดป้ายโปร (ticketFooter.linePromo: false เช่น Teddy 1) ยังไม่ขึ้น
usage: python3 tools/v196_ticket_promo_always.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v195-2026-11-03';", "window.APP_VERSION = 'v196-2026-11-03';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v195';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v195';", "const CACHE_NAME = 'plp-laundry-v196';")

rep("const showPromo = !!(tf.linePromo && config.hasLinePromo && config.linePromoDiscount > 0 && !order.useLinePromo);",
    "const showPromo = !!(tf.linePromo && config.hasLinePromo && config.linePromoDiscount > 0); // v196 ขึ้นทุกใบ (คนอื่นเห็นจะได้สแกน)",
    'promo always')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v196 applied')
