#!/usr/bin/env python3
"""v177 — Teddy 1: แม่บ้านทำบิลงานร้านได้แบบ Teddy 2 (หน้าเดิมของ Teddy 1 · เจ้าของตัดสิน 1 พ.ย. 69)
- ปุ่ม 🔧 บิลงานร้าน (ไม่ใช่ลูกค้า) = 🧼 ล้างเครื่อง · 🔧 ซ่อม/ทดสอบเครื่อง (แม่บ้านทำได้) · 🪙 โทเคนแก้ปัญหา (ใหม่ · บังคับเหตุผล)
  ทุกแบบ = หยอดโทเคนโดยไม่มีเงินเข้า → เจ้าของเห็นในแท็บ งาน → งานภายใน · สิ้นเดือนลงบัญชีเป็นรายจ่าย
- 🎟️ ลูกค้าใช้คูปองแอดไลน์ (ซักเอง ไม่ฝาก) — ร้านโทเคน: ใช้คำว่า 'ให้โทเคน' แทน 'สแกนเครดิต' · เปิดฟอร์มแล้วเลือก LINE ลด 40 ไว้ให้
- หน้าเจ้าของ (ร้านไม่มีระบบยิงพัลส์): แท็บ ส่วนลด เห็นรายการคูปอง/โปรลูกค้าซักเอง + ลบได้
- Teddy 2 / Otteri ไม่เปลี่ยน (แม่บ้าน Teddy 2 ยังทำได้แค่ล้างเครื่อง)
usage: python3 tools/v177_t1_bills.py index.html sw.js
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


# ---------- version ----------
rep("window.APP_VERSION = 'v176-2026-11-01';", "window.APP_VERSION = 'v177-2026-11-01';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v176';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v176';", "const CACHE_NAME = 'plp-laundry-v177';")

# ---------- config ----------
rep("""  hasKev: true,
""", """  hasKev: true,
  tokenFix: true, // 🪙 v177 บิล 'โทเคนแก้ปัญหา' (แม่บ้านให้โทเคนแก้ปัญหาลูกค้า · บังคับเหตุผล)
  maidInternal: ['test'], // 🔧 v177 แม่บ้านทำบิลซ่อม/ทดสอบเครื่องเองได้ (เจ้าของไม่ได้อยู่ร้าน)
""", 'TEDDY_CONFIG flags')
rep("""  linePromoDiscount: 50, // Teddy 2 ลดแอดไลน์ 50 (มากกว่า Teddy 1)
""", """  linePromoDiscount: 50, // Teddy 2 ลดแอดไลน์ 50 (มากกว่า Teddy 1)
  tokenFix: false, maidInternal: [], // v177: บิลโทเคนแก้ปัญหา/ซ่อมโดยแม่บ้าน = เฉพาะ Teddy 1
""", 'TEDDY2_CONFIG override')

# ---------- ประเภทงานภายใน ----------
rep("""  { id: 'other', label: 'อื่นๆ', emoji: '📝' },
];""", """  { id: 'fix', label: 'โทเคนแก้ปัญหา', emoji: '🪙', cfg: 'tokenFix' }, // v177 Teddy 1: ให้โทเคนแก้ปัญหาลูกค้า (เครื่องกินโทเคน ฯลฯ) · บังคับเหตุผล
  { id: 'other', label: 'อื่นๆ', emoji: '📝' },
];""", 'INTERNAL_TYPES fix')
rep("""const INTERNAL_OWNER_ONLY = ['test', 'redo', 'other'];
""", """const INTERNAL_OWNER_ONLY = ['test', 'redo', 'other'];
// 🔧 v177: ร้านที่ให้แม่บ้านทำบิลงานภายในเพิ่มเอง (config.maidInternal) — Teddy 1: ซ่อม/ทดสอบเครื่อง
const internalOwnerOnly = (config) => INTERNAL_OWNER_ONLY.filter(t => !((config && config.maidInternal) || []).includes(t));
const maidInternalTypes = (config) => internalTypesFor(config).filter(t => !internalOwnerOnly(config).includes(t.id));
const maidBillTypes = (config) => maidInternalTypes(config).filter(t => t.id !== 'mine');
// 🪙 ร้านที่ใช้โทเคนของร้าน (Teddy 1) — ไม่มีสแกนเครดิต · แม่บ้าน 'ให้โทเคน'
const tokenShop = (config) => !!(config && COIN_POINTS[config.brand] && COIN_POINTS[config.brand].tokenMode);
""", 'helpers')

# ---------- ฟอร์มงานภายใน ----------
rep("""  const needInternalDetail = internalType === 'test' || internalType === 'other';""",
    """  const needInternalDetail = internalType === 'test' || internalType === 'other' || internalType === 'fix';
  const fixType = internalType === 'fix'; // 🪙 v177 ไม่ต้องเลือกเครื่อง · บังคับยอด + เหตุผล""", 'needInternalDetail')
