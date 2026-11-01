#!/usr/bin/env python3
"""v183 — แอดมิน/เจ้าของ ลงงานไม่คิดเงินแบบเร็ว: กดบันทึก → ส่งใบรายงานเข้า LINE ให้เลย · ไม่ต้องกดเริ่มเครื่อง
ที่มา: เจ้าของ 2 พ.ย. 69 'กดบันทึกแล้ว ส่งไปที่ Line ไม่ต้องกด เริ่มเครื่องก็ได้ เพราะ แอดมิน กับเจ้าของไม่ต้องป้องกันมาก จะได้สะดวก'
ทำอะไร (เฉพาะคนที่ล็อกอินเป็นแอดมินหรือเจ้าของ · แม่บ้านเหมือนเดิม)
  - งานภายใน / งานไม่คิดเงิน (ร้านเกอิชา): ไม่ถามยืนยันก่อนบันทึก
  - ร้าน SOL (Otteri): บันทึกแล้วติ๊ก 'เริ่มใน SOL แล้ว' ให้ทุกช่องของใบงานทันที (pulseLogs method 'sol' · autoFree true)
    เครื่อง = เครื่องที่เลือกในใบงาน / เครื่องเดียวของขนาดนั้น · ไม่รู้เครื่อง = 'SOL · ไม่ระบุเครื่อง' (กระทบยอด SOL เทียบยอดรวมทั้งวัน)
    ใบงานลงย้อนหลัง → ติ๊กเป็นวัน/เวลาของใบงาน
  - งานภายใน: เปิดใบรายงานแล้วเด้งหน้าแชร์ (LINE) ให้เลย · ถ้ามือถือไม่ยอมเด้งเอง ปุ่ม 📤 ส่งเข้ากลุ่ม ยังอยู่
  - ร้านที่ปุ่มเริ่มเครื่องสั่งเครื่องจริง (Teddy 2 EC) ไม่ติ๊กอัตโนมัติ — ยังต้องกดเริ่มเครื่องเหมือนเดิม
usage: python3 tools/v183_admin_fast.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v182-2026-11-01';", "window.APP_VERSION = 'v183-2026-11-02';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v182';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v182';", "const CACHE_NAME = 'plp-laundry-v183';")

# ---------- 1) ติ๊ก SOL อัตโนมัติ ----------
rep("""const solCodeOf = (order) => '#' + (order && order.queueNo != null ? order.queueNo : ((order && order.id) || '').slice(-4));""",
    """const solCodeOf = (order) => '#' + (order && order.queueNo != null ? order.queueNo : ((order && order.id) || '').slice(-4));
// 🔧 v183 แอดมิน/เจ้าของลงงานไม่คิดเงินในร้าน SOL → ติ๊ก 'เริ่มใน SOL แล้ว' ให้ทุกช่องทันที (ไม่ต้องกดเริ่มเครื่องเอง)
function autoSolStartFree(config, order) {
  if (!isSol(config) || !order || !order.id) return [];
  const staff = currentStaffLS(config);
  const at = order.createdAt || Date.now(), now = Date.now();
  const ms = pulseMachines(config);
  const internalIds = (order.internalMachines || []).map(lb => (ms.find(m => m.label === lb) || {}).id).filter(Boolean);
  const used = new Set();
  return pulseSlotsForOrder(order, config).map((sl, i) => {
    const allowed = sl.allowed || [];
    const machine = allowed.length === 1 ? allowed[0] : (internalIds.length ? (allowed.find(x => !used.has(x)) || allowed[0] || null) : null);
    if (machine) used.add(machine);
    const id = `${config.brand}-sol-${at + i}-${Math.random().toString(36).slice(2, 8)}`;
    const log = cleanUndefined({
      brand: config.brand, dateKey: dateKeyOf(new Date(at)), machine: machine || null, machineLabel: machine ? pulseMachineLabel(config, machine) : 'SOL · ไม่ระบุเครื่อง',
      pulses: Math.round((sl.baht || 0) / PULSE_BAHT), baht: sl.baht || 0, method: 'sol', status: 'confirmed',
      refType: isInternalOrder(order) ? 'internal' : 'order', refId: order.id, slotKey: sl.key, refLabel: pulseRefLabel(order, config),
      staffId: staff && staff.id ? staff.id : null, staffName: staff && staff.name ? staff.name : '',
      createdAt: at + i, doneAt: now, kind: sl.kind === 'topup' ? 'dry' : sl.kind === 'custom' ? null : sl.kind, kg: sl.kg || null, temp: sl.temp || null,
      heat: null, dryMin: null, mismatch: null, solCode: solCodeOf(order), autoFree: true,
    });
    pulseLogRef(id).set(log).catch(e => console.error('auto sol log error:', e));
    return { id, ...log };
  });
}""", 'autoSolStartFree')

# ---------- 2) บันทึกแล้ว: ติ๊ก SOL + เด้งส่ง LINE ----------
rep("""  const [autoOpenTicket, setAutoOpenTicket] = useState(false); // เปิดใบงานอัตโนมัติหลังรับงานใหม่""",
    """  const [autoOpenTicket, setAutoOpenTicket] = useState(false); // เปิดใบงานอัตโนมัติหลังรับงานใหม่
  const [autoShareSlip, setAutoShareSlip] = useState(false); // 🔧 v183 แอดมิน/เจ้าของ: บันทึกงานภายในแล้วเด้งส่ง LINE""", 'autoShareSlip state')
