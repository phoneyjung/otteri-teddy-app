#!/usr/bin/env python3
"""v191 — Teddy 2: ลดการเรียกเว็บ EC (บัญชี EC ถูกระงับชั่วคราวเพราะล็อกอินถี่ 3 พ.ย. 69)
ที่มา: เจ้าของส่ง log จากทีม EC + หน้า qrcode.ec.in.th/login 'Account temporarily unavailable'
ทำอะไร (คู่กับ Worker teddy-pulse v1.1 — แอปนี้ใช้กับ Worker v1.0 ได้ด้วย)
  - อ่านประวัติเครื่อง 16 เครื่อง: ทีละ 2 (เดิม 4)
  - ทุกมือถือใช้ผลอ่าน EC ชุดเดียวกัน: เก็บไว้ใน pulseDayNotes/ec_<ร้าน>_<วัน> 10 นาที
    (เครื่องแรกที่อ่าน = เขียน · เครื่องอื่นใช้ต่อ · มีเครื่องกำลังอ่านอยู่ = รอผลเครื่องนั้น)
  - หน้าแรกแม่บ้าน: เช็กกับเครื่องอัตโนมัติทุก 30 นาที (เดิม 15) และเฉพาะตอนเปิดแอปอยู่
  - ปุ่ม '🔄 เช็กกับเครื่องอีกครั้ง' = อ่านใหม่จริง (ไม่ใช้ผลที่แชร์)
  - Worker แจ้งพัก (503 ec-blocked) → หยุดอ่านทันที ไม่ยิงคำขอต่อจนถึงเวลาที่แจ้ง · การ์ดกระทบยอดขึ้น '⏸️ …'
  - เช็กเครื่องเดียว (ยืนยันยิง/เหรียญ) ส่ง &fresh=1 (Worker v1.1 มีแคช 3 นาที)
  - ⚙️ ทดสอบการเชื่อมต่อ: บอกจำนวนล็อกอินชั่วโมงนี้ / ผูก KV แล้วหรือยัง (Worker v1.1 /status)
usage: python3 tools/v191_ec_gentle.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v190-2026-11-02';", "window.APP_VERSION = 'v191-2026-11-03';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v190';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v190';", "const CACHE_NAME = 'plp-laundry-v191';")

# ---------- fetchEcDay: ทีละ 2 · หยุดเมื่อ Worker พัก · fresh สำหรับเช็กเครื่องเดียว ----------
rep("""// อ่านประวัติเครื่องของวันจาก EC (ผ่าน Worker) — ทีละ 4 เครื่องพร้อมกัน
async function fetchEcDay(config, dateKey, machineIds, onProgress) {
  if (isSol(config)) return { byMachine: {}, errors: [], at: Date.now() };
  const ms = pulseMachines(config).filter(m => !machineIds || machineIds.includes(m.id));
  const byMachine = {}, errors = [];
  let i = 0, done = 0;
  const run = async () => {
    while (i < ms.length) {
      const m = ms[i++];
      try {
        const r = await fetch(`${config.pulse.workerUrl}/day?shop=${config.brand}&machine=${m.id}&date=${dateKey}`);
        const j = await r.json();
        if (j.ok) byMachine[m.id] = j; else errors.push(`${m.label}: ${j.error || 'error'}`);
      } catch (e) { errors.push(`${m.label}: ${e && e.message ? e.message : 'network'}`); }
      done++;
      if (onProgress) onProgress(done, ms.length);
    }
  };
  await Promise.all([run(), run(), run(), run()]);
  return { at: Date.now(), byMachine, errors };
}""",
    """// อ่านประวัติเครื่องของวันจาก EC (ผ่าน Worker) — v191: ทีละ 2 เครื่อง (เดิม 4) · EC ระงับบัญชีชั่วคราว 3 พ.ย. 69 เพราะล็อกอินถี่
