// ---------- 🟦 Otteri: เริ่มเครื่องผ่าน SOL (แม่บ้านกด Start ในบัญชีของตัวเอง แล้วกลับมาติ๊กในแอป) ----------
// แอปไม่สั่งเครื่องเอง — จำว่า "รอกดใน SOL" ไว้ในเครื่อง (ปิดแอปก็ไม่หาย) · กด ✅ แล้วค่อยบันทึก pulseLogs method 'sol'
const solCodeOf = (order) => '#' + (order && order.queueNo != null ? order.queueNo : ((order && order.id) || '').slice(-4));
const SOL_PROG = { cold: 'Cold', warm: 'Warm', hot: 'Hot', high: 'High', med: 'Mid', low: 'Low' };
const solPendingKey = (config) => 'sol-pending-' + config.brand;
function solPendingList(config) {
  try { const a = JSON.parse(localStorage.getItem(solPendingKey(config)) || '[]'); return Array.isArray(a) ? a : []; } catch (e) { return []; }
}
function solPendingSave(config, list) {
  try { localStorage.setItem(solPendingKey(config), JSON.stringify(list)); } catch (e) {}
  window.dispatchEvent(new CustomEvent('sol-pending'));
}
function solPendingAdd(config, p) {
  const list = solPendingList(config);
  list.push({ ...p, key: `${p.orderId}-${p.machine}-${p.at}` });
  solPendingSave(config, list);
}
function solPendingRemove(config, key) { solPendingSave(config, solPendingList(config).filter(x => x.key !== key)); }
function solNotify(detail) { window.dispatchEvent(new CustomEvent('sol-done', { detail })); }
// ข้อความ "ไปกด Start ใน SOL…" ในหน้าเลือกเครื่อง → เปลี่ยนเป็นผลจริงเมื่อกด ✅ / ยกเลิก ที่แถบล่าง
function useSolMsgSync(msg, setMsg) {
  useEffect(() => {
    if (!msg || !msg.solPending) return;
    const f = (e) => setMsg(e.detail);
    window.addEventListener('sol-done', f);
    return () => window.removeEventListener('sol-done', f);
  }, [msg]);
}

// บันทึกว่าเริ่มเครื่องใน SOL แล้ว (แทนการยิงพัลส์) — นับเหมือนพัลส์ที่เครื่องรับแล้ว
function solRecordStart(config, { machine, pulses, refType, refId, slotKey, refLabel, meta }) {
  const staff = currentStaffLS(config);
  const now = Date.now();
  const id = `${config.brand}-sol-${now}-${Math.random().toString(36).slice(2, 8)}`;
  const log = cleanUndefined({
    brand: config.brand, dateKey: dateKeyOf(new Date(now)), machine, machineLabel: pulseMachineLabel(config, machine),
    pulses, baht: pulses * PULSE_BAHT, method: 'sol', status: 'confirmed',
    refType, refId: refId || null, slotKey: slotKey || null, refLabel: refLabel || '',
    staffId: staff && staff.id ? staff.id : null, staffName: staff && staff.name ? staff.name : '',
    createdAt: now, doneAt: now, ...(meta || {}),
  });
  pulseLogRef(id).set(log).catch(e => console.error('sol log error:', e));
  return { id, ...log };
}

