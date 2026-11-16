#!/usr/bin/env python3
"""v216: web orders (teddy1-order.html / teddy2-order.html) can now include shop detergent / softener sachets.
Owner request 16 Nov 2026. The order page saves detergentQty / softenerQty (+ extrasTotal) in webOrders;
this version copies them into the job form when the maid picks the web order — otherwise the form total would be
lower than what the customer saw (amber 'ลูกค้าเห็นยอด ~฿… แต่ในฟอร์ม ฿…' warning) and the sachets would be missed.
Old web orders without these fields → 0 (unchanged behaviour).
Usage: python3 tools/v216_web_order_detergent.py index.html sw.js"""
import sys
idx, sw = sys.argv[1], sys.argv[2]
s = open(idx, encoding='utf-8').read()
def rep(old, new):
    global s
    assert s.count(old) == 1, ('count', s.count(old), old[:80])
    s = s.replace(old, new)

rep("""    setDryItems((w.dryItems || []).map(i => ({ size: i.size, qty: i.qty, topUp: 0 })));
    setNoFold(w.wantFold === false);""",
"""    setDryItems((w.dryItems || []).map(i => ({ size: i.size, qty: i.qty, topUp: 0 })));
    // 🧴 v216 ลูกค้าสั่งซื้อน้ำยาร้านมาจากหน้าเว็บ (ซองละ ฿5) → ใส่จำนวนซองให้เลย ยอดในฟอร์มจะตรงกับที่ลูกค้าเห็น
    setDetergentQty(Math.max(0, parseInt(w.detergentQty, 10) || 0));
    setSoftenerQty(Math.max(0, parseInt(w.softenerQty, 10) || 0));
    setNoFold(w.wantFold === false);""")
rep("""{(w.dryItems || []).map(i => `อบ ${i.size}กก.×${i.qty}`).join(', ')}
""", """{(w.dryItems || []).map(i => `อบ ${i.size}กก.×${i.qty}`).join(', ')}{w.detergentQty > 0 ? ` · 🧴×${w.detergentQty}` : ''}{w.softenerQty > 0 ? ` · 🌸×${w.softenerQty}` : ''}
""")
rep("window.APP_VERSION = 'v215-2026-11-16';", "window.APP_VERSION = 'v216-2026-11-16';")
open(idx, 'w', encoding='utf-8').write(s)
w = open(sw, encoding='utf-8').read()
assert w.count("const CACHE_NAME = 'plp-laundry-v215';") == 1
open(sw, 'w', encoding='utf-8').write(w.replace("const CACHE_NAME = 'plp-laundry-v215';", "const CACHE_NAME = 'plp-laundry-v216';"))
print('v216 patched')