// Worker v1.1 แจ้งพัก (503 · blocked) → หยุดทันที และไม่เรียกอีกจนถึงเวลาที่ Worker บอก
let PULSE_EC_PAUSE = null; // { until, message }
const pulseEcPaused = () => !!(PULSE_EC_PAUSE && PULSE_EC_PAUSE.until > Date.now());
async function fetchEcDay(config, dateKey, machineIds, onProgress) {
  if (isSol(config)) return { byMachine: {}, errors: [], at: Date.now() };
  if (pulseEcPaused()) return { at: Date.now(), byMachine: {}, errors: [PULSE_EC_PAUSE.message], paused: PULSE_EC_PAUSE };
  const ms = pulseMachines(config).filter(m => !machineIds || machineIds.includes(m.id));
  const fresh = machineIds && machineIds.length <= 3 ? '&fresh=1' : ''; // เช็กเครื่องเดียว (ยืนยันยิง/เหรียญ) = ขอข้อมูลใหม่
  const byMachine = {}, errors = [];
  let i = 0, done = 0, stop = false;
  const run = async () => {
    while (i < ms.length && !stop) {
      const m = ms[i++];
      try {
        const r = await fetch(`${config.pulse.workerUrl}/day?shop=${config.brand}&machine=${m.id}&date=${dateKey}${fresh}`);
        const j = await r.json();
        if (j.ok) byMachine[m.id] = j;
        else if (j.blocked) { PULSE_EC_PAUSE = { until: j.retryAt || Date.now() + 30 * 60000, message: j.message || j.error || '⏸️ เว็บ EC พักชั่วคราว' }; stop = true; }
        else errors.push(`${m.label}: ${j.error || 'error'}`);
      } catch (e) { errors.push(`${m.label}: ${e && e.message ? e.message : 'network'}`); }
      done++;
      if (onProgress) onProgress(done, ms.length);
    }
  };
  await Promise.all([run(), run()]);
  if (stop) return { at: Date.now(), byMachine, errors: [PULSE_EC_PAUSE.message, ...errors], paused: PULSE_EC_PAUSE };
  return { at: Date.now(), byMachine, errors };
}

