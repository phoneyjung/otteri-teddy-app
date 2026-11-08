#!/usr/bin/env python3
"""v205 — โหมดตัดเครดิต (Teddy 2): ขั้นตอนที่จอกล่องแบบละเอียด + เปลี่ยนคำ 'ยิง/พัลส์' ที่เหลือ
ที่มา: เจ้าของ 8 พ.ย. 69 (ส่งรูปขั้นตอนจริงที่อบ 3) 'กดเลือก 60 อบร้อน 17kg · กด use credit · สแกน · ตัดเครดิต ·
        แล้วไปกดในแอป plp' + ตอบ: อบเกินราคาเริ่ม = 'แตะ 60 จ่ายเครดิต แล้วแตะ 20 จ่ายอีกรอบ' ·
        สด+โอน = 'หยอดเหรียญ 40 แล้วตัดเครดิตส่วนที่เหลือ 20 ได้' · 'อย่าเพิ่งทำคลิป ให้แอปนิ่งก่อน'
ทำอะไร
  - creditPlan(): แบ่งยอดเป็นรอบที่ต้องแตะที่จอกล่อง — ซัก = ราคาเดียว · อบ = ราคาเริ่ม (ถ้ายอด ≥ ราคาเริ่ม) แล้วเพิ่มเวลา 20/10
    เหรียญเงินสดหักจากรอบแรกก่อน (หยอดเหรียญก่อน แล้วตัดเครดิตส่วนที่เหลือ)
  - creditStepLines(): 'แตะ ฿60 ที่จอกล่อง → Use Credit → สแกน → ล็อกอินเบอร์+รหัสของตัวเอง (รอบแรก) → ใส่ 60 → Use credit'
  - หน้าเลือกเครื่อง: กล่องเหลือง 📝 ขั้นตอนที่ตู้ เป็นข้อ ๆ `[data-credit-steps]` · กล่องยืนยัน + โปรซักเอง ใช้ข้อเดียวกัน
  - ct(): คำในหน้าแม่บ้านโหมดตัดเครดิต — โอน ยิงแอป → โอน ตัดเครดิต · ยิงซ้ำไม่ได้ → เริ่มซ้ำไม่ได้ · ยิงไม่ได้ → เริ่มไม่ได้ ·
    เหตุผลแจ้งปัญหา ยิงแล้วเครื่องไม่ทำงาน → จ่ายแล้วเครื่องไม่ทำงาน ฯลฯ · ไอคอน ⚡ → 🎟️
  - โปรซักเอง: บันทึกแล้วขึ้น '🎟️ ตัดเครดิตแล้ว' (เดิมขึ้น 'ส่งคำสั่งแล้ว ดูที่เครื่อง…')
usage: python3 tools/v205_credit_steps.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v204-2026-11-08';", "window.APP_VERSION = 'v205-2026-11-08';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v204';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v204';", "const CACHE_NAME = 'plp-laundry-v205';")

# ---------- MM ----------
rep("""  'ตัดเครดิตของตัวเองที่ตู้': 'စက်တွင် ကိုယ်ပိုင်ခရက်ဒစ်ဖြင့် ပေး', // v204
""", """  'ตัดเครดิตของตัวเองที่ตู้': 'စက်တွင် ကိုယ်ပိုင်ခရက်ဒစ်ဖြင့် ပေး', // v204
  'ที่จอกล่อง': 'ဘေးဘူးမျက်နှာပြင်တွင်', // v205
  'สแกน': 'စကင်ဖတ်', // v205
  'ล็อกอินเบอร์+รหัสของตัวเอง': 'ကိုယ့်ဖုန်းနံပါတ်+စကားဝှက်ဖြင့် ဝင်ပါ', // v205
  'ใส่': 'ထည့်', // v205
  'ขั้นตอนที่ตู้': 'စက်တွင် လုပ်ရမည့်အဆင့်', // v205
  'ใส่ผ้า ปิดประตู กดโหมดที่หน้าเครื่อง': 'အဝတ်ထည့် တံခါးပိတ် စက်ရှေ့တွင် မုဒ်ရွေး', // v205
  'เครื่องเดินแล้ว กดปุ่ม 🎟️ ตัดเครดิตแล้ว ด้านล่าง': 'စက်လည်ပြီးမှ အောက်က 🎟️ ခရက်ဒစ်ဖြင့် ပေးပြီး ခလုတ်နှိပ်', // v205
  'เครื่องเดินแล้ว กดตกลง': 'စက်လည်ပြီးမှ OK နှိပ်', // v205
  'โอน ตัดเครดิต': 'လွှဲ — ခရက်ဒစ်ဖြင့် ပေး', // v205
  'โอน → ตัดเครดิต': 'လွှဲ → ခရက်ဒစ်ဖြင့် ပေး', // v205
  'ส่วนลด ตัดเครดิต': 'လျှော့ငွေ — ခရက်ဒစ်ဖြင့် ပေး', // v205
  'ส่วนลด → ตัดเครดิต (ซัก)': 'လျှော့ငွေ → ခရက်ဒစ် (လျှော်)', // v205
  'ส่วนโอน ตัดเครดิต': 'လွှဲသည့်အပိုင်း — ခရက်ဒစ်ဖြင့် ပေး', // v205
  'ส่วนลดคูปอง — ตัดเครดิตได้ (เฉพาะเครื่องซัก)': 'ကူပွန်လျှော့ငွေ — ခရက်ဒစ်ဖြင့် ပေးနိုင် (လျှော်စက်သာ)', // v205
  'เริ่มไม่ได้': 'မစနိုင်', // v205
  'งานนี้เริ่มเครื่องครบแล้ว — เริ่มซ้ำไม่ได้': 'ဤအလုပ် စက်စပြီးပြီ — ထပ်မစနိုင်', // v205
  'ใบงานนี้เริ่มซักครบแล้ว — เริ่มซ้ำไม่ได้': 'ဤစာရွက် လျှော်ပြီးပြီ — ထပ်မစနိုင်', // v205
  'อบครบตามใบงานแล้ว — เกินใบงานไม่ได้': 'စာရွက်အတိုင်း အခြောက်ခံပြီး — ပိုမလုပ်နိုင်', // v205
  'ยอดต้องลงท้ายด้วย 0': 'ပမာဏ 0 ဖြင့် ဆုံးရမည်', // v205
  'จ่ายแล้วเครื่องไม่ทำงาน': 'ပေးပြီး စက်မလည်', // v205
  'เริ่มผิดเครื่อง': 'စက်မှားစ', // v205
  'ตัดเครดิตไปแล้ว แต่ไม่นับกับใบงาน (ร้านรับภาระ)': 'ခရက်ဒစ်ပေးပြီး သို့သော် စာရွက်တွင် မရေတွက် (ဆိုင်က တာဝန်ယူ)', // v205
  'วันนี้ยังไม่ได้เปิดระบบบันทึกเริ่มเครื่อง': 'ဤနေ့ စက်စတင်မှတ်တမ်းစနစ် မဖွင့်ရသေး', // v205
