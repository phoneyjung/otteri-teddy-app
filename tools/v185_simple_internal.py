#!/usr/bin/env python3
"""v185 — Otteri งานภายใน 4 แบบ + ฟอร์มสั้น (แอดมิน/เจ้าของ)
ที่มา: เจ้าของ 2 พ.ย. 69 (รูปฟอร์มงานภายในยาว: เวลา · โปรดึก · เครื่องซัก/อบทุกขนาด)
  'ล้างเครื่อง · ซ่อมทดสอบ · ปัญหาอื่นๆ/ซักซ่ำ · ผ้าเจ้าของ — แก้ให้มี แค่ 4 งานนี้ พอ' · 'แก้ให้ใส่เท่าที่จำเป็นพอ'
ทำอะไร (เฉพาะร้านที่ตั้ง config.simpleInternal = Otteri)
  - หน้าแอดมิน: 4 ปุ่ม (ล้างเครื่อง · ซ่อม/ทดสอบ · ปัญหาอื่นๆ/ซักซ้ำ · ผ้าเจ้าของ) · เอาปุ่มร้านเกอิชาออก
  - 'อื่นๆ' ใช้ชื่อ 'ปัญหาอื่นๆ / ซักซ้ำ' (config.internalLabels) · ซักซ้ำ (redo) ไม่ให้เลือกใหม่
  - ฟอร์มแอดมิน/เจ้าของ: หัว = ชื่องาน · ชิป 4 งาน · แตะเครื่อง (ล้างเครื่อง = เครื่องซักเท่านั้น) → แอปใส่รายการ+ราคาให้เอง
    ซ่อม/ปัญหา = ช่องเหตุผลช่องเดียว (ไม่มีช่องกรอกยอดเอง) · ไม่มีกล่องเวลาใหญ่ (มีปุ่มเล็ก 'ลงย้อนหลัง แตะเปลี่ยนเวลา')
    ไม่มีป้ายโปร · ไม่มีส่วนเครื่องซัก/อบทุกขนาด
  - งานภายในร้านนี้ไม่คิดโปรวัน/ดึก (ราคา = ราคาเครื่อง = ยอดที่ติ๊ก SOL)
usage: python3 tools/v185_simple_internal.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v184-2026-11-02';", "window.APP_VERSION = 'v185-2026-11-02';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v184';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v184';", "const CACHE_NAME = 'plp-laundry-v185';")

# ---------- config + helper ----------
rep("""  maidNoFree: true, //""",
    """  simpleInternal: ['clean', 'test', 'other', 'mine'], // 🧾 v185 งานภายในที่ลงได้ (แอดมิน/เจ้าของ ฟอร์มสั้น)
  internalLabels: { other: 'ปัญหาอื่นๆ / ซักซ้ำ' },
  maidNoFree: true, //""", 'config otteri')
rep("""const internalTitleOf = (o, config, noEmoji) => { const t = INTERNAL_TYPES.find(x => x.id === o.internalType) || {}; const ms = (o.internalMachines || []).map(m => String(m).replace(/^(ซัก|อบ) /, '')); return `${noEmoji ? '' : (t.emoji || '🔧') + ' '}${tr(config, t.label || 'งานภายใน')}${ms.length ? ' · ' + ms.join(', ') : ''}`; };""",
    """// 🧾 v185 ชื่องานภายในต่อร้าน (Otteri: อื่นๆ = 'ปัญหาอื่นๆ / ซักซ้ำ')
const internalLabelOf = (config, id) => (config && config.internalLabels && config.internalLabels[id]) || (INTERNAL_TYPES.find(t => t.id === id) || {}).label || id || '';
const internalTitleOf = (o, config, noEmoji) => { const t = INTERNAL_TYPES.find(x => x.id === o.internalType) || {}; const ms = (o.internalMachines || []).map(m => String(m).replace(/^(ซัก|อบ) /, '')); return `${noEmoji ? '' : (t.emoji || '🔧') + ' '}${tr(config, (o.internalType && internalLabelOf(config, o.internalType)) || 'งานภายใน')}${ms.length ? ' · ' + ms.join(', ') : ''}`; };""", 'internalLabelOf')
rep("""title: kind === 'internal' ? (it.label || order.internalType) : null,""",
    """title: kind === 'internal' ? internalLabelOf(config, order.internalType) : null,""", 'slip title')
