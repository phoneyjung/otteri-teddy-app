#!/usr/bin/env python3
"""v174 — เช็กหยอดเหรียญตาม 'ขนาดเครื่อง' แทนเลขเครื่อง (เจ้าของตัดสิน 31 ต.ค.: เครื่องไม่ตรงก็ได้ แต่ขนาดต้องตรง)
ที่มา: แม่บ้านลงหยอดเหรียญ ซัก 4 / อบ 2 / อบ 8 แต่หยอดจริงที่เครื่องข้างๆ ขนาดเดียวกัน → ขึ้นแถบเหลือง 'บันทึกหยอดเหรียญ มากกว่าที่เครื่องนับได้' ทั้งที่เงินเข้าเครื่องครบ
- กระทบยอด: รวมเหรียญที่ลง ↔ เหรียญที่เครื่องนับได้ ต่อกลุ่ม (ซัก/อบ × กก.) · เตือนเมื่อทั้งกลุ่มนับได้น้อยกว่าที่ลง (ข้อความบอกกลุ่ม + ยอดลง/ยอดนับ)
  กลุ่มที่อ่านประวัติเครื่องไม่ได้บางเครื่อง = ข้าม (ไม่เตือนมั่ว)
- ป้ายในใบงาน (checkCoinLog): เครื่องนี้ไม่เห็นเหรียญ → ครั้งสุดท้าย/กด 🔄 เช็กเหรียญ นับรวมทุกเครื่องขนาดเดียวกัน
usage: python3 tools/v174_coin_size.py index.html sw.js
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
rep("window.APP_VERSION = 'v173-2026-10-31';", "window.APP_VERSION = 'v174-2026-10-31';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v173';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v173';", "const CACHE_NAME = 'plp-laundry-v174';")

# ---------- กระทบยอด: กลุ่มขนาดเครื่อง ----------
rep("""  if (ec && ec.byMachine) {
    pulseMachines(config).forEach(m => {
      const e = ec.byMachine[m.id];""",
    """  if (ec && ec.byMachine) {
    const coinGroups = {}; // 💵 v174 เหรียญรวมตามขนาดเครื่อง (ซัก/อบ × กก.)
    pulseMachines(config).forEach(m => {
      const e = ec.byMachine[m.id];
      const cg = (coinGroups[m.kind + m.kg] = coinGroups[m.kind + m.kg] || { kind: m.kind, kg: m.kg, app: 0, ec: 0, missing: false });
      if (!e) cg.missing = true;""", 'coin groups init')
rep("""      const coinOld = sumBaht(dayCoins.filter(l => l.machine === m.id && ec.at - (l.createdAt || 0) > 120000));
      if (coinOld > (e.coinBaht || 0)) add(`k:${m.id}:${coinOld}`, 'warn', 'บันทึกหยอดเหรียญ มากกว่าที่เครื่องนับได้', { label: m.label, amount: coinOld - (e.coinBaht || 0) });""",
    """      // v174: ลงผิดเบอร์ได้ ถ้าขนาดเดียวกัน → รวมเป็นกลุ่ม แล้วเทียบหลังวนครบทุกเครื่อง
      cg.app += sumBaht(dayCoins.filter(l => l.machine === m.id && ec.at - (l.createdAt || 0) > 120000));
      cg.ec += e.coinBaht || 0;""", 'coin per machine → group')
rep("""      noSignal.forEach(t => add(`n:${m.id}:${t}`, 'warn', 'สั่งแล้วเครื่องไม่ตอบ', { label: m.label, times: [t.slice(11, 16)] }));
    });""",
    """      noSignal.forEach(t => add(`n:${m.id}:${t}`, 'warn', 'สั่งแล้วเครื่องไม่ตอบ', { label: m.label, times: [t.slice(11, 16)] }));
    });
    Object.values(coinGroups).forEach(g => {
      if (g.missing || g.app <= g.ec) return;
      add(`k:${g.kind}${g.kg}:${g.app}`, 'warn', 'บันทึกหยอดเหรียญ มากกว่าที่เครื่องนับได้',
        { label: `${g.kind === 'wash' ? 'ซัก' : 'อบ'} ${g.kg}kg ทุกเครื่อง · ลง ฿${formatMoney(g.app)} · เครื่องนับได้ ฿${formatMoney(g.ec)}`, amount: g.app - g.ec });
    });""", 'coin group warn')

# ---------- ป้ายในใบงาน: เช็กรวมเครื่องขนาดเดียวกัน ----------
rep("""  const snap = await window.db.collection('pulseLogs').where('dateKey', '==', log.dateKey).get();
  const appCoin = snap.docs.map(d => ({ id: d.id, ...d.data() }))
    .filter(l => l.brand === config.brand && l.machine === log.machine && pulseIsCoin(l) && (pulseLive(l) || pulseRefunded(l)) && ((l.createdAt || 0) <= (log.createdAt || 0) || l.id === log.id))
    .reduce((a, l) => a + (l.baht || 0), 0);
  const seen = (e.coinBaht || 0) >= appCoin;
  if (seen || final) await pulseLogRef(log.id).set({ coinSeen: seen, coinCheckAt: Date.now(), ecCoinBaht: e.coinBaht || 0, appCoinBaht: appCoin }, { merge: true });
  return { ok: true, seen };""",
    """  const snap = await window.db.collection('pulseLogs').where('dateKey', '==', log.dateKey).get();
  const coins = snap.docs.map(d => ({ id: d.id, ...d.data() }))
    .filter(l => l.brand === config.brand && pulseIsCoin(l) && (pulseLive(l) || pulseRefunded(l)) && ((l.createdAt || 0) <= (log.createdAt || 0) || l.id === log.id));
  const appCoin = coins.filter(l => l.machine === log.machine).reduce((a, l) => a + (l.baht || 0), 0);
  let seen = (e.coinBaht || 0) >= appCoin;
  let group = null;
  // 💵 v174: เครื่องนี้ไม่เห็นเหรียญ → ครั้งสุดท้าย/กดเช็กเอง นับรวมทุกเครื่องขนาดเดียวกัน (หยอดผิดเบอร์แต่ขนาดเดียวกัน = ไม่เป็นไร)
  if (!seen && final) {
    const me = pulseMachines(config).find(x => x.id === log.machine);
    const sib = me ? pulseMachines(config).filter(x => x.kind === me.kind && x.kg === me.kg).map(x => x.id) : [];
    if (sib.length > 1) {
      const ecG = await fetchEcDay(config, log.dateKey, sib);
      if (sib.every(id => ecG.byMachine[id])) {
        group = { ec: sib.reduce((a, id) => a + (ecG.byMachine[id].coinBaht || 0), 0), app: coins.filter(l => sib.includes(l.machine)).reduce((a, l) => a + (l.baht || 0), 0) };
        seen = group.ec >= group.app;
      }
    }
  }
  if (seen || final) await pulseLogRef(log.id).set({ coinSeen: seen, coinCheckAt: Date.now(), ecCoinBaht: e.coinBaht || 0, appCoinBaht: appCoin, coinGroup: group }, { merge: true });
  return { ok: true, seen };""", 'checkCoinLog group')

open(IDX, 'w', encoding='utf-8').write(s)
open(SW, 'w', encoding='utf-8').write(sw)
print('v174 applied')
