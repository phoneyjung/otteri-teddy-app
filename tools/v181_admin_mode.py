#!/usr/bin/env python3
"""v181 — โหมดแอดมิน (งานภายในเท่านั้น) + Otteri: แม่บ้านทำงานฟรีเองไม่ได้ + งานร้านเกอิชาไม่นับรายได้
ที่มา: เจ้าของ 1 พ.ย. 69
  - 'งานซ่อม ล้างเครื่อง เจ้าของซัก หรืองานเกอิชา ไม่ต้องนับเป็นรายได้นะ'
  - เลือก 'ห้ามแม่บ้านทำงานฟรีเอง'
  - 'ต้องทำแอปแยก ให้เป็น โหมดแอดมิน ทำงานพวกนี้ได้ แต่ แสดงแค่งานภายในพอ เพราะแอดมินมีหลายคนช่วยกดได้
     ทำหน้าต่างง่ายๆ ให้แอดมินเป็นช่องทางพิเศษ สำหรับงานภายในโดยเฉพาะ'
ทำอะไร
  1. staff.role = 'admin' (เจ้าของตั้งใน ⚙️ จัดการรายชื่อ: ติ๊กตอนเพิ่ม หรือกดปุ่ม แม่บ้าน⇄แอดมิน) → เข้าด้วยชื่อ + PIN เหมือนแม่บ้าน
     แล้วเปิดหน้า AdminHomeView: ปุ่มลงงานภายใน (ล้างเครื่อง ซ่อม/ทดสอบ ซักซ้ำ ผ้าเจ้าของ อื่นๆ) + งานไม่คิดเงิน (ร้านเกอิชา)
     + เริ่มเครื่องเฉพาะงานพวกนี้ + รายการงานภายใน 3 วัน · ไม่เห็นงานลูกค้า/เงิน
  2. config.maidNoFree (Otteri): งานภายในทุกชนิด + งานไม่คิดเงิน = แอดมิน/เจ้าของลงและเริ่มเครื่อง · หน้าแรกแม่บ้านไม่มีปุ่มพวกนี้
  3. accounts[].noRevenue (Otteri ร้านเกอิชา): ไม่คิดเงิน · ไม่นับยอดขาย/ค้างจ่าย · นับเป็นงานภายในในหน้าเจ้าของ
usage: python3 tools/v181_admin_mode.py index.html sw.js
"""
import re
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v180-2026-11-01';", "window.APP_VERSION = 'v181-2026-11-01';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v180';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v180';", "const CACHE_NAME = 'plp-laundry-v181';")

# ---------- 1) config Otteri ----------
rep("""  accounts: [{ id: 'geisha', name: 'ร้านเกอิชา', emoji: '🏢', noFold: true }], // 🏢 ค้างจ่าย รวมบิลสิ้นเดือน · ไม่พับ · ราคาปกติ (ไม่ใช้โปรวันพุธ)""",
    """  accounts: [{ id: 'geisha', name: 'ร้านเกอิชา', emoji: '🏢', noFold: true, noRevenue: true }], // 🏢 v181 งานร้านเกอิชา = ไม่คิดเงิน ไม่นับรายได้ (เดิมค้างจ่ายรวมบิล) · ไม่พับ · ราคาปกติ (ไว้ดูมูลค่า)
  maidNoFree: true, // 🔒 v181 แม่บ้านทำงานฟรีเองไม่ได้ (ล้างเครื่อง ซ่อม ผ้าเจ้าของ เกอิชา) — แอดมิน/เจ้าของลงและเริ่มเครื่อง""", 'config otteri')

# ---------- 2) helpers ----------
rep("""const accountPayText = (o, config) => { const a = accountOf(o, config); return a ? `ค้างจ่าย · ${a.name}` : ''; };""",
    """const accountPayText = (o, config) => { const a = accountOf(o, config); return a ? (a.noRevenue ? `${a.name} · ไม่คิดเงิน` : `ค้างจ่าย · ${a.name}`) : ''; };
// 🆓 v181 งานไม่คิดเงิน: บัญชีที่ไม่นับรายได้ (Otteri ร้านเกอิชา) · ร้านที่แม่บ้านทำงานฟรีเองไม่ได้ · โหมดแอดมิน (งานภายในเท่านั้น)
const freeAccount = (o, config) => { const a = accountOf(o, config); return !!(a && a.noRevenue); };
const isFreeJob = (o, config) => isInternalOrder(o) || freeAccount(o, config);
const maidNoFree = (config) => !!(config && config.maidNoFree);
const isAdminStaff = (st) => !!(st && st.role === 'admin' && !st.isOwnerLogin);
const acctWord = (config, a) => tr(config, a && a.noRevenue ? 'ไม่คิดเงิน' : 'ค้างจ่าย');""", 'helpers')
rep("""const internalOwnerOnly = (config) => INTERNAL_OWNER_ONLY.filter(t => !((config && config.maidInternal) || []).includes(t));""",
    """const internalOwnerOnly = (config) => (config && config.maidNoFree ? INTERNAL_TYPES.map(t => t.id) : INTERNAL_OWNER_ONLY.filter(t => !((config && config.maidInternal) || []).includes(t))); // v181 maidNoFree = งานภายในทุกชนิดเป็นของแอดมิน/เจ้าของ""", 'internalOwnerOnly')

