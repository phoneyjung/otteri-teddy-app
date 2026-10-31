#!/usr/bin/env python3
"""v172 — Teddy 1 ใช้หน้าเจ้าของแบบเท็ดดี้ 2 (เดิมหน้าเก่า: แท็บ 'ทั้งหมด' โหลดใบงานทุกใบพร้อมรูปในครั้งเดียว → ช้ามาก)
- เมนูล่าง เงิน/งาน/เครื่อง/ตั้งค่า · ดูรายวัน/เดือน/ปี · รายการแสดงครั้งละไม่เกิน 150 ใบ (เหมือน Teddy 2)
- ร้านที่ไม่มีระบบยิงพัลส์ (Teddy 1): ไม่มีแท็บพัลส์ · ไม่โหลด pulseLogs · ซ่อนตัวเลข 'เข้าเครื่อง' / 'ยิงจากแอป'
- Teddy 1 เก็บแท็บเดิม 2 อัน: 🪙 แลกโทเค็น (เมนู เงิน) · 👨‍💼 เคฟ (เมนู งาน) — หยอดเพิ่ม/เครดิต ตัดออกเหมือน Teddy 2
- Teddy 2 / Otteri ทดสอบ หน้าตาเหมือนเดิม · Otteri ตัวจริง / มือใหม่ ยังใช้หน้าเก่า
usage: python3 tools/v172_t1_owner.py index.html sw.js
"""
import sys

IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read()
sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    assert n == count, f'{label}: found {n}, expected {count}'
    s = s.replace(old, new)


# ---------- version ----------
rep("window.APP_VERSION = 'v171-2026-10-30';", "window.APP_VERSION = 'v172-2026-10-31';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v171';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v171';", "const CACHE_NAME = 'plp-laundry-v172';")

# ---------- เลือกหน้าเจ้าของ ----------
rep("{view === 'ownerDashboard' && config.brand === 'teddy2' && <OwnerDashboardT2 config={config} orders={orders} collections={collections} tokenExchanges={tokenExchanges} staffList={staffList} ",
    "{view === 'ownerDashboard' && t2OwnerOn(config) && <OwnerDashboardT2 config={config} orders={orders} collections={collections} tokenExchanges={tokenExchanges} staffList={staffList} onDeleteToken={handleDeleteTokenExchange} ",
    'gate owner T2')
rep("{view === 'ownerDashboard' && config.brand !== 'teddy2' && <OwnerDashboardView",
    "{view === 'ownerDashboard' && !t2OwnerOn(config) && <OwnerDashboardView", 'gate owner old')

# ---------- สีหมวด + กลุ่มเมนูต่อร้าน ----------
rep("""  settings: { c: T2_NEUTRAL, soft: '#F1F5F9', ic: '⚙️', name: 'ตั้งค่า' },
};""", """  settings: { c: T2_NEUTRAL, soft: '#F1F5F9', ic: '⚙️', name: 'ตั้งค่า' },
  token: { c: T2_NEUTRAL, soft: '#F1F5F9', ic: '🪙', name: 'Token' }, // v172 Teddy 1 (แลก Token)
  kev: { c: T2_NEUTRAL, soft: '#F1F5F9', ic: '👨‍💼', name: 'เคฟ' }, // v172 Teddy 1
};""", 'T2C extra')
rep("""  { id: 'settings', ic: '⚙️', label: 'ตั้งค่า', tabs: ['settings'] },
];""", """  { id: 'settings', ic: '⚙️', label: 'ตั้งค่า', tabs: ['settings'] },
];
// 🏠 v172: หน้าเจ้าของแบบนี้ใช้กับ Teddy 2 + Teddy 1 (+ ร้านที่เปิด t2Sys) · ร้านอื่นยังใช้หน้าเก่า
const t2OwnerOn = (config) => !!config && (config.brand === 'teddy2' || config.brand === 'teddy' || !!config.t2Sys);
// แท็บเดิมที่บางร้านยังใช้ (Teddy 2 ตัดไปแล้ว) · Teddy 1: แลกโทเค็น (เงิน) + เคฟ (งาน)
const T2_EXTRA_TABS = { teddy: { money: ['token'], work: ['kev'] } };
// สีปุ่ม + รับงาน ตามร้าน (Teddy 2 เขียวเดิม · Teddy 1 น้ำเงิน — เข้มพอให้ตัวหนังสือบนพื้นขาวอ่านชัด)
const T2_BRAND_PRIMARY = { teddy: '#2563EB' };
const t2PrimaryOf = (config) => config.t2Primary || T2_BRAND_PRIMARY[config.brand] || T2_PRIMARY;
// ร้านที่ไม่มีระบบยิงพัลส์ (ไม่มี config.pulse) ไม่มีแท็บพัลส์
function t2Groups(config) {
  const extra = T2_EXTRA_TABS[config.brand] || {};
  return T2_GROUPS.map(g => ({ ...g, tabs: g.tabs.filter(k => k !== 'pulse' || !!config.pulse).concat(extra[g.id] || []) }));
}""", 'groups helper')

