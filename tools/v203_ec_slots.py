#!/usr/bin/env python3
"""v203 — Teddy 2 ใช้เว็บ EC 'ปริมาณเท่าคนใช้' (คู่กับ Worker teddy-pulse v1.3)
ที่มา: เจ้าของ 8 พ.ย. 69 'ส่วนเรื่องแอปทำให้เหมือนว่าคนเข้าไปใช้งานเลย ไม่ login ซ้ำเยอะๆ แล้วไม่เข้าไปเยอะมาก'
ทำอะไร
  - อ่านประวัติเครื่องอัตโนมัติวันละ 2 รอบ (pulse.ecSlots 13:00 / 20:00) แทนทุกชั่วโมง
    มือถือเครื่องแรกที่เปิดหลังถึงรอบอ่านให้ เครื่องอื่นใช้ผลที่แชร์ (pulseDayNotes/ec_*) · ก่อนรอบแรก = ไม่อ่าน
    วันก่อน (ยังไม่ใช่บัญชีเดิม) = อ่านครั้งเดียวหลังจบวัน · เปิดหน้ากระทบยอดซ้ำ = ไม่อ่านซ้ำ
  - ปุ่ม 🔄 เช็กกับเครื่อง: ใช้ผลที่อ่านภายใน 15 นาทีได้ (ไม่อ่านซ้ำ) · อ่านเฉพาะเครื่องที่มีงานจากแอป
  - หยอดเหรียญ: ไม่เช็กทันทีทุกใบแล้ว → เช็กตอนรอบอ่าน (ตั้ง coinSeen จากผลรอบ) · ป้าย '🕐 รอเช็กกับเครื่องรอบถัดไป'
  - ⚙️ ทดสอบ แสดงเวลาล็อกอินล่าสุด (Worker v1.3)
  - ยิงพัลส์ยังเช็กผลทันทีที่ Worker เหมือนเดิม
usage: python3 tools/v203_ec_slots.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v202-2026-11-08';", "window.APP_VERSION = 'v203-2026-11-08';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v202';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v202';", "const CACHE_NAME = 'plp-laundry-v203';")

# ---------- MM ----------
rep("""  'ที่เห็นคือผลที่บันทึกไว้ตอนนั้น': 'မြင်ရသည်မှာ ထိုစဉ်က သိမ်းထားသော ရလဒ်', // v202
""", """  'ที่เห็นคือผลที่บันทึกไว้ตอนนั้น': 'မြင်ရသည်မှာ ထိုစဉ်က သိမ်းထားသော ရလဒ်', // v202
  'รอเช็กกับเครื่องรอบถัดไป': 'နောက်တစ်ကြိမ် စက်နှင့် စစ်ချိန်ကို စောင့်ပါ', // v203
  'เช็กกับเครื่องอัตโนมัติ 13:00 และ 20:00': 'စက်နှင့် အလိုအလျောက် စစ်ချိန် 13:00 နှင့် 20:00', // v203
