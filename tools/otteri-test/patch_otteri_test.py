#!/usr/bin/env python3
"""Otteri test build: index.html (v170) → test/index.html
ส่วนที่ 1 (feature): ระบบแบบเท็ดดี้ 2 ให้ Otteri — เปิดเฉพาะเมื่อ window.TEST_MODE (ตัวจริงไม่เปลี่ยนพฤติกรรม)
  - หน้าแรก/หน้าเจ้าของแบบเท็ดดี้ 2 (config.t2Sys) · ค่าเริ่มต้นจ่ายโอน (config.defaultPay)
  - เริ่มเครื่องโหมด SOL: แอปไม่สั่งเครื่อง — แม่บ้านกด Start ใน SOL (บัญชี WDF ของตัวเอง) แล้วกลับมาติ๊ก ✅
  - กระทบยอดรายวัน: ยอดที่ติ๊กในแอป ↔ ยอด WDF ที่เจ้าของใส่จาก SOL
  - เลือกเครื่องแบบตาราง (Otteri ไม่ได้เป็นแท่นอบบน-ซักล่าง)
ส่วนที่ 2 (test wrapper): Firestore คอลเลกชัน test_* · localStorage คีย์ TEST: · ไม่ใช้ offline cache · ไม่ลง SW · ล็อกร้าน Otteri
"""
import sys

