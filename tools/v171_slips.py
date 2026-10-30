#!/usr/bin/env python3
"""v171 — ใบรายงานเข้ากลุ่ม LINE สำหรับงานที่ไม่ใช่รับงานลูกค้า (ขายน้ำยา · ลูกค้าใช้โปร · ล้างเครื่อง/งานภายใน)
สีตามงาน + มุมขวาบนเป็นสีประจำร้าน (โลโก้ร้าน) · หลังบันทึกขึ้นใบ + ปุ่มส่งเข้ากลุ่มทันที · แตะรายการเก่าเปิดใบส่งซ้ำได้
usage: python3 tools/v171_slips.py index.html sw.js
"""
import sys

IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read()
sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    assert n == count, f'{label}: found {n}, expected {count}'
    s = s.replace(old, new)


# ---------- version ----------
rep("window.APP_VERSION = 'v170-2026-10-29';", "window.APP_VERSION = 'v171-2026-10-30';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v170';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v170';", "const CACHE_NAME = 'plp-laundry-v171';")

# ---------- MM (Burmese) — new maid-facing words ----------
rep("""  '💬 ส่งเข้ากลุ่ม LINE': '💬 LINE Group သို့ပို့ရန်',""",
    """  '💬 ส่งเข้ากลุ่ม LINE': '💬 LINE Group သို့ပို့ရန်',
  // 🧾 v171 ใบรายงานเข้ากลุ่ม
  'กำลังทำใบรายงาน…': 'အစီရင်ခံစာ ပြင်ဆင်နေသည်…',
  'แตะเพื่อเปิดใบรายงาน': 'အစီရင်ခံစာ ဖွင့်ရန် နှိပ်ပါ',
  'ใบรายงานนี้ส่งเข้ากลุ่ม ไม่ต้องส่งลูกค้า': 'ဤအစီရင်ခံစာကို Group သို့ပို့ပါ · ဖောက်သည်ထံ မပို့ရ',""", 'MM words')