rep("""                  <T2Stat key={t.id} label={`${t.emoji} ${t.label}`} value={'฿' + formatMoney((A.intType[t.id] || {}).v || 0)}""",
    """                  <T2Stat key={t.id} label={`${t.emoji} ${internalLabelOf(config, t.id)}`} value={'฿' + formatMoney((A.intType[t.id] || {}).v || 0)}""", 'owner stat label')

# ---------- หน้าแอดมิน: 4 ปุ่ม ----------
rep("""const ADMIN_BTN_SUB = { clean: 'ล้างถังเครื่องซัก', test: 'ตอนช่างมา/เช็กเครื่อง', redo: 'เครื่องมีปัญหา ซักให้ใหม่', mine: 'ไม่นับรายได้', other: 'ใส่เหตุผล' };""",
    """const ADMIN_BTN_SUB = { clean: 'ล้างถังเครื่องซัก', test: 'ตอนช่างมา/เช็กเครื่อง', redo: 'เครื่องมีปัญหา ซักให้ใหม่', mine: 'ไม่นับรายได้', other: 'ใส่เหตุผล' };
const ADMIN_BTN_SUB2 = { other: 'เครื่องมีปัญหา / ซักให้ลูกค้าใหม่' }; // v185 ร้านที่รวม อื่นๆ + ซักซ้ำ""", 'ADMIN_BTN_SUB2')
rep("""    ...internalTypesFor(config).filter(t => t.id !== 'fix').map(t => ({ k: t.id, icon: t.emoji, title: tr(config, (BILL_BTN[t.id] || [t.label])[0]), sub: tr(config, ADMIN_BTN_SUB[t.id] || 'ไม่นับรายได้'), click: () => onInternalOrder(t.id) })),
    ...(config.accounts || []).filter(a => a.noRevenue).map(a =>""",
    """    ...(config.simpleInternal ? config.simpleInternal.map(id => INTERNAL_TYPES.find(t => t.id === id)).filter(Boolean).map(t => ({ k: t.id, icon: t.emoji, title: tr(config, t.id === 'clean' || t.id === 'test' ? BILL_BTN[t.id][0] : internalLabelOf(config, t.id)), sub: tr(config, ADMIN_BTN_SUB2[t.id] || ADMIN_BTN_SUB[t.id] || 'ไม่นับรายได้'), click: () => onInternalOrder(t.id) }))
      : internalTypesFor(config).filter(t => t.id !== 'fix').map(t => ({ k: t.id, icon: t.emoji, title: tr(config, (BILL_BTN[t.id] || [t.label])[0]), sub: tr(config, ADMIN_BTN_SUB[t.id] || 'ไม่นับรายได้'), click: () => onInternalOrder(t.id) }))),
    ...(config.simpleInternal ? [] : config.accounts || []).filter(a => a.noRevenue).map(a =>""", 'admin 4 buttons')

# ---------- ฟอร์มสั้น ----------
rep("""  const freeOk = isOwner || !!isAdmin; // 🔧 v181 แอดมิน = ลงงานภายใน/งานไม่คิดเงินได้ (เดิมใช้ isOwner ทั้งฟอร์ม)""",
    """  const freeOk = isOwner || !!isAdmin; // 🔧 v181 แอดมิน = ลงงานภายใน/งานไม่คิดเงินได้ (เดิมใช้ isOwner ทั้งฟอร์ม)
  const [showTime, setShowTime] = useState(false); // 🧾 v185 ฟอร์มสั้น: กล่องเวลาเปิดเมื่อแตะ""", 'showTime state')
