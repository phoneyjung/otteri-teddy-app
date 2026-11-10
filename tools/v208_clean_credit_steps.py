#!/usr/bin/env python3
"""v208 — โหมดตัดเครดิต (Teddy 2): ล้างเครื่องมีขั้นตอนตัดเครดิตที่ตู้ + ปุ่มโปรซักเองไม่มี ⚡
ที่มา: Claude เจอระหว่างถ่ายหน้าจอทำคลิปสอน EP.8 ล้างเครื่อง (10 พ.ย. 69)
  - งานล้างเครื่อง (งานภายใน ใช้เครดิตแม่บ้าน ฿80 น้ำร้อน) หน้าเลือกเครื่องขึ้นแค่ '🧼 ล้างเครื่อง · อย่าลืมกด 🔥 น้ำร้อน'
    ไม่มีขั้นตอน แตะราคา → Use Credit → สแกน → ใส่ยอด ทั้งในกล่องเหลืองและกล่องยืนยัน (งานลูกค้ามีตั้งแต่ v205)
  - ฟอร์ม 'บันทึกลูกค้าใช้โปร' ปุ่มยังเป็น '⚡ เริ่มเครื่อง + บันทึก' (คำ/ไอคอนยิงพัลส์เดิม)
ทำอะไร
  - หน้าเลือกเครื่อง งานล้างเครื่อง + โหมดเครดิต: ใต้แถบชมพูมีกล่อง 📝 ขั้นตอนที่ตู้ `[data-credit-steps]` แบบเดียวกับงานลูกค้า
  - กล่องยืนยันงานล้างเครื่อง + โหมดเครดิต: ต่อท้ายด้วยข้อขั้นตอนตัดเครดิต + 💳 + ✅ เครื่องเดินแล้ว กดตกลง
  - ปุ่มโปรซักเอง โหมดเครดิต: '🎟️ ตัดเครดิตที่ตู้ + บันทึก'
  - ร้านอื่น (SOL / EC เดิม) เหมือนเดิมทุกอย่าง
usage: python3 tools/v208_clean_credit_steps.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v207-2026-11-10';", "window.APP_VERSION = 'v208-2026-11-10';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v207';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v207';", "const CACHE_NAME = 'plp-laundry-v208';")

PROMO = '🎟️ ตัดเครดิตที่ตู้ + บันทึก'
CLEAN1 = 'ไม่ต้องใส่ผ้า ปิดประตู กด 🔥 น้ำร้อน ที่หน้าเครื่อง'
rep("""  'เครื่องเดินแล้ว กดตกลง': 'စက်လည်ပြီးမှ OK နှိပ်', // v205
""", f"""  'เครื่องเดินแล้ว กดตกลง': 'စက်လည်ပြီးမှ OK နှိပ်', // v205
  '{PROMO}': '🎟️ စက်တွင် ခရက်ဒစ်ဖြတ် + သိမ်း', // v208
  '{CLEAN1}': 'အဝတ်မထည့်ရ တံခါးပိတ် စက်ရှေ့တွင် 🔥 ရေပူ နှိပ်', // v208
""", 'MM')

# ---------- sheet: clean job + credit → steps box ----------
rep("""              <p className="text-sm font-extrabold text-rose-700 bg-rose-50 border-2 border-rose-200 rounded-xl px-3 py-2">🧼 {tr(config, 'ล้างเครื่อง (ไม่ต้องใส่ผ้า)')} · ⚠️ {tr(config, isSol(config) ? 'ใน SOL เลือก Hot (น้ำร้อน)' : 'อย่าลืมกดเลือก 🔥 น้ำร้อน ที่หน้าเครื่องก่อนกดตกลง')}</p>
            ) : (""",
    f"""              <div className="space-y-1.5">
                <p className="text-sm font-extrabold text-rose-700 bg-rose-50 border-2 border-rose-200 rounded-xl px-3 py-2">🧼 {{tr(config, 'ล้างเครื่อง (ไม่ต้องใส่ผ้า)')}} · ⚠️ {{tr(config, isSol(config) ? 'ใน SOL เลือก Hot (น้ำร้อน)' : 'อย่าลืมกดเลือก 🔥 น้ำร้อน ที่หน้าเครื่องก่อนกดตกลง')}}</p>
                {{isCredit(config) && ( // 🎟️ v208 ล้างเครื่องใช้เครดิตแม่บ้าน — ขั้นตอนที่ตู้เหมือนงานลูกค้า
                  <div className="rounded-xl px-3 py-2 border-2" style={{{{ background: '#FFFBEB', borderColor: '#F59E0B' }}}} data-credit-steps data-clean-steps>
                    <p className="text-xs font-extrabold text-slate-700">📝 {{tr(config, 'ขั้นตอนที่ตู้')}}</p>
                    <p className="text-[13px] font-bold text-slate-800 mt-0.5">1) {{tr(config, '{CLEAN1}')}}</p>
                    {{creditStepLines(config, creditPlan(config, {{ kind: selM.kind, kg: selM.kg, baht, coin: 0 }})).map((t, i) => (
                      <p key={{i}} className="text-[13px] font-bold text-slate-800 mt-0.5">{{i + 2}}) {{t}}</p>
                    ))}}
                    <p className="text-[12px] font-extrabold text-rose-700 mt-0.5" data-credit-low>💳 {{tr(config, CREDIT_LOW_TEXT)}}</p>
                    <p className="text-[13px] font-extrabold text-emerald-800 mt-0.5" data-credit-done>✅ {{tr(config, 'เครื่องเดินแล้ว กดปุ่ม 🎟️ ตัดเครดิตแล้ว ด้านล่าง')}}</p>
                  </div>
                )}}
              </div>
            ) : (""", 'sheet clean')

# ---------- confirm: clean job + credit ----------
rep("""  const steps = order && order.internalType === 'clean'
    ? `🧼 ${tr(config, 'ล้างเครื่อง (ไม่ต้องใส่ผ้า)')}\\n⚠️ ${tr(config, 'อย่าลืมกดเลือก 🔥 น้ำร้อน ที่หน้าเครื่องก่อนกดตกลง')}`""",
    f"""  const steps = order && order.internalType === 'clean'
    ? `🧼 ${{tr(config, 'ล้างเครื่อง (ไม่ต้องใส่ผ้า)')}}\\n⚠️ ${{tr(config, 'อย่าลืมกดเลือก 🔥 น้ำร้อน ที่หน้าเครื่องก่อนกดตกลง')}}${{cr && pulseBaht > 0 ? `\\n\\n✅ ${{tr(config, 'ก่อนกดตกลง')}}:\\n1) ${{tr(config, '{CLEAN1}')}}\\n${{creditStepLines(config, creditPlan(config, {{ kind, kg, baht, coin: 0 }})).map((t, i) => `${{i + 2}}) ${{t}}`).join('\\n')}}\\n💳 ${{tr(config, CREDIT_LOW_TEXT)}}\\n✅ ${{tr(config, 'เครื่องเดินแล้ว กดตกลง')}}` : ''}}`  // 🎟️ v208""", 'confirm clean')

# ---------- promo button ----------
rep("""tr(config, pulseOn(config) ? '⚡ เริ่มเครื่อง + บันทึก' : 'บันทึกตัดเครดิต')""",
    f"""tr(config, pulseOn(config) ? (isCredit(config) ? '{PROMO}' : '⚡ เริ่มเครื่อง + บันทึก') : 'บันทึกตัดเครดิต')""", 'promo btn')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v208 ok')