# ---------- shared slip builder + card (global, before ReceiptView) ----------
rep("""function ReceiptView({ config, order, onBack, autoOpenTicket, onTicketOpened, isOwner, collections }) {""",
r"""// 🧾 v171 ใบรายงานเข้ากลุ่ม LINE — งานที่ไม่ใช่รับงานลูกค้า: หัวลายเฉียงสีตามงาน + มุมขวาบนสีประจำร้าน (โลโก้)
// วาดด้วย canvas (ภาพที่เห็น = ภาพที่ส่ง) · ข้อความในภาพเป็นภาษาไทย (เจ้าของอ่านในกลุ่ม)
const SLIP_KINDS = {
  clean: { c: '#F59E0B', c2: '#92400E', t: '#FFFBEB', emoji: '🧼', title: 'ล้างเครื่อง', sub: 'งานภายในร้าน · ไม่นับรายได้' },
  mine: { c: '#6366F1', c2: '#3730A3', t: '#EEF2FF', emoji: '👔', title: 'ผ้าเจ้าของ', sub: 'ฟรี · ไม่นับรายได้' },
  internal: { c: '#64748B', c2: '#1E293B', t: '#F1F5F9', emoji: '🔧', title: 'งานภายใน', sub: 'งานภายในร้าน · ไม่นับรายได้' },
  promo: { c: '#F43F5E', c2: '#9F1239', t: '#FFF1F2', emoji: '🎟️', title: 'ลูกค้าใช้โปร', sub: 'ลูกค้าซักเอง ไม่ฝาก' },
  detergent: { c: '#8B5CF6', c2: '#4C1D95', t: '#F5F3FF', emoji: '🧴', title: 'ขายน้ำยา', sub: 'ไม่ใช่รับงาน · ไม่ต้องเริ่มเครื่อง' },
};
const slipWhen = (ts) => {
  const d = new Date(ts || Date.now());
  return d.toLocaleDateString('th-TH', { weekday: 'short', day: 'numeric', month: 'short', year: '2-digit' }) + ' · ' + d.toTimeString().slice(0, 5);
};
// s = { kind, emoji?, title?, sub?, rows: [[label, value]], foot, photo?, at, staff, no? }
async function buildReportSlip(config, s) {
  const K = Object.assign({}, SLIP_KINDS[s.kind] || SLIP_KINDS.internal, s.emoji ? { emoji: s.emoji } : {}, s.title ? { title: s.title } : {}, s.sub ? { sub: s.sub } : {});
  const FONT = '"Noto Sans Thai", sans-serif';
  try { await Promise.all(['800 64px', '700 30px', '400 28px'].map(f => document.fonts.load(f + ' "Noto Sans Thai"'))); } catch (e) {}
  const loadImg = (src) => new Promise(res => { if (!src) return res(null); const im = new Image(); im.onload = () => res(im); im.onerror = () => res(null); im.src = src; });
  const [logo, photo] = await Promise.all([loadImg(config.logo), loadImg(s.photo)]);
  const W = 720, P = 36, headH = 262, metaH = 112, rowH = 66, footH = 96, photoH = photo ? 400 : 0;
  const rows = (s.rows || []).filter(r => r && r[1] != null && r[1] !== '');
  const H = headH + metaH + (photo ? photoH + 28 : 0) + 18 + rows.length * rowH + 26 + footH + 34 + 22;
  const cv = document.createElement('canvas');
  cv.width = W; cv.height = H;
  const x = cv.getContext('2d');
  const rr = (X, Y, w, h, r) => { x.beginPath(); x.moveTo(X + r, Y); x.arcTo(X + w, Y, X + w, Y + h, r); x.arcTo(X + w, Y + h, X, Y + h, r); x.arcTo(X, Y + h, X, Y, r); x.arcTo(X, Y, X + w, Y, r); x.closePath(); };
  const fit = (txt, weight, size, maxW) => { let z = size; do { x.font = `${weight} ${z}px ${FONT}`; z -= 2; } while (x.measureText(txt).width > maxW && z > 18); return x.font; };
  x.fillStyle = '#FFFFFF'; x.fillRect(0, 0, W, H);
  // หัว: ลายเฉียงสีตามงาน
  x.fillStyle = K.c; x.fillRect(0, 0, W, headH);
  x.save(); x.beginPath(); x.rect(0, 0, W, headH); x.clip(); x.fillStyle = 'rgba(255,255,255,0.17)';
  for (let i = -headH; i < W + headH; i += 72) { x.beginPath(); x.moveTo(i, 0); x.lineTo(i + 36, 0); x.lineTo(i + 36 - headH, headH); x.lineTo(i - headH, headH); x.closePath(); x.fill(); }
  x.restore();
  // มุมขวาบน: สีประจำร้าน + โลโก้
  const cs = 214, brand = config.primaryColor || '#0EA5E9';
  x.fillStyle = brand; x.beginPath(); x.moveTo(W - cs, 0); x.lineTo(W, 0); x.lineTo(W, cs); x.closePath(); x.fill();
  x.strokeStyle = '#FFFFFF'; x.lineWidth = 7; x.beginPath(); x.moveTo(W - cs - 4, -4); x.lineTo(W + 4, cs + 4); x.stroke();
  if (logo) {
    const cx = W - 64, cy = 64, r = 46;
    x.fillStyle = '#FFFFFF'; x.beginPath(); x.arc(cx, cy, r + 5, 0, Math.PI * 2); x.fill();
    x.save(); x.beginPath(); x.arc(cx, cy, r, 0, Math.PI * 2); x.clip(); x.drawImage(logo, cx - r, cy - r, r * 2, r * 2); x.restore();
  }
  // ป้าย "ไม่ใช่ใบรับงานลูกค้า"
  const tag = 'ใบรายงานเข้ากลุ่ม · ไม่ใช่ใบรับงานลูกค้า';
  x.font = `700 23px ${FONT}`;
  const tw = x.measureText(tag).width + 36;
  x.fillStyle = K.c2; rr(P - 8, 26, tw, 44, 22); x.fill();
  x.fillStyle = '#FFFFFF'; x.textBaseline = 'middle'; x.fillText(tag, P + 10, 49);
  // ชื่องาน
  const title = `${K.emoji} ${K.title}`;
  x.font = fit(title, 800, 66, W - P - cs + 10);
  x.fillStyle = 'rgba(0,0,0,0.18)'; x.textBaseline = 'alphabetic'; x.fillText(title, P + 2, 168 + 3);
  x.fillStyle = '#FFFFFF'; x.fillText(title, P, 168);
  x.font = fit(K.sub, 700, 28, W - 2 * P); x.fillText(K.sub, P, 222);
  // แถวร้าน · เวลา · แม่บ้าน
  let y = headH;
  x.fillStyle = K.t; x.fillRect(0, y, W, metaH);
  x.fillStyle = '#0F172A'; x.font = `800 32px ${FONT}`; x.fillText(config.name || '', P, y + 46);
  x.fillStyle = '#475569'; x.font = fit(`${slipWhen(s.at)}${s.staff ? ' · 🧕 ' + s.staff : ''}`, 400, 25, W - 2 * P - 120); x.fillText(`${slipWhen(s.at)}${s.staff ? ' · 🧕 ' + s.staff : ''}`, P, y + 86);
  if (s.no) { x.fillStyle = K.c2; x.font = `800 36px ${FONT}`; x.textAlign = 'right'; x.fillText(s.no, W - P, y + 66); x.textAlign = 'left'; }
  x.strokeStyle = K.c; x.lineWidth = 3; x.setLineDash([12, 9]); x.beginPath(); x.moveTo(0, y + metaH - 1); x.lineTo(W, y + metaH - 1); x.stroke(); x.setLineDash([]);
  y += metaH;
  // รูปหลักฐาน
  if (photo) {
    y += 28;
    const bw = W - 2 * P, bh = photoH, sc = Math.max(bw / photo.width, bh / photo.height);
    const sw2 = bw / sc, sh2 = bh / sc;
    x.save(); rr(P, y, bw, bh, 22); x.clip();
    x.drawImage(photo, (photo.width - sw2) / 2, (photo.height - sh2) / 2, sw2, sh2, P, y, bw, bh);
    x.restore();
    y += bh;
  }
  // รายการ
  y += 18;
  rows.forEach(([k, v], i) => {
    x.fillStyle = '#64748B'; x.font = `400 28px ${FONT}`; x.fillText(String(k), P, y + 44);
    x.fillStyle = '#0F172A'; x.font = fit(String(v), 700, 30, W - 2 * P - x.measureText(String(k)).width - 30); x.textAlign = 'right'; x.fillText(String(v), W - P, y + 44); x.textAlign = 'left';
    if (i < rows.length - 1) { x.fillStyle = '#F1F5F9'; x.fillRect(P, y + rowH - 1, W - 2 * P, 2); }
    y += rowH;
  });
  // กล่องท้าย
  y += 26;
  x.fillStyle = K.t; rr(P - 10, y, W - 2 * P + 20, footH, 24); x.fill();
  x.strokeStyle = K.c; x.lineWidth = 5; rr(P - 10, y, W - 2 * P + 20, footH, 24); x.stroke();
  x.fillStyle = K.c2; x.font = fit(s.foot || '', 800, 40, W - 2 * P - 20); x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(s.foot || '', W / 2, y + footH / 2 + 2);
  x.textAlign = 'left'; x.textBaseline = 'alphabetic';
  // ขอบล่างสีประจำร้าน
  x.fillStyle = brand; x.fillRect(0, H - 22, W, 22);
  return cv.toDataURL('image/png');
}
async function shareReportSlip(config, dataUrl, name, slug) {
  if (!dataUrl) return;
  try {
    const bin = atob(dataUrl.split(',')[1] || ''); const arr = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
    const file = new File([arr], `${config.brand}-${slug || 'report'}-${Date.now()}.png`, { type: 'image/png' }); // ชื่อไฟล์ภาษาอังกฤษล้วน (ไทยเปิดไม่ได้บางเครื่อง)
    if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) { await navigator.share({ files: [file], title: name }); return; }
    const a = document.createElement('a'); a.href = dataUrl; a.download = file.name; document.body.appendChild(a); a.click(); a.remove();
  } catch (e) { /* ผู้ใช้กดยกเลิกแชร์ */ }
}
function ReportSlipCard({ config, slip, slipKey, name, hideButton, onUrl }) {
  const [url, setUrl] = useState(null);
  const [busy, setBusy] = useState(false);
  useEffect(() => {
    let alive = true;
    setUrl(null); if (onUrl) onUrl(null);
    buildReportSlip(config, slip).then(u => { if (alive) { setUrl(u); if (onUrl) onUrl(u); } }).catch(() => {});
    return () => { alive = false; };
  }, [slipKey]);
  return (
    <div data-report-slip={slip.kind}>
      {url ? <img src={url} alt={name} className="w-full rounded-2xl shadow-md border border-slate-200 block" />
        : <div className="h-48 rounded-2xl bg-slate-100 border border-slate-200 flex items-center justify-center text-sm font-bold text-slate-400">{tr(config, 'กำลังทำใบรายงาน…')}</div>}
      {!hideButton && (
        <button onClick={async () => { setBusy(true); await shareReportSlip(config, url, name, slip.kind); setBusy(false); }} disabled={!url || busy}
          className="w-full mt-2 py-3 rounded-2xl text-white font-extrabold active:scale-95 transition disabled:opacity-50" style={{ background: 'linear-gradient(135deg, #06C755, #00B900)' }}>
          {tr(config, '💬 ส่งเข้ากลุ่ม LINE')}
        </button>
      )}
    </div>
  );
}
// ใบรายงานของงานภายใน (ล้างเครื่อง / ผ้าเจ้าของ / ซ่อม-ทดสอบ …)
function internalSlipOf(config, order, total) {
  const it = INTERNAL_TYPES.find(t => t.id === order.internalType) || {};
  const kind = order.internalType === 'clean' ? 'clean' : (order.internalType === 'mine' ? 'mine' : 'internal');
  const tl = { cold: 'น้ำเย็น', warm: 'น้ำอุ่น', hot: 'น้ำร้อน' };
  const rows = [];
  if (order.internalMachines && order.internalMachines.length) rows.push(['เครื่อง', order.internalMachines.join(' · ')]);
  (order.washItems || []).forEach(w => rows.push([`ซัก ${w.size} kg`, `${tl[w.temp || 'cold'] || ''} × ${w.qty}`]));
  (order.dryItems || []).forEach(d => rows.push([`อบ ${d.size} kg`, `× ${d.qty}`]));
  if (total > 0) rows.push(['เครดิตที่ใช้', `฿${formatMoney(total)}`]);
  if (order.internalReason) rows.push(['หมายเหตุ', order.internalReason]);
  return {
    kind, emoji: kind === 'internal' ? it.emoji : null, title: kind === 'internal' ? (it.label || order.internalType) : null,
    rows, foot: kind === 'mine' ? '👔 ผ้าเจ้าของ · ฟรี · ไม่ใช่รายได้' : '🔧 งานภายใน · ไม่ใช่รายได้',
    at: order.createdAt, staff: order.staffName || order.createdByName || '', no: order.queueNo != null ? '#' + String(order.queueNo).padStart(2, '0') : '',
  };
}

function ReceiptView({ config, order, onBack, autoOpenTicket, onTicketOpened, isOwner, collections }) {""", 'slip builder')