rep("""  const maidClean = !!internalType && internalType === 'clean' && !isOwner; // v181 แอดมินใช้ฟอร์มล้างเครื่องแบบง่าย (แตะเครื่องซัก = ใส่รายการให้) เหมือนแม่บ้าน
  useEffect(() => {
    if (!maidClean) return;
    const allM = (COIN_POINTS[config.brand] || COIN_POINTS.teddy2).machines || [];
    const bySize = {};
    allM.filter(m => /^w/i.test(m.id) && internalMachines.includes(m.label)).forEach(m => { const kg = parseInt(m.size, 10) || 0; bySize[kg] = (bySize[kg] || 0) + 1; });
    const items = Object.keys(bySize).map(kg => ({ size: Number(kg), temp: 'hot', qty: bySize[kg] })).filter(i => config.washMachines.some(w => w.size === i.size));
    setWashItems(items);
    setDryItems([]);
  }, [maidClean, internalMachines.join('|')]);""",
    """  const maidClean = !!internalType && internalType === 'clean' && !isOwner; // v181 แอดมินใช้ฟอร์มล้างเครื่องแบบง่าย (แตะเครื่องซัก = ใส่รายการให้) เหมือนแม่บ้าน
  // 🧾 v185 ฟอร์มสั้น (แอดมิน/เจ้าของ ร้าน simpleInternal): แตะเครื่อง = แอปใส่รายการ+ราคาให้ (ซัก/อบ)
  const simpleFree = !!internalType && freeOk && !!config.simpleInternal && internalType !== 'fix';
  const autoItems = maidClean || simpleFree;
  useEffect(() => {
    if (!autoItems) return;
    const allM = (COIN_POINTS[config.brand] || COIN_POINTS.teddy2).machines || [];
    const wBy = {}, dBy = {};
    allM.filter(m => internalMachines.includes(m.label)).forEach(m => { const kg = parseInt(m.size, 10) || 0; if (/^w/i.test(m.id)) wBy[kg] = (wBy[kg] || 0) + 1; else if (/^d/i.test(m.id)) dBy[kg] = (dBy[kg] || 0) + 1; });
    const temp = internalType === 'clean' ? 'hot' : 'cold';
    setWashItems(Object.keys(wBy).map(kg => ({ size: Number(kg), temp, qty: wBy[kg] })).filter(i => config.washMachines.some(w => w.size === i.size)));
    setDryItems(internalType === 'clean' ? [] : Object.keys(dBy).map(kg => ({ size: Number(kg), qty: dBy[kg] })).filter(i => config.dryMachines.some(d => d.size === i.size)));
  }, [autoItems, internalType, internalMachines.join('|')]);""", 'auto items effect')
rep("""    noDayPromo: editingOrder ? (editingOrder.noDayPromo || false) : (config.dayPromoEnabled === false || !!acct), // 🏢 ค้างจ่าย = ราคาปกติ""",
    """    noDayPromo: editingOrder ? (editingOrder.noDayPromo || false) : (config.dayPromoEnabled === false || !!acct || (!!internalType && !!config.simpleInternal)), // 🏢 ค้างจ่าย = ราคาปกติ · v185 งานภายใน = ราคาเครื่อง""", 'noDayPromo internal', count=2)
rep("""  if (isInternal && internalType !== 'mine' && !fixType && internalMachines.length === 0) missingList.push(tr(config, 'เลือกเครื่องที่ทำ (บังคับ)'));
  if (internalType === 'mine' && !washItems.length && !dryItems.length) missingList.push""",
    """  if (isInternal && (internalType !== 'mine' || simpleFree) && !fixType && internalMachines.length === 0) missingList.push(tr(config, 'เลือกเครื่องที่ทำ (บังคับ)'));
  if (internalType === 'mine' && !simpleFree && !washItems.length && !dryItems.length) missingList.push""", 'missing machines')
rep("""        {freeOk && (
          <div className="rounded-2xl p-4 shadow-lg border-2 border-amber-300" style={{background: 'linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%)'}}>""",
    """        {simpleFree && !showTime && (
          <button data-time-toggle onClick={() => setShowTime(true)} className="w-full text-left text-xs font-bold text-slate-500 px-1">
            🕐 {tr(config, 'เวลา: ตอนนี้')} · <span className="underline">{tr(config, 'ลงย้อนหลัง แตะเปลี่ยนเวลา')}</span>
          </button>
        )}
        {freeOk && (!simpleFree || showTime) && (
          <div className="rounded-2xl p-4 shadow-lg border-2 border-amber-300" style={{background: 'linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%)'}}>""", 'time block compact')