""", 'MM')

# ---------- helpers ----------
rep("""const isCredit = (config) => !!(config && config.pulse && config.pulse.mode === 'credit'); // 🎟️ v204 Teddy 2: ตัดเครดิตที่ตู้ (ไม่ติดต่อ EC)""",
    """const isCredit = (config) => !!(config && config.pulse && config.pulse.mode === 'credit'); // 🎟️ v204 Teddy 2: ตัดเครดิตที่ตู้ (ไม่ติดต่อ EC)
// 🎟️ v205 คำในหน้าแม่บ้านโหมดตัดเครดิต (แทนคำว่า ยิง/พัลส์) · ใช้ ct(config, คำเดิม) แทน tr(config, คำเดิม)
const CREDIT_WORDS = {
  'โอน ยิงแอป': 'โอน ตัดเครดิต', 'โอน → ยิงแอป': 'โอน → ตัดเครดิต',
  'ส่วนลด ยิงจากแอป': 'ส่วนลด ตัดเครดิต', 'ส่วนลด → ยิงแอป (ซัก)': 'ส่วนลด → ตัดเครดิต (ซัก)',
  'ส่วนโอน ยิงจากแอป': 'ส่วนโอน ตัดเครดิต', 'ส่วนลดคูปอง — ยิงจากแอปได้ (เฉพาะเครื่องซัก)': 'ส่วนลดคูปอง — ตัดเครดิตได้ (เฉพาะเครื่องซัก)',
  'ยิงไม่ได้': 'เริ่มไม่ได้',
  'งานนี้เริ่มเครื่องครบแล้ว — ยิงซ้ำไม่ได้': 'งานนี้เริ่มเครื่องครบแล้ว — เริ่มซ้ำไม่ได้',
  'ใบงานนี้เริ่มซักครบแล้ว — ยิงซ้ำไม่ได้': 'ใบงานนี้เริ่มซักครบแล้ว — เริ่มซ้ำไม่ได้',
  'อบครบตามใบงานแล้ว — ยิงเกินใบงานไม่ได้': 'อบครบตามใบงานแล้ว — เกินใบงานไม่ได้',
  'ยอดต้องลงท้ายด้วย 0 (1 พัลส์ = 10 บาท)': 'ยอดต้องลงท้ายด้วย 0',
  'ยิงแล้วเครื่องไม่ทำงาน': 'จ่ายแล้วเครื่องไม่ทำงาน', 'ยิงผิดเครื่อง': 'เริ่มผิดเครื่อง',
  'เครื่องได้รับพัลส์แล้ว แต่ไม่นับกับใบงาน (ร้านรับภาระ)': 'ตัดเครดิตไปแล้ว แต่ไม่นับกับใบงาน (ร้านรับภาระ)',
  'วันนี้ยังไม่ได้เปิดระบบยิงพัลส์จากแอป': 'วันนี้ยังไม่ได้เปิดระบบบันทึกเริ่มเครื่อง',
};
const ct = (config, s) => tr(config, isCredit(config) && CREDIT_WORDS[s] ? CREDIT_WORDS[s] : s);
const fireIcon = (config) => (isCredit(config) ? '🎟️' : '⚡');
// 🎟️ v205 รอบที่ต้องแตะที่จอกล่องข้างเครื่อง (เจ้าของยืนยัน 8 พ.ย.): ซัก = ราคาเดียว · อบ = ราคาเริ่ม แล้วเพิ่มเวลา 20/10 ทีละรอบ
// เงินสด (coin) หยอดเหรียญก่อน แล้วตัดเครดิตส่วนที่เหลือ — pay = ยอดที่ใส่ในหน้าเครดิต
function creditPlan(config, { kind, kg, baht, coin }) {
  const taps = [];
  let left = baht || 0;
  if (kind === 'dry') {
    const base = config.dryMachines ? ((config.dryMachines.find(d => d.size === kg) || {}).price || 0) : 0;
    if (base > 0 && left >= base) { taps.push(base); left -= base; }
    while (left >= 20) { taps.push(20); left -= 20; }
    if (left >= 10) { taps.push(10); left -= 10; }
    if (left > 0) taps.push(left);
  } else if (left > 0) taps.push(left);
  let c = Math.max(0, coin || 0);
  return taps.map(t => { const use = Math.min(c, t); c -= use; return { tap: t, coin: use, pay: t - use }; });
}
function creditStepLines(config, rounds) {
  let loginShown = false;
  return rounds.map(r => {
    if (r.pay <= 0) return `💵 ${tr(config, 'หยอดเหรียญ')} ฿${r.coin}`;
    const login = loginShown ? '' : ` → ${tr(config, 'ล็อกอินเบอร์+รหัสของตัวเอง')}`;
    loginShown = true;
    return `${r.coin > 0 ? `💵 ${tr(config, 'หยอดเหรียญ')} ฿${r.coin} → ` : ''}${tr(config, 'แตะ')} ฿${r.tap} ${tr(config, 'ที่จอกล่อง')} → Use Credit → ${tr(config, 'สแกน')}${login} → ${tr(config, 'ใส่')} ${r.pay} → Use credit`;
  });
}""", 'helpers')

