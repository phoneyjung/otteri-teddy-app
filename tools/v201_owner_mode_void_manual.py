#!/usr/bin/env python3
"""v201 — โหมดเจ้าของค้างครึ่งเดียว + ลบงานแล้ว ✍️ ไม่หาย
ที่มา: เจ้าของ 6 พ.ย. 69
  'กดยกเลิกงานซ่อมไปแล้วไม่หาย' → กระทบยอดขึ้น 'ยิงพัลส์แต่ไม่พบงาน ฿60 · นอกแอป (ระบบเก่า) · ซ่อม/ทดสอบเครื่อง'
  'กดงานภายใน งานซ่อมหาย เป็นโหมดเจ้าของแล้ว' → ฟอร์มงานภายในเป็นแบบแม่บ้าน (ล้างเครื่องอย่างเดียว)
สาเหตุ
  1) ลบงาน → รายการ ✍️ 'บันทึกว่าเริ่มแล้ว (ไม่ยิงจริง)' ของงานนั้นยังนับอยู่ (ไม่ใช่พัลส์จริง แต่ไม่ถูกยกเลิกตาม)
  2) กด 'ออก' จากหน้าเจ้าของ → isOwner ปิด แต่ผู้ใช้ยังล็อกอินแบบเจ้าของ (หน้าแรกขึ้น 'โหมดเจ้าของ')
     → ฟอร์มรับงานได้ isOwner=false → กลายเป็นฟอร์มแม่บ้าน
ทำอะไร
  - voidManualLogsOf(refId): ยกเลิก (status void) pulseLog แบบ manual ของงาน/โปรที่ถูกลบ
    เรียกใน deleteOrderFromCloud · deleteOrdersBatch · ลบรายการโปร (creditLedger) · พัลส์จริง/หยอดเหรียญจริง เก็บไว้เหมือนเดิม
  - กระทบยอด: 'ยิงพัลส์แต่ไม่พบงาน' ที่เป็นรายการ ✍️ → เจ้าของมีปุ่ม '🗑️ ลบรายการ ✍️ นี้ (งานถูกลบแล้ว)' (เคลียร์ของค้างวันนี้)
  - App: ล็อกอินแบบเจ้าของอยู่ = isOwner เปิดเสมอ
usage: python3 tools/v201_owner_mode_void_manual.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v200-2026-11-06';", "window.APP_VERSION = 'v201-2026-11-06';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v200';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v200';", "const CACHE_NAME = 'plp-laundry-v201';")

# ---------- MM ----------
rep("""  'ใส่ยอดที่ใช้จริง — หยอดไม่ครบก็ใส่ตามจริง': 'တကယ်သုံးသည့် ပမာဏ ထည့်ပါ — မပြည့်လည်း ရှိသလောက်ထည့်', // v200
""", """  'ใส่ยอดที่ใช้จริง — หยอดไม่ครบก็ใส่ตามจริง': 'တကယ်သုံးသည့် ပမာဏ ထည့်ပါ — မပြည့်လည်း ရှိသလောက်ထည့်', // v200
  'ลบรายการ ✍️ นี้ (งานถูกลบแล้ว)': 'ဤ ✍️ မှတ်တမ်းကို ဖျက်ပါ (အလုပ်ဖျက်ပြီး)', // v201