# ---------- internal job receipt → slip ----------
rep("""  const internal = isInternalOrder(order); // 🔧 งานภายใน — ต้องประกาศบนสุด (useEffect ด้านล่างใช้)
  const orderPhotos = useOrderPhotos(order);""",
    """  const internal = isInternalOrder(order); // 🔧 งานภายใน — ต้องประกาศบนสุด (useEffect ด้านล่างใช้)
  const [slipUrl, setSlipUrl] = useState(null); // 🧾 v171 ใบรายงานงานภายใน
  const orderPhotos = useOrderPhotos(order);""", 'slip state')
rep("""        <div ref={receiptRef} className="bg-white rounded-2xl overflow-hidden shadow-lg" style={{fontFamily: '"Noto Sans Thai", sans-serif'}}>""",
    """        {internal && (
          <ReportSlipCard config={config} slip={internalSlipOf(config, order, total)} slipKey={(order.id || '') + ':' + (order.createdAt || 0) + ':' + total} name={'งานภายใน'} hideButton onUrl={setSlipUrl} />
        )}
        {!internal && <div ref={receiptRef} className="bg-white rounded-2xl overflow-hidden shadow-lg" style={{fontFamily: '"Noto Sans Thai", sans-serif'}}>""", 'receipt card open')
rep("""          <div className="h-1.5" style={{ background: headerStripe }}></div>
        </div>
      </div>

      {/* ===== ใบงาน 80mm (thermal) — modal ดูตัวอย่าง + ปุ่ม ===== */}""",
    """          <div className="h-1.5" style={{ background: headerStripe }}></div>
        </div>}
      </div>

      {/* ===== ใบงาน 80mm (thermal) — modal ดูตัวอย่าง + ปุ่ม ===== */}""", 'receipt card close')
