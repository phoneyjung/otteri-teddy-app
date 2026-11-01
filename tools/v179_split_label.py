#!/usr/bin/env python3
"""v179 — ใบรับงาน/หน้ารายละเอียด: งานสด+โอน ขึ้น 'เงินสด' ทั้งใบ (เจ้าของเห็น 1 พ.ย. ใบ #05 Otteri: สด 180 หยอดตู้ + โอนค่าพับ 20)
ข้อมูลในระบบถูกอยู่แล้ว (paymentMethod 'split' cash 180 / transfer 20) — แก้แค่ป้าย: '💵 สด ฿180 + 💳 โอน ฿20'
usage: python3 tools/v179_split_label.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()
def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)
rep("window.APP_VERSION = 'v178-2026-11-01';", "window.APP_VERSION = 'v179-2026-11-01';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v178';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v178';", "const CACHE_NAME = 'plp-laundry-v179';")
rep("""const isInternalOrder = (o) => !!(o && o.internalType);""",
    """const isInternalOrder = (o) => !!(o && o.internalType);
// 💵 v179 ป้ายวิธีจ่ายบนใบรับงาน — สด+โอน บอกยอดแยก (เดิมขึ้น 'เงินสด' ทั้งใบ)
const payLabelOf = (o, config) => (o.paymentMethod === 'account' ? '🏢 ' + accountPayText(o, config) : o.paymentMethod === 'transfer' ? '💳 โอน' : o.paymentMethod === 'split' ? `💵 สด ฿${formatMoney(o.cashAmount || 0)} + 💳 โอน ฿${formatMoney(o.transferAmount || 0)}` : '💵 เงินสด');""", 'payLabelOf')
rep("""{internal ? '🔧 งานภายใน (ไม่ใช่รายได้)' : order.paymentMethod === 'account' ? '🏢 ' + accountPayText(order, config) : (order.paymentMethod === 'transfer' ? '💳 โอน' : '💵 เงินสด')}""",
    """{internal ? '🔧 งานภายใน (ไม่ใช่รายได้)' : <span data-pay-label>{payLabelOf(order, config)}</span>}""", 'receipt label')
rep("""<span>{order.paymentMethod === 'account' ? '🏢 ' + accountPayText(order, config) : order.paymentMethod === 'transfer' ? '💳 โอน' : '💵 เงินสด'}</span>""",
    """<span data-pay-label>{payLabelOf(order, config)}</span>""", 'detail label')
open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v179 applied')