# ---------- หน้าเลือกเครื่อง: ขั้นตอนที่ตู้ ----------
rep("""                <p className="text-[11px] font-bold text-slate-500 mt-0.5">📝 {tr(config, isSol(config) ? 'ขั้นตอน: ใส่ผ้า → ปิดประตู → กดปุ่มด้านล่าง → กด Start ใน SOL → กลับมากด ✅' : isCredit(config) ? 'ขั้นตอน: ใส่ผ้า → ปิดประตู → เลือกโปรแกรม → จ่ายด้วยเครดิตของตัวเองที่ตู้ → เครื่องเดินแล้วกดปุ่มด้านล่าง' : 'ขั้นตอน: ใส่ผ้า → ปิดประตู → เลือกโปรแกรมที่หน้าเครื่อง → กดเริ่ม (ชำระเงิน)')}</p>""",
    """                {isCredit(config) ? ( // 🎟️ v205 ขั้นตอนที่ตู้เป็นข้อ ๆ
                  <div className="mt-1.5 rounded-lg bg-white/70 px-2 py-1.5" data-credit-steps>
                    <p className="text-xs font-extrabold text-slate-700">📝 {tr(config, 'ขั้นตอนที่ตู้')}</p>
                    <p className="text-[13px] font-bold text-slate-800 mt-0.5">1) {tr(config, 'ใส่ผ้า ปิดประตู กดโหมดที่หน้าเครื่อง')}</p>
                    {creditStepLines(config, creditPlan(config, { kind: selM.kind, kg: selM.kg, baht, coin: cp.coin })).map((t, i) => (
                      <p key={i} className="text-[13px] font-bold text-slate-800 mt-0.5">{i + 2}) {t}</p>
                    ))}
                    <p className="text-[13px] font-extrabold text-emerald-800 mt-0.5">✅ {tr(config, 'เครื่องเดินแล้ว กดปุ่ม 🎟️ ตัดเครดิตแล้ว ด้านล่าง')}</p>
                  </div>
                ) : <p className="text-[11px] font-bold text-slate-500 mt-0.5">📝 {tr(config, isSol(config) ? 'ขั้นตอน: ใส่ผ้า → ปิดประตู → กดปุ่มด้านล่าง → กด Start ใน SOL → กลับมากด ✅' : 'ขั้นตอน: ใส่ผ้า → ปิดประตู → เลือกโปรแกรมที่หน้าเครื่อง → กดเริ่ม (ชำระเงิน)')}</p>}""", 'sheet steps')

