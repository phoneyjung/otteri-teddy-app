#!/usr/bin/env python3
"""v200 — งานภายใน ซ่อม/ทดสอบ/อื่นๆ: เลือกเครื่อง + ใส่ยอดเอง พอ (ไม่ต้องเลือกซัก/อบด้านล่าง)
ที่มา: เจ้าของ 6 พ.ย. 69 'จริงๆ เลือกเครื่อง และใส่จำนวนเงินก็พอแล้ว ไม่ต้องคำนวณให้
       เพราะบางครั้งอาจจะทดสอบแบบหยอดเดิน หรือหยอดไม่ครบก็ได้'
ทำอะไร (ฟอร์มเต็ม · ประเภท ซ่อม/ทดสอบเครื่อง และ อื่นๆ · ไม่รวม ล้างเครื่อง/ซักซ้ำ/ผ้าเจ้าของ/โทเคนแก้ปัญหา)
  - ซ่อนส่วน 'เครื่องซัก' / 'เครื่องอบ' ด้านล่าง · บันทึก washItems/dryItems ว่าง (กันรายการค้างจากประเภทอื่น)
  - ช่องยอด = 'ยอดเครดิตที่ใช้ (บาท) *บังคับ' (Teddy 1 = ยอดโทเคนที่หยอด) กรอบชมพูตอนว่าง · ใส่ตามจริง หยอดไม่ครบก็ได้
  - แถวปุ่มเครื่อง 'เครื่องที่ทำ' ขึ้นกรอบชมพูตอนยังไม่เลือก (ทุกประเภทงานภายในที่ต้องเลือกเครื่อง)
  - ต้องครบ 3 อย่าง: เครื่อง · เหตุผล · ยอด
usage: python3 tools/v200_internal_amount_only.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v199-2026-11-06';", "window.APP_VERSION = 'v200-2026-11-06';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v199';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v199';", "const CACHE_NAME = 'plp-laundry-v200';")

# ---------- MM ----------
rep("""  '🔧 ร้านใช้เอง': '🔧 ဆိုင်သုံး', // v199
""", """  '🔧 ร้านใช้เอง': '🔧 ဆိုင်သုံး', // v199
  'ยอดเครดิตที่ใช้ (บาท)': 'သုံးသော ခရက်ဒစ် (ဘတ်)', // v200
  'ยอดโทเคนที่หยอด (บาท)': 'ထည့်သော တိုကင် (ဘတ်)', // v200
  'ใส่ยอดเครดิตที่ใช้ (บังคับ)': 'သုံးသော ငွေပမာဏ ထည့်ပါ (မဖြစ်မနေ)', // v200
  'ใส่ยอดที่ใช้จริง — หยอดไม่ครบก็ใส่ตามจริง': 'တကယ်သုံးသည့် ပမာဏ ထည့်ပါ — မပြည့်လည်း ရှိသလောက်ထည့်', // v200
""", 'MM')

# ---------- ตัวแปร ----------
rep("""  const simpleMode = simpleFree || simpleAcct;
""", """  const simpleMode = simpleFree || simpleAcct;
  const amtOnly = isInternal && needInternalDetail && !fixType && !simpleFree; // 🔧 v200 ซ่อม/ทดสอบ/อื่นๆ = เลือกเครื่อง + ใส่ยอดเอง (ไม่ใช้ซัก/อบด้านล่าง)
