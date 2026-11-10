#!/usr/bin/env python3
"""v210 — ฟอร์ม 'บันทึกลูกค้าใช้โปร': แยกสีซัก/อบ + แยกขนาดเครื่อง + โปร LINE ไม่มีเครื่องอบ + บอกลำดับการกด
ที่มา: เจ้าของ 10 พ.ย. 69 12:45 (ส่งภาพหน้าจอฟอร์มโปร Teddy 2)
  'อยากให้แยกสี ซัก กับ อบ แล้วมีความแตกต่างเรื่องขนาดเครื่องด้วย กันแม่บ้านกดเลือกผิด'
  'โปร แอดไลน์ ลดแค่การซัก ดังนั้น เมื่อเลือกแล้ว ไม่มีตัวเลือก อบ'
  'บอกลำดับการกด เพื่อความรวดเร็วการทำความเข้าใจ'
ทำอะไร
  - ชิปเลือกเครื่อง: จัดกลุ่ม 💧 เครื่องซัก (ฟ้า) / 🔥 เครื่องอบ (ส้ม) · แต่ละกลุ่มแยกแถวตามขนาด (ป้าย 17 กก. / 12 กก.)
    เครื่องขนาดใหญ่สุดของกลุ่ม = ชิปใหญ่กว่า · ที่เลือกแล้วมี ✓ และบรรทัด 'เลือกแล้ว: ซัก 6 · 12 กก.' `[data-promo-picked]`
  - เลือก 💬 LINE ลด: ซ่อนเครื่องอบทั้งกลุ่ม + บรรทัด 'โปรแอดไลน์ ลดเฉพาะค่าซัก' · ถ้าเลือกเครื่องอบไว้ก่อน → ล้างให้
  - โหมดตัดเครดิต (Teddy 2): แถบลำดับ 1 เลือกโปร → 2 เลือกเครื่อง → 3 ถ่ายรูป → 4 ทำที่ตู้ → 5 กดบันทึก `[data-promo-order]`
    แทนบรรทัดเดิม 'เลือกเครื่อง → ถ่ายรูป → กดเริ่มเครื่อง' + เลขวงกลมหน้าหัวข้อแต่ละส่วนและบนปุ่มบันทึก
  - ร้านอื่น: ชิปจัดกลุ่ม/สีเหมือนกัน (ไม่มีแถบลำดับ) · MM_DICT คำใหม่ (รอตรวจ)
usage: python3 tools/v210_promo_machine_picker.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v209-2026-11-10';", "window.APP_VERSION = 'v210-2026-11-10';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v209';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v209';", "const CACHE_NAME = 'plp-laundry-v210';")

LINE_ONLY = 'โปรแอดไลน์ ลดเฉพาะค่าซัก — เลือกได้แค่เครื่องซัก'
rep("""  'เครื่องเดินแล้ว กดตกลง': 'စက်လည်ပြီးမှ OK နှိပ်', // v205
""", f"""  'เครื่องเดินแล้ว กดตกลง': 'စက်လည်ပြီးမှ OK နှိပ်', // v205
  '{LINE_ONLY}': 'LINE ပရို = လျှော်ခ လျှော့ရုံသာ — အဝတ်လျှော်စက်ကိုသာ ရွေးပါ', // v210
  'เลือกโปร': 'ပရို ရွေး', // v210
  'ทำที่ตู้': 'စက်မှာ လုပ်', // v210
  'กดบันทึก': 'သိမ်း နှိပ်', // v210
  'เลือกแล้ว': 'ရွေးပြီး', // v210
  'กก.': 'ကီလို', // v210
""", 'MM')

# ---------- helpers (next to promoCreditLines) ----------
rep("function promoCreditLines(config, amount) {",
    """// 🎟️ v210 ชิปเครื่องในฟอร์มโปร: แยกซัก/อบ + แยกขนาด (เจ้าของ 10 พ.ย. 69 — กันแม่บ้านกดผิด)