# ---------- กล่องยืนยัน ----------
rep("""    : `✅ ${tr(config, 'ก่อนกดตกลง')}:\\n1) ${tr(config, 'ใส่ผ้า แล้วปิดประตู')}\\n2) ${tr(config, 'เลือกโปรแกรมที่หน้าเครื่อง')}: ${progLabel}\\n3) ${cr && pulseBaht > 0 ? tr(config, coin > 0 ? 'หยอดเหรียญ + จ่ายด้วยเครดิตของตัวเองที่ตู้ จนเครื่องเริ่มทำงาน แล้วกดตกลง' : 'จ่ายด้วยเครดิตของตัวเองที่ตู้ จนเครื่องเริ่มทำงาน แล้วกดตกลง') : coin > 0 ? tr(config, 'หยอดเหรียญ แล้วกดตกลง') : tr(config, 'กดตกลง = ชำระเงิน เครื่องเริ่มทำงาน')}`;""",
    """    : cr && pulseBaht > 0 // 🎟️ v205 ขั้นตอนที่ตู้เป็นรอบ ๆ
    ? `✅ ${tr(config, 'ก่อนกดตกลง')}:\\n1) ${tr(config, 'ใส่ผ้า แล้วปิดประตู')}\\n2) ${tr(config, 'เลือกโปรแกรมที่หน้าเครื่อง')}: ${progLabel}\\n${creditStepLines(config, creditPlan(config, { kind, kg, baht, coin })).map((t, i) => `${i + 3}) ${t}`).join('\\n')}\\n✅ ${tr(config, 'เครื่องเดินแล้ว กดตกลง')}`
    : `✅ ${tr(config, 'ก่อนกดตกลง')}:\\n1) ${tr(config, 'ใส่ผ้า แล้วปิดประตู')}\\n2) ${tr(config, 'เลือกโปรแกรมที่หน้าเครื่อง')}: ${progLabel}\\n3) ${coin > 0 ? tr(config, 'หยอดเหรียญ แล้วกดตกลง') : tr(config, 'กดตกลง = ชำระเงิน เครื่องเริ่มทำงาน')}`;""", 'confirm steps')

