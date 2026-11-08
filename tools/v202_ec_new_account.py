#!/usr/bin/env python3
"""v202 — Teddy 2 เปลี่ยนไปใช้ user EC ใหม่ + อ่านเว็บ EC น้อยลงอีก (คู่กับ Worker teddy-pulse v1.2)
ที่มา: เจ้าของ 8 พ.ย. 69 'teddy 2 ตอนนี้ เขามาแก้ให้ใหม่แล้ว แต่ต้องเปลี่ยน user … ประวัติเก่าหายไปเลย
        แล้วจากนี้ไปจะโดนบล็อคอีกมั้ย … อยากให้ไม่ผิดแบบเดิม'
ปัญหา
  1) user ใหม่ไม่มีประวัติก่อนวันเปลี่ยน → ถ้าเปิดดูวันเก่า แอปจะอ่าน EC ได้ค่าว่าง แล้ว 'เขียนทับ' ผลที่เคยอ่านเก็บไว้
     (pulseDayNotes/ec_<ร้าน>_<วัน>) + กระทบยอดวันเก่าขึ้นผิด
  2) หน้าแรกอ่านทั้ง 16 เครื่องทุก 30 นาที + เช็กเหรียญทุก 20 วิ 8 ครั้ง = เข้าเว็บ EC เยอะ
ทำอะไร
  - TEDDY2 pulse.ecSince = '2026-11-09' (วันแรกที่ใช้ user ใหม่เต็มวัน)
    วันก่อนหน้านั้น: ไม่เรียก Worker เลย · ใช้ผลที่เก็บไว้ (อ่านอย่างเดียว ไม่เขียนทับ) · ขึ้นป้ายว่าอยู่บัญชีเดิม
  - หน้าแรกอ่านอัตโนมัติ: ทุก 60 นาที เฉพาะ 09:00–21:00 · อ่านเฉพาะเครื่องที่มีงานจากแอปวันนั้น
    (หยอดเหรียญ = รวมเครื่องขนาดเดียวกัน) · มีผลที่แชร์อยู่แล้วอ่านเฉพาะเครื่องที่ขาด · ปุ่ม 🔄 = อ่านครบทุกเครื่อง
  - ผลอ่านแต่ละเครื่องมีเวลาที่อ่านจริง (fetchedAt / cachedAt จาก Worker) → กระทบยอดไม่ฟ้อง 'แอปสั่งแต่เครื่องไม่ได้รับ'
    เพราะข้อมูลแคชเก่ากว่าเวลายิง
  - เช็กเหรียญ: 2 ครั้ง (75 วิ / 3 นาที) แทน 8 ครั้ง
  - Worker v1.2 ตอบ 'ec-budget' แบบ readOnly = หยุดเฉพาะการอ่าน (ยิงพัลส์ยังใช้ได้ ไม่ขึ้นโหมดหยอดเหรียญแทน)
  - ⚙️ 🔌 ทดสอบ แสดงล็อกอินวันนี้ / ชั่วโมงนี้ / จำนวนเข้าเว็บ EC วันนี้
usage: python3 tools/v202_ec_new_account.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v201-2026-11-06';", "window.APP_VERSION = 'v202-2026-11-08';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v201';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v201';", "const CACHE_NAME = 'plp-laundry-v202';")

# ---------- MM ----------
rep("""  'ลบรายการ ✍️ นี้ (งานถูกลบแล้ว)': 'ဤ ✍️ မှတ်တမ်းကို ဖျက်ပါ (အလုပ်ဖျက်ပြီး)', // v201
""", """  'ลบรายการ ✍️ นี้ (งานถูกลบแล้ว)': 'ဤ ✍️ မှတ်တမ်းကို ဖျက်ပါ (အလုပ်ဖျက်ပြီး)', // v201
  'ประวัติเครื่องก่อนวันที่': 'ဤနေ့မတိုင်မီ စက်မှတ်တမ်း', // v202
  'อยู่ในบัญชี EC เดิม — แอปไม่อ่านซ้ำ': 'EC အကောင့်ဟောင်းတွင် ရှိသည် — app က ထပ်မဖတ်ပါ', // v202
  'ที่เห็นคือผลที่บันทึกไว้ตอนนั้น': 'မြင်ရသည်မှာ ထိုစဉ်က သိမ်းထားသော ရလဒ်', // v202