""", 'amtOnly')

rep("(!needInternalDetail || (internalReason.trim().length > 0 && (hasAnyItem || customAmt > 0)))",
    "(!needInternalDetail || (internalReason.trim().length > 0 && (amtOnly ? customAmt > 0 : (hasAnyItem || customAmt > 0))))", 'internalOk')
rep("""    if (!hasAnyItem && customAmt <= 0) missingList.push(tr(config, fixType ? 'กรอกจำนวนโทเคนที่ให้' : 'เลือกเครื่อง (ซัก/อบ) หรือกรอกยอดเครดิตเอง'));""",
    """    if (amtOnly ? customAmt <= 0 : (!hasAnyItem && customAmt <= 0)) missingList.push(tr(config, fixType ? 'กรอกจำนวนโทเคนที่ให้' : amtOnly ? 'ใส่ยอดเครดิตที่ใช้ (บังคับ)' : 'เลือกเครื่อง (ซัก/อบ) หรือกรอกยอดเครดิตเอง'));""", 'missing')

# ---------- บันทึก ----------
rep("""      washItems: fixType ? [] : (washItems || []), // 🪙 v189 โทเคนแก้ปัญหา = จำนวนโทเคน + เหตุผล ไม่มีเครื่อง
      dryItems: fixType ? [] : (dryItems || []),""",
    """      washItems: fixType || amtOnly ? [] : (washItems || []), // 🪙 v189 โทเคนแก้ปัญหา = จำนวนโทเคน + เหตุผล ไม่มีเครื่อง · 🔧 v200 ซ่อม/ทดสอบ = ยอดเอง
      dryItems: fixType || amtOnly ? [] : (dryItems || []),""", 'save items')

# ---------- ซ่อนเครื่องซัก/อบด้านล่าง ----------
rep("""{!autoItems && !fixType && <Section iconName="droplet" title={tr(config, "เครื่องซัก")}>""",
    """{!autoItems && !fixType && !amtOnly && <Section iconName="droplet" title={tr(config, "เครื่องซัก")}>""", 'hide wash')
rep("""{!autoItems && !fixType && <Section iconName="wind" title={tr(config, "เครื่องอบ")}>""",
    """{!autoItems && !fixType && !amtOnly && <Section iconName="wind" title={tr(config, "เครื่องอบ")}>""", 'hide dry')

# ---------- ช่องยอด ----------
rep("""                <p className="text-xs font-bold text-slate-700 mb-1 mt-3">{tokenShop(config) ? tr(config, fixType ? 'จำนวนโทเคนที่ให้ (บาท)' : 'ยอดโทเคนที่หยอด (ถ้าไม่เลือกเครื่องด้านล่าง)') : 'กำหนดยอดเครดิตเอง (ถ้าไม่เลือกเครื่องด้านล่าง)'}</p>
                <input type="number" inputMode="numeric" value={internalCustom} onChange={e => setInternalCustom(e.target.value)} onFocus={e => e.target.select()} data-icustom
                  className="w-full px-3 py-2.5 rounded-xl border-2 border-slate-300 bg-white text-lg font-bold text-right" placeholder="0" />""",
    """                {amtOnly ? (
                  <p className="text-xs font-bold text-slate-700 mb-1 mt-3">{tr(config, tokenShop(config) ? 'ยอดโทเคนที่หยอด (บาท)' : 'ยอดเครดิตที่ใช้ (บาท)')} <span className="text-rose-600">*{tr(config, 'บังคับ')}</span></p>
                ) : (
                <p className="text-xs font-bold text-slate-700 mb-1 mt-3">{tokenShop(config) ? tr(config, fixType ? 'จำนวนโทเคนที่ให้ (บาท)' : 'ยอดโทเคนที่หยอด (ถ้าไม่เลือกเครื่องด้านล่าง)') : 'กำหนดยอดเครดิตเอง (ถ้าไม่เลือกเครื่องด้านล่าง)'}</p>
                )}
                <input type="number" inputMode="numeric" value={internalCustom} onChange={e => setInternalCustom(e.target.value)} onFocus={e => e.target.select()} data-icustom
                  className={`w-full px-3 py-2.5 rounded-xl border-2 text-lg font-bold text-right ${amtOnly && customAmt <= 0 ? 'bg-rose-50 border-rose-300' : 'border-slate-300 bg-white'}`} placeholder="0" />""", 'amount field')
rep("""                <p className="text-[11px] text-slate-600 mt-1">{tr(config, 'เลือกเครื่อง+อุณหภูมิด้านล่างจะคิดราคาให้เอง · หรือกรอกยอดเองช่องนี้')}</p>""",
    """                <p className="text-[11px] text-slate-600 mt-1">{tr(config, amtOnly ? 'ใส่ยอดที่ใช้จริง — หยอดไม่ครบก็ใส่ตามจริง' : 'เลือกเครื่อง+อุณหภูมิด้านล่างจะคิดราคาให้เอง · หรือกรอกยอดเองช่องนี้')}</p>""", 'amount hint')

# ---------- กรอบชมพูแถวเครื่อง ----------
rep("""            <div className="flex flex-wrap gap-1.5 mb-3">
              {((COIN_POINTS[config.brand] || COIN_POINTS.teddy2).machines || []).map(m => {
                const on = internalMachines.includes(m.label);
                const dryNo = internalType === 'clean' && (!isOwner || simpleFree) && /^d/i.test(m.id);""",
    """            <div data-imachines className={`flex flex-wrap gap-1.5 mb-3 ${internalMachines.length === 0 ? 'rounded-xl p-1.5 bg-rose-50 border-2 border-rose-300' : ''}`}>
              {((COIN_POINTS[config.brand] || COIN_POINTS.teddy2).machines || []).map(m => {
                const on = internalMachines.includes(m.label);
                const dryNo = internalType === 'clean' && (!isOwner || simpleFree) && /^d/i.test(m.id);""", 'chips pink')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v200 applied')