# ---------- โปรซักเอง ----------
rep("""      ? `🎟️ ${tr(config, 'ยืนยันตัดเครดิต')}\\n\\n🧺 ${pulseMachine.label}\\n🎟️ ${tr(config, 'ตัดเครดิตของตัวเองที่ตู้')} ฿${amount}\\n🎁 ${promoName || 'ส่วนลด'}\\n\\n👉 ${tr(config, 'จ่ายด้วยเครดิตของตัวเองที่ตู้ จนเครื่องเริ่มทำงาน แล้วกดตกลง')}`""",
    """      ? `🎟️ ${tr(config, 'ยืนยันตัดเครดิต')}\\n\\n🧺 ${pulseMachine.label}\\n🎟️ ${tr(config, 'ตัดเครดิตของตัวเองที่ตู้')} ฿${amount}\\n🎁 ${promoName || 'ส่วนลด'}\\n\\n${creditStepLines(config, creditPlan(config, { kind: pulseMachine.kind, kg: pulseMachine.kg, baht: amount, coin: 0 })).map((t, i) => `${i + 1}) ${t}`).join('\\n')}\\n✅ ${tr(config, 'เครื่องเดินแล้ว กดตกลง')}`""", 'promo confirm')
rep("""      if (amount % PULSE_BAHT !== 0) { alert(tr(config, 'ยอดต้องลงท้ายด้วย 0 (1 พัลส์ = 10 บาท)')); return; }""",
    """      if (amount % PULSE_BAHT !== 0) { alert(ct(config, 'ยอดต้องลงท้ายด้วย 0 (1 พัลส์ = 10 บาท)')); return; }""", 'promo alert')
rep("""              <p className={`text-sm font-bold mt-1 ${savedPromo.pulseStatus === 'confirmed' ? 'text-emerald-600' : 'text-amber-600'}`}>
                {savedPromo.pulseStatus === 'confirmed' ? '✅ ' + tr(config, 'เครื่องรับแล้ว') : '⏳ ' + tr(config, 'ส่งคำสั่งแล้ว ดูที่เครื่องว่าเริ่มทำงานไหม')}""",
    """              <p className={`text-sm font-bold mt-1 ${savedPromo.pulseStatus === 'confirmed' || savedPromo.pulseStatus === 'credit' ? 'text-emerald-600' : 'text-amber-600'}`}>
                {savedPromo.pulseStatus === 'credit' ? '🎟️ ' + tr(config, 'ตัดเครดิตแล้ว') : savedPromo.pulseStatus === 'confirmed' ? '✅ ' + tr(config, 'เครื่องรับแล้ว') : '⏳ ' + tr(config, 'ส่งคำสั่งแล้ว ดูที่เครื่องว่าเริ่มทำงานไหม')}""", 'promo saved')

# ---------- คำ ยิง/พัลส์ ที่เหลือ ----------
rep("""  if (pay.transferLeft > 0) parts.push(<span key="t" className="text-sky-700">⚡ {tr(config, 'โอน ยิงแอป')} ฿{pay.transferLeft}</span>);""",
    """  if (pay.transferLeft > 0) parts.push(<span key="t" className="text-sky-700">{fireIcon(config)} {ct(config, 'โอน ยิงแอป')} ฿{pay.transferLeft}</span>);""", 'pay left')
