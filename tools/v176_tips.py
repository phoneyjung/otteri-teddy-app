#!/usr/bin/env python3
"""v176 — 💝 ทิปที่ลูกค้าโอนเกิน (เฉพาะ Otteri · config.transferTip)
เจ้าของ (1 พ.ย.): ทิปเงินสด แม่บ้านเก็บเองไม่ต้องลง · ลูกค้าโอนเกินยอด = ทิป ต้องลงตอนทำใบงาน · เจ้าของจ่ายรวมเงินเดือนวันที่ 1
- ฟอร์มรับงาน (จ่ายโอน / สด+โอน): ช่อง 'ลูกค้าโอนเกิน = ทิป' → order.tip (บาท) + order.tipBy (แม่บ้านที่ลง)
- ทิปไม่รวมในยอดงาน (calculateTotal ไม่เปลี่ยน) · ไม่นับเป็นรายได้ · ไม่อยู่ในเงินสดในมือ
- ใบรับงาน: แถว '💝 ทิป ฿… · ขอบคุณค่ะ'
- หน้าเจ้าของ → เงิน → โอน: กล่องทิปแม่บ้านรายคนตามช่วงเวลา (เลือกรายเดือนเพื่อจ่ายวันที่ 1) + บอกยอดที่จะเกินในบัญชีของใบโอนที่ยังไม่เคลียร์
- Excel รายเดือน: คอลัมน์ 'ทิป (โอนเกิน)' ท้ายชีตรายการงาน + ชีต 'ทิปแม่บ้าน' (เฉพาะร้านที่เปิดทิป)
usage: python3 tools/v176_tips.py index.html sw.js
"""
import sys

IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read()
sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    assert n == count, f'{label}: found {n}, expected {count}'
    s = s.replace(old, new)


rep("window.APP_VERSION = 'v175-2026-11-01';", "window.APP_VERSION = 'v176-2026-11-01';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v175';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v175';", "const CACHE_NAME = 'plp-laundry-v176';")

# ---------- config ----------
rep("  defaultPay: 'transfer', // ให้แม่บ้านถือเงินสดน้อยที่สุด",
    "  defaultPay: 'transfer', // ให้แม่บ้านถือเงินสดน้อยที่สุด\n  transferTip: true, // 💝 v176 ลูกค้าโอนเกิน = ทิปของแม่บ้าน (จ่ายรวมเงินเดือนวันที่ 1) · ทิปเงินสดไม่ต้องลง", 'otteri transferTip')

# ---------- MM ----------
rep("  'ใบรายงานนี้ส่งเข้ากลุ่ม ไม่ต้องส่งลูกค้า':",
    """  // 💝 v176 ทิป (Otteri) — รอพนักงานพม่าตรวจคำแปล
  'ลูกค้าโอนเกิน = ทิป': 'ဖောက်သည် ပိုလွှဲ = ဘောက်ဆူး',
  'ทิป': 'ဘောက်ဆူး',
  'ลูกค้าโอนรวม': 'ဖောက်သည် လွှဲစုစုပေါင်း',
  'ทิปเป็นของแม่บ้าน จ่ายรวมเงินเดือนวันที่ 1 · ทิปเงินสดไม่ต้องลง': 'ဘောက်ဆူးသည် ဝန်ထမ်းအတွက် · ၁ ရက်နေ့ လစာနှင့်အတူ ပေးမည် · ငွေသား ဘောက်ဆူး မှတ်ရန်မလို',
  'ใบรายงานนี้ส่งเข้ากลุ่ม ไม่ต้องส่งลูกค้า':""", 'MM words')

# ---------- ฟอร์มรับงาน ----------
rep("  const [splitTransfer, setSplitTransfer] = useState(seed?.transferAmount != null ? String(seed.transferAmount) : '');",
    "  const [splitTransfer, setSplitTransfer] = useState(seed?.transferAmount != null ? String(seed.transferAmount) : '');\n  const [tipAmt, setTipAmt] = useState(seed?.tip ? String(seed.tip) : ''); // 💝 v176",
    'tip state')