rep("""(internalMachines.length > 0 && (!needInternalDetail || (internalReason.trim().length > 0 && (hasAnyItem || customAmt > 0)))));""",
    """((fixType || internalMachines.length > 0) && (!needInternalDetail || (internalReason.trim().length > 0 && (hasAnyItem || customAmt > 0)))));""", 'internalOk')
rep("""    if (INTERNAL_OWNER_ONLY.includes(internalType)) internalMaidIssues.push('ซ่อม/ทดสอบ ซักซ้ำ และอื่นๆ — เฉพาะเจ้าของ');""",
    """    if (internalOwnerOnly(config).includes(internalType)) internalMaidIssues.push('ซ่อม/ทดสอบ ซักซ้ำ และอื่นๆ — เฉพาะเจ้าของ');""", 'maid issues owner-only')
rep("""  if (isInternal && internalType !== 'mine' && internalMachines.length === 0) missingList.push('เลือกเครื่องที่ทำ (บังคับ)');""",
    """  if (isInternal && internalType !== 'mine' && !fixType && internalMachines.length === 0) missingList.push(tr(config, 'เลือกเครื่องที่ทำ (บังคับ)'));""", 'missing machines')
rep("""    if (!hasAnyItem && customAmt <= 0) missingList.push('เลือกเครื่อง (ซัก/อบ) หรือกรอกยอดเครดิตเอง');
    if (!internalReason.trim()) missingList.push('ใส่เหตุผล (บังคับ)');""",
    """    if (!hasAnyItem && customAmt <= 0) missingList.push(tr(config, fixType ? 'กรอกจำนวนโทเคนที่ให้' : 'เลือกเครื่อง (ซัก/อบ) หรือกรอกยอดเครดิตเอง'));
    if (!internalReason.trim()) missingList.push(tr(config, 'ใส่เหตุผล (บังคับ)'));""", 'missing detail')

rep("""<p className="font-extrabold text-slate-900">{isOwner ? '🔧 งานภายในร้าน' : internalType === 'mine' ? '👔 ' + tr(config, 'ผ้าเจ้าของ') : '🧼 ' + tr(config, 'ล้างเครื่อง')}</p>""",
    """<p className="font-extrabold text-slate-900">{isOwner ? '🔧 งานภายในร้าน' : (() => { const it = INTERNAL_TYPES.find(x => x.id === internalType) || INTERNAL_TYPES[0]; return it.emoji + ' ' + tr(config, it.label); })()}</p>""", 'form title')