# ---------- 3) หน้าแรกแม่บ้าน: ซ่อนปุ่มงานฟรี (maidNoFree) ----------
rep("""          menuOn(config, 'internal') && { k: 'clean', icon: ownerNow ? '🔧' : '🧼',""",
    """          menuOn(config, 'internal') && (ownerNow || !maidNoFree(config)) && { k: 'clean', icon: ownerNow ? '🔧' : '🧼',""", 'tile clean')
rep("""          menuOn(config, 'internal') && config.ownerLaundry && { k: 'mine',""",
    """          menuOn(config, 'internal') && config.ownerLaundry && (ownerNow || !maidNoFree(config)) && { k: 'mine',""", 'tile mine')
rep("""          ...(config.accounts || []).map(a => ({ k: 'acct-' + a.id, icon: a.emoji || '🏢', title: tr(config, a.name), sub: tr(config, a.noFold ? 'ค้างจ่าย · ไม่พับ' : 'ค้างจ่าย'), on: false,""",
    """          ...(config.accounts || []).filter(a => ownerNow || !(a.noRevenue && maidNoFree(config))).map(a => ({ k: 'acct-' + a.id, icon: a.emoji || '🏢', title: tr(config, a.name), sub: tr(config, a.noRevenue ? (a.noFold ? 'ไม่คิดเงิน · ไม่พับ' : 'ไม่คิดเงิน') : (a.noFold ? 'ค้างจ่าย · ไม่พับ' : 'ค้างจ่าย')), on: false,""", 'tile accounts')
rep("""      {pulseOn(config) && <HomePulseStartCard config={config} orders={orders} />}""",
    """      {pulseOn(config) && <HomePulseStartCard config={config} orders={maidNoFree(config) && !ownerNow ? (orders || []).filter(o => !isFreeJob(o, config)) : orders} />}""", 'maid start card filter')
rep("""    if (o.paymentMethod === 'account') return { t: o.collected ? 'ค้างจ่าย · รับแล้ว' : 'ค้างจ่าย', c: '#0369A1', bg: '#E0F2FE' };""",
    """    if (o.paymentMethod === 'account') return freeAccount(o, config) ? { t: 'ไม่คิดเงิน', c: '#475569', bg: '#F1F5F9' } : { t: o.collected ? 'ค้างจ่าย · รับแล้ว' : 'ค้างจ่าย', c: '#0369A1', bg: '#E0F2FE' };""", 'rowStatus')

# ---------- 4) NewOrderView: แอดมิน = ลงงานภายในได้เหมือนเจ้าของ ----------
sig = "function NewOrderView({ config, onCancel, onSubmit, editingOrder, isOwner, internalMode, backdateDay, orders, draft, accountMode }) {"
assert s.count(sig) == 1
a = s.index(sig) + len(sig)
b = s.index('\nfunction ', a)
body = s[a:b]
n = len(re.findall(r'\bisOwner\b', body)); assert n == 17, f'NewOrderView isOwner: {n}'
body = re.sub(r'\bisOwner\b', 'freeOk', body)
s = s[:a] + body + s[b:]
rep("""  const maidClean = !!internalType && internalType === 'clean' && !freeOk;""",
    """  const maidClean = !!internalType && internalType === 'clean' && !isOwner; // v181 แอดมินใช้ฟอร์มล้างเครื่องแบบง่าย (แตะเครื่องซัก = ใส่รายการให้) เหมือนแม่บ้าน""", 'maidClean admin')
rep("""const dryNo = internalType === 'clean' && !freeOk && /^d/i.test(m.id);""", """const dryNo = internalType === 'clean' && !isOwner && /^d/i.test(m.id);""", 'dryNo admin')
rep("""{tr(config, "โหมดเจ้าของ — วันเวลารับงาน")}""", """{tr(config, isOwner ? "โหมดเจ้าของ — วันเวลารับงาน" : "วันเวลาที่ทำงาน")}""", 'time title admin')
rep(sig, """function NewOrderView({ config, onCancel, onSubmit, editingOrder, isOwner, isAdmin, internalMode, backdateDay, orders, draft, accountMode }) {
  const freeOk = isOwner || !!isAdmin; // 🔧 v181 แอดมิน = ลงงานภายใน/งานไม่คิดเงินได้ (เดิมใช้ isOwner ทั้งฟอร์ม)""", 'NewOrderView sig')
rep("""  const acct = internalType || !accountId ? null : (((config.accounts || []).find(a => a.id === accountId)) || (editingOrder && editingOrder.paymentMethod === 'account' ? { id: accountId, name: editingOrder.customerName || '' } : null));""",
    """  const acct = internalType || !accountId ? null : (((config.accounts || []).find(a => a.id === accountId)) || (editingOrder && editingOrder.paymentMethod === 'account' ? { id: accountId, name: editingOrder.customerName || '' } : null));
  const acctPayLong = acct ? tr(config, acct.noRevenue ? 'งานร้าน · ไม่คิดเงิน · ไม่นับรายได้' : 'ค้างจ่าย รวมบิลสิ้นเดือน · ไม่ต้องรับเงิน') : ''; // 🆓 v181""", 'acctPayLong')
