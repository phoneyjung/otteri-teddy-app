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

// ขั้นตอนที่หน้าเว็บ SOL ของเครื่องนั้น
function solSteps(config, p) {
  const out = [`${tr(config, 'เปิด SOL → แตะ ⚙️ ที่เครื่อง')} ${p.machine}`];
  if (p.kind === 'wash') {
    out.push(`${tr(config, 'เลือก')} ${SOL_PROG[p.temp] || p.temp || '-'} (${p.progLabel || ''})`);
  } else {
    const base = dryPriceFor(config, p.kg);
    const heat = SOL_PROG[p.heat] || 'High';
    if (p.baht >= base && base > 0) {
      out.push(`${tr(config, 'เลือก')} ${heat} → ${tr(config, 'ราคา')} ฿${base}`);
      if (p.baht > base) out.push(`${tr(config, 'กด Start แล้วเพิ่มเวลา (Extra)')} +฿${p.baht - base}`);
    } else {
      out.push(`${tr(config, 'เพิ่มเวลา (Extra)')} +฿${p.baht}`);
    }
  }
  out.push(`${tr(config, 'ช่อง Note ใส่')} ${p.code} → ${tr(config, 'กด Start')}`);
  out.push(tr(config, 'กลับมาแอป กด ✅'));
  return out;
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
  if (!list.length) return null;
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
    } catch (e) { alert(tr(config, 'บันทึกไม่สำเร็จ') + ': ' + (e && e.message ? e.message : e)); }
    setBusy(false);
  };
  const cancel = () => {
    if (confirm(`${tr(config, 'ยกเลิกรายการนี้? (ยังไม่ได้กด Start ใน SOL)')}\n\n🧺 ${p.machineLabel} · ${p.refLabel}`)) solPendingRemove(config, p.key);
  };
  return (
    <div className="fixed left-0 right-0 bottom-0 flex justify-center pointer-events-none" style={{ zIndex: 70 }}>
      <div className="w-full max-w-md m-2 rounded-2xl bg-slate-900 text-white shadow-2xl p-3 pointer-events-auto" data-sol-bar="1">
        <div className="flex items-center gap-2">
          <span className="text-[11px] font-extrabold px-2 py-0.5 rounded-full bg-sky-500">SOL</span>
          <p className="flex-1 min-w-0 font-extrabold truncate">{tr(config, 'รอกด Start')} · {p.machineLabel} · ฿{p.baht}</p>
          {list.length > 1 && <span className="text-xs font-bold text-amber-300">+{list.length - 1} {tr(config, 'รายการ')}</span>}
        </div>
        <p className="text-xs text-slate-300 mt-0.5 truncate">{p.refLabel}</p>
        <ol className="text-[13px] mt-2 space-y-0.5 list-decimal pl-5 leading-snug">
          {solSteps(config, p).map((s, i) => <li key={i}>{s}</li>)}
        </ol>
        <div className="grid grid-cols-2 gap-2 mt-2.5">
          <button onClick={copy} className="py-2.5 rounded-xl bg-white text-slate-900 font-extrabold text-sm active:scale-95">{copied ? `✓ ${tr(config, 'คัดลอกแล้ว')}` : `📋 ${tr(config, 'คัดลอก')} ${p.code}`}</button>
          <a href={config.pulse.solUrl} target="_blank" rel="noopener noreferrer" className="py-2.5 rounded-xl bg-sky-500 text-white font-extrabold text-sm text-center active:scale-95">↗ {tr(config, 'เปิด SOL')}</a>
        </div>
        <div className="grid grid-cols-3 gap-2 mt-2">
          <button onClick={cancel} disabled={busy} className="py-3 rounded-xl bg-slate-700 font-bold text-sm active:scale-95">{tr(config, 'ยกเลิก')}</button>
          <button onClick={done} disabled={busy} className="col-span-2 py-3 rounded-xl bg-emerald-500 font-extrabold active:scale-95 disabled:opacity-50">{busy ? '⏳' : `✅ ${tr(config, 'กด Start ใน SOL แล้ว')}`}</button>
        </div>
      </div>
    </div>
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
  const today0 = (() => { const d = new Date(); d.setHours(0, 0, 0, 0); return d.getTime(); })();
  const toggle = async () => {
    if (!on && !confirm('เปิดระบบเริ่มเครื่องผ่าน SOL?\n\n• แม่บ้านใช้บัญชี SOL ของตัวเอง (สิทธิ์ Wash Dry Fold)\n• กดเริ่มในแอป → ไปกด Start ใน SOL → กลับมากด ✅\n• กระทบยอด: เจ้าของใส่ยอด WDF จากหน้า Dashboard ของ SOL\n• นับใบงานตั้งแต่เช้าวันนี้')) return;
    try {
      // เปิดครั้งแรก = นับใบงานตั้งแต่เช้าวันนี้ (ใบที่รับก่อนเปิดสวิตช์ก็ขึ้นให้เริ่มเครื่อง)
      await saveShopSettings(config.brand, on ? { pulseEnabled: false } : { pulseEnabled: true, pulseSinceMs: pulseSinceOf(config) || today0 });
    } catch (e) { alert('บันทึกไม่สำเร็จ: ' + (e && e.message ? e.message : e)); }
  };
  const fromToday = async () => {
    if (!confirm('นับใบงานตั้งแต่เช้าวันนี้ (00:00)?\n\nใบงานที่รับวันนี้ก่อนเปิดสวิตช์ จะขึ้นในรายการรอเริ่มเครื่องและในกระทบยอด')) return;
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
        <button onClick={fromToday} className="w-full mt-2 py-2 rounded-xl text-sm font-bold bg-sky-50 border border-sky-300 text-sky-800 active:scale-95">📅 นับใบงานตั้งแต่เช้าวันนี้</button>
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

