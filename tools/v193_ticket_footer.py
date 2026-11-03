#!/usr/bin/env python3
"""v193 — ท้ายใบงาน (ใบรับฝากซัก-อบ-พับ) = โปรโมทร้าน + ช่องทางติดต่อกลับ
ที่มา: เจ้าของ 3 พ.ย. 69 'เปลี่ยนข้อความข้างล่างเป็นโปรโมทร้านดีกว่า และให้เจ้าของผ้าติดต่อกลับได้ด้วย
       เช่นพบปัญหาติดต่อได้ · QR แอดไลน์ ไอดีไลน์ และก็เบอร์โทร'
ทำอะไร
  - config.ticketFooter ต่อร้าน (ข้อมูลจาก FACTS-shop.md 29 ต.ค.):
      Teddy 2: LINE @736vkujr (lin.ee/tLp9JME) · เบอร์ร้าน · แอดมินตอบ 09:00–21:00 · เปิด 24 ชม. ·
               ฝากซัก อบ พับ ฟรี · ส่งก่อน 20:00 ได้คืนวันเดียวกัน · เดลิเวอรี่ 20–50฿ · แอดไลน์ครั้งแรก ลดค่าซัก 50฿
      Teddy 1: LINE @teddy.np · ฝากซัก อบ พับ ฟรี · เดลิเวอรี่ 20–50฿ (เบอร์/โปร รอเจ้าของยืนยัน)
  - ท้ายใบงาน: สโลแกน · จุดเด่นร้าน · กรอบ 'ผ้ามีปัญหา / สอบถาม' + QR แอดไลน์ + ไอดีไลน์ + เบอร์ ·
    ป้ายโปรแอดไลน์ (ซ่อนถ้าใบนี้ใช้โปรแอดไลน์แล้ว) · ชื่อร้าน · ขอบคุณที่ใช้บริการ
  - ร้านที่ไม่มี ticketFooter (Otteri) = ท้ายใบแบบเดิม
usage: python3 tools/v193_ticket_footer.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v192-2026-11-03';", "window.APP_VERSION = 'v193-2026-11-03';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v192';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v192';", "const CACHE_NAME = 'plp-laundry-v193';")

# ---------- ข้อมูลร้านท้ายใบงาน ----------
rep("""  hasLinePromo: true,
  linePromoDiscount: 40,
""", """  hasLinePromo: true,
  linePromoDiscount: 40,
  // 🧾 v193 ท้ายใบงาน = โปรโมทร้าน + ช่องทางติดต่อกลับ (เบอร์/โปรแอดไลน์ Teddy 1 รอเจ้าของยืนยัน)
  ticketFooter: { slogan: 'ซักก็ไว ใส่ก็วิ๊ง! ที่เท็ดดี้', lineId: '@teddy.np', lineUrl: 'https://line.me/R/ti/p/@teddy.np', phone: '', hours: '', linePromo: false, perks: ['ฝากซัก อบ พับ ฟรี · จ่ายแค่ค่าเครื่อง', 'เดลิเวอรี่ 20–50฿'] },
""", 'teddy1 footer')
rep("""  linePromoDiscount: 50, // Teddy 2 ลดแอดไลน์ 50 (มากกว่า Teddy 1)
""", """  linePromoDiscount: 50, // Teddy 2 ลดแอดไลน์ 50 (มากกว่า Teddy 1)
  // 🧾 v193 ท้ายใบงาน (ข้อมูลจาก FACTS-shop.md 29 ต.ค.)
  ticketFooter: { slogan: 'ซักก็ไว ใส่ก็วิ๊ง! ที่เท็ดดี้', lineId: '@736vkujr', lineUrl: 'https://lin.ee/tLp9JME', phone: '083-145-6588', hours: 'แอดมินตอบ 09:00–21:00', linePromo: true, perks: ['เปิด 24 ชม. · ฝากซัก อบ พับ ฟรี จ่ายแค่ค่าเครื่อง', 'ส่งก่อน 20:00 ได้คืนวันเดียวกัน · เดลิเวอรี่ 20–50฿'] }, // leakcheck:allow เบอร์ร้าน (เจ้าของสั่งพิมพ์บนใบงาน 3 พ.ย.)
""", 'teddy2 footer')

# ---------- ท้ายใบงาน ----------
rep("""              <div style={{ textAlign: 'center', fontSize: '18px', borderTop: '1px dashed #000', paddingTop: '6px' }}>
                {config.subtitle}<br/>ขอบคุณที่ใช้บริการ
              </div>
""", """              {config.ticketFooter ? (() => {
                // 🧾 v193 ท้ายใบงาน: โปรโมทร้าน + ลูกค้าติดต่อกลับได้ (QR แอดไลน์ · ไอดีไลน์ · เบอร์โทร)
                const tf = config.ticketFooter;
                const lineQr = tf.lineUrl ? buildLinkQrDataUrl(tf.lineUrl, 5, 6) : null;
                const showPromo = !!(tf.linePromo && config.hasLinePromo && config.linePromoDiscount > 0 && !order.useLinePromo);
                return (
                  <div data-ticket-footer style={{ borderTop: '2px dashed #000', paddingTop: '8px', textAlign: 'center' }}>
                    {tf.slogan && <div style={{ fontSize: '25px', fontWeight: 900, lineHeight: 1.25 }}>{tf.slogan}</div>}
                    {(tf.perks || []).map((p, i) => <div key={'tfp' + i} style={{ fontSize: '18px', fontWeight: 600, lineHeight: 1.35 }}>{p}</div>)}
                    <div style={{ display: 'flex', alignItems: 'center', gap: '14px', border: '2px solid #000', borderRadius: '10px', padding: '10px 12px', margin: '8px 0 8px', textAlign: 'left' }}>
                      {lineQr && (
                        <div style={{ textAlign: 'center', flex: 'none' }}>
                          <img src={lineQr} alt="LINE" data-line-qr style={{ display: 'block', imageRendering: 'pixelated' }} />
                          <div style={{ fontSize: '16px', fontWeight: 800 }}>สแกนแอดไลน์</div>
                        </div>
                      )}
                      <div style={{ lineHeight: 1.3 }}>
                        <div style={{ fontSize: '21px', fontWeight: 900 }}>ผ้ามีปัญหา / สอบถาม</div>
                        <div style={{ fontSize: '18px', fontWeight: 600 }}>ติดต่อร้านได้เลย</div>
                        {tf.lineId && <div style={{ fontSize: '23px', fontWeight: 900, marginTop: '4px' }}>LINE {tf.lineId}</div>}
                        {tf.phone && <div style={{ fontSize: '23px', fontWeight: 900 }}>โทร {tf.phone}</div>}
                        {tf.hours && <div style={{ fontSize: '17px', fontWeight: 600 }}>{tf.hours}</div>}
                      </div>
                    </div>
                    {showPromo && <div data-line-promo style={{ display: 'inline-block', fontSize: '20px', fontWeight: 800, border: '2px solid #000', borderRadius: '999px', padding: '2px 14px', marginBottom: '6px' }}>แอดไลน์ครั้งแรก ลดค่าซัก {config.linePromoDiscount}฿</div>}
                    <div style={{ fontSize: '17px' }}>{config.subtitle} · ขอบคุณที่ใช้บริการ</div>
                  </div>
                );
              })() : (
                <div style={{ textAlign: 'center', fontSize: '18px', borderTop: '1px dashed #000', paddingTop: '6px' }}>
                  {config.subtitle}<br/>ขอบคุณที่ใช้บริการ
                </div>
              )}
""", 'ticket footer')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v193 applied')
