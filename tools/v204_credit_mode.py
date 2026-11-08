#!/usr/bin/env python3
"""v204 — Teddy 2 กลับไปใช้ 'ตัดเครดิต' (แม่บ้านแต่ละคนจ่ายด้วยเครดิตของตัวเองที่ตู้) · แอปไม่ติดต่อเว็บ EC อีก
ที่มา: เจ้าของ 8 พ.ย. 69 (EC กันโปรแกรมตั้งแต่ล็อกอินครั้งแรกของ user ใหม่ · เจ้าของลบ EC_USER/EC_PASS ออกจาก Worker แล้ว)
  'ต้องใช้วิธีใหม่แล้ว วางระบบใหม่ แบบใช้ตัดเครดิต เหมือนเดิม แล้วกระทบยอดในแอปเอา
   ผมจะค่อยดึงข้อมูลการใช้เครดิตมาให้คุณกระทบยอดให้'
  ตอบคำถาม: แม่บ้านแต่ละคนมีบัญชีเครดิตของตัวเอง · เงินสด = หยอดเหรียญ (เงินลูกค้า) ส่วนโอน = ตัดเครดิต ·
            ในแอปแตะเครื่อง + '🎟️ ตัดเครดิตแล้ว'
ทำอะไร
  - TEDDY2 pulse.mode = 'credit' → isCredit(config)
  - firePulse → creditRecordStart(): pulseLog method/status 'credit' + staffName = แม่บ้านที่ล็อกอิน (เจ้าของบัญชีเครดิต)
    ไม่เรียก Worker · PULSE_LIVE รวม 'credit' (นับว่าเริ่มเครื่องแล้ว)
  - ไม่อ่านเว็บ EC เลย: fetchEcDay / refreshEc / checkCoinLog คืนค่าทันที · ปุ่ม 🔄 เช็กกับเครื่อง ซ่อน
  - ข้อความหน้าเริ่มเครื่อง/ยืนยัน/ผลลัพธ์/โปรซักเอง: '🎟️ ตัดเครดิต' แทน '⚡ ยิงพัลส์' · ขั้นตอน 'จ่ายด้วยเครดิตของตัวเองที่ตู้ จนเครื่องเริ่มทำงาน แล้วกดตกลง'
  - ปุ่มรอง 🪙 หยอดเหรียญร้านแทน = 'เครดิตหมด → หยอดเหรียญร้านแทน'
  - หยอดเหรียญ: ไม่มีชิป 🕐 รอเช็กกับเครื่อง / ปุ่มเช็กเหรียญ (เหลือปุ่มยกเลิก) · แจ้งปัญหาเครื่องได้เลย
  - กระทบยอด: แถว 'ตัดเครดิต' + '🪙 หยอดเหรียญ' แทน 'เครื่องจริง (EC)' · หน้าแรก '🎟️ ฿ · 🪙 ฿'
  - 🎟️ เครดิต (เจ้าของ): ยอดใช้ของแต่ละคน = pulseLogs method 'credit' ของคนนั้น (งานฝาก/ส่ง/ภายใน/โปร · คืนเครดิตแล้วยังนับ เพราะเครดิตถูกตัดไปแล้ว)
  - ⚙️ ตั้งค่า: การ์ด '🎟️ เริ่มเครื่องในแอป (โหมดตัดเครดิต)' ไม่มีปุ่มทดสอบ Worker
usage: python3 tools/v204_credit_mode.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v203-2026-11-08';", "window.APP_VERSION = 'v204-2026-11-08';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v203';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v203';", "const CACHE_NAME = 'plp-laundry-v204';")

# ---------- MM ----------
rep("""  'เช็กกับเครื่องอัตโนมัติ 13:00 และ 20:00': 'စက်နှင့် အလိုအလျောက် စစ်ချိန် 13:00 နှင့် 20:00', // v203
""", """  'เช็กกับเครื่องอัตโนมัติ 13:00 และ 20:00': 'စက်နှင့် အလိုအလျောက် စစ်ချိန် 13:00 နှင့် 20:00', // v203
  'ตัดเครดิต': 'ခရက်ဒစ်ဖြင့် ပေး', // v204
  'ตัดเครดิตแล้ว': 'ခရက်ဒစ်ဖြင့် ပေးပြီး', // v204
  'ยืนยันตัดเครดิต': 'ခရက်ဒစ်ဖြင့် ပေးကြောင်း အတည်ပြု', // v204
  'เริ่มเครื่อง (ตัดเครดิต)': 'စက်စတင် (ခရက်ဒစ်)', // v204
  'จ่ายด้วยเครดิตของตัวเองที่ตู้ จนเครื่องเริ่มทำงาน แล้วกดตกลง': 'စက်တွင် ကိုယ်ပိုင်ခရက်ဒစ်ဖြင့် ပေးပါ၊ စက်စလည်ပြီးမှ OK နှိပ်ပါ', // v204
  'หยอดเหรียญ + จ่ายด้วยเครดิตของตัวเองที่ตู้ จนเครื่องเริ่มทำงาน แล้วกดตกลง': 'အကြွေစေ့ထည့် + ကိုယ်ပိုင်ခရက်ဒစ်ဖြင့် ပေးပါ၊ စက်စလည်ပြီးမှ OK နှိပ်ပါ', // v204
  'ขั้นตอน: ใส่ผ้า → ปิดประตู → เลือกโปรแกรม → จ่ายด้วยเครดิตของตัวเองที่ตู้ → เครื่องเดินแล้วกดปุ่มด้านล่าง': 'အဆင့်: အဝတ်ထည့် → တံခါးပိတ် → ပရိုဂရမ်ရွေး → ကိုယ်ပိုင်ခရက်ဒစ်ဖြင့် ပေး → စက်လည်ပြီးမှ အောက်ခလုတ်နှိပ်', // v204
  'เครดิตหมด → หยอดเหรียญร้านแทน': 'ခရက်ဒစ်ကုန် → ဆိုင်အကြွေစေ့ ထည့်ပါ', // v204
  'ตัดเครดิตของตัวเองที่ตู้': 'စက်တွင် ကိုယ်ပိုင်ခရက်ဒစ်ဖြင့် ပေး', // v204