""", 'MM')

# ---------- ยกเลิก ✍️ ตอนลบงาน ----------
rep("""async function deleteOrderFromCloud(orderId) {
  try {
    await window.db.collection('orders').doc(orderId).delete();""",
    """// ✍️ v201 ลบงาน/โปร → ยกเลิกรายการ 'บันทึกว่าเริ่มแล้ว (ไม่ยิงจริง)' ของงานนั้น (ไม่ใช่พัลส์จริง · เดิมค้างเป็น 'ยิงพัลส์แต่ไม่พบงาน')
// พัลส์จริง / หยอดเหรียญจริง ไม่แตะ (เครื่องได้เงินไปแล้ว ต้องเห็นในกระทบยอด)
async function voidManualLogsOf(refId) {
  if (!refId) return;
  const snap = await window.db.collection('pulseLogs').where('refId', '==', refId).get();
  const jobs = [];
  snap.forEach(d => { const l = d.data() || {}; if (l.method === 'manual' && l.status === 'manual') jobs.push(voidPulseLog(d.id, 'ลบงานแล้ว (บันทึกว่าเริ่ม ไม่ได้ยิงจริง)')); });
  await Promise.all(jobs);
}
async function deleteOrderFromCloud(orderId) {
  try {
    await window.db.collection('orders').doc(orderId).delete();
    voidManualLogsOf(orderId).catch(e => console.error('void manual logs:', e)); // ✍️ v201""", 'delete one')
rep("""      if (window.__photoSplitOK) orderIds.slice(i, i + chunkSize).forEach(id => window.db.collection('orderPhotos').doc(id).delete().catch(() => {}));""",
    """      if (window.__photoSplitOK) orderIds.slice(i, i + chunkSize).forEach(id => window.db.collection('orderPhotos').doc(id).delete().catch(() => {}));
      orderIds.slice(i, i + chunkSize).forEach(id => voidManualLogsOf(id).catch(() => {})); // ✍️ v201""", 'delete batch')
rep("""  try { await window.db.collection('creditLedger').doc(id).delete(); }""",
    """  try { await window.db.collection('creditLedger').doc(id).delete(); voidManualLogsOf(id).catch(() => {}); /* ✍️ v201 โปรที่เจ้าของบันทึก */ }""", 'delete promo')

# ---------- กระทบยอด: ปุ่มลบ ✍️ ที่ค้าง ----------
rep("""    if (!exists) add(`x:${l.id}`, 'error', 'ยิงพัลส์แต่ไม่พบงาน', { label: `${l.machineLabel} · ${l.refLabel || ''}`, amount: l.baht });""",
    """    if (!exists) add(`x:${l.id}`, 'error', 'ยิงพัลส์แต่ไม่พบงาน', { label: `${l.machineLabel} · ${l.refLabel || ''}`, amount: l.baht, voidId: pulseIsManual(l) ? l.id : null });""", 'orphan voidId')
rep("""                    {isOwner && i.ecOut && claimBtn([i], '🔧 เจ้าของยิงทดสอบ → เปลี่ยนเป็นงานซ่อม/ทดสอบ')}""",
    """                    {isOwner && i.ecOut && claimBtn([i], '🔧 เจ้าของยิงทดสอบ → เปลี่ยนเป็นงานซ่อม/ทดสอบ')}
                    {isOwner && i.voidId && (
                      <button data-void-orphan onClick={() => { if (confirm('🗑️ ลบรายการ ✍️ ที่บันทึกว่าเริ่มแล้ว (ไม่ยิงจริง)?\\n\\nงานของรายการนี้ถูกลบไปแล้ว')) voidPulseLog(i.voidId, 'เจ้าของลบ (งานถูกลบแล้ว)').catch(e => alert('ลบไม่สำเร็จ: ' + e.message)); }}
                        className="mt-1.5 w-full py-1.5 rounded-lg border-2 border-slate-300 bg-white text-xs font-extrabold text-slate-600 active:scale-95">🗑️ {tr(config, 'ลบรายการ ✍️ นี้ (งานถูกลบแล้ว)')}</button>
                    )}""", 'orphan button')

# ---------- โหมดเจ้าของ ----------
rep("""  const [currentStaff, setCurrentStaff] = useState(() => {
    try { return JSON.parse(localStorage.getItem('staff-' + config.brand) || 'null'); } catch { return null; }
  });
""", """  const [currentStaff, setCurrentStaff] = useState(() => {
    try { return JSON.parse(localStorage.getItem('staff-' + config.brand) || 'null'); } catch { return null; }
  });
  // 👔 v201 ล็อกอินแบบเจ้าของอยู่ = โหมดเจ้าของเสมอ (เดิมกด 'ออก' จากหน้าเจ้าของ → isOwner ปิด แต่หน้าแรกยัง 'โหมดเจ้าของ' → ฟอร์มงานภายในกลายเป็นแบบแม่บ้าน)
  useEffect(() => { if (currentStaff && currentStaff.isOwnerLogin && !isOwner) setIsOwner(true); }, [currentStaff, isOwner]);
""", 'owner sync')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v201 applied')