""", 'MM')

# ---------- config ----------
rep("""  pulse: { workerUrl: 'https://teddy-pulse.phoneyjung.workers.dev', maxPerShot: 12, stacks: 8, dryMinPer10: { 12: 7, 17: 6 }, washBusyMin: 45 }, // ⚡ ยิงพัลส์ผ่านระบบ EC (เปิด/ปิดที่ ตั้งค่า)""",
    """  pulse: { workerUrl: 'https://teddy-pulse.phoneyjung.workers.dev', maxPerShot: 12, stacks: 8, dryMinPer10: { 12: 7, 17: 6 }, washBusyMin: 45, ecSince: '2026-11-09' }, // ⚡ ยิงพัลส์ผ่านระบบ EC (เปิด/ปิดที่ ตั้งค่า) · v202 ecSince = วันแรกของ user EC ใหม่ (EC ระงับ user เดิม 3 พ.ย. · ให้ user ใหม่ 8 พ.ย.) — วันก่อนหน้าไม่อ่าน EC อีก""",
    'config')

# ---------- helpers ----------
rep("""const pulseSinceOf = (config) => (config && config.settings && config.settings.pulseSinceMs) || 0;""",
    """const pulseSinceOf = (config) => (config && config.settings && config.settings.pulseSinceMs) || 0;
// 🔁 v202 user EC ใหม่: วันก่อน ecSince ประวัติอยู่ในบัญชีเดิม → ไม่อ่าน Worker · ใช้ผลที่เก็บไว้อย่างเดียว
const ecSinceOf = (config) => (config && config.pulse && config.pulse.ecSince) || '';
const ecOldDay = (config, dateKey) => !!ecSinceOf(config) && String(dateKey) < ecSinceOf(config);""", 'helpers')

# ---------- fetchEcDay ----------
rep("""let PULSE_EC_PAUSE = null; // { until, message }
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
}""",
    """let PULSE_EC_PAUSE = null; // { until, message }
let PULSE_EC_READ_PAUSE = null; // v202 Worker v1.2 'ec-budget' readOnly = หยุดเฉพาะการอ่าน (ยิงพัลส์ยังได้)
const pulseEcPaused = () => !!(PULSE_EC_PAUSE && PULSE_EC_PAUSE.until > Date.now());
const pulseEcReadPause = () => (pulseEcPaused() ? PULSE_EC_PAUSE : PULSE_EC_READ_PAUSE && PULSE_EC_READ_PAUSE.until > Date.now() ? PULSE_EC_READ_PAUSE : null);
const pulseEcOldResult = (config) => ({ at: Date.now(), byMachine: {}, errors: [], oldAccount: true });
async function fetchEcDay(config, dateKey, machineIds, onProgress, opts) {
  if (isSol(config)) return { byMachine: {}, errors: [], at: Date.now() };
  if (ecOldDay(config, dateKey)) return pulseEcOldResult(config); // 🔁 v202 วันเก่า = บัญชี EC เดิม ไม่เรียก Worker
  const rp = pulseEcReadPause();
  if (rp) return { at: Date.now(), byMachine: {}, errors: [rp.message], paused: rp };
  const ms = pulseMachines(config).filter(m => !machineIds || machineIds.includes(m.id));
  const wantFresh = opts && opts.fresh !== undefined ? opts.fresh : !!(machineIds && machineIds.length <= 3);
  const fresh = wantFresh ? '&fresh=1' : ''; // เช็กเครื่องเดียว (ยืนยันยิง/เหรียญ) = ขอข้อมูลใหม่ · อ่านอัตโนมัติ = ใช้แคช Worker ได้
  const byMachine = {}, errors = [];
  let i = 0, done = 0, stop = null;
  const run = async () => {
    while (i < ms.length && !stop) {
      const m = ms[i++];
      try {
        const r = await fetch(`${config.pulse.workerUrl}/day?shop=${config.brand}&machine=${m.id}&date=${dateKey}${fresh}`);
        const j = await r.json();
        if (j.ok) byMachine[m.id] = { ...j, fetchedAt: j.cachedAt || Date.now() }; // v202 เวลาที่อ่านจริง (แคช Worker = เวลาตอนแคช)
        else if (j.blocked) {
          const p = { until: j.retryAt || Date.now() + 30 * 60000, message: j.message || j.error || '⏸️ เว็บ EC พักชั่วคราว' };
          if (j.readOnly) PULSE_EC_READ_PAUSE = p; else PULSE_EC_PAUSE = p;
          stop = p;
        }
        else errors.push(`${m.label}: ${j.error || 'error'}`);
      } catch (e) { errors.push(`${m.label}: ${e && e.message ? e.message : 'network'}`); }
      done++;
      if (onProgress) onProgress(done, ms.length);
    }
  };
  await Promise.all([run(), run()]);
  if (stop) return { at: Date.now(), byMachine, errors: [stop.message, ...errors], paused: stop };
  return { at: Date.now(), byMachine, errors };
}

// v202 อ่านอัตโนมัติเฉพาะเครื่องที่มีงานจากแอปวันนั้น (ยิงพัลส์/หยอดเหรียญ) — หยอดเหรียญรวมเครื่องขนาดเดียวกัน (ลงผิดเบอร์ได้ v174)
function ecActiveIds(config, logs, dateKey) {
  const ms = pulseMachines(config);
  const ids = new Set();
  (logs || []).filter(l => l.brand === config.brand && l.dateKey === dateKey && (pulseLive(l) || pulseRefunded(l)) && !pulseIsManual(l)).forEach(l => {
    const me = ms.find(m => m.id === l.machine);
    if (!me) return;
    ids.add(me.id);
    if (pulseIsCoin(l)) ms.filter(m => m.kind === me.kind && m.kg === me.kg).forEach(m => ids.add(m.id));
  });
  return ms.map(m => m.id).filter(id => ids.has(id));
}
const ecAutoHour = () => { const h = new Date().getHours(); return h >= 9 && h < 21; }; // v202 อ่านอัตโนมัติเฉพาะช่วงแม่บ้านอยู่ร้าน""", 'fetchEcDay')

