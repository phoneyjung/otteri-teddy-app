#!/usr/bin/env python3
"""v198 — บันทึกลูกค้าใช้โปร (ซักเอง ไม่ฝาก): เจ้าของกดบันทึกได้โดยไม่ยิงเครื่อง
ที่มา: เจ้าของ 5 พ.ย. 69 'ตอนนี้ยิงไม่ได้ แก้ไขให้เจ้าของกดบันทึกได้ แบบที่เริ่มงาน' (EC ระงับบัญชีถึงอาทิตย์ 8 พ.ย.)
ทำอะไร (เหมือนปุ่ม ✍️ ในหน้าเริ่มเครื่องของใบงาน v149)
  - ฟอร์มโปร: ปุ่มม่วง '✍️ เจ้าของ: บันทึกว่าเริ่มแล้ว (ไม่ยิงจริง) ฿50' เฉพาะล็อกอินแบบเจ้าของ + ร้านยิงพัลส์
  - กดแล้ว: ตรวจเหมือนเดิม (ยอด หาร 10 ลงตัว · เลือกเครื่อง · รูปหลักฐาน) → ยืนยัน → บันทึกโปร (creditLedger)
    + pulseLog method/status 'manual' (refType 'promo', refId = รายการโปร) → กระทบยอด: โปรครบ ไม่ขึ้น 'ยิงไม่ครบ'
    และไม่เอาไปจับคู่กับเว็บ EC · เจ้าของลบรายการได้เหมือน ✍️ เดิม
  - หน้าบันทึกเสร็จ/ใบรายงาน LINE: '✍️ เจ้าของบันทึก (ไม่ยิงเครื่อง)'
usage: python3 tools/v198_promo_owner_manual.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v197-2026-11-03';", "window.APP_VERSION = 'v198-2026-11-05';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v197';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v197';", "const CACHE_NAME = 'plp-laundry-v198';")

# ---------- บันทึก ----------
rep("""  const handleSubmitPromo = async () => {
    const amount = parseInt(promoAmount, 10) || 0;""",
    """  const promoOwner = role === 'owner' || pulseIsOwnerNow(config, false); // ✍️ v198 เจ้าของบันทึกโปรโดยไม่ยิงเครื่องได้
  const handleSubmitPromo = async (opts) => {
    const manual = !!(opts && opts.manual === true && promoOwner); // ✍️ v198 (onClick เดิมส่ง event มา = ไม่ใช่ manual)
    const amount = parseInt(promoAmount, 10) || 0;""", 'submit head')

rep("""    if (usePulse && !confirm(`⚡ ${tr(config, 'ยืนยันเริ่มเครื่อง')}""",
    """    if (manual && !confirm(`✍️ เจ้าของบันทึกโปร (ไม่ยิงเครื่อง)\\n\\n🧺 ${pulseMachine.label}\\n🎁 ${promoName || 'ส่วนลด'} ฿${amount}\\n\\n⚠️ แอปไม่สั่งเครื่องให้ — เริ่มเครื่องเอง (หยอดเหรียญ / ตู้) · นับว่าเริ่มแล้ว`)) return;
    if (usePulse && !manual && !confirm(`⚡ ${tr(config, 'ยืนยันเริ่มเครื่อง')}""", 'manual confirm')

rep("""      let id;
      if (usePulse) {
        const entryRef = window.db.collection('creditLedger').doc(); // จอง id ก่อน → พัลส์ผูกกับรายการนี้""",
    """      let id;
      if (usePulse && manual) {
        // ✍️ v198 เจ้าของบันทึก (ไม่ยิงเครื่อง) — pulseLog แบบ manual ผูกกับรายการโปร (กระทบยอดนับว่าครบ · ไม่จับคู่ EC)
        const entryRef = window.db.collection('creditLedger').doc();
        const now = Date.now();
        const logId = `${config.brand}-manual-${now}-${Math.random().toString(36).slice(2, 8)}`;
        await pulseLogRef(logId).set({
          brand: config.brand, dateKey: dateKeyOf(new Date(now)), machine: pulseMachine.id, machineLabel: pulseMachine.label,
          pulses: amount / PULSE_BAHT, baht: amount, method: 'manual', status: 'manual',
          refType: 'promo', refId: entryRef.id, slotKey: 'p', refLabel: '🎟️ ' + entry.promoName,
          staffId: 'owner', staffName: 'เจ้าของ', createdAt: now,
          kind: pulseMachine.kind || null, kg: pulseMachine.kg || null,
          manualNote: 'เจ้าของบันทึกโปร (ไม่ยิงเครื่อง)',
        });
        entry.pulseLogId = logId; entry.pulseStatus = 'manual'; entry.machineId = pulseMachine.id; entry.manual = true;
        id = await saveCreditEntryWithId(config.brand, entryRef.id, entry);
      } else if (usePulse) {
        const entryRef = window.db.collection('creditLedger').doc(); // จอง id ก่อน → พัลส์ผูกกับรายการนี้""", 'manual save')

# ---------- ปุ่ม ----------
rep("""            <button onClick={handleSubmitPromo} disabled={savingPromo}
              className="w-full py-3.5 rounded-2xl bg-rose-500 text-white font-bold text-base active:scale-95 transition disabled:opacity-50">""",
    """            {pulseOn(config) && promoOwner && (
              <button onClick={() => handleSubmitPromo({ manual: true })} disabled={savingPromo} data-promo-manual
                className="w-full py-2.5 rounded-xl border-2 text-sm font-extrabold active:scale-95 transition disabled:opacity-50" style={{ borderColor: '#8B5CF6', background: '#F5F3FF', color: '#5B21B6' }}>
                ✍️ {tr(config, 'เจ้าของ: บันทึกว่าเริ่มแล้ว (ไม่ยิงจริง)')} {promoMachine || ''} ฿{parseInt(promoAmount, 10) || 0}
              </button>
            )}
            <button onClick={handleSubmitPromo} disabled={savingPromo}
              className="w-full py-3.5 rounded-2xl bg-rose-500 text-white font-bold text-base active:scale-95 transition disabled:opacity-50">""", 'manual button')

# ---------- หน้าบันทึกเสร็จ / ใบรายงาน / ข้อความแชร์ ----------
rep("""            <p className="text-lg font-extrabold text-slate-800">{savedPromo.pulseLogId ? tr(config, 'เริ่มเครื่องแล้ว')""",
    """            <p className="text-lg font-extrabold text-slate-800">{savedPromo.manual ? '✍️ ' + tr(config, 'เจ้าของบันทึกแล้ว (ไม่ยิงจริง)') : savedPromo.pulseLogId ? tr(config, 'เริ่มเครื่องแล้ว')""", 'saved title')
rep("""            {savedPromo.pulseLogId && (
              <p className={`text-sm font-bold mt-1 ${savedPromo.pulseStatus === 'confirmed'""",
    """            {savedPromo.pulseLogId && !savedPromo.manual && (
              <p className={`text-sm font-bold mt-1 ${savedPromo.pulseStatus === 'confirmed'""", 'saved status')
rep("""                    savedPromo.pulseLogId ? ['เริ่มเครื่อง', savedPromo.pulseStatus === 'confirmed' ? '⚡ เครื่องรับแล้ว' : '⚡ ส่งคำสั่งแล้ว']""",
    """                    savedPromo.manual ? ['เริ่มเครื่อง', '✍️ เจ้าของบันทึก (ไม่ยิงเครื่อง)'] : savedPromo.pulseLogId ? ['เริ่มเครื่อง', savedPromo.pulseStatus === 'confirmed' ? '⚡ เครื่องรับแล้ว' : '⚡ ส่งคำสั่งแล้ว']""", 'slip row')
rep("""        p.pulseLogId ? `🎁 ${p.promoName} · ⚡ ยิงพัลส์ ${p.amount}฿`""",
    """        p.manual ? `🎁 ${p.promoName} · ✍️ เจ้าของบันทึก ${p.amount}฿` : p.pulseLogId ? `🎁 ${p.promoName} · ⚡ ยิงพัลส์ ${p.amount}฿`""", 'share image line')
rep("""      savedPromo.pulseLogId ? `⚡ ยิงพัลส์: ${savedPromo.amount}฿""",
    """      savedPromo.manual ? `✍️ เจ้าของบันทึก (ไม่ยิงเครื่อง): ${savedPromo.amount}฿` : savedPromo.pulseLogId ? `⚡ ยิงพัลส์: ${savedPromo.amount}฿""", 'share text')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v198 applied')
