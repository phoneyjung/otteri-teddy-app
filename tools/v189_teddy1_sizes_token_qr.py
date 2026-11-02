#!/usr/bin/env python3
"""v189 — Teddy 1: ขนาดเครื่องซักตามจริง + QR บัญชีร้านในฟอร์มแลก Token (โอน)
ที่มา: เจ้าของ 2 พ.ย. 69
  1) 'เปลี่ยนใหม่ เป็น 17kg ,13kg ,10kg,10kg,10kg,10kg' (ชิปเครื่องในฟอร์มล้างเครื่อง Teddy 1)
  2) ลูกค้าไม่มีเงินสด อยากเพิ่มเวลา → แม่บ้านหยอดโทเคนให้ → เลือก 'ทำ v189: QR ร้านในฟอร์ม'
  3) 'โทเคนแก้ปัญหา เปลี่ยนเป็น ใส่จำนวน token และบอกเหตุผล พอ ไม่ต้องเลือกเครื่อง'
ทำอะไร
  - Teddy 1 (+ โหมดฝึก): ซัก 1 = 17kg · ซัก 2 = 13kg · ซัก 3–6 = 10kg (เดิม ซัก 2 = 10kg, ซัก 6 = 13kg)
    ชิปเลือกเครื่อง (ล้างเครื่อง/ซ่อม/โทเคนแก้ปัญหา) ขึ้นขนาดด้วย เช่น 'ซัก 1 · 17kg' (เฉพาะร้านที่ตั้ง chipSize)
  - ฟอร์มแลก Token: เลือก 💳 โอน + ใส่ยอด → ขึ้น QR พร้อมเพย์บัญชีร้านพร้อมยอด ให้ลูกค้าสแกนเข้าร้านตรง
    (แม่บ้านไม่ต้องรับโอนเข้าบัญชีตัวเอง) · ดูสลิปก่อนให้โทเคน
  - ปุ่ม 🪙 แลก Token: '(ตู้แลกเหรียญเสีย)' → '(ตู้แลกเสีย / ไม่มีเงินสด)' (Teddy 1) · ไทล์ Teddy 2 เหมือนกัน
  - 🪙 โทเคนแก้ปัญหา (Teddy 1): ใส่จำนวนโทเคน (− / +) + เหตุผล พอ · ไม่มีชิปเครื่อง ไม่มีส่วนเครื่องซัก/อบ
    เก็บ internalCustom เป็นบาท (โทเคน × 10) เหมือนเดิม → รายงาน/ยอดเดิมใช้ได้ · บันทึก internalMachines/washItems/dryItems ว่าง
usage: python3 tools/v189_teddy1_sizes_token_qr.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v188-2026-11-02';", "window.APP_VERSION = 'v189-2026-11-02';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v188';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v188';", "const CACHE_NAME = 'plp-laundry-v189';")

# ---------- 1) Teddy 1 ขนาดเครื่องซัก ----------
rep("""    tokenMode: true, tokenValue: 10, unitName: 'โทเคน',
    machines: [
      { id: 'w1', label: 'ซัก 1', size: '17kg' },
      { id: 'w2', label: 'ซัก 2', size: '10kg' },
      { id: 'w3', label: 'ซัก 3', size: '10kg' },
      { id: 'w4', label: 'ซัก 4', size: '10kg' },
      { id: 'w5', label: 'ซัก 5', size: '10kg' },
      { id: 'w6', label: 'ซัก 6', size: '13kg' },""",
    """    tokenMode: true, tokenValue: 10, unitName: 'โทเคน',
    chipSize: true, // v189 ชิปเลือกเครื่องขึ้นขนาดด้วย (ซัก 1 · 17kg)
    machines: [ // v189 เจ้าของแก้: ซัก 1 = 17kg · ซัก 2 = 13kg · ซัก 3–6 = 10kg
      { id: 'w1', label: 'ซัก 1', size: '17kg' },
      { id: 'w2', label: 'ซัก 2', size: '13kg' },
      { id: 'w3', label: 'ซัก 3', size: '10kg' },
      { id: 'w4', label: 'ซัก 4', size: '10kg' },
      { id: 'w5', label: 'ซัก 5', size: '10kg' },
      { id: 'w6', label: 'ซัก 6', size: '10kg' },""", 'teddy sizes')
rep("""{m.label}{lock ? ` 🔒${until}` : ''}""",
    """{m.label}{(COIN_POINTS[config.brand] || {}).chipSize && m.size ? ` · ${m.size}` : ''}{lock ? ` 🔒${until}` : ''}""", 'chip size')

# ---------- 2) QR บัญชีร้านในฟอร์มแลก Token ----------
rep("""              {/* Teddy: 2 ช่อง — Token ของร้าน + เหรียญ 10 จริง */}""",
    """              {/* 💳 v189 เลือกโอน → QR บัญชีร้านพร้อมยอด · ลูกค้าโอนเข้าร้านตรง ไม่ผ่านบัญชีแม่บ้าน */}
              {tokenPayment === 'transfer' && amountNum > 0 && (() => {
                const qrSrc = buildPromptPayQr(config.brand, amountNum) || PAYMENT_QRS[config.brand] || null;
                if (!qrSrc) return null;
                return (
                  <div className="rounded-xl p-3 border-2 border-violet-300 bg-violet-50 flex items-center gap-3" data-token-qr>
                    <div className="bg-white p-1.5 rounded-lg border border-slate-200 flex-none">
                      <img src={qrSrc} alt="QR" style={{ width: '132px', height: '132px', display: 'block' }} />
                    </div>
                    <div className="min-w-0">
                      <p className="text-xs font-extrabold text-violet-800">📱 {tr(config, 'ให้ลูกค้าสแกนจ่ายเข้าบัญชีร้าน')}</p>
                      <p className="text-2xl font-extrabold text-slate-900 leading-tight">฿{formatMoney(amountNum)}</p>
                      <p className="text-[11px] text-slate-600">{PAYMENT_ACCOUNT_NAMES[config.brand] || ''}</p>
                      <p className="text-[11px] font-bold text-rose-600 mt-1">{tr(config, 'ดูสลิปว่าโอนสำเร็จก่อน แล้วค่อยให้ลูกค้า')}</p>
                    </div>
                  </div>
                );
              })()}

              {/* Teddy: 2 ช่อง — Token ของร้าน + เหรียญ 10 จริง */}""", 'token qr')

# ---------- 3) ปุ่ม/ไทล์แลก Token: บอกว่าใช้ตอนลูกค้าไม่มีเงินสดได้ ----------
rep(""": tr(config, 'ตู้แลกเสีย'),""", """: tr(config, 'ตู้แลกเสีย / ไม่มีเงินสด'), // v189""", 'tile sub (Teddy 2 หน้าแบบใหม่)')
rep("""{tr(config, exchangeName(config))} {tr(config, '(ตู้แลกเหรียญเสีย)')}""",
    """{tr(config, exchangeName(config))} {tr(config, '(ตู้แลกเสีย / ไม่มีเงินสด)')}""", 'button title (Teddy 1 หน้าเดิม)')

# ---------- 4) 🪙 โทเคนแก้ปัญหา: ใส่จำนวนโทเคน + เหตุผล พอ (ไม่ต้องเลือกเครื่อง) ----------
# เจ้าของ 2 พ.ย. 69: 'โทเคนแก้ปัญหา เปลี่ยนเป็น ใส่จำนวน token และบอกเหตุผล พอ ไม่ต้องเลือกเครื่อง'
rep("""            {(internalType !== 'mine' || simpleFree) && <React.Fragment>""",
    """            {(internalType !== 'mine' || simpleFree) && !fixType && <React.Fragment>""", 'fix: no machine chips')
rep("""        {!autoItems && <Section iconName="droplet" title={tr(config, "เครื่องซัก")}>""",
    """        {!autoItems && !fixType && <Section iconName="droplet" title={tr(config, "เครื่องซัก")}>""", 'fix: no wash section')
rep("""        {!autoItems && <Section iconName="wind" title={tr(config, "เครื่องอบ")}>""",
    """        {!autoItems && !fixType && <Section iconName="wind" title={tr(config, "เครื่องอบ")}>""", 'fix: no dry section')
rep("""                {!simpleFree && <React.Fragment>""",
    """                {!simpleFree && fixType && (() => { // 🪙 v189 ใส่เป็นจำนวนโทเคน (เก็บเป็นบาท = โทเคน × ราคาโทเคน เหมือนเดิม)
                  const tv = (COIN_POINTS[config.brand] || {}).tokenValue || 10;
                  const qty = customAmt > 0 ? Math.round(customAmt / tv) : 0;
                  const setQty = (n) => setInternalCustom(n > 0 ? String(n * tv) : '');
                  return (
                    <React.Fragment>
                      <p className="text-xs font-bold text-slate-700 mb-1 mt-3">{tr(config, 'จำนวนโทเคนที่ให้')} <span className="text-rose-600">*{tr(config, 'บังคับ')}</span></p>
                      <div className="flex items-center gap-2" data-itoken>
                        <button type="button" onClick={() => setQty(Math.max(0, qty - 1))} data-itoken-minus className="w-11 h-11 rounded-full bg-white border-2 border-slate-300 text-xl font-extrabold text-slate-700 active:scale-90">−</button>
                        <input type="number" inputMode="numeric" value={qty > 0 ? String(qty) : ''} onChange={e => setQty(Math.max(0, parseInt(e.target.value, 10) || 0))} onFocus={e => e.target.select()} data-icustom
                          className="flex-1 min-w-0 px-3 py-2.5 rounded-xl border-2 border-slate-300 bg-white text-lg font-bold text-center" placeholder="0" />
                        <button type="button" onClick={() => setQty(qty + 1)} data-itoken-plus className="w-11 h-11 rounded-full bg-amber-500 text-white text-xl font-extrabold active:scale-90">+</button>
                        <span className="text-sm font-extrabold text-slate-700">🪙 {tr(config, 'โทเคน')}</span>
                      </div>
                      {qty > 0 && <p className="text-xs font-extrabold text-slate-800 mt-1">= ฿{formatMoney(customAmt)}</p>}
                    </React.Fragment>
                  );
                })()}
                {!simpleFree && !fixType && <React.Fragment>""", 'fix: token count input')
rep("""if (!freeOk) { setWashItems([]); setDryItems([]); } } setInternalType(t.id); }}""",
    """if (!freeOk) { setWashItems([]); setDryItems([]); } } if (t.id !== internalType && (t.id === 'fix' || internalType === 'fix')) setInternalCustom(''); setInternalType(t.id); }}""", 'fix: clear amount when switching type') # ยอดโทเคนแก้ปัญหาไม่ติดไปงานอื่น (และกลับกัน)
rep("""      washItems: washItems || [],
      dryItems: dryItems || [],""",
    """      washItems: fixType ? [] : (washItems || []), // 🪙 v189 โทเคนแก้ปัญหา = จำนวนโทเคน + เหตุผล ไม่มีเครื่อง
      dryItems: fixType ? [] : (dryItems || []),""", 'fix: save no items')
rep("""      internalMachines: internalType || simpleAcct ? internalMachines : null,""",
    """      internalMachines: internalType || simpleAcct ? (fixType ? [] : internalMachines) : null,""", 'fix: save no machines')

# ---------- MM ----------
rep("""  'ตู้แลกเสีย': 'အကြွေလဲစက် ပျက်',""",
    """  'ตู้แลกเสีย': 'အကြွေလဲစက် ပျက်',
  'ตู้แลกเสีย / ไม่มีเงินสด': 'အကြွေလဲစက် ပျက် / ငွေသားမရှိ', // v189
  'ให้ลูกค้าสแกนจ่ายเข้าบัญชีร้าน': 'ဖောက်သည်ကို ဆိုင်အကောင့်သို့ စကင်ဖတ်ပြီး ပေးချေခိုင်းပါ', // v189
  'ดูสลิปว่าโอนสำเร็จก่อน แล้วค่อยให้ลูกค้า': 'လွှဲပြီးကြောင်း စလစ်ကို အရင်ကြည့်ပြီးမှ ဖောက်သည်ကို ပေးပါ', // v189
  'จำนวนโทเคนที่ให้': 'ပေးသော တိုကင် အရေအတွက်', // v189
  '(ตู้แลกเสีย / ไม่มีเงินสด)': '(အကြွေလဲစက် ပျက် / ငွေသားမရှိ)', // v189""", 'MM')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v189 applied')