""", 'MM')

# ---------- config ----------
rep("washBusyMin: 45, ecSince: '2026-11-09' },", "washBusyMin: 45, ecSince: '2026-11-09', ecSlots: [13, 20] },", 'config slots')

# ---------- shared pack: freshness ตามรอบ ----------
rep("""function ecSharePack(config, d, dateKey, want) {
  const bm = {};
  Object.entries(d.byMachine || {}).forEach(([k, v]) => { bm[k] = v && v.fetchedAt ? v : { ...v, fetchedAt: d.at }; });
  const need = want || pulseMachines(config).map(m => m.id);
  return { at: d.at, byMachine: bm, errors: d.errors || [], shared: true, missing: need.filter(id => !bm[id] || !ecFreshAt(bm[id].fetchedAt, dateKey)) };
}
async function loadEcShared(config, dateKey, force, want) {""",
    """function ecSharePack(config, d, dateKey, want, since) {
  const bm = {};
  Object.entries(d.byMachine || {}).forEach(([k, v]) => { bm[k] = v && v.fetchedAt ? v : { ...v, fetchedAt: d.at }; });
  const need = want || pulseMachines(config).map(m => m.id);
  const fresh = (t) => (since != null ? !!(t && t >= since) : ecFreshAt(t, dateKey)); // v203 since = อ่านหลังเวลานี้ถึงนับว่าใหม่ (รอบอ่าน)
  return { at: d.at, byMachine: bm, errors: d.errors || [], shared: true, missing: need.filter(id => !bm[id] || !fresh(bm[id].fetchedAt)) };
}
async function loadEcShared(config, dateKey, force, want, since) {""", 'pack')
rep("ecSharePack(config, d, dateKey, want)", "ecSharePack(config, d, dateKey, want, since)", 'pack calls', 3)

rep("""// v202 วันก่อน ecSince: ใช้ผลที่เคยเก็บไว้ (อ่านอย่างเดียว ไม่เขียนอะไรเลย)""",
    """// v203 ดูผลที่แชร์ไว้เฉยๆ (ไม่เขียน ไม่เรียก Worker) — ยังไม่ถึงรอบอ่าน / พักอ่าน / ยังไม่มีงานจากแอป
async function peekEcShared(config, dateKey, want) {
  if (!window.db) return null;
  try {
    const s = await ecShareRef(config, dateKey).get();
    const d = s.exists ? s.data() : null;
    if (d && d.byMachine && Object.keys(d.byMachine).length) return ecSharePack(config, d, dateKey, want, null);
  } catch (e) { console.error('ecShared peek error:', e); }
  return null;
}
// v203 รอบอ่าน EC: วันนี้ = เวลาเริ่มรอบล่าสุดที่ผ่านมาแล้ว (null = ยังไม่ถึงรอบแรก) · วันก่อน = หลังจบวัน
const PULSE_EC_MANUAL_MS = 15 * 60000; // ปุ่ม 🔄: ผลที่อ่านภายใน 15 นาทีใช้ได้เลย
const PULSE_EC_PEEKED = {}; // brand|date → เวลาที่ดูผลแชร์ล่าสุด (ก่อนถึงรอบ ดูไม่เกิน 10 นาทีครั้ง)
function ecNeedSince(config, dateKey) {
  const today = dateKeyOf(new Date());
  if (dateKey > today) return null;
  if (dateKey < today) return new Date(dateKey + 'T00:00:00').getTime() + 86400000;
  const slots = (config.pulse && config.pulse.ecSlots) || [13, 20];
  const h = new Date().getHours();
  const passed = slots.filter(x => h >= x);
  if (!passed.length) return null;
  const d = new Date(); d.setHours(Math.max(...passed), 0, 0, 0);
  return d.getTime();
}
// v202 วันก่อน ecSince: ใช้ผลที่เคยเก็บไว้ (อ่านอย่างเดียว ไม่เขียนอะไรเลย)""", 'helpers')

# ---------- refreshEc ----------
rep("""  const refreshEc = (force) => { // force === true = ปุ่ม 🔄 เช็กกับเครื่องอีกครั้ง (อ่านครบทุกเครื่อง ไม่ใช้ผลที่แชร์)
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
      .then(res => { PULSE_EC_CACHE[cacheKey] = res; window.dispatchEvent(new CustomEvent('pulse-ec', { detail: cacheKey })); return res; })""",
    """  // v203 mode: true = ปุ่ม 🔄 (ผลที่อ่านภายใน 15 นาทีใช้ได้เลย) · อื่นๆ = ตามรอบอ่าน (ecSlots วันนี้ / หลังจบวันสำหรับวันก่อน)
  // อ่านเฉพาะเครื่องที่มีงานจากแอป (หยอดเหรียญ = รวมขนาดเดียวกัน) · ยังไม่ถึงรอบ/ยังไม่มีงาน = ดูผลที่แชร์อย่างเดียว
  const refreshEc = (mode) => {
    if (!config.pulse || isSol(config)) return Promise.resolve(null);
    if (PULSE_EC_INFLIGHT[cacheKey]) return PULSE_EC_INFLIGHT[cacheKey];
    const force = mode === true;
    const old = ecOldDay(config, dateKey);
    const since = force ? Date.now() - PULSE_EC_MANUAL_MS : ecNeedSince(config, dateKey);
    const c0 = PULSE_EC_CACHE[cacheKey];
    if (!old && !force && c0 && (since == null || (c0.at || 0) >= since)) return Promise.resolve(c0); // มีผลของรอบนี้แล้ว → ไม่แตะอะไรเลย
    if (!old && !force && since == null && Date.now() - (PULSE_EC_PEEKED[cacheKey] || 0) < 10 * 60000) return Promise.resolve(c0 || null);
    const prog = (text) => window.dispatchEvent(new CustomEvent('pulse-ec-progress', { detail: { key: cacheKey, text } }));
    const want = old ? null : ecActiveIds(config, logsRef.current, dateKey);
    prog('0/' + (want ? want.length : pulseMachines(config).length));
    const read = async () => {
      if (old) return loadEcSnapshot(config, dateKey); // 🔁 วันเก่า: ผลที่เก็บไว้เท่านั้น
      if (pulseEcReadPause() || since == null || (want && !want.length)) { PULSE_EC_PEEKED[cacheKey] = Date.now(); return peekEcShared(config, dateKey, want); }
      const sh = await loadEcShared(config, dateKey, false, want, since);
      if (sh && !sh.missing.length) return sh;
      const ids = sh ? sh.missing : want;
      const res = await fetchEcDay(config, dateKey, ids, (n, t) => prog(n + '/' + t), { fresh: false });
      const merged = sh ? { ...res, byMachine: { ...sh.byMachine, ...res.byMachine } } : res;
      await saveEcShared(config, dateKey, merged);
      return merged;
    };
    const p = read()
      .then(res => { if (res) PULSE_EC_CACHE[cacheKey] = res; window.dispatchEvent(new CustomEvent('pulse-ec', { detail: cacheKey })); return res || PULSE_EC_CACHE[cacheKey] || null; })""", 'refreshEc')

# ---------- รอ logs โหลดก่อนตัดสินว่าต้องอ่านเครื่องไหน ----------
rep("""  useEffect(() => {
    if (!window.db) return;
    const u = subscribePulseLogsByDays(dayKeys, setLogs);
    return () => { if (u) u(); };
  }, [dayKeys.join(',')]);""",
    """  const logsLoadedRef = useRef(false); // v203 ยังไม่ได้ logs ชุดแรก = ยังไม่รู้ว่าเครื่องไหนมีงาน → ยังไม่อ่านอัตโนมัติ
  useEffect(() => {
    if (!window.db) return;
    logsLoadedRef.current = false;
    const u = subscribePulseLogsByDays(dayKeys, (arr) => { logsLoadedRef.current = true; setLogs(arr); });
    return () => { if (u) u(); };
  }, [dayKeys.join(',')]);""", 'logs loaded ref')
rep("""    const c0 = PULSE_EC_CACHE[cacheKey];
    if (!old && !force && c0 && (since == null || (c0.at || 0) >= since)) return Promise.resolve(c0); // มีผลของรอบนี้แล้ว → ไม่แตะอะไรเลย""",
    """    const c0 = PULSE_EC_CACHE[cacheKey];
    if (!old && !force && c0 && (since == null || (c0.at || 0) >= since)) return Promise.resolve(c0); // มีผลของรอบนี้แล้ว → ไม่แตะอะไรเลย
    if (!old && !force && !logsLoadedRef.current) return Promise.resolve(c0 || null); // รอ logs ก่อน (ตัวเรียกจะเรียกใหม่เมื่อ logs มา)""", 'wait logs')

# ---------- เหรียญ: ตั้ง coinSeen จากรอบอ่าน ----------
rep("""        .forEach(l => pulseLogRef(l.id).set({ status: 'confirmed', recheckAt: Date.now() }, { merge: true }).catch(() => {}));
    });
  }, [ec, logs.length]);""",
    """        .forEach(l => pulseLogRef(l.id).set({ status: 'confirmed', recheckAt: Date.now() }, { merge: true }).catch(() => {}));
    });
  }, [ec, logs.length]);

  // 💵 v203 เช็กเหรียญจากรอบอ่าน (แทนเช็กทันทีทุกใบ) — กติกาเดียวกับ checkCoinLog (เครื่องเดียว → รวมขนาดเดียวกัน)
  useEffect(() => {
    if (!ec || ec.oldAccount || !ec.byMachine || !window.db) return;
    const ms = pulseMachines(config);
    const coins = logs.filter(l => l.brand === config.brand && l.dateKey === dateKey && pulseIsCoin(l) && (pulseLive(l) || pulseRefunded(l)));
    coins.filter(l => pulseLive(l) && l.coinSeen !== true).forEach(l => {
      const e = ec.byMachine[l.machine];
      if (!e) return;
      const eAt = e.fetchedAt || ec.at;
      if ((l.createdAt || 0) > eAt - 120000) return; // บันทึกหลังรอบอ่านนี้ → รอรอบถัดไป
      const upTo = (x) => (x.createdAt || 0) <= (l.createdAt || 0);
      const app = coins.filter(x => x.machine === l.machine && upTo(x)).reduce((a, x) => a + (x.baht || 0), 0);
      let seen = (e.coinBaht || 0) >= app;
      let group = null;
      if (!seen) {
        const me = ms.find(m => m.id === l.machine);
        const sib = me ? ms.filter(m => m.kind === me.kind && m.kg === me.kg).map(m => m.id) : [];
        if (sib.length > 1 && sib.every(id => ec.byMachine[id])) {
          group = { ec: sib.reduce((a, id) => a + (ec.byMachine[id].coinBaht || 0), 0), app: coins.filter(x => sib.includes(x.machine) && upTo(x)).reduce((a, x) => a + (x.baht || 0), 0) };
          seen = group.ec >= group.app;
        }
      }
      if (l.coinSeen !== seen) pulseLogRef(l.id).set({ coinSeen: seen, coinCheckAt: Date.now(), ecCoinBaht: e.coinBaht || 0, appCoinBaht: app, coinGroup: group, coinCheckVia: 'slot' }, { merge: true }).catch(() => {});
    });
  }, [ec, logs.length]);""", 'coin from slot')

rep("""  if (coinLog && !isSol(config)) watchCoinLog(config, coinLog); // 💵 v148: เช็กกับ EC ว่าเครื่องนับเหรียญแล้ว""",
    """  // 💵 v148 เคยเช็กกับ EC ทันที (watchCoinLog) · v203 เช็กตอนรอบอ่าน 13:00 / 20:00 แทน (เข้าเว็บ EC น้อยลง)""", 'no coin watch')

rep("""        : age < 180000 ? chip('bg-amber-100 text-amber-800', '⏳ ' + tr(config, 'กำลังเช็กเหรียญ…')) : null}""",
    """        : chip('bg-slate-100 text-slate-600', '🕐 ' + tr(config, 'รอเช็กกับเครื่องรอบถัดไป'))}""", 'coin chip')

# ---------- หน้าแรก / หน้ากระทบยอด ----------
rep("""  // เช็กกับเครื่องตอนเปิดหน้า (ถ้าเก่ากว่า 30 นาที) และทุก 60 นาที เฉพาะ 09:00–21:00 · v202 (v191 ทุก 30 นาที · เดิม 15)
  // อ่านเฉพาะเครื่องที่มีงานจากแอปวันนี้ — ปุ่ม 🔄 ในหน้ารายละเอียด = อ่านครบทุกเครื่อง
  useEffect(() => {
    const c = PULSE_EC_CACHE[config.brand + '|' + todayKey];
    if (!c || Date.now() - c.at > 30 * 60000) refreshEc();
    const t = setInterval(() => { if (!document.hidden && ecAutoHour()) refreshEc(); }, 60 * 60000);
    return () => clearInterval(t);
  }, [config.brand, todayKey]);""",
    """  // v203 อ่าน EC ตามรอบเท่านั้น (ecSlots 13:00 / 20:00) — มือถือเครื่องแรกที่เปิดหลังถึงรอบอ่านให้ เครื่องอื่นใช้ผลที่แชร์
  // ก่อนรอบแรกของวัน = ไม่อ่าน (ดูผลแชร์อย่างเดียว) · ยิงพัลส์ยังเช็กผลทันทีที่ Worker เหมือนเดิม · (v202 ทุก 60 นาที · v191 ทุก 30 นาที)
  useEffect(() => {
    const tick = () => { if (!document.hidden) refreshEc({ auto: true }); };
    tick();
    const t = setInterval(tick, 5 * 60000);
    return () => clearInterval(t);
  }, [config.brand, todayKey]);
  useEffect(() => { refreshEc({ auto: true }); }, [logs.length]); // v203 logs มาแล้ว/มีงานใหม่ → เช็กรอบ (มีผลรอบนี้แล้วจะไม่อ่านซ้ำ)""", 'home slots')
rep("""    if (!autoEc) return;
    const c = PULSE_EC_CACHE[config.brand + '|' + dateKey];
    if (!c || Date.now() - c.at > 5 * 60000) refreshEc();
  }, [dateKey, autoEc]);""",
    """    if (!autoEc) return;
    refreshEc({ auto: true }); // v203 ตามรอบอ่าน — เปิดหน้านี้ซ้ำไม่อ่าน EC ซ้ำ
  }, [dateKey, autoEc, logs.length]);""", 'panel auto')
rep("""  const { recon, ecBusy, refreshEc, note, unexplained } = usePulseRecon(config, orders, dateKey);""",
    """  const { recon, ecBusy, refreshEc, note, unexplained, logs } = usePulseRecon(config, orders, dateKey);""", 'panel logs')
rep("""    try { const n = await askClaimOutside(config, issues); if (n) refreshEc(); }""",
    """    try { const n = await askClaimOutside(config, issues); if (n) refreshEc({ auto: true }); }""", 'claim')
rep("""            {ecBusy ? `⏳ ${tr(config, 'กำลังเช็กกับเครื่อง')} ${ecBusy}` : `${compact ? '' : '🔄 '}${tr(config, 'เช็กกับเครื่องอีกครั้ง')}`}
          </button>}""",
    """            {ecBusy ? `⏳ ${tr(config, 'กำลังเช็กกับเครื่อง')} ${ecBusy}` : `${compact ? '' : '🔄 '}${tr(config, 'เช็กกับเครื่องอีกครั้ง')}`}
          </button>}
          {!isSol(config) && config.pulse && config.pulse.ecSlots && <p className="text-[11px] text-slate-400 text-center" data-ec-slots>{tr(config, 'เช็กกับเครื่องอัตโนมัติ 13:00 และ 20:00')}</p>}""", 'slot hint')

# ---------- ⚙️ ทดสอบ: ล็อกอินล่าสุด ----------
rep("""          + (st.loginsToday != null ? ` · วันนี้ ${st.loginsToday}/${st.maxLoginsPerDay} · เข้าเว็บ EC วันนี้ ${st.reqToday}/${st.maxReqPerDay}` : '') // v202 Worker v1.2""",
    """          + (st.loginsToday != null ? ` · วันนี้ ${st.loginsToday}/${st.maxLoginsPerDay} · เข้าเว็บ EC วันนี้ ${st.reqToday}/${st.maxReqPerDay}` : '') // v202 Worker v1.2
          + (st.recentLogins && st.recentLogins.length ? ` · ล็อกอินล่าสุด ${st.recentLogins.slice(-3).map(x => x.at.slice(6)).join(', ')}` : '') // v203 Worker v1.3""", 'test logins')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v203 patched')
