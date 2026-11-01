#!/usr/bin/env python3
"""v188 — งานร้านเกอิชา กลับเข้าหน้าแอดมิน (ฟอร์มสั้นแบบเดียวกับงานภายใน) + ส่ง LINE อัตโนมัติ
ที่มา: เจ้าของ 2 พ.ย. 69 'เพิ่มงาน เกอิชา เข้าไปในโหมด แอดมิน พร้อมทำคู่มือ'
ทำอะไร (แอดมิน/เจ้าของ · ร้าน simpleInternal = Otteri)
  - หน้าแอดมิน: 5 ปุ่ม (4 งานภายใน + 🏢 ร้านเกอิชา)
  - ฟอร์มเกอิชา: กล่องเดียว — แตะเครื่อง (ซัก/อบ) → แอปใส่รายการให้ · มีเครื่องอบ = ปุ่ม ⏱️ เพิ่มเวลาอบ ±฿10
    ซ่อน: ข้อมูลลูกค้า · รูปตะกร้า · รายการเสริม · ส่วนเครื่องทุกขนาด · กล่องการชำระเงิน · กล่องเวลาใหญ่ (เหลือลิงก์เล็ก)
  - บันทึก: เก็บเครื่องที่แตะ (internalMachines) → ติ๊ก SOL ตรงเครื่อง · เพิ่มเวลาอบติ๊กเครื่องเดียวกัน
  - ใบรับงานเกอิชา (แอดมิน/เจ้าของ): เด้งหน้าแชร์ใบรับงานเข้า LINE ให้เลย (ไม่เด้ง = ปุ่มส่งเข้า Line ยังอยู่)
usage: python3 tools/v188_admin_geisha.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v187-2026-11-02';", "window.APP_VERSION = 'v188-2026-11-02';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v187';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v187';", "const CACHE_NAME = 'plp-laundry-v188';")

# ---------- หน้าแอดมิน: เกอิชากลับมา ----------
rep("""    ...(config.simpleInternal ? [] : config.accounts || []).filter(a => a.noRevenue).map(a =>""",
    """    ...(config.accounts || []).filter(a => a.noRevenue).map(a =>""", 'admin geisha button')

# ---------- NewOrderView: ฟอร์มสั้นงานเกอิชา ----------
rep("""  const [showTime, setShowTime] = useState(false); // 🧾 v185 ฟอร์มสั้น: กล่องเวลาเปิดเมื่อแตะ""",
    """  const [showTime, setShowTime] = useState(false); // 🧾 v185 ฟอร์มสั้น: กล่องเวลาเปิดเมื่อแตะ
  const [topUpAmt, setTopUpAmt] = useState(() => { const d = editingOrder && (editingOrder.dryItems || []).find(i => i.topUp > 0); return d ? d.topUp : 0; }); // ⏱️ v188 เพิ่มเวลาอบ (ฟอร์มสั้น)""", 'topUp state')
rep("""  const autoItems = maidClean || simpleFree;""",
    """  const simpleAcct = !internalType && !!acct && !!acct.noRevenue && freeOk && !!config.simpleInternal; // 🏢 v188 งานเกอิชา (แอดมิน/เจ้าของ) ฟอร์มสั้น
  const simpleMode = simpleFree || simpleAcct;
  const autoItems = maidClean || simpleFree || simpleAcct;""", 'simpleAcct')
rep("""    setDryItems(internalType === 'clean' ? [] : Object.keys(dBy).map(kg => ({ size: Number(kg), qty: dBy[kg] })).filter(i => config.dryMachines.some(d => d.size === i.size)));
  }, [autoItems, internalType, internalMachines.join('|')]);""",
    """    const dry = internalType === 'clean' ? [] : Object.keys(dBy).map(kg => ({ size: Number(kg), qty: dBy[kg] })).filter(i => config.dryMachines.some(d => d.size === i.size));
    if (dry.length && topUpAmt > 0) dry[0] = { ...dry[0], topUp: topUpAmt }; // ⏱️ v188
    setDryItems(dry);
  }, [autoItems, internalType, internalMachines.join('|'), topUpAmt]);""", 'effect topUp')
rep("""  if (!isInternal && !hasAnyItem) missingList.push(tr(config, 'เลือกบริการอย่างน้อย 1 อย่าง (ซัก / อบ / น้ำยา / พับ)'));""",
    """  if (!isInternal && !hasAnyItem) missingList.push(tr(config, simpleAcct ? 'เลือกเครื่องที่ทำ (บังคับ)' : 'เลือกบริการอย่างน้อย 1 อย่าง (ซัก / อบ / น้ำยา / พับ)'));""", 'missing acct')
rep("""        {simpleFree && !showTime && (""", """        {simpleMode && !showTime && (""", 'time toggle')
rep("""        {freeOk && (!simpleFree || showTime) && (""", """        {freeOk && (!simpleMode || showTime) && (""", 'time block')
rep("""        {!isInternal && !isEdit && (!config.ui2 || pendingWeb.length > 0 || !!webPicked) && (""",
    """        {simpleAcct && (
          <div className="rounded-2xl p-4 border-2 border-sky-300 bg-sky-50" data-simple-acct>
            <p className="font-extrabold text-slate-900">{acct.emoji || '🏢'} {tr(config, acct.name)}</p>
            <p className="text-xs font-bold text-sky-800 mb-3">{acctPayLong}{acct.noFold ? ' · ' + tr(config, 'ไม่พับ') : ''}</p>
            <p className="text-xs font-bold text-slate-700 mb-1.5">{tr(config, 'เครื่องที่ทำ')} <span className="text-rose-600">*{tr(config, 'บังคับ')}</span></p>
            <div className="flex flex-wrap gap-1.5 mb-3">
              {((COIN_POINTS[config.brand] || COIN_POINTS.teddy2).machines || []).map(m => {
                const on = internalMachines.includes(m.label);
                return (
                  <button key={m.id} data-acct-machine={m.id} onClick={() => setInternalMachines(on ? internalMachines.filter(x => x !== m.label) : [...internalMachines, m.label])}
                    className={`px-2.5 py-1 rounded-full text-xs font-bold border-2 ${on ? 'bg-slate-900 text-white border-slate-900' : 'bg-white text-slate-700 border-slate-300'}`}>{m.label}</button>
                );
              })}
            </div>
            {dryItems.length > 0 && (
              <div className="flex items-center gap-2 mb-2" data-topup>
                <span className="text-xs font-bold text-slate-700 flex-1">⏱️ {tr(config, 'เพิ่มเวลาอบ')}</span>
                <button onClick={() => setTopUpAmt(v => Math.max(0, v - 10))} data-topup-minus className="w-9 h-9 rounded-full bg-white border border-slate-300 font-extrabold text-slate-700 active:scale-90">−</button>
                <span className="w-14 text-center font-extrabold tabular-nums">฿{topUpAmt}</span>
                <button onClick={() => setTopUpAmt(v => v + 10)} data-topup-plus className="w-9 h-9 rounded-full bg-sky-600 text-white font-extrabold active:scale-90">+</button>
              </div>
            )}
            <div className="rounded-xl bg-white border-2 border-slate-200 px-3 py-2" data-simple-items>
              {washItems.length || dryItems.length
                ? <p className="text-xs font-bold text-slate-700">{[...washItems.map(i => `${tr(config, 'ซัก')} ${i.size}kg × ${i.qty}`), ...dryItems.map(i => `${tr(config, 'อบ')} ${i.size}kg × ${i.qty}${i.topUp ? ` (+${tr(config, 'เพิ่มเวลา')} ฿${i.topUp})` : ''}`)].join(' · ')} · ฿{formatMoney(total)}</p>
                : <p className="text-xs text-slate-500">{tr(config, 'แตะเครื่องที่ทำด้านบน')}</p>}
            </div>
            <p className="text-[11px] text-slate-700 mt-2">{tr(config, 'แตะเครื่อง แล้วกดบันทึก — แอปติ๊กเริ่มเครื่องให้เอง')}</p>
          </div>
        )}

        {!isInternal && !simpleAcct && !isEdit && (!config.ui2 || pendingWeb.length > 0 || !!webPicked) && (""", 'simple acct box')
rep("""        {!isInternal && <Section iconName="user" title={tr(config, "ข้อมูลลูกค้า")}>""",
    """        {!isInternal && !simpleAcct && <Section iconName="user" title={tr(config, "ข้อมูลลูกค้า")}>""", 'hide customer')
rep("""        {!isInternal && <Section iconName="camera" title={tr(config, "รูปตะกร้าผ้า")}>""",
    """        {!isInternal && !simpleAcct && <Section iconName="camera" title={tr(config, "รูปตะกร้าผ้า")}>""", 'hide photo')
rep("""        {!isInternal && <Section iconName="sparkles" title={tr(config, "รายการเสริม / ขายแยก")}>""",
    """        {!isInternal && !simpleAcct && <Section iconName="sparkles" title={tr(config, "รายการเสริม / ขายแยก")}>""", 'hide extras')
rep("""        {!isInternal && acct && <Section iconName="dollar-sign" title={tr(config, "การชำระเงิน")}>""",
    """        {!isInternal && acct && !simpleAcct && <Section iconName="dollar-sign" title={tr(config, "การชำระเงิน")}>""", 'hide pay')
rep("""      internalMachines: internalType ? internalMachines : null,""",
    """      internalMachines: internalType || simpleAcct ? internalMachines : null, // v188 งานเกอิชา (ฟอร์มสั้น) เก็บเครื่องที่แตะ → ติ๊ก SOL ตรงเครื่อง""", 'save machines')

# ---------- บันทึกแล้วส่ง LINE (งานเกอิชาด้วย) ----------
rep("""      if (fastFree && isInternalOrder(savedOrder)) setAutoShareSlip(true);""",
    """      if (fastFree) setAutoShareSlip(true); // v188 งานเกอิชาด้วย (แชร์ใบรับงาน)""", 'autoShare geisha')
rep("""  }, [autoShareSlip, slipUrl, internal]);""",
    """  }, [autoShareSlip, slipUrl, internal]);
  useEffect(() => { // 🏢 v188 งานไม่คิดเงิน (เกอิชา) โดยแอดมิน/เจ้าของ: เด้งแชร์ใบรับงานเข้า LINE · ไม่เด้ง = ปุ่มส่งเข้า Line ยังอยู่
    if (!autoShareSlip || internal || slipSharedRef.current) return;
    slipSharedRef.current = true;
    const t = setTimeout(() => { if (onSlipShared) onSlipShared(); handleShare(); }, 700); // ปิดธงใน timeout (ปิดก่อน = effect cleanup ยกเลิก timer)
    return () => clearTimeout(t);
  }, [autoShareSlip, internal]);""", 'receipt auto share')

# ---------- MM ----------
add = []
if "  'เพิ่มเวลาอบ':" not in s: add.append("  'เพิ่มเวลาอบ': 'အခြောက်ခံချိန် တိုးရန်',")
if "  'เพิ่มเวลา':" not in s: add.append("  'เพิ่มเวลา': 'အချိန်တိုး',")
if add:
    rep("""  'หน้าเจ้าของ': 'ပိုင်ရှင်စာမျက်နှာ', // v187""", """  'หน้าเจ้าของ': 'ပိုင်ရှင်စာမျက်နှာ', // v187
""" + '\n'.join(add) + " // v188", 'MM')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v188 applied')