rep("note, deliveryZone, riderId, fromKev, fromLine, useLinePromo, pickupTime, hadPhoto: !!basketPhoto, accountId: accountId || null });\n  }, [name, phone, clothCount, washItems, dryItems, detergentQty, softenerQty, foldBaskets, noFold, paymentMethod, splitCash, splitTransfer, note, deliveryZone, riderId, fromKev, fromLine, useLinePromo, pickupTime, basketPhoto, accountId]);",
    "note, deliveryZone, riderId, fromKev, fromLine, useLinePromo, pickupTime, hadPhoto: !!basketPhoto, accountId: accountId || null, tip: tipAmt === '' ? null : Number(tipAmt) });\n  }, [name, phone, clothCount, washItems, dryItems, detergentQty, softenerQty, foldBaskets, noFold, paymentMethod, splitCash, splitTransfer, note, deliveryZone, riderId, fromKev, fromLine, useLinePromo, pickupTime, basketPhoto, accountId, tipAmt]);",
    'tip in draft')
rep("  const breakdown = calculateBreakdown(tempOrder, config);\n",
    "  const breakdown = calculateBreakdown(tempOrder, config);\n  const tipNum = parseInt(tipAmt, 10) || 0; // 💝 v176\n",
    'tipNum')
rep("\n          <div className={`rounded-2xl p-4 border ${paymentMethod === 'transfer' ? 'bg-gradient-to-br from-violet-50 to-purple-50 border-violet-200'",
    """
          {/* 💝 v176 ลูกค้าโอนเกิน = ทิปของแม่บ้าน (Otteri) · ทิปเงินสดไม่ต้องลง */}
          {config.transferTip && (paymentMethod === 'transfer' || paymentMethod === 'split') && (
            <div data-tip-box className="rounded-2xl px-3 py-2.5 border border-pink-200 bg-pink-50">
              <div className="flex items-center gap-2">
                <span className="flex-1 text-sm font-extrabold text-pink-800">💝 {tr(config, 'ลูกค้าโอนเกิน = ทิป')}</span>
                <span className="text-sm font-bold text-pink-700">฿</span>
                <input type="number" inputMode="numeric" value={tipAmt} onChange={e => setTipAmt(e.target.value.replace(/[^\\d]/g, ''))} placeholder="0" aria-label={tr(config, 'ทิป')}
                  className="w-24 px-3 py-2 bg-white rounded-xl border-2 border-pink-200 focus:border-pink-400 outline-none text-lg font-bold text-pink-700 text-right" />
              </div>
              <p className="text-[11px] text-pink-700 mt-1">{tipNum > 0 ? `${tr(config, 'ลูกค้าโอนรวม')} ฿${formatMoney((paymentMethod === 'split' ? (parseFloat(splitTransfer) || 0) : total) + tipNum)} · ` : ''}{tr(config, 'ทิปเป็นของแม่บ้าน จ่ายรวมเงินเดือนวันที่ 1 · ทิปเงินสดไม่ต้องลง')}</p>
            </div>
          )}

          <div className={`rounded-2xl p-4 border ${paymentMethod === 'transfer' ? 'bg-gradient-to-br from-violet-50 to-purple-50 border-violet-200'""", 'tip box')
rep("      transferAmount: !acct && paymentMethod === 'split' ? splitTransferNum : null,\n",
    """      transferAmount: !acct && paymentMethod === 'split' ? splitTransferNum : null,
      // 💝 v176 ทิป (ลูกค้าโอนเกิน) — ไม่รวมในยอดงาน
      tip: config.transferTip && !internalType && !acct && (paymentMethod === 'transfer' || paymentMethod === 'split') && tipNum > 0 ? tipNum : null,
      tipBy: config.transferTip && !internalType && !acct && (paymentMethod === 'transfer' || paymentMethod === 'split') && tipNum > 0 ? ((editingOrder && editingOrder.tipBy) || ((currentStaffLS(config) || {}).name) || '') : null,
""", 'tip saved')

# ---------- ใบรับงาน ----------
rep("""              {order.deliveryZone && (
                <div className="col-span-2">
                  <p className="text-xs text-slate-500">บริการ Delivery</p>""",
    """              {order.tip > 0 && (
                <div className="col-span-2" data-tip-line>
                  <p className="text-xs text-slate-500">ทิป (ลูกค้าโอนเกิน)</p>
                  <p className="font-bold text-sm" style={{ color: '#BE185D' }}>💝 ฿{formatMoney(order.tip)} · ขอบคุณค่ะ 🙏</p>
                </div>
              )}
              {order.deliveryZone && (
                <div className="col-span-2">
                  <p className="text-xs text-slate-500">บริการ Delivery</p>""", 'receipt tip line', count=1)

