#!/usr/bin/env python3
"""v217: Teddy 2 owner — list 'ลูกค้าใช้โปร (ซักเอง)' records in the ส่วนลด tab with a delete button.
Case (owner, 16 Nov 2026): a maid recorded a self-wash coupon as 'ตัดเครดิต' but the owner had fired the machine himself;
the Teddy 2 owner screen had no way to delete it (only token shops / Teddy 1 listed these records).
Delete = remove the creditLedger entry + void the linked 'credit' / owner-'manual' pulse logs in ONE batch
(void = not counted as credit the maid used). Records whose machine start was a real app pulse or coins cannot be
deleted here — those logs must stay for the machine reconciliation.
Usage: python3 tools/v217_t2_self_promo_delete.py index.html sw.js"""
import sys
idx, sw = sys.argv[1], sys.argv[2]
s = open(idx, encoding='utf-8').read()
def rep(old, new):
    global s
    assert s.count(old) == 1, ('count', s.count(old), old[:80])
    s = s.replace(old, new)

# 1) helper next to deleteCreditEntry
rep("""async function updateCreditEntry(id, updates) {""", """// 🗑️ v217 เจ้าของลบรายการ "ลูกค้าใช้โปร (ซักเอง)" ของร้านที่เริ่มเครื่องผ่านแอป/ตัดเครดิต (Teddy 2)
// ใช้เมื่อรายการนั้นไม่ได้เกิดขึ้นจริง (ลงซ้ำ/ลงผิด/เจ้าของยิงเครื่องให้เอง) → ลบรายการ + ยกเลิก (void) บันทึกตัดเครดิต / บันทึกของเจ้าของ ที่ผูกอยู่ ในครั้งเดียว
// void = ไม่นับเป็นเครดิตที่แม่บ้านใช้ · พัลส์ที่ยิงเครื่องจริงผ่านแอปหรือเหรียญที่หยอดจริง ลบไม่ได้ (ต้องเหลือไว้กระทบยอดกับเครื่อง)
async function selfPromoLinkedLogs(entryId) {
  const snap = await window.db.collection('pulseLogs').where('refId', '==', entryId).get();
  const linked = snap.docs.map(d => ({ id: d.id, ...d.data() })).filter(l => l.refType === 'promo' && PULSE_LIVE.includes(l.status));
  const soft = linked.filter(l => l.method === 'credit' || l.method === 'manual');
  return { soft, real: linked.filter(l => !soft.includes(l)) };
}
async function deleteSelfPromoEntry(entryId, soft) {
  const b = window.db.batch();
  b.delete(window.db.collection('creditLedger').doc(entryId));
  const now = Date.now();
  (soft || []).forEach(l => b.set(window.db.collection('pulseLogs').doc(l.id), { status: 'void', voidAt: now,
    voidReason: l.method === 'manual' ? 'เจ้าของลบรายการโปร (บันทึกว่าเริ่ม ไม่ได้ยิงจริง)' : 'เจ้าของลบรายการโปร — ไม่ได้ตัดเครดิตจริง' }, { merge: true }));
  await b.commit();
}

async function updateCreditEntry(id, updates) {""")

# 2) owner dashboard: load the records for machine shops too
rep("""    if (!window.db || machineSys || !menuOn(config, 'promoCredit')) { setSelfPromo([]); return; }
    const u = subscribeToCreditLedger(config.brand, l => setSelfPromo(l.filter(e => e.type === 'promo')));
    return () => { if (u) u(); };
  }, [config.brand, machineSys]);""", """    if (!window.db || !menuOn(config, 'promoCredit')) { setSelfPromo([]); return; } // v217: ร้านที่เริ่มเครื่องผ่านแอป/ตัดเครดิต (Teddy 2) ก็โหลด → มีปุ่มลบ
    const u = subscribeToCreditLedger(config.brand, l => setSelfPromo(l.filter(e => e.type === 'promo')));
    return () => { if (u) u(); };
  }, [config.brand, machineSys]);
  const [promoDelBusy, setPromoDelBusy] = useState(null);
  const delSelfPromo = async (e) => {
    if (promoDelBusy) return;
    setPromoDelBusy(e.id);
    try {
      const { soft, real } = await selfPromoLinkedLogs(e.id);
      if (real.length) { alert(`ลบที่นี่ไม่ได้ — รายการนี้${real.some(pulseIsCoin) ? 'หยอดเหรียญ' : 'ยิงเครื่อง'}จริง (${real.map(l => l.machineLabel + ' ฿' + l.baht).join(', ')})\\nต้องเหลือไว้กระทบยอดกับเครื่อง`); return; }
      const cr = soft.filter(l => l.method === 'credit'), mn = soft.filter(l => l.method === 'manual');
      const lines = [`🗑️ ลบรายการนี้?`, `🎟️ ${e.promoName || 'โปร'}${e.machine ? ' · ' + e.machine : ''} · ฿${formatMoney(e.amount || 0)}`, `👤 ${e.staffName || '-'} · ${t2When(e.createdAt)}`, ''];
      if (cr.length) lines.push(`บันทึก "ตัดเครดิต ฿${formatMoney(cr.reduce((a, l) => a + (l.baht || 0), 0))}" ของ ${cr[0].staffName || '-'} จะถูกยกเลิกด้วย`, `(ใช้เมื่อแม่บ้านไม่ได้ตัดเครดิตจริง · เครดิตที่ใช้ในแอปจะลดลง)`);
      if (mn.length) lines.push(`บันทึกของเจ้าของ (ไม่ยิงเครื่อง) จะถูกยกเลิกด้วย`);
      lines.push('ลบแล้วกู้คืนไม่ได้');
      if (!confirm(lines.join('\\n'))) return;
      await deleteSelfPromoEntry(e.id, soft);
    } catch (err) { alert('ลบไม่สำเร็จ: ' + (err && err.message ? err.message : err)); }
    finally { setPromoDelBusy(null); }
  };""")

