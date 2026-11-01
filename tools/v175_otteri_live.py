#!/usr/bin/env python3
"""v175 — Otteri ตัวจริงใช้ระบบใหม่ (เดิมเปิดเฉพาะหน้าทดสอบ test/)
ขั้นตอน (ทำครั้งเดียว):
  1) python3 tools/otteri-test/patch_otteri_test.py index.html /tmp/feat.html tools/otteri-test/sol_core.jsx --feature-only
  2) python3 tools/v175_otteri_live.py /tmp/feat.html index.html sw.js
ข้อ 2 เอาเงื่อนไข window.TEST_MODE หน้า flags ของ Otteri ออก (ระบบแบบเท็ดดี้ 2 · เริ่มเครื่องผ่าน SOL · ui2 · ผ้าเจ้าของ · ร้านเกอิชาค้างจ่าย · ล้างเครื่อง)
  — ป้าย 'ยังไม่ได้ใส่ QR บัญชีร้าน' ในใบรับงานยังขึ้นเฉพาะหน้าทดสอบ (ตัวจริงไม่มี QR ก็ไม่ขึ้นอะไร เหมือนเดิม)
หลังจากนี้ index.html เป็นต้นฉบับของทุกอย่าง · หน้าทดสอบสร้างด้วย tools/otteri-test/make_test.py (ห่อทดสอบอย่างเดียว)
"""
import sys

SRC, IDX, SW = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(SRC, encoding='utf-8').read()
sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    assert n == count, f'{label}: found {n}, expected {count}'
    s = s.replace(old, new)


rep("window.APP_VERSION = 'v174-2026-10-31';", "window.APP_VERSION = 'v175-2026-11-01';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v174';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v174';", "const CACHE_NAME = 'plp-laundry-v175';")

rep("// 🧪 Otteri ใช้ระบบแบบเท็ดดี้ 2 (เงินสดในมือ · เริ่มเครื่องผ่าน SOL · กระทบยอด WDF) — เปิดเฉพาะหน้าทดสอบก่อน\nif (window.TEST_MODE) Object.assign(OTTERI_CONFIG, {",
    "// 🟢 v175 (1 พ.ย. 69): Otteri ตัวจริงใช้ระบบแบบเท็ดดี้ 2 (เงินสดในมือ · เริ่มเครื่องผ่าน SOL · กระทบยอด WDF · ui2 · ผ้าเจ้าของ · ร้านเกอิชาค้างจ่าย)\nObject.assign(OTTERI_CONFIG, {", 'otteri flags live')
rep("if (window.TEST_MODE) SHOP_MENUS.otteri.internal = true; // 🧪 Otteri:", "SHOP_MENUS.otteri.internal = true; // 🟢 v175 Otteri:", 'otteri internal menu live')
# แถวงานภายในในรายการหน้าแรก: กล่องซ้ายโชว์อีโมจิอยู่แล้ว (หน้าแบบเท็ดดี้ 2) → ชื่อไม่ต้องซ้ำอีโมจิ (เดิมขึ้น 🧼 🧼 ล้างเครื่อง)
rep("const internalTitleOf = (o, config) => { const t = INTERNAL_TYPES.find(x => x.id === o.internalType) || {}; const ms = (o.internalMachines || []).map(m => String(m).replace(/^(ซัก|อบ) /, '')); return `${t.emoji || '🔧'} ${tr(config, t.label || 'งานภายใน')}",
    "const internalTitleOf = (o, config, noEmoji) => { const t = INTERNAL_TYPES.find(x => x.id === o.internalType) || {}; const ms = (o.internalMachines || []).map(m => String(m).replace(/^(ซัก|อบ) /, '')); return `${noEmoji ? '' : (t.emoji || '🔧') + ' '}${tr(config, t.label || 'งานภายใน')}", 'internal title emoji opt')
rep("{isInternalOrder(o) ? internalTitleOf(o, config) : o.customerName}", "{isInternalOrder(o) ? internalTitleOf(o, config, T2H) : o.customerName}", 'home row no double emoji')
assert s.count("if (window.TEST_MODE) Object.assign(OTTERI_CONFIG") == 0
assert s.count('window.TEST_MODE') == 1, 'only the receipt QR hint stays test-only'

open(IDX, 'w', encoding='utf-8').write(s)
open(SW, 'w', encoding='utf-8').write(sw)
print('v175 applied:', len(s), 'chars')