""", 'MM')

# ---------- config ----------
rep("""washBusyMin: 45, ecSince: '2026-11-09', ecSlots: [13, 20] }, // ⚡ ยิงพัลส์ผ่านระบบ EC""",
    """washBusyMin: 45, ecSince: '2026-11-09', ecSlots: [13, 20], mode: 'credit' }, // 🎟️ v204 mode 'credit' = แม่บ้านจ่ายด้วยเครดิตของตัวเองที่ตู้ แล้วกดบันทึก (EC กันโปรแกรม 8 พ.ย. — แอปไม่ติดต่อ EC) · เดิม ⚡ ยิงพัลส์ผ่านระบบ EC""",
    'config')

# ---------- helpers ----------
rep("""const isSol = (config) => !!(config && config.pulse && config.pulse.mode === 'sol'); // 🟦 Otteri: เริ่มเครื่องผ่าน SOL""",
    """const isSol = (config) => !!(config && config.pulse && config.pulse.mode === 'sol'); // 🟦 Otteri: เริ่มเครื่องผ่าน SOL
const isCredit = (config) => !!(config && config.pulse && config.pulse.mode === 'credit'); // 🎟️ v204 Teddy 2: ตัดเครดิตที่ตู้ (ไม่ติดต่อ EC)""", 'isCredit')
rep("""const PULSE_LIVE = ['confirmed', 'forced', 'sent', 'unknown', 'sending', 'coin', 'manual'];""",
    """const PULSE_LIVE = ['confirmed', 'forced', 'sent', 'unknown', 'sending', 'coin', 'manual', 'credit']; // v204 credit = แม่บ้านตัดเครดิตที่ตู้""", 'PULSE_LIVE')
rep("""const pulseIsManual = (l) => !!(l && l.method === 'manual');""",
    """const pulseIsManual = (l) => !!(l && l.method === 'manual');
const pulseIsCredit = (l) => !!(l && l.method === 'credit'); // 🎟️ v204
// 🎟️ v204 บันทึกว่าแม่บ้านจ่ายด้วยเครดิตของตัวเองที่ตู้แล้ว (แทนการยิงพัลส์) — staffName = เจ้าของบัญชีเครดิต
function creditRecordStart(config, { machine, pulses, refType, refId, slotKey, refLabel, retryOf, meta }) {
  const staff = currentStaffLS(config);
  const now = Date.now();
  const id = `${config.brand}-credit-${now}-${Math.random().toString(36).slice(2, 8)}`;
  const log = cleanUndefined({
    brand: config.brand, dateKey: dateKeyOf(new Date(now)), machine, machineLabel: pulseMachineLabel(config, machine),
    pulses, baht: pulses * PULSE_BAHT, method: 'credit', status: 'credit',
    refType, refId: refId || null, slotKey: slotKey || null, refLabel: refLabel || '', retryOf: retryOf || null,
    staffId: staff && staff.id ? staff.id : null, staffName: staff && staff.name ? staff.name : '',
    createdAt: now, doneAt: now, ...(meta || {}),
  });
  pulseLogRef(id).set(log).catch(e => console.error('credit log error:', e));
  return { id, ...log };
}""", 'pulseIsCredit')