// 🤝 v191 ผลอ่าน EC ทั้งร้านใช้ร่วมกันทุกมือถือ (pulseDayNotes/ec_<ร้าน>_<วัน>) — เครื่องเดียวอ่าน เครื่องอื่นใช้ต่อ
const PULSE_EC_SHARE_MS = 10 * 60000;
const ecShareRef = (config, dateKey) => window.db.collection('pulseDayNotes').doc('ec_' + config.brand + '_' + dateKey);
const ecShareFresh = (d, dateKey) => !!(d && d.at && Date.now() - d.at < (dateKey === dateKeyOf(new Date()) ? PULSE_EC_SHARE_MS : 6 * 3600000));
async function loadEcShared(config, dateKey, force) {
  if (!window.db) return null;
  try {
    const ref = ecShareRef(config, dateKey);
    let s = await ref.get();
    let d = s.exists ? s.data() : null;
    if (!force && ecShareFresh(d, dateKey)) return { at: d.at, byMachine: d.byMachine || {}, errors: d.errors || [], shared: true };
    if (d && d.fetchingAt && Date.now() - d.fetchingAt < 90000 && !(d.at >= d.fetchingAt)) { // มือถืออื่นกำลังอ่านอยู่ → รอผล
      await new Promise(r => setTimeout(r, 25000));
      s = await ref.get(); d = s.exists ? s.data() : null;
      if (ecShareFresh(d, dateKey)) return { at: d.at, byMachine: d.byMachine || {}, errors: d.errors || [], shared: true };
    }
    await ref.set({ brand: config.brand, dateKey, kind: 'ecShared', fetchingAt: Date.now() }, { merge: true });
  } catch (e) { console.error('ecShared load error:', e); }
  return null;
}
async function saveEcShared(config, dateKey, res) {
  if (!window.db || !res) return;
  try {
    if (res.paused || !Object.keys(res.byMachine || {}).length) { await ecShareRef(config, dateKey).set({ brand: config.brand, fetchingAt: 0 }, { merge: true }); return; }
    await ecShareRef(config, dateKey).set({ brand: config.brand, dateKey, kind: 'ecShared', at: res.at, byMachine: res.byMachine, errors: res.errors || [], fetchingAt: 0 });
  } catch (e) { console.error('ecShared save error:', e); }
}""", 'fetchEcDay')

# ---------- refreshEc: ใช้ผลที่แชร์ก่อน (ยกเว้นกดปุ่มเช็กเอง) ----------
rep("""  const refreshEc = () => {
    if (!config.pulse || isSol(config)) return Promise.resolve(null);
    if (PULSE_EC_INFLIGHT[cacheKey]) return PULSE_EC_INFLIGHT[cacheKey];
    const prog = (text) => window.dispatchEvent(new CustomEvent('pulse-ec-progress', { detail: { key: cacheKey, text } }));
    prog('0/' + pulseMachines(config).length);
    const p = fetchEcDay(config, dateKey, null, (n, t) => prog(n + '/' + t))""",
    """  const refreshEc = (force) => { // force === true = ปุ่ม 🔄 เช็กกับเครื่องอีกครั้ง (อ่านใหม่ ไม่ใช้ผลที่แชร์)
    if (!config.pulse || isSol(config)) return Promise.resolve(null);
    if (PULSE_EC_INFLIGHT[cacheKey]) return PULSE_EC_INFLIGHT[cacheKey];
    const prog = (text) => window.dispatchEvent(new CustomEvent('pulse-ec-progress', { detail: { key: cacheKey, text } }));
    prog('0/' + pulseMachines(config).length);
    const p = (pulseEcPaused() ? Promise.resolve(null) : loadEcShared(config, dateKey, force === true))
      .then(sh => sh || fetchEcDay(config, dateKey, null, (n, t) => prog(n + '/' + t)).then(res => { saveEcShared(config, dateKey, res); return res; }))""", 'refreshEc shared')
rep("""          {!isSol(config) && <button onClick={refreshEc} disabled={!!ecBusy}""",
    """          {!isSol(config) && <button onClick={() => refreshEc(true)} disabled={!!ecBusy}""", 'manual refresh = force')

# ---------- หน้าแรกแม่บ้าน: ทุก 30 นาที เฉพาะตอนเปิดแอปอยู่ ----------
rep("""    const t = setInterval(() => refreshEc(), 15 * 60000);""",
    """    const t = setInterval(() => { if (!document.hidden) refreshEc(); }, 30 * 60000); // v191 เดิม 15 นาที""", 'interval 30')

# ---------- การ์ดกระทบยอด: แจ้งพัก ----------
rep("""    machineRows, ecAt: ec ? ec.at : null, ecErrors: ec ? ec.errors : null,""",
    """    machineRows, ecAt: ec ? ec.at : null, ecErrors: ec ? ec.errors : null, ecPaused: ec && ec.paused ? ec.paused : null,""", 'recon ecPaused')
rep("""          {recon.ecErrors && recon.ecErrors.length > 0 && (
            <p className="text-xs text-amber-700 bg-amber-50 border border-amber-200 rounded-xl px-3 py-2">{tr(config, 'เช็กกับเครื่องไม่ได้')}""",
    """          {recon.ecPaused && (
            <p className="text-xs font-bold text-slate-700 bg-slate-100 border border-slate-300 rounded-xl px-3 py-2" data-ec-paused>{recon.ecPaused.message}</p>
          )}
          {!recon.ecPaused && recon.ecErrors && recon.ecErrors.length > 0 && (
            <p className="text-xs text-amber-700 bg-amber-50 border border-amber-200 rounded-xl px-3 py-2">{tr(config, 'เช็กกับเครื่องไม่ได้')}""", 'paused banner')

# ---------- ⚙️ ทดสอบการเชื่อมต่อ: บอกโควตาล็อกอิน ----------
rep("""      const r = await fetch(config.pulse.workerUrl + '/ping');
      const j = await r.json();
      setPing(j.ok ? `✅ เชื่อมต่อได้ · ล็อกอิน EC ผ่าน (${j.version})` : `❌ ${j.error || 'ไม่ผ่าน'}`);""",
    """      const r = await fetch(config.pulse.workerUrl + '/ping');
      const j = await r.json();
      let extra = ''; // v191 Worker v1.1: จำนวนล็อกอินชั่วโมงนี้ / ผูก KV แล้วหรือยัง
      try { const st = await (await fetch(config.pulse.workerUrl + '/status')).json(); if (st && st.ok && st.version) extra = ` · ล็อกอิน ${st.loginsLastHour}/${st.maxLoginsPerHour} ครั้งใน 1 ชม.${st.kv ? '' : ' · ยังไม่ได้ผูก KV'}${st.paused ? ' · ⏸️ พักถึง ' + new Date(st.pausedUntil).toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit' }) : ''}`; } catch (e) {}
      setPing((j.ok ? `✅ เชื่อมต่อได้ · ใช้ session EC ได้ (${j.version})` : `❌ ${j.error || 'ไม่ผ่าน'}`) + extra);""", 'ping status')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v191 applied')
