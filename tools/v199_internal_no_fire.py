#!/usr/bin/env python3
"""v199 — งานภายใน (ซ่อม/ทดสอบ/ล้างเครื่อง) ทำได้ตอนยิงแอปไม่ได้
ที่มา: เจ้าของ 6 พ.ย. 69 'วันนี้ มีทดสอบลองเครื่อง ต้องทำให้รองรับได้ด้วยเพราะตอนนี้ยัง กดยิงไม่ได้' (EC ระงับถึงอาทิตย์ 8 พ.ย.)
ทำอะไร (หน้าเริ่มเครื่อง ของใบงานภายใน)
  - ✍️ 'บันทึกว่าเริ่มแล้ว (ไม่ยิงจริง)': เดิมเฉพาะเจ้าของ → งานภายในให้ 'แอดมิน' กดได้ด้วย (ไม่มีเงินเกี่ยว)
    ยืนยันข้อความงานภายใน (ไม่ถามเงินสด/โอน) · pulseLog manual ใส่ชื่อคนกดจริง · กระทบยอดนับว่าเริ่มครบ ไม่จับคู่ EC
  - 🪙 'ยิงไม่ได้ → หยอดเหรียญแทน' ของงานภายใน: บันทึกเป็นเหรียญร้าน paymentMethod 'internal' (เดิมลงเป็น 'โอน' ผิด)
    ข้อความยืนยัน 'งานภายใน — ใช้เหรียญร้าน ไม่มีเงินเข้า' · ประวัติแลกเหรียญแสดง '🔧 ร้านใช้เอง' · ไม่นับเป็นเงินสดที่ต้องส่ง
usage: python3 tools/v199_internal_no_fire.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v198-2026-11-05';", "window.APP_VERSION = 'v199-2026-11-06';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v198';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v198';", "const CACHE_NAME = 'plp-laundry-v199';")

# ---------- MM ----------
rep("""  'เหรียญร้าน': 'ဆိုင်အကြွေစေ့', // v192
""", """  'เหรียญร้าน': 'ဆိုင်အကြွေစေ့', // v192
  'บันทึกว่าเริ่มแล้ว (ไม่ยิงจริง)': 'စတင်ပြီးဟု မှတ်တမ်းတင် (တကယ် မပို့)', // v199
  'แอปไม่สั่งเครื่อง — ช่างเปิดเครื่องเอง': 'အက်ပ်က စက်ကို မစေခိုင်း — ပြင်ဆင်သူက စက်ကို ကိုယ်တိုင်ဖွင့်', // v199
  'เครื่องเริ่มทำงานแล้ว กดตกลง': 'စက်စတင်ပြီးမှ OK နှိပ်ပါ', // v199
  'บันทึกแล้ว (ไม่ยิงจริง)': 'မှတ်တမ်းတင်ပြီး (တကယ် မပို့)', // v199
  'งานภายใน — ใช้เหรียญร้าน ไม่มีเงินเข้า': 'ဆိုင်တွင်းအလုပ် — ဆိုင်အကြွေစေ့သုံး ငွေမဝင်', // v199
  '🔧 ร้านใช้เอง': '🔧 ဆိုင်သုံး', // v199