# ---------- ไม่ติดต่อ EC ----------
rep("""  if (isSol(config)) return solRecordStart(config, { machine, pulses, refType, refId, slotKey, refLabel, meta }); // 🟦 ไม่สั่งเครื่อง""",
    """  if (isSol(config)) return solRecordStart(config, { machine, pulses, refType, refId, slotKey, refLabel, meta }); // 🟦 ไม่สั่งเครื่อง
  if (isCredit(config)) return creditRecordStart(config, { machine, pulses, refType, refId, slotKey, refLabel, retryOf, meta }); // 🎟️ v204 ไม่สั่งเครื่อง""", 'firePulse')
rep("""  if (isSol(config)) return { ok: true, seen: false };""",
    """  if (isSol(config) || isCredit(config)) return { ok: true, seen: false }; // v204 โหมดตัดเครดิตไม่อ่าน EC""", 'checkCoinLog')
rep("""  if (isSol(config)) return { byMachine: {}, errors: [], at: Date.now() };""",
    """  if (isSol(config) || isCredit(config)) return { byMachine: {}, errors: [], at: Date.now() }; // v204""", 'fetchEcDay')
rep("""    if (!config.pulse || isSol(config)) return Promise.resolve(null);""",
    """    if (!config.pulse || isSol(config) || isCredit(config)) return Promise.resolve(null); // v204 โหมดตัดเครดิตไม่อ่าน EC""", 'refreshEc')
rep("""          {!isSol(config) && <button onClick={() => refreshEc(true)}""",
    """          {!isSol(config) && !isCredit(config) && <button onClick={() => refreshEc(true)}""", 'recon refresh btn')

# ---------- ยืนยันเริ่มเครื่อง (fireForOrder) ----------
rep("""    : `⚡ ${tr(config, 'ยืนยันเริ่มเครื่อง')}`;
  const payTxt = coin > 0
    ? `💵 ${tr(config, 'หยอดเหรียญเอง')} ฿${coin}${pulseBaht > 0 ? `\\n⚡ ${tr(config, 'ยิงจากแอป')} ${pulses} ${tr(config, 'พัลส์')} (฿${pulseBaht})` : ''}\\n\\n👉 ${tr(config, 'หยอดเหรียญที่เครื่องให้ครบก่อน แล้วค่อยกดตกลง')}`
    : `🔢 ${pulses} ${tr(config, 'พัลส์')} (฿${baht})${discBaht > 0 ? `\\n🎟️ ${tr(config, 'ส่วนลดคูปอง')} ฿${discBaht}` : ''}`;""",
    """    : isCredit(config) ? `🎟️ ${tr(config, 'ยืนยันตัดเครดิต')}` : `⚡ ${tr(config, 'ยืนยันเริ่มเครื่อง')}`;
  const cr = isCredit(config); // 🎟️ v204
  const payTxt = coin > 0
    ? `💵 ${tr(config, 'หยอดเหรียญเอง')} ฿${coin}${pulseBaht > 0 ? (cr ? `\\n🎟️ ${tr(config, 'ตัดเครดิตของตัวเองที่ตู้')} ฿${pulseBaht}` : `\\n⚡ ${tr(config, 'ยิงจากแอป')} ${pulses} ${tr(config, 'พัลส์')} (฿${pulseBaht})`) : ''}\\n\\n👉 ${tr(config, 'หยอดเหรียญที่เครื่องให้ครบก่อน แล้วค่อยกดตกลง')}`
    : cr ? `🎟️ ${tr(config, 'ตัดเครดิตของตัวเองที่ตู้')} ฿${baht}${discBaht > 0 ? `\\n🎟️ ${tr(config, 'ส่วนลดคูปอง')} ฿${discBaht}` : ''}`
    : `🔢 ${pulses} ${tr(config, 'พัลส์')} (฿${baht})${discBaht > 0 ? `\\n🎟️ ${tr(config, 'ส่วนลดคูปอง')} ฿${discBaht}` : ''}`;""", 'fireForOrder pay')