SRC, OUT = sys.argv[1], sys.argv[2]
FRAG = sys.argv[3] if len(sys.argv) > 3 else 'sol_core.jsx'
s = open(SRC, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    assert n == count, f'{label}: anchor found {n} times (want {count})'
    s = s.replace(old, new)


def rep_between(start, end, fn, label):
    """แทนข้อความตั้งแต่ start ถึง end (รวม end) ด้วย fn(chunk)"""
    global s
    a = s.find(start)
    assert a >= 0 and s.count(start) == 1, f'{label}: start anchor'
    b = s.find(end, a)
    assert b >= 0, f'{label}: end anchor'
    b += len(end)
    s = s[:a] + fn(s[a:b]) + s[b:]


# ======================= ส่วนที่ 1: feature =======================
rep("""  hasToken: false, // Otteri ใช้แค่เหรียญ 10 ไม่มี token ของร้าน
};""", """  hasToken: false, // Otteri ใช้แค่เหรียญ 10 ไม่มี token ของร้าน
};
// 🧪 Otteri ใช้ระบบแบบเท็ดดี้ 2 (เงินสดในมือ · เริ่มเครื่องผ่าน SOL · กระทบยอด WDF) — เปิดเฉพาะหน้าทดสอบก่อน
if (window.TEST_MODE) Object.assign(OTTERI_CONFIG, {
  t2Sys: true,
  defaultPay: 'transfer', // ให้แม่บ้านถือเงินสดน้อยที่สุด
  pulse: { mode: 'sol', solUrl: 'https://backoffice.otteri-sol.com/dashboard', maxPerShot: 15, stacks: 0, dryMinPer10: {}, washBusyMin: 35, dayStartHour: 9, solMap: { top: ['', '', '', '', '', '', '', '', 'D4', 'D6'], bottom: ['W1', 'W2', 'W3', 'W4', 'W6', 'W7', 'W8', 'D1', 'D5', 'D7'] } },
});""", 'otteri flags')

rep("""  brand: 'teddy2',
""", """  brand: 'teddy2',
  t2Sys: true, // หน้าแรก/หน้าเจ้าของแบบเท็ดดี้ 2
""", 'teddy2 t2Sys')

# gates: brand === 'teddy2' → config.t2Sys
# v172: ตัวจริงเลือกหน้าเจ้าของด้วย t2OwnerOn(config) (teddy2 · teddy · t2Sys) แล้ว — ทดสอบแค่เพิ่มแถบ SOL
rep("{view === 'ownerDashboard' && t2OwnerOn(config) && <OwnerDashboardT2",
    "{isSol(config) && <SolPendingBar config={config} />}\n      {view === 'ownerDashboard' && t2OwnerOn(config) && <OwnerDashboardT2", 'gate owner T2')
rep("  const T2H = config.brand === 'teddy2';", "  const T2H = !!config.t2Sys;", 'gate home')
rep("{config.brand === 'teddy2' && order.id && <CashCollectedNote", "{config.t2Sys && order.id && <CashCollectedNote", 'gate cash note')

# ค่าเริ่มต้นวิธีจ่าย
rep("useState(seed?.paymentMethod || 'cash')", "useState(seed?.paymentMethod || config.defaultPay || 'cash')", 'default pay')

# helpers
rep("const pulseOn = (config) => !!(config && config.pulse && config.settings && config.settings.pulseEnabled === true);",
    """const pulseOn = (config) => !!(config && config.pulse && config.settings && config.settings.pulseEnabled === true);
const isSol = (config) => !!(config && config.pulse && config.pulse.mode === 'sol'); // 🟦 Otteri: เริ่มเครื่องผ่าน SOL
const ecName = (config) => (isSol(config) ? 'SOL' : 'EC');""", 'isSol helper')

# firePulse → โหมด SOL บันทึกอย่างเดียว
rep("""async function firePulse(config, { machine, pulses, refType, refId, slotKey, refLabel, retryOf, meta }) {
""", """async function firePulse(config, { machine, pulses, refType, refId, slotKey, refLabel, retryOf, meta }) {
  if (isSol(config)) return solRecordStart(config, { machine, pulses, refType, refId, slotKey, refLabel, meta }); // 🟦 ไม่สั่งเครื่อง
""", 'firePulse sol')

# fireForOrder → โหมด SOL: ยืนยัน → (หยอดเหรียญส่วนเงินสด) → แถบรอกด Start ใน SOL
rep("""  const progLabel = kind === 'wash' ? tr(config, washTempLabel(temp)) : (heat ? tr(config, dryHeatLabel(heat)) : tr(config, 'ความร้อนตามใบงาน'));
""", """  const progLabel = kind === 'wash' ? tr(config, washTempLabel(temp)) : (heat ? tr(config, dryHeatLabel(heat)) : tr(config, 'ความร้อนตามใบงาน'));
  if (isSol(config)) { // 🟦 Otteri: แม่บ้านกด Start ใน SOL เอง แล้วกลับมาติ๊กในแอป
    const code = solCodeOf(order);
    const lines = [];
    if (coin > 0) lines.push(`💵 ${tr(config, 'หยอดเหรียญที่เครื่อง')} ฿${coin}`);
    if (pulseBaht > 0) lines.push(`🟦 ${tr(config, 'กด Start ใน SOL')} ฿${pulseBaht} · ${tr(config, 'ช่อง Note ใส่')} ${code}`);
    const tail = pulseBaht > 0 ? `\\n\\n👉 ${tr(config, 'กดตกลง แล้วไปกด Start ใน SOL — เสร็จแล้วกด ✅ ที่แถบล่างของแอป')}` : `\\n\\n👉 ${tr(config, 'หยอดเหรียญที่เครื่องแล้วกดตกลง')}`;
    if (!confirm(`🧺 ${mLabel} (${kg}kg) · ${kind === 'wash' ? '💧' : '🌡️'} ${progLabel}\\n📋 ${pulseRefLabel(order, config)}\\n\\n${lines.join('\\n')}${warn ? `\\n\\n⚠️ ${warn}` : ''}${tail}`)) return null;
    const coinLog = coin > 0 ? logCoinInsert(config, order, logs, { machine, kind, kg, temp, heat, baht: coin, dryMin, warn }) : null;
    if (pulseBaht <= 0) return { ...coinLog, coinBaht: coin };
    solPendingAdd(config, { orderId: order.id, refType: isInternalOrder(order) ? 'internal' : 'order', refLabel: pulseRefLabel(order, config), code, machine, machineLabel: mLabel, kind, kg, temp: temp || null, heat: heat || null, baht: pulseBaht, progLabel, discBaht: discBaht || null, warn: warn || null, at: Date.now() });
    return { status: 'sol-pending', machineLabel: mLabel, coinBaht: coin };
  }
""", 'fireForOrder sol')

rep("""  if (res.status === 'coin') return { ok: true, text: `✅ ${mLabel} · ${coinTxt} — ${tr(config, 'บันทึกแล้ว — กำลังเช็กว่าเครื่องนับเหรียญ')}` };""",
    """  if (res.status === 'sol-pending') return { ok: null, solPending: true, text: `👉 ${mLabel} — ${tr(config, 'ไปกด Start ใน SOL แล้วกด ✅ ที่แถบล่าง')}${coinTxt ? ' · ' + coinTxt : ''}` };
  if (res.status === 'coin' && isSol(config)) return { ok: true, text: `✅ ${mLabel} · ${coinTxt} — ${tr(config, 'บันทึกแล้ว')}` };
  if (res.status === 'coin') return { ok: true, text: `✅ ${mLabel} · ${coinTxt} — ${tr(config, 'บันทึกแล้ว — กำลังเช็กว่าเครื่องนับเหรียญ')}` };""", 'result msg')

# ไม่เช็กเหรียญกับ EC ในโหมด SOL
rep("  if (coinLog) watchCoinLog(config, coinLog); // 💵 v148",
    "  if (coinLog && !isSol(config)) watchCoinLog(config, coinLog); // 💵 v148", 'no coin watch')
rep("async function checkCoinLog(config, log, final) {\n",
    "async function checkCoinLog(config, log, final) {\n  if (isSol(config)) return { ok: true, seen: false };\n", 'checkCoinLog guard')
rep("async function fetchEcDay(config, dateKey, machineIds, onProgress) {\n",
    "async function fetchEcDay(config, dateKey, machineIds, onProgress) {\n  if (isSol(config)) return { byMachine: {}, errors: [], at: Date.now() };\n", 'fetchEcDay guard')

# ส่วนประกอบ SOL
frag = open(FRAG, encoding='utf-8').read()
rep("// ---------- หน้าเลือกเครื่อง (เต็มจอ) ----------", frag + "\n// ---------- หน้าเลือกเครื่อง (เต็มจอ) ----------", 'sol fragment')

# เลือกเครื่องแบบตาราง
rep("<MachineWall config={config} stacks={stacks} marks={marks} selected={sel} onPick={pick} problems={problems} />",
    "{stacks.length ? <MachineWall config={config} stacks={stacks} marks={marks} selected={sel} onPick={pick} problems={problems} /> : <MachineGrid config={config} machines={ms} marks={marks} selected={sel} onPick={pick} problems={problems} />}", 'grid')
rep("<span>{tr(config, 'แตะ อบ (บน) หรือ ซัก (ล่าง)')}</span>",
    "<span>{tr(config, stacks.length ? 'แตะ อบ (บน) หรือ ซัก (ล่าง)' : 'แตะเครื่องที่จะเริ่ม')}</span>", 'grid legend')
rep("""<p className="text-xs font-bold text-slate-500">≈ {dryMinutesFor(config, selM.kg, amount)} {tr(config, 'นาที')} · +฿10 = +{((config.pulse && config.pulse.dryMinPer10) || {})[selM.kg] || '?'} {tr(config, 'นาที')}</p>""",
    """{dryMinutesFor(config, selM.kg, amount) > 0 && <p className="text-xs font-bold text-slate-500">≈ {dryMinutesFor(config, selM.kg, amount)} {tr(config, 'นาที')} · +฿10 = +{((config.pulse && config.pulse.dryMinPer10) || {})[selM.kg] || '?'} {tr(config, 'นาที')}</p>}""", 'dry minutes')

# กระทบยอด: โหมด SOL ใช้ยอด WDF ที่เจ้าของใส่
rep("""  const refreshEc = () => {
    if (!config.pulse) return Promise.resolve(null);""", """  const refreshEc = () => {
    if (!config.pulse || isSol(config)) return Promise.resolve(null);""", 'refreshEc guard')
rep("  const recon = useMemo(() => buildPulseRecon({ config, dateKey, orders, ledger, logs, ec }), [config, dateKey, orders, ledger, logs, ec]);",
    "  const ecUse = isSol(config) ? solEcFromNote(note) : ec; // 🟦 SOL: ยอด WDF ที่เจ้าของใส่\n  const recon = useMemo(() => buildPulseRecon({ config, dateKey, orders, ledger, logs, ec: ecUse }), [config, dateKey, orders, ledger, logs, ec, note]);", 'recon ec')
rep("  return { recon, ec, ecBusy, refreshEc, note, unexplained, logs, ledger };",
    "  return { recon, ec: ecUse, ecBusy, refreshEc, note, unexplained, logs, ledger };", 'recon return')
rep("""  const machineRows = [];
  if (ec && ec.byMachine) {""", """  const machineRows = [];
  if (ec && ec.sol) { // 🟦 SOL: เทียบยอดรวมทั้งวัน
    const appSol = sumBaht(dayPulse) + sumBaht(dayRefundedPulse);
    const diff = (ec.solWdf || 0) - appSol;
    if (diff !== 0) add(`s:${dateKey}:${ec.solWdf}:${appSol}`, 'error', diff > 0 ? 'SOL มียอดมากกว่าที่ติ๊กในแอป' : 'ติ๊กในแอปมากกว่ายอดใน SOL', { label: `SOL WDF ฿${formatMoney(ec.solWdf)} · ${tr(config, 'แอป')} ฿${formatMoney(appSol)}`, amount: Math.abs(diff) });
  } else if (ec && ec.byMachine) {""", 'recon sol branch')
rep("    ecBaht: ec && ec.byMachine && Object.keys(ec.byMachine).length ?",
    "    ecBaht: ec && ec.sol ? ec.solWdf : ec && ec.byMachine && Object.keys(ec.byMachine).length ?", 'recon ecBaht')

rep("[tr(config, 'เครื่องจริง (EC)'), recon.ecBaht, ecBusy ? `⏳ ${ecBusy}` : recon.ecAt ? new Date(recon.ecAt).toTimeString().slice(0, 5) : '-'],",
    "[isSol(config) ? 'SOL (WDF)' : tr(config, 'เครื่องจริง (EC)'), recon.ecBaht, isSol(config) ? (recon.ecAt ? new Date(recon.ecAt).toTimeString().slice(0, 5) : tr(config, 'ยังไม่ได้ใส่')) : ecBusy ? `⏳ ${ecBusy}` : recon.ecAt ? new Date(recon.ecAt).toTimeString().slice(0, 5) : '-'],", 'panel tile')
rep("{recon.ecBaht == null && <p className=\"text-[11px] text-emerald-700 mt-0.5\">{tr(config, 'ยังไม่ได้เทียบกับเครื่องจริง')}</p>}",
    "{recon.ecBaht == null && <p className=\"text-[11px] text-emerald-700 mt-0.5\">{tr(config, isSol(config) ? 'ยังไม่ได้ใส่ยอด WDF จาก SOL' : 'ยังไม่ได้เทียบกับเครื่องจริง')}</p>}", 'panel not compared')
rep("          {recon.manualBaht > 0 && (", "          {isSol(config) && isOwner && <SolWdfInput config={config} dateKey={dateKey} current={recon.ecBaht} />}\n          {recon.manualBaht > 0 && (", 'wdf input')
rep_between("          <button onClick={refreshEc} disabled={!!ecBusy}", "</button>",
            lambda c: "          {!isSol(config) && " + c[len("          "):] + "}", 'hide refresh')

# การ์ดหน้าแรก: EC → SOL · เมื่อวานใช้ยอด WDF ที่ใส่ไว้
rep("· EC {ecBusy ? '…' : recon.ecBaht == null ? '…' : '฿' + formatMoney(recon.ecBaht)}",
    "· {ecName(config)} {ecBusy ? '…' : recon.ecBaht == null ? '…' : '฿' + formatMoney(recon.ecBaht)}", 'card slim EC')
rep("· EC {ecBusy ? `⏳ ${ecBusy}` :", "· {ecName(config)} {ecBusy ? `⏳ ${ecBusy}` :", 'card full EC')
rep("  const yRecon = useMemo(() => buildPulseRecon({ config, dateKey: yKey, orders, ledger, logs, ec: null }), [config, yKey, orders, ledger, logs]);",
    "  const yRecon = useMemo(() => buildPulseRecon({ config, dateKey: yKey, orders, ledger, logs, ec: isSol(config) ? solEcFromNote(yNote) : null }), [config, yKey, orders, ledger, logs, yNote]);", 'yesterday sol')

# ตั้งค่า
rep("{config.pulse && <PulseSettingsCard config={config} />}",
    "{config.pulse && (isSol(config) ? <SolSettingsCard config={config} /> : <PulseSettingsCard config={config} />)}", 'settings card')

# QR: ร้านที่ยังไม่มี QR บัญชี (Otteri) — ไม่ให้ขึ้นว่าเป็นเงินสด
rep("""              {qr ? (
                <>
                  <p className="text-sm font-extrabold" style={{ color: '#6D28D9' }}>💳 {tr(config, 'ให้ลูกค้าสแกนจ่าย · ทุกธนาคาร')}</p>
                  <img src={qr} alt="QR" className="mx-auto my-2 rounded-xl border border-slate-200" style={{ width: '240px', height: '240px', display: 'block' }} />""",
    """              {done.paymentMethod === 'transfer' ? (
                <>
                  <p className="text-sm font-extrabold" style={{ color: '#6D28D9' }}>💳 {tr(config, 'ให้ลูกค้าสแกนจ่าย · ทุกธนาคาร')}</p>
                  {qr ? <img src={qr} alt="QR" className="mx-auto my-2 rounded-xl border border-slate-200" style={{ width: '240px', height: '240px', display: 'block' }} />
                    : <p className="my-3 text-sm font-bold text-amber-800 bg-amber-50 border border-amber-200 rounded-xl px-3 py-6">⚠️ {tr(config, 'ยังไม่ได้ใส่ QR บัญชีร้าน')}</p>}""", 'det qr')
rep("""            const qrSrc = buildPromptPayQr(config.brand, amt) || payQr;
            if (!qrSrc) return null;""", """            const qrSrc = buildPromptPayQr(config.brand, amt) || payQr;
            if (!qrSrc) return window.TEST_MODE ? <div className="px-6 py-3 bg-amber-50 border-t border-amber-200 text-sm font-bold text-amber-800">⚠️ ยังไม่ได้ใส่ QR บัญชีร้าน · ยอดโอน ฿{formatMoney(amt)}</div> : null;""", 'receipt qr')

# ปุ่มเริ่มเครื่อง: โหมด SOL ไม่พูดถึงพัลส์
rep("""              : cp.coin > 0 ? `💵 ฿${cp.coin} + ⚡ ฿${cp.pulse} · ${tr(config, 'เริ่มเครื่อง')} ${selM.label}`
              : `⚡ ${tr(config, 'เริ่มเครื่อง')} ${selM.label} · ฿${baht} (${baht / PULSE_BAHT} ${tr(config, 'พัลส์')})`}""",
    """              : cp.coin > 0 ? `💵 ฿${cp.coin} + ${isSol(config) ? '🟦' : '⚡'} ฿${cp.pulse} · ${tr(config, 'เริ่มเครื่อง')} ${selM.label}`
              : isSol(config) ? `🟦 ${tr(config, 'เริ่มเครื่อง')} ${selM.label} · ฿${baht} (${tr(config, 'กดใน SOL')})`
              : `⚡ ${tr(config, 'เริ่มเครื่อง')} ${selM.label} · ฿${baht} (${baht / PULSE_BAHT} ${tr(config, 'พัลส์')})`}""", 'fire label')

# คำแนะนำในหน้าเลือกเครื่อง: โหมด SOL เลือกโปรแกรมใน SOL (ไม่ใช่ที่หน้าเครื่อง)
rep("""<p className="text-sm font-extrabold text-amber-900">⚠️ {tr(config, 'กดโหมดที่หน้าเครื่องให้ตรงใบงาน')}:""",
    """<p className="text-sm font-extrabold text-amber-900">⚠️ {tr(config, isSol(config) ? 'เลือกโปรแกรมใน SOL ให้ตรงใบงาน' : 'กดโหมดที่หน้าเครื่องให้ตรงใบงาน')}:""", 'picker mode line')
rep("""<p className="text-[11px] font-bold text-slate-500 mt-0.5">📝 {tr(config, 'ขั้นตอน: ใส่ผ้า → ปิดประตู → เลือกโปรแกรมที่หน้าเครื่อง → กดเริ่ม (ชำระเงิน)')}</p>""",
    """<p className="text-[11px] font-bold text-slate-500 mt-0.5">📝 {tr(config, isSol(config) ? 'ขั้นตอน: ใส่ผ้า → ปิดประตู → กดปุ่มด้านล่าง → กด Start ใน SOL → กลับมากด ✅' : 'ขั้นตอน: ใส่ผ้า → ปิดประตู → เลือกโปรแกรมที่หน้าเครื่อง → กดเริ่ม (ชำระเงิน)')}</p>""", 'picker steps')

rep("""<p className="text-xs font-bold text-slate-500">≈ {dryMinutesFor(config, selM.kg, baht)} {tr(config, 'นาที')}{dryBaseLeft""",
    """<p className="text-xs font-bold text-slate-500">{dryMinutesFor(config, selM.kg, baht) > 0 ? `≈ ${dryMinutesFor(config, selM.kg, baht)} ${tr(config, 'นาที')}` : ''}{dryBaseLeft""", 'locked dry minutes')

# คำในหน้าเจ้าของ: โหมด SOL ไม่ใช่ "ยิงแอป/พัลส์"
rep("['transfer', 'โอน (ยิงแอป)', PB.transfer], ['discount', 'ส่วนลด (ยิงแอป)', PB.discount]",
    "['transfer', isSol(config) ? 'โอน (กดใน SOL)' : 'โอน (ยิงแอป)', PB.transfer], ['discount', isSol(config) ? 'ส่วนลด (กดใน SOL)' : 'ส่วนลด (ยิงแอป)', PB.discount]", 'owner pulse rows')
rep("[tr(config, 'ยิงจากแอป'), recon.appBaht, tr(config, 'ทุกเครื่อง')],",
    "[isSol(config) ? 'ติ๊กในแอป' : tr(config, 'ยิงจากแอป'), recon.appBaht, tr(config, 'ทุกเครื่อง')],", 'panel app tile')
rep("{T2C[k].name}{k === 'pulse' && refundPendingN > 0 ?",
    "{k === 'pulse' && isSol(config) ? 'เริ่มเครื่อง' : T2C[k].name}{k === 'pulse' && refundPendingN > 0 ?", 'owner tab name')

# ข้อความ "ไปกด Start ใน SOL" เปลี่ยนเป็น "เริ่มแล้ว" เมื่อกด ✅ ที่แถบล่าง (3 จุดที่มีข้อความผลเริ่มเครื่อง)
rep("  const [msg, setMsg] = useState(null);\n", "  const [msg, setMsg] = useState(null);\n  useSolMsgSync(msg, setMsg); // 🟦\n", 'sol msg sync', count=3)

# ---------- 👔 ผ้าเจ้าของ (งานภายใน · แม่บ้านลงได้ · ฟรี) + 🏢 ลูกค้าประจำค้างจ่าย (เกอิชา · รวมบิลสิ้นเดือน · ไม่พับ) ----------
# เปิดด้วย config.ownerLaundry / config.accounts (ตอนนี้ตั้งเฉพาะ Otteri ในหน้าทดสอบ)
rep("""  hasToken: false, // Otteri ใช้แค่เหรียญ 10 ไม่มี token ของร้าน
};
// 🧪 Otteri ใช้ระบบแบบเท็ดดี้ 2 (เงินสดในมือ · เริ่มเครื่องผ่าน SOL · กระทบยอด WDF) — เปิดเฉพาะหน้าทดสอบก่อน
if (window.TEST_MODE) Object.assign(OTTERI_CONFIG, {
  t2Sys: true,""", """  hasToken: false, // Otteri ใช้แค่เหรียญ 10 ไม่มี token ของร้าน
};
// 🧪 Otteri ใช้ระบบแบบเท็ดดี้ 2 (เงินสดในมือ · เริ่มเครื่องผ่าน SOL · กระทบยอด WDF) — เปิดเฉพาะหน้าทดสอบก่อน
if (window.TEST_MODE) Object.assign(OTTERI_CONFIG, {
  ownerLaundry: true, // 👔 แม่บ้านลงผ้าเจ้าของเองได้ (ฟรี · งานภายใน)
  accounts: [{ id: 'geisha', name: 'ร้านเกอิชา', emoji: '🏢', noFold: true }], // 🏢 ค้างจ่าย รวมบิลสิ้นเดือน · ไม่พับ · ราคาปกติ (ไม่ใช้โปรวันพุธ)
  t2Sys: true,""", 'jobs: otteri flags')
rep("const SHOP_MENUS = { otteri: { internal: false, promoCredit: false, exchange: false } };",
    "const SHOP_MENUS = { otteri: { internal: false, promoCredit: false, exchange: false } };\nif (window.TEST_MODE) SHOP_MENUS.otteri.internal = true; // 🧪 Otteri: แม่บ้านล้างเครื่อง (ทุก 7 วัน) + ผ้าเจ้าของ", 'jobs: otteri internal menu')

# งานภายในประเภทใหม่ + ตัวช่วย
rep("""  { id: 'redo', label: 'ซักซ้ำให้ลูกค้า', emoji: '🔁' },
  { id: 'other', label: 'อื่นๆ', emoji: '📝' },
];
const isInternalOrder = (o) => !!(o && o.internalType);""", """  { id: 'redo', label: 'ซักซ้ำให้ลูกค้า', emoji: '🔁' },
  { id: 'mine', label: 'ผ้าเจ้าของ', emoji: '👔', cfg: 'ownerLaundry' }, // แม่บ้านลงได้ · ฟรี · ไม่ต้องระบุเครื่อง
  { id: 'other', label: 'อื่นๆ', emoji: '📝' },
];
const isInternalOrder = (o) => !!(o && o.internalType);
const internalTypesFor = (config) => INTERNAL_TYPES.filter(t => !t.cfg || !!(config && config[t.cfg]));
// 🏢 ลูกค้าประจำแบบค้างจ่าย (paymentMethod 'account' + accountId) — ไม่ใช่เงินสด/โอน · เจ้าของกดรับเงินทีหลัง
const accountOf = (o, config) => (o && o.paymentMethod === 'account' ? (((config && config.accounts) || []).find(a => a.id === o.accountId) || { id: o.accountId || '', name: o.customerName || '' }) : null);
const accountPayText = (o, config) => { const a = accountOf(o, config); return a ? `ค้างจ่าย · ${a.name}` : ''; };""", 'jobs: internal type + helpers')

# ---- หน้าแรก: ไทล์ 👔 ผ้าเจ้าของ + 🏢 ร้านเกอิชา ----
rep("function HomeView({ onResumeDraft, onToggleLang, onOpenChecklist, config, orders, tokenExchanges, collections, onAddToken, onDeleteToken, onNewOrder, onInternalOrder,",
    "function HomeView({ onResumeDraft, onToggleLang, onOpenChecklist, config, orders, tokenExchanges, collections, onAddToken, onDeleteToken, onNewOrder, onInternalOrder, onAccountOrder,", 'jobs: home props')
rep("""          menuOn(config, 'internal') && { k: 'clean', icon: ownerNow ? '🔧' : '🧼', title: ownerNow ? tr(config, 'งานภายในร้าน') : tr(config, 'ล้างเครื่อง'), sub: ownerNow ? tr(config, 'ไม่ใช่รายได้') : tr(config, 'ทุก 7 วัน'), on: false, click: onInternalOrder },
""", """          menuOn(config, 'internal') && { k: 'clean', icon: ownerNow ? '🔧' : '🧼', title: ownerNow ? tr(config, 'งานภายในร้าน') : tr(config, 'ล้างเครื่อง'), sub: ownerNow ? tr(config, 'ไม่ใช่รายได้') : tr(config, 'ทุก 7 วัน'), on: false, click: onInternalOrder },
          menuOn(config, 'internal') && config.ownerLaundry && { k: 'mine', icon: '👔', title: tr(config, 'ผ้าเจ้าของ'), sub: tr(config, 'ฟรี · ไม่นับรายได้'), on: false, click: () => onInternalOrder('mine') },
          ...(config.accounts || []).map(a => ({ k: 'acct-' + a.id, icon: a.emoji || '🏢', title: tr(config, a.name), sub: tr(config, a.noFold ? 'ค้างจ่าย · ไม่พับ' : 'ค้างจ่าย'), on: false, click: () => onAccountOrder && onAccountOrder(a.id) })),
""", 'jobs: home tiles')
rep("""    if (isInternalOrder(o)) return { t: 'งานภายใน', c: '#475569', bg: '#F1F5F9' };
""", """    if (isInternalOrder(o)) return { t: 'งานภายใน', c: '#475569', bg: '#F1F5F9' };
    if (o.paymentMethod === 'account') return { t: o.collected ? 'ค้างจ่าย · รับแล้ว' : 'ค้างจ่าย', c: '#0369A1', bg: '#E0F2FE' };
""", 'jobs: home row status')

# ---- App: เปิดฟอร์มตามปุ่ม ----
rep("  const [internalMode, setInternalMode] = useState(false); // 🔧 เปิดหน้ารับงานในโหมดงานภายในร้าน",
    "  const [internalMode, setInternalMode] = useState(false); // 🔧 เปิดหน้ารับงานในโหมดงานภายในร้าน (true = ล้างเครื่อง · 'mine' = ผ้าเจ้าของ)\n  const [accountMode, setAccountMode] = useState(null); // 🏢 เปิดหน้ารับงานเป็นงานลูกค้าประจำค้างจ่าย", 'jobs: app state')
rep("onResumeDraft={(d) => { setOrderDraft(d); setInternalMode(false); setBackdateDay(null); setView('newOrder'); }}",
    "onResumeDraft={(d) => { setOrderDraft(d); setInternalMode(false); setAccountMode(null); setBackdateDay(null); setView('newOrder'); }}", 'jobs: app resume')
rep("onNewOrder={(day) => { setOrderDraft(null); setInternalMode(false); setBackdateDay(typeof day === 'number' ? day : null); setView('newOrder'); }} onInternalOrder={() => { setOrderDraft(null); setInternalMode(true); setBackdateDay(null); setView('newOrder'); }}",
    "onNewOrder={(day) => { setOrderDraft(null); setInternalMode(false); setAccountMode(null); setBackdateDay(typeof day === 'number' ? day : null); setView('newOrder'); }} onInternalOrder={(t) => { setOrderDraft(null); setAccountMode(null); setInternalMode(typeof t === 'string' ? t : true); setBackdateDay(null); setView('newOrder'); }} onAccountOrder={(id) => { setOrderDraft(null); setInternalMode(false); setAccountMode(id); setBackdateDay(null); setView('newOrder'); }}", 'jobs: app home handlers')
rep("onNewOrder={() => { setOrderDraft(null); setBackdateDay(null); setView('newOrder'); }}",
    "onNewOrder={() => { setOrderDraft(null); setAccountMode(null); setBackdateDay(null); setView('newOrder'); }}", 'jobs: app owner new', count=2)
rep("<NewOrderView config={config} orders={orders} backdateDay={internalMode ? null : backdateDay} draft={internalMode ? null : orderDraft}",
    "<NewOrderView config={config} orders={orders} backdateDay={internalMode ? null : backdateDay} draft={internalMode ? null : orderDraft} accountMode={internalMode ? null : accountMode}", 'jobs: app form prop')

# ---- ฟอร์มรับงาน ----
rep("function NewOrderView({ config, onCancel, onSubmit, editingOrder, isOwner, internalMode, backdateDay, orders, draft }) {",
    "function NewOrderView({ config, onCancel, onSubmit, editingOrder, isOwner, internalMode, backdateDay, orders, draft, accountMode }) {", 'jobs: form props')
rep("  const [internalType, setInternalType] = useState(() => editingOrder?.internalType || (internalMode ? 'clean' : ''));",
    "  const [internalType, setInternalType] = useState(() => editingOrder?.internalType || (internalMode ? (typeof internalMode === 'string' ? internalMode : 'clean') : ''));", 'jobs: form internal init')
rep("  const [internalMachines, setInternalMachines] = useState(() => editingOrder?.internalMachines || []);\n",
    """  const [internalMachines, setInternalMachines] = useState(() => editingOrder?.internalMachines || []);
  // 🏢 ลูกค้าประจำค้างจ่าย
  const [accountId, setAccountId] = useState(() => (editingOrder ? (editingOrder.paymentMethod === 'account' ? editingOrder.accountId || null : null) : ((draft && draft.accountId) || accountMode || null)));
  const acct = internalType || !accountId ? null : (((config.accounts || []).find(a => a.id === accountId)) || (editingOrder && editingOrder.paymentMethod === 'account' ? { id: accountId, name: editingOrder.customerName || '' } : null));
""", 'jobs: form account state')
rep("  const [foldBaskets, setFoldBaskets] = useState(seed?.foldBaskets ?? (config.freeService ? 0 : 1));",
    "  const [foldBaskets, setFoldBaskets] = useState(seed?.foldBaskets ?? (acct && acct.noFold ? 0 : config.freeService ? 0 : 1));", 'jobs: form fold init')
rep("  const [noFold, setNoFold] = useState(seed?.noFold || false); // ลูกค้าไม่ต้องการพับ (เฉพาะร้านฟรี)\n",
    """  const [noFold, setNoFold] = useState(seed?.noFold || false); // ลูกค้าไม่ต้องการพับ (เฉพาะร้านฟรี)
  const pickAccount = (id) => { // 🏢 สลับ งานลูกค้าทั่วไป ⇄ งานลูกค้าประจำค้างจ่าย
    const a = id ? (config.accounts || []).find(x => x.id === id) : null;
    setAccountId(id || null);
    if (a && a.noFold) setFoldBaskets(0);
    else if (!a && !config.freeService && foldBaskets === 0) setFoldBaskets(1);
  };
""", 'jobs: form pickAccount')
rep("pickupTime, hadPhoto: !!basketPhoto });", "pickupTime, hadPhoto: !!basketPhoto, accountId: accountId || null });", 'jobs: draft accountId')
rep("fromKev, fromLine, useLinePromo, pickupTime, basketPhoto]);", "fromKev, fromLine, useLinePromo, pickupTime, basketPhoto, accountId]);", 'jobs: draft deps')
rep("noDayPromo: editingOrder ? (editingOrder.noDayPromo || false) : (config.dayPromoEnabled === false),",
    "noDayPromo: editingOrder ? (editingOrder.noDayPromo || false) : (config.dayPromoEnabled === false || !!acct), // 🏢 ค้างจ่าย = ราคาปกติ", 'jobs: no day promo', count=2)
rep("  const needCustomerInfo = !isInternal && !!config.requirePhone && isWalkIn;",
    "  const needCustomerInfo = !isInternal && !acct && !!config.requirePhone && isWalkIn;", 'jobs: customer info')
rep("  const internalOk = !isInternal || (internalMachines.length > 0 && (!needInternalDetail || (internalReason.trim().length > 0 && (hasAnyItem || customAmt > 0))));",
    "  const internalOk = !isInternal || (internalType === 'mine' ? (washItems.length > 0 || dryItems.length > 0) : (internalMachines.length > 0 && (!needInternalDetail || (internalReason.trim().length > 0 && (hasAnyItem || customAmt > 0)))));", 'jobs: internal ok')
rep("  if (isInternal && internalMachines.length === 0) missingList.push('เลือกเครื่องที่ทำ (บังคับ)');",
    "  if (isInternal && internalType !== 'mine' && internalMachines.length === 0) missingList.push('เลือกเครื่องที่ทำ (บังคับ)');\n  if (internalType === 'mine' && !washItems.length && !dryItems.length) missingList.push(tr(config, 'เลือกซักหรืออบอย่างน้อย 1 อย่าง'));", 'jobs: missing mine')
rep("\\nเครื่อง: ${internalMachines.join(', ')}", "${internalMachines.length ? '\\nเครื่อง: ' + internalMachines.join(', ') : ''}", 'jobs: internal confirm')
rep("""    } else if (paymentMethod === 'split') {
      splitCashNum = parseFloat(splitCash) || 0;""", """    } else if (acct) { // 🏢 ค้างจ่าย — ไม่รับเงิน
      if (!confirm(`✅ ${tr(config, 'ยืนยันการรับงาน')}\\n\\n${acct.emoji || '🏢'} ${tr(config, acct.name)}\\n${tr(config, 'วิธีจ่าย')}: ${tr(config, 'ค้างจ่าย รวมบิลสิ้นเดือน · ไม่ต้องรับเงิน')}\\n${tr(config, 'ยอด')}: ${formatMoney(total)} ${tr(config, 'บาท')}${acct.noFold ? '\\n🚫 ' + tr(config, 'ไม่พับ · ซักอบอย่างเดียว') : ''}`)) return;
    } else if (paymentMethod === 'split') {
      splitCashNum = parseFloat(splitCash) || 0;""", 'jobs: account confirm')
rep("      customerName: name.trim() || '(ไม่ระบุชื่อ)',\n      customerPhone: phone.trim() || '',",
    "      customerName: acct ? acct.name : internalType === 'mine' ? '👔 ผ้าเจ้าของ' : (name.trim() || '(ไม่ระบุชื่อ)'),\n      customerPhone: acct ? '' : (phone.trim() || ''),", 'jobs: submit name')
rep("    washItems, dryItems, detergentQty, softenerQty, foldBaskets,\n    deliveryZone, useLinePromo,",
    "    washItems, dryItems, detergentQty, softenerQty, foldBaskets: internalType ? 0 : foldBaskets, // งานภายในไม่มีค่าพับ (ร้านที่คิดค่าพับ เช่น Otteri)\n    deliveryZone, useLinePromo,", 'jobs: temp order fold')
rep("      foldBaskets: foldBaskets || 0,\n      noFold: config.freeService ? (noFold || false) : false,\n      paymentMethod: internalType ? 'internal' : (paymentMethod || 'cash'),\n      cashAmount: paymentMethod === 'split' ? splitCashNum : null,\n      transferAmount: paymentMethod === 'split' ? splitTransferNum : null,",
    "      foldBaskets: internalType || (acct && acct.noFold) ? 0 : (foldBaskets || 0),\n      noFold: acct && acct.noFold ? true : config.freeService ? (noFold || false) : false,\n      paymentMethod: internalType ? 'internal' : acct ? 'account' : (paymentMethod || 'cash'),\n      accountId: acct ? acct.id : null,\n      cashAmount: !acct && paymentMethod === 'split' ? splitCashNum : null,\n      transferAmount: !acct && paymentMethod === 'split' ? splitTransferNum : null,", 'jobs: submit pay')
rep("      cashCollected: paymentMethod === 'split' ? (editingOrder?.cashCollected || false) : null,\n      transferCollected: paymentMethod === 'split' ? (editingOrder?.transferCollected || false) : null,",
    "      cashCollected: !acct && paymentMethod === 'split' ? (editingOrder?.cashCollected || false) : null,\n      transferCollected: !acct && paymentMethod === 'split' ? (editingOrder?.transferCollected || false) : null,", 'jobs: submit split flags')

# ฟอร์มงานภายใน: แม่บ้านเลือก ล้างเครื่อง / ผ้าเจ้าของ
rep("""              <p className="font-extrabold text-slate-900">{isOwner ? '🔧 งานภายในร้าน' : '🧼 ' + tr(config, 'ล้างเครื่อง')}</p>""",
    """              <p className="font-extrabold text-slate-900">{isOwner ? '🔧 งานภายในร้าน' : internalType === 'mine' ? '👔 ' + tr(config, 'ผ้าเจ้าของ') : '🧼 ' + tr(config, 'ล้างเครื่อง')}</p>""", 'jobs: internal title')
rep("""            {isOwner && <p className="text-xs font-bold text-slate-700 mb-1.5">ประเภทงาน</p>}
            {isOwner && <div className="flex flex-wrap gap-1.5 mb-3">
              {INTERNAL_TYPES.map(t => {
                const locked = !isOwner && INTERNAL_OWNER_ONLY.includes(t.id);
                return (
                  <button key={t.id} onClick={() => { if (locked) { alert('🔒 ' + t.label + ' — เฉพาะเจ้าของ'); return; } setInternalType(t.id); }}""",
    """            {isOwner && <p className="text-xs font-bold text-slate-700 mb-1.5">ประเภทงาน</p>}
            {(isOwner || config.ownerLaundry) && <div className="flex flex-wrap gap-1.5 mb-3">
              {internalTypesFor(config).filter(t => isOwner || !INTERNAL_OWNER_ONLY.includes(t.id)).map(t => {
                const locked = !isOwner && INTERNAL_OWNER_ONLY.includes(t.id);
                return (
                  <button key={t.id} data-itype={t.id} onClick={() => { if (locked) { alert('🔒 ' + t.label + ' — เฉพาะเจ้าของ'); return; } if (t.id !== internalType && (t.id === 'mine' || internalType === 'mine')) { setInternalMachines([]); if (!isOwner) { setWashItems([]); setDryItems([]); } } setInternalType(t.id); }}""", 'jobs: internal chips')
rep("""                    {locked ? '🔒' : t.emoji} {t.label}""", """                    {locked ? '🔒' : t.emoji} {isOwner ? t.label : tr(config, t.label)}""", 'jobs: chip label')
rep("""            {!isOwner && <p className="text-[11px] font-bold text-slate-700 mb-3">{tr(config, 'ล้างได้เฉพาะเครื่องซัก เครื่องละ 1 ครั้งต่อ 7 วัน')}</p>}
            <p className="text-xs font-bold text-slate-700 mb-1.5">""", """            {!isOwner && internalType === 'clean' && <p className="text-[11px] font-bold text-slate-700 mb-3">{tr(config, 'ล้างได้เฉพาะเครื่องซัก เครื่องละ 1 ครั้งต่อ 7 วัน')}</p>}
            {internalType === 'mine' && <p className="text-[11px] font-bold text-slate-700 mb-1">{tr(config, 'ฟรี · ไม่นับเป็นรายได้ · เลือกซัก/อบด้านล่าง แล้วเริ่มเครื่องเหมือนงานลูกค้า')}</p>}
            {internalType !== 'mine' && <React.Fragment>
            <p className="text-xs font-bold text-slate-700 mb-1.5">""", 'jobs: internal hint')
rep("""            </div>

            {maidClean && (""", """            </div>
            </React.Fragment>}

            {maidClean && (""", 'jobs: internal machines wrap')
rep(": 'เลือกเครื่องด้านล่างได้เลย — ไม่ต้องกรอกเหตุผล/ราคา'}</p>", ": internalType === 'mine' ? '' : 'เลือกเครื่องด้านล่างได้เลย — ไม่ต้องกรอกเหตุผล/ราคา'}</p>", 'jobs: internal footer')

# ข้อมูลลูกค้า: ปุ่ม 🏢 ร้านเกอิชา
rep("""        {!isInternal && <Section iconName="user" title={tr(config, "ข้อมูลลูกค้า")}>
""", """        {!isInternal && <Section iconName="user" title={tr(config, "ข้อมูลลูกค้า")}>
          {(config.accounts || []).length > 0 && <div className="flex flex-wrap gap-1.5 mb-3">
            {(config.accounts || []).map(a => (
              <button key={a.id} data-account={a.id} onClick={() => pickAccount(accountId === a.id ? null : a.id)}
                className={`px-3 py-1.5 rounded-full text-sm font-bold border-2 transition ${accountId === a.id ? 'bg-sky-700 text-white border-sky-700' : 'bg-white text-sky-800 border-sky-200'}`}>
                {accountId === a.id ? '✓ ' : ''}{a.emoji || '🏢'} {tr(config, a.name)} · {tr(config, 'ค้างจ่าย')}
              </button>
            ))}
          </div>}
          {acct ? (
            <div className="rounded-xl bg-sky-50 border-2 border-sky-300 px-3 py-2.5" data-account-box>
              <p className="font-extrabold text-sky-900">{acct.emoji || '🏢'} {tr(config, acct.name)}</p>
              <p className="text-xs font-bold text-sky-800">{tr(config, 'ค้างจ่าย รวมบิลสิ้นเดือน · ไม่ต้องรับเงิน')}{acct.noFold ? ' · ' + tr(config, 'ไม่พับ') : ''}</p>
            </div>
          ) : <React.Fragment>
""", 'jobs: customer account chips')
rep("""            {needPhone && !phoneOk && <p className="text-xs text-amber-700 mt-1 font-medium">{tr(config, "จำเป็นต้องกรอก — ใช้ติดต่อลูกค้าตอนงานเสร็จ")}</p>}
          </Field>
        </Section>}""", """            {needPhone && !phoneOk && <p className="text-xs text-amber-700 mt-1 font-medium">{tr(config, "จำเป็นต้องกรอก — ใช้ติดต่อลูกค้าตอนงานเสร็จ")}</p>}
          </Field>
          </React.Fragment>}
        </Section>}""", 'jobs: customer account close')
# ค่าพับ: งานเกอิชาไม่พับ
rep("""          {!config.freeService && (
            <CounterRow iconEmoji="🧺" label={tr(config, "ค่าพับผ้า")}""", """          {acct && acct.noFold && <p className="text-xs font-bold text-sky-800 bg-sky-50 border border-sky-200 rounded-xl px-3 py-2">🚫 {tr(config, acct.name)}: {tr(config, 'ไม่พับ · ซักอบอย่างเดียว')}</p>}
          {!config.freeService && !(acct && acct.noFold) && (
            <CounterRow iconEmoji="🧺" label={tr(config, "ค่าพับผ้า")}""", 'jobs: fold hide')
# การชำระเงิน: ค้างจ่าย
rep("""        {!isInternal && <Section iconName="dollar-sign" title={tr(config, "การชำระเงิน")}>""", """        {!isInternal && acct && <Section iconName="dollar-sign" title={tr(config, "การชำระเงิน")}>
          <div className="rounded-2xl p-4 border bg-sky-50 border-sky-200" data-account-pay>
            <p className="text-sm font-extrabold text-sky-900">{acct.emoji || '🏢'} {tr(config, 'ค้างจ่าย')} · {tr(config, acct.name)}</p>
            <p className="text-xs font-bold text-sky-800 mt-0.5">{tr(config, 'ไม่ต้องรับเงิน ไม่ต้องให้สแกน — เจ้าของเก็บรวมสิ้นเดือน')}</p>
            <div className="flex items-center justify-between mt-2">
              <span className="text-slate-600 text-sm font-semibold">{tr(config, 'ยอดลงบิล')}</span>
              <span className="text-2xl font-extrabold text-sky-700">฿{formatMoney(total)}</span>
            </div>
          </div>
          <Field label={tr(config, "หมายเหตุ (ไม่บังคับ)")}>
            <textarea value={note} onChange={(e) => setNote(e.target.value)} rows={2} className="w-full px-4 py-3 bg-slate-50 rounded-xl border border-slate-200 focus:border-sky-500 focus:bg-white outline-none transition resize-none" />
          </Field>
        </Section>}
        {!isInternal && !acct && <Section iconName="dollar-sign" title={tr(config, "การชำระเงิน")}>""", 'jobs: account pay section')
rep("{isInternal ? '🔧 เครดิตที่ใช้ (งานภายใน)' : tr(config, 'ยอดรวม') + ' • ' + tr(config, paymentMethod === 'transfer' ? 'โอน' : 'เงินสด')}",
    "{isInternal ? (internalType === 'mine' ? '👔 ' + tr(config, 'ผ้าเจ้าของ · ฟรี') : '🔧 เครดิตที่ใช้ (งานภายใน)') : tr(config, 'ยอดรวม') + ' • ' + (acct ? tr(config, 'ค้างจ่าย') + ' · ' + tr(config, acct.name) : tr(config, paymentMethod === 'transfer' ? 'โอน' : 'เงินสด'))}", 'jobs: bottom label')

# ---- ใบรับงาน / ใบงาน / ข้อความ LINE / หน้ารายละเอียด / Excel ----
rep("(${order.paymentMethod === 'transfer' ? 'โอน' : 'เงินสด'})", "(${order.paymentMethod === 'account' ? accountPayText(order, config) : order.paymentMethod === 'transfer' ? 'โอน' : 'เงินสด'})", 'jobs: line text')
rep("{internal ? '🔧 งานภายใน (ไม่ใช่รายได้)' : (order.paymentMethod === 'transfer' ? '💳 โอน' : '💵 เงินสด')}",
    "{internal ? '🔧 งานภายใน (ไม่ใช่รายได้)' : order.paymentMethod === 'account' ? '🏢 ' + accountPayText(order, config) : (order.paymentMethod === 'transfer' ? '💳 โอน' : '💵 เงินสด')}", 'jobs: receipt pay')
rep("{order.paymentMethod === 'transfer' ? 'โอน' : order.paymentMethod === 'split' ? `แยกจ่าย",
    "{order.paymentMethod === 'account' ? accountPayText(order, config) : order.paymentMethod === 'transfer' ? 'โอน' : order.paymentMethod === 'split' ? `แยกจ่าย", 'jobs: ticket pay')
rep("""                    return `${order.foldBaskets > 0 ? '☑' : '☐'} พับ""", """                    if (order.paymentMethod === 'account' && order.noFold) return '☒ ไม่พับ (ซักอบอย่างเดียว)';
                    return `${order.foldBaskets > 0 ? '☑' : '☐'} พับ""", 'jobs: ticket fold')
rep("""          {order.paymentMethod === 'transfer' ? '💳 โอน' : '💵 สด'}""", """          {order.paymentMethod === 'account' ? '🏢 ค้างจ่าย' : order.paymentMethod === 'transfer' ? '💳 โอน' : '💵 สด'}""", 'jobs: detail badge')
rep("""            <span>{order.paymentMethod === 'transfer' ? '💳 โอน' : '💵 เงินสด'}</span>""", """            <span>{order.paymentMethod === 'account' ? '🏢 ' + accountPayText(order, config) : order.paymentMethod === 'transfer' ? '💳 โอน' : '💵 เงินสด'}</span>""", 'jobs: detail pay')
rep("      o.paymentMethod === 'transfer' ? 'โอน' : o.paymentMethod === 'split' ? 'สด+โอน' : 'เงินสด',",
    "      o.paymentMethod === 'account' ? accountPayText(o, config) : o.paymentMethod === 'transfer' ? 'โอน' : o.paymentMethod === 'split' ? 'สด+โอน' : 'เงินสด',", 'jobs: excel pay')

# ---- ลูกค้าเพิ่มเวลาอบ: งานค้างจ่าย → รวมในบิล ----
rep("setAddPay(job.order.paymentMethod === 'transfer' ? 'transfer' :", "setAddPay(job.order.paymentMethod === 'transfer' || job.order.paymentMethod === 'account' ? 'transfer' :", 'jobs: addtime default')
rep("""                  {tile(addPay === 'cash', '#059669', () => setAddPay('cash'), '💵', <span>{tr(config, 'เงินสด')}<br /><span className="text-[11px] font-bold opacity-80">{tr(config, 'หยอดเหรียญที่เครื่อง')}</span></span>, null)}
                  {tile(addPay === 'transfer', '#0284C7', () => setAddPay('transfer'), '💳', <span>{tr(config, 'โอน')}<br /><span className="text-[11px] font-bold opacity-80">{tr(config, 'ยิงจากแอป')}</span></span>, null)}""",
    """                  {job.order.paymentMethod === 'account' ? tile(true, '#0369A1', () => setAddPay('transfer'), '🏢', <span>{tr(config, 'รวมในบิลค้างจ่าย')}</span>, null) : <React.Fragment>
                  {tile(addPay === 'cash', '#059669', () => setAddPay('cash'), '💵', <span>{tr(config, 'เงินสด')}<br /><span className="text-[11px] font-bold opacity-80">{tr(config, 'หยอดเหรียญที่เครื่อง')}</span></span>, null)}
                  {tile(addPay === 'transfer', '#0284C7', () => setAddPay('transfer'), '💳', <span>{tr(config, 'โอน')}<br /><span className="text-[11px] font-bold opacity-80">{tr(config, 'ยิงจากแอป')}</span></span>, null)}
                  </React.Fragment>}""", 'jobs: addtime tiles')

# ---- สรุปค่าเครื่อง (5 ก้อน) ----
rep("clean: 0, cleanN: 0, repair: 0, repairN: 0, redo: 0, redoN: 0,", "clean: 0, cleanN: 0, repair: 0, repairN: 0, redo: 0, redoN: 0, mine: 0, mineN: 0, account: 0, accountN: 0,", 'jobs: buckets init')
rep("      else if (o.internalType === 'redo') { B.redo += used; if (used > 0) B.redoN++; }\n",
    "      else if (o.internalType === 'redo') { B.redo += used; if (used > 0) B.redoN++; }\n      else if (o.internalType === 'mine') { B.mine += used; if (used > 0) B.mineN++; }\n", 'jobs: buckets mine')
rep("    B.transfer += t + manual; B.manual += manual;",
    "    if (o.paymentMethod === 'account') { B.account += t + manual; if (t + manual > 0) B.accountN++; } else B.transfer += t + manual;\n    B.manual += manual;", 'jobs: buckets account')
rep("  B.total = B.cash + B.transfer + B.discount + B.clean + B.repair + B.redo + B.refire + B.over;",
    "  B.total = B.cash + B.transfer + B.discount + B.clean + B.repair + B.redo + B.mine + B.account + B.refire + B.over;", 'jobs: buckets total')
rep("['internal', 'ซ่อม/ทดสอบ', PB.repair]].map(([k, lb, v], i) => (",
    "['internal', 'ซ่อม/ทดสอบ', PB.repair], ...(PB.mine ? [['internal', 'ผ้าเจ้าของ', PB.mine]] : []), ...(PB.account ? [['account', isSol(config) ? 'ค้างจ่าย (กดใน SOL)' : 'ค้างจ่าย (ยิงแอป)', PB.account]] : [])].map(([k, lb, v], i) => (", 'jobs: pulse tab rows')

# ---- หน้าเจ้าของ: แท็บ 🏢 ค้างจ่าย + รับเงินรายเดือน ----
rep("  transfer: { c: '#6D28D9', soft: '#F5F3FF', ic: '💳', name: 'โอน' },\n",
    "  transfer: { c: '#6D28D9', soft: '#F5F3FF', ic: '💳', name: 'โอน' },\n  account: { c: '#0369A1', soft: '#E0F2FE', ic: '🏢', name: 'ค้างจ่าย' },\n", 'jobs: T2C account')
rep("  { id: 'money', ic: '💰', label: 'เงิน', tabs: ['overview', 'cash', 'transfer', 'discount'] },",
    "  { id: 'money', ic: '💰', label: 'เงิน', tabs: ['overview', 'cash', 'transfer', 'discount', 'account'] }, // account = เฉพาะร้านที่มีลูกค้าค้างจ่าย", 'jobs: T2 groups')
rep("const t2RoundLabel = (m) => (m === 'cash' ? 'เก็บเงินสด' :", "const t2RoundLabel = (m) => (m === 'account' ? 'รับเงินค้างจ่าย' : m === 'cash' ? 'เก็บเงินสด' :", 'jobs: round label')
rep("det: 0, detN: 0, detCash: 0, detTransfer: 0, dlist: [] };", "det: 0, detN: 0, detCash: 0, detTransfer: 0, dlist: [], account: 0, accountN: 0, accountPending: 0 };", 'jobs: agg init')
rep("    const cash = orderCashPart(o, config), tr = orderTransferPart(o, config);\n",
    "    const cash = orderCashPart(o, config), tr = orderTransferPart(o, config);\n    if (o.paymentMethod === 'account') { A.account += b.total; A.accountN++; if (!o.collected) A.accountPending += b.total; }\n", 'jobs: agg account')
rep("  const bar = internal ? T2C.internal.c : pm === 'transfer' ? T2C.transfer.c :", "  const bar = internal ? T2C.internal.c : pm === 'account' ? T2C.account.c : pm === 'transfer' ? T2C.transfer.c :", 'jobs: row bar')
rep("            : pm === 'transfer' ? pay('โอน', 'transfer') : pay('สด', 'cash')}",
    "            : pm === 'account' ? pay(o.collected ? 'ค้างจ่าย · รับแล้ว' : 'ค้างจ่าย', 'account') : pm === 'transfer' ? pay('โอน', 'transfer') : pay('สด', 'cash')}", 'jobs: row pay')
rep("            {moneyRow('transfer', A.transfer, `${formatMoney(A.transferN)} ใบ`, A.sales > 0 ? 100 - cashPct : 0)}",
    "            {moneyRow('transfer', A.transfer, `${formatMoney(A.transferN)} ใบ`, A.sales > 0 ? 100 - cashPct - pct(A.account) : 0)}\n            {A.account > 0 && moneyRow('account', A.account, `${formatMoney(A.accountN)} ใบ · ${A.accountPending > 0 ? 'ยังไม่ได้รับ ฿' + formatMoney(A.accountPending) : 'รับเงินครบแล้ว'}`, pct(A.account))}", 'jobs: money row')
rep("""            <div style={{ width: (A.sales > 0 ? 100 - cashPct : 0) + '%', background: T2C.transfer.c }}></div>""",
    """            <div style={{ width: (A.sales > 0 ? 100 - cashPct - pct(A.account) : 0) + '%', background: T2C.transfer.c }}></div>
            {A.account > 0 && <div style={{ width: pct(A.account) + '%', background: T2C.account.c }}></div>}""", 'jobs: money bar')
rep("{A.internal > 0 && moneyRow('internal', A.internal, `${A.internalN} งาน · ล้าง/ซ่อม/ซักซ้ำ`, null, true)}",
    "{A.internal > 0 && moneyRow('internal', A.internal, `${A.internalN} งาน · ${config.ownerLaundry ? 'ล้าง/ผ้าเจ้าของ/ซ่อม' : 'ล้าง/ซ่อม/ซักซ้ำ'}`, null, true)}", 'jobs: internal row')
rep("""  if (riderUnpaid > 0) todo.push(""", """  const accPendList = cust.filter(o => o.paymentMethod === 'account' && !o.collected); // 🏢
  if (accPendList.length) todo.push({ k: 'account', title: `🏢 ค้างจ่าย ฿${formatMoney(accPendList.reduce((s, o) => s + calculateTotal(o, config), 0))}`, sub: `${accPendList.length} ใบ · ${[...new Set(accPendList.map(o => (accountOf(o, config) || {}).name))].join(', ')} · รวมบิลสิ้นเดือน`, nav: 'ดูบิล', go: 'account' });
  if (riderUnpaid > 0) todo.push(""", 'jobs: todo account')
rep("""            {group.tabs.map(k => (
              <button key={k} onClick={() => setTab(k)}""", """            {group.tabs.filter(k => k !== 'account' || (config.accounts || []).length > 0).map(k => (
              <button key={k} onClick={() => setTab(k)}""", 'jobs: tabs filter')
rep("""        {tab === 'discount' && (""", """        {tab === 'account' && (() => {
          const accAll = cust.filter(o => o.paymentMethod === 'account');
          const inR = (o) => { const t = t2Ts(o.createdAt); return t >= R.from && t < R.to; };
          const sumOf = (arr) => arr.reduce((s, o) => s + calculateTotal(o, config), 0);
          const accList = A.list.filter(o => o.paymentMethod === 'account');
          return (
          <div className="space-y-2.5">
            {(config.accounts || []).map(a => {
              const mine = accAll.filter(o => o.accountId === a.id);
              const per = mine.filter(inR), perPend = per.filter(o => !o.collected), allPend = mine.filter(o => !o.collected);
              return (
                <T2Box key={a.id} k="account" title={`${a.emoji || '🏢'} ${a.name} · ${R.label}`} right={<span className="text-xs font-bold text-slate-500">{a.noFold ? 'ไม่พับ · ' : ''}รวมบิลสิ้นเดือน</span>}>
                  <div className="grid grid-cols-2 gap-2 mb-2">
                    <T2Stat label="ยอดบิล" value={'฿' + formatMoney(sumOf(per))} sub={`${per.length} ใบ`} color={T2C.account.c} />
                    <T2Stat label="ยังไม่ได้รับ" value={'฿' + formatMoney(sumOf(perPend))} sub={allPend.length > perPend.length ? `ค้างทุกเดือน ฿${formatMoney(sumOf(allPend))}` : `${perPend.length} ใบ`} />
                  </div>
                  {perPend.length > 0
                    ? actBtn('account', `รับเงินแล้ว · บิล${R.label} ฿${formatMoney(sumOf(perPend))}`, () => doCollectAccount(a, perPend))
                    : <p className="text-sm font-bold text-emerald-700">✓ {R.label} รับเงินครบแล้ว{allPend.length ? ` · ยังค้างช่วงอื่น ${allPend.length} ใบ` : ''}</p>}
                  {mode === 'day' && perPend.length > 0 && <p className="text-xs text-slate-500 mt-1.5">💡 เลือก "รายเดือน" ด้านบน เพื่อรับเงินทั้งบิลของเดือน</p>}
                </T2Box>
              );
            })}
            {history(m => m === 'account', 'account')}
            {listHead(`ใบงานค้างจ่าย · ${R.label}`, accList.length)}
            {list(accList)}
          </div>
          ); })()}

        {tab === 'discount' && (""", 'jobs: account tab')
rep("""  const doPayRider = async (riderId) => {""", """  const doCollectAccount = async (a, items) => { // 🏢 รับเงินบิลค้างจ่าย (กด ↶ ยกเลิกได้)
    const sum = items.reduce((s, o) => s + calculateTotal(o, config), 0);
    if (!items.length || !confirm(`🏢 รับเงินจาก ${a.name} แล้ว?\\n\\nบิล${R.label} · ${items.length} ใบ · ฿${formatMoney(sum)}\\n\\nใบงานจะเป็น "รับเงินแล้ว" (กด ↶ ยกเลิกได้)`)) return;
    setBusy(true);
    try {
      const now = Date.now();
      const round = { prev: items.map(o => ({ id: o.id, collected: !!o.collected, collectedAt: o.collectedAt || null, collectedVia: o.collectedVia || null })),
        collectedAt: now, method: 'account', accountId: a.id, accountName: a.name, period: R.label,
        orderIds: items.map(o => o.id), orderCount: items.length, totalReceived: sum, totalShould: sum };
      const id = await saveCollectionToCloud(config.brand, round);
      await batchUpdateOrders(round.orderIds, { collected: true, collectedAt: now, collectedVia: 'account' });
      showToast(`✓ รับเงิน ${a.name} ฿${formatMoney(sum)} (${items.length} ใบ)`, () => undoRound({ ...round, id }, false));
    } catch (e) { alert('บันทึกไม่สำเร็จ: ' + (e && e.message ? e.message : e)); }
    finally { setBusy(false); }
  };
  const doPayRider = async (riderId) => {""", 'jobs: collect account')
rep("""                {INTERNAL_TYPES.map(t => (
                  <T2Stat key={t.id}""", """                {internalTypesFor(config).map(t => (
                  <T2Stat key={t.id}""", 'jobs: internal tab types')

# คำแปลพม่า (ให้พนักงานพม่าตรวจ)
rep("""  'ทำต่อ': 'ဆက်လုပ်',
};""", """  'ทำต่อ': 'ဆက်လုပ်',
  // 👔 ผ้าเจ้าของ · 🏢 ลูกค้าค้างจ่าย (หน้าทดสอบ Otteri)
  'ผ้าเจ้าของ': 'ပိုင်ရှင်၏ အဝတ်',
  'ฟรี · ไม่นับรายได้': 'အခမဲ့ · ဝင်ငွေ မတွက်',
  'ผ้าเจ้าของ · ฟรี': 'ပိုင်ရှင်၏ အဝတ် · အခမဲ့',
  'ฟรี · ไม่นับเป็นรายได้ · เลือกซัก/อบด้านล่าง แล้วเริ่มเครื่องเหมือนงานลูกค้า': 'အခမဲ့ · ဝင်ငွေ မတွက် · အောက်တွင် လျှော်/အခြောက်ခံ ရွေးပြီး ဖောက်သည်အလုပ်လို စက်စပါ',
  'เลือกซักหรืออบอย่างน้อย 1 อย่าง': 'လျှော် သို့မဟုတ် အခြောက်ခံ အနည်းဆုံး ၁ ခု ရွေးပါ',
  'ร้านเกอิชา': 'Geisha ဆိုင်',
  'ค้างจ่าย': 'အကြွေး',
  'ค้างจ่าย · ไม่พับ': 'အကြွေး · မခေါက်',
  'ค้างจ่าย · รับแล้ว': 'အကြွေး · ငွေရပြီး',
  'ไม่พับ': 'မခေါက်',
  'ไม่พับ · ซักอบอย่างเดียว': 'မခေါက် · လျှော်/အခြောက်ခံ သာ',
  'ค้างจ่าย รวมบิลสิ้นเดือน · ไม่ต้องรับเงิน': 'အကြွေး လကုန်ပေါင်းရှင်း · ငွေမယူရ',
  'ไม่ต้องรับเงิน ไม่ต้องให้สแกน — เจ้าของเก็บรวมสิ้นเดือน': 'ငွေမယူရ · စကင်မဖတ်ခိုင်းရ — ပိုင်ရှင် လကုန်တွင် ပေါင်းကောက်မည်',
  'ยอดลงบิล': 'ဘေလ်ထဲထည့်မည့်ငွေ',
  'รวมในบิลค้างจ่าย': 'အကြွေးဘေလ်ထဲ ပေါင်းထည့်',
};""", 'jobs: mm dict')

# ---------- 🎨 ui2: หน้าแอป Otteri อ่านง่ายขึ้น (จากรีวิว 29 ต.ค. · 10 ข้อ) — เปิดด้วย config.ui2 ----------
rep("""  ownerLaundry: true, // 👔 แม่บ้านลงผ้าเจ้าของเองได้ (ฟรี · งานภายใน)
""", """  ownerLaundry: true, // 👔 แม่บ้านลงผ้าเจ้าของเองได้ (ฟรี · งานภายใน)
  ui2: true, // 🎨 หน้าตาแบบใหม่ (แจ้งเตือนภาษาคน · แถบเข้างานเล็ก · ฟอร์มสั้นลง · สีเดียว · ผังเครื่องตามหน้าร้าน)
  ui2Accent: '#0EA5E9', // ฟ้า Otteri — ปุ่ม + ทุกปุ่ม
  t2Primary: '#0284C7', // ปุ่มรับงานหน้าเจ้าของ = ฟ้า Otteri (เดิมเขียว Teddy 2)
""", 'ui2: flags')
rep("const internalTypesFor = (config) => INTERNAL_TYPES.filter(t => !t.cfg || !!(config && config[t.cfg]));",
    """const internalTypesFor = (config) => INTERNAL_TYPES.filter(t => !t.cfg || !!(config && config[t.cfg]));
// ชื่องานภายในในรายการ เช่น "🧼 ล้างเครื่อง · W1" (เดิมขึ้น "(ไม่ระบุชื่อ)")
const internalTitleOf = (o, config) => { const t = INTERNAL_TYPES.find(x => x.id === o.internalType) || {}; const ms = (o.internalMachines || []).map(m => String(m).replace(/^(ซัก|อบ) /, '')); return `${t.emoji || '🔧'} ${tr(config, t.label || 'งานภายใน')}${ms.length ? ' · ' + ms.join(', ') : ''}`; };""", 'ui2: internal title helper')
rep("  const [accountMode, setAccountMode] = useState(null); // 🏢 เปิดหน้ารับงานเป็นงานลูกค้าประจำค้างจ่าย",
    "  const [accountMode, setAccountMode] = useState(null); // 🏢 เปิดหน้ารับงานเป็นงานลูกค้าประจำค้างจ่าย\n  window.UI_ACCENT = config.ui2 ? (config.ui2Accent || config.primaryColor) : null; // 🎨 ui2: ปุ่ม + สีเดียว", 'ui2: accent global')

# (3) รายการงานในหน้าแรก: งานภายในขึ้นชื่อประเภท
rep('<p className="font-semibold text-slate-900 truncate">{o.customerName}</p>', '<p className="font-semibold text-slate-900 truncate">{isInternalOrder(o) ? internalTitleOf(o, config) : o.customerName}</p>', 'ui2: home list internal name')
rep("{isInternalOrder(o) ? '🔧' : o.queueNo", "{isInternalOrder(o) ? ((INTERNAL_TYPES.find(t => t.id === o.internalType) || {}).emoji || '🔧') : o.queueNo", 'ui2: home list internal icon')

# (4) การ์ด "วันนี้" อ่านง่ายบนพื้นฟ้าอ่อน
rep("""              <div className="bg-white bg-opacity-15 rounded-2xl p-3 border border-white border-opacity-25">
                <p className="text-white text-xs font-bold">{tr(config, "วันนี้")}</p>""", """              <div className={`rounded-2xl p-3 border border-white border-opacity-25 ${config.ui2 ? '' : 'bg-white bg-opacity-15'}`} style={config.ui2 ? { background: 'rgba(3,105,161,0.78)' } : undefined}>
                <p className="text-white text-xs font-bold">{tr(config, "วันนี้")}</p>""", 'ui2: today card contrast')

# (1) แจ้งเตือนกระทบยอดบนหน้าแรกแม่บ้าน: บอกเป็นภาษาคนว่าต้องทำอะไร
rep("{onlyPending ? `⏳ ${tr(config, 'รอเริ่มเครื่อง')} ${bad} ${tr(config, 'งาน')} — ${tr(config, 'แตะดู')}` : bad > 0 ?",
    "{config.ui2 && bad > 0 ? `${onlyPending ? '⏳' : '⚠️'} ${tr(config, recon.errors[0].text)}${recon.errors[0].label ? ' · ' + recon.errors[0].label : ''}${bad > 1 ? ` ${tr(config, 'และอีก')} ${bad - 1}` : ''}` : onlyPending ? `⏳ ${tr(config, 'รอเริ่มเครื่อง')} ${bad} ${tr(config, 'งาน')} — ${tr(config, 'แตะดู')}` : bad > 0 ?", 'ui2: recon title')
rep("""          <p className="text-xs text-slate-600">
            {tr(config, slim ? 'ค่าเครื่อง' : 'งาน')}""", """          <p className="text-xs text-slate-600">
            {config.ui2 && bad > 0 ? <span data-recon-plain>{tr(config, onlyPending ? 'แตะเพื่อเริ่มเครื่อง' : 'แตะดูว่าต้องทำอะไร')}</span> : <React.Fragment>
            {tr(config, slim ? 'ค่าเครื่อง' : 'งาน')}""", 'ui2: recon sub open')
rep("""recon.issues.filter(i => i.key.startsWith('r:')).length}` : ''}
          </p>
        </div>
        <Icon name="chevron-right" className="w-5 h-5 text-slate-500" />""", """recon.issues.filter(i => i.key.startsWith('r:')).length}` : ''}
            </React.Fragment>}
          </p>
        </div>
        <Icon name="chevron-right" className="w-5 h-5 text-slate-500" />""", 'ui2: recon sub close')

# (1 ต่อ) แถบสรุปเล็ก: ไม่ซ้ำกับการ์ด 🧺 เริ่มเครื่อง (ซ่อนตอนแค่รอเริ่ม) · ไม่โชว์ตัวเลขบัญชี
rep('<button onClick={() => setSheetDate(todayKey)} className="w-full rounded-xl px-3 py-2.5 bg-white border border-slate-200 flex items-center gap-2 text-left active:scale-95 transition">',
    '<button onClick={() => setSheetDate(todayKey)} className={`w-full rounded-xl px-3 py-2.5 bg-white border border-slate-200 flex items-center gap-2 text-left active:scale-95 transition ${config.ui2 && tone === \'amber\' ? \'hidden\' : \'\'}`}>', 'ui2: slim recon hide pending')
rep("<span className=\"text-slate-500\"> · {tr(config, 'แอป')} ฿{formatMoney(recon.appBaht)}", "{!config.ui2 && <span className=\"text-slate-500\"> · {tr(config, 'แอป')} ฿{formatMoney(recon.appBaht)}", 'ui2: slim recon numbers open')
rep(""".length}` : ''}</span>
          </span>
          <span className="text-slate-400 font-bold">›</span>""", """.length}` : ''}</span>}
          </span>
          <span className="text-slate-400 font-bold">›</span>""", 'ui2: slim recon numbers close')
# (2) เข้างานแล้ว → แถบเล็ก · งานประจำวัน → แถบเล็ก
rep("""      {state === 'none' && (
        <button onClick={() => startCapture('in')}""", """      {config.ui2 && state !== 'none' && (
        <button onClick={() => { if (state === 'in') startCapture('out'); }} disabled={busy || state === 'out'} data-att-slim
          className="w-full rounded-xl px-3 py-2.5 bg-white border border-slate-200 flex items-center gap-2 text-left active:scale-95 transition">
          <span className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ background: '#047857' }}></span>
          <span className="flex-1 min-w-0 text-xs font-bold text-slate-700 truncate">✓ {tr(config, 'เข้างาน')} {fmtTime(rec.inAt)}{state === 'out' ? ` · ${tr(config, 'ออกงานแล้ว')} ${fmtTime(rec.outAt)}` : ''}</span>
          {state === 'in' && <span className="text-xs font-extrabold whitespace-nowrap" style={{ color: '#0369A1' }}>🚪 {tr(config, 'ออกงาน')} ›</span>}
        </button>
      )}
      {state === 'none' && (
        <button onClick={() => startCapture('in')}""", 'ui2: attendance slim')
rep("""      {state === 'in' && (
        <button onClick={() => startCapture('out')}""", """      {state === 'in' && !config.ui2 && (
        <button onClick={() => startCapture('out')}""", 'ui2: attendance in old')
rep("""      {state === 'out' && (
        <div className="w-full rounded-2xl p-3 border-2 border-emerald-200""", """      {state === 'out' && !config.ui2 && (
        <div className="w-full rounded-2xl p-3 border-2 border-emerald-200""", 'ui2: attendance out old')
rep("""      {config.hasChecklist && (
        <div className="px-5 mt-3">
          <button onClick={onOpenChecklist}""", """      {config.hasChecklist && config.ui2 && (
        <div className="px-5 mt-2">
          <button onClick={onOpenChecklist} data-check-slim className="w-full rounded-xl px-3 py-2.5 bg-white border border-slate-200 flex items-center gap-2 text-left active:scale-95 transition">
            <span className="text-base leading-none">📋</span>
            <span className="flex-1 min-w-0 text-xs font-bold text-slate-700 truncate">{tr(config, 'งานประจำวัน')} <span className="text-slate-500">· {tr(config, 'ติ๊กก่อนกลับบ้าน')}</span></span>
            <span className="text-slate-400 font-bold">›</span>
          </button>
        </div>
      )}
      {config.hasChecklist && !config.ui2 && (
        <div className="px-5 mt-3">
          <button onClick={onOpenChecklist}""", 'ui2: checklist slim')

# (5) ฟอร์มรับงาน: ซ่อนกล่องงานเว็บตอนว่าง · Line เป็นปุ่มเล็กในข้อมูลลูกค้า
rep("{!isInternal && !isEdit && (", "{!isInternal && !isEdit && (!config.ui2 || pendingWeb.length > 0 || !!webPicked) && (", 'ui2: web box hide')
rep("""        {!isInternal && <button 
          onClick={() => !fromKev && setFromLine(!fromLine)}""", """        {!isInternal && !config.ui2 && <button 
          onClick={() => !fromKev && setFromLine(!fromLine)}""", 'ui2: big line toggle off')
rep("""          {(config.accounts || []).length > 0 && <div className="flex flex-wrap gap-1.5 mb-3">
            {(config.accounts || []).map(a => (""", """          {((config.accounts || []).length > 0 || config.ui2) && <div className="flex flex-wrap gap-1.5 mb-3">
            {config.ui2 && !acct && (
              <button data-line-chip onClick={() => !fromKev && setFromLine(!fromLine)}
                className={`px-3 py-1.5 rounded-full text-sm font-bold border-2 transition ${fromLine ? 'text-white border-transparent' : 'bg-white text-green-700 border-green-200'}`} style={fromLine ? { background: '#06C755' } : undefined}>
                {fromLine ? '✓ ' : '💬 '}{tr(config, 'งานจาก Line')}
              </button>
            )}
            {(config.accounts || []).map(a => (""", 'ui2: line chip')

# (6) ค่าพับ: เริ่ม 0 → ใส่ 1 ตะกร้าให้เองเมื่อเลือกซัก/อบ (แตะ +/− เองแล้วไม่เปลี่ยนให้อีก)
rep("useState(seed?.foldBaskets ?? (acct && acct.noFold ? 0 : config.freeService ? 0 : 1));",
    "useState(seed?.foldBaskets ?? (acct && acct.noFold ? 0 : config.freeService || config.ui2 ? 0 : 1));\n  const foldTouched = useRef(!!seed); // 🎨 ui2: แม่บ้านแตะจำนวนพับเองแล้ว", 'ui2: fold init')
rep("    else if (!a && !config.freeService && foldBaskets === 0) setFoldBaskets(1);",
    "    else if (!a && !config.freeService && foldBaskets === 0 && (!config.ui2 || washItems.length || dryItems.length)) setFoldBaskets(1);", 'ui2: fold on account off')
rep("""  const tempOrder = { 
    washItems, dryItems, detergentQty, softenerQty,""", """  useEffect(() => { // 🎨 ui2: มีซัก/อบ = ฝากพับ 1 ตะกร้า (ยังไม่เลือกอะไร = ยอด 0)
    if (!config.ui2 || foldTouched.current || config.freeService || internalType || (acct && acct.noFold)) return;
    setFoldBaskets(washItems.length || dryItems.length ? 1 : 0);
  }, [washItems.length, dryItems.length]);
  const tempOrder = { 
    washItems, dryItems, detergentQty, softenerQty,""", 'ui2: fold auto')
rep("onAdd={() => setFoldBaskets(q => q + 1)} onRemove={() => setFoldBaskets(q => Math.max(0, q - 1))}",
    "onAdd={() => { foldTouched.current = true; setFoldBaskets(q => q + 1); }} onRemove={() => { foldTouched.current = true; setFoldBaskets(q => Math.max(0, q - 1)); }}", 'ui2: fold touched')

rep("hint={foldBaskets === 0 ?", "hint={foldBaskets === 0 && (!config.ui2 || washItems.length || dryItems.length) ?", 'ui2: fold hint only with machines')
rep("  if (isInternalOrder(order)) return '🔧 ' + ((INTERNAL_TYPES.find(t => t.id === order.internalType) || {}).label || 'งานภายใน');",
    "  if (isInternalOrder(order)) return (config && config.ui2 ? ((INTERNAL_TYPES.find(t => t.id === order.internalType) || {}).emoji || '🔧') : '🔧') + ' ' + ((INTERNAL_TYPES.find(t => t.id === order.internalType) || {}).label || 'งานภายใน');", 'ui2: job label emoji')
# (7) ปุ่ม + สีเดียว · ไม่ใส่อีโมจิซ้ำกับไอคอน
rep("""          <button onClick={onAdd} className={`w-9 h-9 rounded-full flex items-center justify-center text-white shadow-md active:scale-90 transition ${bgClass}`}>""",
    """          <button onClick={onAdd} className={`w-9 h-9 rounded-full flex items-center justify-center text-white shadow-md active:scale-90 transition ${bgClass}`} style={window.UI_ACCENT ? { background: window.UI_ACCENT } : undefined}>""", 'ui2: machine plus color')
rep("""          <button onClick={onAdd} className={`w-9 h-9 rounded-full flex items-center justify-center text-white shadow-md active:scale-90 transition ${colorActive}`}>""",
    """          <button onClick={onAdd} className={`w-9 h-9 rounded-full flex items-center justify-center text-white shadow-md active:scale-90 transition ${colorActive}`} style={window.UI_ACCENT ? { background: window.UI_ACCENT } : undefined}>""", 'ui2: counter plus color')
rep('<span className="text-xs text-sky-700 font-bold">{tr(config, "📷 ถ่ายรูป")}</span>', '<span className="text-xs text-sky-700 font-bold">{tr(config, config.ui2 ? "ถ่ายรูป" : "📷 ถ่ายรูป")}</span>', 'ui2: photo label 1')
rep('<span className="text-xs text-slate-600 font-bold">{tr(config, "🖼️ เลือกจากอัลบั้ม")}</span>', '<span className="text-xs text-slate-600 font-bold">{tr(config, config.ui2 ? "เลือกจากอัลบั้ม" : "🖼️ เลือกจากอัลบั้ม")}</span>', 'ui2: photo label 2')
rep('<span className="text-xs text-sky-700 font-bold">{tr(config, "📷 ถ่าย")}</span>', '<span className="text-xs text-sky-700 font-bold">{tr(config, config.ui2 ? "ถ่าย" : "📷 ถ่าย")}</span>', 'ui2: photo label 3', count=2)
rep('<span className="text-xs text-slate-600 font-bold">{tr(config, "🖼️ เลือกอัลบั้ม")}</span>', '<span className="text-xs text-slate-600 font-bold">{tr(config, config.ui2 ? "เลือกอัลบั้ม" : "🖼️ เลือกอัลบั้ม")}</span>', 'ui2: photo label 4', count=2)

# (8) ใบรับงาน: คำของโหมด SOL
rep("""        <span className="text-2xl">⚡</span>
        <div className="flex-1 min-w-0">
          <p className="font-extrabold text-slate-900">{tr(config, 'เริ่มเครื่อง (ยิงพัลส์)')}</p>""", """        <span className="text-2xl">{isSol(config) ? '🧺' : '⚡'}</span>
        <div className="flex-1 min-w-0">
          <p className="font-extrabold text-slate-900">{tr(config, isSol(config) ? 'เริ่มเครื่อง (กดใน SOL)' : 'เริ่มเครื่อง (ยิงพัลส์)')}</p>""", 'ui2: receipt starter title')
rep("{tr(config, 'เปิดแล้ว')} ฿${fired}", "{tr(config, isSol(config) ? 'เริ่มแล้ว' : 'เปิดแล้ว')} ฿${fired}", 'ui2: receipt started word')
rep("(${tr(config, 'ขาด')} ฿${need - fired})", "(${tr(config, isSol(config) ? 'ยังไม่เริ่ม' : 'ขาด')} ฿${need - fired})", 'ui2: receipt left word')

# (10) หน้าเจ้าของ: ปุ่มรับงานสีของร้าน
# v172: ตัวจริงใช้ t2PrimaryOf(config) (อ่าน config.t2Primary ก่อน) แล้ว — แค่ตรวจว่ายังอยู่
assert s.count("style={{ background: t2PrimaryOf(config) }}>+") == 1, 'ui2: owner fab'

# ล้างเครื่องในหน้าเลือกเครื่อง (โหมด SOL): เลือก Hot ใน SOL ไม่ใช่ที่หน้าเครื่อง
rep("""🧼 {tr(config, 'ล้างเครื่อง (ไม่ต้องใส่ผ้า)')} · ⚠️ {tr(config, 'อย่าลืมกดเลือก 🔥 น้ำร้อน ที่หน้าเครื่องก่อนกดตกลง')}</p>""",
    """🧼 {tr(config, 'ล้างเครื่อง (ไม่ต้องใส่ผ้า)')} · ⚠️ {tr(config, isSol(config) ? 'ใน SOL เลือก Hot (น้ำร้อน)' : 'อย่าลืมกดเลือก 🔥 น้ำร้อน ที่หน้าเครื่องก่อนกดตกลง')}</p>""", 'clean picker SOL wording')
# เลขใบรับงาน: ใช้เลขคิว (เดิม id ใหม่ "otteri-c…" ทำให้ขึ้น #OTTERI ทุกใบ)
rep("""<p className="text-slate-900 font-extrabold text-sm">#{order.id.split('-')[0].toUpperCase()}</p>""",
    """<p className="text-slate-900 font-extrabold text-sm">#{order.queueNo != null ? String(order.queueNo).padStart(2, '0') : order.id.split('-')[0].toUpperCase()}</p>""", 'receipt no = queue no')
# 🏢 ใบงานร้านเกอิชา (ค้างจ่าย) — แถบม่วงแทนแถบดำ "ใบรับงานบริการซักผ้า" ให้รู้ว่าไม่ใช่รับงานปกติ
rep("""            <div className="bg-slate-900 text-white text-center py-2.5">
              <h2 className="text-base font-bold tracking-widest">ใบรับงานบริการซักผ้า</h2>
              <p className="text-slate-300 text-xs mt-0.5">LAUNDRY SERVICE RECEIPT</p>
            </div>
          )}""",
    """            accountOf(order, config) ? (
              <div className="text-white text-center py-3 px-4 border-b-4" data-account-band style={{ background: 'repeating-linear-gradient(135deg, #7C3AED 0 14px, #8B5CF6 14px 28px)', borderColor: '#4C1D95' }}>
                <p className="text-xs font-bold tracking-widest opacity-90">ไม่ใช่รับงานปกติ · งานจากร้านในเครือ</p>
                <p className="text-2xl font-extrabold leading-tight">{(config.accounts || []).find(a => a.id === order.accountId)?.emoji || '🏢'} งาน{accountOf(order, config).name}</p>
                <p className="text-sm font-bold mt-0.5">ค้างจ่าย · รวมบิลสิ้นเดือน{(config.accounts || []).find(a => a.id === order.accountId)?.noFold ? ' · ไม่พับ' : ''}</p>
              </div>
            ) : (
            <div className="bg-slate-900 text-white text-center py-2.5">
              <h2 className="text-base font-bold tracking-widest">ใบรับงานบริการซักผ้า</h2>
              <p className="text-slate-300 text-xs mt-0.5">LAUNDRY SERVICE RECEIPT</p>
            </div>
            )
          )}""", 'geisha receipt band')
# สด+โอน: แถบยอดรวมท้ายฟอร์ม + ข้อความ LINE เดิมขึ้น "เงินสด"
rep("""tr(config, 'ค้างจ่าย') + ' · ' + tr(config, acct.name) : tr(config, paymentMethod === 'transfer' ? 'โอน' : 'เงินสด'))}""",
    """tr(config, 'ค้างจ่าย') + ' · ' + tr(config, acct.name) : tr(config, paymentMethod === 'transfer' ? 'โอน' : paymentMethod === 'split' ? 'สด+โอน' : 'เงินสด'))}""", 'footer split label')
rep("""order.paymentMethod === 'account' ? accountPayText(order, config) : order.paymentMethod === 'transfer' ? 'โอน' : 'เงินสด'})\\n⏰""",
    """order.paymentMethod === 'account' ? accountPayText(order, config) : order.paymentMethod === 'transfer' ? 'โอน' : order.paymentMethod === 'split' ? 'สด+โอน' : 'เงินสด'})\\n⏰""", 'LINE text split label')

# คำแปลพม่า (รอพนักงานพม่าตรวจ)
rep("""  'รวมในบิลค้างจ่าย': 'အကြွေးဘေလ်ထဲ ပေါင်းထည့်',
};""", """  'รวมในบิลค้างจ่าย': 'အကြွေးဘေလ်ထဲ ပေါင်းထည့်',
  // 🎨 ui2 (หน้าทดสอบ Otteri)
  'และอีก': 'နှင့် နောက်ထပ်',
  'แตะเพื่อเริ่มเครื่อง': 'စက်စရန် နှိပ်ပါ',
  'แตะดูว่าต้องทำอะไร': 'ဘာလုပ်ရမလဲ ကြည့်ရန် နှိပ်ပါ',
  'เข้างาน': 'အလုပ်ဝင်',
  'ออกงาน': 'အလုပ်ဆင်း',
  'ออกงานแล้ว': 'အလုပ်ဆင်းပြီး',
  'งานประจำวัน': 'နေ့စဉ်အလုပ်',
  'ติ๊กก่อนกลับบ้าน': 'အိမ်မပြန်ခင် အမှတ်ခြစ်ပါ',
  'งานจาก Line': 'LINE မှ အလုပ်',
  'ถ่าย': 'ရိုက်',
  'เลือกอัลบั้ม': 'အယ်လ်ဘမ်မှ ရွေး',
  'เริ่มเครื่อง (กดใน SOL)': 'စက်စတင် (SOL တွင်နှိပ်)',
  'เริ่มแล้ว': 'စပြီး',
  'ยังไม่เริ่ม': 'မစရသေး',
  'เรียงตามหน้าร้าน ซ้าย → ขวา (เหมือนใน SOL)': 'ဆိုင်ရှေ့အတိုင်း ဘယ် → ညာ (SOL ကဲ့သို့)',
  'ใน SOL เลือก Hot (น้ำร้อน)': 'SOL တွင် Hot (ရေပူ) ရွေးပါ',
};""", 'ui2: mm dict')

FEATURE_ONLY = '--feature-only' in sys.argv
if FEATURE_ONLY:
    open(OUT, 'w', encoding='utf-8').write(s)
    print('feature-only OK:', len(s), 'chars')
    sys.exit(0)
# ======================= ส่วนที่ 2: test wrapper =======================
rep("""<meta charset="UTF-8">
""", """<meta charset="UTF-8">
<script>
  // 🧪 หน้าทดสอบ: แยกข้อมูลในเครื่อง (localStorage) จากแอปตัวจริง — ทุกคีย์ขึ้นต้น TEST:
  window.TEST_MODE = true;
  (function () {
    var P = Storage.prototype, g = P.getItem, st = P.setItem, rm = P.removeItem;
    var k = function (x) { return 'TEST:' + x; };
    P.getItem = function (x) { return g.call(this, k(x)); };
    P.setItem = function (x, v) { return st.call(this, k(x), v); };
    P.removeItem = function (x) { return rm.call(this, k(x)); };
  })();
  document.addEventListener('DOMContentLoaded', function () {
    var b = document.createElement('div');
    b.textContent = '🧪 Otteri ทดสอบ · ข้อมูลแยกจากร้านจริง';
    b.setAttribute('style', 'position:fixed;top:0;left:50%;transform:translateX(-50%);z-index:99999;background:#F97316;color:#fff;font:700 11px sans-serif;padding:2px 10px;border-radius:0 0 10px 10px;pointer-events:none;white-space:nowrap');
    document.body.appendChild(b);
  });
</script>
""", 'test head')
rep("<title>PLP Laundromat - ร้านสะดวกซักผ้า</title>", "<title>🧪 Otteri ทดสอบ</title>", 'title')

rep_between("  firebase.initializeApp(firebaseConfig);\n  window.db = firebase.firestore();", "  })();\n</script>", lambda c: """  firebase.initializeApp(firebaseConfig);
  window.db = firebase.firestore();
  window.APP_VERSION = 'otteri-test-2026-10-31';
  // 🧪 ทุกคอลเลกชันขึ้นต้น test_ — ไม่แตะใบงาน/เงินของร้านจริง
  (function () {
    var d = window.db, orig = d.collection.bind(d);
    d.collection = function (p) { p = String(p); return orig(p.indexOf('test_') === 0 ? p : 'test_' + p); };
  })();
  // 🧪 ไม่เปิด offline cache (ไม่ยุ่งกับ cache ของแอปตัวจริงในเครื่องเดียวกัน)
  window.dbReady = Promise.resolve();
</script>""", 'test db')

rep("  setInterval(trySwReload, 5000);", "  // 🧪 หน้าทดสอบ: ไม่รีโหลดตามตัวอัปเดตของแอปจริง", 'no sw reload')
rep("  if ('serviceWorker' in navigator) {\n    window.addEventListener('load', () => {\n      navigator.serviceWorker.register('./sw.js')",
    "  if (false && 'serviceWorker' in navigator) { // 🧪 หน้าทดสอบไม่ลง Service Worker\n    window.addEventListener('load', () => {\n      navigator.serviceWorker.register('./sw.js')", 'no sw')
rep('<link rel="manifest" href="./manifest.json">\n', '', 'no manifest')
rep('href="./icon-', 'href="../icon-', 'icons', count=3)
rep("const GUIDE_BASE = 'guide/';", "const GUIDE_BASE = '../guide/';", 'guide base')
rep("const APP_SHARE_URL = 'https://phoneyjung.github.io/otteri-teddy-app/';",
    "const APP_SHARE_URL = 'https://phoneyjung.github.io/otteri-teddy-app/test/';", 'share url')
rep("  const [brand, setBrand] = useState(DEEP_START ? DEEP_START.b : null);",
    "  const [brand, setBrand] = useState(DEEP_START ? DEEP_START.b : 'otteri'); // 🧪 ล็อกร้าน Otteri", 'lock brand')
rep("onChangeBrand={() => { setDeep(null); setBrand(null); }}",
    "onChangeBrand={() => { setDeep(null); setBrand('otteri'); }}", 'lock brand change')

assert 'teddy-pulse.phoneyjung.workers.dev' in s
open(OUT, 'w', encoding='utf-8').write(s)
print('patched OK:', len(s), 'chars')
