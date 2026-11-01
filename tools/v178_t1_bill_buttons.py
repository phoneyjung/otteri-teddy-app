#!/usr/bin/env python3
"""v178 — Teddy 1: ปุ่มบิลงานร้านแยกเป็นปุ่มเล็ก ๆ บนหน้าแรก (เจ้าของขอ 1 พ.ย. — กดแล้วเข้าแบบนั้นเลย ไม่ต้องจำไปเลือกในฟอร์ม)
- กล่อง '🔧 บิลงานร้าน · ไม่ใช่ลูกค้า · ไม่นับเป็นรายได้' + ปุ่มเล็ก 🧼 ล้างเครื่อง · 🔧 ซ่อม/ทดสอบ · 🪙 โทเคนแก้ปัญหา
- กดปุ่มไหน ฟอร์มเปิดเป็นแบบนั้นทันที (ชิปในฟอร์มยังสลับได้ถ้ากดผิด)
- ร้านที่แม่บ้านทำได้แบบเดียว (ล้างเครื่อง) / ล็อกอินเจ้าของ = ปุ่มเดิม · Teddy 2/Otteri (หน้าไทล์) ไม่เปลี่ยน
usage: python3 tools/v178_t1_bill_buttons.py index.html sw.js
"""
import re
import sys

IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read()
sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    assert n == count, f'{label}: found {n}, expected {count}'
    s = s.replace(old, new)


rep("window.APP_VERSION = 'v177-2026-11-01';", "window.APP_VERSION = 'v178-2026-11-01';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v177';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v177';", "const CACHE_NAME = 'plp-laundry-v178';")

# ชื่อสั้น + บรรทัดช่วยจำ ของปุ่มเล็ก
rep("""const maidBillTypes = (config) => maidInternalTypes(config).filter(t => t.id !== 'mine');
""", """const maidBillTypes = (config) => maidInternalTypes(config).filter(t => t.id !== 'mine');
// 🔘 v178 ปุ่มเล็กหน้าแรก: ชื่อสั้น + บรรทัดช่วยจำ
const BILL_BTN = { clean: ['ล้างเครื่อง', 'ทุก 7 วัน'], test: ['ซ่อม/ทดสอบ', 'ตอนช่างมา'], fix: ['โทเคนแก้ปัญหา', 'ใส่เหตุผล'] };
""", 'BILL_BTN')

# ปุ่มเดิม = ร้านที่มีแบบเดียว / ล็อกอินเจ้าของ · หลายแบบ = กล่องปุ่มเล็ก
rep("""      {menuOn(config, 'internal') && !T2H && <div className="px-5 mt-3">
        <button onClick={onInternalOrder}
          className="w-full rounded-2xl p-3 border-2 border-amber-400 bg-amber-50 active:scale-95 transition flex items-center gap-3">""",
    """      {menuOn(config, 'internal') && !T2H && maidBillTypes(config).length > 1 && !(currentStaff && currentStaff.isOwnerLogin) && (
        <div className="px-5 mt-3">
          <div data-maid-bills className="rounded-2xl p-3 border-2 border-amber-400 bg-amber-50">
            <p className="text-sm font-extrabold text-slate-900 mb-2">🔧 {tr(config, 'บิลงานร้าน')} <span className="text-xs font-bold text-amber-800">· {tr(config, 'ไม่ใช่ลูกค้า · ไม่นับเป็นรายได้')}</span></p>
            <div className={`grid gap-2 ${maidBillTypes(config).length >= 3 ? 'grid-cols-3' : 'grid-cols-2'}`}>
              {maidBillTypes(config).map(t => (
                <button key={t.id} data-bill={t.id} onClick={() => onInternalOrder(t.id)}
                  className="rounded-xl bg-white border border-amber-300 px-1.5 py-2.5 flex flex-col items-center gap-0.5 active:scale-95 transition min-w-0">
                  <span className="text-2xl leading-none">{t.emoji}</span>
                  <span className="text-xs font-extrabold text-slate-900 text-center leading-tight mt-1">{tr(config, (BILL_BTN[t.id] || [t.label])[0])}</span>
                  {BILL_BTN[t.id] && <span className="text-[10px] font-bold text-amber-700 text-center leading-tight">{tr(config, BILL_BTN[t.id][1])}</span>}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
      {menuOn(config, 'internal') && !T2H && !(maidBillTypes(config).length > 1 && !(currentStaff && currentStaff.isOwnerLogin)) && <div className="px-5 mt-3">
        <button onClick={onInternalOrder}
          className="w-full rounded-2xl p-3 border-2 border-amber-400 bg-amber-50 active:scale-95 transition flex items-center gap-3">""", 'home small bill buttons')

MM_NEW = {
    'บิลงานร้าน': 'ဆိုင်အလုပ် ဘောက်ချာ',
    'ไม่ใช่ลูกค้า · ไม่นับเป็นรายได้': 'ဖောက်သည် မဟုတ် · ဝင်ငွေ မရေတွက်',
    'ซ่อม/ทดสอบ': 'ပြင်/စမ်းသပ်',
    'ตอนช่างมา': 'စက်ပြင်ဆရာ လာချိန်',
    'ใส่เหตุผล': 'အကြောင်းပြချက် ထည့်',
}
start = s.index('const MM_DICT = {')
end = s.index('\n};\nfunction tr(config, th) {', start)
existing = set(re.findall(r"^  '((?:[^'\\]|\\.)*)':", s[start:end], re.M))
add = ''.join(f"  '{k}': '{v}', // v178\n" for k, v in MM_NEW.items() if k not in existing)
skipped = [k for k in MM_NEW if k in existing]
s = s[:end] + '\n' + add.rstrip('\n') + s[end:]

open(IDX, 'w', encoding='utf-8').write(s)
open(SW, 'w', encoding='utf-8').write(sw)
print('v178 applied · MM added', len(MM_NEW) - len(skipped), 'skipped', skipped)