rep("""block = tr(config, 'งานนี้เริ่มเครื่องครบแล้ว — ยิงซ้ำไม่ได้');""", """block = ct(config, 'งานนี้เริ่มเครื่องครบแล้ว — ยิงซ้ำไม่ได้');""", 'block1')
rep("""block = tr(config, 'ใบงานนี้เริ่มซักครบแล้ว — ยิงซ้ำไม่ได้');""", """block = ct(config, 'ใบงานนี้เริ่มซักครบแล้ว — ยิงซ้ำไม่ได้');""", 'block2')
rep("""tr(config, 'อบครบตามใบงานแล้ว — ยิงเกินใบงานไม่ได้')""", """ct(config, 'อบครบตามใบงานแล้ว — ยิงเกินใบงานไม่ได้')""", 'block3')
rep("""{cp.disc > 0 && <p className="text-sm font-bold text-amber-700">🎟️ {tr(config, 'ส่วนลด ยิงจากแอป')} ฿{cp.disc}</p>}
                {cp.pulse - cp.disc > 0 && <p className="text-sm font-bold text-sky-800">⚡ {tr(config, 'ส่วนโอน ยิงจากแอป')} ฿{cp.pulse - cp.disc}</p>}""",
    """{cp.disc > 0 && <p className="text-sm font-bold text-amber-700">🎟️ {ct(config, 'ส่วนลด ยิงจากแอป')} ฿{cp.disc}</p>}
                {cp.pulse - cp.disc > 0 && <p className="text-sm font-bold text-sky-800">{fireIcon(config)} {ct(config, 'ส่วนโอน ยิงจากแอป')} ฿{cp.pulse - cp.disc}</p>}""", 'split card')
rep("""🎟️ {tr(config, 'ส่วนลดคูปอง — ยิงจากแอปได้ (เฉพาะเครื่องซัก)')}""", """🎟️ {ct(config, 'ส่วนลดคูปอง — ยิงจากแอปได้ (เฉพาะเครื่องซัก)')}""", 'disc card')
rep("""block ? `🚫 ${tr(config, 'ยิงไม่ได้')}`""", """block ? `🚫 ${ct(config, 'ยิงไม่ได้')}`""", 'main blocked')
rep("""<span key="d" className="text-amber-700">🎟️ {tr(config, 'ส่วนลด → ยิงแอป (ซัก)')}""", """<span key="d" className="text-amber-700">🎟️ {ct(config, 'ส่วนลด → ยิงแอป (ซัก)')}""", 'ticket disc')
rep("""<span key="t" className="text-sky-700">⚡ {tr(config, 'โอน → ยิงแอป')}""", """<span key="t" className="text-sky-700">{fireIcon(config)} {ct(config, 'โอน → ยิงแอป')}""", 'ticket transfer')
rep("""({pulseIsCoin(log) ? '💵 ' + tr(config, 'หยอดเหรียญ') : log.pulses + ' ' + tr(config, 'พัลส์')})""",
    """({pulseIsCoin(log) ? '💵 ' + tr(config, 'หยอดเหรียญ') : pulseIsCredit(log) ? '🎟️ ' + tr(config, 'ตัดเครดิต') : log.pulses + ' ' + tr(config, 'พัลส์')})""", 'refund sheet item')
rep("""                  {r.emoji} {tr(config, r.label)}""", """                  {r.emoji} {ct(config, r.label)}""", 'refund reasons')
rep("""tr(config, refundReasonLabel(""", """ct(config, refundReasonLabel(""", 'refund labels', count=3)
rep("""{tr(config, 'เครื่องได้รับพัลส์แล้ว แต่ไม่นับกับใบงาน (ร้านรับภาระ)')}""", """{ct(config, 'เครื่องได้รับพัลส์แล้ว แต่ไม่นับกับใบงาน (ร้านรับภาระ)')}""", 'refund note')
rep("""{tr(config, 'วันนี้ยังไม่ได้เปิดระบบยิงพัลส์จากแอป')}""", """{ct(config, 'วันนี้ยังไม่ได้เปิดระบบยิงพัลส์จากแอป')}""", 'inactive day')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v205 patched')