rep("""3) ${coin > 0 ? tr(config, 'หยอดเหรียญ แล้วกดตกลง') : tr(config, 'กดตกลง = ชำระเงิน เครื่องเริ่มทำงาน')}`;""",
    """3) ${cr && pulseBaht > 0 ? tr(config, coin > 0 ? 'หยอดเหรียญ + จ่ายด้วยเครดิตของตัวเองที่ตู้ จนเครื่องเริ่มทำงาน แล้วกดตกลง' : 'จ่ายด้วยเครดิตของตัวเองที่ตู้ จนเครื่องเริ่มทำงาน แล้วกดตกลง') : coin > 0 ? tr(config, 'หยอดเหรียญ แล้วกดตกลง') : tr(config, 'กดตกลง = ชำระเงิน เครื่องเริ่มทำงาน')}`;""", 'fireForOrder steps')

# ---------- ผลลัพธ์ ----------
rep("""  if (res.status === 'coin' && isSol(config)) return { ok: true, text: `✅ ${mLabel} · ${coinTxt} — ${tr(config, 'บันทึกแล้ว')}` };""",
    """  if (res.status === 'credit') return { ok: true, text: `✅ ${mLabel} · 🎟️ ${tr(config, 'ตัดเครดิต')} ฿${res.baht || 0}${coinTxt ? ' · ' + coinTxt : ''} — ${tr(config, 'บันทึกแล้ว')}` }; // v204
  if (res.status === 'coin' && (isSol(config) || isCredit(config))) return { ok: true, text: `✅ ${mLabel} · ${coinTxt} — ${tr(config, 'บันทึกแล้ว')}` };""", 'fireResultMsg')
rep("""if (res.status === 'confirmed' || res.status === 'coin') playSuccessSound();""",
    """if (res.status === 'confirmed' || res.status === 'coin' || res.status === 'credit') playSuccessSound();""", 'success sound', count=3)

# ---------- หน้าเลือกเครื่อง ----------
rep("""{tr(config, isSol(config) ? 'ขั้นตอน: ใส่ผ้า → ปิดประตู → กดปุ่มด้านล่าง → กด Start ใน SOL → กลับมากด ✅' : 'ขั้นตอน: ใส่ผ้า → ปิดประตู → เลือกโปรแกรมที่หน้าเครื่อง → กดเริ่ม (ชำระเงิน)')}""",
    """{tr(config, isSol(config) ? 'ขั้นตอน: ใส่ผ้า → ปิดประตู → กดปุ่มด้านล่าง → กด Start ใน SOL → กลับมากด ✅' : isCredit(config) ? 'ขั้นตอน: ใส่ผ้า → ปิดประตู → เลือกโปรแกรม → จ่ายด้วยเครดิตของตัวเองที่ตู้ → เครื่องเดินแล้วกดปุ่มด้านล่าง' : 'ขั้นตอน: ใส่ผ้า → ปิดประตู → เลือกโปรแกรมที่หน้าเครื่อง → กดเริ่ม (ชำระเงิน)')}""", 'sheet steps')
rep("""<span className="text-[11px] font-bold opacity-80">{tr(config, 'ยิงจากแอป')}</span></span>, null)}""",
    """<span className="text-[11px] font-bold opacity-80">{tr(config, isCredit(config) ? 'ตัดเครดิต' : 'ยิงจากแอป')}</span></span>, null)}""", 'add time tile')
rep("""              if (!confirm(`🪙 ${tr(config, 'ยิงไม่ได้ → หยอดเหรียญแทน')}\\n\\n📋""",
    """              if (!confirm(`🪙 ${tr(config, isCredit(config) ? 'เครดิตหมด → หยอดเหรียญร้านแทน' : 'ยิงไม่ได้ → หยอดเหรียญแทน')}\\n\\n📋""", 'float confirm')
rep("""              🪙 {tr(config, 'ยิงไม่ได้ → หยอดเหรียญแทน')} {selM.label} ฿{cp.pulse}""",
    """              🪙 {tr(config, isCredit(config) ? 'เครดิตหมด → หยอดเหรียญร้านแทน' : 'ยิงไม่ได้ → หยอดเหรียญแทน')} {selM.label} ฿{cp.pulse}""", 'float label')
rep("""              : cp.coin > 0 ? `💵 ฿${cp.coin} + ${isSol(config) ? '🟦' : '⚡'} ฿${cp.pulse} · ${tr(config, 'เริ่มเครื่อง')} ${selM.label}`
              : isSol(config) ? `🟦 ${tr(config, 'เริ่มเครื่อง')} ${selM.label} · ฿${baht} (${tr(config, 'กดใน SOL')})`""",
    """              : cp.coin > 0 ? `💵 ฿${cp.coin} + ${isSol(config) ? '🟦' : isCredit(config) ? '🎟️' : '⚡'} ฿${cp.pulse} · ${tr(config, 'เริ่มเครื่อง')} ${selM.label}`
              : isSol(config) ? `🟦 ${tr(config, 'เริ่มเครื่อง')} ${selM.label} · ฿${baht} (${tr(config, 'กดใน SOL')})`
              : isCredit(config) ? `🎟️ ${tr(config, 'ตัดเครดิตแล้ว')} · ${selM.label} ฿${baht}`""", 'main button')