rep("tr(config, 'ค้างจ่าย รวมบิลสิ้นเดือน · ไม่ต้องรับเงิน')}", "acctPayLong}", 'acct long texts', count=2)
rep("""    if (internalOwnerOnly(config).includes(internalType)) internalMaidIssues.push('ซ่อม/ทดสอบ ซักซ้ำ และอื่นๆ — เฉพาะเจ้าของ');""",
    """    if (internalOwnerOnly(config).includes(internalType)) internalMaidIssues.push(maidNoFree(config) ? tr(config, 'งานไม่คิดเงิน — แอดมินหรือเจ้าของเป็นคนลง') : 'ซ่อม/ทดสอบ ซักซ้ำ และอื่นๆ — เฉพาะเจ้าของ');""", 'maid issue text')
rep("""  const canSubmit = isInternal
    ? internalOk && internalMaidIssues.length === 0
    : (hasAnyItem && nameOk && phoneOk && (!useLinePromo || promoPhotoOk));""",
    """  const freeLocked = !freeOk && !!acct && !!acct.noRevenue && maidNoFree(config); // 🔒 v181 แม่บ้านลงงานไม่คิดเงินไม่ได้
  const canSubmit = isInternal
    ? internalOk && internalMaidIssues.length === 0
    : (hasAnyItem && nameOk && phoneOk && (!useLinePromo || promoPhotoOk) && !freeLocked);""", 'canSubmit')
rep("""  internalMaidIssues.forEach(t => missingList.push(t));""",
    """  internalMaidIssues.forEach(t => missingList.push(t));
  if (freeLocked) missingList.push(tr(config, 'งานไม่คิดเงิน — แอดมินหรือเจ้าของเป็นคนลง'));""", 'missing freeLocked')
rep("""            {(config.accounts || []).map(a => (
              <button key={a.id} data-account={a.id} onClick={() => pickAccount(accountId === a.id ? null : a.id)}""",
    """            {(config.accounts || []).filter(a => freeOk || !(a.noRevenue && maidNoFree(config))).map(a => (
              <button key={a.id} data-account={a.id} onClick={() => pickAccount(accountId === a.id ? null : a.id)}""", 'account chips filter')
rep("""{accountId === a.id ? '✓ ' : ''}{a.emoji || '🏢'} {tr(config, a.name)} · {tr(config, 'ค้างจ่าย')}""",
    """{accountId === a.id ? '✓ ' : ''}{a.emoji || '🏢'} {tr(config, a.name)} · {acctWord(config, a)}""", 'account chip word')
rep("""{acct.emoji || '🏢'} {tr(config, 'ค้างจ่าย')} · {tr(config, acct.name)}</p>""",
    """{acct.emoji || '🏢'} {acctWord(config, acct)} · {tr(config, acct.name)}</p>""", 'pay section title')
rep("""{tr(config, 'ไม่ต้องรับเงิน ไม่ต้องให้สแกน — เจ้าของเก็บรวมสิ้นเดือน')}""",
    """{tr(config, acct.noRevenue ? 'ไม่ต้องรับเงิน ไม่ต้องให้สแกน — ไม่นับรายได้' : 'ไม่ต้องรับเงิน ไม่ต้องให้สแกน — เจ้าของเก็บรวมสิ้นเดือน')}""", 'pay section sub')
rep("""{tr(config, 'ยอดลงบิล')}""", """{tr(config, acct.noRevenue ? 'มูลค่างาน' : 'ยอดลงบิล')}""", 'pay section amount')
rep("""(acct ? tr(config, 'ค้างจ่าย') + ' · ' + tr(config, acct.name) :""",
    """(acct ? acctWord(config, acct) + ' · ' + tr(config, acct.name) :""", 'total bar word')

# ---------- 5) ป้ายอื่นๆ ----------
rep("""{order.paymentMethod === 'account' ? '🏢 ค้างจ่าย' : order.paymentMethod === 'transfer' ? '💳 โอน' : '💵 สด'}""",
    """{order.paymentMethod === 'account' ? (freeAccount(order, config) ? '🏢 ไม่คิดเงิน' : '🏢 ค้างจ่าย') : order.paymentMethod === 'transfer' ? '💳 โอน' : '💵 สด'}""", 'detail badge')
rep("""<span>{tr(config, 'รวมในบิลค้างจ่าย')}</span>""",
    """<span>{tr(config, freeAccount(job.order, config) ? 'ไม่คิดเงิน' : 'รวมในบิลค้างจ่าย')}</span>""", 'extra time tile')

rep("""                <p className="text-sm font-bold mt-0.5">ค้างจ่าย · รวมบิลสิ้นเดือน{(config.accounts || []).find(a => a.id === order.accountId)?.noFold ? ' · ไม่พับ' : ''}</p>""",
    """                <p className="text-sm font-bold mt-0.5">{freeAccount(order, config) ? 'ไม่คิดเงิน · ไม่นับรายได้' : 'ค้างจ่าย · รวมบิลสิ้นเดือน'}{(config.accounts || []).find(a => a.id === order.accountId)?.noFold ? ' · ไม่พับ' : ''}</p>""", 'receipt band')