rep("""            <button onClick={handleShare} disabled={saving} className="py-3 rounded-xl font-bold text-white flex items-center justify-center gap-1.5 active:scale-95 transition disabled:opacity-50" style={{background: 'linear-gradient(135deg, #06C755, #00B900)'}}>
              <span className="text-lg">📤</span>
              <span className="text-sm">ส่งเข้ากลุ่ม</span>
            </button>
            <p className="col-span-2 text-center text-xs text-slate-400">🔧 งานภายใน — ส่งเข้ากลุ่มเพื่อรายงาน (ไม่ต้องส่งลูกค้า)</p>""",
    """            <button onClick={() => shareReportSlip(config, slipUrl, 'งานภายใน', 'internal-' + (order.internalType || ''))} disabled={!slipUrl} data-slip-share="internal" className="py-3 rounded-xl font-bold text-white flex items-center justify-center gap-1.5 active:scale-95 transition disabled:opacity-50" style={{background: 'linear-gradient(135deg, #06C755, #00B900)'}}>
              <span className="text-lg">📤</span>
              <span className="text-sm">{tr(config, 'ส่งเข้ากลุ่ม')}</span>
            </button>
            <p className="col-span-2 text-center text-xs text-slate-400">🔧 {tr(config, 'ใบรายงานนี้ส่งเข้ากลุ่ม ไม่ต้องส่งลูกค้า')}</p>""", 'internal share button')

