#!/usr/bin/env python3
"""v215: machine-cleaning quota resets every Monday 09:00 (owner, 16 Nov 2026).
Before: rolling 7x24h from the last clean -> a maid who cleaned Mon 12:00 could not clean next Mon before 12:00.
Now: 1 clean per washer per week; the week starts Monday 09:00 (device local time). Owner is still never locked.
Usage: python3 tools/v215_clean_week_reset.py index.html sw.js"""
import sys
idx, sw = sys.argv[1], sys.argv[2]
s = open(idx, encoding='utf-8').read()
def rep(old, new):
    global s
    assert s.count(old) == 1, ('count', s.count(old), old[:80])
    s = s.replace(old, new)

rep("""// เครื่องที่ล้างไปแล้วภายใน 7 วัน → { label: { at, until } }
function cleanLocksOf(orders, exceptId) {
  const out = {};
  const now = Date.now();
  (orders || []).forEach(o => {
    if (o.internalType !== 'clean' || (exceptId && o.id === exceptId)) return;
    const at = o.createdAt || 0;
    if (now - at >= CLEAN_EVERY_DAYS * 86400000) return;
    (o.internalMachines || []).forEach(lb => { if (!out[lb] || out[lb].at < at) out[lb] = { at, until: at + CLEAN_EVERY_DAYS * 86400000 }; });
  });
  return out;
}""", """// 🧼 v215 สิทธิ์ล้างเครื่องเริ่มนับใหม่ทุกวันจันทร์ 9:00 (เดิมนับ 7×24 ชม. จากครั้งก่อน → ล้างจันทร์เที่ยง จันทร์หน้าเช้าล้างไม่ได้)
const CLEAN_RESET_DOW = 1, CLEAN_RESET_HOUR = 9; // จันทร์ 9:00 เวลาเครื่อง
function cleanWeekStart(now) {
  const d = new Date(now == null ? Date.now() : now);
  const s = new Date(d.getFullYear(), d.getMonth(), d.getDate(), CLEAN_RESET_HOUR, 0, 0, 0);
  s.setDate(s.getDate() - ((d.getDay() - CLEAN_RESET_DOW + 7) % 7));
  if (s.getTime() > d.getTime()) s.setDate(s.getDate() - 7); // จันทร์ก่อน 9:00 = ยังเป็นสัปดาห์ก่อน
  return s.getTime();
}
// เครื่องที่ล้างไปแล้วในสัปดาห์นี้ (ตั้งแต่จันทร์ 9:00) → { label: { at, until } }
function cleanLocksOf(orders, exceptId, nowMs) {
  const out = {};
  const start = cleanWeekStart(nowMs);
  const ns = new Date(start); ns.setDate(ns.getDate() + CLEAN_EVERY_DAYS);
  const until = ns.getTime();
  (orders || []).forEach(o => {
    if (o.internalType !== 'clean' || (exceptId && o.id === exceptId)) return;
    const at = o.createdAt || 0;
    if (at < start) return;
    (o.internalMachines || []).forEach(lb => { if (!out[lb] || out[lb].at < at) out[lb] = { at, until }; });
  });
  return out;
}""")
rep("internalMaidIssues.push(`ล้างไปแล้วใน ${CLEAN_EVERY_DAYS} วัน: ${lockedSel.join(', ')}`);",
    "internalMaidIssues.push(`ล้างไปแล้วในสัปดาห์นี้ (ล้างได้อีกจันทร์ ${CLEAN_RESET_HOUR}:00): ${lockedSel.join(', ')}`);")
rep("\\nล้างได้อีกครั้ง ${until}`); return; }", "\\nล้างได้อีกครั้ง จันทร์ ${until} ${CLEAN_RESET_HOUR}:00`); return; }")
rep("window.APP_VERSION = 'v214-2026-11-12';", "window.APP_VERSION = 'v215-2026-11-16';")
open(idx, 'w', encoding='utf-8').write(s)
w = open(sw, encoding='utf-8').read()
assert w.count("const CACHE_NAME = 'plp-laundry-v214';") == 1
open(sw, 'w', encoding='utf-8').write(w.replace("const CACHE_NAME = 'plp-laundry-v214';", "const CACHE_NAME = 'plp-laundry-v215';"))
print('v215 patched')