""", 'MM')

# ---------- recordManualStart: คนกด + หมายเหตุ ----------
rep("function recordManualStart(config, order, { machine, kind, kg, temp, heat, baht, warn }) {",
    "function recordManualStart(config, order, { machine, kind, kg, temp, heat, baht, warn, byStaff, note }) { // v199 byStaff/note (แอดมินงานภายใน)", 'manual sig')
rep("""    refType: isInternalOrder(order) ? 'internal' : 'order', refId: order.id, slotKey: null, refLabel: pulseRefLabel(order, config),
    staffId: 'owner', staffName: 'เจ้าของ', createdAt: now,""",
    """    refType: isInternalOrder(order) ? 'internal' : 'order', refId: order.id, slotKey: null, refLabel: pulseRefLabel(order, config),
    staffId: byStaff && byStaff.id ? byStaff.id : 'owner', staffName: byStaff && byStaff.name ? byStaff.name : 'เจ้าของ', createdAt: now,""", 'manual staff')
rep("    manualNote: 'เจ้าของบันทึก (แบบโอน · ไม่ยิงเครื่อง)',",
    "    manualNote: note || 'เจ้าของบันทึก (แบบโอน · ไม่ยิงเครื่อง)',", 'manual note')

# ---------- floatCoinInsert: งานภายใน = เหรียญร้าน ----------
rep("    brand: config.brand, kind: 'floatCoin', amount: baht, paymentMethod: 'transfer',",
    "    brand: config.brand, kind: 'floatCoin', amount: baht, paymentMethod: isInternalOrder(order) ? 'internal' : 'transfer', // 🔧 v199 งานภายใน = เหรียญร้าน ไม่มีเงินเข้า",
    'float pm')
rep("    staffName: log.staffName, photo: '', note: 'หยอดแทนยิงแอป (ยิงไม่ได้)', createdAt: now,",
    "    staffName: log.staffName, photo: '', note: isInternalOrder(order) ? 'เหรียญร้านใช้งานภายใน (ยิงไม่ได้)' : 'หยอดแทนยิงแอป (ยิงไม่ได้)', createdAt: now,",
    'float note')

# ---------- ปุ่ม ✍️ ----------
rep("""          {owner && ready && !busyText && (
            <button onClick={() => {
              const o = job.order;
              const cashNote""",
    """          {(owner || (adminOk && job && isInternalOrder(job.order))) && ready && !busyText && (
            <button data-manual-start onClick={() => {
              const o = job.order;
              if (isInternalOrder(o)) { // 🔧 v199 งานภายใน — เจ้าของ/แอดมิน บันทึกว่าเริ่มเองได้ (ไม่มีเงินเกี่ยว)
                const me = currentStaffLS(config);
                if (!confirm(`✍️ ${tr(config, 'บันทึกว่าเริ่มแล้ว (ไม่ยิงจริง)')}\\n\\n📋 ${pulseRefLabel(o, config)}\\n🧺 ${selM.label} (${selM.kg}kg) · ฿${baht}\\n\\n⚠️ ${tr(config, 'แอปไม่สั่งเครื่อง — ช่างเปิดเครื่องเอง')}\\n👉 ${tr(config, 'เครื่องเริ่มทำงานแล้ว กดตกลง')}`)) return;
                recordManualStart(config, o, { machine: selM.id, kind: selM.kind, kg: selM.kg, temp: selM.kind === 'wash' ? tempUse : null, heat: selM.kind === 'dry' ? heat : null, warn, baht,
                  byStaff: owner ? null : me, note: 'บันทึกเริ่มเครื่องเอง (งานภายใน · ไม่ยิงเครื่อง)' });
                setOwnerMsg(`✍️ ${selM.label} ฿${baht} — ${tr(config, 'บันทึกแล้ว (ไม่ยิงจริง)')}`);
                setSel(null);
                return;
              }
              const cashNote""", 'manual btn head')
rep("""              ✍️ {tr(config, 'เจ้าของ: บันทึกว่าเริ่มแล้ว (ไม่ยิงจริง)')} {selM.label} ฿{baht}""",
    """              ✍️ {tr(config, job && isInternalOrder(job.order) ? 'บันทึกว่าเริ่มแล้ว (ไม่ยิงจริง)' : 'เจ้าของ: บันทึกว่าเริ่มแล้ว (ไม่ยิงจริง)')} {selM.label} ฿{baht}""", 'manual btn label')

# ---------- ปุ่ม 🪙 ยืนยันของงานภายใน ----------
rep("""\\n\\n• ${tr(config, 'ใบงานยังเป็นโอน — เงินอยู่ในบัญชีร้านแล้ว ไม่ต้องส่งเงิน')}\\n• ${tr(config, 'แอปหักเหรียญตั้งต้นให้')}""",
    """\\n\\n• ${tr(config, isInternalOrder(o) ? 'งานภายใน — ใช้เหรียญร้าน ไม่มีเงินเข้า' : 'ใบงานยังเป็นโอน — เงินอยู่ในบัญชีร้านแล้ว ไม่ต้องส่งเงิน')}\\n• ${tr(config, 'แอปหักเหรียญตั้งต้นให้')}""", 'float confirm')

# ---------- ป้ายวิธีจ่ายในประวัติแลกเหรียญ ----------
rep("""{tr(config, pm === 'transfer' ? '💳 โอน' : '💵 สด')}""",
    """{tr(config, pm === 'transfer' ? '💳 โอน' : pm === 'internal' ? '🔧 ร้านใช้เอง' : '💵 สด')}""", 'ex label', count=2)
rep("    const payLabel = t.paymentMethod === 'transfer' ? '💳 โอน' : '💵 เงินสด';",
    "    const payLabel = t.paymentMethod === 'transfer' ? '💳 โอน' : t.paymentMethod === 'internal' ? '🔧 ร้านใช้เอง' : '💵 เงินสด';", 'share label')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v199 applied')