rep("""            {(isOwner || config.ownerLaundry) && <div className="flex flex-wrap gap-1.5 mb-3">
              {internalTypesFor(config).filter(t => isOwner || !INTERNAL_OWNER_ONLY.includes(t.id)).map(t => {
                const locked = !isOwner && INTERNAL_OWNER_ONLY.includes(t.id);
                return (
                  <button key={t.id} data-itype={t.id} onClick={() => { if (locked) { alert('🔒 ' + t.label + ' — เฉพาะเจ้าของ'); return; } if (t.id !== internalType && (t.id === 'mine' || internalType === 'mine')) { setInternalMachines([]); if (!isOwner) { setWashItems([]); setDryItems([]); } } setInternalType(t.id); }}""",
    """            {(isOwner || maidInternalTypes(config).length > 1) && <div className="flex flex-wrap gap-1.5 mb-3">
              {internalTypesFor(config).filter(t => isOwner || !internalOwnerOnly(config).includes(t.id)).map(t => {
                const locked = !isOwner && internalOwnerOnly(config).includes(t.id);
                return (
                  <button key={t.id} data-itype={t.id} onClick={() => { if (locked) { alert('🔒 ' + t.label + ' — เฉพาะเจ้าของ'); return; } if (t.id !== internalType && (t.id === 'mine' || internalType === 'mine' || (!isOwner && (t.id === 'clean' || internalType === 'clean')))) { setInternalMachines([]); if (!isOwner) { setWashItems([]); setDryItems([]); } } setInternalType(t.id); }}""", 'type chips')
rep("""            <p className="text-xs font-bold text-slate-700 mb-1.5">{isOwner ? 'เครื่องที่ทำ' : tr(config, 'เครื่องซักที่จะล้าง')} <span className="text-rose-600">*บังคับ</span> (เลือกได้หลายเครื่อง)</p>""",
    """            <p className="text-xs font-bold text-slate-700 mb-1.5">{isOwner ? 'เครื่องที่ทำ' : internalType === 'clean' ? tr(config, 'เครื่องซักที่จะล้าง') : tr(config, 'เครื่องที่ทำ')} {fixType ? <span className="text-slate-500">({tr(config, 'ถ้ามี')})</span> : <span className="text-rose-600">*{tr(config, 'บังคับ')}</span>} ({tr(config, 'เลือกได้หลายเครื่อง')})</p>""", 'machines header')
rep("""                <p className="text-xs font-bold text-slate-700 mb-1">เหตุผล <span className="text-rose-600">*บังคับ</span></p>
                <input type="text" value={internalReason} onChange={e => setInternalReason(e.target.value)}
                  className={`w-full px-3 py-2.5 rounded-xl border-2 text-sm ${internalReason.trim() ? 'bg-white border-slate-300' : 'bg-rose-50 border-rose-300'}`}
                  placeholder="เช่น ทดสอบหลังช่างซ่อม" />
                <p className="text-xs font-bold text-slate-700 mb-1 mt-3">กำหนดยอดเครดิตเอง (ถ้าไม่เลือกเครื่องด้านล่าง)</p>
                <input type="number" inputMode="numeric" value={internalCustom} onChange={e => setInternalCustom(e.target.value)} onFocus={e => e.target.select()}
                  className="w-full px-3 py-2.5 rounded-xl border-2 border-slate-300 bg-white text-lg font-bold text-right" placeholder="0" />
                <p className="text-[11px] text-slate-600 mt-1">เลือกเครื่อง+อุณหภูมิด้านล่างจะคิดราคาให้เอง · หรือกรอกยอดเองช่องนี้</p>""",
    """                <p className="text-xs font-bold text-slate-700 mb-1">{tr(config, 'เหตุผล')} <span className="text-rose-600">*{tr(config, 'บังคับ')}</span></p>
                <input type="text" value={internalReason} onChange={e => setInternalReason(e.target.value)} data-ireason
                  className={`w-full px-3 py-2.5 rounded-xl border-2 text-sm ${internalReason.trim() ? 'bg-white border-slate-300' : 'bg-rose-50 border-rose-300'}`}
                  placeholder={tr(config, fixType ? 'เช่น เครื่องกินโทเคน ให้ลูกค้าใหม่ 4 อัน' : 'เช่น ทดสอบหลังช่างซ่อม')} />
                <p className="text-xs font-bold text-slate-700 mb-1 mt-3">{tokenShop(config) ? tr(config, fixType ? 'จำนวนโทเคนที่ให้ (บาท)' : 'ยอดโทเคนที่หยอด (ถ้าไม่เลือกเครื่องด้านล่าง)') : 'กำหนดยอดเครดิตเอง (ถ้าไม่เลือกเครื่องด้านล่าง)'}</p>
                <input type="number" inputMode="numeric" value={internalCustom} onChange={e => setInternalCustom(e.target.value)} onFocus={e => e.target.select()} data-icustom
                  className="w-full px-3 py-2.5 rounded-xl border-2 border-slate-300 bg-white text-lg font-bold text-right" placeholder="0" />
                {tokenShop(config) && customAmt > 0 && <p className="text-xs font-extrabold text-slate-800 mt-1">🪙 = {Math.round(customAmt / ((COIN_POINTS[config.brand] || {}).tokenValue || 10) * 10) / 10} {tr(config, 'โทเคน')}</p>}
                <p className="text-[11px] text-slate-600 mt-1">{tr(config, 'เลือกเครื่อง+อุณหภูมิด้านล่างจะคิดราคาให้เอง · หรือกรอกยอดเองช่องนี้')}</p>""", 'reason + amount')