# ---------- shared snapshot ----------
rep("""const ecShareFresh = (d, dateKey) => !!(d && d.at && Date.now() - d.at < (dateKey === dateKeyOf(new Date()) ? PULSE_EC_SHARE_MS : 6 * 3600000));
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
  if (!window.db || !res) return;""",
    """const ecShareFresh = (d, dateKey) => !!(d && d.at && Date.now() - d.at < (dateKey === dateKeyOf(new Date()) ? PULSE_EC_SHARE_MS : 6 * 3600000));
const ecFreshAt = (t, dateKey) => !!(t && Date.now() - t < (dateKey === dateKeyOf(new Date()) ? PULSE_EC_SHARE_MS : 6 * 3600000));
// v202 ผลที่แชร์ → บอกด้วยว่าเครื่องไหนยังขาด/เก่า (want = เครื่องที่ต้องการ · null = ทุกเครื่อง)
function ecSharePack(config, d, dateKey, want) {
  const bm = {};
  Object.entries(d.byMachine || {}).forEach(([k, v]) => { bm[k] = v && v.fetchedAt ? v : { ...v, fetchedAt: d.at }; });
  const need = want || pulseMachines(config).map(m => m.id);
  return { at: d.at, byMachine: bm, errors: d.errors || [], shared: true, missing: need.filter(id => !bm[id] || !ecFreshAt(bm[id].fetchedAt, dateKey)) };
}
async function loadEcShared(config, dateKey, force, want) {
  if (!window.db) return null;
  try {
    const ref = ecShareRef(config, dateKey);
    let s = await ref.get();
    let d = s.exists ? s.data() : null;
    if (!force && d && d.byMachine) { const pk = ecSharePack(config, d, dateKey, want); if (!pk.missing.length) return pk; }
    if (d && d.fetchingAt && Date.now() - d.fetchingAt < 90000 && !(d.at >= d.fetchingAt)) { // มือถืออื่นกำลังอ่านอยู่ → รอผล
      await new Promise(r => setTimeout(r, 25000));
      s = await ref.get(); d = s.exists ? s.data() : null;
      if (d && d.byMachine) { const pk = ecSharePack(config, d, dateKey, want); if (!pk.missing.length) return pk; }
    }
    await ref.set({ brand: config.brand, dateKey, kind: 'ecShared', fetchingAt: Date.now() }, { merge: true });
    if (!force && d && d.byMachine) return ecSharePack(config, d, dateKey, want); // มีบางเครื่องแล้ว → อ่านเฉพาะที่ขาด
  } catch (e) { console.error('ecShared load error:', e); }
  return null;
}
// v202 วันก่อน ecSince: ใช้ผลที่เคยเก็บไว้ (อ่านอย่างเดียว ไม่เขียนอะไรเลย)
async function loadEcSnapshot(config, dateKey) {
  const old = pulseEcOldResult(config);
  if (!window.db) return old;
  try {
    const s = await ecShareRef(config, dateKey).get();
    const d = s.exists ? s.data() : null;
    if (d && d.byMachine && Object.keys(d.byMachine).length) return { ...ecSharePack(config, d, dateKey, null), oldAccount: true, missing: [] };
  } catch (e) { console.error('ecSnapshot load error:', e); }
  return old;
}
async function saveEcShared(config, dateKey, res) {
  if (!window.db || !res) return;
  if (ecOldDay(config, dateKey) || res.oldAccount) return; // 🔁 v202 ไม่เขียนทับผลของบัญชีเดิม""", 'shared')

