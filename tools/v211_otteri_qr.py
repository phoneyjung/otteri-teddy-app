#!/usr/bin/env python3
"""v211: Otteri gets its own PromptPay QR (K+ shop QR the owner sent 10 Nov 2026).
Shows on: 🧴 detergent sale paid by transfer, and the job receipt of transfer / split jobs (QR with the amount).
Usage: python3 tools/v211_otteri_qr.py index.html sw.js <static-qr-dataurl.txt>"""
import sys
idx, sw, durl = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(idx, encoding='utf-8').read()
static_qr = open(durl, encoding='utf-8').read().strip()
assert static_qr.startswith('data:image/png;base64,')

def rep(old, new):
    global s
    assert s.count(old) == 1, ('count', s.count(old), old[:80])
    s = s.replace(old, new)

rep("PROMPTPAY_MERCHANTS.teddy2 = '0016A0000006770101110315004999219820098'; // K+ Teddy 2 (บัญชีคุณทองไป่)\n",
    "PROMPTPAY_MERCHANTS.teddy2 = '0016A0000006770101110315004999219820098'; // K+ Teddy 2 (บัญชีคุณทองไป่)\n"
    "PROMPTPAY_MERCHANTS.otteri = '0016A0000006770101110315004999228697883'; // K+ Otteri (บัญชีคุณปุรวิชญ์ · QR ร้าน Otteri · v211)\n")
rep("PAYMENT_ACCOUNT_NAMES.trainee = PAYMENT_ACCOUNT_NAMES.teddy;\n",
    "PAYMENT_ACCOUNT_NAMES.trainee = PAYMENT_ACCOUNT_NAMES.teddy;\n"
    "PAYMENT_ACCOUNT_NAMES.otteri = 'นาย ปุรวิชญ์ หงษาชาติ · KBank'; // v211\n")
rep("PAYMENT_QRS.trainee = PAYMENT_QRS.teddy;",
    "PAYMENT_QRS.otteri = '" + static_qr + "'; // v211 QR ร้าน Otteri แบบไม่ระบุยอด (สำรองตอนไลบรารี QR โหลดไม่ทัน)\nPAYMENT_QRS.trainee = PAYMENT_QRS.teddy;")
rep("window.APP_VERSION = 'v210-2026-11-10';", "window.APP_VERSION = 'v211-2026-11-10';")
open(idx, 'w', encoding='utf-8').write(s)

w = open(sw, encoding='utf-8').read()
assert w.count("const CACHE_NAME = 'plp-laundry-v210';") == 1
w = w.replace("const CACHE_NAME = 'plp-laundry-v210';", "const CACHE_NAME = 'plp-laundry-v211';")
open(sw, 'w', encoding='utf-8').write(w)
print('v211 patched')