# งานภายในที่กรอกยอดเอง (ไม่เลือกซัก/อบ) บันทึกได้ — เดิมติดเช็ก 'เลือกบริการอย่างน้อย 1 รายการ'
rep("""  const handleSubmit = () => {
    if (!hasAnyItem) {""", """  const handleSubmit = () => {
    if (!hasAnyItem && !(isInternal && customAmt > 0)) {""", 'submit: internal custom amount')
rep("""\\nเครดิตที่ใช้: ฿${formatMoney(total)}\\n\\n⚠️ ไม่นับเป็นรายได้ — ยืนยันไหม?`""",
    """\\n${tokenShop(config) ? 'โทเคนที่ใช้' : 'เครดิตที่ใช้'}: ฿${formatMoney(total)}\\n\\n⚠️ ไม่นับเป็นรายได้ — ยืนยันไหม?`""", 'internal confirm label')
rep("""'🔧 เครดิตที่ใช้ (งานภายใน)')""", """(tokenShop(config) ? '🔧 ' + tr(config, 'โทเคนที่ใช้ (งานภายใน)') : '🔧 เครดิตที่ใช้ (งานภายใน)'))""", 'form bottom label')
rep("""  if (total > 0) rows.push(['เครดิตที่ใช้', `฿${formatMoney(total)}`]);""",
    """  if (total > 0) rows.push([tokenShop(config) ? 'โทเคนที่ใช้' : 'เครดิตที่ใช้', `฿${formatMoney(total)}`]);""", 'internal slip label')
rep("""<p className="text-sm font-bold text-slate-800">⚠️ ไม่นับเป็นรายได้ · เครดิตที่ใช้ ฿{formatMoney(total)}</p>""",
    """<p className="text-sm font-bold text-slate-800">⚠️ ไม่นับเป็นรายได้ · {tokenShop(config) ? 'โทเคนที่ใช้' : 'เครดิตที่ใช้'} ฿{formatMoney(total)}</p>""", 'receipt internal label')

# หน้าเจ้าของ: แถวงานภายในโชว์เหตุผล (โทเคนแก้ปัญหา/ซ่อม ต้องรู้ว่าเพราะอะไร)
rep("""{o.staffName ? ` · ${o.staffName}` : ''}</span>
        <span className="flex flex-wrap gap-1 mt-1">""",
    """{o.staffName ? ` · ${o.staffName}` : ''}</span>
        {internal && o.internalReason ? <span data-ireason-row className="block text-xs text-slate-600 truncate">📝 {o.internalReason}</span> : null}
        <span className="flex flex-wrap gap-1 mt-1">""", 'owner row reason')