# 3) ส่วนลด tab: list + delete for machine shops (Teddy 2)
rep("""            {listHead(`ใบงานที่มีส่วนลด · ${R.label}`, A.discN)}""", """            {machineSys && menuOn(config, 'promoCredit') && (() => {
              const sp = selfPromo.filter(e => { const x = t2Ts(e.createdAt); return x >= R.from && x < R.to; }).sort((a, b) => t2Ts(b.createdAt) - t2Ts(a.createdAt));
              const spSum = sp.reduce((a2, e) => a2 + (e.amount || 0), 0);
              const how = (e) => e.manual || e.pulseStatus === 'manual' ? '✍️ เจ้าของบันทึก (ไม่ยิงเครื่อง)' : e.pulseStatus === 'credit' ? '🎟️ ตัดเครดิต' : e.pulseLogId ? '⚡ ยิงแอป' : '';
              return (
                <T2Box k="discount" title={`🎟️ ลูกค้าใช้โปร (ซักเอง) · ${R.label}`} right={<span className="text-xs font-bold text-slate-500 tabular-nums">฿{formatMoney(spSum)} · {sp.length} รายการ</span>}>
                  <div data-self-promo-t2 className="divide-y divide-slate-100">
                    {sp.map(e => (
                      <div key={e.id} className="flex items-center gap-2 py-2">
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-extrabold text-slate-900 truncate">{e.promoName || 'โปร'}{e.machine ? ' · ' + e.machine : ''}</p>
                          <p className="text-xs text-slate-500">{t2When(e.createdAt)} · {e.staffName || '-'}</p>
                          {how(e) && <p className="text-xs font-bold text-slate-600">{how(e)}{e.note ? ' · ' + e.note : ''}</p>}
                        </div>
                        <span className="text-sm font-extrabold tabular-nums">฿{formatMoney(e.amount || 0)}</span>
                        <button data-self-promo-del onClick={() => delSelfPromo(e)} disabled={promoDelBusy === e.id}
                          className="px-2.5 py-1.5 rounded-lg border border-slate-200 text-xs font-bold text-slate-500 active:scale-95 disabled:opacity-50">{promoDelBusy === e.id ? '…' : 'ลบ'}</button>
                      </div>
                    ))}
                    {sp.length === 0 && <p className="text-sm text-slate-500 py-1">ไม่มีรายการใน{R.label}</p>}
                  </div>
                  <p className="text-[11px] text-slate-500 mt-1.5">ลูกค้าซักเอง ไม่ใช่งานฝาก · ลบ = ลบรายการ และยกเลิกบันทึกตัดเครดิตที่ผูกอยู่ (ใช้เมื่อไม่ได้ตัดเครดิตจริง)</p>
                </T2Box>
              );
            })()}
            {listHead(`ใบงานที่มีส่วนลด · ${R.label}`, A.discN)}""")

rep("window.APP_VERSION = 'v216-2026-11-16';", "window.APP_VERSION = 'v217-2026-11-16';")
open(idx, 'w', encoding='utf-8').write(s)
w = open(sw, encoding='utf-8').read()
assert w.count("const CACHE_NAME = 'plp-laundry-v216';") == 1
open(sw, 'w', encoding='utf-8').write(w.replace("const CACHE_NAME = 'plp-laundry-v216';", "const CACHE_NAME = 'plp-laundry-v217';"))
print('v217 patched')
