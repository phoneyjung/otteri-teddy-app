#!/usr/bin/env python3
"""Otteri test build: index.html (v169) → test/index.html
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
rep("{view === 'ownerDashboard' && config.brand === 'teddy2' && <OwnerDashboardT2",
    "{isSol(config) && <SolPendingBar config={config} />}\n      {view === 'ownerDashboard' && config.t2Sys && <OwnerDashboardT2", 'gate owner T2')
rep("{view === 'ownerDashboard' && config.brand !== 'teddy2' && <OwnerDashboardView",
    "{view === 'ownerDashboard' && !config.t2Sys && <OwnerDashboardView", 'gate owner old')
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
    """  if (res.status === 'sol-pending') return { ok: null, text: `👉 ${mLabel} — ${tr(config, 'ไปกด Start ใน SOL แล้วกด ✅ ที่แถบล่าง')}${coinTxt ? ' · ' + coinTxt : ''}` };
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
  window.APP_VERSION = 'otteri-test-2026-10-28';
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