# ---------- หน้าแรก (หน้าเดิม): ปุ่มบิลงานร้าน ----------
rep("""          <div className="w-10 h-10 rounded-xl bg-slate-900 flex items-center justify-center text-xl flex-shrink-0">{currentStaff && currentStaff.isOwnerLogin ? '🔧' : '🧼'}</div>
          <div className="text-left flex-1 min-w-0">
            <p className="font-bold text-slate-900 text-sm">{currentStaff && currentStaff.isOwnerLogin ? tr(config, 'งานภายในร้าน (ล้าง/ทดสอบเครื่อง)') : tr(config, 'ล้างเครื่อง')}</p>
            <p className="text-xs text-amber-800">{currentStaff && currentStaff.isOwnerLogin ? tr(config, 'ไม่นับเป็นรายได้ · บังคับใส่เหตุผล') : tr(config, 'เฉพาะเครื่องซัก · เครื่องละ 1 ครั้งต่อ 7 วัน · ไม่นับเป็นรายได้')}</p>""",
    """          <div className="w-10 h-10 rounded-xl bg-slate-900 flex items-center justify-center text-xl flex-shrink-0">{currentStaff && currentStaff.isOwnerLogin ? '🔧' : maidBillTypes(config).length > 1 ? '🔧' : '🧼'}</div>
          <div className="text-left flex-1 min-w-0" data-maid-bill>
            <p className="font-bold text-slate-900 text-sm">{currentStaff && currentStaff.isOwnerLogin ? tr(config, 'งานภายในร้าน (ล้าง/ทดสอบเครื่อง)') : maidBillTypes(config).length > 1 ? tr(config, 'บิลงานร้าน (ไม่ใช่ลูกค้า)') : tr(config, 'ล้างเครื่อง')}</p>
            <p className="text-xs text-amber-800">{currentStaff && currentStaff.isOwnerLogin ? tr(config, 'ไม่นับเป็นรายได้ · บังคับใส่เหตุผล') : maidBillTypes(config).length > 1 ? maidBillTypes(config).map(t => t.emoji + ' ' + tr(config, t.label)).join(' · ') + ' · ' + tr(config, 'ไม่นับเป็นรายได้') : tr(config, 'เฉพาะเครื่องซัก · เครื่องละ 1 ครั้งต่อ 7 วัน · ไม่นับเป็นรายได้')}</p>""", 'home bill button')

# ---------- 🎟️ ลูกค้าใช้โปร: ร้านโทเคน ----------
rep("""          <button onClick={() => setShowPromoForm(true)}
            className="w-full bg-rose-50 rounded-2xl p-3 border-2 border-rose-200 active:scale-95 transition flex items-center gap-3">""",
    """          <button onClick={() => { setShowPromoForm(true); if (tokenShop(config) && config.hasLinePromo && !promoName) { setPromoName(`LINE ลด ${config.linePromoDiscount}฿`); setPromoAmount(String(config.linePromoDiscount)); } }} data-promo-open
            className="w-full bg-rose-50 rounded-2xl p-3 border-2 border-rose-200 active:scale-95 transition flex items-center gap-3">""", 'promo open preselect LINE')
rep("""<p className="font-bold text-rose-900 text-sm">{tr(config, "ลูกค้าใช้โปร (ซักเอง ไม่ฝาก)")}</p>""",
    """<p className="font-bold text-rose-900 text-sm">{tr(config, tokenShop(config) ? 'ลูกค้าใช้คูปองแอดไลน์ (ซักเอง ไม่ฝาก)' : "ลูกค้าใช้โปร (ซักเอง ไม่ฝาก)")}</p>""", 'promo title')
rep("""tr(config, pulseOn(config) ? 'เลือกเครื่อง → ถ่ายรูป → กดเริ่มเครื่อง' : "สแกนเครดิตให้ลูกค้า → ถ่ายรูป → ส่งกลุ่ม")""",
    """tr(config, pulseOn(config) ? 'เลือกเครื่อง → ถ่ายรูป → กดเริ่มเครื่อง' : tokenShop(config) ? 'ให้โทเคนลูกค้า → ถ่ายรูป → ส่งกลุ่ม' : "สแกนเครดิตให้ลูกค้า → ถ่ายรูป → ส่งกลุ่ม")""", 'promo steps', count=2)
