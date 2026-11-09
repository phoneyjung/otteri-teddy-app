#!/usr/bin/env python3
"""v206 — โหมดตัดเครดิต (Teddy 2): เตือนแม่บ้านดูเครดิตที่เหลือ ต่ำกว่า 1,000 → บอกเจ้าของร้านเติม
ที่มา: เจ้าของรีวิวคลิปสอน EP.3 (9 พ.ย. 69) 'เครดิตหมด ต้องบอกให้เจ้าของร้านเติมให้ ควรบอกเมื่อเครดิตเหลือต่ำกว่า 1000'
        + ตอบ 'ให้แอปเตือนแม่บ้านด้วยไหม' = 'เพิ่มในแอปด้วย'
ทำอะไร
  - CREDIT_LOW_TEXT ใช้ที่เดียว: กล่อง 📝 ขั้นตอนที่ตู้ (หน้าเลือกเครื่อง) บรรทัดสีแดง `[data-credit-low]` ก่อนบรรทัด ✅
  - กล่องยืนยันตัดเครดิต (ใบงาน + โปรซักเอง) มีบรรทัด 💳 เดียวกันก่อน ✅ เครื่องเดินแล้ว กดตกลง
  - MM_DICT: คำแปลพม่า (รอแม่บ้านที่อ่านพม่าตรวจ เหมือน v204/v205)
  - แอปไม่ได้อ่านยอดเครดิตเอง (แอปไม่เข้าเว็บ EC) — เป็นข้อความเตือนให้แม่บ้านดูในหน้า Amount to pay
usage: python3 tools/v206_credit_low.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v205-2026-11-08';", "window.APP_VERSION = 'v206-2026-11-10';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v205';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v205';", "const CACHE_NAME = 'plp-laundry-v206';")

LOW = 'ดูเครดิตที่เหลือ (Available credits) ต่ำกว่า 1,000 → บอกเจ้าของร้านเติม'

# ---------- MM ----------
rep("""  'เครื่องเดินแล้ว กดตกลง': 'စက်လည်ပြီးမှ OK နှိပ်', // v205
""", f"""  'เครื่องเดินแล้ว กดตกลง': 'စက်လည်ပြီးမှ OK နှိပ်', // v205
  '{LOW}': 'ကျန်ခရက်ဒစ် (Available credits) ကြည့်ပါ — 1,000 အောက်ဆိုရင် ဆိုင်ရှင်ကို ဖြည့်ခိုင်းပါ', // v206
""", 'MM')

# ---------- constant ----------
rep("const CREDIT_WORDS = {", f"const CREDIT_LOW_TEXT = '{LOW}'; // 💳 v206 เจ้าของ: ต่ำกว่า 1,000 บอกเจ้าของเติม\nconst CREDIT_WORDS = {{", 'const')

# ---------- steps box ----------
rep("""                    <p className="text-[13px] font-extrabold text-emerald-800 mt-0.5">✅ {tr(config, 'เครื่องเดินแล้ว กดปุ่ม 🎟️ ตัดเครดิตแล้ว ด้านล่าง')}</p>""",
    """                    <p className="text-[12px] font-extrabold text-rose-700 mt-0.5" data-credit-low>💳 {tr(config, CREDIT_LOW_TEXT)}</p>
                    <p className="text-[13px] font-extrabold text-emerald-800 mt-0.5">✅ {tr(config, 'เครื่องเดินแล้ว กดปุ่ม 🎟️ ตัดเครดิตแล้ว ด้านล่าง')}</p>""", 'steps box')

# ---------- confirms ----------
rep("""coin: 0 })).map((t, i) => `${i + 1}) ${t}`).join('\\n')}\\n✅ ${tr(config, 'เครื่องเดินแล้ว กดตกลง')}`""",
    """coin: 0 })).map((t, i) => `${i + 1}) ${t}`).join('\\n')}\\n💳 ${tr(config, CREDIT_LOW_TEXT)}\\n✅ ${tr(config, 'เครื่องเดินแล้ว กดตกลง')}`""", 'promo confirm')
rep("""baht, coin })).map((t, i) => `${i + 3}) ${t}`).join('\\n')}\\n✅ ${tr(config, 'เครื่องเดินแล้ว กดตกลง')}`""",
    """baht, coin })).map((t, i) => `${i + 3}) ${t}`).join('\\n')}\\n💳 ${tr(config, CREDIT_LOW_TEXT)}\\n✅ ${tr(config, 'เครื่องเดินแล้ว กดตกลง')}`""", 'start confirm')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v206 ok')