# ---------- 6) เริ่มเครื่อง: แอดมินเริ่มงานภายในได้ · แม่บ้านเริ่มงานไม่คิดเงินไม่ได้ ----------
rep("""  if (selM && job && internalOwnerOnly(config).includes(job.order.internalType) && !owner && !block) block = tr(config, 'งานภายในนี้ เจ้าของเป็นคนเริ่มเครื่อง'); // v151/v154: ซ่อม/ทดสอบ ซักซ้ำ อื่นๆ""",
    """  const adminOk = isAdminStaff(currentStaffLS(config)); // 🔧 v181 แอดมิน = เริ่มเครื่องงานภายในได้
  if (selM && job && internalOwnerOnly(config).includes(job.order.internalType) && !owner && !adminOk && !block) block = tr(config, maidNoFree(config) ? 'งานไม่คิดเงิน — แอดมินหรือเจ้าของเป็นคนเริ่มเครื่อง' : 'งานภายในนี้ เจ้าของเป็นคนเริ่มเครื่อง'); // v151/v154: ซ่อม/ทดสอบ ซักซ้ำ อื่นๆ
  if (selM && job && maidNoFree(config) && freeAccount(job.order, config) && !owner && !adminOk && !block) block = tr(config, 'งานไม่คิดเงิน — แอดมินหรือเจ้าของเป็นคนเริ่มเครื่อง'); // v181 งานเกอิชา""", 'start block')

# กระทบยอด: งานภายใน/ไม่คิดเงินของร้าน maidNoFree = งานแอดมิน → เตือน (warn) ไม่บังคับแม่บ้านใส่เหตุผล/กันออกจากระบบ
rep("""    const fresh = dateKey === dateKeyOf(new Date()) && Date.now() - (o.createdAt || 0) < 3 * 3600000;
    allocatePulseLogs(o, config, live.filter(l => l.refId === o.id)).mismatches
      .forEach(mm => add(`m:${o.id}:${mm.logId}`, 'error', 'เครื่องไม่ตรงใบงาน',""",
    """    const fresh = dateKey === dateKeyOf(new Date()) && Date.now() - (o.createdAt || 0) < 3 * 3600000;
    const lv = maidNoFree(config) && isFreeJob(o, config) ? 'warn' : 'error'; // 🔧 v181 งานแอดมิน → เตือนเฉยๆ
    allocatePulseLogs(o, config, live.filter(l => l.refId === o.id)).mismatches
      .forEach(mm => add(`m:${o.id}:${mm.logId}`, lv, 'เครื่องไม่ตรงใบงาน',""", 'recon lv mismatch')
rep("""    if (fired < need) add(`o:${o.id}:${need - fired}`, 'error', fired === 0""", """    if (fired < need) add(`o:${o.id}:${need - fired}`, lv, fired === 0""", 'recon lv not started')
rep("""    if (pulseExcess > 0) add(`o:${o.id}:+${pulseExcess}`, 'error',""", """    if (pulseExcess > 0) add(`o:${o.id}:+${pulseExcess}`, lv,""", 'recon lv excess')

# ใบงานภายใน/ไม่คิดเงิน ที่แม่บ้านเปิดดู → แจ้งว่าแอดมิน/เจ้าของเป็นคนเริ่มเครื่อง (แทนปุ่มเลือกเครื่อง)
rep("""  const order = liveOrder && orderProp && liveOrder.id === orderProp.id ? { ...orderProp, ...liveOrder } : orderProp;""",
    """  const order = liveOrder && orderProp && liveOrder.id === orderProp.id ? { ...orderProp, ...liveOrder } : orderProp;
  const adminJobLocked = !!order && maidNoFree(config) && isFreeJob(order, config) && !pulseIsOwnerNow(config, isOwner) && !isAdminStaff(currentStaffLS(config)); // 🔒 v181""", 'starter lock flag')
rep("""      <button onClick={() => setPicker({ preset: null, retryLog: null })} disabled={!!busy}""",
    """      {adminJobLocked ? <p data-admin-job-lock className="mt-3 rounded-xl bg-slate-100 text-slate-700 text-sm font-bold px-3 py-3 text-center">🔒 {tr(config, 'งานไม่คิดเงิน — แอดมินหรือเจ้าของเป็นคนเริ่มเครื่อง')}</p> : (
      <button onClick={() => setPicker({ preset: null, retryLog: null })} disabled={!!busy}""", 'starter lock open')
rep("""      </button>
      {!allDone && <p className="text-[11px] text-slate-500 mt-1.5 text-center">{tr(config, 'ยังไม่ต้องเริ่มตอนนี้ก็ได้""",
    """      </button>)}
      {!allDone && !adminJobLocked && <p className="text-[11px] text-slate-500 mt-1.5 text-center">{tr(config, 'ยังไม่ต้องเริ่มตอนนี้ก็ได้""", 'starter lock close')

# ---------- 7) หน้าเจ้าของ: งานไม่คิดเงิน = งานภายใน ----------
rep("""mine: 0, mineN: 0, account: 0, accountN: 0,
    over: 0,""", """mine: 0, mineN: 0, account: 0, accountN: 0, free: 0, freeN: 0,
    over: 0,""", 'PB init')
