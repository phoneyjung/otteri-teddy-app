#!/usr/bin/env python3
"""v207 — โหมดตัดเครดิต (Teddy 2): กล่อง 📝 ขั้นตอนที่ตู้ ของใบงานเงินสด/สด+โอน บอกปุ่มให้ตรง
ที่มา: Claude เจอระหว่างถ่ายหน้าจอทำคลิปสอน EP.4 (10 พ.ย. 69)
  - ใบงานเงินสดล้วน: กล่องขึ้น '💳 ดูเครดิตที่เหลือ…' (v206) ทั้งที่ไม่ได้ใช้เครดิต และ '✅ … กดปุ่ม 🎟️ ตัดเครดิตแล้ว'
    แต่ปุ่มด้านล่างคือ '💵 หยอดที่เครื่องแล้ว · บันทึก'
  - สด+โอน: '✅ … กดปุ่ม 🎟️ ตัดเครดิตแล้ว' แต่ปุ่มคือ '💵 ฿40 + 🎟️ ฿20 · เริ่มเครื่อง'
ทำอะไร
  - 💳 ขึ้นเฉพาะเมื่อมีรอบที่ตัดเครดิต
  - ✅ บรรทัดสุดท้ายตามชนิด: เครดิตล้วน = 🎟️ ตัดเครดิตแล้ว · เงินสดล้วน = 💵 หยอดที่เครื่องแล้ว · สด+เครดิต = 💵+🎟️ เริ่มเครื่อง
  - MM_DICT 2 คำใหม่ (รอตรวจ)
usage: python3 tools/v207_cash_steps_fix.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v206-2026-11-10';", "window.APP_VERSION = 'v207-2026-11-10';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v206';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v206';", "const CACHE_NAME = 'plp-laundry-v207';")

CASH = 'เครื่องเดินแล้ว กดปุ่ม 💵 หยอดที่เครื่องแล้ว ด้านล่าง'
MIX = 'เครื่องเดินแล้ว กดปุ่ม 💵+🎟️ เริ่มเครื่อง ด้านล่าง'
rep("""  'เครื่องเดินแล้ว กดตกลง': 'စက်လည်ပြီးမှ OK နှိပ်', // v205
""", f"""  'เครื่องเดินแล้ว กดตกลง': 'စက်လည်ပြီးမှ OK နှိပ်', // v205
  '{CASH}': 'စက်လည်ပြီးမှ အောက်က 💵 စက်တွင်ထည့်ပြီး ခလုတ်နှိပ်', // v207
  '{MIX}': 'စက်လည်ပြီးမှ အောက်က 💵+🎟️ စက်စတင် ခလုတ်နှိပ်', // v207
""", 'MM')

rep("""                    {creditStepLines(config, creditPlan(config, { kind: selM.kind, kg: selM.kg, baht, coin: cp.coin })).map((t, i) => (
                      <p key={i} className="text-[13px] font-bold text-slate-800 mt-0.5">{i + 2}) {t}</p>
                    ))}
                    <p className="text-[12px] font-extrabold text-rose-700 mt-0.5" data-credit-low>💳 {tr(config, CREDIT_LOW_TEXT)}</p>
                    <p className="text-[13px] font-extrabold text-emerald-800 mt-0.5">✅ {tr(config, 'เครื่องเดินแล้ว กดปุ่ม 🎟️ ตัดเครดิตแล้ว ด้านล่าง')}</p>""",
    f"""                    {{(() => {{ // 💵 v207 ใบงานเงินสด/สด+โอน: 💳 เฉพาะตอนใช้เครดิต · ✅ บอกปุ่มให้ตรง
                      const rounds = creditPlan(config, {{ kind: selM.kind, kg: selM.kg, baht, coin: cp.coin }});
                      const useCredit = rounds.some(r => r.pay > 0), useCoin = rounds.some(r => r.coin > 0);
                      return (<>
                        {{creditStepLines(config, rounds).map((t, i) => (
                          <p key={{i}} className="text-[13px] font-bold text-slate-800 mt-0.5">{{i + 2}}) {{t}}</p>
                        ))}}
                        {{useCredit && <p className="text-[12px] font-extrabold text-rose-700 mt-0.5" data-credit-low>💳 {{tr(config, CREDIT_LOW_TEXT)}}</p>}}
                        <p className="text-[13px] font-extrabold text-emerald-800 mt-0.5" data-credit-done>✅ {{tr(config, !useCredit ? '{CASH}' : useCoin ? '{MIX}' : 'เครื่องเดินแล้ว กดปุ่ม 🎟️ ตัดเครดิตแล้ว ด้านล่าง')}}</p>
                      </>);
                    }})()}}""", 'steps box')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v207 ok')