rep("""      const savedOrder = { ...orderWithoutId, id: newId };
      playSuccessSound();
      setSelectedOrder(savedOrder);""",
    """      const savedOrder = { ...orderWithoutId, id: newId };
      const fastFree = (isOwner || isAdminUser) && isFreeJob(savedOrder, config); // 🔧 v183 แอดมิน/เจ้าของ ไม่ต้องกดเริ่มเครื่อง/ส่งเอง
      if (fastFree) autoSolStartFree(config, savedOrder);
      if (fastFree && isInternalOrder(savedOrder)) setAutoShareSlip(true);
      playSuccessSound();
      setSelectedOrder(savedOrder);""", 'handleNewOrder fast')
rep("""<ReceiptView config={config} order={selectedOrder} isOwner={isOwner} collections={collections} autoOpenTicket={autoOpenTicket} onTicketOpened={() => setAutoOpenTicket(false)}""",
    """<ReceiptView config={config} order={selectedOrder} isOwner={isOwner} collections={collections} autoOpenTicket={autoOpenTicket} onTicketOpened={() => setAutoOpenTicket(false)} autoShareSlip={autoShareSlip} onSlipShared={() => setAutoShareSlip(false)}""", 'ReceiptView props')
rep("""function ReceiptView({ config, order, onBack, autoOpenTicket, onTicketOpened, isOwner, collections }) {""",
    """function ReceiptView({ config, order, onBack, autoOpenTicket, onTicketOpened, isOwner, collections, autoShareSlip, onSlipShared }) {""", 'ReceiptView sig')
rep("""  const [slipUrl, setSlipUrl] = useState(null); // 🧾 v171 ใบรายงานงานภายใน""",
    """  const [slipUrl, setSlipUrl] = useState(null); // 🧾 v171 ใบรายงานงานภายใน
  const slipSharedRef = useRef(false);
  useEffect(() => { // 🔧 v183 แอดมิน/เจ้าของ: ใบรายงานพร้อม → เด้งหน้าแชร์ (LINE) ให้เลย · ไม่เด้ง = ปุ่ม 📤 ยังอยู่
    if (!autoShareSlip || !internal || !slipUrl || slipSharedRef.current) return;
    slipSharedRef.current = true;
    if (onSlipShared) onSlipShared();
    shareReportSlip(config, slipUrl, 'งานภายใน', 'internal-' + (order.internalType || ''));
  }, [autoShareSlip, slipUrl, internal]);""", 'ReceiptView auto share')

# ---------- 3) ไม่ถามยืนยัน (แอดมิน/เจ้าของ) ----------
rep("""      if (!confirm(`🔧 งานภายในร้าน\\n\\nประเภท: ${tLabel}""",
    """      if (!freeOk && !confirm(`🔧 งานภายในร้าน\\n\\nประเภท: ${tLabel}""", 'skip internal confirm')
rep("""      if (!confirm(`✅ ${tr(config, 'ยืนยันการรับงาน')}\\n\\n${acct.emoji""",
    """      if (!(freeOk && acct.noRevenue) && !confirm(`✅ ${tr(config, 'ยืนยันการรับงาน')}\\n\\n${acct.emoji""", 'skip free account confirm')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v183 applied')