rep("""    if (o.paymentMethod === 'account') { B.account += t + manual; if (t + manual > 0) B.accountN++; } else B.transfer += t + manual;""",
    """    if (freeAccount(o, config)) { B.free += t + manual; if (t + manual > 0) B.freeN++; } // 🆓 v181 งานไม่คิดเงิน (ร้านเกอิชา)
    else if (o.paymentMethod === 'account') { B.account += t + manual; if (t + manual > 0) B.accountN++; } else B.transfer += t + manual;""", 'PB account')
rep("""  B.total = B.cash + B.transfer + B.discount + B.clean + B.repair + B.redo + B.mine + B.account + B.refire + B.over;""",
    """  B.total = B.cash + B.transfer + B.discount + B.clean + B.repair + B.redo + B.mine + B.account + B.free + B.refire + B.over;""", 'PB total')
rep("""...(PB.mine ? [['internal', 'ผ้าเจ้าของ', PB.mine]] : []), ...(PB.account ?""",
    """...(PB.mine ? [['internal', 'ผ้าเจ้าของ', PB.mine]] : []), ...(PB.free ? [['internal', 'ไม่คิดเงิน · ' + (config.accounts || []).filter(a => a.noRevenue).map(a => a.name).join('/'), PB.free]] : []), ...(PB.account ?""", 'PB rows')
rep("""      A.ilist.push(o);
      return;
    }
    const b = calculateBreakdown(o, config);
    A.jobs++; A.sales += b.total; A.list.push(o);""",
    """      A.ilist.push(o);
      return;
    }
    if (freeAccount(o, config)) { // 🆓 v181 งานไม่คิดเงิน (ร้านเกอิชา) = งานภายใน ไม่นับยอดขาย/ค้างจ่าย
      const v = calculateTotal(o, config), k = 'acct_' + o.accountId;
      A.internal += v; A.internalN++;
      A.intType[k] = A.intType[k] || { n: 0, v: 0 };
      A.intType[k].n++; A.intType[k].v += v;
      A.ilist.push(o);
      return;
    }
    const b = calculateBreakdown(o, config);
    A.jobs++; A.sales += b.total; A.list.push(o);""", 't2Agg free')
rep("""  const accPendList = cust.filter(o => o.paymentMethod === 'account' && !o.collected); // 🏢""",
    """  const accPendList = cust.filter(o => o.paymentMethod === 'account' && !o.collected && !freeAccount(o, config)); // 🏢 (v181 ไม่รวมงานไม่คิดเงิน)""", 'todo account')
rep("""            {(config.accounts || []).map(a => {
              const mine = accAll.filter(o => o.accountId === a.id);""",
    """            {(config.accounts || []).map(a => {
              const mine = accAll.filter(o => o.accountId === a.id);
              if (a.noRevenue) { const per = mine.filter(inR); return ( // 🆓 v181 งานไม่คิดเงิน — ดูมูลค่าอย่างเดียว ไม่มีปุ่มรับเงิน
                <T2Box key={a.id} k="internal" title={`${a.emoji || '🏢'} ${a.name} · ${R.label}`} right={<span className="text-xs font-bold text-slate-500">ไม่นับรายได้</span>}>
                  <div className="grid grid-cols-2 gap-2" data-free-account={a.id}>
                    <T2Stat label="มูลค่างาน" value={'฿' + formatMoney(sumOf(per))} sub={`${per.length} ใบ`} />
                    <T2Stat label="ทั้งหมด" value={`${mine.length} ใบ`} />
                  </div>
                  <p className="text-[11px] text-slate-500 mt-1.5">งานร้าน ไม่ต้องเก็บเงิน · แอดมิน/เจ้าของเป็นคนลงและเริ่มเครื่อง · ดูรายการที่ งานภายใน</p>
                </T2Box>); }""", 'account tab free')
rep("""                {internalTypesFor(config).map(t => (
                  <T2Stat key={t.id} label={`${t.emoji} ${t.label}`} value={'฿' + formatMoney((A.intType[t.id] || {}).v || 0)} sub={`${(A.intType[t.id] || {}).n || 0} งาน`} />
                ))}""",
    """                {internalTypesFor(config).map(t => (
                  <T2Stat key={t.id} label={`${t.emoji} ${t.label}`} value={'฿' + formatMoney((A.intType[t.id] || {}).v || 0)} sub={`${(A.intType[t.id] || {}).n || 0} งาน`} />
                ))}
                {(config.accounts || []).filter(a => a.noRevenue).map(a => (
                  <T2Stat key={'acct_' + a.id} label={`${a.emoji || '🏢'} ${a.name}`} value={'฿' + formatMoney((A.intType['acct_' + a.id] || {}).v || 0)} sub={`${(A.intType['acct_' + a.id] || {}).n || 0} งาน`} />
                ))}""", 'internal tab free stats')

# ---------- 8) จัดการรายชื่อ: ตั้งแอดมิน ----------
rep("""  const [newAvatar, setNewAvatar] = useState({ skin: 0, hair: 0, hairColor: 0, sex: 'f' });
  const [editingStaffId, setEditingStaffId]""",
    """  const [newAvatar, setNewAvatar] = useState({ skin: 0, hair: 0, hairColor: 0, sex: 'f' });
  const [newAdmin, setNewAdmin] = useState(false); // 🔧 v181 แอดมิน = งานภายในเท่านั้น
  const [editingStaffId, setEditingStaffId]""", 'newAdmin state')