// สิ่งที่ต้องกดในหน้าต่าง "Select Menu" ของ SOL (ไม่มีลิงก์ตรงไปเครื่อง — URL ของ SOL ค้างที่ /dashboard)
const SOL_WASH_BTNS = [['hot', 'Hot', '#F8A5A5'], ['warm', 'Warm', '#FBD938'], ['cold', 'Cold', '#93C5FD']]; // สีเหมือนปุ่มใน SOL
const SOL_DRY_BTNS = [['high', 'High', '#F8A5A5'], ['med', 'Mid', '#FBD938'], ['low', 'Low', '#93C5FD']]; // เครื่องอบ: สีเดียวกับเครื่องซัก (เห็นหน้าจริง 29 ต.ค.)
function solPlan(config, p) {
  if (p.kind === 'wash') return { btns: SOL_WASH_BTNS, prog: p.temp || 'cold', price: p.baht, extra: 0 };
  const base = dryPriceFor(config, p.kg);
  const prog = p.heat || 'high';
  if (p.baht >= base && base > 0) return { btns: SOL_DRY_BTNS, prog, price: base, extra: p.baht - base };
  return { btns: null, prog, price: null, extra: p.baht }; // เติมเวลาอย่างเดียว
}
// ข้อความขั้นตอน (ใช้ทดสอบ/อ่านง่าย)
function solSteps(config, p) {
  const pl = solPlan(config, p);
  const out = [`${tr(config, 'เปิด SOL → แตะรูปเครื่อง')} ${p.machine} → ${pl.price != null ? 'Select Menu' : 'Extra Time'}`];
  if (pl.price != null) {
    out.push(`${tr(config, 'กด')} ${SOL_PROG[pl.prog] || pl.prog} → Price ${pl.price} → Start`);
    if (pl.extra > 0) out.push(`${tr(config, 'แล้วกด Extra Time')} +฿${pl.extra}`);
  } else {
    out.push(`Extra Time +฿${pl.extra}`);
  }
  out.push(tr(config, 'กลับมาแอป กด ✅'));
  return out;
}
// ผังเครื่องเหมือนหน้า Dashboard ของ SOL — ไฮไลต์เครื่องที่ต้องแตะรูป
function SolMiniMap({ config, machine }) {
  const map = config.pulse && config.pulse.solMap;
  if (!map) return null;
  const rows = [map.top, map.bottom].filter(Boolean);
  const cols = Math.max(...rows.map(r => r.length));
  return (
    <div className="mt-1.5 rounded-lg p-1.5" style={{ background: '#FDF3E7' }} data-sol-map="1">
      {rows.map((r, ri) => (
        <div key={ri} className="grid gap-0.5 mt-0.5" style={{ gridTemplateColumns: `repeat(${cols}, minmax(0, 1fr))` }}>
          {Array.from({ length: cols }, (_, ci) => {
            const m = r[ci];
            if (!m) return <div key={ci} />;
            const on = m === machine;
            const dry = m[0] === 'D';
            return (
              <div key={ci} className="rounded text-center font-black leading-none" data-map-machine={m}
                style={{ fontSize: 10, padding: '4px 0', color: '#fff', background: dry ? '#E14D4D' : '#3B82F6', opacity: on ? 1 : 0.35, boxShadow: on ? '0 0 0 2px #F59E0B, 0 0 0 4px #0F172A' : 'none' }}>
                {m}{on ? <span className="block mt-0.5">👆</span> : null}
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}
// หน้าตาเหมือนหน้าต่าง Select Menu ของ SOL — แม่บ้านกดตามช่องที่ชี้ไว้
function SolDialogGuide({ config, p, copied, onCopy }) {
  const pl = solPlan(config, p);
  const lab = 'shrink-0 whitespace-nowrap text-[12px] font-bold text-slate-500';
  const labW = { width: 68 };
  const box = 'flex-1 min-w-0 rounded-lg border-2 border-slate-300 px-2 py-1 text-lg font-black leading-tight';
  return (
    <div className="mt-2 rounded-xl bg-white text-slate-900 p-2.5" data-sol-guide="1">
      <p className="text-[12px] font-bold text-slate-500">① {tr(config, 'แตะรูปเครื่อง')} <span className="text-base font-black text-slate-900 px-1.5 rounded bg-amber-200">{p.machine}</span> → <span className="text-slate-900">{pl.price != null ? 'Select Menu' : 'Extra Time'}</span></p>
      <SolMiniMap config={config} machine={p.machine} />
      {pl.price != null ? (
        <>
          <p className="text-[12px] font-bold text-slate-500 mt-2">② {tr(config, 'กด')}</p>
          <div className="grid grid-cols-3 gap-1.5 mt-1">
            {pl.btns.map(([k, label, color]) => {
              const on = k === pl.prog;
              return (
                <div key={k} className="rounded-lg py-2 text-center text-sm font-extrabold text-white"
                  style={{ background: color, opacity: on ? 1 : 0.18, boxShadow: on ? '0 0 0 3px #0F172A' : 'none', textShadow: '0 1px 2px rgba(0,0,0,.35)' }}>
                  {on ? '👉 ' : ''}{label}
                </div>
              );
            })}
          </div>
          <div className="flex items-center gap-2 mt-2"><span className={lab} style={labW}>③ Price</span><span className={box}>{pl.price}</span></div>
          <p className="text-[11px] text-slate-500 mt-0.5" style={{ paddingLeft: 76 }}>{tr(config, 'ขึ้นเองหลังกดปุ่ม — ถ้าไม่ใช่')} {pl.price} {tr(config, 'ให้แก้เป็น')} {pl.price}</p>
        </>
      ) : (
        <p className="text-sm font-extrabold mt-2">② {tr(config, 'เติมเวลา')} +฿{pl.extra}</p>
      )}
      <div className="flex items-center gap-2 mt-1.5">
        <span className={lab} style={labW}>{pl.price != null ? '④' : '③'} Note<span className="block text-[10px] font-normal">{tr(config, 'ไม่บังคับ')}</span></span>
        <span className={box}>{p.code}</span>
        <button onClick={onCopy} className="shrink-0 px-2.5 py-1.5 rounded-lg bg-slate-900 text-white text-xs font-extrabold active:scale-95">{copied ? `✓ ${tr(config, 'คัดลอกแล้ว')}` : `📋 ${tr(config, 'คัดลอก')} ${p.code}`}</button>
      </div>
      <p className="text-[12px] font-bold text-slate-500 mt-2">{pl.price != null ? '⑤' : '④'} {tr(config, 'กด')} <span className="inline-block px-3 py-0.5 rounded-md text-white font-extrabold" style={{ background: '#2563EB' }}>Start</span>
        {pl.price != null && pl.extra > 0 && <span className="text-slate-900"> → {tr(config, 'แล้วกด')} Extra Time +฿{pl.extra}</span>}
      </p>
    </div>
  );
}

function SolPendingBar({ config }) {
  const [list, setList] = useState(() => solPendingList(config));
  const [busy, setBusy] = useState(false);
  const [copied, setCopied] = useState(false);
  useEffect(() => {
    const f = () => setList(solPendingList(config));
    window.addEventListener('sol-pending', f);
    window.addEventListener('storage', f);
    return () => { window.removeEventListener('sol-pending', f); window.removeEventListener('storage', f); };
  }, [config.brand]);
  const [toast, setToast] = useState(null);
  useEffect(() => {
    let tm = null;
    const f = (e) => { setToast(e.detail); clearTimeout(tm); tm = setTimeout(() => setToast(null), 2600); };
    window.addEventListener('sol-done', f);
    return () => { window.removeEventListener('sol-done', f); clearTimeout(tm); };
  }, []);
  const toastEl = toast ? (
    <div className="fixed left-0 right-0 flex justify-center pointer-events-none" style={{ zIndex: 71, bottom: list.length ? 360 : 24 }} data-sol-toast="1">
      <div className={`m-2 px-4 py-3 rounded-2xl shadow-2xl font-extrabold text-white text-center ${toast.ok ? 'bg-emerald-600' : 'bg-slate-700'}`}>{toast.text}</div>
    </div>
  ) : null;
  if (!list.length) return toastEl;
  const p = list[list.length - 1];
  const copy = async () => {
    try { await navigator.clipboard.writeText(p.code); setCopied(true); setTimeout(() => setCopied(false), 1500); }
    catch (e) { prompt(tr(config, 'คัดลอกข้อความนี้'), p.code); }
  };
  const done = async () => {
    if (busy) return;
    setBusy(true);
    try {
      await firePulse(config, {
        machine: p.machine, pulses: Math.round(p.baht / PULSE_BAHT), refType: p.refType, refId: p.orderId, slotKey: null, refLabel: p.refLabel,
        meta: { kind: p.kind, kg: p.kg, temp: p.temp || null, heat: p.heat || null, dryMin: null, mismatch: p.warn || null, discBaht: p.discBaht || null, solCode: p.code },
      });
      solPendingRemove(config, p.key);
      playSuccessSound();
      solNotify({ ok: true, text: `✅ ${p.machineLabel} — ${tr(config, 'บันทึกแล้ว · เครื่องเริ่มทำงาน')}` });
    } catch (e) { alert(tr(config, 'บันทึกไม่สำเร็จ') + ': ' + (e && e.message ? e.message : e)); }
    setBusy(false);
  };
  const cancel = () => {
    if (confirm(`${tr(config, 'ยกเลิกรายการนี้? (ยังไม่ได้กด Start ใน SOL)')}\n\n🧺 ${p.machineLabel} · ${p.refLabel}`)) {
      solPendingRemove(config, p.key);
      solNotify({ ok: null, text: `${tr(config, 'ยกเลิกแล้ว')} · ${p.machineLabel}` });
    }
  };
  return (
    <>{toastEl}
    <div className="fixed left-0 right-0 bottom-0 flex justify-center pointer-events-none" style={{ zIndex: 70 }}>
      <div className="w-full max-w-md m-2 rounded-2xl bg-slate-900 text-white shadow-2xl p-3 pointer-events-auto" data-sol-bar="1">
        <div className="flex items-center gap-2">
          <span className="text-[11px] font-extrabold px-2 py-0.5 rounded-full bg-sky-500">SOL</span>
          <p className="flex-1 min-w-0 font-extrabold truncate">{tr(config, 'รอกด Start')} · {p.machineLabel} · ฿{p.baht}</p>
          {list.length > 1 && <span className="text-xs font-bold text-amber-300">+{list.length - 1} {tr(config, 'รายการ')}</span>}
        </div>
        <p className="text-xs text-slate-300 mt-0.5 truncate">{p.refLabel}</p>
        <SolDialogGuide config={config} p={p} copied={copied} onCopy={copy} />
        <a href={config.pulse.solUrl} target="_blank" rel="noopener noreferrer" className="block mt-2 py-2.5 rounded-xl bg-sky-500 text-white font-extrabold text-sm text-center active:scale-95">↗ {tr(config, 'เปิด SOL')} → 👆 {p.machine}</a>
        <div className="grid grid-cols-3 gap-2 mt-2">
          <button onClick={cancel} disabled={busy} className="py-3 rounded-xl bg-slate-700 font-bold text-sm active:scale-95">{tr(config, 'ยกเลิก')}</button>
          <button onClick={done} disabled={busy} className="col-span-2 py-3 rounded-xl bg-emerald-500 font-extrabold active:scale-95 disabled:opacity-50">{busy ? '⏳' : `✅ ${tr(config, 'กด Start ใน SOL แล้ว')}`}</button>
        </div>
      </div>
    </div>
    </>
  );
}

// เครื่องแบบตาราง (ร้านที่ไม่ได้วางเครื่องเป็นแท่นอบบน-ซักล่าง เช่น Otteri)
function MachineGrid({ config, machines, marks, selected, onPick, problems }) {
  const rows = [['wash', '💧 ' + tr(config, 'เครื่องซัก'), '#113D6C'], ['dry', '🌬️ ' + tr(config, 'เครื่องอบ'), '#BA3D4D']];
  return (
    <div className="space-y-2">
      {rows.map(([kind, title, color]) => {
        const list = machines.filter(m => m.kind === kind);
        if (!list.length) return null;
        return (
          <div key={kind}>
            <p className="text-xs font-extrabold text-slate-600 mb-1 px-1">{title}</p>
            <div className="grid grid-cols-4 gap-1.5">
              {list.map(m => {
                const mk = marks[m.id];
                const sel = selected === m.id;
                return (
                  <button key={m.id} onClick={() => onPick(m)} data-machine={m.id}
                    className={`relative rounded-xl py-2 px-1 text-center border-2 active:scale-95 transition ${mk === 'dim' && !sel ? 'opacity-40' : ''}`}
                    style={{ background: sel ? color : '#fff', color: sel ? '#fff' : '#0F172A', borderColor: sel ? color : mk === 'target' ? '#C68B4A' : '#E2E8F0' }}>
                    <span className="block text-base font-extrabold leading-tight">{m.id}</span>
                    <span className="block text-[11px] font-bold" style={{ opacity: 0.75 }}>{m.kg}kg</span>
                    {mk === 'done' && <span className="absolute -top-1.5 -right-1.5 text-sm">✅</span>}
                    {mk === 'busy' && <span className="absolute -top-1.5 -right-1.5 text-sm">⏳</span>}
                    {problems && problems.has(m.id) && <span className="absolute -top-1.5 -left-1.5 w-4 h-4 rounded-full bg-red-600 text-white text-[10px] font-black" style={{ lineHeight: '16px' }}>!</span>}
                  </button>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
}

// ⚙️ ตั้งค่า (เจ้าของ) — โหมด SOL
function SolSettingsCard({ config }) {
  const on = pulseOn(config);
  // เวลาเริ่มนับใบงาน = เวลาเข้างานแม่บ้าน (ค่าเริ่มต้น 09:00) — ถ้ายังไม่ถึงเวลา ใช้เวลาตอนกด
  const startHour = (config.pulse && config.pulse.dayStartHour != null) ? config.pulse.dayStartHour : 9;
  const hhmm = String(startHour).padStart(2, '0') + ':00';
  const today0 = (() => { const d = new Date(); d.setHours(startHour, 0, 0, 0); return Math.min(d.getTime(), Date.now()); })();
  const toggle = async () => {
    if (!on && !confirm('เปิดระบบเริ่มเครื่องผ่าน SOL?\n\n• แม่บ้านใช้บัญชี SOL ของตัวเอง (สิทธิ์ Wash Dry Fold)\n• กดเริ่มในแอป → ไปกด Start ใน SOL → กลับมากด ✅\n• กระทบยอด: เจ้าของใส่ยอด WDF จากหน้า Dashboard ของ SOL\n• นับใบงานตั้งแต่ ' + hhmm + ' วันนี้ (เวลาเข้างานแม่บ้าน)')) return;
    try {
      // เปิดครั้งแรก = นับใบงานตั้งแต่เวลาเข้างานวันนี้ (ใบที่รับก่อนเปิดสวิตช์ก็ขึ้นให้เริ่มเครื่อง)
      await saveShopSettings(config.brand, on ? { pulseEnabled: false } : { pulseEnabled: true, pulseSinceMs: pulseSinceOf(config) || today0 });
    } catch (e) { alert('บันทึกไม่สำเร็จ: ' + (e && e.message ? e.message : e)); }
  };
  const fromToday = async () => {
    if (!confirm('นับใบงานตั้งแต่ ' + hhmm + ' วันนี้?\n\nใบงานที่รับวันนี้ก่อนเปิดสวิตช์ จะขึ้นในรายการรอเริ่มเครื่องและในกระทบยอด')) return;
    try { await saveShopSettings(config.brand, { pulseSinceMs: today0 }); } catch (e) { alert('บันทึกไม่สำเร็จ: ' + (e && e.message ? e.message : e)); }
  };
  return (
    <div className="bg-white rounded-2xl p-4 border border-slate-200">
      <p className="text-sm font-bold text-slate-800 mb-2">🟦 เริ่มเครื่องผ่าน SOL (บันทึกในแอป)</p>
      <button onClick={toggle}
        className={`w-full py-2.5 rounded-xl text-sm font-bold border-2 flex items-center justify-between px-3 active:scale-95 transition ${on ? 'bg-emerald-50 border-emerald-300 text-emerald-800' : 'bg-slate-100 border-slate-300 text-slate-500'}`}>
        <span>{on ? '✅ เปิดอยู่' : '⛔ ปิดอยู่'}</span>
        <span>แตะเพื่อ{on ? 'ปิด' : 'เปิด'}</span>
      </button>
      <p className="text-[11px] text-slate-400 mt-1.5">เปิดแล้ว: หน้าแรกมีปุ่ม 🧺 เริ่มเครื่อง · ใบงานโอน = กดใน SOL · ใบงานเงินสด = หยอดเหรียญที่เครื่อง</p>
      {pulseSinceOf(config) > 0 && <p className="text-[11px] text-slate-400">เริ่มกระทบยอดตั้งแต่ {formatDate(pulseSinceOf(config))}</p>}
      {on && pulseSinceOf(config) > today0 && (
        <button onClick={fromToday} className="w-full mt-2 py-2 rounded-xl text-sm font-bold bg-sky-50 border border-sky-300 text-sky-800 active:scale-95">📅 นับใบงานตั้งแต่ {hhmm} วันนี้</button>
      )}
    </div>
  );
}

// ใส่ยอด WDF จาก SOL (เจ้าของ) → ใช้เทียบกับยอดที่แม่บ้านติ๊กในแอป
function SolWdfInput({ config, dateKey, current }) {
  const [v, setV] = useState('');
  const [saving, setSaving] = useState(false);
  const save = async () => {
    const n = Number(String(v).replace(/[^\d.]/g, ''));
    if (!(n >= 0) || v === '') { alert('ใส่ตัวเลขยอด WDF ก่อน'); return; }
    setSaving(true);
    try {
      await window.db.collection('pulseDayNotes').doc(config.brand + '_' + dateKey).set({ brand: config.brand, dateKey, solWdf: Math.round(n), solWdfAt: Date.now(), updatedAt: Date.now() }, { merge: true });
      setV('');
      playSuccessSound();
    } catch (e) { alert('บันทึกไม่สำเร็จ: ' + (e && e.message ? e.message : e)); }
    setSaving(false);
  };
  return (
    <div className="rounded-2xl p-3 bg-sky-50 border border-sky-200">
      <p className="text-sm font-extrabold text-sky-900">🟦 ยอด WDF จาก SOL{current != null ? ` · ใส่แล้ว ฿${formatMoney(current)}` : ''}</p>
      <p className="text-[11px] text-sky-800">เปิด SOL → Dashboard → Income → ตัวเลขช่อง WDF ของวันนี้</p>
      <div className="flex gap-2 mt-2">
        <input value={v} onChange={e => setV(e.target.value)} inputMode="numeric" placeholder={current != null ? String(current) : 'เช่น 260'}
          className="flex-1 min-w-0 px-3 py-2.5 rounded-xl border border-sky-300 bg-white text-lg font-bold" />
        <button onClick={save} disabled={saving} className="px-4 rounded-xl bg-sky-600 text-white font-extrabold active:scale-95 disabled:opacity-50">{saving ? '⏳' : 'บันทึก'}</button>
      </div>
    </div>
  );
}
const solEcFromNote = (note) => (note && note.solWdf != null ? { sol: true, at: note.solWdfAt || 0, solWdf: note.solWdf } : null);

