#!/usr/bin/env python3
"""v186 — ปุ่ม 📲 ติดตั้งแอปลงเครื่อง บนหน้าล็อกอิน (หน้าแรก)
ที่มา: เจ้าของ 2 พ.ย. 69 'ขอลิงส่งให้ admin เปิด แล้วมีปุ่มติดตั้งลงเครื่อง iphone หรือ แอนดรอยในหน้าแรก'
ทำอะไร
  - หน้าล็อกอินรวม: การ์ด 📲 ติดตั้งแอป (ซ่อนเมื่อเปิดจากไอคอนที่ติดตั้งแล้ว)
    Android (Chrome ส่ง beforeinstallprompt) = กดแล้วเด้งหน้าติดตั้งของเครื่องเลย
    iPhone/iPad = กดแล้วบอก 3 ขั้น (แชร์ ⬆️ → เพิ่มไปยังหน้าจอโฮม → เพิ่ม) · Android ที่ไม่เด้ง = บอกวิธีจากเมนู ⋮
  - ป๊อปอัปติดตั้งเดิม (เด้ง 5 วิ ล่างจอ) ไม่เด้งบนหน้าล็อกอินแล้ว (มีปุ่มแทน)
  - ลิงก์ส่ง LINE: ?openExternalBrowser=1 → LINE เปิดใน Chrome/Safari ให้เอง (ติดตั้งได้)
usage: python3 tools/v186_install_button.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v185-2026-11-02';", "window.APP_VERSION = 'v186-2026-11-02';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v185';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v185';", "const CACHE_NAME = 'plp-laundry-v186';")

# ---------- head script: เก็บ prompt ให้ React ใช้ · ไม่เด้งป๊อปอัปเดิมบนหน้าล็อกอิน ----------
rep("""    deferredPrompt = e;""",
    """    deferredPrompt = e;
    window.__installPrompt = e; // 📲 v186 ปุ่มติดตั้งบนหน้าล็อกอินใช้ตัวนี้
    window.dispatchEvent(new Event('pwa-installable'));""", 'expose prompt')
rep("""        document.getElementById('install-prompt').style.display = 'block';""",
    """        if (window.__loginPage) return; // v186 หน้าล็อกอินมีปุ่มติดตั้งแล้ว
        document.getElementById('install-prompt').style.display = 'block';""", 'android popup skip')
rep("""          document.getElementById('ios-install').style.display = 'block';""",
    """          if (window.__loginPage) return; // v186
          document.getElementById('ios-install').style.display = 'block';""", 'ios popup skip')

# ---------- การ์ดติดตั้ง ----------
rep("""function StaffLoginView({ config, staffList, staffStatus = 'ok', onLogin, onToggleLang, global, guestShops, onGuest, onOpenGuide }) {""",
    """// 📲 v186 ปุ่มติดตั้งแอปลงเครื่อง (หน้าล็อกอิน) — Android เด้งหน้าติดตั้ง · iPhone บอกวิธี · ติดตั้งแล้ว (เปิดจากไอคอน) = ซ่อน
function InstallAppCard({ config }) {
  const standalone = (() => { try { return window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true; } catch (e) { return false; } })();
  const ua = (navigator.userAgent || '').toLowerCase();
  const ios = /iphone|ipad|ipod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  const [, setTick] = useState(0);
  const [help, setHelp] = useState(false);
  const [done, setDone] = useState(false);
  useEffect(() => {
    window.__loginPage = true;
    const f = () => setTick(x => x + 1);
    const g = () => setDone(true);
    window.addEventListener('pwa-installable', f);
    window.addEventListener('appinstalled', g);
    return () => { window.__loginPage = false; window.removeEventListener('pwa-installable', f); window.removeEventListener('appinstalled', g); };
  }, []);
  if (standalone || done) return null;
  const go = async () => {
    const p = window.__installPrompt;
    if (p && !ios) {
      try { p.prompt(); const r = await p.userChoice; if (r && r.outcome === 'accepted') setDone(true); } catch (e) {}
      window.__installPrompt = null; setTick(x => x + 1);
      return;
    }
    setHelp(h => !h);
  };
  const step = (n, body) => (
    <p className="flex items-start gap-2 text-[13px] text-slate-700 leading-snug mt-1.5">
      <span className="flex-none w-5 h-5 rounded-full bg-sky-600 text-white text-[11px] font-extrabold flex items-center justify-center mt-0.5">{n}</span>
      <span>{body}</span>
    </p>
  );
  return (
    <div className="bg-white rounded-3xl p-4 shadow-2xl mb-3" data-install-card>
      <button onClick={go} data-install-btn className="w-full py-3 rounded-2xl text-white font-extrabold text-base active:scale-95 transition flex items-center justify-center gap-2" style={{ background: 'linear-gradient(135deg, #0EA5E9, #14B8A6)' }}>
        📲 {tr(config, ios ? 'ติดตั้งแอปลง iPhone' : 'ติดตั้งแอปลงเครื่อง')}
      </button>
      <p className="text-[11px] text-slate-500 text-center mt-1.5">{tr(config, 'ติดตั้งครั้งเดียว แล้วเปิดจากไอคอน PLP บนหน้าจอได้เลย')}</p>
      {help && (ios ? (
        <div className="mt-2 rounded-2xl bg-sky-50 border border-sky-200 px-3 py-2.5" data-install-help="ios">
          {step(1, <span>{tr(config, 'แตะปุ่มแชร์')} <b>⬆️</b> {tr(config, '(แถบล่างของ Safari)')}</span>)}
          {step(2, <span>{tr(config, 'เลื่อนลง เลือก')} <b>{tr(config, 'เพิ่มไปยังหน้าจอโฮม')}</b> (Add to Home Screen)</span>)}
          {step(3, <span>{tr(config, 'กด')} <b>{tr(config, 'เพิ่ม')}</b> {tr(config, 'มุมขวาบน')}</span>)}
          <p className="text-[11px] text-slate-500 mt-2">{tr(config, 'เปิดจาก LINE อยู่? แตะ ⋯ มุมขวาบน → เปิดใน Safari ก่อน')}</p>
        </div>
      ) : (
        <div className="mt-2 rounded-2xl bg-sky-50 border border-sky-200 px-3 py-2.5" data-install-help="android">
          {step(1, <span>{tr(config, 'แตะ')} <b>⋮</b> {tr(config, 'มุมขวาบนของ Chrome')}</span>)}
          {step(2, <span>{tr(config, 'เลือก')} <b>{tr(config, 'ติดตั้งแอป')}</b> {tr(config, 'หรือ')} <b>{tr(config, 'เพิ่มลงในหน้าจอหลัก')}</b></span>)}
          {step(3, <span>{tr(config, 'กด')} <b>{tr(config, 'ติดตั้ง')}</b></span>)}
          <p className="text-[11px] text-slate-500 mt-2">{tr(config, 'เปิดจาก LINE อยู่? แตะ ⋮ มุมขวาบน → เปิดด้วย Chrome ก่อน')}</p>
        </div>
      ))}
    </div>
  );
}

function StaffLoginView({ config, staffList, staffStatus = 'ok', onLogin, onToggleLang, global, guestShops, onGuest, onOpenGuide }) {""", 'InstallAppCard')
rep("""        {/* ===== โหมดจัดการรายชื่อ ===== */}""",
    """        {global && !manageMode && step === 'pick' && <InstallAppCard config={config} />}
        {/* ===== โหมดจัดการรายชื่อ ===== */}""", 'card on login page')

# ---------- MM ----------
rep("""  // v185 ฟอร์มงานภายในแบบสั้น""",
    """  // v186 ปุ่มติดตั้งแอป
  'ติดตั้งแอปลง iPhone': 'iPhone တွင် အက်ပ်ထည့်ရန်',
  'ติดตั้งแอปลงเครื่อง': 'ဖုန်းထဲ အက်ပ်ထည့်ရန်',
  'ติดตั้งครั้งเดียว แล้วเปิดจากไอคอน PLP บนหน้าจอได้เลย': 'တစ်ခါထည့်ပြီး မျက်နှာပြင်ရှိ PLP အိုင်ကွန်မှ ဖွင့်နိုင်သည်',
  'แตะปุ่มแชร์': 'Share ခလုတ်ကို နှိပ်ပါ',
  '(แถบล่างของ Safari)': '(Safari အောက်ဘား)',
  'เลื่อนลง เลือก': 'အောက်ဆွဲပြီး ရွေးပါ',
  'เพิ่มไปยังหน้าจอโฮม': 'Home Screen သို့ထည့်ရန်',
  'กด': 'နှိပ်ပါ',
  'มุมขวาบน': 'ညာဘက်အပေါ်ထောင့်',
  'เปิดจาก LINE อยู่? แตะ ⋯ มุมขวาบน → เปิดใน Safari ก่อน': 'LINE မှဖွင့်ထားလား? ⋯ ကိုနှိပ် → Safari ဖြင့်ဖွင့်ပါ',
  'แตะ': 'နှိပ်ပါ',
  'มุมขวาบนของ Chrome': 'Chrome ညာဘက်အပေါ်ထောင့်',
  'เลือก': 'ရွေးပါ',
  'ติดตั้งแอป': 'အက်ပ်ထည့်သွင်းရန်',
  'หรือ': 'သို့မဟုတ်',
  'เพิ่มลงในหน้าจอหลัก': 'Home Screen သို့ထည့်ရန်',
  'ติดตั้ง': 'ထည့်သွင်းရန်',
  'เปิดจาก LINE อยู่? แตะ ⋮ มุมขวาบน → เปิดด้วย Chrome ก่อน': 'LINE မှဖွင့်ထားလား? ⋮ ကိုနှိပ် → Chrome ဖြင့်ဖွင့်ပါ',
  // v185 ฟอร์มงานภายในแบบสั้น""", 'MM')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v186 applied')