rep("""      await saveStaffToCloud(config.brand, { name, pin: newPin, avatar: newAvatar, active: true, createdAt: Date.now() });
      setNewName('');
      setNewPin('');""",
    """      await saveStaffToCloud(config.brand, { name, pin: newPin, avatar: newAvatar, active: true, createdAt: Date.now(), ...(newAdmin ? { role: 'admin' } : {}) });
      setNewAdmin(false);
      setNewName('');
      setNewPin('');""", 'save role')
# หน้าตั้งค่าเจ้าของ (SettingsView): ปุ่ม แม่บ้าน⇄แอดมิน
rep("""                <p className="text-[11px] text-slate-400">PIN ****</p>
              </div>
              <button onClick={() => openEditStaff(s)} className="text-[11px] font-bold text-sky-600 px-2 py-1">แก้ไข</button>""",
    """                <p className="text-[11px] text-slate-400">PIN ****{s.role === 'admin' ? ' · 🔧 แอดมิน (งานภายในเท่านั้น)' : ''}</p>
              </div>
              <button data-role-toggle={s.id} onClick={() => updateStaffInCloud(s.id, { role: s.role === 'admin' ? null : 'admin' }).catch(e => alert('อัปเดตไม่สำเร็จ: ' + e.message))}
                className={`text-[11px] font-bold px-2 py-1 rounded-lg ${s.role === 'admin' ? 'bg-indigo-100 text-indigo-700' : 'text-slate-500'}`}>{s.role === 'admin' ? '🔧 แอดมิน' : 'แม่บ้าน'}</button>
              <button onClick={() => openEditStaff(s)} className="text-[11px] font-bold text-sky-600 px-2 py-1">แก้ไข</button>""", 'settings role toggle')
rep("""              <button onClick={handleAddStaff} className="w-full py-2 rounded-xl text-white font-bold text-sm active:scale-95 transition" style={{ background: config.gradient }}>""",
    """              <label className="flex items-start gap-2 mb-2 text-xs font-bold text-slate-700" data-new-admin>
                <input type="checkbox" className="mt-0.5" checked={newAdmin} onChange={(e) => setNewAdmin(e.target.checked)} />
                <span>🔧 {tr(config, 'แอดมิน — เห็นและลงได้แค่งานภายใน (ล้างเครื่อง ซ่อม ผ้าเจ้าของ งานไม่คิดเงิน)')}</span>
              </label>
              <button onClick={handleAddStaff} className="w-full py-2 rounded-xl text-white font-bold text-sm active:scale-95 transition" style={{ background: config.gradient }}>""", 'admin checkbox')
rep("""                      <p className="text-xs text-slate-400">PIN: {s.pin}</p>
                    </div>
                    <button
                      onClick={() => handleStartEdit(s)}""",
    """                      <p className="text-xs text-slate-400">PIN: {s.pin}</p>
                    </div>
                    <button data-role-toggle={s.id} onClick={() => updateStaffInCloud(s.id, { role: s.role === 'admin' ? null : 'admin' }).catch(e => alert('อัปเดตไม่สำเร็จ: ' + e.message))}
                      className={`text-xs font-bold px-2.5 py-1 rounded-lg ${s.role === 'admin' ? 'bg-indigo-100 text-indigo-700' : 'bg-slate-100 text-slate-500'}`}>
                      {s.role === 'admin' ? '🔧 ' + tr(config, 'แอดมิน') : tr(config, 'แม่บ้าน')}
                    </button>
                    <button
                      onClick={() => handleStartEdit(s)}""", 'role toggle')
rep("""                    <span className="font-bold text-slate-800 text-sm">{s.name}</span>""",
    """                    <span className="font-bold text-slate-800 text-sm">{s.name}</span>
                    {s.role === 'admin' && <span className="text-[10px] font-bold text-indigo-700">🔧 {tr(config, 'แอดมิน · งานภายใน')}</span>}""", 'pick badge')

# ---------- 9) App: เปิดหน้าแอดมิน ----------
rep("""  const handleStaffLogin = (staff) => {""",
    """  const isAdminUser = !isOwner && isAdminStaff((staffList || []).find(x => x.id === (currentStaff && currentStaff.id)) || currentStaff); // 🔧 v181 โหมดแอดมิน (role ล่าสุดจากรายชื่อ)
  const handleStaffLogin = (staff) => {""", 'isAdminUser')
rep("""    if (gate && gate.needReason && currentStaff && !currentStaff.isOwnerLogin && !currentStaff.previewOwner) {""",
    """    if (gate && gate.needReason && currentStaff && !currentStaff.isOwnerLogin && !currentStaff.previewOwner && !isAdminUser) {""", 'gate admin')
rep("""      {view === 'home' && <HomeView """,
    """      {view === 'home' && isAdminUser && <AdminHomeView config={config} orders={orders} currentStaff={currentStaff} onSwitchStaff={handleSwitchStaff} onToggleLang={toggleLang}
        onInternalOrder={(t) => { setOrderDraft(null); setAccountMode(null); setInternalMode(typeof t === 'string' ? t : true); setBackdateDay(null); setView('newOrder'); }}
        onAccountOrder={(id) => { setOrderDraft(null); setInternalMode(false); setAccountMode(id); setBackdateDay(null); setView('newOrder'); }}
        onSelectOrder={(o) => { setSelectedOrder(o); setView('receipt'); }} />}
      {view === 'home' && !isAdminUser && <HomeView """, 'home route')