# ---------- recon: เวลาอ่านรายเครื่อง ----------
rep("""      if (!e) { machineRows.push({ id: m.id, label: m.label, appBaht: appBaht + sumBaht(refList), ecBaht: null, ok: null, appCoin, ecCoin: null }); return; }""",
    """      if (!e) { machineRows.push({ id: m.id, label: m.label, appBaht: appBaht + sumBaht(refList), ecBaht: null, ok: null, appCoin, ecCoin: null }); return; }
      const eAt = e.fetchedAt || ec.at; // v202 เวลาที่อ่านเครื่องนี้จริง (แคช/ผลที่แชร์อาจเก่ากว่า ec.at)""", 'recon eAt')
rep("""        if (!matchEc(l) && ec.at - (l.createdAt || 0) > 60000) missing.push(l); // เพิ่งยิงไม่ถึงนาที ยังไม่ขึ้นประวัติ — ข้ามไปก่อน""",
    """        if (!matchEc(l) && eAt - (l.createdAt || 0) > 60000) missing.push(l); // เพิ่งยิงไม่ถึงนาที (นับจากเวลาที่อ่าน) ยังไม่ขึ้นประวัติ — ข้ามไปก่อน""", 'recon missing')
rep("""      machineRows.push({ id: m.id, label: m.label, appBaht, ecBaht, ok: !outside.length && !missing.length, appCoin, ecCoin: e.coinBaht || 0 });""",
    """      machineRows.push({ id: m.id, label: m.label, appBaht, ecBaht, ok: !outside.length && !missing.length, appCoin, ecCoin: e.coinBaht || 0, at: eAt });""", 'recon row at')
rep("""      cg.app += sumBaht(dayCoins.filter(l => l.machine === m.id && ec.at - (l.createdAt || 0) > 120000));""",
    """      cg.app += sumBaht(dayCoins.filter(l => l.machine === m.id && eAt - (l.createdAt || 0) > 120000));""", 'recon coin at')
rep("""    machineRows, ecAt: ec ? ec.at : null, ecErrors: ec ? ec.errors : null, ecPaused: ec && ec.paused ? ec.paused : null,""",
    """    machineRows, ecAt: ec ? ec.at : null, ecErrors: ec ? ec.errors : null, ecPaused: ec && ec.paused ? ec.paused : null,
    ecOld: !!(ec && ec.oldAccount), ecOldSaved: !!(ec && ec.oldAccount && ec.byMachine && Object.keys(ec.byMachine).length), // 🔁 v202""", 'recon flags')