const promoKindOf = (m) => (/^อบ/.test(m.label) || /^d/i.test(m.id) ? 'dry' : 'wash');
const promoKgOf = (m) => parseInt(String(m.size || '').replace(/[^\\d]/g, ''), 10) || 0;
function promoMachineGroups(config, washOnly) {
  const all = ((COIN_POINTS[config.brand] || COIN_POINTS.teddy2).machines || []).filter(m => pulseOn(config) || m.label.startsWith('ซัก'));
  const out = [];
  ['wash', 'dry'].forEach(kind => {
    if (kind === 'dry' && washOnly) return;
    const list = all.filter(m => promoKindOf(m) === kind);
    if (!list.length) return;
    const sizes = [...new Set(list.map(promoKgOf))].sort((a, b) => b - a);
    out.push({ kind, rows: sizes.map(kg => ({ kg, big: kg === sizes[0] && sizes.length > 1, items: list.filter(m => promoKgOf(m) === kg) })) });
  });
  return out;
}
const PROMO_KIND_STYLE = {
  wash: { icon: '💧', title: 'เครื่องซัก', on: '#0284C7', bg: '#F0F9FF', bd: '#7DD3FC', tx: '#075985', tag: '#E0F2FE' },
  dry: { icon: '🔥', title: 'เครื่องอบ', on: '#EA580C', bg: '#FFF7ED', bd: '#FDBA74', tx: '#9A3412', tag: '#FFEDD5' },
};
function PromoStepNo({ n }) { // เลขลำดับการกด (โหมดตัดเครดิต)
  return <span className="inline-flex items-center justify-center w-5 h-5 rounded-full text-white text-[11px] font-extrabold mr-1.5 align-middle" style={{ background: '#E11D48' }}>{n}</span>;
}
function promoCreditLines(config, amount) {""", 'helpers')

# ---------- order strip (replaces the one-line subtitle in credit mode) ----------
rep("""            {T2H && <p className="text-xs font-bold text-slate-500 -mt-1">{tr(config, pulseOn(config) ? 'เลือกเครื่อง → ถ่ายรูป → กดเริ่มเครื่อง' : tokenShop(config) ? 'ให้โทเคนลูกค้า → ถ่ายรูป → ส่งกลุ่ม' : "สแกนเครดิตให้ลูกค้า → ถ่ายรูป → ส่งกลุ่ม")}</p>}
""", """            {T2H && !(pulseOn(config) && isCredit(config)) && <p className="text-xs font-bold text-slate-500 -mt-1">{tr(config, pulseOn(config) ? 'เลือกเครื่อง → ถ่ายรูป → กดเริ่มเครื่อง' : tokenShop(config) ? 'ให้โทเคนลูกค้า → ถ่ายรูป → ส่งกลุ่ม' : "สแกนเครดิตให้ลูกค้า → ถ่ายรูป → ส่งกลุ่ม")}</p>}
            {pulseOn(config) && isCredit(config) && ( // 🔢 v210 ลำดับการกด
              <div className="flex flex-wrap items-center gap-1 -mt-1" data-promo-order>
                {['เลือกโปร', 'เลือกเครื่อง', 'ถ่ายรูป', 'ทำที่ตู้', 'กดบันทึก'].map((t, i) => (
                  <React.Fragment key={t}>
                    {i > 0 && <span className="text-slate-400 text-xs font-bold">→</span>}
                    <span className="inline-flex items-center rounded-full pl-0.5 pr-2 py-0.5 text-[12px] font-extrabold text-rose-900" style={{ background: '#FFE4E6' }}><PromoStepNo n={i + 1} />{tr(config, t)}</span>
                  </React.Fragment>
                ))}
              </div>
            )}
""", 'order strip')

# ---------- section numbers ----------
rep("""              <p className="text-xs font-bold text-slate-600 mb-1.5">{tr(config, "โปรที่ใช้")}</p>""",
    """              <p className="text-xs font-bold text-slate-600 mb-1.5">{pulseOn(config) && isCredit(config) && <PromoStepNo n={1} />}{tr(config, "โปรที่ใช้")}</p>""", 'no1')
rep("""                  <button onClick={() => { setPromoName(`LINE ลด ${config.linePromoDiscount}฿`); setPromoAmount(String(config.linePromoDiscount)); }}""",
    """                  <button onClick={() => { setPromoName(`LINE ลด ${config.linePromoDiscount}฿`); setPromoAmount(String(config.linePromoDiscount)); if (/^อบ/.test(promoMachine)) setPromoMachine(''); /* v210 LINE ลดเฉพาะซัก */ }}""", 'line clears dryer')

# ---------- machine picker ----------
rep("""              <p className="text-xs font-bold text-slate-600 mb-1.5">{tr(config, "เครื่องที่ลูกค้าใช้")}</p>
              <div className="flex flex-wrap gap-1.5">
                {((COIN_POINTS[config.brand] || COIN_POINTS.teddy2).machines || []).filter(m => pulseOn(config) || m.label.startsWith('ซัก')).map(m => (
                  <button key={m.id} onClick={() => setPromoMachine(promoMachine === m.label ? '' : m.label)}
                    className={`px-2.5 py-1 rounded-full text-xs font-bold border ${promoMachine === m.label ? 'bg-sky-500 text-white border-sky-500' : 'bg-white text-slate-600 border-slate-300'}`}>
                    {m.label}
                  </button>
                ))}
              </div>""",
    """              <p className="text-xs font-bold text-slate-600 mb-1.5">{pulseOn(config) && isCredit(config) && <PromoStepNo n={2} />}{tr(config, "เครื่องที่ลูกค้าใช้")}</p>
              {(() => { // 🎟️ v210 แยกสี ซัก (ฟ้า) / อบ (ส้ม) + แถวตามขนาด · โปร LINE = เฉพาะเครื่องซัก
                const lineOnly = promoName.startsWith('LINE');
                const picked = ((COIN_POINTS[config.brand] || COIN_POINTS.teddy2).machines || []).find(m => m.label === promoMachine);
                return (
                  <div className="space-y-2" data-promo-machines>
                    {lineOnly && pulseOn(config) && <p className="text-[12px] font-extrabold rounded-lg px-2 py-1" style={{ background: '#E0F2FE', color: '#075985' }} data-promo-lineonly>💬 {tr(config, 'โปรแอดไลน์ ลดเฉพาะค่าซัก — เลือกได้แค่เครื่องซัก')}</p>}
                    {promoMachineGroups(config, lineOnly).map(g => { const st = PROMO_KIND_STYLE[g.kind]; return (
                      <div key={g.kind} className="rounded-xl p-2 border-2" style={{ borderColor: st.bd, background: st.bg }} data-promo-kind={g.kind}>
                        <p className="text-[13px] font-extrabold mb-1" style={{ color: st.tx }}>{st.icon} {tr(config, st.title)}</p>
                        {g.rows.map(r => (
                          <div key={r.kg} className="flex items-center gap-1.5 mt-1">
                            {r.kg > 0 && <span className="flex-shrink-0 w-14 text-center rounded-md py-0.5 text-[11px] font-extrabold" style={{ background: r.big ? st.on : st.tag, color: r.big ? '#fff' : st.tx }}>{r.kg} {tr(config, 'กก.')}</span>}
                            <div className="flex flex-wrap gap-1.5">
                              {r.items.map(m => { const on = promoMachine === m.label; return (
                                <button key={m.id} onClick={() => setPromoMachine(on ? '' : m.label)} data-promo-m={m.id}
                                  className={`rounded-full font-extrabold border-2 active:scale-95 transition ${r.big ? 'px-3.5 py-1.5 text-sm' : 'px-2.5 py-1 text-xs'}`}
                                  style={on ? { background: st.on, borderColor: st.on, color: '#fff' } : { background: '#fff', borderColor: st.bd, color: st.tx }}>
                                  {on ? '✓ ' : ''}{m.label}
                                </button>
                              ); })}
                            </div>
                          </div>
                        ))}
                      </div>
                    ); })}
                    {picked && <p className="text-[13px] font-extrabold" style={{ color: PROMO_KIND_STYLE[promoKindOf(picked)].tx }} data-promo-picked>✓ {tr(config, 'เลือกแล้ว')}: {picked.label}{promoKgOf(picked) ? ` · ${promoKgOf(picked)} ${tr(config, 'กก.')}` : ''}</p>}
                  </div>
                );
              })()}""", 'picker')

# ---------- photo / steps / button numbers ----------
rep("""              <p className="text-xs font-bold text-slate-600 mb-1">{tr(config, "📷 รูปหลักฐาน (จำเป็น)")}</p>""",
    """              <p className="text-xs font-bold text-slate-600 mb-1">{pulseOn(config) && isCredit(config) && <PromoStepNo n={3} />}{tr(config, "📷 รูปหลักฐาน (จำเป็น)")}</p>""", 'no3')
rep("""                <p className="text-xs font-extrabold text-slate-700">📝 {tr(config, 'ขั้นตอนที่ตู้')}</p>
                {promoCreditLines(""",
    """                <p className="text-xs font-extrabold text-slate-700"><PromoStepNo n={4} />📝 {tr(config, 'ขั้นตอนที่ตู้')}</p>
                {promoCreditLines(""", 'no4')
# main button: number 5 in credit mode (the button text itself is unchanged)
i = s.index("""            <button onClick={handleSubmitPromo} disabled={savingPromo}
              className="w-full py-3.5 rounded-2xl bg-rose-500 text-white font-bold text-base active:scale-95 transition disabled:opacity-50">""")
j = s.index('</button>', i)
seg = s[i:j]
assert seg.count("{savingPromo ?") <= 1, seg
k = seg.index('disabled:opacity-50">') + len('disabled:opacity-50">')
seg2 = seg[:k] + """
              {pulseOn(config) && isCredit(config) && <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-white text-rose-600 text-sm font-extrabold mr-1.5 align-middle">5</span>}""" + seg[k:]
s = s[:i] + seg2 + s[j:]
assert s.count('text-rose-600 text-sm font-extrabold mr-1.5 align-middle">5</span>') == 1

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v210 ok')