rep("""{tr(config, pulseOn(config) ? 'ยอดโปรที่ร้านจ่ายให้ (บาท)' : "ยอดเครดิตที่สแกนให้ลูกค้า (บาท)")}""",
    """{tr(config, pulseOn(config) ? 'ยอดโปรที่ร้านจ่ายให้ (บาท)' : tokenShop(config) ? 'ยอดโทเคนที่ให้ลูกค้า (บาท)' : "ยอดเครดิตที่สแกนให้ลูกค้า (บาท)")}""", 'promo amount label')
rep("""    if (amount <= 0) { alert('ใส่ยอดเครดิตที่สแกนให้ลูกค้า'); return; }""",
    """    if (amount <= 0) { alert(tr(config, tokenShop(config) ? 'ใส่ยอดโทเคนที่ให้ลูกค้า' : 'ใส่ยอดเครดิตที่สแกนให้ลูกค้า')); return; }""", 'promo alert')
rep("""        p.pulseLogId ? `🎁 ${p.promoName} · ⚡ ยิงพัลส์ ${p.amount}฿` : `🎁 ${p.promoName} · เครดิต ${p.amount}฿`,""",
    """        p.pulseLogId ? `🎁 ${p.promoName} · ⚡ ยิงพัลส์ ${p.amount}฿` : `🎁 ${p.promoName} · ${tokenShop(config) ? '🪙 โทเคน' : 'เครดิต'} ${p.amount}฿`,""", 'promo share image')
rep("""savedPromo.pulseLogId ? `⚡ ยิงพัลส์: ${savedPromo.amount}฿ (${savedPromo.pulseStatus === 'confirmed' ? 'เครื่องรับแล้ว' : 'ส่งคำสั่งแล้ว'})` : `💳 เครดิตที่สแกน: ${savedPromo.amount}฿`,""",
    """savedPromo.pulseLogId ? `⚡ ยิงพัลส์: ${savedPromo.amount}฿ (${savedPromo.pulseStatus === 'confirmed' ? 'เครื่องรับแล้ว' : 'ส่งคำสั่งแล้ว'})` : tokenShop(config) ? `🪙 โทเคนที่ให้: ${savedPromo.amount}฿` : `💳 เครดิตที่สแกน: ${savedPromo.amount}฿`,""", 'promo share text')
rep("""{savedPromo.pulseLogId ? tr(config, 'เริ่มเครื่องแล้ว') : tr(config, "บันทึกตัดเครดิตแล้ว")}""",
    """{savedPromo.pulseLogId ? tr(config, 'เริ่มเครื่องแล้ว') : tokenShop(config) ? tr(config, 'บันทึกให้โทเคนแล้ว') : tr(config, "บันทึกตัดเครดิตแล้ว")}""", 'promo saved title')
rep("""savedPromo.pulseLogId ? ['เริ่มเครื่อง', savedPromo.pulseStatus === 'confirmed' ? '⚡ เครื่องรับแล้ว' : '⚡ ส่งคำสั่งแล้ว'] : ['ตัดเครดิต', `${savedPromo.amount}฿`],""",
    """savedPromo.pulseLogId ? ['เริ่มเครื่อง', savedPromo.pulseStatus === 'confirmed' ? '⚡ เครื่องรับแล้ว' : '⚡ ส่งคำสั่งแล้ว'] : [tokenShop(config) ? 'ให้โทเคน' : 'ตัดเครดิต', `${savedPromo.amount}฿`],""", 'promo slip row')

# ---------- เริ่มเครื่อง (ร้านยิงพัลส์): ใช้กติกาเดียวกัน ----------
rep("""INTERNAL_OWNER_ONLY.includes(job.order.internalType) && !owner && !block""",
    """internalOwnerOnly(config).includes(job.order.internalType) && !owner && !block""", 'start sheet owner-only')