rep("""onSubmit={handleNewOrder} isOwner={isOwner} internalMode={internalMode} />}""",
    """onSubmit={handleNewOrder} isOwner={isOwner} isAdmin={isAdminUser} internalMode={internalMode} />}""", 'newOrder isAdmin')

# ---------- 10) AdminHomeView ----------
rep("""function HomePulseStartCard({ config, orders }) {""",
    """// 🔧 v181 โหมดแอดมิน — ช่องทางพิเศษสำหรับงานภายในโดยเฉพาะ (ล้างเครื่อง · ซ่อม/ทดสอบ · ซักซ้ำ · ผ้าเจ้าของ · งานไม่คิดเงิน เช่น ร้านเกอิชา)
// แอดมินหลายคนช่วยกดได้ (เจ้าของตั้งใน ⚙️ จัดการรายชื่อ) · เห็นแค่งานภายใน ไม่เห็นงานลูกค้า/เงิน · ไม่นับรายได้
const ADMIN_BTN_SUB = { clean: 'ล้างถังเครื่องซัก', test: 'ตอนช่างมา/เช็กเครื่อง', redo: 'เครื่องมีปัญหา ซักให้ใหม่', mine: 'ไม่นับรายได้', other: 'ใส่เหตุผล' };
function AdminHomeView({ config, orders, currentStaff, onSwitchStaff, onToggleLang, onInternalOrder, onAccountOrder, onSelectOrder }) {
  const [dayOff, setDayOff] = useState(0);
  const freeOrders = useMemo(() => (orders || []).filter(o => isFreeJob(o, config)), [orders, config]);
  const from = (() => { const d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() - dayOff); return d.getTime(); })();
  const list = freeOrders.filter(o => (o.createdAt || 0) >= from && (o.createdAt || 0) < from + 86400000).sort((x, y) => (y.createdAt || 0) - (x.createdAt || 0));
  const btns = [
    ...internalTypesFor(config).filter(t => t.id !== 'fix').map(t => ({ k: t.id, icon: t.emoji, title: tr(config, (BILL_BTN[t.id] || [t.label])[0]), sub: tr(config, ADMIN_BTN_SUB[t.id] || 'ไม่นับรายได้'), click: () => onInternalOrder(t.id) })),
    ...(config.accounts || []).filter(a => a.noRevenue).map(a => ({ k: 'acct-' + a.id, icon: a.emoji || '🏢', title: tr(config, a.name), sub: tr(config, a.noFold ? 'ไม่คิดเงิน · ไม่พับ' : 'ไม่คิดเงิน'), click: () => onAccountOrder(a.id) })),
  ];
  const titleOf = (o) => (isInternalOrder(o) ? internalTitleOf(o, config) : `${(accountOf(o, config) || {}).emoji || '🏢'} ${tr(config, o.customerName || '')}`);
  const days = [tr(config, 'วันนี้'), tr(config, 'เมื่อวาน'), tr(config, '2 วันก่อน')];
  return (
    <div className="min-h-screen bg-slate-50 pb-28" data-admin-home>
      <div className="px-5 pt-6 pb-5 text-white" style={{ background: 'linear-gradient(135deg, #1E293B 0%, #334155 100%)' }}>
        <div className="flex items-center gap-3">
          <img src={config.logo} alt="logo" className="w-11 h-11 rounded-xl bg-white flex-shrink-0" />
          <div className="flex-1 min-w-0">
            <p className="text-lg font-extrabold leading-tight">🔧 {tr(config, 'โหมดแอดมิน')}</p>
            <p className="text-xs text-slate-300 truncate">{config.name} · {currentStaff && currentStaff.name}</p>
          </div>
          <button onClick={onToggleLang} className="px-2.5 py-1.5 rounded-full bg-white bg-opacity-10 text-[11px] font-bold flex-shrink-0">{config.lang === 'mm' ? 'TH' : 'MM'}</button>
          <button onClick={onSwitchStaff} data-admin-logout className="px-3 py-1.5 rounded-full bg-white text-slate-900 text-xs font-extrabold active:scale-95 flex-shrink-0">{tr(config, 'สลับผู้ใช้')}</button>
        </div>
        <p className="text-xs font-bold text-amber-300 mt-3">{tr(config, 'งานภายในเท่านั้น · ไม่นับรายได้')}</p>
      </div>
      {pulseOn(config) && <HomePulseStartCard config={config} orders={freeOrders} />}
      <div className="px-5 mt-4">
        <p className="text-sm font-extrabold text-slate-900 mb-2">➕ {tr(config, 'ลงงานภายใน')}</p>
        <div className="grid grid-cols-2 gap-2">
          {btns.map(x => (
            <button key={x.k} data-admin-btn={x.k} onClick={x.click} className="rounded-2xl bg-white border border-slate-200 px-3 py-3 flex items-center gap-2.5 text-left active:scale-95 transition min-w-0">
              <span className="text-2xl leading-none flex-shrink-0">{x.icon}</span>
              <span className="min-w-0"><span className="block text-sm font-extrabold text-slate-900">{x.title}</span><span className="block text-[11px] text-slate-500 leading-snug">{x.sub}</span></span>
            </button>
          ))}
        </div>
      </div>
      <div className="px-5 mt-5">
        <div className="flex gap-1.5 mb-2">
          {days.map((lb, i) => (
            <button key={i} data-admin-day={i} onClick={() => setDayOff(i)} className={`px-3 py-1.5 rounded-full text-xs font-bold border ${dayOff === i ? 'bg-slate-900 text-white border-slate-900' : 'bg-white text-slate-600 border-slate-200'}`}>{lb}</button>
          ))}
        </div>
        <div className="space-y-2" data-admin-list>
          {list.map(o => (
            <button key={o.id} onClick={() => onSelectOrder(o)} className="w-full rounded-xl bg-white border border-slate-200 px-3 py-2.5 flex items-center gap-3 text-left active:scale-[0.98]">
              <div className="flex-1 min-w-0">
                <p className="text-sm font-extrabold text-slate-900 truncate">{titleOf(o)}</p>
                <p className="text-xs text-slate-500 truncate">{fmtTime(o.createdAt)} · {o.staffName || '-'}{o.internalReason ? ' · ' + o.internalReason : ''}</p>
              </div>
              <span className="text-sm font-extrabold text-slate-500 tabular-nums">฿{formatMoney(calculateTotal(o, config))}</span>
            </button>
          ))}
          {list.length === 0 && <p className="text-sm text-slate-500 py-3 text-center">{tr(config, 'ยังไม่มีงานภายใน')}</p>}
        </div>
      </div>
    </div>
  );
}

function HomePulseStartCard({ config, orders }) {""", 'AdminHomeView')