# ---------- OwnerDashboardT2 ----------
rep("function OwnerDashboardT2({ config, orders, collections, tokenExchanges, staffList, onLogout, onSelectOrder, onCollect, onPayFees, onNewOrder, onChangeBrand, onResetAll, onDeleteSelected }) {\n  const [tab, setTab] = useState(T2_DASH_MEM.tab);",
    "function OwnerDashboardT2({ config, orders, collections, tokenExchanges, staffList, onLogout, onSelectOrder, onCollect, onPayFees, onDeleteToken, onNewOrder, onChangeBrand, onResetAll, onDeleteSelected }) {\n"
    "  const G = useMemo(() => t2Groups(config), [config]); // v172 เมนูต่อร้าน\n"
    "  const hasTab = (k) => G.some(g => g.tabs.includes(k));\n"
    "  const [tab, setTab] = useState(() => (hasTab(T2_DASH_MEM.tab) ? T2_DASH_MEM.tab : 'overview'));\n"
    "  useEffect(() => { if (!hasTab(tab)) setTab('overview'); }, [G]); // สลับร้านแล้วแท็บเดิมไม่มี → กลับภาพรวม\n"
    "  const machineSys = !!config.pulse; // ร้านที่เปิดเครื่องผ่านแอป/SOL",
    'T2 head')
rep("""    if (!window.db) return;
    const u = window.db.collection('pulseLogs').where('dateKey', '>=', R.fromKey).where('dateKey', '<=', R.toKey).onSnapshot(
      sn => setLogs(sn.docs.map(x => ({ id: x.id, ...x.data() }))), e => console.error('t2 logs error:', e));
    return () => { if (u) u(); };
  }, [R.fromKey, R.toKey]);""", """    if (!window.db || !machineSys) { setLogs([]); return; } // v172: ร้านไม่มีระบบยิงพัลส์ ไม่ต้องโหลด (และไม่เอาของร้านอื่นมาปน)
    const u = window.db.collection('pulseLogs').where('dateKey', '>=', R.fromKey).where('dateKey', '<=', R.toKey).onSnapshot(
      sn => setLogs(sn.docs.map(x => ({ id: x.id, ...x.data() }))), e => console.error('t2 logs error:', e));
    return () => { if (u) u(); };
  }, [R.fromKey, R.toKey, machineSys]);""", 'logs gate')
rep("  const openTab = (k) => { if (!T2_GROUPS.find(g => g.tabs.includes(k)).tabs.includes(tab)) setToast(null);",
    "  const openTab = (k) => { if (!(G.find(g => g.tabs.includes(k)) || G[0]).tabs.includes(tab)) setToast(null);", 'openTab')
rep("  const group = T2_GROUPS.find(g => g.tabs.includes(tab)) || T2_GROUPS[0];",
    "  const group = G.find(g => g.tabs.includes(tab)) || G[0];", 'group')
rep("{[T2_GROUPS[0], T2_GROUPS[1], null, T2_GROUPS[2], T2_GROUPS[3]].map((g, i) => g ? (",
    "{[G[0], G[1], null, G[2], G[3]].map((g, i) => g ? (", 'bottom nav')

# ข้อความ/ตัวเลขที่เป็นของระบบเปิดเครื่อง → ซ่อนในร้านที่ไม่มี
rep("sub: `${cashPendList.length} ใบ · ค่าน้ำยา/ยังไม่หยอดเครื่อง${coinCashSum > 0",
    "sub: `${cashPendList.length} ใบ${machineSys ? ' · ค่าน้ำยา/ยังไม่หยอดเครื่อง' : ''}${coinCashSum > 0", 'todo cash sub')