# ---------- การ์ดใบงาน ----------
rep("""        <span className="text-2xl">{isSol(config) ? '🧺' : '⚡'}</span>""",
    """        <span className="text-2xl">{isSol(config) ? '🧺' : isCredit(config) ? '🎟️' : '⚡'}</span>""", 'card icon')
rep("""{tr(config, isSol(config) ? 'เริ่มเครื่อง (กดใน SOL)' : 'เริ่มเครื่อง (ยิงพัลส์)')}""",
    """{tr(config, isSol(config) ? 'เริ่มเครื่อง (กดใน SOL)' : isCredit(config) ? 'เริ่มเครื่อง (ตัดเครดิต)' : 'เริ่มเครื่อง (ยิงพัลส์)')}""", 'card title')
rep("""      manual: ['bg-violet-100 text-violet-800', '✍️ ' + tr(config, 'เจ้าของบันทึก')],""",
    """      manual: ['bg-violet-100 text-violet-800', '✍️ ' + tr(config, 'เจ้าของบันทึก')],
      credit: ['bg-sky-100 text-sky-800', '🎟️ ' + tr(config, 'ตัดเครดิต') + (l.staffName ? ' · ' + l.staffName : '')], // v204""", 'status chip')
rep("""        <RefundAction config={config} log={l} isOwner={isOwner} hideRequest={unconfirmed || (pulseIsCoin(l) && l.coinSeen !== true)} />""",
    """        <RefundAction config={config} log={l} isOwner={isOwner} hideRequest={unconfirmed || (pulseIsCoin(l) && l.coinSeen !== true && !isCredit(config))} />""", 'refund 1')
rep("""          {pulseIsManual(l) && <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-full bg-violet-100 text-violet-800">✍️ {tr(config, 'เจ้าของบันทึก')}</span>}
          <RefundAction config={config} log={l} isOwner={isOwner} hideRequest={pulseIsCoin(l) && l.coinSeen !== true} />""",
    """          {pulseIsManual(l) && <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-full bg-violet-100 text-violet-800">✍️ {tr(config, 'เจ้าของบันทึก')}</span>}
          {pulseIsCredit(l) && <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-full bg-sky-100 text-sky-800" data-credit-chip>🎟️ {tr(config, 'ตัดเครดิต')}{l.staffName ? ' · ' + l.staffName : ''}</span>}
          <RefundAction config={config} log={l} isOwner={isOwner} hideRequest={pulseIsCoin(l) && l.coinSeen !== true && !isCredit(config)} />""", 'job fired list')

# ---------- หยอดเหรียญ: ไม่มีเช็กกับเครื่อง ----------
rep("""  return (
    <>
      {log.coinSeen === false ? chip('bg-rose-100 text-rose-700', '⚠️ ' + tr(config, 'ยังไม่เห็นเหรียญเข้าเครื่อง'))""",
    """  if (isCredit(config)) return btn('bg-rose-50 border-rose-300 text-rose-700', undo, tr(config, 'ยกเลิก — ยังไม่ได้หยอด')); // v204 ไม่เช็กกับ EC
  return (
    <>
      {log.coinSeen === false ? chip('bg-rose-100 text-rose-700', '⚠️ ' + tr(config, 'ยังไม่เห็นเหรียญเข้าเครื่อง'))""", 'coin check action')

# ---------- กระทบยอด ----------
rep("""              [isSol(config) ? 'ติ๊กในแอป' : tr(config, 'ยิงจากแอป'), recon.appBaht, tr(config, 'ทุกเครื่อง')],
              [isSol(config) ? 'SOL (WDF)' :""",
    """              [isSol(config) ? 'ติ๊กในแอป' : tr(config, isCredit(config) ? 'ตัดเครดิต' : 'ยิงจากแอป'), recon.appBaht, tr(config, 'ทุกเครื่อง')],
              isCredit(config) ? [tr(config, 'หยอดเหรียญ'), recon.coinBaht, tr(config, 'ทุกเครื่อง')] : // v204
              [isSol(config) ? 'SOL (WDF)' :""", 'recon rows')