# ---------- หน้าเจ้าของ: คูปอง/โปรลูกค้าซักเอง (ร้านไม่มีระบบยิงพัลส์) ----------
rep("""  useEffect(() => { setSelecting(false); setSel(new Set()); setAskPwd(false); }, [tab, mode, anchor]);
  useEffect(() => () => { if (toastTimer.current) clearTimeout(toastTimer.current); }, []);
  const detAll = useMemo(""",
    """  useEffect(() => { setSelecting(false); setSel(new Set()); setAskPwd(false); }, [tab, mode, anchor]);
  useEffect(() => () => { if (toastTimer.current) clearTimeout(toastTimer.current); }, []);
  // 🎟️ v177: ร้านไม่มีระบบยิงพัลส์ (Teddy 1) — บิลลูกค้าใช้คูปอง/โปรซักเอง อยู่ใน creditLedger
  const [selfPromo, setSelfPromo] = useState([]);
  useEffect(() => {
    if (!window.db || machineSys || !menuOn(config, 'promoCredit')) { setSelfPromo([]); return; }
    const u = subscribeToCreditLedger(config.brand, l => setSelfPromo(l.filter(e => e.type === 'promo')));
    return () => { if (u) u(); };
  }, [config.brand, machineSys]);
  const detAll = useMemo(""", 'owner selfPromo hook')
rep("""            {listHead(`ใบงานที่มีส่วนลด · ${R.label}`, A.discN)}""",
    """            {!machineSys && menuOn(config, 'promoCredit') && (() => {
              const sp = selfPromo.filter(e => { const x = t2Ts(e.createdAt); return x >= R.from && x < R.to; }).sort((a, b) => t2Ts(b.createdAt) - t2Ts(a.createdAt));
              const spSum = sp.reduce((a2, e) => a2 + (e.amount || 0), 0);
              return (
                <T2Box k="discount" title={`🎟️ ลูกค้าซักเอง ใช้คูปอง/โปร · ${R.label}`} right={<span className="text-xs font-bold text-slate-500 tabular-nums">฿{formatMoney(spSum)} · {sp.length} ใบ</span>}>
                  <div data-self-promo className="divide-y divide-slate-100">
                    {sp.map(e => (
                      <div key={e.id} className="flex items-center gap-2 py-2">
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-extrabold text-slate-900 truncate">{e.promoName || 'โปร'}{e.machine ? ' · ' + e.machine : ''}</p>
                          <p className="text-xs text-slate-500 truncate">{t2When(e.createdAt)} · {e.staffName || '-'}{e.note ? ' · ' + e.note : ''}</p>
                        </div>
                        <span className="text-sm font-extrabold tabular-nums">฿{formatMoney(e.amount || 0)}</span>
                        <button onClick={async () => { if (!confirm(`ลบรายการนี้?\\n🎟️ ${e.promoName || 'โปร'} ฿${formatMoney(e.amount || 0)} · ${e.staffName || '-'}`)) return; await deleteCreditEntry(e.id); }}
                          className="px-2 py-1 rounded-lg border border-slate-200 text-xs font-bold text-slate-500 active:scale-95">ลบ</button>
                      </div>
                    ))}
                    {sp.length === 0 && <p className="text-sm text-slate-500 py-1">ยังไม่มี · แม่บ้านกด 🎟️ ลูกค้าใช้คูปองแอดไลน์ ที่หน้าแรก</p>}
                  </div>
                  <p className="text-[11px] text-slate-500 mt-1.5">ให้โทเคนลูกค้าซักเอง (ไม่ใช่งานฝาก) · ลงบัญชีเป็นรายจ่ายส่วนลดแอดไลน์</p>
                </T2Box>
              );
            })()}
            {listHead(`ใบงานที่มีส่วนลด · ${R.label}`, A.discN)}""", 'owner self promo box')