# ---------- usePulseRecon: refresh ----------
rep("""  const refreshEc = (force) => { // force === true = ปุ่ม 🔄 เช็กกับเครื่องอีกครั้ง (อ่านใหม่ ไม่ใช้ผลที่แชร์)
    if (!config.pulse || isSol(config)) return Promise.resolve(null);
    if (PULSE_EC_INFLIGHT[cacheKey]) return PULSE_EC_INFLIGHT[cacheKey];
    const prog = (text) => window.dispatchEvent(new CustomEvent('pulse-ec-progress', { detail: { key: cacheKey, text } }));
    prog('0/' + pulseMachines(config).length);
    const p = (pulseEcPaused() ? Promise.resolve(null) : loadEcShared(config, dateKey, force === true))
      .then(sh => sh || fetchEcDay(config, dateKey, null, (n, t) => prog(n + '/' + t)).then(res => { saveEcShared(config, dateKey, res); return res; }))
      .then(res => { PULSE_EC_CACHE[cacheKey] = res; window.dispatchEvent(new CustomEvent('pulse-ec', { detail: cacheKey })); return res; })""",
    """  const logsRef = useRef(logs); // v202 interval ของหน้าแรกเรียก refreshEc ตัวเก่า → อ่าน logs ล่าสุดจาก ref
  logsRef.current = logs;
  const refreshEc = (force) => { // force === true = ปุ่ม 🔄 เช็กกับเครื่องอีกครั้ง (อ่านครบทุกเครื่อง ไม่ใช้ผลที่แชร์)
    if (!config.pulse || isSol(config)) return Promise.resolve(null);
    if (PULSE_EC_INFLIGHT[cacheKey]) return PULSE_EC_INFLIGHT[cacheKey];
    const prog = (text) => window.dispatchEvent(new CustomEvent('pulse-ec-progress', { detail: { key: cacheKey, text } }));
    const old = ecOldDay(config, dateKey);
    const want = old || force === true ? null : ecActiveIds(config, logsRef.current, dateKey); // v202 อัตโนมัติ = เฉพาะเครื่องที่มีงานจากแอป
    prog('0/' + (want ? want.length : pulseMachines(config).length));
    const read = async () => {
      if (old) return loadEcSnapshot(config, dateKey); // 🔁 วันเก่า: ผลที่เก็บไว้เท่านั้น
      if (pulseEcReadPause()) return null;
      const sh = await loadEcShared(config, dateKey, force === true, want);
      if (sh && !sh.missing.length) return sh;
      if (want && !want.length) return sh; // ยังไม่มีงานจากแอปวันนี้ → ไม่ต้องอ่าน EC
      const ids = sh ? sh.missing : want; // null = ทุกเครื่อง
      const res = await fetchEcDay(config, dateKey, ids, (n, t) => prog(n + '/' + t), { fresh: false });
      const merged = sh ? { ...res, byMachine: { ...sh.byMachine, ...res.byMachine } } : res;
      await saveEcShared(config, dateKey, merged);
      return merged;
    };
    const p = read()
      .then(res => { PULSE_EC_CACHE[cacheKey] = res; window.dispatchEvent(new CustomEvent('pulse-ec', { detail: cacheKey })); return res; })""", 'refreshEc')

rep("""      logs.filter(l => l.machine === r.id && l.dateKey === dateKey && ['sent', 'unknown', 'sending', 'forced'].includes(l.status) && (l.createdAt || 0) <= ec.at - 60000)""",
    """      logs.filter(l => l.machine === r.id && l.dateKey === dateKey && ['sent', 'unknown', 'sending', 'forced'].includes(l.status) && (l.createdAt || 0) <= (r.at || ec.at) - 60000)""", 'confirm at')

# ---------- หน้าแรก: อ่านทุก 60 นาที เฉพาะ 09–21 ----------
rep("""  // เช็กกับเครื่องตอนเปิดหน้า (ถ้าเก่ากว่า 10 นาที) และทุก 15 นาที
  useEffect(() => {
    const c = PULSE_EC_CACHE[config.brand + '|' + todayKey];
    if (!c || Date.now() - c.at > 10 * 60000) refreshEc();
    const t = setInterval(() => { if (!document.hidden) refreshEc(); }, 30 * 60000); // v191 เดิม 15 นาที
    return () => clearInterval(t);
  }, [config.brand, todayKey]);""",
    """  // เช็กกับเครื่องตอนเปิดหน้า (ถ้าเก่ากว่า 30 นาที) และทุก 60 นาที เฉพาะ 09:00–21:00 · v202 (v191 ทุก 30 นาที · เดิม 15)
  // อ่านเฉพาะเครื่องที่มีงานจากแอปวันนี้ — ปุ่ม 🔄 ในหน้ารายละเอียด = อ่านครบทุกเครื่อง
  useEffect(() => {
    const c = PULSE_EC_CACHE[config.brand + '|' + todayKey];
    if (!c || Date.now() - c.at > 30 * 60000) refreshEc();
    const t = setInterval(() => { if (!document.hidden && ecAutoHour()) refreshEc(); }, 60 * 60000);
    return () => clearInterval(t);
  }, [config.brand, todayKey]);""", 'home interval')

