#!/usr/bin/env python3
"""v212: Otteri (SOL) cash+transfer jobs — the start sheet no longer says '⚡ ยิงจากแอป' for the transfer part.
SOL words: '🟦 ส่วนโอน กด Start ใน SOL' · last line: coins for the cash part first → bottom button → Start in SOL for the transfer part.
Usage: python3 tools/v212_sol_split_words.py index.html sw.js"""
import sys
idx, sw = sys.argv[1], sys.argv[2]
s = open(idx, encoding='utf-8').read()

def rep(old, new):
    global s
    assert s.count(old) == 1, ('count', s.count(old), old[:80])
    s = s.replace(old, new)

rep("const ct = (config, s) => tr(config, isCredit(config) && CREDIT_WORDS[s] ? CREDIT_WORDS[s] : s);\n"
    "const fireIcon = (config) => (isCredit(config) ? '🎟️' : '⚡');\n",
    "// 🟦 v212 ร้าน SOL (Otteri): ส่วนโอน = แม่บ้านกด Start ใน SOL เอง (แอปไม่ได้ยิง)\n"
    "const SOL_WORDS = { 'โอน ยิงแอป': 'โอน กด Start ใน SOL', 'โอน → ยิงแอป': 'โอน → Start ใน SOL', 'ส่วนโอน ยิงจากแอป': 'ส่วนโอน กด Start ใน SOL' };\n"
    "const ct = (config, s) => tr(config, isCredit(config) && CREDIT_WORDS[s] ? CREDIT_WORDS[s] : isSol(config) && SOL_WORDS[s] ? SOL_WORDS[s] : s);\n"
    "const fireIcon = (config) => (isCredit(config) ? '🎟️' : isSol(config) ? '🟦' : '⚡');\n")
rep("                <p className=\"text-[11px] font-bold text-amber-800 mt-1\">{tr(config, 'หยอดเหรียญจนเครื่องเริ่มทำงาน แล้วค่อยกดบันทึก')}</p>\n",
    "                <p className=\"text-[11px] font-bold text-amber-800 mt-1\" data-sol-split-step={isSol(config) && cp.pulse - cp.disc > 0 ? '1' : undefined}>{isSol(config) && cp.pulse - cp.disc > 0 ? tr(config, 'หยอดเหรียญส่วนสดก่อน → กดปุ่มด้านล่าง → ไปกด Start ใน SOL ส่วนโอน') : tr(config, 'หยอดเหรียญจนเครื่องเริ่มทำงาน แล้วค่อยกดบันทึก')}</p>\n")
rep("  'ส่วนโอน ยิงจากแอป': 'လွှဲငွေအပိုင်း အက်ပ်မှ ပို့',\n",
    "  'ส่วนโอน ยิงจากแอป': 'လွှဲငွေအပိုင်း အက်ပ်မှ ပို့',\n"
    "  'ส่วนโอน กด Start ใน SOL': 'လွှဲငွေအပိုင်း SOL တွင် Start နှိပ်', // v212\n"
    "  'โอน กด Start ใน SOL': 'လွှဲငွေ SOL တွင် Start နှိပ်', // v212\n"
    "  'โอน → Start ใน SOL': 'လွှဲငွေ → SOL တွင် Start', // v212\n"
    "  'หยอดเหรียญส่วนสดก่อน → กดปุ่มด้านล่าง → ไปกด Start ใน SOL ส่วนโอน': 'ငွေသားအပိုင်း ဒင်္ဂါးအရင်ထည့် → အောက်ခလုတ်နှိပ် → လွှဲငွေအပိုင်း SOL တွင် Start နှိပ်', // v212\n")
rep("window.APP_VERSION = 'v211-2026-11-10';", "window.APP_VERSION = 'v212-2026-11-10';")
open(idx, 'w', encoding='utf-8').write(s)
w = open(sw, encoding='utf-8').read()
assert w.count("const CACHE_NAME = 'plp-laundry-v211';") == 1
open(sw, 'w', encoding='utf-8').write(w.replace("const CACHE_NAME = 'plp-laundry-v211';", "const CACHE_NAME = 'plp-laundry-v212';"))
print('v212 patched')