rep("""        {breakdown.promo.active && (""", """        {breakdown.promo.active && !isInternal && (""", 'promo banner hide')
rep("""<p className="font-extrabold text-slate-900">{freeOk ? '🔧 งานภายในร้าน' : (() => { const it = INTERNAL_TYPES.find(x => x.id === internalType) || INTERNAL_TYPES[0]; return it.emoji + ' ' + tr(config, it.label); })()}</p>""",
    """<p className="font-extrabold text-slate-900" data-itype-title>{freeOk && !simpleFree ? '🔧 งานภายในร้าน' : (() => { const it = INTERNAL_TYPES.find(x => x.id === internalType) || INTERNAL_TYPES[0]; return it.emoji + ' ' + tr(config, internalLabelOf(config, it.id)); })()}</p>""", 'title')
rep("""              <button onClick={() => { setInternalType(''); setInternalReason(''); setInternalCustom(''); }}
                className="text-[11px] font-bold text-slate-600 bg-white rounded-lg px-2 py-1">เปลี่ยนเป็นงานลูกค้า</button>""",
    """              {!simpleFree && <button onClick={() => { setInternalType(''); setInternalReason(''); setInternalCustom(''); }}
                className="text-[11px] font-bold text-slate-600 bg-white rounded-lg px-2 py-1">เปลี่ยนเป็นงานลูกค้า</button>}""", 'hide to-customer')
rep("""              {internalTypesFor(config).filter(t => freeOk || !internalOwnerOnly(config).includes(t.id)).map(t => {""",
    """              {(simpleFree ? config.simpleInternal.map(id => INTERNAL_TYPES.find(t => t.id === id)).filter(Boolean) : internalTypesFor(config)).filter(t => freeOk || !internalOwnerOnly(config).includes(t.id)).map(t => {""", 'chips 4')
rep("""{locked ? '🔒' : t.emoji} {freeOk ? t.label : tr(config, t.label)}""",
    """{locked ? '🔒' : t.emoji} {freeOk ? internalLabelOf(config, t.id) : tr(config, internalLabelOf(config, t.id))}""", 'chip label')
rep("""            {internalType === 'mine' && <p className="text-[11px] font-bold text-slate-700 mb-1">""",
    """            {internalType === 'mine' && !simpleFree && <p className="text-[11px] font-bold text-slate-700 mb-1">""", 'mine note')
rep("""            {internalType !== 'mine' && <React.Fragment>""", """            {(internalType !== 'mine' || simpleFree) && <React.Fragment>""", 'machines for mine')
rep("""const dryNo = internalType === 'clean' && !isOwner && /^d/i.test(m.id);""",
    """const dryNo = internalType === 'clean' && (!isOwner || simpleFree) && /^d/i.test(m.id);""", 'dryNo simple')
rep("""            {maidClean && (
              <div className="rounded-xl bg-white border-2 border-rose-200 px-3 py-2 mb-2">""",
    """            {simpleFree && internalType !== 'clean' && (
              <div className="rounded-xl bg-white border-2 border-slate-200 px-3 py-2 mb-2" data-simple-items>
                {washItems.length || dryItems.length
                  ? <p className="text-xs font-bold text-slate-700">{[...washItems.map(i => `${tr(config, 'ซัก')} ${i.size}kg × ${i.qty}`), ...dryItems.map(i => `${tr(config, 'อบ')} ${i.size}kg × ${i.qty}`)].join(' · ')} · ฿{formatMoney(total)}</p>
                  : <p className="text-xs text-slate-500">{tr(config, 'แตะเครื่องที่ทำด้านบน')}</p>}
              </div>
            )}
            {maidClean && (
              <div className="rounded-xl bg-white border-2 border-rose-200 px-3 py-2 mb-2">""", 'simple items box')
rep("""                <p className="text-xs font-bold text-slate-700 mb-1 mt-3">{tokenShop(config)""",
    """                {!simpleFree && <React.Fragment>
                <p className="text-xs font-bold text-slate-700 mb-1 mt-3">{tokenShop(config)""", 'custom amt open')