# ---------- หน้าเจ้าของ → โอน ----------
rep("            {history(m => m === 'transfer', 'transfer')}",
    """            {history(m => m === 'transfer', 'transfer')}
            {config.transferTip && (() => { // 💝 v176 ทิปแม่บ้าน (ลูกค้าโอนเกิน) — จ่ายรวมเงินเดือนวันที่ 1
              const tl = A.list.filter(o => (o.tip || 0) > 0);
              const by = {}; tl.forEach(o => { const k = o.tipBy || o.staffName || '-'; by[k] = (by[k] || 0) + (o.tip || 0); });
              const sum = tl.reduce((a, o) => a + (o.tip || 0), 0);
              const pend = trPendList.reduce((a, o) => a + (o.tip || 0), 0);
              return (
                <T2Box k="transfer" title={`💝 ทิปแม่บ้าน · ${R.label}`} right={<span className="text-xs font-bold text-slate-500">จ่ายรวมเงินเดือนวันที่ 1</span>}>
                  <div data-tip-owner>
                    {sum > 0 ? (
                      <div className="divide-y divide-slate-100">
                        {Object.entries(by).sort((a, b) => b[1] - a[1]).map(([n, v]) => (
                          <div key={n} className="flex items-center justify-between py-2">
                            <span className="text-sm font-bold text-slate-800">{n}</span>
                            <span className="text-sm font-extrabold tabular-nums" style={{ color: '#BE185D' }}>฿{formatMoney(v)}</span>
                          </div>
                        ))}
                        <div className="flex items-center justify-between pt-2">
                          <span className="text-sm font-extrabold text-slate-900">รวม {tl.length} ใบ</span>
                          <span className="text-base font-extrabold tabular-nums" style={{ color: '#BE185D' }}>฿{formatMoney(sum)}</span>
                        </div>
                      </div>
                    ) : <p className="text-sm text-slate-500">ไม่มีทิปใน{R.label}</p>}
                    <p className="text-xs text-slate-500 mt-1.5">ลูกค้าโอนเกินยอด = ทิป · ไม่นับเป็นรายได้ร้าน{pend > 0 ? ` · ใบโอนที่ยังไม่เคลียร์ ในบัญชีจะเกินอีก ฿${formatMoney(pend)} (ทิป)` : ''}</p>
                  </div>
                </T2Box>
              );
            })()}""", 'owner tip box')

# ---------- Excel ----------
rep("'ส่วนลดคูปอง', 'ส่วนลดโปร', 'เก็บเงินแล้ว', 'หมายเหตุ']];",
    "'ส่วนลดคูปอง', 'ส่วนลดโปร', 'เก็บเงินแล้ว', 'หมายเหตุ'].concat(config.transferTip ? ['ทิป (โอนเกิน)', 'ทิปของ'] : [])];", 'excel header')
rep("      x.lineDiscount, x.promoDiscount, o.collected ? 'เก็บแล้ว' : 'รอเก็บ', o.note || '',\n    ]);",
    "      x.lineDiscount, x.promoDiscount, o.collected ? 'เก็บแล้ว' : 'รอเก็บ', o.note || '',\n    ].concat(config.transferTip ? [o.tip || 0, o.tip > 0 ? (o.tipBy || o.staffName || '') : ''] : []));", 'excel row')
rep("  window.XLSX.utils.book_append_sheet(wb, window.XLSX.utils.aoa_to_sheet(sheetOrders), 'รายการงาน');\n",
    """  window.XLSX.utils.book_append_sheet(wb, window.XLSX.utils.aoa_to_sheet(sheetOrders), 'รายการงาน');
  if (config.transferTip) { // 💝 v176 ทิปแม่บ้าน (ลูกค้าโอนเกิน) — จ่ายรวมเงินเดือนวันที่ 1
    const by = {}; inMonth.filter(o => o.tip > 0).forEach(o => { const k = o.tipBy || o.staffName || '-'; (by[k] = by[k] || { n: 0, sum: 0 }); by[k].n++; by[k].sum += o.tip; });
    const sheetTips = [['ทิปแม่บ้าน (ลูกค้าโอนเกิน)', label], [], ['แม่บ้าน', 'จำนวนใบ', 'ทิปรวม']];
    Object.keys(by).sort().forEach(k => sheetTips.push([k, by[k].n, by[k].sum]));
    sheetTips.push(['รวม', Object.values(by).reduce((a, v) => a + v.n, 0), Object.values(by).reduce((a, v) => a + v.sum, 0)]);
    window.XLSX.utils.book_append_sheet(wb, window.XLSX.utils.aoa_to_sheet(sheetTips), 'ทิปแม่บ้าน');
  }
""", 'excel tips sheet')

open(IDX, 'w', encoding='utf-8').write(s)
open(SW, 'w', encoding='utf-8').write(sw)
print('v176 applied')
