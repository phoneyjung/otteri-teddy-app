#!/usr/bin/env python3
"""v190 — Teddy 1: แม่บ้านลงงานย้อนหลังได้จากฟอร์มเลย (ลืมลงตอนลูกค้ามา)
ที่มา: เจ้าของ 2 พ.ย. 69 'ทำให้ teddy1 ลงย้อนหลังได้ เพราะแม่บ้านที่นี่อายุเยอะแล้ว ลืมบ่อย'
ทำอะไร (ร้านที่ตั้ง config.maidBackdate = Teddy 1 + โหมดฝึก)
  - ฟอร์มรับงานใหม่ + บิลงานร้าน (ล้างเครื่อง/ซ่อม/โทเคนแก้ปัญหา) ของแม่บ้าน: ปุ่มบนสุด
    '🕐 เวลา: ตอนนี้ · ⏪ ลืมลง? แตะเพื่อลงย้อนหลัง' → กล่องเหลืองเลือกวัน-เวลา (เหมือนลงย้อนหลังจากหน้าแรก)
    + ปุ่ม '↩ ใช้เวลาตอนนี้' ยกเลิกได้ · เลือกอนาคตไม่ได้
  - บันทึก: เวลาที่เลือกเป็นเวลางาน · ต่างวัน = ถามยืนยันเหมือนเดิม
    ย้อนเกิน 10 นาที = ติดป้าย ⏪ ลงย้อนหลัง + เวลาที่บันทึกจริง (enteredAt) ให้เจ้าของเห็น แม้เป็นวันเดียวกัน
  - แก้ไขงานเดิม: ไม่เปลี่ยน (แม่บ้านแก้เวลาไม่ได้เหมือนเดิม)
usage: python3 tools/v190_teddy1_backdate.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v189-2026-11-02';", "window.APP_VERSION = 'v190-2026-11-02';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v189';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v189';", "const CACHE_NAME = 'plp-laundry-v190';")

# ---------- config ----------
rep("""  maidInternal: ['test'], // 🔧 v177 แม่บ้านทำบิลซ่อม/ทดสอบเครื่องเองได้ (เจ้าของไม่ได้อยู่ร้าน)""",
    """  maidInternal: ['test'], // 🔧 v177 แม่บ้านทำบิลซ่อม/ทดสอบเครื่องเองได้ (เจ้าของไม่ได้อยู่ร้าน)
  maidBackdate: true, // ⏪ v190 แม่บ้านลงย้อนหลังได้จากฟอร์ม (ลืมลงตอนลูกค้ามา)""", 'TEDDY maidBackdate')

rep("""  tokenFix: false, maidInternal: [], // v177: บิลโทเคนแก้ปัญหา/ซ่อมโดยแม่บ้าน = เฉพาะ Teddy 1""",
    """  tokenFix: false, maidInternal: [], // v177: บิลโทเคนแก้ปัญหา/ซ่อมโดยแม่บ้าน = เฉพาะ Teddy 1
  maidBackdate: false, // v190 ลงย้อนหลังจากฟอร์ม = เฉพาะ Teddy 1 (Teddy 2 ยิงพัลส์ ใช้ลงย้อนหลังจากหน้าแรกเหมือนเดิม)""", 'TEDDY2 maidBackdate off')

# ---------- NewOrderView ----------
rep("""  const canPickTime = freeOk || backdateMode;""",
    """  const maidBack = !freeOk && !isEdit && !backdateMode && !!config.maidBackdate; // ⏪ v190 Teddy 1: แม่บ้านแตะลงย้อนหลังในฟอร์มได้
  const canPickTime = freeOk || backdateMode || maidBack;""", 'maidBack')
rep("""        {!freeOk && backdateMode && (
          <div className="rounded-2xl p-4 shadow-lg border-2 border-amber-400" style={{background: 'linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%)'}}>
            <p className="font-extrabold text-amber-900 text-base mb-1">⏪ {tr(config, 'กำลังลงงานย้อนหลัง')}</p>
            <p className="text-xs text-amber-800 mb-3">{tr(config, 'เลือกวัน-เวลาที่ลูกค้ามาจริง')}</p>""",
    """        {maidBack && !useCustomTime && (
          <button data-backdate-toggle onClick={() => { setCustomDateTime(toLocalInputValue(Date.now())); setUseCustomTime(true); }}
            className="w-full rounded-2xl px-4 py-3 bg-white border-2 border-dashed border-amber-300 text-left active:scale-95 transition">
            <p className="text-sm font-extrabold text-slate-800">🕐 {tr(config, 'เวลา: ตอนนี้')}</p>
            <p className="text-sm font-bold text-amber-700">⏪ {tr(config, 'ลืมลง? แตะเพื่อลงย้อนหลัง')}</p>
          </button>
        )}
        {!freeOk && (backdateMode || (maidBack && useCustomTime)) && (
          <div className="rounded-2xl p-4 shadow-lg border-2 border-amber-400" data-backdate-box style={{background: 'linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%)'}}>
            <p className="font-extrabold text-amber-900 text-base mb-1">⏪ {tr(config, 'กำลังลงงานย้อนหลัง')}</p>
            <p className="text-xs text-amber-800 mb-3">{tr(config, isInternal ? 'เลือกวัน-เวลาที่ทำจริง' : 'เลือกวัน-เวลาที่ลูกค้ามาจริง')}</p>""", 'maid backdate box')
rep("""              <p className="text-sm font-extrabold text-amber-900 mt-2 text-center">📅 {new Date(customDateTime).toLocaleString('th-TH', { weekday: 'long', day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit' })} น.</p>
            )}
          </div>
        )}""",
    """              <p className="text-sm font-extrabold text-amber-900 mt-2 text-center">📅 {new Date(customDateTime).toLocaleString('th-TH', { weekday: 'long', day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit' })} น.</p>
            )}
            {maidBack && <button data-backdate-cancel onClick={() => setUseCustomTime(false)} className="mt-3 w-full py-2.5 rounded-xl bg-white text-amber-900 text-sm font-bold border border-amber-300 active:scale-95 transition">↩ {tr(config, 'ใช้เวลาตอนนี้')}</button>}
          </div>
        )}""", 'cancel button')

# ---------- บันทึก: ย้อนเกิน 10 นาที (แม่บ้านเลือกเอง) = ติดป้าย ⏪ ให้เจ้าของเห็น ----------
rep("""      backdated: isBackdated || !!(editingOrder && editingOrder.backdated),
      enteredAt: isBackdated ? Date.now() :""",
    """      backdated: isBackdated || (maidBack && useCustomTime && finalCreatedAt < Date.now() - 600000) || !!(editingOrder && editingOrder.backdated), // v190 แม่บ้านลงย้อนหลังวันเดียวกัน (>10 นาที) ก็ติดป้าย
      enteredAt: isBackdated || (maidBack && useCustomTime && finalCreatedAt < Date.now() - 600000) ? Date.now() :""", 'save flags')

# ---------- MM ----------
rep("""  'เลือกวัน-เวลาที่ลูกค้ามาจริง':""",
    """  'ลืมลง? แตะเพื่อลงย้อนหลัง': 'မေ့သွားလား? နောက်ကြောင်းပြန်ထည့်ရန် နှိပ်ပါ', // v190
  'ใช้เวลาตอนนี้': 'ယခုအချိန် သုံးမည်', // v190
  'เลือกวัน-เวลาที่ทำจริง': 'တကယ်လုပ်ခဲ့သည့် ရက်-အချိန် ရွေးပါ', // v190
  'เลือกวัน-เวลาที่ลูกค้ามาจริง':""", 'MM')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v190 applied')