# ---------- 11) MM ----------
rep("""  'ไม่นับเป็นรายได้': 'ဝင်ငွေအဖြစ် မရေတွက်', // v177""",
    """  'ไม่นับเป็นรายได้': 'ဝင်ငွေအဖြစ် မရေတွက်', // v177
  // v181 โหมดแอดมิน · งานไม่คิดเงิน
  'ไม่คิดเงิน': 'ငွေမယူ',
  'ไม่คิดเงิน · ไม่พับ': 'ငွေမယူ · မခေါက်',
  'ไม่นับรายได้': 'ဝင်ငွေ မတွက်',
  'งานร้าน · ไม่คิดเงิน · ไม่นับรายได้': 'ဆိုင်အလုပ် · ငွေမယူ · ဝင်ငွေ မတွက်',
  'ไม่ต้องรับเงิน ไม่ต้องให้สแกน — ไม่นับรายได้': 'ငွေမယူရ · စကင်မလုပ်ရ — ဝင်ငွေ မတွက်',
  'มูลค่างาน': 'အလုပ်တန်ဖိုး',
  'งานไม่คิดเงิน — แอดมินหรือเจ้าของเป็นคนลง': 'ငွေမယူသောအလုပ် — အက်ဒမင် (သို့) ပိုင်ရှင်က ထည့်ရမည်',
  'งานไม่คิดเงิน — แอดมินหรือเจ้าของเป็นคนเริ่มเครื่อง': 'ငွေမယူသောအလုပ် — အက်ဒမင် (သို့) ပိုင်ရှင်က စက်စတင်ရမည်',
  'โหมดแอดมิน': 'အက်ဒမင် မုဒ်',
  'งานภายในเท่านั้น · ไม่นับรายได้': 'ဆိုင်တွင်းအလုပ်သာ · ဝင်ငွေ မတွက်',
  'ลงงานภายใน': 'ဆိုင်တွင်းအလုပ် ထည့်ရန်',
  'ล้างถังเครื่องซัก': 'အဝတ်လျှော်စက် ကန်ဆေးရန်',
  'ตอนช่างมา/เช็กเครื่อง': 'ပြင်ဆင်သူလာချိန် / စက်စစ်ချိန်',
  'เครื่องมีปัญหา ซักให้ใหม่': 'စက်ပြဿနာ · ပြန်လျှော်ပေး',
  'ซักซ้ำให้ลูกค้า': 'ဖောက်သည်အတွက် ပြန်လျှော်',
  '2 วันก่อน': '၂ ရက်က',
  'ยังไม่มีงานภายใน': 'ဆိုင်တွင်းအလုပ် မရှိသေး',
  'แอดมิน': 'အက်ဒမင်',
  'วันเวลาที่ทำงาน': 'အလုပ်လုပ်သည့် ရက်/အချိန်',
  'แอดมิน · งานภายใน': 'အက်ဒမင် · ဆိုင်တွင်းအလုပ်',
  'แอดมิน — เห็นและลงได้แค่งานภายใน (ล้างเครื่อง ซ่อม ผ้าเจ้าของ งานไม่คิดเงิน)': 'အက်ဒမင် — ဆိုင်တွင်းအလုပ်သာ မြင်/ထည့်နိုင် (စက်ဆေး · ပြင် · ပိုင်ရှင်အဝတ် · ငွေမယူအလုပ်)',""", 'MM')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v181 applied')
