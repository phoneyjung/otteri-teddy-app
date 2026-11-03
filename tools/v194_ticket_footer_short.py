#!/usr/bin/env python3
"""v194 — ท้ายใบงาน: ตัดไอดีไลน์ออก · ข้อความสั้น ชัด เด่น ให้คนเห็นแล้วสแกน
ที่มา: เจ้าของ 3 พ.ย. 69 'ไม่มี id ดีกว่า แล้ว ขอข้อความสั้นๆ ชัดๆเด่นๆ คนอื่นเห็นจะได้สแกน ซัก อบ พับ.ฟรี'
ทำอะไร
  - แถบดำตัวขาวใหญ่ 'ซัก อบ พับ ฟรี!' + บรรทัดรอง 'รับฝาก จ่ายแค่ค่าเครื่อง · เปิด 24 ชม.' (Teddy 1 ไม่มี 24 ชม.)
  - กรอบ QR แอดไลน์ (ใหญ่ขึ้น) + 'สแกนแอดไลน์' ตัวใหญ่ + 'ผ้ามีปัญหา / สอบถาม' + เบอร์ร้าน
  - ตัดออก: ไอดีไลน์ · สโลแกน · บรรทัดส่งก่อน 20:00/เดลิเวอรี่ · เวลาแอดมิน
  - ป้ายโปรแอดไลน์ครั้งแรกเหมือน v193 (ซ่อนถ้าใบนั้นใช้โปรแล้ว)
usage: python3 tools/v194_ticket_footer_short.py index.html sw.js
"""
import sys
IDX, SW = sys.argv[1], sys.argv[2]
s = open(IDX, encoding='utf-8').read(); sw = open(SW, encoding='utf-8').read()


def rep(old, new, label, count=1):
    global s
    n = s.count(old); assert n == count, f'{label}: found {n}, expected {count}'; s = s.replace(old, new)


rep("window.APP_VERSION = 'v193-2026-11-03';", "window.APP_VERSION = 'v194-2026-11-03';", 'APP_VERSION')
assert sw.count("const CACHE_NAME = 'plp-laundry-v193';") == 1
sw = sw.replace("const CACHE_NAME = 'plp-laundry-v193';", "const CACHE_NAME = 'plp-laundry-v194';")

rep("""  ticketFooter: { slogan: 'ซักก็ไว ใส่ก็วิ๊ง! ที่เท็ดดี้', lineId: '@teddy.np', lineUrl: 'https://line.me/R/ti/p/@teddy.np', phone: '', hours: '', linePromo: false, perks: ['ฝากซัก อบ พับ ฟรี · จ่ายแค่ค่าเครื่อง', 'เดลิเวอรี่ 20–50฿'] },""",
    """  ticketFooter: { headline: 'ซัก อบ พับ ฟรี!', sub: 'รับฝาก จ่ายแค่ค่าเครื่อง', lineUrl: 'https://line.me/R/ti/p/@teddy.np', phone: '', linePromo: false }, // v194 สั้น ชัด เด่น (ไม่มีไอดีไลน์)""", 'teddy1 footer')
rep("""  ticketFooter: { slogan: 'ซักก็ไว ใส่ก็วิ๊ง! ที่เท็ดดี้', lineId: '@736vkujr', lineUrl: 'https://lin.ee/tLp9JME', phone: '083-145-6588', hours: 'แอดมินตอบ 09:00–21:00', linePromo: true, perks: ['เปิด 24 ชม. · ฝากซัก อบ พับ ฟรี จ่ายแค่ค่าเครื่อง', 'ส่งก่อน 20:00 ได้คืนวันเดียวกัน · เดลิเวอรี่ 20–50฿'] }, // leakcheck:allow เบอร์ร้าน (เจ้าของสั่งพิมพ์บนใบงาน 3 พ.ย.)""",
    """  ticketFooter: { headline: 'ซัก อบ พับ ฟรี!', sub: 'รับฝาก จ่ายแค่ค่าเครื่อง · เปิด 24 ชม.', lineUrl: 'https://lin.ee/tLp9JME', phone: '083-145-6588', linePromo: true }, // v194 สั้น ชัด เด่น (ไม่มีไอดีไลน์) · leakcheck:allow เบอร์ร้าน (เจ้าของสั่งพิมพ์บนใบงาน 3 พ.ย.)""", 'teddy2 footer')
rep("""              {config.ticketFooter ? (() => {
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
              )}""",
    """              {config.ticketFooter ? (() => {
                // 🧾 v193/v194 ท้ายใบงาน: ข้อความสั้น ชัด เด่น ให้คนเห็นแล้วสแกนแอดไลน์ + ติดต่อร้านได้ (ไม่มีไอดีไลน์)
                const tf = config.ticketFooter;
                const lineQr = tf.lineUrl ? buildLinkQrDataUrl(tf.lineUrl, 6, 6) : null;
                const showPromo = !!(tf.linePromo && config.hasLinePromo && config.linePromoDiscount > 0 && !order.useLinePromo);
                return (
                  <div data-ticket-footer style={{ borderTop: '2px dashed #000', paddingTop: '10px', textAlign: 'center' }}>
                    {tf.headline && <div data-ticket-headline style={{ background: '#000', color: '#fff', borderRadius: '12px', padding: '6px 10px 10px', fontSize: '52px', fontWeight: 900, lineHeight: 1.2 }}>{tf.headline}</div>}
                    {tf.sub && <div style={{ fontSize: '22px', fontWeight: 800, margin: '6px 0 2px' }}>{tf.sub}</div>}
                    <div style={{ display: 'flex', alignItems: 'center', gap: '16px', border: '3px solid #000', borderRadius: '12px', padding: '10px 14px', margin: '8px 0', textAlign: 'left' }}>
                      {lineQr && <img src={lineQr} alt="LINE" data-line-qr style={{ display: 'block', flex: 'none', imageRendering: 'pixelated' }} />}
                      <div style={{ lineHeight: 1.25 }}>
                        <div style={{ fontSize: '34px', fontWeight: 900 }}>สแกนแอดไลน์</div>
                        <div style={{ fontSize: '21px', fontWeight: 700, marginTop: '4px' }}>ผ้ามีปัญหา / สอบถาม</div>
                        {tf.phone && <div style={{ fontSize: '26px', fontWeight: 900 }}>โทร {tf.phone}</div>}
                      </div>
                    </div>
                    {showPromo && <div data-line-promo style={{ display: 'inline-block', fontSize: '21px', fontWeight: 800, border: '2px solid #000', borderRadius: '999px', padding: '2px 14px', marginBottom: '6px' }}>แอดไลน์ครั้งแรก ลดค่าซัก {config.linePromoDiscount}฿</div>}
                    <div style={{ fontSize: '17px' }}>{config.subtitle} · ขอบคุณที่ใช้บริการ</div>
                  </div>
                );
              })() : (
                <div style={{ textAlign: 'center', fontSize: '18px', borderTop: '1px dashed #000', paddingTop: '6px' }}>
                  {config.subtitle}<br/>ขอบคุณที่ใช้บริการ
                </div>
              )}""", 'ticket footer')

open(IDX, 'w', encoding='utf-8').write(s); open(SW, 'w', encoding='utf-8').write(sw)
print('v194 applied')
