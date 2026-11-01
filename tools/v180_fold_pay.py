#!/usr/bin/env python3
"""v180 — หน้าเจ้าของแบบเท็ดดี้ 2: ค่าพับที่ต้องจ่ายแม่บ้าน (Otteri · config.foldPricePerBasket > 0)
ที่มา: เจ้าของ 1 พ.ย. 'ยอดเงินที่ต้องจ่ายฝากพับให้แม่บ้านหายไป' — หน้าเจ้าของเก่ามีแท็บ ค่าพับ (ส่วนของแม่บ้าน)
แต่ Otteri ย้ายมาหน้าเจ้าของใหม่ (v175) แล้วไม่มีกล่องนี้
- งาน → ฝากพับ: กล่อง 'ค่าพับค้างจ่ายแม่บ้าน ฿…' แยกรายคน (ตะกร้า × เรท) + ปุ่ม จ่าย ฿… (ใช้ handlePayFees('service') เดิม · ↶ ยกเลิกได้)
  + ประวัติรอบจ่ายค่าพับ
- ภาพรวม → ต้องจัดการ: 'ค่าพับค้างจ่ายแม่บ้าน ฿…'
- แก้ตัวนับ: ร้านที่คิดค่าพับ (ไม่ใช่ฝากพับฟรี) งานพับ = งานที่มีตะกร้าพับ — แยกตามแม่บ้าน/รายการ/มีส่งด้วย ใช้เกณฑ์เดียวกับตัวเลข 'งานพับ'
usage: python3 tools/v180_fold_pay.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v179-2026-11-01';", "window.APP_VERSION = 'v180-2026-11-01';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v179';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v179';", "const CACHE_NAME = 'plp-laundry-v180';")

# ข้อมูล: ค่าพับค้างจ่าย (ทุกช่วงเวลา ไม่ขึ้นกับวันที่ที่เลือก — เหมือนค่าไรเดอร์ค้างจ่าย)
rep("""  const riderUnpaid = riderUnpaidList.reduce((s, o) => s + riderFeeFor(o, config), 0);
  const rounds = (collections || [])""",
    """  const riderUnpaid = riderUnpaidList.reduce((s, o) => s + riderFeeFor(o, config), 0);
  // 🧺 v180 ค่าพับส่วนของแม่บ้าน (ร้านที่คิดค่าพับ เช่น Otteri) — จ่ายด้วย handlePayFees('service') เดิม
  const foldRate = config.foldPricePerBasket || 0;
  const foldUnpaidList = foldRate > 0 ? cust.filter(o => (o.foldBaskets || 0) > 0 && !o.serviceFeePaid) : [];
  const foldUnpaid = foldUnpaidList.reduce((s, o) => s + (o.foldBaskets || 0) * foldRate, 0);
  const rounds = (collections || [])""", 'fold unpaid data')
rep("""  if (riderUnpaid > 0) todo.push({ k: 'delivery',""",
    """  if (foldUnpaid > 0) todo.push({ k: 'fold', title: `ค่าพับค้างจ่ายแม่บ้าน ฿${formatMoney(foldUnpaid)}`, sub: `${foldUnpaidList.reduce((s, o) => s + (o.foldBaskets || 0), 0)} ตะกร้า × ฿${foldRate} · ${foldUnpaidList.length} ใบ`, nav: 'ดู', go: 'fold' });
  if (riderUnpaid > 0) todo.push({ k: 'delivery',""", 'todo fold')
rep("""  const doPayRider = async (riderId) => {""",
    """  const doPayFold = async () => { // 🧺 v180
    setBusy(true);
    try {
      const r = await onPayFees('service', null, { silent: true });
      if (r && r.id) showToast(`✓ ${t2RoundLabel('service')} ฿${formatMoney(r.total)} (${r.count} ใบ)`, () => undoRound({ ...r.round, id: r.id }, false));
    } finally { setBusy(false); }
  };
  const doPayRider = async (riderId) => {""", 'doPayFold')

# แท็บฝากพับ
rep("""                <T2Stat label="มีส่งด้วย" value={A.list.filter(o => !o.noFold && o.deliveryZone).length} />
              </div>
            </T2Box>
            <T2Box k="fold" title="แยกตามแม่บ้านที่รับงาน">
              {(() => {
                const m = {};
                A.list.filter(o => !o.noFold).forEach(o => {""",
    """                <T2Stat label="มีส่งด้วย" value={A.list.filter(o => isFoldJob(o) && o.deliveryZone).length} />
              </div>
            </T2Box>
            {foldRate > 0 && (
              <T2Box k="fold" title={foldUnpaid > 0 ? `ค่าพับค้างจ่ายแม่บ้าน ฿${formatMoney(foldUnpaid)}` : 'ค่าพับค้างจ่ายแม่บ้าน'} right={<span className="text-xs font-bold text-slate-500">ค้างทั้งหมด</span>}>
                <div data-fold-pay className="divide-y divide-slate-100">
                  {(() => {
                    const m = {};
                    foldUnpaidList.forEach(o => { const k = o.staffName || 'ไม่ระบุ'; m[k] = m[k] || { n: 0, b: 0 }; m[k].n++; m[k].b += (o.foldBaskets || 0); });
                    return Object.entries(m).sort((a, b) => b[1].b - a[1].b).map(([n, v]) => (
                      <div key={n} className="flex items-center gap-3 py-2">
                        <span className="text-2xl">🧹</span>
                        <div className="flex-1">
                          <p className="text-sm font-extrabold text-slate-900">{n}</p>
                          <p className="text-xs text-slate-500 tabular-nums">{v.b} ตะกร้า × ฿{foldRate} · {v.n} ใบ</p>
                        </div>
                        <span className="text-sm font-extrabold text-slate-900 tabular-nums">฿{formatMoney(v.b * foldRate)}</span>
                      </div>
                    ));
                  })()}
                  {foldUnpaidList.length === 0 && <p className="text-sm font-bold text-emerald-700 py-1">✓ ไม่มีค่าพับค้างจ่าย</p>}
                </div>
                {foldUnpaid > 0 && <div className="mt-2">{actBtn('fold', `จ่ายค่าพับ ฿${formatMoney(foldUnpaid)}`, doPayFold)}</div>}
                <p className="text-[11px] text-slate-500 mt-1.5">฿{foldRate} ต่อตะกร้าที่ลงค่าพับในใบงาน · จ่ายแล้วกด ↶ ยกเลิกได้</p>
              </T2Box>
            )}
            {foldRate > 0 && history(m => m === 'service', 'fold')}
            <T2Box k="fold" title="แยกตามแม่บ้านที่รับงาน">
              {(() => {
                const m = {};
                A.list.filter(isFoldJob).forEach(o => {""", 'fold tab box')
rep("""            {listHead(`งานพับ · ${R.label}`, A.foldN)}
            {list(A.list.filter(o => !o.noFold))}""",
    """            {listHead(`งานพับ · ${R.label}`, A.foldN)}
            {list(A.list.filter(isFoldJob))}""", 'fold list filter')
# เกณฑ์งานพับเดียวกับ t2Agg (foldN): ไม่ใช่ 'ไม่ให้พับ' และ (ฝากพับฟรี หรือ มีตะกร้าพับ)
rep("""  const doPayFold = async () => { // 🧺 v180""",
    """  const isFoldJob = (o) => !o.noFold && (!!config.freeService || (o.foldBaskets || 0) > 0);
  const doPayFold = async () => { // 🧺 v180""", 'isFoldJob')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v180 applied')
