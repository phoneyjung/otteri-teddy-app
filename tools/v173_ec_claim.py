#!/usr/bin/env python3
"""v173 — เจ้าของเปลี่ยน 'มีการยิงนอกแอป' (กดจากเว็บ EC เอง) เป็นงานภายใน 🔧 ซ่อม/ทดสอบเครื่อง ย้อนหลัง → ยอดแอปตรงกับเครื่อง
- ปุ่มเฉพาะเจ้าของ ในกระทบยอดเปิดเครื่อง (หน้าเจ้าของ → เครื่อง → พัลส์ และแผ่นกระทบยอดเมื่อล็อกอินแบบเจ้าของ)
- สร้างใบงานภายใน internalType 'test' (internalCustom = ยอด, internalMachines = เครื่องนั้น, เวลา = เวลาที่ยิงใน EC)
  + pulseLogs method 'ec-claim' status 'confirmed' เวลาเดียวกับ EC → จับคู่กับ 'บังคับส่งพัลส์' ได้พอดี
- id ตายตัวจากเครื่อง+เวลา EC → กดซ้ำไม่เกิดซ้ำ · ไม่นับเป็นรายได้ (งานภายใน)
usage: python3 tools/v173_ec_claim.py index.html sw.js
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
rep("window.APP_VERSION = 'v172-2026-10-31';", "window.APP_VERSION = 'v173-2026-10-31';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v172';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v172';", "const CACHE_NAME = 'plp-laundry-v173';")

# ---------- เก็บรายการ EC ที่ยิงนอกแอปไว้กับ issue ----------
rep("""'มีการยิงนอกแอป', { label: m.label, amount: outside.reduce((s, f) => s + f.pulses, 0) * PULSE_BAHT, times: outside.map(f => f.time.slice(11, 16)) });""",
    """'มีการยิงนอกแอป', { label: m.label, amount: outside.reduce((s, f) => s + f.pulses, 0) * PULSE_BAHT, times: outside.map(f => f.time.slice(11, 16)), machine: m.id, ecOut: outside.map(f => ({ time: f.time, pulses: f.pulses })) });""",
    'outside issue data')

# ---------- ฟังก์ชันผูกเป็นงานซ่อม/ทดสอบ (ก่อน PulseReconPanel) ----------
rep("""function PulseReconPanel({ config, orders, dateKey, setDateKey, isOwner, autoEc, compact }) {""",
r"""// 🔧 v173 เจ้าของยิงทดสอบจากเว็บ EC → เปลี่ยนเป็นงานภายใน 'ซ่อม/ทดสอบเครื่อง' ย้อนหลัง
// ใบงาน 1 ใบต่อเครื่อง (ยอด = พัลส์ที่ยิงนอกแอปของเครื่องนั้นในวันนั้น) + pulseLogs เวลาเดียวกับ EC → จับคู่ได้ ยอดตรง
// id ตายตัวจากเครื่อง+เวลา → กดซ้ำเขียนทับของเดิม ไม่เกิดซ้ำ
async function claimOutsideAsTest(config, issue) {
  const m = pulseMachines(config).find(x => x.id === issue.machine);
  const list = (issue.ecOut || []).map(f => ({ ...f, ms: pulseBkkMs(f.time) })).filter(f => f.ms > 0 && f.pulses > 0).sort((a, b) => a.ms - b.ms);
  if (!m || !list.length) throw new Error('ไม่พบข้อมูลการยิงของเครื่องนี้');
  const baht = list.reduce((s, f) => s + f.pulses, 0) * PULSE_BAHT;
  const now = Date.now();
  const orderId = `${config.brand}-ectest-${m.id}-${list[0].ms}`;
  const order = {
    brand: config.brand, createdAt: list[0].ms, backdated: true, enteredAt: now,
    customerName: '', customerPhone: '', clothCount: '', pickupTime: '', note: '',
    washItems: [], dryItems: [], detergentQty: 0, softenerQty: 0, foldBaskets: 0, noFold: false,
    paymentMethod: 'internal', internalType: 'test', internalMachines: [m.label], internalCustom: baht,
    internalReason: `เจ้าของยิงทดสอบจากเว็บ EC (${list.map(f => f.time.slice(11, 16)).join(', ')}) · เปลี่ยนเป็นงานภายในย้อนหลัง`,
    staffName: 'เจ้าของ', collected: false, ecClaim: true, ecClaimAt: now,
  };
  const refLabel = pulseRefLabel({ ...order, id: orderId }, config);
  const b = window.db.batch();
  b.set(window.db.collection('orders').doc(orderId), order, { merge: true });
  list.forEach(f => {
    b.set(pulseLogRef(`${orderId}-${f.ms}`), {
      brand: config.brand, dateKey: dateKeyOf(new Date(f.ms)), machine: m.id, machineLabel: m.label,
      pulses: f.pulses, baht: f.pulses * PULSE_BAHT, refType: 'internal', refId: orderId, slotKey: null, refLabel,
      staffId: 'owner', staffName: 'เจ้าของ', createdAt: f.ms, sentAt: f.ms, ecTime: f.time, status: 'confirmed', method: 'ec-claim',
      kind: m.kind, kg: m.kg || null, retryOf: null, claimNote: 'เจ้าของยิงจากเว็บ EC · เปลี่ยนเป็นงานซ่อม/ทดสอบ', claimedAt: now,
    }, { merge: true });
  });
  await b.commit();
  return { orderId, baht };
}
async function askClaimOutside(config, issues) {
  const list = (issues || []).filter(i => i.ecOut && i.ecOut.length);
  if (!list.length) return 0;
  const sum = list.reduce((s, i) => s + (i.amount || 0), 0);
  if (!confirm(`🔧 เปลี่ยนเป็นงานซ่อม/ทดสอบเครื่อง?\n\n${list.map(i => `${i.label} ฿${formatMoney(i.amount || 0)} · ${(i.times || []).join(', ')}`).join('\n')}\n\nแอปจะลงงานภายใน "ซ่อม/ทดสอบเครื่อง" ย้อนหลังตามเวลาที่ยิง (ไม่นับรายได้) แล้วนับว่าเปิดผ่านแอป → ยอดแอปตรงกับเครื่อง\n\nใช้เฉพาะที่เจ้าของยิงทดสอบเอง · รวม ฿${formatMoney(sum)}`)) return 0;
  let n = 0;
  for (const i of list) { await claimOutsideAsTest(config, i); n++; }
  return n;
}

function PulseReconPanel({ config, orders, dateKey, setDateKey, isOwner, autoEc, compact }) {""", 'claim fns')

# ---------- ปุ่มในแผงกระทบยอด ----------
rep("""  const [openKind, setOpenKind] = useState(null); // v162 โหมดย่อ""",
    """  const [openKind, setOpenKind] = useState(null); // v162 โหมดย่อ
  const [claiming, setClaiming] = useState(false); // 🔧 v173
  const doClaim = async (issues) => {
    setClaiming(true);
    try { const n = await askClaimOutside(config, issues); if (n) refreshEc(); }
    catch (e) { alert('เปลี่ยนไม่สำเร็จ: ' + (e && e.message ? e.message : e)); }
    finally { setClaiming(false); }
  };
  const claimBtn = (issues, label) => (
    <button onClick={() => doClaim(issues)} disabled={claiming}
      className="mt-1.5 px-3 py-1.5 rounded-lg border border-slate-300 bg-white text-xs font-extrabold text-slate-800 active:scale-95 disabled:opacity-50">
      {claiming ? '…' : label}
    </button>
  );""", 'claim state')
# โหมดย่อ (หน้าเจ้าของ Teddy 2 → เครื่อง → พัลส์)
rep("""                        {g.list.map(i => <p key={i.key} className="text-xs text-slate-600 pl-4">• {i.label}{i.amount ? ` ฿${formatMoney(i.amount)}` : ''}{i.times && i.times.length ? ` · ${i.times.join(', ')}` : ''}</p>)}""",
    """                        {g.list.map(i => <p key={i.key} className="text-xs text-slate-600 pl-4">• {i.label}{i.amount ? ` ฿${formatMoney(i.amount)}` : ''}{i.times && i.times.length ? ` · ${i.times.join(', ')}` : ''}</p>)}
                        {isOwner && g.list.some(i => i.ecOut) && <div className="pl-4">{claimBtn(g.list.filter(i => i.ecOut), `🔧 เจ้าของยิงทดสอบ → เปลี่ยนเป็นงานซ่อม/ทดสอบ${g.list.filter(i => i.ecOut).length > 1 ? ' ทั้งหมด' : ''}`)}</div>}""",
    'claim btn compact')
# โหมดเต็ม
rep("""                    <p className="text-xs text-slate-600">{i.label}{i.times && i.times.length ? ` · 🕐 ${i.times.join(', ')}` : ''}</p>
                  </div>""",
    """                    <p className="text-xs text-slate-600">{i.label}{i.times && i.times.length ? ` · 🕐 ${i.times.join(', ')}` : ''}</p>
                    {isOwner && i.ecOut && claimBtn([i], '🔧 เจ้าของยิงทดสอบ → เปลี่ยนเป็นงานซ่อม/ทดสอบ')}
                  </div>""", 'claim btn full')

open(IDX, 'w', encoding='utf-8').write(s)
open(SW, 'w', encoding='utf-8').write(sw)
print('v173 applied')