rep("""                <p className="text-[11px] text-slate-600 mt-1">{tr(config, 'เลือกเครื่อง+อุณหภูมิด้านล่างจะคิดราคาให้เอง · หรือกรอกยอดเองช่องนี้')}</p>""",
    """                <p className="text-[11px] text-slate-600 mt-1">{tr(config, 'เลือกเครื่อง+อุณหภูมิด้านล่างจะคิดราคาให้เอง · หรือกรอกยอดเองช่องนี้')}</p>
                </React.Fragment>}""", 'custom amt close')
rep("""<p className="text-[11px] text-slate-700">{maidClean ? tr(config, 'กดบันทึกด้านล่าง แล้วกดเริ่มเครื่องได้เลย') : internalType === 'mine' ? '' : 'เลือกเครื่องด้านล่างได้เลย — ไม่ต้องกรอกเหตุผล/ราคา'}</p>""",
    """<p className="text-[11px] text-slate-700">{simpleFree ? tr(config, 'แตะเครื่อง แล้วกดบันทึก — แอปติ๊กเริ่มเครื่องให้เอง') : maidClean ? tr(config, 'กดบันทึกด้านล่าง แล้วกดเริ่มเครื่องได้เลย') : internalType === 'mine' ? '' : 'เลือกเครื่องด้านล่างได้เลย — ไม่ต้องกรอกเหตุผล/ราคา'}</p>""", 'hint simple')
rep("""        {!maidClean && <Section iconName="droplet" title={tr(config, "เครื่องซัก")}>""",
    """        {!autoItems && <Section iconName="droplet" title={tr(config, "เครื่องซัก")}>""", 'hide wash section')
rep("""        {!maidClean && <Section iconName="wind" title={tr(config, "เครื่องอบ")}>""",
    """        {!autoItems && <Section iconName="wind" title={tr(config, "เครื่องอบ")}>""", 'hide dry section')
# ปุ่มบันทึกในฟอร์มสั้น: เหตุผลช่องเดียวสำหรับ ซ่อม/ปัญหา — placeholder ตามงาน
rep("""placeholder={tr(config, fixType ? 'เช่น เครื่องกินโทเคน ให้ลูกค้าใหม่ 4 อัน' : 'เช่น ทดสอบหลังช่างซ่อม')} />""",
    """placeholder={tr(config, fixType ? 'เช่น เครื่องกินโทเคน ให้ลูกค้าใหม่ 4 อัน' : internalType === 'other' && simpleFree ? 'เช่น เครื่องหยุดกลางคัน ซักให้ลูกค้าใหม่' : 'เช่น ทดสอบหลังช่างซ่อม')} />""", 'reason placeholder')

# ---------- MM ----------
rep("""  'จัดการรายชื่อ': 'ဝန်ထမ်းစာရင်း စီမံရန်',""",
    """  'จัดการรายชื่อ': 'ဝန်ထမ်းစာရင်း စီမံရန်',
  // v185 ฟอร์มงานภายในแบบสั้น
  'ปัญหาอื่นๆ / ซักซ้ำ': 'အခြားပြဿနာ / ပြန်လျှော်',
  'เครื่องมีปัญหา / ซักให้ลูกค้าใหม่': 'စက်ပြဿနာ / ဖောက်သည်အတွက် ပြန်လျှော်',
  'เวลา: ตอนนี้': 'အချိန်: ယခု',
  'ลงย้อนหลัง แตะเปลี่ยนเวลา': 'နောက်ကြောင်းပြန်ထည့်ရန် အချိန်ပြောင်းပါ',
  'แตะเครื่องที่ทำด้านบน': 'အပေါ်ရှိ စက်ကို နှိပ်ပါ',
  'แตะเครื่อง แล้วกดบันทึก — แอปติ๊กเริ่มเครื่องให้เอง': 'စက်ကိုနှိပ်ပြီး သိမ်းပါ — အက်ပ်က စက်စတင်ကြောင်း အလိုအလျောက် မှတ်ပေးမည်',
  'เช่น เครื่องหยุดกลางคัน ซักให้ลูกค้าใหม่': 'ဥပမာ စက်လမ်းခုလတ်ရပ် ဖောက်သည်အတွက် ပြန်လျှော်',""", 'MM')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v185 applied')