# ---------- คำแปลพม่า (ข้อความที่แม่บ้านเห็น) ----------
MM_NEW = {
    'โทเคนแก้ปัญหา': 'ပြဿနာဖြေရှင်း တိုကင်',
    'ซ่อม/ทดสอบเครื่อง': 'စက်ပြင်/စမ်းသပ်',
    'บิลงานร้าน (ไม่ใช่ลูกค้า)': 'ဆိုင်အလုပ် ဘောက်ချာ (ဖောက်သည် မဟုတ်)',
    'ไม่นับเป็นรายได้': 'ဝင်ငွေအဖြစ် မရေတွက်',
    'เครื่องที่ทำ': 'လုပ်ဆောင်သည့်စက်',
    'ถ้ามี': 'ရှိလျှင်',
    'บังคับ': 'မဖြစ်မနေ',
    'เลือกได้หลายเครื่อง': 'စက်အများ ရွေးနိုင်',
    'เหตุผล': 'အကြောင်းပြချက်',
    'เช่น ทดสอบหลังช่างซ่อม': 'ဥပမာ - ပြင်ပြီးနောက် စမ်းသပ်',
    'เช่น เครื่องกินโทเคน ให้ลูกค้าใหม่ 4 อัน': 'ဥပမာ - စက်က တိုကင်စား၍ ဖောက်သည်ကို ၄ ခု ပြန်ပေး',
    'จำนวนโทเคนที่ให้ (บาท)': 'ပေးသော တိုကင် (ဘတ်)',
    'ยอดโทเคนที่หยอด (ถ้าไม่เลือกเครื่องด้านล่าง)': 'ထည့်သော တိုကင် (အောက်တွင် စက်မရွေးလျှင်)',
    'เลือกเครื่อง+อุณหภูมิด้านล่างจะคิดราคาให้เอง · หรือกรอกยอดเองช่องนี้': 'အောက်တွင် စက်+အပူချိန် ရွေးလျှင် ဈေးတွက်ပေးမည် · သို့မဟုတ် ဤနေရာတွင် ဖြည့်ပါ',
    'โทเคน': 'တိုကင်',
    'ใส่เหตุผล (บังคับ)': 'အကြောင်းပြချက် ဖြည့်ပါ (မဖြစ်မနေ)',
    'เลือกเครื่องที่ทำ (บังคับ)': 'လုပ်ဆောင်သည့်စက် ရွေးပါ (မဖြစ်မနေ)',
    'เลือกเครื่อง (ซัก/อบ) หรือกรอกยอดเครดิตเอง': 'စက် (လျှော်/အခြောက်ခံ) ရွေးပါ သို့မဟုတ် ပမာဏ ဖြည့်ပါ',
    'กรอกจำนวนโทเคนที่ให้': 'ပေးသော တိုကင် ပမာဏ ဖြည့်ပါ',
    'ลูกค้าใช้คูปองแอดไลน์ (ซักเอง ไม่ฝาก)': 'ဖောက်သည် LINE ကူပွန်သုံး (ကိုယ်တိုင်လျှော် မအပ်)',
    'ให้โทเคนลูกค้า → ถ่ายรูป → ส่งกลุ่ม': 'ဖောက်သည်ကို တိုကင်ပေး → ဓာတ်ပုံရိုက် → Group ပို့',
    'ยอดโทเคนที่ให้ลูกค้า (บาท)': 'ဖောက်သည်ကို ပေးသော တိုကင် (ဘတ်)',
    'ใส่ยอดโทเคนที่ให้ลูกค้า': 'ဖောက်သည်ကို ပေးသော တိုကင် ဖြည့်ပါ',
    'บันทึกให้โทเคนแล้ว': 'တိုကင်ပေးမှု သိမ်းပြီး',
    'โทเคนที่ใช้ (งานภายใน)': 'သုံးသော တိုကင် (ဆိုင်တွင်းအလုပ်)',
}
start = s.index('const MM_DICT = {')
end = s.index('\n};\nfunction tr(config, th) {', start)
existing = set(re.findall(r"^  '((?:[^'\\]|\\.)*)':", s[start:end], re.M))
add = ''.join(f"  '{k}': '{v}', // v177\n" for k, v in MM_NEW.items() if k not in existing)
skipped = [k for k in MM_NEW if k in existing]
s = s[:end] + '\n' + add.rstrip('\n') + s[end:]

open(IDX, 'w', encoding='utf-8').write(s)
open(SW, 'w', encoding='utf-8').write(sw)
print('v177 applied · MM added', len(MM_NEW) - len(skipped), 'skipped (exists)', skipped)
