#!/usr/bin/env python3
"""v182 — ล็อกอินก่อนเลือกร้าน (ทุกร้านใช้หน้าล็อกอินเดียว) + ล็อกอินค้าง + จำร้านล่าสุด
ที่มา: เจ้าของ 1 พ.ย. 69
  'เปลี่ยนรูปแบบการใช้งานเป็นการ login ก่อนเลยดีกว่า … เปิดสิทให้แม่บ้านเห็นเฉพาะที่ตัวเองดูแล
   ถ้าดูแลมากกว่า 1 ร้าน ก็ต้องเลือกร้านก่อน ถ้าดูแลแค่ร้านเดียว ข้ามหน้านี้ไปเลย
   สิทแม่บ้าน ลงใบงานเหมือนเดิม · เจ้าของเห็นทุกอย่าง · แอดมิน มีแค่งานภายในที่ไม่นับเงิน'
  'ทำ login ค้างด้วยนะ จะได้เร็วๆ'
ทำอะไร
  - App: ไม่มี session → หน้าล็อกอินรวม (StaffLoginView global: รายชื่อทุกร้าน + PIN · 👔 เจ้าของ · คู่มือ)
    session เก็บใน localStorage 'plp-session' (ค้างจนกดออก) · เครื่องที่ล็อกอินแบบเดิมค้างอยู่ ย้ายมาเป็น session ให้เอง
  - ร้านที่เข้าได้ = staff.shops (ไม่มี = staff.brand เดิม) · เจ้าของ = ทุกร้าน · 1 ร้าน = เข้าเลย · หลายร้าน = หน้าเลือกร้าน (เฉพาะร้านตัวเอง)
    จำร้านล่าสุด 'plp-last-shop' → เปิดแอปเข้าร้านนั้นเลย (สลับร้านได้ที่ปุ่มเดิม)
  - ร้านที่ไม่เคยต้องล็อกอิน (Teddy 1 · hasStaffLogin ไม่มี) และยังไม่มีบัญชีแม่บ้าน → ปุ่ม 'เข้าร้าน … · ยังไม่มีบัญชีแม่บ้าน' ชั่วคราว
    (มีบัญชีแม่บ้านของร้านนั้นเมื่อไหร่ ปุ่มหาย + เครื่องที่เข้าแบบนี้ออกจากระบบเอง)
  - จัดการรายชื่อ (หน้าล็อกอิน · รหัสเจ้าของ): เพิ่มคนเลือกร้านที่ดูแล + แอดมิน · แถวรายชื่อกดเปิด/ปิดร้านที่ดูแล
  - subscribeToStaff(ร้าน) รวมคนที่ shops มีร้านนั้นด้วย · ออกจากระบบในร้าน = ออกทั้งแอป
usage: python3 tools/v182_login_first.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


def wrap(start, end, pre, post, label):
    """ใส่ pre หน้า start และ post หน้า end (end = จุดแรกหลัง start)"""
    global s
    assert s.count(start) == 1, f'{label}: start {s.count(start)}'
    a = s.index(start); b = s.index(end, a)
    s = s[:a] + pre + s[a:b] + post + s[b:]


rep("window.APP_VERSION = 'v181-2026-11-01';", "window.APP_VERSION = 'v182-2026-11-01';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v181';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v181';", "const CACHE_NAME = 'plp-laundry-v182';")

# ---------- 1) helpers ----------
rep("""function subscribeToStaff(brand, callback) {
  return window.db.collection('staff').where('brand', '==', brand).onSnapshot(
    { includeMetadataChanges: true },
    snapshot => {
      const items = snapshot.docs.map(d => ({ id: d.id, ...d.data() }));
      const fromCache = snapshot.metadata.fromCache;
      if (!fromCache) { try { localStorage.setItem('staffCache-' + brand, JSON.stringify(items)); } catch {} }
      callback(items, { fromCache });
    },
    error => { console.error('subscribe staff error:', error); callback(null, { error }); }
  );
}""",
    """function subscribeToStaff(brand, callback) {
  // 🔑 v182: รวมคนที่ดูแลหลายร้าน (staff.shops มีร้านนี้) แม้ staff.brand เป็นร้านอื่น
  let main = null, mainMeta = { fromCache: true }, extra = [];
  const emit = () => {
    if (!main) return;
    const ids = new Set(main.map(x => x.id));
    const items = [...main, ...extra.filter(x => !ids.has(x.id))];
    if (!mainMeta.fromCache) { try { localStorage.setItem('staffCache-' + brand, JSON.stringify(items)); } catch {} }
    callback(items, mainMeta);
  };
  const u1 = window.db.collection('staff').where('brand', '==', brand).onSnapshot(
    { includeMetadataChanges: true },
    snapshot => { main = snapshot.docs.map(d => ({ id: d.id, ...d.data() })); mainMeta = { fromCache: snapshot.metadata.fromCache }; emit(); },
    error => { console.error('subscribe staff error:', error); callback(null, { error }); }
  );
  const u2 = window.db.collection('staff').where('shops', 'array-contains', brand).onSnapshot(
    snapshot => { extra = snapshot.docs.map(d => ({ id: d.id, ...d.data() })); emit(); },
    () => {}
  );
  return () => { if (u1) u1(); if (u2) u2(); };
}
// 🔑 v182 ล็อกอินก่อนเลือกร้าน — หน้าล็อกอินเดียวทุกร้าน · ล็อกอินค้างในเครื่อง · แม่บ้านเห็นเฉพาะร้านที่ดูแล
const ALL_SHOPS = ['otteri', 'teddy', 'teddy2'];
const SHOP_NAME = { otteri: 'Otteri', teddy: 'Teddy', teddy2: 'Teddy 2' };
const shopsOf = (st) => (!st ? [] : st.isOwnerLogin ? ALL_SHOPS.slice() : (Array.isArray(st.shops) && st.shops.filter(b => ALL_SHOPS.includes(b)).length ? st.shops.filter(b => ALL_SHOPS.includes(b)) : (ALL_SHOPS.includes(st.brand) ? [st.brand] : [])));
const SESSION_KEY = 'plp-session';
const sessionOf = (st) => { const x = { ...(st || {}) }; delete x.pin; return x; };
function saveSession(x) { try { if (x) localStorage.setItem(SESSION_KEY, JSON.stringify(x)); else localStorage.removeItem(SESSION_KEY); } catch (e) {} }
function loadSession() {
  try { const x = JSON.parse(localStorage.getItem(SESSION_KEY) || 'null'); if (x && (x.id || x.guest)) return x; } catch (e) {}
  // ย้ายจากแบบเดิม (เลือกร้านแล้วค่อยล็อกอิน) — เครื่องที่ล็อกอินค้างไว้ใช้ต่อได้เลย
  for (const b of ['otteri', 'teddy2', 'teddy']) {
    try {
      const st = JSON.parse(localStorage.getItem('staff-' + b) || 'null');
      if (st && st.id && !st.previewOwner) { const x = sessionOf(st.isOwnerLogin ? st : { ...st, brand: st.brand || b }); saveSession(x); try { localStorage.setItem('plp-last-shop', b); } catch (e) {} return x; }
    } catch (e) {}
  }
  return null;
}
function subscribeToAllStaff(callback) {
  return window.db.collection('staff').onSnapshot(
    { includeMetadataChanges: true },
    snapshot => {
      const items = snapshot.docs.map(d => ({ id: d.id, ...d.data() }));
      const fromCache = snapshot.metadata.fromCache;
      if (!fromCache) { try { localStorage.setItem('staffCache-all', JSON.stringify(items)); } catch {} }
      callback(items, { fromCache });
    },
    error => { console.error('subscribe all staff error:', error); callback(null, { error }); }
  );
}
const LOGIN_CONFIG = { brand: 'all', name: 'PLP Laundromat', subtitle: 'Otteri · Teddy · Teddy 2', gradient: 'linear-gradient(135deg, #0EA5E9 0%, #14B8A6 100%)', primaryColor: '#0EA5E9' };
const shopConfigOf = (b) => (b === 'otteri' ? OTTERI_CONFIG : b === 'trainee' ? TRAINEE_CONFIG : b === 'teddy2' ? TEDDY2_CONFIG : TEDDY_CONFIG);""", 'helpers')

# ---------- 2) App ----------
rep("""function App() {
  const [deep, setDeep] = useState(DEEP_START);
  const [brand, setBrand] = useState(DEEP_START ? DEEP_START.b : null);
  useEffect(() => {
    if (DEEP_START) { try { window.history.replaceState(null, '', window.location.pathname + window.location.hash); } catch (e) {} }
  }, []);
  const [showDelivery, setShowDelivery] = useState(false);
  const [showGuide, setShowGuide] = useState(false);
""",
    """function App() {
  const [deep, setDeep] = useState(DEEP_START);
  const [brand, setBrandState] = useState(() => { if (DEEP_START) return DEEP_START.b; try { return localStorage.getItem('plp-last-shop') || null; } catch (e) { return null; } }); // 🔑 v182 จำร้านล่าสุด
  const setBrand = (b) => { try { if (b) localStorage.setItem('plp-last-shop', b); else localStorage.removeItem('plp-last-shop'); } catch (e) {} setBrandState(b); };
  useEffect(() => {
    if (DEEP_START) { try { window.history.replaceState(null, '', window.location.pathname + window.location.hash); } catch (e) {} }
  }, []);
  const [showDelivery, setShowDelivery] = useState(false);
  const [showGuide, setShowGuide] = useState(false);
  // 🔑 v182 ล็อกอินก่อนเลือกร้าน · ค้างในเครื่องจนกดออก
  const [session, setSessionState] = useState(() => loadSession());
  const setSession = (x) => { saveSession(x); setSessionState(x); };
  const [allStaff, setAllStaff] = useState(() => loadStaffCache('all'));
  const [staffStatus, setStaffStatus] = useState('loading');
  const [loginLang, setLoginLang] = useState(() => { try { return localStorage.getItem('lang-all') || (['otteri', 'teddy2', 'teddy'].some(b => localStorage.getItem('lang-' + b) === 'mm') ? 'mm' : 'th'); } catch (e) { return 'th'; } });
  const syncedRef = useRef('');
  useEffect(() => {
    if (!window.db) return;
    const t = setTimeout(() => setStaffStatus(x => x === 'loading' ? 'slow' : x), 10000);
    const u = subscribeToAllStaff((items, meta) => {
      if (meta.error) { setStaffStatus('error:' + (meta.error.code || 'unknown')); return; }
      if (meta.fromCache && items.length === 0) return;
      setAllStaff(items.sort((a, b) => (a.createdAt || 0) - (b.createdAt || 0)));
      if (!meta.fromCache) setStaffStatus('ok');
    });
    return () => { clearTimeout(t); if (u) u(); };
  }, []);
  const live = session && !session.isOwnerLogin && !session.guest ? (allStaff.find(x => x.id === session.id) || session) : session;
  // ร้านที่เดิมไม่ต้องล็อกอิน (Teddy 1) และยังไม่มีบัญชีแม่บ้าน → เข้าได้ชั่วคราว จนกว่าเจ้าของจะเพิ่มชื่อ
  const guestShops = ALL_SHOPS.filter(b => !shopConfigOf(b).hasStaffLogin && !allStaff.some(x => x.active !== false && shopsOf(x).includes(b)));
  const logout = () => { syncedRef.current = ''; setSession(null); setDeep(null); setBrand(null); };
  useEffect(() => { // บัญชีถูกปิด · ร้านชั่วคราวมีบัญชีแม่บ้านแล้ว → ออกจากระบบ
    if (!session) return;
    if (session.guest && !guestShops.includes(session.guest)) logout();
    else if (live && !live.isOwnerLogin && !live.guest && live.active === false) logout();
  }, [session && (session.id || session.guest), live && live.active, guestShops.join()]);
""", 'App state')
rep("""  if (!brand) {
    return <BrandSelector onSelect={setBrand} onOpenDelivery={() => setShowDelivery(true)} onOpenGuide={() => setShowGuide(true)} />;
  }
  
  const config = brand === 'otteri' ? OTTERI_CONFIG : brand === 'trainee' ? TRAINEE_CONFIG : brand === 'teddy2' ? TEDDY2_CONFIG : TEDDY_CONFIG;
  return <BrandApp config={config} onChangeBrand={() => { setDeep(null); setBrand(null); }} deepJobId={deep && deep.b === brand ? deep.o : null} onDeepDone={() => setDeep(null)} />;
}""",
    """  if (!session) {
    return <StaffLoginView global config={{ ...LOGIN_CONFIG, lang: loginLang }} staffList={allStaff} staffStatus={staffStatus}
      onToggleLang={() => setLoginLang(l => { const n = l === 'th' ? 'mm' : 'th'; try { localStorage.setItem('lang-all', n); } catch (e) {} return n; })}
      onLogin={(st) => { syncedRef.current = ''; setSession(sessionOf(st)); }}
      guestShops={guestShops} onGuest={(b) => { syncedRef.current = ''; setSession({ guest: b, id: 'guest-' + b, name: '' }); setBrand(b); }}
      onOpenGuide={() => setShowGuide(true)} />;
  }
  const shops = live.guest ? [live.guest] : shopsOf(live);
  const b = brand && shops.includes(brand) ? brand : shops.length === 1 ? shops[0] : null;
  if (!b) {
    if (!shops.length) return (
      <div className="min-h-screen flex flex-col items-center justify-center p-6 text-center" style={{ background: LOGIN_CONFIG.gradient }} data-no-shop>
        <p className="text-white text-lg font-extrabold">{live.name} · ยังไม่ได้กำหนดร้านที่ดูแล</p>
        <p className="text-white text-sm mt-1">แจ้งเจ้าของร้านให้ติ๊กร้านในหน้าจัดการรายชื่อ</p>
        <button onClick={logout} className="mt-4 px-5 py-2.5 rounded-xl bg-white text-slate-800 font-bold text-sm active:scale-95">ออกจากระบบ</button>
      </div>
    );
    return <BrandSelector allowed={shops} who={live} onLogout={logout} onSelect={setBrand} onOpenDelivery={() => setShowDelivery(true)} onOpenGuide={() => setShowGuide(true)} />;
  }
  // ส่งตัวตนให้ร้าน (BrandApp อ่าน staff-<ร้าน> ตอนเปิด) — ทำครั้งเดียวต่อการเข้าร้าน
  if (syncedRef.current !== b + '|' + (live.id || live.guest)) {
    syncedRef.current = b + '|' + (live.id || live.guest);
    try {
      if (live.guest) localStorage.removeItem('staff-' + b);
      else localStorage.setItem('staff-' + b, JSON.stringify(sessionOf(live)));
      localStorage.setItem('plp-last-shop', b);
      const lg = localStorage.getItem('lang-all');
      if (lg) localStorage.setItem('lang-' + b, lg);
    } catch (e) {}
  }
  const config = shopConfigOf(b);
  return <BrandApp key={b + '|' + (live.id || live.guest)} config={config} onChangeBrand={shops.length > 1 ? () => { setDeep(null); setBrand(null); setBrandState(null); try { localStorage.removeItem('plp-last-shop'); } catch (e) {} } : null}
    onLogout={logout} deepJobId={deep && deep.b === b ? deep.o : null} onDeepDone={() => setDeep(null)} />;
}""", 'App routing')

# ---------- 3) หน้าเลือกร้าน: เฉพาะร้านที่ดูแล ----------
rep("""function BrandSelector({ onSelect, onOpenDelivery, onOpenGuide }) {""",
    """function BrandSelector({ onSelect, onOpenDelivery, onOpenGuide, allowed, who, onLogout }) {
  const can = (b) => !allowed || allowed.includes(b); // 🔑 v182 เฉพาะร้านที่ดูแล""", 'BrandSelector sig')
rep("""        <p className="text-slate-500 text-sm">Welcome • เลือกแบรนด์เพื่อเริ่มต้น</p>""",
    """        <p className="text-slate-500 text-sm" data-brand-who>{who ? `${who.isOwnerLogin ? '👔 เจ้าของ' : (who.role === 'admin' ? '🔧 ' : '🧹 ') + (who.name || '')} · เลือกร้านเพื่อเริ่มต้น` : 'Welcome • เลือกแบรนด์เพื่อเริ่มต้น'}</p>
        {onLogout && <button onClick={onLogout} data-brand-logout className="mt-3 px-4 py-1.5 rounded-full bg-white border border-slate-200 text-xs font-bold text-slate-600 active:scale-95">🚪 ออกจากระบบ</button>}""", 'BrandSelector header')
wrap("""        <button onClick={() => onSelect('otteri')}""", """

        {/* การ์ด Teddy — มีปุ่มเช็คค่าส่งเล็กมุมขวา */}""", "{can('otteri') && (\n", "\n        )}", 'card otteri')
wrap("""        <div className="w-full bg-white rounded-3xl p-5 shadow-xl border-2 border-blue-100">""", """

        {/* การ์ด Teddy 2""", "{can('teddy') && (\n", "\n        )}", 'card teddy')
wrap("""        <div className="w-full bg-white rounded-3xl p-5 shadow-xl" style={{ border: '2px solid #4FD1C5' }}>""", """

        {/* แบรนด์ที่ 3""", "{can('teddy2') && (\n", "\n        )}", 'card teddy2')

# ---------- 4) หน้าล็อกอินรวม (StaffLoginView global) ----------
rep("""function StaffLoginView({ config, staffList, staffStatus = 'ok', onLogin, onToggleLang }) {""",
    """function StaffLoginView({ config, staffList, staffStatus = 'ok', onLogin, onToggleLang, global, guestShops, onGuest, onOpenGuide }) {
  const [newShops, setNewShops] = useState([]); // 🔑 v182 ร้านที่ดูแล (หน้าล็อกอินรวม)
  const toggleShop = (st, b) => { // เจ้าของเปิด/ปิดร้านที่คนนี้ดูแล
    const cur = shopsOf(st), on = cur.includes(b);
    const next = on ? cur.filter(x => x !== b) : [...cur, b];
    if (!next.length) { alert(tr(config, 'ต้องดูแลอย่างน้อย 1 ร้าน')); return; }
    updateStaffInCloud(st.id, { shops: next }).catch(e => alert('อัปเดตไม่สำเร็จ: ' + e.message));
  };""", 'StaffLoginView sig')
rep("""          <img src={config.logo} alt="logo" className="w-20 h-20 rounded-2xl shadow-lg mb-3" />""",
    """          {global ? (
            <div className="flex gap-2 mb-3" data-login-global>
              {[OTTERI_LOGO, TEDDY_LOGO, TEDDY2_LOGO].map((src, i) => <img key={i} src={src} alt="" className="w-14 h-14 rounded-2xl shadow-lg bg-white object-cover" />)}
            </div>
          ) : <img src={config.logo} alt="logo" className="w-20 h-20 rounded-2xl shadow-lg mb-3" />}""", 'login logos')
rep("""    if (!/^\\d{4}$/.test(newPin)) { alert('PIN ต้องเป็นตัวเลข 4 หลัก'); return; }
    try {
      await saveStaffToCloud(config.brand, { name, pin: newPin, avatar: newAvatar, active: true, createdAt: Date.now(), ...(newAdmin ? { role: 'admin' } : {}) });
      setNewAdmin(false);""",
    """    if (!/^\\d{4}$/.test(newPin)) { alert('PIN ต้องเป็นตัวเลข 4 หลัก'); return; }
    if (global && !newShops.length) { alert(tr(config, 'เลือกร้านที่ดูแลอย่างน้อย 1 ร้าน')); return; }
    try {
      await saveStaffToCloud(global ? newShops[0] : config.brand, { name, pin: newPin, avatar: newAvatar, active: true, createdAt: Date.now(), ...(newAdmin ? { role: 'admin' } : {}), ...(global ? { shops: newShops } : {}) });
      setNewAdmin(false);
      setNewShops([]);""", 'add staff shops')
rep("""              <label className="flex items-start gap-2 mb-2 text-xs font-bold text-slate-700" data-new-admin>""",
    """              {global && (
                <div className="mb-2" data-new-shops>
                  <p className="text-xs font-bold text-slate-700 mb-1">🏪 {tr(config, 'ร้านที่ดูแล')}</p>
                  <div className="flex gap-1.5 flex-wrap">
                    {ALL_SHOPS.map(b => (
                      <button key={b} type="button" data-new-shop={b} onClick={() => setNewShops(v => v.includes(b) ? v.filter(x => x !== b) : [...v, b])}
                        className={`px-2.5 py-1 rounded-lg text-xs font-bold border ${newShops.includes(b) ? 'bg-teal-600 text-white border-teal-600' : 'bg-white text-slate-600 border-slate-200'}`}>{newShops.includes(b) ? '✓ ' : ''}{SHOP_NAME[b]}</button>
                    ))}
                  </div>
                </div>
              )}
              <label className="flex items-start gap-2 mb-2 text-xs font-bold text-slate-700" data-new-admin>""", 'add form shops')
rep("""                      <p className="text-xs text-slate-400">PIN: {s.pin}</p>
                    </div>
                    <button data-role-toggle={s.id}""",
    """                      <p className="text-xs text-slate-400">PIN: {s.pin}</p>
                      {global && (
                        <div className="flex gap-1 mt-1 flex-wrap">
                          {ALL_SHOPS.map(b => { const on = shopsOf(s).includes(b); return (
                            <button key={b} data-shop-toggle={s.id + ':' + b} onClick={() => toggleShop(s, b)}
                              className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${on ? 'bg-teal-100 text-teal-800' : 'bg-slate-100 text-slate-400'}`}>{on ? '✓ ' : ''}{SHOP_NAME[b]}</button>
                          ); })}
                        </div>
                      )}
                    </div>
                    <button data-role-toggle={s.id}""", 'row shop toggles')
rep("""                    {s.role === 'admin' && <span className="text-[10px] font-bold text-indigo-700">🔧 {tr(config, 'แอดมิน · งานภายใน')}</span>}""",
    """                    {s.role === 'admin' && <span className="text-[10px] font-bold text-indigo-700">🔧 {tr(config, 'แอดมิน · งานภายใน')}</span>}
                    {global && <span className="text-[10px] font-bold text-slate-400" data-pick-shops>{shopsOf(s).map(b => SHOP_NAME[b]).join(' · ')}</span>}""", 'pick shops label')
rep("""              <button onClick={handleOwnerLogin} className="flex-1 py-2 text-xs font-bold text-slate-500 bg-slate-50 rounded-xl active:scale-95 transition">
                {tr(config, "👔 เข้าแบบเจ้าของ")}
              </button>
            </div>""",
    """              <button onClick={handleOwnerLogin} className="flex-1 py-2 text-xs font-bold text-slate-500 bg-slate-50 rounded-xl active:scale-95 transition">
                {tr(config, "👔 เข้าแบบเจ้าของ")}
              </button>
              {global && <button onClick={handleOpenManage} data-open-manage className="flex-1 py-2 text-xs font-bold text-slate-500 bg-slate-50 rounded-xl active:scale-95 transition">⚙️ {tr(config, 'จัดการรายชื่อ')}</button>}
            </div>
            {global && (guestShops || []).map(b => (
              <button key={b} data-guest={b} onClick={() => onGuest && onGuest(b)} className="w-full mt-2 py-2.5 text-xs font-bold text-amber-900 bg-amber-50 border border-amber-200 rounded-xl active:scale-95 transition">
                🏪 {tr(config, 'เข้าร้าน')} {SHOP_NAME[b]} · {tr(config, 'ยังไม่มีบัญชีแม่บ้าน')}
              </button>
            ))}
            {global && onOpenGuide && (
              <button onClick={onOpenGuide} className="w-full mt-2 py-2 text-xs font-bold text-sky-700 bg-sky-50 rounded-xl active:scale-95 transition">📖 {tr(config, 'คู่มือช่วยงาน')}</button>
            )}""", 'login bottom buttons')

# หน้าตั้งค่าเจ้าของ (SettingsView): เปิด/ปิดร้านที่ดูแลรายคน
rep("""                <p className="text-[11px] text-slate-400">PIN ****{s.role === 'admin' ? ' · 🔧 แอดมิน (งานภายในเท่านั้น)' : ''}</p>""",
    """                <p className="text-[11px] text-slate-400">PIN ****{s.role === 'admin' ? ' · 🔧 แอดมิน (งานภายในเท่านั้น)' : ''}</p>
                <div className="flex gap-1 mt-1 flex-wrap" data-settings-shops={s.id}>
                  {ALL_SHOPS.map(b => { const on = shopsOf(s).includes(b); return (
                    <button key={b} onClick={() => { const cur = shopsOf(s); const next = on ? cur.filter(x => x !== b) : [...cur, b]; if (!next.length) { alert('ต้องดูแลอย่างน้อย 1 ร้าน'); return; } updateStaffInCloud(s.id, { shops: next }).catch(e => alert('อัปเดตไม่สำเร็จ: ' + e.message)); }}
                      className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${on ? 'bg-teal-100 text-teal-800' : 'bg-slate-100 text-slate-400'}`}>{on ? '✓ ' : ''}{SHOP_NAME[b]}</button>
                  ); })}
                </div>""", 'settings shop toggles')

# ---------- 5) BrandApp: ออกจากระบบ = ออกทั้งแอป · ปุ่มเปลี่ยนร้านเฉพาะคนที่มีหลายร้าน ----------
rep("""function BrandApp({ config: baseConfig, onChangeBrand, deepJobId, onDeepDone }) {""",
    """function BrandApp({ config: baseConfig, onChangeBrand, deepJobId, onDeepDone, onLogout }) {""", 'BrandApp sig')
rep("""    if (!confirm('ออกจากระบบและสลับผู้ใช้?')) return false;
    try { localStorage.removeItem('staff-' + config.brand); } catch {}
    savePrevStaff(null);""",
    """    if (!confirm('ออกจากระบบและสลับผู้ใช้?')) return false;
    try { localStorage.removeItem('staff-' + config.brand); } catch {}
    savePrevStaff(null);
    if (onLogout) { onLogout(); return true; } // 🔑 v182 กลับหน้าล็อกอินรวม""", 'logout global')
rep("""              <button onClick={onChangeBrand} className="bg-white bg-opacity-20 backdrop-blur-sm rounded-full p-2.5 border border-white border-opacity-30 active:scale-95 transition" title={tr(config, "เปลี่ยนร้าน")}>
                <Icon name="repeat" className="w-5 h-5 text-white" />
              </button>""",
    """              {onChangeBrand && <button onClick={onChangeBrand} className="bg-white bg-opacity-20 backdrop-blur-sm rounded-full p-2.5 border border-white border-opacity-30 active:scale-95 transition" title={tr(config, "เปลี่ยนร้าน")}>
                <Icon name="repeat" className="w-5 h-5 text-white" />
              </button>}""", 'home change brand')
rep("""            <button onClick={onChangeBrand} className="h-10 px-3.5 rounded-full bg-slate-800 border border-slate-700 text-white text-sm font-bold active:scale-95">เปลี่ยนร้าน</button>""",
    """            {onChangeBrand && <button onClick={onChangeBrand} className="h-10 px-3.5 rounded-full bg-slate-800 border border-slate-700 text-white text-sm font-bold active:scale-95">เปลี่ยนร้าน</button>}""", 'owner t2 change brand')
rep("""              <button onClick={onChangeBrand} className="bg-white bg-opacity-10 backdrop-blur-sm rounded-full px-2.5 py-2 border border-white border-opacity-20 active:scale-95 transition flex items-center gap-1 text-white text-xs">
                <Icon name="repeat" className="w-3 h-3" />
              </button>""",
    """              {onChangeBrand && <button onClick={onChangeBrand} className="bg-white bg-opacity-10 backdrop-blur-sm rounded-full px-2.5 py-2 border border-white border-opacity-20 active:scale-95 transition flex items-center gap-1 text-white text-xs">
                <Icon name="repeat" className="w-3 h-3" />
              </button>}""", 'owner old change brand')

# ---------- 6) MM ----------
rep("""  'วันเวลาที่ทำงาน': 'အလုပ်လုပ်သည့် ရက်/အချိန်',""",
    """  'วันเวลาที่ทำงาน': 'အလုပ်လုပ်သည့် ရက်/အချိန်',
  // v182 ล็อกอินรวม
  'เข้าร้าน': 'ဆိုင်ထဲဝင်ရန်',
  'จัดการรายชื่อ': 'ဝန်ထမ်းစာရင်း စီမံရန်',
  'ยังไม่มีบัญชีแม่บ้าน': 'ဝန်ထမ်းအကောင့် မရှိသေး',
  'ร้านที่ดูแล': 'တာဝန်ယူသည့် ဆိုင်',
  'ต้องดูแลอย่างน้อย 1 ร้าน': 'အနည်းဆုံး ဆိုင် ၁ ဆိုင် ရွေးရမည်',
  'เลือกร้านที่ดูแลอย่างน้อย 1 ร้าน': 'တာဝန်ယူသည့် ဆိုင် အနည်းဆုံး ၁ ဆိုင် ရွေးပါ',""", 'MM')
if "  'คู่มือช่วยงาน':" not in s:
    rep("""  'เข้าร้าน': 'ဆိုင်ထဲဝင်ရန်',""", """  'เข้าร้าน': 'ဆိုင်ထဲဝင်ရန်',
  'คู่มือช่วยงาน': 'အလုပ်လမ်းညွှန်',""", 'MM guide')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v182 applied')