rep("""{!config.ui2 && <span className="text-slate-500"> · {tr(config, 'แอป')} ฿{formatMoney(recon.appBaht)} · {ecName(config)} {ecBusy ? '…' : recon.ecBaht == null ? '…' : '฿' + formatMoney(recon.ecBaht)}""",
    """{!config.ui2 && <span className="text-slate-500"> · {isCredit(config) ? `🎟️ ฿${formatMoney(recon.appBaht)} · 🪙 ฿${formatMoney(recon.coinBaht)}` : <React.Fragment>{tr(config, 'แอป')} ฿{formatMoney(recon.appBaht)} · {ecName(config)} {ecBusy ? '…' : recon.ecBaht == null ? '…' : '฿' + formatMoney(recon.ecBaht)}</React.Fragment>}""", 'home slim')
rep("""            {tr(config, slim ? 'ค่าเครื่อง' : 'งาน')} ฿{formatMoney(recon.need)} · {tr(config, 'แอป')} ฿{formatMoney(recon.appBaht)} · {ecName(config)} {ecBusy ? `⏳ ${ecBusy}` : recon.ecBaht == null ? '…' : '฿' + formatMoney(recon.ecBaht)}""",
    """            {tr(config, slim ? 'ค่าเครื่อง' : 'งาน')} ฿{formatMoney(recon.need)} · {isCredit(config) ? `🎟️ ฿${formatMoney(recon.appBaht)} · 🪙 ฿${formatMoney(recon.coinBaht)}` : <React.Fragment>{tr(config, 'แอป')} ฿{formatMoney(recon.appBaht)} · {ecName(config)} {ecBusy ? `⏳ ${ecBusy}` : recon.ecBaht == null ? '…' : '฿' + formatMoney(recon.ecBaht)}</React.Fragment>}""", 'home card')
rep("""    ['💳', 'โอน', 'ยิงจากแอป', B.transfer,""",
    """    ['💳', 'โอน', isCredit(config) ? 'แม่บ้านตัดเครดิต' : 'ยิงจากแอป', B.transfer,""", 'buckets')

# ---------- โปรซักเอง ----------
rep("""    if (usePulse && !manual && !confirm(`⚡ ${tr(config, 'ยืนยันเริ่มเครื่อง')}\\n\\n🧺 ${pulseMachine.label}\\n🔢 ${amount / PULSE_BAHT} ${tr(config, 'พัลส์')} (฿${amount})\\n🎁 ${promoName || 'ส่วนลด'}`)) return;""",
    """    if (usePulse && !manual && !confirm(isCredit(config) // 🎟️ v204
      ? `🎟️ ${tr(config, 'ยืนยันตัดเครดิต')}\\n\\n🧺 ${pulseMachine.label}\\n🎟️ ${tr(config, 'ตัดเครดิตของตัวเองที่ตู้')} ฿${amount}\\n🎁 ${promoName || 'ส่วนลด'}\\n\\n👉 ${tr(config, 'จ่ายด้วยเครดิตของตัวเองที่ตู้ จนเครื่องเริ่มทำงาน แล้วกดตกลง')}`
      : `⚡ ${tr(config, 'ยืนยันเริ่มเครื่อง')}\\n\\n🧺 ${pulseMachine.label}\\n🔢 ${amount / PULSE_BAHT} ${tr(config, 'พัลส์')} (฿${amount})\\n🎁 ${promoName || 'ส่วนลด'}`)) return;""", 'promo confirm')

# ---------- เจ้าของ: แท็บ / ตั้งค่า ----------
rep("""{pulseOn(config) && <TabBtn active={tab === 'pulse'} onClick={() => setTab('pulse')}>⚡ พัลส์{""",
    """{pulseOn(config) && <TabBtn active={tab === 'pulse'} onClick={() => setTab('pulse')}>{isCredit(config) ? '🎟️ เริ่มเครื่อง' : '⚡ พัลส์'}{""", 'owner tab')
rep("""      <p className="text-sm font-bold text-slate-800 mb-2">⚡ ยิงพัลส์เข้าเครื่องจากแอป (ระบบ EC)</p>""",
    """      <p className="text-sm font-bold text-slate-800 mb-2">{isCredit(config) ? '🎟️ เริ่มเครื่องในแอป (โหมดตัดเครดิต · ไม่เชื่อมต่อเว็บ EC)' : '⚡ ยิงพัลส์เข้าเครื่องจากแอป (ระบบ EC)'}</p>""", 'settings title')