rep("{moneyRow('cash', A.cash, `เข้าเครื่อง ฿${formatMoney(A.coin)} · แม่บ้านรับ ฿${formatMoney(A.held)}`, cashPct)}",
    "{moneyRow('cash', A.cash, machineSys ? `เข้าเครื่อง ฿${formatMoney(A.coin)} · แม่บ้านรับ ฿${formatMoney(A.held)}` : `${formatMoney(A.cashN)} ใบ`, cashPct)}", 'money row cash')
rep("""              <div className="grid grid-cols-3 gap-2">
                <T2Stat label="เงินสดรวม" value={'฿' + formatMoney(A.cash)} sub={`${A.cashN} ใบ`} color={T2C.cash.c} />
                <T2Stat label="เข้าเครื่อง" value={'฿' + formatMoney(A.coin)} sub="ไม่ต้องเก็บ" />""",
    """              <div className={machineSys ? 'grid grid-cols-3 gap-2' : 'grid grid-cols-2 gap-2'}>
                <T2Stat label="เงินสดรวม" value={'฿' + formatMoney(A.cash)} sub={`${A.cashN} ใบ`} color={T2C.cash.c} />
                {machineSys && <T2Stat label="เข้าเครื่อง" value={'฿' + formatMoney(A.coin)} sub="ไม่ต้องเก็บ" />}""", 'cash stats')
rep("""              <div className="grid grid-cols-2 gap-2">
                <T2Stat label="โอนทั้งหมด" """, """              <div className={machineSys ? 'grid grid-cols-2 gap-2' : 'grid grid-cols-1 gap-2'}>
                <T2Stat label="โอนทั้งหมด" """, 'transfer grid')
rep("""                <T2Stat label="ยิงจากแอป (ส่วนโอน)" value={'฿' + formatMoney(PB.transfer)}""",
    """                {machineSys && <T2Stat label="ยิงจากแอป (ส่วนโอน)" value={'฿' + formatMoney(PB.transfer)}""", 'transfer stat open')
# ปิดปีกกาของ stat โอน: หาแถวเต็มแล้วต่อ '}'
i = s.find("{machineSys && <T2Stat label=\"ยิงจากแอป (ส่วนโอน)\"")
j = s.find("/>", i)
assert i > 0 and j > i
s = s[:j + 2] + "}" + s[j + 2:]
rep("""                <T2Stat label="ยิงแอปให้ส่วนลด" value={'฿' + formatMoney(PB.discount)} sub={PB.promo ? `รวมโปรซักเอง ฿${formatMoney(PB.promo)}` : 'เฉพาะเครื่องซัก'} />""",
    """                {machineSys && <T2Stat label="ยิงแอปให้ส่วนลด" value={'฿' + formatMoney(PB.discount)} sub={PB.promo ? `รวมโปรซักเอง ฿${formatMoney(PB.promo)}` : 'เฉพาะเครื่องซัก'} />}""", 'discount stat')

rep("style={{ background: T2_PRIMARY }}>+", "style={{ background: t2PrimaryOf(config) }}>+", 'fab colour')
rep("style={{ color: T2_PRIMARY }}>รับงาน", "style={{ color: t2PrimaryOf(config) }}>รับงาน", 'fab label colour')
# ชื่อการแลกตามร้าน (Teddy 1 = แลก Token · Teddy 2 = แลกเหรียญ เหมือนเดิม)
rep("` · แลกเหรียญ ฿${formatMoney(coinCashSum)}`", "` · ${exchangeName(config)} ฿${formatMoney(coinCashSum)}`", 'todo exchange name')
rep("`🪙 แลกเหรียญ ฿${formatMoney(coinCashSum)}", "`🪙 ${exchangeName(config)} ฿${formatMoney(coinCashSum)}", 'cash note exchange name')

# แท็บเดิมของ Teddy 1
rep("""        {tab === 'coins' && <CoinCountView config={config} />}""",
    """        {tab === 'coins' && <CoinCountView config={config} />}
        {tab === 'token' && <TokenExchangeReportView config={config} tokenExchanges={tokenExchanges || []} onDelete={onDeleteToken} />}
        {tab === 'kev' && <KevReportView orders={orders} config={config} />}""", 'extra tabs')

open(IDX, 'w', encoding='utf-8').write(s)
open(SW, 'w', encoding='utf-8').write(sw)
print('v172 applied')