# ---------- 🎟️ ลูกค้าใช้โปร: modal หลังบันทึก → ใบรายงานสีแดงชมพู ----------
rep("""            <p className="text-sm text-slate-600 mt-1">{savedPromo.promoName} · <b>{savedPromo.amount}฿</b></p>
            <p className="text-xs text-slate-500">🧕 {savedPromo.staffName}{savedPromo.machine ? ` · 🧺 ${savedPromo.machine}` : ''}</p>
            <img src={savedPromo.photo} className="w-full h-32 object-cover rounded-xl mt-3 border border-slate-200" alt="" />
            <button onClick={handleSharePromo} className="w-full mt-4 py-3 rounded-2xl bg-emerald-500 text-white font-bold active:scale-95 transition">{tr(config, "💬 ส่งเข้ากลุ่ม LINE")}</button>
            <button onClick={() => setSavedPromo(null)} className="mt-2 text-xs text-slate-400">{tr(config, "ปิด")}</button>""",
    """            <div className="mt-3 text-left">
              <ReportSlipCard config={config} name="ลูกค้าใช้โปร" slipKey={String(savedPromo.createdAt || '') + ':' + (savedPromo.pulseStatus || '')}
                slip={{ kind: 'promo', photo: savedPromo.photo, at: savedPromo.createdAt, staff: savedPromo.staffName,
                  rows: [['โปร', savedPromo.promoName], ['เครื่อง', savedPromo.machine || ''],
                    savedPromo.pulseLogId ? ['เริ่มเครื่อง', savedPromo.pulseStatus === 'confirmed' ? '⚡ เครื่องรับแล้ว' : '⚡ ส่งคำสั่งแล้ว'] : ['ตัดเครดิต', `${savedPromo.amount}฿`],
                    ['หมายเหตุ', savedPromo.note || '']],
                  foot: `ยอดโปร ${savedPromo.amount}฿` }} />
            </div>
            <button onClick={() => setSavedPromo(null)} className="mt-2 text-xs text-slate-400">{tr(config, "ปิด")}</button>""", 'promo modal slip')