rep("""      <button onClick={test} className="w-full mt-2 py-2 rounded-xl text-sm font-bold bg-slate-900 text-white active:scale-95">🔌 ทดสอบการเชื่อมต่อ (ไม่ยิงเครื่อง)</button>""",
    """      {!isCredit(config) && <button onClick={test} className="w-full mt-2 py-2 rounded-xl text-sm font-bold bg-slate-900 text-white active:scale-95">🔌 ทดสอบการเชื่อมต่อ (ไม่ยิงเครื่อง)</button>}
      {isCredit(config) && <p className="text-[11px] text-slate-500 mt-1.5" data-credit-mode>เปิดแล้ว: ใบงานมีปุ่มเริ่มเครื่อง → แม่บ้านจ่ายด้วยเครดิตของตัวเองที่ตู้ แล้วกด 🎟️ ตัดเครดิตแล้ว · ลูกค้าจ่ายสด = หยอดเหรียญ · ยอดใช้รายคนดูที่แท็บ 🎟️ เครดิต · แอปไม่เข้าเว็บ EC เลย</p>}""", 'settings test')
rep("""      <p className="text-[11px] text-slate-400 mt-1.5">เปิดแล้ว: หน้าใบรับงานมีปุ่ม ▶ เริ่มเครื่อง""",
    """      {!isCredit(config) && <p className="text-[11px] text-slate-400 mt-1.5">เปิดแล้ว: หน้าใบรับงานมีปุ่ม ▶ เริ่มเครื่อง""", 'settings help open')
rep("""· Worker: {config.pulse.workerUrl.replace('https://', '')}</p>""",
    """· Worker: {config.pulse.workerUrl.replace('https://', '')}</p>}""", 'settings help close')
rep("""    if (!on && !confirm('เปิดยิงพัลส์จากแอป?\\n\\n• ต้องตั้ง Worker teddy-pulse (ใส่ EC_USER / EC_PASS) เสร็จแล้ว\\n• กดทดสอบการเชื่อมต่อให้ผ่านก่อน\\n• เริ่มกระทบยอดตั้งแต่ตอนนี้')) return;""",
    """    if (!on && !confirm(isCredit(config) ? 'เปิดปุ่มเริ่มเครื่องในใบงาน (โหมดตัดเครดิต)?\\n\\n• แม่บ้านจ่ายด้วยเครดิตของตัวเองที่ตู้ แล้วกดบันทึกในแอป\\n• เริ่มกระทบยอดตั้งแต่ตอนนี้' : 'เปิดยิงพัลส์จากแอป?\\n\\n• ต้องตั้ง Worker teddy-pulse (ใส่ EC_USER / EC_PASS) เสร็จแล้ว\\n• กดทดสอบการเชื่อมต่อให้ผ่านก่อน\\n• เริ่มกระทบยอดตั้งแต่ตอนนี้')) return;""", 'settings toggle')

# ---------- 🎟️ เครดิต (เจ้าของ) ----------
rep("""  const [statMode, setStatMode] = useState('all'); // all = คงเหลือสะสม | month = สรุปรายเดือน
  const [statDate, setStatDate] = useState(() => new Date());
""", """  const [statMode, setStatMode] = useState('all'); // all = คงเหลือสะสม | month = สรุปรายเดือน
  const [statDate, setStatDate] = useState(() => new Date());
  // 🎟️ v204 โหมดตัดเครดิต: ยอดใช้ = pulseLogs method 'credit' ของแม่บ้านแต่ละคน
  const creditMode = isCredit(config);
  const [creditLogs, setCreditLogs] = useState([]);
  useEffect(() => {
    if (!window.db || !creditMode) return;
    const u = window.db.collection('pulseLogs').where('method', '==', 'credit').onSnapshot(
      snap => setCreditLogs(snap.docs.map(d => ({ id: d.id, ...d.data() })).filter(l => l.brand === config.brand)),
      e => console.error('credit logs error:', e));
    return () => u();
  }, [config.brand, creditMode]);
""", 'credit hooks')
rep("""  (orders || []).forEach(o => { if (o.staffName && !staffMap[o.staffName]) staffMap[o.staffName] = { id: o.staffId || null, name: o.staffName }; });
  const staffs = Object.values(staffMap);""",
    """  (orders || []).forEach(o => { if (o.staffName && !staffMap[o.staffName]) staffMap[o.staffName] = { id: o.staffId || null, name: o.staffName }; });
  creditLogs.forEach(l => { if (l.staffName && !staffMap[l.staffName]) staffMap[l.staffName] = { id: l.staffId || null, name: l.staffName }; }); // v204
  const staffs = Object.values(staffMap);
  // 🎟️ v204 ยอดตัดเครดิตของแม่บ้าน (คืนเครดิตแล้วยังนับ — เครดิตในบัญชี EC ถูกตัดไปแล้ว)
  const orderById = {};
  (orders || []).forEach(o => { if (o.id) orderById[o.id] = o; });
  const creditUseFor = (name, inT) => {
    let dropUse = 0, deliveryUse = 0, internalUse = 0, promoUse = 0, promoN = 0;
    const ords = new Set();
    creditLogs.filter(l => l.staffName === name && inT(l.createdAt || 0) && (pulseLive(l) || pulseRefunded(l))).forEach(l => {
      const b = l.baht || 0;
      const o = l.refId ? orderById[l.refId] : null;
      if (l.refType === 'promo') { promoUse += b; promoN++; return; }
      if (l.refId) ords.add(l.refId);
      if (l.refType === 'internal' || (o && isInternalOrder(o))) internalUse += b;
      else if (o && o.deliveryZone) deliveryUse += b;
      else dropUse += b;
    });
    return { dropUse, deliveryUse, internalUse, orderUse: dropUse + deliveryUse + internalUse, promoUse, promoN, orderN: ords.size };
  };""", 'credit use')
