#!/usr/bin/env python3
"""v213: Teddy 2 (credit mode) — owner-only button '🎟️ จริงๆ ตัดเครดิต' on a coin record of a cash job.
Case (owner, 12 Nov 2026): customer paid cash, the maid forgot and paid the machine with her own EC credit instead of the coins.
The coin record becomes that maid's credit record → job still counts as started · the cash goes back into 'เงินสดในมือ'
(it is really in the drawer) · credit used matches EC.
Usage: python3 tools/v213_coin_to_credit.py index.html sw.js"""
import sys
idx, sw = sys.argv[1], sys.argv[2]
s = open(idx, encoding='utf-8').read()

def rep(old, new):
    global s
    assert s.count(old) == 1, ('count', s.count(old), old[:90])
    s = s.replace(old, new)

# 1) logic — next to undoCoinLog
rep("// บันทึกว่าแม่บ้านหยอดเหรียญเข้าเครื่องแล้ว (ไม่ยิงพัลส์)",
"""// 🎟️ v213 Teddy 2 (ตัดเครดิต): ใบงานเงินสดที่แม่บ้านลืมหยอด ใช้เครดิตตัวเองจ่ายที่ตู้แทน → เจ้าของเปลี่ยนบันทึก 'หยอดเหรียญ' เป็น 'ตัดเครดิต' ของแม่บ้านคนนั้น
// ใบงานยังนับว่าเริ่มเครื่องแล้ว · เงินสดกลับไปอยู่ใน 'เงินสดในมือ' (เงินอยู่ในลิ้นชักจริง) · ยอดเครดิตที่ใช้เทียบ EC ตรง
async function convertCoinToCredit(config, order, logs, log) {
  const now = Date.now();
  await pulseLogRef(log.id).set({ method: 'credit', status: 'credit', doneAt: log.createdAt || now, convertedFrom: 'coin', convertedAt: now, convertedBy: 'เจ้าของ',
    creditNote: 'เจ้าของเปลี่ยนจากหยอดเหรียญ — แม่บ้านใช้เครดิตตัวเองแทนเงินสดลูกค้า (เงินสดอยู่ในลิ้นชัก)' }, { merge: true });
  if (!order || !order.id) return;
  try { const f = await window.db.collection('orders').doc(order.id).get(); if (f.exists) order = { ...order, ...f.data(), id: order.id }; } catch (e) {} // ใช้ข้อมูลใบงานล่าสุด
  const cashPart = orderCashPart(order, config);
  const remaining = (logs || []).filter(l => l.refId === order.id && l.id !== log.id && pulseIsCoin(l) && (pulseLive(l) || pulseRefunded(l))).reduce((a, l) => a + (l.baht || 0), 0);
  const upd = { brand: order.brand || config.brand, cashInMachine: Math.min(cashPart, remaining) };
  if (order.collectedVia === 'machine' && remaining < cashPart) {
    if (order.paymentMethod === 'cash') Object.assign(upd, { collected: false, collectedAt: null, collectedVia: null });
    if (order.paymentMethod === 'split') Object.assign(upd, { cashCollected: false, collected: false, collectedVia: null });
  }
  await window.db.collection('orders').doc(order.id).set(upd, { merge: true });
}
function CoinToCreditAction({ config, log, order, logs, isOwner }) { // 🎟️ v213 เจ้าของกดได้คนเดียว
  const [busy, setBusy] = useState(false);
  if (!isCredit(config) || !log || !pulseIsCoin(log) || !pulseLive(log) || log.coinFromFloat || !pulseIsOwnerNow(config, isOwner)) return null;
  const go = async () => {
    const ref = order ? pulseRefLabel(order, config) : (log.refLabel || '');
    if (!confirm(`🎟️ เปลี่ยนเป็น "ตัดเครดิต" (แม่บ้านไม่ได้หยอดเหรียญ)\\n\\n📋 ${ref}\\n🧺 ${log.machineLabel} ฿${log.baht}${log.staffName ? `\\n👤 เครดิตของ ${log.staffName}` : ''}\\n\\n• ใบงานยังนับว่าเริ่มเครื่องแล้ว\\n• เงินสด ฿${log.baht} กลับไปอยู่ใน "เงินสดในมือ" (เงินอยู่ในลิ้นชัก)\\n• เครดิตที่ใช้ของแม่บ้านคนนี้ +฿${log.baht}`)) return;
    setBusy(true);
    try { await convertCoinToCredit(config, order, logs, log); }
    catch (e) { alert('บันทึกไม่สำเร็จ: ' + (e && e.message ? e.message : e)); }
    setBusy(false);
  };
  return <button data-coin-to-credit onClick={go} disabled={busy} className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-sky-50 border border-sky-300 text-sky-800 active:scale-95 disabled:opacity-50">{busy ? '…' : '🎟️ จริงๆ ตัดเครดิต'}</button>;
}

// บันทึกว่าแม่บ้านหยอดเหรียญเข้าเครื่องแล้ว (ไม่ยิงพัลส์)""")

# 2) UI — job start list on the receipt (has setMsg/busy)
rep("""        {pulseIsCoin(l) && <CoinCheckAction config={config} log={l} order={order} logs={logs} />}
        {pulseIsManual(l) && pulseLive(l) && pay.coinLeft > 0 && pulseIsOwnerNow(config, isOwner) && (""",
"""        {pulseIsCoin(l) && <CoinCheckAction config={config} log={l} order={order} logs={logs} />}
        {pulseIsCoin(l) && <CoinToCreditAction config={config} log={l} order={order} logs={logs} isOwner={isOwner} />}
        {pulseIsManual(l) && pulseLive(l) && pay.coinLeft > 0 && pulseIsOwnerNow(config, isOwner) && (""")
# 3) UI — start sheet list (QR / home)
rep("""          {pulseIsCoin(l) && <CoinCheckAction config={config} log={l} order={order} logs={logs} />}
          {pulseIsManual(l) && <span""",
"""          {pulseIsCoin(l) && <CoinCheckAction config={config} log={l} order={order} logs={logs} />}
          {pulseIsCoin(l) && <CoinToCreditAction config={config} log={l} order={order} logs={logs} isOwner={isOwner} />}
          {pulseIsManual(l) && <span""")
rep("window.APP_VERSION = 'v212-2026-11-10';", "window.APP_VERSION = 'v213-2026-11-12';")
open(idx, 'w', encoding='utf-8').write(s)
w = open(sw, encoding='utf-8').read()
assert w.count("const CACHE_NAME = 'plp-laundry-v212';") == 1
open(sw, 'w', encoding='utf-8').write(w.replace("const CACHE_NAME = 'plp-laundry-v212';", "const CACHE_NAME = 'plp-laundry-v213';"))
print('v213 patched')