# ---------- เช็กเหรียญ 2 ครั้ง ----------
rep("""    if (pulseEcPaused()) return; // v192 Worker แจ้งพัก (EC ใช้ไม่ได้) → ไม่เช็กต่อ
    n++;
    const final = n >= 8;
    try { const r = await checkCoinLog(config, log, final); if (r.ok && r.seen) return; } catch (e) { console.error('coin check error:', e); }
    if (!final) setTimeout(tick, 20000);
  };
  setTimeout(tick, 15000);""",
    """    if (pulseEcReadPause()) return; // v192 Worker แจ้งพัก (EC ใช้ไม่ได้) → ไม่เช็กต่อ · v202 รวมพักอ่าน
    n++;
    const final = n >= 2; // v202 เช็ก 2 ครั้ง (75 วิ / 3 นาที) — เดิมทุก 20 วิ 8 ครั้ง
    try { const r = await checkCoinLog(config, log, final); if (r.ok && r.seen) return; } catch (e) { console.error('coin check error:', e); }
    if (!final) setTimeout(tick, 105000);
  };
  setTimeout(tick, 75000);""", 'coin watch')

# ---------- UI: ป้ายวันเก่า ----------
rep("""          {recon.ecPaused && (
            <p className="text-xs font-bold text-slate-700 bg-slate-100 border border-slate-300 rounded-xl px-3 py-2" data-ec-paused>{recon.ecPaused.message}</p>
          )}""",
    """          {recon.ecOld && (
            <p className="text-xs font-bold text-slate-700 bg-slate-100 border border-slate-300 rounded-xl px-3 py-2" data-ec-old>🔁 {tr(config, 'ประวัติเครื่องก่อนวันที่')} {new Date(ecSinceOf(config) + 'T00:00:00').toLocaleDateString('th-TH', { day: 'numeric', month: 'short' })} {tr(config, 'อยู่ในบัญชี EC เดิม — แอปไม่อ่านซ้ำ')}{recon.ecOldSaved ? ' · ' + tr(config, 'ที่เห็นคือผลที่บันทึกไว้ตอนนั้น') : ''}</p>
          )}
          {recon.ecPaused && (
            <p className="text-xs font-bold text-slate-700 bg-slate-100 border border-slate-300 rounded-xl px-3 py-2" data-ec-paused>{recon.ecPaused.message}</p>
          )}""", 'ui old')

# ---------- ⚙️ ทดสอบ: ตัวนับ v1.2 ----------
rep("""      try { const st = await (await fetch(config.pulse.workerUrl + '/status')).json(); if (st && st.ok && st.version) extra = ` · ล็อกอิน ${st.loginsLastHour}/${st.maxLoginsPerHour} ครั้งใน 1 ชม.${st.kv ? '' : ' · ยังไม่ได้ผูก KV'}${st.paused ? ' · ⏸️ พักถึง ' + new Date(st.pausedUntil).toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit' }) : ''}`; } catch (e) {}""",
    """      try {
        const st = await (await fetch(config.pulse.workerUrl + '/status')).json();
        if (st && st.ok && st.version) extra = ` · ล็อกอิน ${st.loginsLastHour}/${st.maxLoginsPerHour} ครั้งใน 1 ชม.`
          + (st.loginsToday != null ? ` · วันนี้ ${st.loginsToday}/${st.maxLoginsPerDay} · เข้าเว็บ EC วันนี้ ${st.reqToday}/${st.maxReqPerDay}` : '') // v202 Worker v1.2
          + `${st.kv ? '' : ' · ยังไม่ได้ผูก KV'}${st.paused ? ' · ⏸️ พักถึง ' + new Date(st.pausedUntil).toLocaleString('th-TH', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) : ''}`;
      } catch (e) {}""", 'test button')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v202 patched')
