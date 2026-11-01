#!/usr/bin/env python3
"""v187 — ปุ่มขวาบนหน้าแรก: แม่บ้าน/แอดมินไม่เห็น · เจ้าของกดเข้าหน้าเจ้าของได้เลย (ไม่ถามรหัส) · ไอคอนแดชบอร์ดแทนแม่กุญแจ
ที่มา: เจ้าของ 2 พ.ย. 69 'ถ้าเป็นแม่บ้าน หรือ แอดมิน จะไม่มีรูป แม่กุญแจอยู่ขวาบน แต่ถ้าเป็นเจ้าของเข้าไม่ต้องใส่ พาสเวตแล้ว
  แล้วก็เปลี่ยนเป็นรูปอื่นแทนกุญแจด้วยให้สอดคลองกับงาน'
(เจ้าของล็อกอินด้วยรหัสที่หน้าล็อกอินแล้ว · ใช้มือถือแม่บ้าน → ชิปชื่อ → สลับเป็นเจ้าของ (ใส่รหัส) เหมือนเดิม)
usage: python3 tools/v187_owner_button.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v186-2026-11-02';", "window.APP_VERSION = 'v187-2026-11-02';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v186';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v186';", "const CACHE_NAME = 'plp-laundry-v187';")
rep("""              <button onClick={onOwnerLogin} className="bg-white bg-opacity-20 backdrop-blur-sm rounded-full p-2.5 border border-white border-opacity-30 active:scale-95 transition">
                <Icon name="lock" className="w-5 h-5 text-white" />
              </button>""",
    """              {(ownerNow || !currentStaff) && <button onClick={onOwnerLogin} data-owner-dash={ownerNow ? '1' : undefined} title={tr(config, 'หน้าเจ้าของ')} className="bg-white bg-opacity-20 backdrop-blur-sm rounded-full p-2.5 border border-white border-opacity-30 active:scale-95 transition">
                <Icon name={ownerNow ? 'layout-dashboard' : 'lock'} className="w-5 h-5 text-white" />
              </button>}{/* v187 แม่บ้าน/แอดมินไม่เห็น · เจ้าของ = 📊 เข้าได้เลย · ร้านที่ยังไม่มีบัญชี (Teddy 1 ชั่วคราว) = 🔒 ใส่รหัสเหมือนเดิม */}""", 'owner button')
rep("""onOwnerLogin={() => setView('ownerLogin')}""",
    """onOwnerLogin={() => { if (isOwner || (currentStaff && currentStaff.isOwnerLogin)) { setIsOwner(true); setView('ownerDashboard'); } else setView('ownerLogin'); }}""", 'owner direct')
if "  'หน้าเจ้าของ':" not in s:
    rep("""  // v186 ปุ่มติดตั้งแอป""", """  'หน้าเจ้าของ': 'ပိုင်ရှင်စာမျက်နှာ', // v187
  // v186 ปุ่มติดตั้งแอป""", 'MM')
open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v187 applied')
