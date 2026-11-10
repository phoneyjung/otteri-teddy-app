#!/usr/bin/env python3
"""v209 — โหมดตัดเครดิต (Teddy 2): โปรซักเอง (ลูกค้าไม่ฝาก) บอกขั้นตอนที่ตู้ให้ถูก
ที่มา: เจ้าของ 10 พ.ย. 69 (ตอนทำคลิปสอน EP.9) ตอบว่า โปรลด 50 แต่เครื่อง 60–80 =
  'ลูกค้าหยอดส่วนที่เหลือก่อน → แม่บ้านตัดเครดิต 50'
เดิม (v205) กล่องยืนยันโปรบอก 'แตะ ฿50 ที่จอกล่อง → … → ใส่ 50' ซึ่งไม่ตรงราคาโปรแกรม (ซัก 50/60/70/80)
ทำอะไร
  - กล่องยืนยันโปร โหมดเครดิต: 1) ลูกค้าเลือกโปรแกรม แล้วหยอดเหรียญส่วนที่เหลือเอง (ถ้ามี)
    2) แตะราคาโปรแกรมที่จอกล่อง → Use Credit → สแกน → ล็อกอินเบอร์+รหัสของตัวเอง → ใส่ <ยอดโปร> → Use credit · 💳 · ✅
  - ฟอร์มโปร โหมดเครดิต: กล่อง 📝 ขั้นตอนที่ตู้ `[data-promo-steps]` เหนือปุ่ม (ข้อเดียวกัน ยอดตามช่องยอดโปร)
  - ใบรายงานโปร + ข้อความแชร์ โหมดเครดิต: '🎟️ ตัดเครดิตแล้ว' (เดิม '⚡ ส่งคำสั่งแล้ว')
  - ร้านอื่นเหมือนเดิม · MM_DICT 2 คำ (รอตรวจ)
usage: python3 tools/v209_promo_credit_steps.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v208-2026-11-10';", "window.APP_VERSION = 'v209-2026-11-10';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v208';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v208';", "const CACHE_NAME = 'plp-laundry-v209';")

P1 = 'ลูกค้าเลือกโปรแกรม แล้วหยอดเหรียญส่วนที่เหลือเอง (ถ้ามี)'
P2 = 'แตะราคาโปรแกรมที่จอกล่อง'
rep("""  'เครื่องเดินแล้ว กดตกลง': 'စက်လည်ပြီးမှ OK နှိပ်', // v205
""", f"""  'เครื่องเดินแล้ว กดตกลง': 'စက်လည်ပြီးမှ OK နှိပ်', // v205
  '{P1}': 'ဖောက်သည်က ပရိုဂရမ်ရွေးပြီး ကျန်ငွေကို အကြွေစေ့ ကိုယ်တိုင်ထည့် (ရှိလျှင်)', // v209
  '{P2}': 'ဘေးဘူးမျက်နှာပြင်တွင် ပရိုဂရမ်ဈေးနှုန်းကို နှိပ်', // v209
""", 'MM')

# helper next to creditStepLines
rep("function creditStepLines(config, rounds) {",
    f"""// 🎁 v209 โปรซักเอง: ลูกค้าหยอดส่วนที่เหลือก่อน แล้วแม่บ้านตัดเครดิตเท่ายอดโปร (เจ้าของ 10 พ.ย. 69)
function promoCreditLines(config, amount) {{
  return [tr(config, '{P1}'),
    `${{tr(config, '{P2}')}} → Use Credit → ${{tr(config, 'สแกน')}} → ${{tr(config, 'ล็อกอินเบอร์+รหัสของตัวเอง')}} → ${{tr(config, 'ใส่')}} ${{amount}} → Use credit`];
}}
function creditStepLines(config, rounds) {{""", 'helper')

# confirm
rep("""\\n🎁 ${promoName || 'ส่วนลด'}\\n\\n${creditStepLines(config, creditPlan(config, { kind: pulseMachine.kind, kg: pulseMachine.kg, baht: amount, coin: 0 })).map((t, i) => `${i + 1}) ${t}`).join('\\n')}""",
    """\\n🎁 ${promoName || 'ส่วนลด'}\\n\\n${promoCreditLines(config, amount).map((t, i) => `${i + 1}) ${t}`).join('\\n')}""", 'promo confirm')

# form steps box above the main button
rep("""            <button onClick={handleSubmitPromo} disabled={savingPromo}
              className="w-full py-3.5 rounded-2xl bg-rose-500 text-white font-bold text-base active:scale-95 transition disabled:opacity-50">""",
    """            {pulseOn(config) && isCredit(config) && ( // 🎁 v209 ขั้นตอนที่ตู้ของโปรซักเอง
              <div className="rounded-xl px-3 py-2 border-2" style={{ background: '#FFFBEB', borderColor: '#F59E0B' }} data-promo-steps>
                <p className="text-xs font-extrabold text-slate-700">📝 {tr(config, 'ขั้นตอนที่ตู้')}</p>
                {promoCreditLines(config, parseInt(promoAmount, 10) || 0).map((t, i) => (
                  <p key={i} className="text-[13px] font-bold text-slate-800 mt-0.5">{i + 1}) {t}</p>
                ))}
                <p className="text-[12px] font-extrabold text-rose-700 mt-0.5">💳 {tr(config, CREDIT_LOW_TEXT)}</p>
              </div>
            )}
            <button onClick={handleSubmitPromo} disabled={savingPromo}
              className="w-full py-3.5 rounded-2xl bg-rose-500 text-white font-bold text-base active:scale-95 transition disabled:opacity-50">""", 'promo form box')

# report card + share text: credit mode says 🎟️ ตัดเครดิตแล้ว (เดิม ⚡ ส่งคำสั่งแล้ว)
rep("""savedPromo.pulseLogId ? ['เริ่มเครื่อง', savedPromo.pulseStatus === 'confirmed' ? '⚡ เครื่องรับแล้ว' : '⚡ ส่งคำสั่งแล้ว']""",
    """savedPromo.pulseLogId ? ['เริ่มเครื่อง', savedPromo.pulseStatus === 'credit' ? '🎟️ ตัดเครดิตแล้ว' : savedPromo.pulseStatus === 'confirmed' ? '⚡ เครื่องรับแล้ว' : '⚡ ส่งคำสั่งแล้ว']""", 'report row')
rep("""savedPromo.pulseLogId ? `⚡ ยิงพัลส์: ${savedPromo.amount}฿ (${savedPromo.pulseStatus === 'confirmed' ? 'เครื่องรับแล้ว' : 'ส่งคำสั่งแล้ว'})`""",
    """savedPromo.pulseLogId ? (savedPromo.pulseStatus === 'credit' ? `🎟️ ตัดเครดิต: ${savedPromo.amount}฿` : `⚡ ยิงพัลส์: ${savedPromo.amount}฿ (${savedPromo.pulseStatus === 'confirmed' ? 'เครื่องรับแล้ว' : 'ส่งคำสั่งแล้ว'})`)""", 'share text')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v209 ok')