rep("""          <div className="bg-white rounded-3xl w-full max-w-xs p-5 text-center" onClick={e => e.stopPropagation()}>
            <p className="text-4xl mb-1">✅</p>""",
    """          <div className="bg-white rounded-3xl w-full max-w-xs p-5 text-center max-h-[92vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
            <p className="text-4xl mb-1">✅</p>""", 'promo modal scroll')

# ---------- 🧴 ขายน้ำยา: หลังบันทึก + แตะรายการเก่า → ใบรายงานสีม่วง ----------
rep("""              <p className="text-xs font-bold text-slate-500 mt-1">{t2DetItems(config, done)}</p>
              <div className="grid grid-cols-2 gap-2 mt-3">""",
    """              <p className="text-xs font-bold text-slate-500 mt-1">{t2DetItems(config, done)}</p>
              <div className="mt-3 text-left">
                <ReportSlipCard config={config} name="ขายน้ำยา" slipKey={done.id || String(done.createdAt)}
                  slip={{ kind: 'detergent', at: done.createdAt, staff: done.staffName,
                    rows: [['🧴 น้ำยาซัก', done.detergentQty ? `× ${done.detergentQty}` : ''], ['🌸 น้ำยาปรับผ้านุ่ม', done.softenerQty ? `× ${done.softenerQty}` : ''],
                      ['ลูกค้าจ่าย', done.paymentMethod === 'transfer' ? '💳 โอน' : '💵 เงินสด']],
                    foot: `รวม ฿${formatMoney(done.amount || 0)}` }} />
              </div>
              <div className="grid grid-cols-2 gap-2 mt-3">""", 'detergent slip')
rep("""                      <button onClick={() => { if (tr2) setDone(t); }} className="flex-1 min-w-0 text-left">
                        <span className="block text-sm font-bold text-slate-900 truncate">{t2DetItems(config, t)}</span>
                        <span className="block text-xs text-slate-500">{t2HHMM(t.createdAt)} · {t.staffName || '-'}{tr2 ? ` · ${tr(config, 'แตะเพื่อเปิด QR')}` : ''}</span>""",
    """                      <button onClick={() => setDone(t)} className="flex-1 min-w-0 text-left" data-det-row={t.id}>
                        <span className="block text-sm font-bold text-slate-900 truncate">{t2DetItems(config, t)}</span>
                        <span className="block text-xs text-slate-500">{t2HHMM(t.createdAt)} · {t.staffName || '-'} · {tr(config, tr2 ? 'แตะเพื่อเปิด QR' : 'แตะเพื่อเปิดใบรายงาน')}</span>""", 'detergent rows tap')
open(IDX, 'w', encoding='utf-8').write(s)
open(SW, 'w', encoding='utf-8').write(sw)
print('stage 1 OK')
