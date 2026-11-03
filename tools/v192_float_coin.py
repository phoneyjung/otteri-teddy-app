#!/usr/bin/env python3
"""v192 — Teddy 2: ยิงผ่านแอปไม่ได้ (EC ใช้ไม่ได้) → ปุ่ม '🪙 ยิงไม่ได้ → หยอดเหรียญแทน'
ที่มา: เจ้าของ 3 พ.ย. 69 'ตอนนี้ยิงผ่านแอปไม่ได้ ยอดที่โอนเลยต้องให้เหรียญไปหยอดก่อน ทำยังไงดี' → เลือก 'ทำ v192'
ทำอะไร (ร้านยิงพัลส์ EC เท่านั้น · ไม่ใช่ SOL)
  - หน้าเลือกเครื่อง: ใบงานที่มีส่วนโอน/ส่วนลด (ยิงแอป) มีปุ่ม '🪙 ยิงไม่ได้ → หยอดเหรียญแทน <เครื่อง> ฿X'
    ปุ่มเด่น (สีส้ม) เมื่อ Worker แจ้งพัก หรือมียิงไม่สำเร็จใน 2 ชม. · ปกติเป็นปุ่มรอง
  - กดแล้ว: บันทึกหยอดเหรียญ (pulseLog method coin · coinFromFloat) → ใบงานนับว่าเริ่มเครื่องแล้ว
    + บันทึกใช้เหรียญตั้งต้นของร้าน (tokenExchanges kind 'floatCoin' · โอน) → เหรียญตั้งต้นในมือแม่บ้านลดลง
    ใบงานยังเป็น 'โอน' (เงินอยู่ในบัญชีร้านแล้ว) · ไม่นับเป็นเงินสดในมือ · ไม่เข้ารอบเคลียร์ยอดโอน
    ส่วนเงินสดของลูกค้า (ถ้ามี) บันทึกหยอดเหรียญตามปกติ
  - ยกเลิกบันทึกหยอดเหรียญ (ยังไม่ได้หยอด) → ลบรายการใช้เหรียญตั้งต้นด้วย
  - ไม่เช็กเหรียญกับ EC อัตโนมัติสำหรับรายการนี้ (EC ใช้ไม่ได้อยู่) · เช็กเหรียญอัตโนมัติหยุดเมื่อ Worker แจ้งพัก
  - รายการเปิดเครื่อง: ป้าย '🪙 เหรียญร้าน'
usage: python3 tools/v192_float_coin.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v191-2026-11-03';", "window.APP_VERSION = 'v192-2026-11-03';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v191';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v191';", "const CACHE_NAME = 'plp-laundry-v192';")

# ---------- บันทึกหยอดเหรียญแทน (เหรียญตั้งต้นของร้าน) ----------
rep("""async function syncCashInMachine(config, order, coinSum) {""",
    """// 🪙 v192 ยิงผ่านแอปไม่ได้ → แม่บ้านใช้เหรียญตั้งต้นของร้านหยอดแทน (ส่วนโอน/ส่วนลดของใบงาน)
// pulseLog = หยอดเหรียญ (นับว่าเริ่มเครื่องแล้ว · เทียบกับเหรียญที่เครื่องนับได้) · tokenExchanges 'floatCoin' = เหรียญตั้งต้นลดลง
function floatCoinInsert(config, order, { machine, kind, kg, temp, heat, baht, dryMin, warn, discBaht }) {
  const staff = currentStaffLS(config);
  const now = Date.now();
  const id = `${config.brand}-coin-${now}-${Math.random().toString(36).slice(2, 8)}`;
  const fid = 'float-' + id;
  const cp0 = COIN_POINTS[config.brand] || {};
  const log = {
    brand: config.brand, dateKey: dateKeyOf(new Date(now)), machine, machineLabel: pulseMachineLabel(config, machine),
    pulses: Math.round(baht / PULSE_BAHT), baht, method: 'coin', status: 'coin', coinFromFloat: true, floatExchangeId: fid,
    refType: isInternalOrder(order) ? 'internal' : 'order', refId: order.id, slotKey: null, refLabel: pulseRefLabel(order, config),
    staffId: staff && staff.id ? staff.id : null, staffName: staff && staff.name ? staff.name : '',
    createdAt: now, kind: kind || null, kg: kg || null, temp: temp || null, heat: heat || null, dryMin: dryMin || null, mismatch: warn || null,
  };
  pulseLogRef(id).set(log).catch(e => console.error('float coin log error:', e));
  const ex = {
    brand: config.brand, kind: 'floatCoin', amount: baht, paymentMethod: 'transfer',
    tokenCount: cp0.tokenMode ? Math.round(baht / (cp0.tokenValue || 10)) : 0, coinCount: cp0.tokenMode ? 0 : Math.round(baht / 10),
    discBaht: discBaht || 0, refId: order.id, refLabel: pulseRefLabel(order, config), machine, machineLabel: log.machineLabel, pulseLogId: id,
    staffName: log.staffName, photo: '', note: 'หยอดแทนยิงแอป (ยิงไม่ได้)', createdAt: now,
  };
  window.db.collection('tokenExchanges').doc(fid).set(ex).catch(e => console.error('float exchange error:', e));
  return { id, ...log };
}

async function syncCashInMachine(config, order, coinSum) {""", 'floatCoinInsert')

# ยกเลิกบันทึกหยอดเหรียญ → ลบรายการใช้เหรียญตั้งต้นด้วย
rep("""  await pulseLogRef(log.id).set({ status: 'void', voidReason: 'ยกเลิกบันทึกหยอดเหรียญ — ยังไม่ได้หยอด', voidAt: Date.now() }, { merge: true });""",
    """  await pulseLogRef(log.id).set({ status: 'void', voidReason: 'ยกเลิกบันทึกหยอดเหรียญ — ยังไม่ได้หยอด', voidAt: Date.now() }, { merge: true });
  if (log.floatExchangeId) await window.db.collection('tokenExchanges').doc(log.floatExchangeId).delete().catch(e => console.error('float exchange delete error:', e)); // 🪙 v192""", 'undo float')

# เช็กเหรียญกับ EC อัตโนมัติ: หยุดเมื่อ Worker แจ้งพัก
rep("""  const tick = async () => {
    n++;
    const final = n >= 8;""",
    """  const tick = async () => {
    if (pulseEcPaused()) return; // v192 Worker แจ้งพัก (EC ใช้ไม่ได้) → ไม่เช็กต่อ
    n++;
    const final = n >= 8;""", 'watch paused')

# ---------- หน้าเลือกเครื่อง: ปุ่มหยอดเหรียญแทน ----------
rep("""  const owner = pulseIsOwnerNow(config, isOwner); // ✍️ v149: บันทึกว่าเริ่มแล้วโดยไม่ยิงจริง ได้เฉพาะเจ้าของ""",
    """  const owner = pulseIsOwnerNow(config, isOwner); // ✍️ v149: บันทึกว่าเริ่มแล้วโดยไม่ยิงจริง ได้เฉพาะเจ้าของ
  // 🪙 v192 ยิงผ่านแอปไม่ได้ (Worker แจ้งพัก / ยิงไม่สำเร็จใน 2 ชม.) → ปุ่มหยอดเหรียญแทนเด่นขึ้น
  const ecDown = pulseEcPaused() || (dayLogs || []).some(l => l.status === 'failed' && Date.now() - (l.createdAt || 0) < 2 * 3600000);""", 'ecDown')
rep("""          <button disabled={!ready || !!busyText}
            onClick={() => onFire(job,""",
    """          {ready && !busyText && !block && !isSol(config) && cp.pulse > 0 && (
            <button data-float-coin onClick={() => {
              const o = job.order;
              const floatBaht = cp.pulse, coinPart = cp.coin;
              const lines = [];
              if (coinPart > 0) lines.push(`💵 ${tr(config, 'เงินสดของลูกค้า')} ฿${coinPart}`);
              lines.push(`🪙 ${tr(config, 'เหรียญตั้งต้นของร้าน')} ฿${floatBaht} (${Math.round(floatBaht / 10)} ${tr(config, 'เหรียญ')})`);
              if (!confirm(`🪙 ${tr(config, 'ยิงไม่ได้ → หยอดเหรียญแทน')}\\n\\n📋 ${pulseRefLabel(o, config)}\\n🧺 ${selM.label} (${selM.kg}kg) · ฿${baht}\\n${lines.join('\\n')}\\n\\n• ${tr(config, 'ใบงานยังเป็นโอน — เงินอยู่ในบัญชีร้านแล้ว ไม่ต้องส่งเงิน')}\\n• ${tr(config, 'แอปหักเหรียญตั้งต้นให้')}\\n\\n👉 ${tr(config, 'หยอดเหรียญจนเครื่องเริ่มทำงาน แล้วกดตกลง')}`)) return;
              const mp = { machine: selM.id, kind: selM.kind, kg: selM.kg, temp: selM.kind === 'wash' ? tempUse : null, heat: selM.kind === 'dry' ? heat : null, warn };
              const dm = (b) => (selM.kind === 'dry' ? dryMinutesFor(config, selM.kg, b) : null);
              if (coinPart > 0) logCoinInsert(config, o, job.logs || jobLogs || [], { ...mp, baht: coinPart, dryMin: dm(coinPart) });
              floatCoinInsert(config, o, { ...mp, baht: floatBaht, dryMin: dm(floatBaht), discBaht: cp.disc || 0 });
              playSuccessSound();
              setOwnerMsg(`🪙 ${selM.label} ฿${baht} — ${tr(config, 'บันทึกหยอดเหรียญแทนแล้ว')}`);
              setSel(null);
            }}
              className={`w-full mb-2 rounded-xl border-2 font-extrabold active:scale-95 transition ${ecDown ? 'py-3 text-base' : 'py-2 text-sm'}`}
              style={ecDown ? { borderColor: '#D97706', background: '#FEF3C7', color: '#92400E' } : { borderColor: '#E2E8F0', background: '#FFFFFF', color: '#475569' }}>
              🪙 {tr(config, 'ยิงไม่ได้ → หยอดเหรียญแทน')} {selM.label} ฿{cp.pulse}
            </button>
          )}
          <button disabled={!ready || !!busyText}
            onClick={() => onFire(job,""", 'float button')

# ---------- ป้ายในรายการเปิดเครื่อง ----------
rep("""{pulseIsCoin(l) && <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800">💵 {tr(config, 'หยอดเหรียญ')}</span>}""",
    """{pulseIsCoin(l) && <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800">💵 {tr(config, 'หยอดเหรียญ')}</span>}
          {l.coinFromFloat && <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-full bg-amber-100 text-amber-900" data-float-chip>🪙 {tr(config, 'เหรียญร้าน')}</span>}""", 'chip job list')
rep("""        {statusChip(l)}
        {pulseIsCoin(l) && <CoinCheckAction""",
    """        {statusChip(l)}
        {l.coinFromFloat && <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-full bg-amber-100 text-amber-900" data-float-chip>🪙 {tr(config, 'เหรียญร้าน')}</span>}
        {pulseIsCoin(l) && <CoinCheckAction""", 'chip starter card')

# ---------- MM ----------
rep("""  'โอน ยิงแอป': 'လွှဲငွေ အက်ပ်မှ ပို့',""",
    """  'โอน ยิงแอป': 'လွှဲငွေ အက်ပ်မှ ပို့',
  'ยิงไม่ได้ → หยอดเหรียญแทน': 'အက်ပ်မှ မပို့နိုင် → အကြွေစေ့ ထည့်ပါ', // v192
  'เงินสดของลูกค้า': 'ဖောက်သည်၏ ငွေသား', // v192
  'เหรียญตั้งต้นของร้าน': 'ဆိုင်၏ အရန်အကြွေစေ့', // v192
  'ใบงานยังเป็นโอน — เงินอยู่ในบัญชีร้านแล้ว ไม่ต้องส่งเงิน': 'အလုပ်စာရွက်သည် လွှဲငွေအဖြစ်ရှိ — ငွေ ဆိုင်အကောင့်ထဲ ရောက်ပြီး ငွေပေးစရာမလို', // v192
  'แอปหักเหรียญตั้งต้นให้': 'အက်ပ်က အရန်အကြွေစေ့ကို နုတ်ပေးမည်', // v192
  'หยอดเหรียญจนเครื่องเริ่มทำงาน แล้วกดตกลง': 'စက်စတင်သည်အထိ အကြွေစေ့ထည့်ပြီး OK နှိပ်ပါ', // v192
  'บันทึกหยอดเหรียญแทนแล้ว': 'အကြွေစေ့ထည့်မှု သိမ်းပြီး', // v192
  'เหรียญร้าน': 'ဆိုင်အကြွေစေ့', // v192""", 'MM')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v192 applied')
