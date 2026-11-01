#!/usr/bin/env python3
"""หน้าทดสอบ Otteri: index.html (ตัวจริง v175+) → test/index.html
ตั้งแต่ v175 ระบบใหม่ของ Otteri อยู่ในตัวจริงแล้ว → สคริปต์นี้แค่ห่อเป็นหน้าทดสอบ:
Firestore คอลเลกชัน test_* · localStorage คีย์ TEST: · ไม่ใช้ offline cache · ไม่ลง SW · ล็อกร้าน Otteri · ป้ายส้ม
usage: python3 tools/otteri-test/make_test.py index.html test/index.html
(patch_otteri_test.py = สคริปต์เดิมที่ใส่ฟีเจอร์ — ใช้ไปแล้วตอนทำ v175 ห้ามรันกับ index.html ปัจจุบัน)
"""
import sys

SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding='utf-8').read()
assert '// 🟢 v175' in s, 'index.html ยังไม่ใช่ v175+'


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    assert n == count, f'{label}: anchor found {n} times (want {count})'
    s = s.replace(old, new)


def rep_between(start, end, fn, label):
    """แทนข้อความตั้งแต่ start ถึง end (รวม end) ด้วย fn(chunk)"""
    global s
    a = s.find(start)
    assert a >= 0 and s.count(start) == 1, f'{label}: start anchor'
    b = s.find(end, a)
    assert b >= 0, f'{label}: end anchor'
    b += len(end)
    s = s[:a] + fn(s[a:b]) + s[b:]


# ======================= ส่วนที่ 2: test wrapper =======================
rep("""<meta charset="UTF-8">
""", """<meta charset="UTF-8">
<script>
  // 🧪 หน้าทดสอบ: แยกข้อมูลในเครื่อง (localStorage) จากแอปตัวจริง — ทุกคีย์ขึ้นต้น TEST:
  window.TEST_MODE = true;
  (function () {
    var P = Storage.prototype, g = P.getItem, st = P.setItem, rm = P.removeItem;
    var k = function (x) { return 'TEST:' + x; };
    P.getItem = function (x) { return g.call(this, k(x)); };
    P.setItem = function (x, v) { return st.call(this, k(x), v); };
    P.removeItem = function (x) { return rm.call(this, k(x)); };
  })();
  document.addEventListener('DOMContentLoaded', function () {
    var b = document.createElement('div');
    b.textContent = '🧪 Otteri ทดสอบ · ข้อมูลแยกจากร้านจริง';
    b.setAttribute('style', 'position:fixed;top:0;left:50%;transform:translateX(-50%);z-index:99999;background:#F97316;color:#fff;font:700 11px sans-serif;padding:2px 10px;border-radius:0 0 10px 10px;pointer-events:none;white-space:nowrap');
    document.body.appendChild(b);
  });
</script>
""", 'test head')
rep("<title>PLP Laundromat - ร้านสะดวกซักผ้า</title>", "<title>🧪 Otteri ทดสอบ</title>", 'title')

rep_between("  firebase.initializeApp(firebaseConfig);\n  window.db = firebase.firestore();", "  })();\n</script>", lambda c: """  firebase.initializeApp(firebaseConfig);
  window.db = firebase.firestore();
  window.APP_VERSION = 'otteri-test-2026-11-01';
  // 🧪 ทุกคอลเลกชันขึ้นต้น test_ — ไม่แตะใบงาน/เงินของร้านจริง
  (function () {
    var d = window.db, orig = d.collection.bind(d);
    d.collection = function (p) { p = String(p); return orig(p.indexOf('test_') === 0 ? p : 'test_' + p); };
  })();
  // 🧪 ไม่เปิด offline cache (ไม่ยุ่งกับ cache ของแอปตัวจริงในเครื่องเดียวกัน)
  window.dbReady = Promise.resolve();
</script>""", 'test db')

rep("  setInterval(trySwReload, 5000);", "  // 🧪 หน้าทดสอบ: ไม่รีโหลดตามตัวอัปเดตของแอปจริง", 'no sw reload')
rep("  if ('serviceWorker' in navigator) {\n    window.addEventListener('load', () => {\n      navigator.serviceWorker.register('./sw.js')",
    "  if (false && 'serviceWorker' in navigator) { // 🧪 หน้าทดสอบไม่ลง Service Worker\n    window.addEventListener('load', () => {\n      navigator.serviceWorker.register('./sw.js')", 'no sw')
rep('<link rel="manifest" href="./manifest.json">\n', '', 'no manifest')
rep('href="./icon-', 'href="../icon-', 'icons', count=3)
rep("const GUIDE_BASE = 'guide/';", "const GUIDE_BASE = '../guide/';", 'guide base')
rep("const APP_SHARE_URL = 'https://phoneyjung.github.io/otteri-teddy-app/';",
    "const APP_SHARE_URL = 'https://phoneyjung.github.io/otteri-teddy-app/test/';", 'share url')
rep("  const [brand, setBrand] = useState(DEEP_START ? DEEP_START.b : null);",
    "  const [brand, setBrand] = useState(DEEP_START ? DEEP_START.b : 'otteri'); // 🧪 ล็อกร้าน Otteri", 'lock brand')
rep("onChangeBrand={() => { setDeep(null); setBrand(null); }}",
    "onChangeBrand={() => { setDeep(null); setBrand('otteri'); }}", 'lock brand change')

assert 'teddy-pulse.phoneyjung.workers.dev' in s
open(OUT, 'w', encoding='utf-8').write(s)
print('patched OK:', len(s), 'chars')