rep("""    return { baseline, base, topup, promo, promoCount: promoList.length, dropUse, deliveryUse, internalUse, orderUse, orderCount: myOrders.length, expected, lastCheck };""",
    """    if (creditMode) { // v204
      const cu = creditUseFor(name, t => t > t0);
      return { baseline, base, topup, promo: cu.promoUse, promoCount: cu.promoN, dropUse: cu.dropUse, deliveryUse: cu.deliveryUse, internalUse: cu.internalUse, orderUse: cu.orderUse, orderCount: cu.orderN, expected: base + topup - cu.promoUse - cu.orderUse, lastCheck };
    }
    return { baseline, base, topup, promo, promoCount: promoList.length, dropUse, deliveryUse, internalUse, orderUse, orderCount: myOrders.length, expected, lastCheck };""", 'statFor')
rep("""    return { baseline: true, base: 0, topup, promo, promoCount: promoList.length, dropUse, deliveryUse, internalUse, orderUse, orderCount: myOrders.length, expected: topup - promo - orderUse, lastCheck: null, monthMode: true };""",
    """    if (creditMode) { // v204
      const cu = creditUseFor(name, inM);
      return { baseline: true, base: 0, topup, promo: cu.promoUse, promoCount: cu.promoN, dropUse: cu.dropUse, deliveryUse: cu.deliveryUse, internalUse: cu.internalUse, orderUse: cu.orderUse, orderCount: cu.orderN, expected: topup - cu.promoUse - cu.orderUse, lastCheck: null, monthMode: true };
    }
    return { baseline: true, base: 0, topup, promo, promoCount: promoList.length, dropUse, deliveryUse, internalUse, orderUse, orderCount: myOrders.length, expected: topup - promo - orderUse, lastCheck: null, monthMode: true };""", 'monthStatFor')
rep("""        {pulseOn(config) && <p className="text-xs font-bold text-amber-700 bg-amber-50 rounded-lg px-2 py-1.5 mt-1">⚡ สาขานี้เลิกใช้เครดิตแม่บ้านแล้ว""",
    """        {creditMode && <p className="text-xs font-bold text-sky-800 bg-sky-50 rounded-lg px-2 py-1.5 mt-1" data-credit-banner>🎟️ โหมดตัดเครดิต (เริ่ม 8 พ.ย. 69): ยอดใช้ของแต่ละคน = ที่แม่บ้านกด '🎟️ ตัดเครดิตแล้ว' ในแอป (งานลูกค้าจ่ายสดหยอดเหรียญ ไม่นับ) · ก่อนเริ่มให้กด 🎯 ตั้งยอดต้นของทุกคนตามยอดจริงในบัญชี EC</p>}
        {pulseOn(config) && !creditMode && <p className="text-xs font-bold text-amber-700 bg-amber-50 rounded-lg px-2 py-1.5 mt-1">⚡ สาขานี้เลิกใช้เครดิตแม่บ้านแล้ว""", 'credit banner')

rep("""              <p className="text-slate-500">งานฝาก ({st.orderCount} งาน · สด+โอน)</p>""",
    """              <p className="text-slate-500">งานฝาก ({st.orderCount} งาน · {creditMode ? 'ส่วนที่ตัดเครดิต' : 'สด+โอน'})</p>""", 'drop label')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v204 patched')
