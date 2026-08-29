// ============== D.D. Solution App (Browser Build) ==============
const { useState, useEffect, useMemo, useRef } = React;

// ============== LUCIDE SVG ICONS (inline) ==============
const Icon = ({ children, className = '', size = 16, strokeWidth = 2, ...props }) => 
  React.createElement('svg', {
    className, width: size, height: size, viewBox: '0 0 24 24',
    fill: 'none', stroke: 'currentColor', strokeWidth,
    strokeLinecap: 'round', strokeLinejoin: 'round', ...props
  }, children);

const _icons = {
  Sun: ['M12 2v2', 'M12 20v2', 'm4.93 4.93 1.41 1.41', 'm17.66 17.66 1.41 1.41', 'M2 12h2', 'M20 12h2', 'm6.34 17.66-1.41 1.41', 'm19.07 4.93-1.41 1.41'],
};
const Sun = (p) => Icon({...p, children: [
  React.createElement('circle', {key:'c', cx:12, cy:12, r:4}),
  ..._icons.Sun.map((d,i) => React.createElement('path', {key:i, d}))
]});
const Wallet = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M21 12V7H5a2 2 0 0 1 0-4h14v4'}),
  React.createElement('path', {key:'2', d:'M3 5v14a2 2 0 0 0 2 2h16v-5'}),
  React.createElement('path', {key:'3', d:'M18 12a2 2 0 0 0 0 4h4v-4Z'}),
]});
const Package = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M16.5 9.4 7.55 4.24'}),
  React.createElement('path', {key:'2', d:'M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z'}),
  React.createElement('polyline', {key:'3', points:'3.29 7 12 12 20.71 7'}),
  React.createElement('line', {key:'4', x1:12, x2:12, y1:22, y2:12}),
]});
const Users = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2'}),
  React.createElement('circle', {key:'2', cx:9, cy:7, r:4}),
  React.createElement('path', {key:'3', d:'M22 21v-2a4 4 0 0 0-3-3.87'}),
  React.createElement('path', {key:'4', d:'M16 3.13a4 4 0 0 1 0 7.75'}),
]});
const Briefcase = (p) => Icon({...p, children: [
  React.createElement('rect', {key:'1', width:20, height:14, x:2, y:7, rx:2, ry:2}),
  React.createElement('path', {key:'2', d:'M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16'}),
]});
const Plus = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M5 12h14'}),
  React.createElement('path', {key:'2', d:'M12 5v14'}),
]});
const Trash2 = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M3 6h18'}),
  React.createElement('path', {key:'2', d:'M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6'}),
  React.createElement('path', {key:'3', d:'M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2'}),
  React.createElement('line', {key:'4', x1:10, x2:10, y1:11, y2:17}),
  React.createElement('line', {key:'5', x1:14, x2:14, y1:11, y2:17}),
]});
const Edit2 = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z'}),
]});
const TrendingUp = (p) => Icon({...p, children: [
  React.createElement('polyline', {key:'1', points:'22 7 13.5 15.5 8.5 10.5 2 17'}),
  React.createElement('polyline', {key:'2', points:'16 7 22 7 22 13'}),
]});
const TrendingDown = (p) => Icon({...p, children: [
  React.createElement('polyline', {key:'1', points:'22 17 13.5 8.5 8.5 13.5 2 7'}),
  React.createElement('polyline', {key:'2', points:'16 17 22 17 22 11'}),
]});
const DollarSign = (p) => Icon({...p, children: [
  React.createElement('line', {key:'1', x1:12, x2:12, y1:2, y2:22}),
  React.createElement('path', {key:'2', d:'M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6'}),
]});
const AlertCircle = (p) => Icon({...p, children: [
  React.createElement('circle', {key:'1', cx:12, cy:12, r:10}),
  React.createElement('line', {key:'2', x1:12, x2:12, y1:8, y2:12}),
  React.createElement('line', {key:'3', x1:12, x2:12.01, y1:16, y2:16}),
]});
const X = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M18 6 6 18'}),
  React.createElement('path', {key:'2', d:'m6 6 12 12'}),
]});
const Save = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z'}),
  React.createElement('polyline', {key:'2', points:'17 21 17 13 7 13 7 21'}),
  React.createElement('polyline', {key:'3', points:'7 3 7 8 15 8'}),
]});
const PieChart = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M21.21 15.89A10 10 0 1 1 8 2.83'}),
  React.createElement('path', {key:'2', d:'M22 12A10 10 0 0 0 12 2v10z'}),
]});
const BarChart3 = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M3 3v18h18'}),
  React.createElement('path', {key:'2', d:'M18 17V9'}),
  React.createElement('path', {key:'3', d:'M13 17V5'}),
  React.createElement('path', {key:'4', d:'M8 17v-3'}),
]});
const Eye = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z'}),
  React.createElement('circle', {key:'2', cx:12, cy:12, r:3}),
]});
const EyeOff = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M9.88 9.88a3 3 0 1 0 4.24 4.24'}),
  React.createElement('line', {key:'4', x1:2, x2:22, y1:2, y2:22}),
]});
const Truck = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M5 18H3c-.6 0-1-.4-1-1V7c0-.6.4-1 1-1h10c.6 0 1 .4 1 1v11'}),
  React.createElement('path', {key:'2', d:'M14 9h4l4 4v4c0 .6-.4 1-1 1h-2'}),
  React.createElement('circle', {key:'3', cx:7, cy:18, r:2}),
  React.createElement('path', {key:'4', d:'M15 18H9'}),
  React.createElement('circle', {key:'5', cx:17, cy:18, r:2}),
]});
const Wrench = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z'}),
]});
const Coffee = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M17 8h1a4 4 0 1 1 0 8h-1'}),
  React.createElement('path', {key:'2', d:'M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4Z'}),
]});
const Box = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z'}),
  React.createElement('polyline', {key:'2', points:'3.27 6.96 12 12.01 20.73 6.96'}),
  React.createElement('line', {key:'3', x1:12, x2:12, y1:22.08, y2:12}),
]});
const History = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8'}),
  React.createElement('path', {key:'2', d:'M3 3v5h5'}),
  React.createElement('path', {key:'3', d:'M12 7v5l4 2'}),
]});
const ArrowUpRight = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M7 7h10v10'}),
  React.createElement('path', {key:'2', d:'M7 17 17 7'}),
]});
const ArrowDownLeft = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M17 17H7V7'}),
  React.createElement('path', {key:'2', d:'M17 7 7 17'}),
]});
const Lock = (p) => Icon({...p, children: [
  React.createElement('rect', {key:'1', width:18, height:11, x:3, y:11, rx:2, ry:2}),
  React.createElement('path', {key:'2', d:'M7 11V7a5 5 0 0 1 10 0v4'}),
]});
const LogOut = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4'}),
  React.createElement('polyline', {key:'2', points:'16 17 21 12 16 7'}),
  React.createElement('line', {key:'3', x1:21, x2:9, y1:12, y2:12}),
]});
const Phone = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z'}),
]});
const MapPin = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M20 10c0 7-8 13-8 13s-8-6-8-13a8 8 0 0 1 16 0Z'}),
  React.createElement('circle', {key:'2', cx:12, cy:10, r:3}),
]});
const Download = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4'}),
  React.createElement('polyline', {key:'2', points:'7 10 12 15 17 10'}),
  React.createElement('line', {key:'3', x1:12, x2:12, y1:15, y2:3}),
]});
const Camera = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3Z'}),
  React.createElement('circle', {key:'2', cx:12, cy:13.5, r:3.5}),
]});
const Activity = (p) => Icon({...p, children: [
  React.createElement('polyline', {key:'1', points:'22 12 18 12 15 21 9 3 6 12 2 12'}),
]});
const UserCircle = (p) => Icon({...p, children: [
  React.createElement('path', {key:'1', d:'M18 20a6 6 0 0 0-12 0'}),
  React.createElement('circle', {key:'2', cx:12, cy:10, r:4}),
  React.createElement('circle', {key:'3', cx:12, cy:12, r:10}),
]});


// ============== AUTH CONFIG ==============
const USERS = {
  '0000': { id: 'p-pa', name: 'พ่อ', icon: '🔧' },
  '8888': { id: 'p-phone', name: 'โฟน', icon: '💼' },
  '1234': { id: 'p-aam', name: 'อาม', icon: '📱' },
};

const STOCK_CATEGORIES = [
  { id: 'panel', label: 'แผงโซล่า' },
  { id: 'inverter', label: 'อินเวอร์เตอร์' },
  { id: 'battery', label: 'แบตเตอรี่' },
  { id: 'wire', label: 'สายไฟ', byMeter: true },
  { id: 'panel_box', label: 'ตู้คอนโทรล' },
];

// ============== JOB WORKFLOW (11 ขั้นตอนงาน) ==============
const JOB_WORKFLOW_STEPS = [
  { id: 1, icon: '💬', label: 'ตกลงขาย', hint: 'คุยปิดดีล · เก็บข้อมูลบ้าน รูปหลังคา ทิศ บิลไฟ' },
  { id: 2, icon: '📋', label: 'ใบเสนอราคา', optional: true, hint: 'ออกที่ Tab เสนอขาย (ลูกค้าเชื่อใจสั่งเลย = ข้ามได้)' },
  { id: 3, icon: '💰', label: 'รับมัดจำ', optional: true, hint: 'เลือกได้ ไม่บังคับ — ลูกค้าเชื่อใจจ่ายทีเดียวก็ข้ามได้ · ถ้ารับ: แนะนำ 30-50% ก่อนสั่งของหลัก กันจมทุน · ออกใบเสร็จมัดจำให้ลูกค้าได้ที่งานเอกสาร' },
  { id: 4, icon: '🛒', label: 'สั่งของหลัก', hint: 'Inverter / แบต / แผง ตามออเดอร์ · บันทึกที่ Tab สต็อก "+ เพิ่มสินค้า" (รายจ่ายอัตโนมัติ)' },
  { id: 5, icon: '📐', label: 'สำรวจหน้างาน', hint: 'วัดหลังคา จุดติด Inverter ระยะเดินสาย ตู้ไฟ มิเตอร์ · ☑ ทำ Checklist ของในขั้นถัดไป · ⚡ ยื่นขนานไฟ PEA/MEA ถ้าต้อง' },
  { id: 6, icon: '📦', label: 'เตรียมของ', hint: 'ติ๊ก Checklist ด้านล่าง · ของขาดซื้อเพิ่มที่ Tab สต็อก หรือใส่ต้นทุนงานตรงนี้' },
  { id: 7, icon: '🔧', label: 'ติดตั้ง', hint: 'ถ่ายรูป Before/After เก็บไว้ (การตลาด + อ้างอิงประกัน) · บันทึกค่าแรง/ของซื้อหน้างานในต้นทุน' },
  { id: 8, icon: '✅', label: 'ทดสอบ + ตั้งระบบ', hint: 'Megger test · ตั้ง Zero-export / CT clamp ให้ถูกทิศ · เชื่อม WiFi logger · สอนลูกค้าใช้แอป Deye Cloud' },
  { id: 9, icon: '🧾', label: 'เก็บเงิน + เอกสาร', hint: 'ใบแจ้งหนี้ (ถ้าลูกค้าต้องการ) → ใบเสร็จเต็ม + ใบรับประกัน + นามบัตร (กระดาษ+อีเมล) ที่งานเอกสาร' },
  { id: 10, icon: '🔒', label: 'ปิดงาน', hint: 'กด "✅ จบงาน" ที่งานเอกสาร — ระบบสรุปกำไร เก็บเงินที่ขาด ของเหลือเข้าสต๊อก แล้วล็อกงาน' },
  { id: 11, icon: '📞', label: 'ติดตามผล', optional: true, hint: 'นัด 1 เดือน เช็คผลผลิตจากแอป · ขอรีวิว/แนะนำต่อ — ลูกค้าประทับใจ งานใหม่ตามมา' },
];

// Checklist ของติดตั้งมาตรฐาน (งาน solar 1 หลัง)
const DEFAULT_INSTALL_CHECKLIST = [
  { group: 'ของหลัก', items: ['แผงโซล่า (ครบจำนวน)', 'Inverter', 'แบตเตอรี่ (ถ้ามี)'] },
  { group: 'โครงยึด', items: ['Rail อลูมิเนียม', 'Rail splice (ข้อต่อราง)', 'Mid clamp', 'End clamp', 'Roof hook / L-feet', 'สกรู+พุก'] },
  { group: 'ไฟฟ้า DC', items: ['สาย PV (DC) ดำ+แดง', 'หัว MC4', 'ท่อร้อยสาย + แคลมป์จับท่อ'] },
  { group: 'ไฟฟ้า AC + กราวด์', items: ['สาย AC', 'เบรคเกอร์', 'ตู้ Combiner + SPD', 'แท่งกราวด์ + สายกราวด์ + Grounding lug', 'แผ่นกราวด์แผง'] },
  { group: 'Monitoring', items: ['WiFi/4G Logger', 'CT Clamp (เช็คทิศลูกศร!)'] },
  { group: 'อื่นๆ', items: ['ซิลิโคนกันรั่ว', 'Cable tie / Cable clip', 'เครื่องมือ + บันได + อุปกรณ์เซฟตี้'] },
];

// ============== IMGBB CONFIG ==============
const IMGBB_API_KEY = 'a1fd3c5abb27a3efc0683a282c97860a';
const MAX_PHOTOS_PER_CUSTOMER = 10;
const MAX_PHOTO_LONG_EDGE = 1440;
const PHOTO_QUALITY = 0.9;

// Compress รูปก่อนอัพโหลด
async function compressImage(file, maxLongEdge = MAX_PHOTO_LONG_EDGE, quality = PHOTO_QUALITY) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => {
        // คำนวณขนาดใหม่
        let { width, height } = img;
        if (width > height) {
          if (width > maxLongEdge) {
            height = Math.round((height * maxLongEdge) / width);
            width = maxLongEdge;
          }
        } else {
          if (height > maxLongEdge) {
            width = Math.round((width * maxLongEdge) / height);
            height = maxLongEdge;
          }
        }

        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, width, height);

        canvas.toBlob(
          (blob) => {
            if (blob) resolve(blob);
            else reject(new Error('Failed to compress image'));
          },
          'image/jpeg',
          quality
        );
      };
      img.onerror = () => reject(new Error('Failed to load image'));
      img.src = e.target.result;
    };
    reader.onerror = () => reject(new Error('Failed to read file'));
    reader.readAsDataURL(file);
  });
}

// อัพโหลดรูปไป ImgBB
async function uploadToImgBB(blob) {
  const formData = new FormData();
  formData.append('image', blob);

  const response = await fetch(`https://api.imgbb.com/1/upload?key=${IMGBB_API_KEY}`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Upload failed: ${response.status}`);
  }

  const data = await response.json();
  if (!data.success) {
    throw new Error(data.error?.message || 'Upload failed');
  }

  return {
    url: data.data.url,                    // รูปเต็มขนาด
    thumb: data.data.thumb?.url || data.data.url,  // thumbnail
    medium: data.data.medium?.url || data.data.url, // medium size
    deleteUrl: data.data.delete_url,       // ลิงก์สำหรับลบ
    id: data.data.id,
  };
}

const COST_CATEGORIES = [
  { id: 'panel', label: 'แผงโซล่า', icon: Sun },
  { id: 'inverter', label: 'อินเวอร์เตอร์', icon: Box },
  { id: 'battery', label: 'แบตเตอรี่', icon: Box },
  { id: 'wire', label: 'สายไฟ', icon: Box },
  { id: 'panel_box', label: 'ตู้คอนโทรล', icon: Box },
  { id: 'equipment', label: 'อุปกรณ์', icon: Wrench },
  { id: 'material', label: 'วัสดุอื่นๆ', icon: Package },
  { id: 'labor', label: 'ค่าแรง', icon: Users },
  { id: 'travel', label: 'ค่าเดินทาง', icon: Truck },
  { id: 'food', label: 'ค่าน้ำค่าข้าว', icon: Coffee },
  { id: 'commission', label: 'ค่าคอม (แนะนำ)', icon: Users },
  { id: 'other', label: 'อื่นๆ', icon: Box },
];

const getCatLabel = (id) => COST_CATEGORIES.find(c => c.id === id)?.label || id;

const DEFAULT_PARTNERS = [
  { id: 'p-aam', name: 'อาม', fullName: 'ศิรินทร์ ริวัฒนา', role: 'Sales / Marketing / ประสานงาน', bankAccount: '8682177528 กสิกร', totalReturn: 0, note: '' },
  { id: 'p-phone', name: 'โฟน', fullName: 'Phoneyjung', role: 'Operations / Finance / ระบบ', bankAccount: '', totalReturn: 0, note: '' },
  { id: 'p-pa', name: 'พ่อ', fullName: 'aku', role: 'Technical / ช่าง / Sourcing', bankAccount: '3164190533', totalReturn: 0, note: '' },
];

const DEFAULT_STOCK = [
  // ✅ มีของเหลือในสต๊อกจริง (qty > 0)
  { id: 'stk-longi', name: 'แผง Longi 640W', category: 'panel', qty: 27, unitCost: 2911, supplier: '-', owner: 'บริษัท', note: 'ซื้อจากเงินงานแรก+ทุน · ซื้อมา 36 ใช้ในงาน 2 ไป 9', purchaseDate: '2026-04-08', unit: 'แผ่น',
    inSalesCatalog: true, salesSpecs: { brand: 'Longi', model: '640W', watt: 640, tier: 'standard' } },
  { id: 'stk-inv10', name: 'Inverter Hybrid 10kW', category: 'inverter', qty: 1, unitCost: 59000, supplier: '-', owner: 'โฟน', note: 'โฟนซื้อตุนไว้', purchaseDate: '2026-04-26', unit: 'เครื่อง',
    inSalesCatalog: true, salesSpecs: { brand: 'Hybrid', model: '10kW', size: 10, type: 'hybrid', tier: 'premium' } },
  // 📋 ประวัติ — ของที่เคยซื้อแล้วใช้หมด (qty = 0)
  { id: 'stk-hist-1', name: 'แผง Jinko 725W N-Type', category: 'panel', qty: 0, unitCost: 3585, supplier: 'aku connection', owner: 'อาม', note: 'ใช้ในงาน 1 (8 แผ่น)', purchaseDate: '2026-04-08', unit: 'แผ่น',
    inSalesCatalog: true, salesSpecs: { brand: 'Jinko', model: '725W', watt: 725, tier: 'premium' } },
  { id: 'stk-hist-2', name: 'Inverter Hybrid 5kW (งาน 1)', category: 'inverter', qty: 0, unitCost: 33500, supplier: '-', owner: 'โฟน', note: 'ใช้ในงาน 1', purchaseDate: '2026-04-08', unit: 'เครื่อง',
    inSalesCatalog: true, salesSpecs: { brand: 'Deye', model: 'Hybrid 5kW', size: 5, type: 'hybrid', tier: 'standard' } },
  { id: 'stk-hist-3', name: 'Inverter Deye 5kW Hybrid', category: 'inverter', qty: 0, unitCost: 33705, supplier: '-', owner: 'อาม', note: 'รวม VAT 7% · ใช้ในงาน 2', purchaseDate: '2026-04-16', unit: 'เครื่อง' },
  { id: 'stk-hist-4', name: 'แบต Deye 51.2V 314Ah 16kWh', category: 'battery', qty: 0, unitCost: 67303, supplier: '-', owner: 'อาม', note: 'รวม VAT · ใช้ในงาน 2', purchaseDate: '2026-04-18', unit: 'ลูก',
    inSalesCatalog: true, salesSpecs: { brand: 'Deye', model: '16kWh', capacity: 16, tier: 'standard' } },
  { id: 'stk-hist-5', name: 'สาย PV 6mm KUKA แดง', category: 'wire', qty: 0, unitCost: 37.236, supplier: 'aku', owner: 'อาม', note: 'ม้วน 100ม. 3,723.60 ฿ (รวม VAT) · ใช้ในงาน 1', purchaseDate: '2026-04-08', unit: 'เมตร', perRoll: 100, rollPrice: 3723.6 },
  { id: 'stk-hist-6', name: 'สาย PV 6mm KUKA ดำ', category: 'wire', qty: 0, unitCost: 37.236, supplier: 'aku', owner: 'อาม', note: 'ม้วน 100ม. 3,723.60 ฿ (รวม VAT) · ใช้ในงาน 1', purchaseDate: '2026-04-08', unit: 'เมตร', perRoll: 100, rollPrice: 3723.6 },
  { id: 'stk-hist-7', name: 'สาย Yazaki 10mm เมน', category: 'wire', qty: 0, unitCost: 48.50, supplier: '-', owner: 'พ่อ', note: 'ม้วน 100ม. 4,850 ฿ · ใช้ในงาน 1', purchaseDate: '2026-04-04', unit: 'เมตร', perRoll: 100, rollPrice: 4850 },
  { id: 'stk-hist-8', name: 'ตู้ Combiner งาน 1', category: 'panel_box', qty: 0, unitCost: 2500, supplier: '-', owner: 'พ่อ', note: 'ใช้ในงาน 1', purchaseDate: '2026-04-08', unit: 'ตู้' },
  { id: 'stk-hist-9', name: 'ตู้ Combiner 2 String งาน 2', category: 'panel_box', qty: 0, unitCost: 3462, supplier: '-', owner: 'อาม', note: 'ใช้ในงาน 2', purchaseDate: '2026-04-26', unit: 'ตู้' },
];

const DEFAULT_JOBS = [
  {
    id: 'job-1', date: '2026-04-08', customer: 'พี่เกรียงศักดิ์ วงวาลย์',
    location: 'ดอนไก่ดี กระทุ่มแบน สมุทรสาคร', type: '5kW Hybrid + Jinko 725W × 8',
    salePrice: 108000, originalPrice: 110000, discount: 2000,
    discountNote: 'ส่วนลด: ค่าแนะนำของอาม',
    status: 'completed',
    investments: { 'p-aam': 55447.20, 'p-phone': 33500, 'p-pa': 8870 },
    costsByCategory: {
      panel: [
        { item: 'แผง Jinko N-Type 725W × 8 แผ่น (รวม VAT)', amount: 28676 },
        { item: 'DC Solar cable KUKA 6sqmm 100M × 2 (รวม VAT)', amount: 7447.20 },
      ],
      inverter: [{ item: 'Inverter Hybrid 5kW (โฟน)', amount: 33500 }],
      panel_box: [{ item: 'Combiner', amount: 2500 }],
      equipment: [
        { item: 'Rail 4.2 × 8', amount: 3400 },
        { item: 'Rail splice × 8', amount: 304 },
        { item: 'Mid clamp × 26', amount: 520 },
        { item: 'End clamp 35/10mm × 10', amount: 200 },
        { item: 'แผ่นกราวด์ × 30', amount: 150 },
        { item: 'Grounding Lug × 10', amount: 270 },
        { item: 'C-Pack Roof Hook × 26', amount: 3120 },
        { item: 'Cable clip × 30', amount: 150 },
        { item: 'Link × 10', amount: 350 },
        { item: 'โฮซอ', amount: 320 },
        { item: 'เบรคเกอร์', amount: 120 },
        { item: 'สายกาว', amount: 900 },
        { item: 'แปรงทาสี', amount: 20 },
        { item: 'ค่าของติดตั้งเพิ่มเติม', amount: 3500 },
        { item: 'ข้อต่อท่อร้อยสาย ก้ามปู', amount: 220 },
      ],
      wire: [{ item: 'สายไฟ เบอร์ 10 (1 ม้วน)', amount: 4850 }],
      labor: [
        { item: 'ค่าช่างสิทธิ์', amount: 6000 },
        { item: 'ค่าแรงช่างเอ๋', amount: 800 },
        { item: 'ค่าแรงช่างหนึ่ง', amount: 500 },
      ],
    },
    totalCost: 97817.20, profit: 10182.80,
    note: 'งานแรก! ผลิตไฟ 28kW/วัน · อาม 55,447.20 + โฟน 33,500 + พ่อ 8,870',
  },
  {
    id: 'job-2', date: '2026-05-02', customer: 'งานที่ 2',
    location: 'หลักสี่ กรุงเทพฯ', type: '5kW Hybrid Deye + แบต 16kW + Longi 640W × 9',
    salePrice: 190000, originalPrice: 190000, discount: 0, discountNote: '',
    status: 'completed',
    investments: { 'p-aam': 127460, 'p-pa': 3200 },
    costsByCategory: {
      panel: [{ item: 'Longi 640W × 9 (จากสต๊อก)', amount: 26199, stockId: 'stk-longi', qtyUsed: 9 }],
      inverter: [{ item: 'Inverter Deye 5kW Hybrid (รวม VAT 7%)', amount: 33705 }],
      battery: [{ item: 'Deye แบต 51.2V 314Ah 16kWh (รวม VAT 7%)', amount: 67303 }],
      panel_box: [{ item: 'Combiner', amount: 3462 }],
      equipment: [{ item: 'วัสดุติดตั้ง (ซื้อเพิ่มหน้างาน)', amount: 1372 }],
      labor: [
        { item: 'ค่าแรง+ของ ติดแผง (เหมา)', amount: 20000 },
        { item: 'ค่าช่างเอ๋,ช่างหนึ่ง', amount: 1700 },
      ],
      travel: [
        { item: 'ค่าส่งแบต (ค่ารถ)', amount: 700 },
        { item: 'ค่าน้ำมัน', amount: 1000 },
      ],
      other: [
        { item: 'ค่าข้าวช่าง', amount: 918 },
        { item: 'ค่าข้าว', amount: 500 },
      ],
    },
    totalCost: 156859, profit: 33141,
    note: 'อาม 127,460 + พ่อ 3,200 + แผง Longi 9 แผ่นจากสต๊อก (26,199)',
  },
];

const DEFAULT_TRANSACTIONS = [
  // ========================================
  // งานที่ 1 - พี่เกรียงศักดิ์
  // ========================================
  // รายได้จากลูกค้า
  { id: 't-1', date: '2026-04-08', type: 'income', category: 'รายได้จากงาน', amount: 108000, description: 'งานพี่เกรียงศักดิ์ - 5kW Hybrid', jobId: 'job-1', partnerId: '' },
  
  // ทุนหุ้นส่วน (income) - หุ้นส่วนใส่เงินส่วนตัวซื้อของให้บริษัท
  { id: 't-c1a', date: '2026-04-08', type: 'income', category: 'เพิ่มทุน', amount: 55447.20, description: 'อาม ลงทุน งาน 1', jobId: 'job-1', partnerId: 'p-aam' },
  { id: 't-c1b', date: '2026-04-08', type: 'income', category: 'เพิ่มทุน', amount: 33500, description: 'โฟน ลงทุน งาน 1 (Inverter 5kW)', jobId: 'job-1', partnerId: 'p-phone' },
  { id: 't-c1c', date: '2026-04-08', type: 'income', category: 'เพิ่มทุน', amount: 8870, description: 'พ่อ ลงทุน งาน 1 (สาย+ตู้+ค่าแรง)', jobId: 'job-1', partnerId: 'p-pa' },
  
  // ต้นทุนงาน (expense) - บริษัทจ่ายค่าของ
  { id: 't-2', date: '2026-04-08', type: 'expense', category: 'ต้นทุนงาน', amount: 55447.20, description: 'ค่าของ+ค่าแรง งาน 1 (อาม)', jobId: 'job-1', partnerId: 'p-aam' },
  { id: 't-3', date: '2026-04-08', type: 'expense', category: 'ต้นทุนงาน', amount: 33500, description: 'ค่าของ งาน 1 (Inverter โฟน)', jobId: 'job-1', partnerId: 'p-phone' },
  { id: 't-4', date: '2026-04-08', type: 'expense', category: 'ต้นทุนงาน', amount: 8870, description: 'ค่าของ+ค่าแรง งาน 1 (พ่อ)', jobId: 'job-1', partnerId: 'p-pa' },
  
  // ========================================
  // สต๊อก - ซื้อของตุน
  // ========================================
  // ซื้อ Longi 36 แผ่น - บริษัทจ่าย (เงินจากกำไรงาน 1 + ทุน)
  { id: 't-5', date: '2026-04-08', type: 'expense', category: 'ต้นทุนสต๊อก', amount: 104796, description: 'ซื้อแผง Longi 640W × 36 แผ่น (เงินจากกำไรงาน 1+ทุน)', jobId: '', partnerId: '' },
  
  // โฟนซื้อ Inverter Hybrid 10kW ตุนไว้ - เพิ่มทุน + ซื้อของ
  { id: 't-c2a', date: '2026-04-26', type: 'income', category: 'เพิ่มทุน', amount: 59000, description: 'โฟน ลงทุน (ซื้อ Inverter Hybrid 10kW ตุน)', jobId: '', partnerId: 'p-phone' },
  { id: 't-6', date: '2026-04-26', type: 'expense', category: 'ต้นทุนสต๊อก', amount: 59000, description: 'ซื้อ Inverter Hybrid 10kW ตุน (โฟน)', jobId: '', partnerId: 'p-phone' },
  
  // ========================================
  // งานที่ 2 - หลักสี่
  // ========================================
  // รายได้จากลูกค้า
  { id: 't-7', date: '2026-05-02', type: 'income', category: 'รายได้จากงาน', amount: 190000, description: 'งานที่ 2 - 5kW Hybrid + แบต 16kW', jobId: 'job-2', partnerId: '' },
  
  // ทุนหุ้นส่วน (income)
  { id: 't-c3a', date: '2026-05-02', type: 'income', category: 'เพิ่มทุน', amount: 127460, description: 'อาม ลงทุน งาน 2 (Inverter Deye+แบต+อื่นๆ)', jobId: 'job-2', partnerId: 'p-aam' },
  { id: 't-c3b', date: '2026-05-02', type: 'income', category: 'เพิ่มทุน', amount: 3200, description: 'พ่อ ลงทุน งาน 2 (ค่าช่าง+น้ำมัน+ข้าว)', jobId: 'job-2', partnerId: 'p-pa' },
  
  // ต้นทุนงาน (expense)
  { id: 't-8', date: '2026-05-02', type: 'expense', category: 'ต้นทุนงาน', amount: 127460, description: 'ค่าของ งาน 2 (Inverter Deye+แบต+อื่นๆ)', jobId: 'job-2', partnerId: 'p-aam' },
  { id: 't-9', date: '2026-05-02', type: 'expense', category: 'ต้นทุนงาน', amount: 3200, description: 'ค่าช่าง+น้ำมัน+ข้าว งาน 2 (พ่อ)', jobId: 'job-2', partnerId: 'p-pa' },
  
  // Longi 9 แผ่นจากสต๊อก - ใช้ของในสต๊อก ไม่ใช่ Cash transaction
  // (ไม่นับ "เบิกสต๊อก" เป็น expense - ของซื้อจ่ายไปแล้วตอนเข้าสต๊อก)
];

const DEFAULT_CUSTOMERS = [
  {
    id: 'cust-1', name: 'พี่เกรียงศักดิ์ วงวาลย์', phone: '',
    address: '21 ตำบล ดอนไก่ดี อำเภอกระทุ่มแบน สมุทรสาคร 74110',
    mapLink: 'https://maps.google.com/maps?f=q&q=13.642025,100.255410&spn=0.029488,0.083942&z=14',
    installDate: '2026-04-08', system: '5kW Hybrid + Jinko 725W × 8',
    warranty: 'แผง 30 ปี · Inverter 10 ปี · ติดตั้ง 5 ปี',
    jobId: 'job-1', note: 'งานแรก! ผลิตไฟ 28kW/วัน',
  },
  {
    id: 'cust-2', name: 'งานที่ 2 (หลักสี่)', phone: '',
    address: '67/593 ซอย เกษตร แขวงทุ่งสองห้อง เขตหลักสี่ กรุงเทพมหานคร 10210',
    mapLink: 'https://maps.google.com/maps?f=q&q=13.907270,100.568337&spn=0.029488,0.083942&z=14',
    installDate: '2026-05-02', system: '5kW Hybrid Deye + แบต 16kW + Longi 640W × 9',
    warranty: 'แผง 30 ปี · Inverter 10 ปี · แบต 10 ปี · ติดตั้ง 5 ปี',
    jobId: 'job-2', note: '',
  },
];

// ============== COMPANY INFO (สำหรับใบเสนอราคา/บิล) ==============
const DEFAULT_COMPANY_INFO = {
  name: 'D.D. Solution',
  subName: 'Daddy Solution',
  tagline: 'ติดตั้งโซล่าเซลล์ครบวงจร',
  address: '',
  phone: '',
  lineId: '',
  email: '',
  taxId: '',
  bankAccounts: [
    { bank: 'ธ.กสิกรไทย', number: '868-2-17752-8', name: 'ศิรินทร์ ริวัฒนา' },
  ],
  // === รับประกัน (แสดงในใบเสนอราคา) ===
  warranty: [
    { id: 'w-inv',     icon: '🔌', label: 'Inverter',                years: 10, note: '' },
    { id: 'w-batt',    icon: '🔋', label: 'แบตเตอรี่',                 years: 10, note: '' },
    { id: 'w-panel-p', icon: '☀️', label: 'แผง (Power Output)',       years: 30, note: '' },
    { id: 'w-panel-m', icon: '☀️', label: 'แผง (Product/Material)',   years: 15, note: '' },
    { id: 'w-install', icon: '🔧', label: 'งานติดตั้ง',                  years: 10, note: '' },
    { id: 'w-support', icon: '📞', label: 'After-sale Support',         years: 99, note: 'ตลอดอายุระบบ' },
  ],
  // === สเปคที่ใช้ (ใส่ใจรายละเอียด) ===
  specs: [
    { id: 's-dc',     label: 'สาย PV (DC)',         value: 'PV1-F 6mm² ดำ+แดง ทนแดด UV' },
    { id: 's-ac',     label: 'สาย AC + Ground',     value: 'Yasaki THW 10mm² (≤5kW) / 16mm² (>5kW) + เขียวเหลือง' },
    { id: 's-comb',   label: 'ตู้ Combiner',        value: 'พร้อม Surge Protection' },
    { id: 's-rail',   label: 'รางอลูมิเนียม',       value: 'หนา 1.6mm + Stainless' },
    { id: 's-test',   label: 'ทดสอบหลังติดตั้ง',   value: 'Megger Test + ขนานไฟ' },
    { id: 's-cert',   label: 'มาตรฐาน',             value: 'ตามวิศวกรไฟฟ้า + กกพ.' },
  ],
  // === ของแถม / Value-add ===
  freebies: [
    { id: 'f-net',     icon: '🪺', label: 'ตาข่ายกันนก',                  active: true },
    { id: 'f-clean',   icon: '🧹', label: 'ทำความสะอาดแผงปีแรก ฟรี!',  active: true },
    { id: 'f-check',   icon: '🔍', label: 'ตรวจระบบฟรี 1 ปี',           active: true },
    { id: 'f-monitor', icon: '📱', label: 'แอป Monitor ตลอดอายุ',        active: true },
    { id: 'f-manual',  icon: '📖', label: 'คู่มือการใช้งาน',              active: true },
  ],
  // === Slogan สำหรับใบเสนอราคา ===
  saleSlogan: 'คืนทุนเร็ว สำรองไฟ คุ้มค่าระยะยาว',
  // === DEPRECATED (เก็บไว้กันพัง) ===
  defaultWarranty: [
    'แผงโซล่าเซลล์: 25 ปี',
    'Inverter: 10 ปี',
    'แบตเตอรี่: 10 ปี',
    'งานติดตั้ง: 5 ปี',
  ],
  defaultPaymentTerms: 'มัดจำ 50% ตอนยืนยันสั่งซื้อ\nชำระส่วนที่เหลือหลังติดตั้งเสร็จ',
  // === Sales Settings ===
  margins: {
    small: 25,   // < 5kW
    medium: 20,  // 5-10kW
    large: 15,   // > 10kW
  },
  // ต้นทุนแฝงต่องานติดตั้ง (จะคิดเข้าไปทุกงาน — เซลส์ปรับได้)
  // ค่าเริ่มต้น: ประมาณการจากข้อมูลงาน 1, 2 (ระบบ ~5kW)
  hiddenCosts: [
    { id: 'hc-mounting',  label: 'วัสดุติดตั้ง (Rail/Clamp/Hook/etc.)', amount: 13500, perJob: true },
    { id: 'hc-wire-pv',    label: 'สาย PV (PV1-F 6mm² ดำ+แดง) ~30m',   amount: 1650,  perJob: true },
    { id: 'hc-wire-ac-5k', label: 'สาย AC 10mm² (ระบบ ≤5kW) ~45m',     amount: 4275,  perJob: true, applyIfInvSize: '<=5' },
    { id: 'hc-wire-ac-10k',label: 'สาย AC 16mm² (ระบบ >5kW) ~45m',     amount: 6300,  perJob: true, applyIfInvSize: '>5' },
    { id: 'hc-combiner',  label: 'ตู้ Combiner + เบรคเกอร์',            amount: 3000,  perJob: true },
    { id: 'hc-labor',     label: 'ค่าแรงช่าง',                           amount: 8000,  perJob: true },
    { id: 'hc-travel',    label: 'ค่าเดินทาง + ค่าน้ำมัน',              amount: 1500,  perJob: true },
    { id: 'hc-meal',      label: 'ค่าข้าวช่าง',                          amount: 1500,  perJob: true },
    { id: 'hc-misc',      label: 'เบ็ดเตล็ด/ของเพิ่มเติมหน้างาน',      amount: 2500,  perJob: true },
  ],
  installCostPct: 0,  // (deprecated - เปลี่ยนมาใช้ hiddenCosts แทน)
};

const DEFAULT_DOCUMENTS = [];  // เอกสารเริ่มต้น (เสนอราคา/แจ้งหนี้/ใบเสร็จ)

// ============== SALES PRESENTATION CONSTANTS ==============
// Solar irradiance ของไทย — อิงจากงานวิจัย
// ที่มา: World Bank/SolarGIS, งานวิจัยมหาวิทยาลัยและกรมพลังงาน
// PSH ทฤษฎี = ค่าแสงเต็มทางทฤษฎี (Standard Test Condition)
// PR (Performance Ratio) = ประสิทธิภาพระบบจริง (วิจัยพบ 0.71-0.85 ในไทย)
// realPSH = PSH × PR = ผลผลิตจริงเฉลี่ย
const SOLAR_REGIONS = {
  north:   { 
    label: '🏔️ ภาคเหนือ',     
    theoreticalPSH: 4.8,    // ทฤษฎี (kWh/m²/day)
    pr: 0.73,                // Performance Ratio (งานวิจัยไทย)
    hours: 3.50,             // ผลิตจริง (= theoretical × PR)
    provinces: 'เชียงใหม่ เชียงราย ลำปาง น่าน...',
  },
  central: { 
    label: '🏛️ ภาคกลาง/อีสาน', 
    theoreticalPSH: 5.06,   // SolarGIS ค่าเฉลี่ยไทย
    pr: 0.73,
    hours: 3.70,
    provinces: 'กรุงเทพ นนทบุรี ขอนแก่น...',
  },
  east:    { 
    label: '🌅 ภาคตะวันออก',  
    theoreticalPSH: 5.0,
    pr: 0.73,
    hours: 3.65,
    provinces: 'ชลบุรี ระยอง จันทบุรี ตราด...',
  },
  south:   { 
    label: '🌴 ภาคใต้',        
    theoreticalPSH: 4.8,    // ภาคใต้ฝนเยอะ PSH ทฤษฎีน้อยกว่า
    pr: 0.73,
    hours: 3.50,
    provinces: 'ภูเก็ต กระบี่ สงขลา...',
  },
};

// Degradation rate ของแผง (NREL: median 0.5%/ปี)
// เขตร้อน + Rooftop จะสูงกว่าค่ากลาง — ใช้ 0.6% เพื่อความ realistic
const PANEL_DEGRADATION_RATE = 0.006; // 0.6%/ปี (อิง NREL + tropical adjustment)

// ============== ปัจจัยที่ส่งผลต่อการผลิตไฟ (โหมดคำนวณตามจริง) ==============

// ทิศการติดตั้งแผง (8 ทิศ) + factor ที่ส่งผลต่อการผลิตในประเทศไทย
// อิง: ประเทศไทยอยู่ในซีกโลกเหนือ → หันใต้ดีที่สุด
// ค่าตัวคูณเทียบกับการหันใต้ที่มุม optimal
const PANEL_DIRECTIONS = {
  S:  { label: 'ใต้',           icon: '⬇️', factor: 1.00 },  // ดีที่สุด
  SE: { label: 'ตะวันออกเฉียงใต้', icon: '↙️', factor: 0.96 },
  SW: { label: 'ตะวันตกเฉียงใต้',  icon: '↘️', factor: 0.96 },
  E:  { label: 'ตะวันออก',       icon: '⬅️', factor: 0.88 },
  W:  { label: 'ตะวันตก',        icon: '➡️', factor: 0.88 },
  NE: { label: 'ตะวันออกเฉียงเหนือ', icon: '↖️', factor: 0.78 },
  NW: { label: 'ตะวันตกเฉียงเหนือ',  icon: '↗️', factor: 0.78 },
  N:  { label: 'เหนือ',          icon: '⬆️', factor: 0.68 },  // แย่ที่สุด
};

// คำนวณ factor จากมุมแผง (tilt angle) สำหรับประเทศไทย
// optimal tilt ≈ 10-15° (ใกล้ละติจูดของไทย)
// 0° = แบนราบ (loss น้อย), 30°+ = เสีย efficiency มากขึ้น
function getTiltFactor(angleDeg) {
  // optimal range: 10-20° ได้เต็ม 100%
  // ฐาน: cos function จากมุมที่ดีที่สุด ~15°
  const optimal = 15;
  const diff = Math.abs(angleDeg - optimal);
  // ทุกๆ 10° ที่ห่างจาก optimal → ลด ~3%
  const factor = 1 - (diff / 10) * 0.03;
  return Math.max(0.5, Math.min(1.0, factor));
}

// ฤดูกาลในประเทศไทย (factor การผลิตไฟ)
// อิง: ฝน พ.ค.-ต.ค. ลด 20-30%, ฤดูร้อน มี.ค.-เม.ย. peak
function getSeasonFactor(month) {
  // month: 1-12
  const factors = {
    1: 1.05,  // ม.ค. (อากาศเย็น แผงทำงานดี)
    2: 1.05,  // ก.พ.
    3: 1.10,  // มี.ค. (ฤดูร้อน peak)
    4: 1.10,  // เม.ย. (ฤดูร้อน peak สูงสุด)
    5: 0.90,  // พ.ค. (เริ่มฝน)
    6: 0.80,  // มิ.ย. (ฝน)
    7: 0.78,  // ก.ค. (ฝนหนัก)
    8: 0.78,  // ส.ค. (ฝนหนัก)
    9: 0.80,  // ก.ย. (ฝน)
    10: 0.85, // ต.ค. (ฝนปลาย)
    11: 0.95, // พ.ย. (เย็น)
    12: 1.00, // ธ.ค. (เย็น)
  };
  return factors[month] || 0.95;
}

// คำนวณกำลังผลิต ณ เวลาปัจจุบัน (kW ที่ผลิตได้ ณ ขณะนั้น)
// ใช้ check กับค่าที่ inverter วัดจริง
function calculateCurrentProduction({ kW, hour, month, direction = 'S', tilt = 15, factors = {} }) {
  // สร้าง bell curve ของแสงแดดในวันนั้น (peak ที่เที่ยง)
  // sun rises ~6:00, sets ~18:00, peak ~12:00
  let hourFactor = 0;
  if (hour >= 6 && hour <= 18) {
    // sin curve: 6:00 = 0, 12:00 = 1, 18:00 = 0
    hourFactor = Math.sin(((hour - 6) / 12) * Math.PI);
  }
  
  const dirFactor = PANEL_DIRECTIONS[direction]?.factor || 1.0;
  const tiltFactor = getTiltFactor(tilt);
  const seasonFactor = getSeasonFactor(month);
  
  // ปัจจัยลบเพิ่มเติม (toggle ได้)
  const dustFactor = factors.dust ? 0.95 : 1.0;          // ฝุ่น
  const shadeFactor = factors.shade ? 0.85 : 1.0;        // เงา
  const tempFactor = factors.heatLoss ? 0.92 : 1.0;      // อุณหภูมิสูง
  const cableFactor = factors.cableLoss ? 0.97 : 1.0;    // loss ในสาย
  const inverterFactor = factors.inverterEff ? 0.96 : 1.0; // ประสิทธิภาพ inverter
  
  // ผลิตได้ ณ ขณะนั้น = kW × factors ทั้งหมด
  return kW * hourFactor * dirFactor * tiltFactor * seasonFactor 
       * dustFactor * shadeFactor * tempFactor * cableFactor * inverterFactor;
}

const PRICING_CONFIG = {
  // ค่าไฟปัจจุบัน (งวด พ.ค.-ส.ค. 2569 + VAT 7%)
  electricityRate: 4.23,           // ฿/kWh (3.95 × 1.07)
  touOnPeak: 6.20,                  // ฿/kWh (5.7982 × 1.07) ช่วงจ-ศ 9:00-22:00
  touOffPeak: 2.79,                 // ฿/kWh (2.6037 × 1.07) ช่วงอื่น
  electricityInflation: 0,          // ไม่คิดเงินเฟ้อ (ตัวเลขที่นิ่ง)
  marginByCategory: { small: 25, medium: 20, large: 15 },
  comparisonRates: { bank: 1.5, stock: 7, gold: 6 },
  daysPerMonth: 30,
};

// Sales Catalog Default (สินค้าที่ขาย + ราคาตลาด) - เซลส์จัดการได้ในแอป
// ราคา = ราคาตลาดปัจจุบัน (ไม่รวม VAT 7%) - ใช้เมื่อสต็อกหมด ต้องซื้อใหม่
const DEFAULT_SALES_CATALOG = [
  // ============ SOLIS HYBRID INVERTER (รับประกัน 5 ปี) ============
  { id: 'sc-solis-8k1p',  category: 'inverter', brand: 'Solis', model: 'Hybrid 8kW 1P',  size: 8,  type: 'hybrid', marketPrice: 39500, tier: 'standard', active: true },
  { id: 'sc-solis-10k3p', category: 'inverter', brand: 'Solis', model: 'Hybrid 10kW 3P', size: 10, type: 'hybrid', marketPrice: 61500, tier: 'standard', active: true },
  { id: 'sc-solis-15k3p', category: 'inverter', brand: 'Solis', model: 'Hybrid 15kW 3P', size: 15, type: 'hybrid', marketPrice: 65900, tier: 'standard', active: true },
  { id: 'sc-solis-20k3p', category: 'inverter', brand: 'Solis', model: 'Hybrid 20kW 3P', size: 20, type: 'hybrid', marketPrice: 68900, tier: 'standard', active: true },
  
  // ============ DEYE HYBRID INVERTER (รับประกัน 10 ปี) ============
  { id: 'sc-deye-5k1p',   category: 'inverter', brand: 'Deye', model: 'SUN-5k-SG05LP1-EU',     size: 5,  type: 'hybrid', marketPrice: 31500,  tier: 'standard', active: true },
  { id: 'sc-deye-6k1p',   category: 'inverter', brand: 'Deye', model: 'SUN-6k-SG04LP1-SM2',    size: 6,  type: 'hybrid', marketPrice: 34500,  tier: 'standard', active: true },
  { id: 'sc-deye-8k1p',   category: 'inverter', brand: 'Deye', model: 'SUN-8k-SG05LP1-EU-SM2', size: 8,  type: 'hybrid', marketPrice: 40900,  tier: 'standard', active: true },
  { id: 'sc-deye-10k1p',  category: 'inverter', brand: 'Deye', model: 'SUN-10k-SG02LP1-EU-AM3', size: 10, type: 'hybrid', marketPrice: 51900,  tier: 'standard', active: true },
  { id: 'sc-deye-5k3p',   category: 'inverter', brand: 'Deye', model: 'SUN-5k-SG05LP3-SM2',    size: 5,  type: 'hybrid', marketPrice: 49900,  tier: 'standard', active: true },
  { id: 'sc-deye-10k3p',  category: 'inverter', brand: 'Deye', model: 'SUN-10k-SG04LP3-EU',    size: 10, type: 'hybrid', marketPrice: 59500,  tier: 'standard', active: true },
  { id: 'sc-deye-12k3p',  category: 'inverter', brand: 'Deye', model: 'SUN-12k-SG04LP3-EU',    size: 12, type: 'hybrid', marketPrice: 62500,  tier: 'standard', active: true },
  { id: 'sc-deye-20k3p',  category: 'inverter', brand: 'Deye', model: 'SUN-20k-SG05LP3-EU-SM2', size: 20, type: 'hybrid', marketPrice: 89500,  tier: 'standard', active: true },
  { id: 'sc-deye-30k3p',  category: 'inverter', brand: 'Deye', model: 'SUN-30k-SG01HP3-EU-BM3 (HV)', size: 30, type: 'hybrid', marketPrice: 112500, tier: 'premium',  active: true },
  { id: 'sc-deye-40k3p',  category: 'inverter', brand: 'Deye', model: 'SUN-40k-SG01HP3-EU-BM4 (HV)', size: 40, type: 'hybrid', marketPrice: 134900, tier: 'premium',  active: true },
  { id: 'sc-deye-50k3p',  category: 'inverter', brand: 'Deye', model: 'SUN-50k-SG01HP3-EU-BM4 (HV)', size: 50, type: 'hybrid', marketPrice: 149000, tier: 'premium',  active: true },
  { id: 'sc-deye-60k3p',  category: 'inverter', brand: 'Deye', model: 'SUN-60k-SG01HP3-EU-BM4 (HV)', size: 60, type: 'hybrid', marketPrice: 181550, tier: 'premium',  active: true },
  { id: 'sc-deye-80k3p',  category: 'inverter', brand: 'Deye', model: 'SUN-80k-SG01HP3-EU-BM4 (HV)', size: 80, type: 'hybrid', marketPrice: 204900, tier: 'premium',  active: true },
  
  // ============ TMDA ON-GRID INVERTER (รับประกัน 10 ปี) ============
  { id: 'sc-tmda-3k1p',   category: 'inverter', brand: 'TMDA', model: 'SUN-3K-G04P1-EU-AM1',     size: 3,  type: 'ongrid', marketPrice: 9500,  tier: 'standard', active: true },
  { id: 'sc-tmda-5k1p',   category: 'inverter', brand: 'TMDA', model: 'SUN-5K-G05P1-EU-AM2',     size: 5,  type: 'ongrid', marketPrice: 15200, tier: 'standard', active: true },
  { id: 'sc-tmda-10k1p',  category: 'inverter', brand: 'TMDA', model: 'SUN-10K-G02P1-EU-AM2',    size: 10, type: 'ongrid', marketPrice: 22500, tier: 'standard', active: true },
  { id: 'sc-tmda-6k3p',   category: 'inverter', brand: 'TMDA', model: 'SUN-6K-G06P3-EU-BM2-P1',  size: 6,  type: 'ongrid', marketPrice: 18900, tier: 'standard', active: true },
  { id: 'sc-tmda-10k3p',  category: 'inverter', brand: 'TMDA', model: 'SUN-15K-G06P3-EU-BM2-P1', size: 10, type: 'ongrid', marketPrice: 21900, tier: 'standard', active: true },
  
  // ============ SOLAR PANELS ============
  { id: 'sc-pan-jinko-725', category: 'panel', brand: 'Jinko', model: '725W', watt: 725, marketPrice: 4000, tier: 'premium',  active: true },
  { id: 'sc-pan-longi-640', category: 'panel', brand: 'Longi', model: '640W', watt: 640, marketPrice: 2911, tier: 'standard', active: true },
  
  // ============ BATTERIES ============
  { id: 'sc-bat-deye-16', category: 'battery', brand: 'Deye', model: '16kWh', capacity: 16, marketPrice: 67303, tier: 'standard', active: true },
  
  // ============ WIRES (สายไฟ) — ขายแยก/เสริม ============
  // หมายเหตุ: ราคาเป็น ฿/เมตร — ต้องคูณความยาวที่ลูกค้าใช้
  { id: 'sc-wire-pv-bk',     category: 'wire', brand: 'Yasaki', model: 'PV1-F 6mm² สีดำ',          watt: 6, marketPrice: 55,  tier: 'standard', active: true, unit: 'm', wireType: 'pv' },
  { id: 'sc-wire-pv-rd',     category: 'wire', brand: 'Yasaki', model: 'PV1-F 6mm² สีแดง',         watt: 6, marketPrice: 55,  tier: 'standard', active: true, unit: 'm', wireType: 'pv' },
  { id: 'sc-wire-ac-10-bk',  category: 'wire', brand: 'Yasaki', model: 'THW 10mm² สีดำ (5kW)',     watt: 10, marketPrice: 95, tier: 'standard', active: true, unit: 'm', wireType: 'ac', forInvSize: '<=5' },
  { id: 'sc-wire-ac-10-gy',  category: 'wire', brand: 'Yasaki', model: 'THW 10mm² เขียวเหลือง (5kW)', watt: 10, marketPrice: 95, tier: 'standard', active: true, unit: 'm', wireType: 'ac', forInvSize: '<=5' },
  { id: 'sc-wire-ac-16-bk',  category: 'wire', brand: 'Yasaki', model: 'THW 16mm² สีดำ (10kW+)',   watt: 16, marketPrice: 140, tier: 'standard', active: true, unit: 'm', wireType: 'ac', forInvSize: '>5' },
  { id: 'sc-wire-ac-16-gy',  category: 'wire', brand: 'Yasaki', model: 'THW 16mm² เขียวเหลือง (10kW+)', watt: 16, marketPrice: 140, tier: 'standard', active: true, unit: 'm', wireType: 'ac', forInvSize: '>5' },
];

// Legacy fallback (เผื่อ catalog ว่าง)
const EQUIPMENT_CATALOG = {
  inverters: DEFAULT_SALES_CATALOG.filter(i => i.category === 'inverter').map(i => ({...i, cost: i.marketPrice})),
  panels: DEFAULT_SALES_CATALOG.filter(i => i.category === 'panel').map(i => ({...i, cost: i.marketPrice})),
  batteries: DEFAULT_SALES_CATALOG.filter(i => i.category === 'battery').map(i => ({...i, cost: i.marketPrice})),
};

// Smart cost calculator: ใช้ stock ก่อน → ส่วนที่เหลือ market price
function calcSmartCost(catalogItem, qtyNeeded, stock = []) {
  // หา stock ที่ตรงกับ catalog (match brand+model+watt/size/capacity)
  const matchingStock = stock
    .filter(s => s.qty > 0 && s.salesSpecs &&
      s.salesSpecs.brand === catalogItem.brand && 
      s.salesSpecs.model === catalogItem.model)
    .sort((a, b) => a.unitCost - b.unitCost); // ใช้ของถูกก่อน
  
  let cost = 0;
  let remaining = qtyNeeded;
  let fromStock = 0;
  let fromMarket = 0;
  const breakdown = [];
  
  for (const stk of matchingStock) {
    if (remaining <= 0) break;
    const useQty = Math.min(stk.qty, remaining);
    cost += useQty * stk.unitCost;
    fromStock += useQty;
    breakdown.push({ source: 'stock', stockId: stk.id, qty: useQty, unitCost: stk.unitCost });
    remaining -= useQty;
  }
  
  if (remaining > 0) {
    cost += remaining * catalogItem.marketPrice;
    fromMarket = remaining;
    breakdown.push({ source: 'market', qty: remaining, unitCost: catalogItem.marketPrice });
  }
  
  return { cost, fromStock, fromMarket, breakdown, total: qtyNeeded };
}

function getMargin(inverterKW, companyInfo = null) {
  const margins = companyInfo?.margins || PRICING_CONFIG.marginByCategory;
  if (inverterKW < 5)  return margins.small;
  if (inverterKW <= 10) return margins.medium;
  return margins.large;
}

// ผลรวมต้นทุนแฝง (เปิดอยู่ทั้งหมด)
function sumHiddenCosts(companyInfo, inverterSize = null) {
  const items = companyInfo?.hiddenCosts || [];
  return items.filter(i => {
    if (i.perJob === false) return false;
    // เช็ค applyIfInvSize - applied conditionally
    if (i.applyIfInvSize && inverterSize !== null) {
      const cond = i.applyIfInvSize.trim();
      if (cond.startsWith('<=')) {
        const max = parseFloat(cond.slice(2));
        return inverterSize <= max;
      }
      if (cond.startsWith('>=')) {
        const min = parseFloat(cond.slice(2));
        return inverterSize >= min;
      }
      if (cond.startsWith('<')) {
        const max = parseFloat(cond.slice(1));
        return inverterSize < max;
      }
      if (cond.startsWith('>')) {
        const min = parseFloat(cond.slice(1));
        return inverterSize > min;
      }
    }
    return true;
  }).reduce((sum, i) => sum + (Number(i.amount) || 0), 0);
}

function applyMargin(cost, marginPct) {
  return Math.round(cost * (1 + marginPct / 100));
}

// ปัดราคาขึ้นให้ลงท้าย 999 (Psychological Pricing)
// ใช้กับราคาขายทุกที่ (Closer, Custom, ใบเสนอราคา)
// 213,123 → 213,999 (+876)  
// 199,500 → 199,999 (+499)
// 100,000 → 100,999 (+999)
// 99,999  → 99,999  (ลงท้าย 999 แล้วไม่ปัด)
function roundUpTo999(price) {
  if (price < 1000) return 999;
  const thousands = Math.floor(price / 1000);
  const remainder = price % 1000;
  if (remainder === 999) return price;
  return thousands * 1000 + 999;
}

// คำนวณ ROI พร้อม 2 mode
// mode='dream' ขายฝัน: ใช้ PSH ทฤษฎี ไม่หัก degradation
// mode='honest' จริงใจ: ใช้ PSH × PR (จริง) + หัก degradation 0.6%/ปี (NREL)
function calculateROI({ kW, region, meterType = 'normal', electricityRate = null, touRates = null, inflation = null, mode = 'dream' }) {
  const regionData = SOLAR_REGIONS[region] || SOLAR_REGIONS.central;
  // เลือก PSH ตาม mode
  const peakHours = mode === 'dream' 
    ? (regionData.theoreticalPSH || regionData.hours)
    : (regionData.hours || 3.7);
  
  const monthlyKwh = kW * peakHours * PRICING_CONFIG.daysPerMonth;
  const yearlyKwh = monthlyKwh * 12;
  
  // คำนวณค่าไฟตามประเภทมิเตอร์
  let effectiveRate;
  if (meterType === 'tou' && touRates) {
    // Solar ผลิตช่วง on-peak (กลางวัน) ~95% ของผลผลิต
    const onPeakPct = 0.95;
    effectiveRate = (touRates.onPeak * onPeakPct) + (touRates.offPeak * (1 - onPeakPct));
  } else {
    effectiveRate = electricityRate || PRICING_CONFIG.electricityRate;
  }
  
  const inflationRate = (inflation !== null ? inflation : PRICING_CONFIG.electricityInflation) / 100;
  
  // mode 'honest' หัก degradation, mode 'dream' ไม่หัก
  const degradation = mode === 'honest' ? PANEL_DEGRADATION_RATE : 0;
  
  const cumProfit = (years) => {
    let total = 0;
    for (let y = 1; y <= years; y++) {
      const yearProduction = yearlyKwh * Math.pow(1 - degradation, y - 1);
      total += yearProduction * effectiveRate * Math.pow(1 + inflationRate, y - 1);
    }
    return Math.round(total);
  };
  
  return {
    monthlyKwh: Math.round(monthlyKwh),
    yearlyKwh: Math.round(yearlyKwh),
    monthlySavings: Math.round(monthlyKwh * effectiveRate),
    yearlySavings: Math.round(yearlyKwh * effectiveRate),
    effectiveRate,
    profit5: cumProfit(5),
    profit10: cumProfit(10),
    profit20: cumProfit(20),
    profit30: cumProfit(30),
    mode,
    peakHours,        // เพื่อแสดงให้ user เห็น
    pr: regionData.pr || 0.73,
    degradation,
  };
}

function calculateInvestmentComparison(principal, years, ratePct) {
  return Math.round(principal * (Math.pow(1 + ratePct / 100, years) - 1));
}

function calculateCO2(yearlyKwh, years) {
  return Math.round(yearlyKwh * 0.5 * years / 1000); // ตัน
}

// Smart Package Recommender — ใช้ catalog + smart pricing
function recommendPackages({ monthlyBill, hasBattery, region, meterType = 'normal', stock = [], catalog = [], companyInfo = null }) {
  // ใช้ dream peakHours (PSH ทฤษฎี) สำหรับ filter
  // เพื่อให้ filter สอดคล้องกับการแสดงผล (Closer แสดงด้วย dream by default)
  const regionData = SOLAR_REGIONS[region] || SOLAR_REGIONS.central;
  const peakHours = regionData.theoreticalPSH || regionData.hours || 5.0;
  const electricityRate = PRICING_CONFIG.electricityRate;
  
  const monthlyKwhUsage = monthlyBill / electricityRate;
  const requiredKW = monthlyKwhUsage / 30 / peakHours;
  
  // ดึงเฉพาะ active items ใน catalog
  const activeCatalog = (catalog || []).filter(c => c.active !== false);
  const inverters = activeCatalog.filter(c => c.category === 'inverter');
  const panels = activeCatalog.filter(c => c.category === 'panel');
  const batteries = activeCatalog.filter(c => c.category === 'battery');
  
  if (inverters.length === 0 || panels.length === 0) return null;
  
  // คำนวณ kW ที่เหมาะสมกับลูกค้า
  const targetKW = Math.max(3, Math.min(20, Math.ceil(requiredKW)));
  
  // หา inverter ตามขนาด + ประเภท
  const findInverter = (preferKW, preferType, preferTier) => {
    // 1. ลองหา type ที่ต้องการ + ขนาดใกล้ preferKW
    let candidates = inverters.filter(i => !preferType || i.type === preferType);
    if (candidates.length === 0) candidates = inverters;
    if (preferTier) {
      const tiered = candidates.filter(i => i.tier === preferTier);
      if (tiered.length > 0) candidates = tiered;
    }
    // เรียงตามความใกล้ kW (ถ้าเจอเท่ากันให้ราคาถูกก่อน)
    return [...candidates].sort((a, b) => {
      const diffA = Math.abs(a.size - preferKW);
      const diffB = Math.abs(b.size - preferKW);
      if (diffA !== diffB) return diffA - diffB;
      return a.marketPrice - b.marketPrice;
    })[0];
  };
  
  const hiddenCostsTotal = sumHiddenCosts(companyInfo);
  
  // === Build a package with capped savings ===
  // capRatio: 1.0 = ไม่เกินค่าไฟปัจจุบัน, 2.0 = ไม่เกิน 2 เท่า
  const buildPackage = (inverter, panel, panelCount, battery, label, badge) => {
    // Smart cost: ใช้ stock ก่อน → ที่ขาด ใช้ market
    const invCost = calcSmartCost(inverter, 1, stock);
    const panCost = calcSmartCost(panel, panelCount, stock);
    const batCost = battery ? calcSmartCost(battery, 1, stock) : { cost: 0, fromStock: 0, fromMarket: 0, breakdown: [], total: 0 };
    
    const equipmentCost = invCost.cost + panCost.cost + batCost.cost;
    // คิดต้นทุนแฝงตามขนาด inverter (สาย 5kW vs 10kW ต่างกัน)
    const installCost = sumHiddenCosts(companyInfo, inverter.size);
    const grandCost = equipmentCost + installCost;
    const margin = getMargin(inverter.size, companyInfo);
    const sellPriceRaw = applyMargin(grandCost, margin);
    const sellPrice = roundUpTo999(sellPriceRaw); // 🎯 ปัดขึ้น 999
    
    const totalKW = (panel.watt * panelCount) / 1000;
    // ใช้ mode 'dream' + meterType + touRates ตามลูกค้าเลือก
    // เพื่อให้ตัวเลขที่แสดงในทุกหน้าตรงกัน
    const roi = calculateROI({ 
      kW: Math.min(totalKW, inverter.size), 
      region, 
      meterType,
      touRates: { onPeak: PRICING_CONFIG.touOnPeak, offPeak: PRICING_CONFIG.touOffPeak },
      mode: 'dream' 
    });
    const breakEven = sellPrice / roi.yearlySavings;
    
    return {
      label, badge,
      inverter, panel, panelCount, battery,
      costBreakdown: { invCost, panCost, batCost },
      equipmentCost,
      installCost,
      totalCost: grandCost,
      sellPrice,
      margin,
      profit: sellPrice - grandCost,
      totalKW: Math.round(totalKW * 100) / 100,
      roi,
      breakEven: Math.round(breakEven * 10) / 10,
    };
  };
  
  // === Brute force: ลองทุกชุด แล้วเลือกที่ดีที่สุด ===
  // Helper: นับจำนวนแผงตามเงื่อนไข
  // panelCountForRatio(inv, pan, ratio): จำนวนแผงที่วัตต์รวมไม่เกิน inv.size × ratio
  const panelCountForRatio = (inv, pan, ratio) => {
    return Math.floor(inv.size * 1000 * ratio / pan.watt);
  };
  
  const yearlyBill = monthlyBill * 12;
  
  // ============ Package 1: ถูกสุด (ลงทุนน้อยสุด) ============
  // Rule: ราคาขายต่ำสุด, จำนวนแผงไม่เกินกำลัง inverter (วัตต์รวม ≤ inverter kW × 100%)
  let cheapPackage = null;
  let cheapPrice = Infinity;
  for (const inv of inverters) {
    for (const pan of panels) {
      // จำนวนแผง: เต็ม inverter (100%) แต่ไม่เกิน
      const panelCount = panelCountForRatio(inv, pan, 1.0);
      if (panelCount < 1) continue;
      
      // ไม่มีแบต (ถูกสุด)
      const pkg = buildPackage(inv, pan, panelCount, null);
      if (pkg.sellPrice < cheapPrice) {
        cheapPrice = pkg.sellPrice;
        cheapPackage = pkg;
      }
    }
  }
  if (!cheapPackage) {
    // Fallback: ใช้ตัวเล็กสุด
    const smallestInv = [...inverters].sort((a, b) => a.size - b.size)[0];
    const cheapestPan = [...panels].sort((a, b) => a.marketPrice - b.marketPrice)[0];
    const count = Math.max(1, panelCountForRatio(smallestInv, cheapestPan, 1.0));
    cheapPackage = buildPackage(smallestInv, cheapestPan, count, null);
  }
  cheapPackage.label = 'ถูกสุด (ลงทุนน้อย แต่ก็ประหยัดนะ)';
  cheapPackage.badge = '💰';
  
  // ============ Package 2: คุ้มสุด (คืนทุนเร็วสุด) ============
  // Rule: breakEven ต่ำสุด
  //   - จำนวนแผง วัตต์รวม ≤ inverter kW × 1.05 (เกิน 5% ได้)
  //   - ผลิตไฟ × ค่าไฟ ≤ ค่าไฟปัจจุบัน (ไม่ผลิตเกินใช้)
  let bestPackage = null;
  let bestBreakEven = Infinity;
  for (const inv of inverters) {
    for (const pan of panels) {
      // จำนวนแผง: ใส่ได้ถึง 105% ของ inverter
      const panelCount = panelCountForRatio(inv, pan, 1.05);
      if (panelCount < 1) continue;
      
      const bat = hasBattery && batteries.length > 0 ? batteries[0] : null;
      const pkg = buildPackage(inv, pan, panelCount, bat);
      
      // ⛔ กรอง: ผลิตเกินค่าไฟปัจจุบัน
      if (pkg.roi.yearlySavings > yearlyBill) continue;
      
      if (pkg.breakEven > 0 && pkg.breakEven < bestBreakEven) {
        bestBreakEven = pkg.breakEven;
        bestPackage = pkg;
      }
    }
  }
  if (!bestPackage) {
    bestPackage = cheapPackage;
  }
  bestPackage.label = 'คุ้มสุด (คืนทุนเร็วสุด)';
  bestPackage.badge = '🌟';
  
  // ============ Package 3: Premium (เพื่ออนาคต) ============
  // Rule: 
  //   - inverter ผลิตไฟได้ × ค่าไฟ > 2 เท่าค่าไฟปัจจุบัน (เผื่อขยายในอนาคต)
  //   - แต่จำนวนแผงปัจจุบัน × ผลิตไฟ × ค่าไฟ ≤ ค่าไฟปัจจุบัน
  // → inverter ใหญ่ + แผงน้อย (เผื่อเพิ่มแผงในอนาคต)
  
  let premiumPackage = null;
  let premiumBestBE = Infinity;
  
  // กำลังผลิตของ inverter เต็ม (kWh/ปี)
  const inverterYearlyProduction = (invSize) => invSize * peakHours * 30 * 12;
  // มูลค่าไฟ/ปี ที่ inverter ผลิตเต็มได้
  const inverterYearlyValue = (invSize) => inverterYearlyProduction(invSize) * electricityRate;
  
  for (const inv of inverters) {
    // ⛔ inverter ต้องผลิตได้ > 2x ของค่าไฟปัจจุบัน
    if (inverterYearlyValue(inv.size) <= yearlyBill * 2) continue;
    
    for (const pan of panels) {
      // จำนวนแผง: ผลิตไฟ × ค่าไฟ ≤ ค่าไฟปัจจุบัน (100%)
      // → maxPanelKW = yearlyBill / (peakHours × 30 × 12 × rate)
      const maxPanelKW = yearlyBill / (peakHours * 30 * 12 * electricityRate);
      const panelCount = Math.floor(maxPanelKW * 1000 / pan.watt);
      if (panelCount < 1) continue;
      
      const bat = batteries.length > 0 ? batteries[0] : null;
      const pkg = buildPackage(inv, pan, panelCount, bat);
      
      // เลือกตัวที่ breakEven ต่ำสุด (ในกลุ่ม premium)
      if (pkg.breakEven > 0 && pkg.breakEven < premiumBestBE) {
        premiumBestBE = pkg.breakEven;
        premiumPackage = pkg;
      }
    }
  }
  
  // Fallback: ถ้าไม่มี inverter ใหญ่พอ ให้ใช้ตัวใหญ่สุดที่มี
  if (!premiumPackage) {
    const biggestInv = [...inverters].sort((a, b) => b.size - a.size)[0];
    const bestPan = [...panels].sort((a, b) => b.watt - a.watt)[0];
    // จำนวนแผงเต็ม (100% ของ inverter)
    const count = Math.max(1, panelCountForRatio(biggestInv, bestPan, 1.0));
    const bat = batteries.length > 0 ? batteries[0] : null;
    premiumPackage = buildPackage(biggestInv, bestPan, count, bat);
  }
  premiumPackage.label = 'Premium (เพื่ออนาคต)';
  premiumPackage.badge = '👑';
  
  return {
    cheap:   cheapPackage,
    best:    bestPackage,
    premium: premiumPackage,
  };
}

// ============== DOCUMENT TYPES ==============
const DOC_TYPES = {
  quotation:        { label: 'ใบเสนอราคา',          shortLabel: 'ใบเสนอราคา',  prefix: 'QT',   color: 'blue',    icon: '📄' },
  invoice:          { label: 'ใบแจ้งหนี้',           shortLabel: 'ใบแจ้งหนี้',   prefix: 'INV',  color: 'amber',   icon: '🧾' },
  'receipt-deposit':{ label: 'ใบเสร็จรับเงิน (มัดจำ)', shortLabel: 'RC มัดจำ',     prefix: 'RCD',  color: 'cyan',    icon: '💰' },
  'receipt-final':  { label: 'ใบเสร็จรับเงิน (เต็ม)',  shortLabel: 'RC เต็ม',      prefix: 'RC',   color: 'emerald', icon: '✅' },
  receipt:          { label: 'ใบเสร็จรับเงิน',         shortLabel: 'ใบเสร็จ',      prefix: 'RC',   color: 'emerald', icon: '✅' },
};

// QT2026/04-001 = ใบเสนอราคา ปี 2026 เดือน 04 ลำดับที่ 001
function generateDocNumber(type, existingDocs = []) {
  const info = DOC_TYPES[type] || { prefix: 'DOC' };
  const prefix = info.prefix;
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const yearMonth = `${year}/${month}`;
  
  // หาเลขลำดับล่าสุดของเดือนนี้ (เช็คทั้ง prefix เดียวกัน)
  const sameMonthDocs = existingDocs.filter(d => 
    d.docNumber && d.docNumber.startsWith(`${prefix}${yearMonth}`)
  );
  const seq = sameMonthDocs.length + 1;
  return `${prefix}${yearMonth}-${String(seq).padStart(3, '0')}`;
}

// Helper: รับ type info (รองรับเอกสารเก่าที่ type='receipt')
function getDocTypeInfo(type) {
  return DOC_TYPES[type] || DOC_TYPES.quotation;
}

// Migration: เพิ่ม jobChainId, jobStatus ให้เอกสารเก่า
// ============== Auto-Migration: Transactions ==============
// แก้ปัญหา data ที่ logic ไม่ถูก:
// 1. "ทุน X" ถูกบันทึกเป็น expense 'ต้นทุนงาน' อย่างเดียว (ขาด income 'เพิ่มทุน' คู่)
// 2. "เบิกสต๊อก" ถูกนับเป็น expense (double-count)
// 3. ซื้อสต๊อกที่มี partnerId แต่ไม่มี income 'เพิ่มทุน' คู่
// ============== Auto-Migration: Jobs ==============
// ใส่ stockId + qtyUsed ให้ item เก่าที่เบิกจากสต๊อกแต่ไม่ได้ track
// (match เฉพาะกรณีชัดเจน: item มีคำ "สต๊อก" + ชื่อตรงกับ stock ตัวเดียว)
function migrateJobs(jobsList, stockList) {
  if (!Array.isArray(jobsList)) return { jobs: [], changed: false };
  let changed = false;
  const jobs = jobsList.map(job => {
    if (!job.costsByCategory) return job;
    let jobChanged = false;
    const newCats = {};
    Object.entries(job.costsByCategory).forEach(([cat, items]) => {
      newCats[cat] = (items || []).map(item => {
        if (item.stockId || !item.item || !item.item.includes('สต๊อก')) return item;
        // ดึงชื่อหลัก (ตัด "× N (จากสต๊อก)" ออก) + จำนวนจาก "× N"
        const qtyMatch = item.item.match(/[×x]\s*(\d+)/);
        const baseName = item.item.replace(/\s*[×x]\s*\d+.*$/, '').trim();
        const matches = (stockList || []).filter(s => 
          s.name.includes(baseName) || baseName.includes(s.name.replace(/^แผง\s*/, ''))
        );
        if (matches.length === 1 && qtyMatch) {
          jobChanged = true;
          return { ...item, stockId: matches[0].id, qtyUsed: Number(qtyMatch[1]) };
        }
        return item;
      });
    });
    if (jobChanged) { changed = true; return { ...job, costsByCategory: newCats }; }
    return job;
  });
  return { jobs, changed };
}

// ============== Sync เงินจากงาน (เซฟงาน = บันทึกเงินทันที) ==============
// หลัก: ยอด income ของงาน = salePrice เสมอ / expense จ่ายจริง = cashCost เสมอ
// ใช้ tx id ตายตัวต่องาน (t-jobinc-X / t-jobcost-X) → update แทนสร้างซ้ำ, กันซ้ำ 100%
// ใบเสร็จ/รายการมือที่มีอยู่ = นับรวมก่อน เหลือเท่าไหร่ auto เติมเท่านั้น
function syncJobFinanceTxs(job, txs, userName) {
  if (!job || !job.id) return { txs, changes: [] };
  const changes = [];
  let list = [...txs];
  const now = new Date().toISOString();
  const today = now.split('T')[0];

  const upsert = (kind, type, category, target, desc) => {
    const autoId = `t-job${kind}-${job.id}`;
    const others = list.filter(t => t.type === type && t.category === category && t.jobId === job.id && !t.isService && t.id !== autoId)
      .reduce((s, t) => s + Number(t.amount || 0), 0);
    const need = Math.round((target - others) * 100) / 100;
    const existing = list.find(t => t.id === autoId);
    if (need > 0.5) {
      if (!existing) {
        list.push({
          id: autoId, date: job.date || today, type, category, amount: need,
          description: desc, jobId: job.id, partnerId: '', auto: true,
          createdBy: `${userName} (บันทึกจากงาน)`, createdAt: now,
        });
        changes.push(`${type === 'income' ? '+' : '−'}${need.toLocaleString()} ${category}`);
      } else if (Math.abs(Number(existing.amount) - need) > 0.5) {
        list = list.map(t => t.id === autoId ? { ...t, amount: need, description: desc, editedBy: `${userName} (sync จากงาน)`, editedAt: now, editCount: (t.editCount || 0) + 1 } : t);
        changes.push(`ปรับ${category}เป็น ${need.toLocaleString()}`);
      }
    } else if (existing) {
      list = list.filter(t => t.id !== autoId);
      changes.push(`ตัด${category}อัตโนมัติ (มีรายการอื่นครบแล้ว)`);
    }
    return list;
  };

  // รายได้ = ราคาขาย
  const salePrice = Number(job.salePrice || 0);
  if (salePrice > 0) list = upsert('inc', 'income', 'รายได้จากงาน', salePrice, `${job.customer} - ${job.type || 'งานติดตั้ง'} (บันทึกจากงาน)`);
  // ต้นทุนจ่ายจริง (ไม่รวมเบิกสต๊อก — จ่ายไปแล้วตอนซื้อเข้า)
  let cashCost = 0;
  Object.values(job.costsByCategory || {}).forEach(items => (items || []).forEach(it => { if (!it.stockId) cashCost += Number(it.amount || 0); }));
  list = upsert('cost', 'expense', 'ต้นทุนงาน', cashCost, `ต้นทุนงาน ${job.customer} - จ่ายจริง (บันทึกจากงาน)`);

  return { txs: list, changes };
}

function migrateTransactions(transactions) {
  if (!Array.isArray(transactions)) return { transactions: [], changed: false, summary: '' };
  
  let txs = [...transactions];
  let changes = [];
  
  // 1. ลบ "เบิกสต๊อก" (double-count)
  const beforeLen = txs.length;
  txs = txs.filter(t => !(t.type === 'expense' && t.category === 'เบิกสต๊อก'));
  if (txs.length < beforeLen) {
    changes.push(`ลบ "เบิกสต๊อก" ${beforeLen - txs.length} รายการ`);
  }
  
  // 2. Deduplicate: ลบ income "เพิ่มทุน" ที่ซ้ำ (ผูก partnerId + jobId + amount เดียวกัน)
  // เก็บแค่ตัวแรก
  const capitalKeys = new Set();
  const beforeDedup = txs.length;
  txs = txs.filter(t => {
    if (t.type === 'income' && (t.category === 'เพิ่มทุน' || t.category === 'ทุน')) {
      const key = `${t.partnerId}|${t.jobId || ''}|${Number(t.amount).toFixed(2)}`;
      if (capitalKeys.has(key)) {
        return false; // ซ้ำ - ลบ
      }
      capitalKeys.add(key);
    }
    return true;
  });
  if (txs.length < beforeDedup) {
    changes.push(`ลบ "เพิ่มทุน" ซ้ำ ${beforeDedup - txs.length} รายการ`);
  }
  
  // ✨ โครงสร้างใหม่: ไม่ auto-gen "เพิ่มทุน" คู่กับรายจ่ายอีกแล้ว
  // เพิ่มทุน = ทำผ่านปุ่ม "เพิ่มทุน" ใน Dashboard เท่านั้น
  // (migration เก่าสร้าง tx ครบแล้ว ข้อมูลเก่าปลอดภัย)
  
  // 3. ลบ flags `_migration*` ออก (clean up)
  txs = txs.map(t => {
    const { _migration, _migrationFor, ...rest } = t;
    return rest;
  });
  
  return {
    transactions: txs,
    changed: changes.length > 0,
    summary: changes.join(', '),
  };
}

function migrateDocuments(docs) {
  if (!Array.isArray(docs)) return [];
  return docs.map(d => {
    // ถ้าเป็นเอกสารเก่าที่ไม่มี jobChainId
    if (!d.jobChainId) {
      // ถ้าเป็น quotation → ใช้ id ตัวเองเป็น chain (เป็น master)
      // ถ้าเป็นใบอื่น → ถ้ามี linkedDocId ให้ตามไปหา quotation root
      let chainId = d.id;
      if (d.type !== 'quotation' && d.linkedDocId) {
        // ตามไปหา root (quotation)
        const visited = new Set();
        let current = d;
        while (current && current.linkedDocId && !visited.has(current.id)) {
          visited.add(current.id);
          const next = docs.find(x => x.id === current.linkedDocId);
          if (!next) break;
          current = next;
        }
        chainId = current?.id || d.id;
      }
      d = { ...d, jobChainId: chainId };
    }
    // เพิ่ม jobStatus default
    if (!d.jobStatus) {
      d = { ...d, jobStatus: d.status === 'closed' ? 'closed' : 'active' };
    }
    return d;
  });
}

// ============== APP WRAPPER WITH LOGIN ==============
function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [checkingAuth, setCheckingAuth] = useState(true);

  // Load SheetJS for Excel export
  useEffect(() => {
    if (!window.XLSX) {
      const script = document.createElement('script');
      script.src = 'https://cdn.jsdelivr.net/npm/xlsx-js-style@1.2.0/dist/xlsx.bundle.js';
      script.async = true;
      document.head.appendChild(script);
    }
  }, []);

  // Check saved login on mount
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const saved = await window.storage.get('dd:auth:current', false).catch(() => null);
        if (saved && saved.value) {
          const userId = saved.value;
          const userEntry = Object.entries(USERS).find(([_, u]) => u.id === userId);
          if (userEntry) {
            setCurrentUser({ pin: userEntry[0], ...userEntry[1] });
          }
        }
      } catch (e) {}
      setCheckingAuth(false);
    };
    checkAuth();
  }, []);

  const handleLogin = async (user) => {
    setCurrentUser(user);
    try { await window.storage.set('dd:auth:current', user.id, false); } catch (e) {}
  };

  const handleLogout = async () => {
    if (!window.confirm('ออกจากระบบ?')) return;
    setCurrentUser(null);
    try { await window.storage.delete('dd:auth:current', false); } catch (e) {}
  };

  if (checkingAuth) {
    return (
      <div className="min-h-screen bg-stone-100 flex items-center justify-center">
        <Sun className="w-16 h-16 text-amber-500 animate-spin" />
      </div>
    );
  }

  if (!currentUser) {
    return <LoginScreen onLogin={handleLogin} />;
  }

  return <DDSolutionManager currentUser={currentUser} onLogout={handleLogout} />;
}

function LoginScreen({ onLogin }) {
  const [pin, setPin] = useState('');
  const [error, setError] = useState('');
  const [shake, setShake] = useState(false);

  const tryLogin = (newPin) => {
    if (newPin.length === 4) {
      const user = USERS[newPin];
      if (user) {
        onLogin({ pin: newPin, ...user });
      } else {
        setError('PIN ไม่ถูกต้อง');
        setShake(true);
        setTimeout(() => { setShake(false); setPin(''); setError(''); }, 1000);
      }
    }
  };

  const addDigit = (d) => {
    if (pin.length < 4) {
      const newPin = pin + d;
      setPin(newPin);
      setError('');
      tryLogin(newPin);
    }
  };

  const removeDigit = () => {
    setPin(pin.slice(0, -1));
    setError('');
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4" style={{fontFamily: "'Sarabun', system-ui, sans-serif", background: 'linear-gradient(135deg, #0d1f43 0%, #1e3a5f 50%, #0d1f43 100%)'}}>
      <style>{`
        
        .display-font { font-family: 'Bebas Neue', sans-serif; letter-spacing: 0.04em; }
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-10px); }
          75% { transform: translateX(10px); }
        }
        .animate-shake { animation: shake 0.4s ease-in-out 2; }
      `}</style>
      <div className={`bg-white rounded-3xl shadow-2xl p-8 w-full max-w-sm ${shake ? 'animate-shake' : ''}`}>
        <div className="text-center mb-6">
          <img src="icons/icon-192.png" alt="DD Logo" className="w-24 h-24 mx-auto mb-3 rounded-2xl shadow-md" />
          <h1 className="display-font text-3xl text-stone-900">D.D. SOLUTION</h1>
          <p className="text-sm text-stone-500 mt-1">ใส่ PIN 4 หลักเพื่อเข้าใช้งาน</p>
        </div>

        {/* PIN dots */}
        <div className="flex justify-center gap-3 mb-3">
          {[0,1,2,3].map(i => (
            <div key={i} className={`w-4 h-4 rounded-full border-2 transition-all ${
              i < pin.length ? 'bg-amber-500 border-amber-500 scale-110' : 'border-stone-300'
            }`} />
          ))}
        </div>

        {error && <p className="text-center text-red-500 text-sm mb-3">{error}</p>}

        {/* Number pad */}
        <div className="grid grid-cols-3 gap-3">
          {[1,2,3,4,5,6,7,8,9].map(n => (
            <button key={n} onClick={() => addDigit(String(n))}
              className="aspect-square rounded-2xl bg-stone-100 hover:bg-amber-100 active:bg-amber-200 text-2xl font-bold text-stone-700 transition-colors">
              {n}
            </button>
          ))}
          <div></div>
          <button onClick={() => addDigit('0')}
            className="aspect-square rounded-2xl bg-stone-100 hover:bg-amber-100 active:bg-amber-200 text-2xl font-bold text-stone-700 transition-colors">
            0
          </button>
          <button onClick={removeDigit}
            className="aspect-square rounded-2xl bg-rose-100 hover:bg-rose-200 active:bg-rose-300 text-stone-700 transition-colors flex items-center justify-center">
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="mt-6 pt-4 border-t border-stone-200">
          <p className="text-xs text-stone-400 text-center">
            👨 พ่อ · 💼 โฟน · 📱 อาม
          </p>
        </div>
      </div>
    </div>
  );
}

// ============== MAIN APP ==============
function DDSolutionManager({ currentUser, onLogout }) {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [loading, setLoading] = useState(true);
  const [jobs, setJobs] = useState([]);
  const [stock, setStock] = useState([]);
  const [partners, setPartners] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [activityLog, setActivityLog] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [companyInfo, setCompanyInfo] = useState(DEFAULT_COMPANY_INFO);
  const [salesCatalog, setSalesCatalog] = useState([]);
  const [showJobModal, setShowJobModal] = useState(false);
  const [showPickQuotation, setShowPickQuotation] = useState(false);
  const [showStockModal, setShowStockModal] = useState(false);
  const [showPartnerModal, setShowPartnerModal] = useState(false);
  const [showTransactionModal, setShowTransactionModal] = useState(false);
  const [financeTab, setFinanceTab] = useState('cash'); // 'cash' | 'pnl'
  const [showCustomerModal, setShowCustomerModal] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [showCapitalModal, setShowCapitalModal] = useState(false);
  const [capitalMode, setCapitalMode] = useState('deposit'); // 'deposit' | 'withdraw'
  const [showDividendModal, setShowDividendModal] = useState(false);
  const [customerGuide, setCustomerGuide] = useState(null); // { customerName, systemType }
  const [showDocumentModal, setShowDocumentModal] = useState(false);
  const [defaultDocType, setDefaultDocType] = useState('quotation');
  const [docFilter, setDocFilter] = useState('active'); // 'active' | 'quotation' | 'invoice' | 'receipt' | 'closed'
  const [docSearch, setDocSearch] = useState('');
  const [showDocumentPreview, setShowDocumentPreview] = useState(false);
  const [showCompanySettings, setShowCompanySettings] = useState(false);
  const [previewDoc, setPreviewDoc] = useState(null);
  const [editingItem, setEditingItem] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [j, s, p, t, c, a, d, ci, sc] = await Promise.all([
          window.storage.get('dd5:jobs', true).catch(() => null),
          window.storage.get('dd5:stock', true).catch(() => null),
          window.storage.get('dd5:partners', true).catch(() => null),
          window.storage.get('dd5:transactions', true).catch(() => null),
          window.storage.get('dd5:customers', true).catch(() => null),
          window.storage.get('dd5:activity', true).catch(() => null),
          window.storage.get('dd5:documents', true).catch(() => null),
          window.storage.get('dd5:company', true).catch(() => null),
          window.storage.get('dd5:salesCatalog', true).catch(() => null),
        ]);
        // ✨ Jobs: migration ใส่ stockId ให้ item เบิกสต๊อกเก่า (เพื่อ track ซื้อ/ใช้/เหลือ)
        const stockData = s ? JSON.parse(s.value) : DEFAULT_STOCK;
        let jobsData = j ? JSON.parse(j.value) : DEFAULT_JOBS;
        const jobMig = migrateJobs(jobsData, stockData);
        if (jobMig.changed) {
          jobsData = jobMig.jobs;
          await window.storage.set('dd5:jobs', JSON.stringify(jobsData), true);
          console.log('[Auto-Migration] ใส่ stockId ให้รายการเบิกสต๊อกเก่า');
        }
        setJobs(jobsData);
        setStock(stockData);
        setPartners(p ? JSON.parse(p.value) : DEFAULT_PARTNERS);
        
        // ✨ Transactions: รัน auto-migration แบบเงียบ ๆ
        let txData = t ? JSON.parse(t.value) : DEFAULT_TRANSACTIONS;
        const migrated = migrateTransactions(txData);
        if (migrated.changed) {
          txData = migrated.transactions;
          await window.storage.set('dd5:transactions', JSON.stringify(txData), true);
          console.log(`[Auto-Migration] แก้ ${migrated.summary}`);
        }
        setTransactions(txData);
        
        setCustomers(c ? JSON.parse(c.value) : DEFAULT_CUSTOMERS);
        setActivityLog(a ? JSON.parse(a.value) : []);
        setDocuments(d ? migrateDocuments(JSON.parse(d.value)) : DEFAULT_DOCUMENTS);
        // Migration: ถ้า companyInfo เก่าไม่มี fields ใหม่ ใส่ default ให้
        const ciData = ci ? JSON.parse(ci.value) : DEFAULT_COMPANY_INFO;
        let needsCiSave = false;
        
        if (!ciData.warranty) {
          ciData.warranty = DEFAULT_COMPANY_INFO.warranty;
          needsCiSave = true;
        }
        if (!ciData.specs) {
          ciData.specs = DEFAULT_COMPANY_INFO.specs;
          needsCiSave = true;
        }
        // Force migrate specs (V4): reset ถ้ามี IP65/MDB/สาย 16mm²เก่า/spec ที่ไม่ตรง
        else if (ciData.specs.some(s => 
          (s.id === 's-mdb') ||                                  // มี ตู้ MDB เก่า
          (s.value && s.value.includes('IP65')) ||               // มี IP65 ที่ไหนก็ตาม
          (s.id === 's-ac' && s.value === 'Yasaki THW 16mm²') || // สาย AC default เก่า
          (s.id === 's-dc' && s.value === 'PV1-F 6mm² ทนแดด UV') || // สาย DC ไม่บอกสี
          (s.id === 's-ac' && s.value && s.value.includes('Yasaki 10mm²') && !s.value.includes('เขียวเหลือง')) ||
          (s.id === 's-dc' && s.value && !s.value.includes('ดำ+แดง'))  // DC ไม่บอก ดำ+แดง
        )) {
          ciData.specs = DEFAULT_COMPANY_INFO.specs;
          needsCiSave = true;
        }
        if (!ciData.freebies) {
          ciData.freebies = DEFAULT_COMPANY_INFO.freebies;
          needsCiSave = true;
        }
        if (!ciData.saleSlogan) {
          ciData.saleSlogan = DEFAULT_COMPANY_INFO.saleSlogan;
          needsCiSave = true;
        }
        // บังคับ save กลับถ้ามีการเปลี่ยน
        if (needsCiSave) {
          await window.storage.set('dd5:company', JSON.stringify(ciData), true);
        }
        setCompanyInfo(ciData);
        // Migrate catalog: ถ้าเป็น version เก่า (มีไม่ถึง 10 รายการ) → reset เป็น default ใหม่
        let catalogToUse = sc ? JSON.parse(sc.value) : DEFAULT_SALES_CATALOG;
        const needsMigration = !sc || catalogToUse.length < 10 || !catalogToUse.some(c => c.brand === 'Solis' || c.brand === 'TMDA');
        if (needsMigration) {
          catalogToUse = DEFAULT_SALES_CATALOG;
          await window.storage.set('dd5:salesCatalog', JSON.stringify(DEFAULT_SALES_CATALOG), true);
        }
        setSalesCatalog(catalogToUse);
        if (!j) await window.storage.set('dd5:jobs', JSON.stringify(DEFAULT_JOBS), true);
        if (!s) await window.storage.set('dd5:stock', JSON.stringify(DEFAULT_STOCK), true);
        if (!p) await window.storage.set('dd5:partners', JSON.stringify(DEFAULT_PARTNERS), true);
        if (!t) await window.storage.set('dd5:transactions', JSON.stringify(DEFAULT_TRANSACTIONS), true);
        if (!c) await window.storage.set('dd5:customers', JSON.stringify(DEFAULT_CUSTOMERS), true);
      } catch (e) { console.error(e); }
      finally { setLoading(false); }
    };
    load();
  }, []);

  // === Activity Log Helper ===
  const logActivity = async (action, target, details = '') => {
    const entry = {
      id: `log-${Date.now()}-${Math.random().toString(36).slice(2,7)}`,
      timestamp: new Date().toISOString(),
      userId: currentUser.id,
      userName: currentUser.name,
      action,  // 'add' | 'edit' | 'delete'
      target,  // 'งาน' | 'สต๊อก' | 'ลูกค้า' | 'การเงิน' | 'ผู้ลงทุน'
      details,
    };
    const newLog = [entry, ...activityLog].slice(0, 500); // เก็บแค่ 500 รายการล่าสุด
    setActivityLog(newLog);
    try { await window.storage.set('dd5:activity', JSON.stringify(newLog), true); } catch (e) {}
  };

  const saveJobs = async (data, action, details) => {
    setJobs(data);
    try { await window.storage.set('dd5:jobs', JSON.stringify(data), true); } catch(e){}
    if (action) await logActivity(action, 'งาน', details);
  };
  const saveStock = async (data, action, details) => {
    setStock(data);
    try { await window.storage.set('dd5:stock', JSON.stringify(data), true); } catch(e){}
    if (action) await logActivity(action, 'สต๊อก', details);
  };
  const saveSalesCatalog = async (data, action, details) => {
    setSalesCatalog(data);
    try { await window.storage.set('dd5:salesCatalog', JSON.stringify(data), true); } catch(e){}
    if (action) await logActivity(action, 'แคตตาล็อกขาย', details);
  };
  const savePartners = async (data, action, details) => {
    setPartners(data);
    try { await window.storage.set('dd5:partners', JSON.stringify(data), true); } catch(e){}
    if (action) await logActivity(action, 'ผู้ลงทุน', details);
  };
  const saveTransactions = async (data, action, details) => {
    setTransactions(data);
    try { await window.storage.set('dd5:transactions', JSON.stringify(data), true); } catch(e){}
    if (action) await logActivity(action, 'การเงิน', details);
  };
  const saveCustomers = async (data, action, details) => {
    setCustomers(data);
    try { await window.storage.set('dd5:customers', JSON.stringify(data), true); } catch(e){}
    if (action) await logActivity(action, 'ลูกค้า', details);
  };
  const saveDocuments = async (data, action, details) => {
    setDocuments(data);
    try { await window.storage.set('dd5:documents', JSON.stringify(data), true); } catch(e){}
    if (action) await logActivity(action, 'เอกสาร', details);
  };
  const saveCompanyInfo = async (data) => {
    setCompanyInfo(data);
    try { await window.storage.set('dd5:company', JSON.stringify(data), true); } catch(e){}
    await logActivity('edit', 'ข้อมูลบริษัท', 'แก้ไขข้อมูลบริษัทในใบเสนอราคา/บิล');
  };

  const totalRevenue = jobs.reduce((s, j) => s + (Number(j.salePrice) || 0), 0);
  const totalCost = jobs.reduce((s, j) => s + (Number(j.totalCost) || 0), 0);
  // กำไรสะสม = กำไรติดตั้ง + บริการหลังการขายสุทธิ (ล้างแผง/ซ่อม) — ตรงกับ tx ในการเงิน
  const totalServiceNet = jobs.reduce((s, j) => s + (Array.isArray(j.serviceLog) ? j.serviceLog.reduce((x, l) => x + Number(l.income || 0) - Number(l.cost || 0), 0) : 0), 0);
  const totalProfit = totalRevenue - totalCost + totalServiceNet;
  const completedJobs = jobs.filter(j => j.status === 'completed').length;
  const totalStockValue = stock.filter(s => Number(s.qty) > 0).reduce((sum, s) => sum + Number(s.qty || 0) * Number(s.unitCost || 0), 0);

  const actualInvestments = useMemo(() => {
    // ✨ โครงสร้างใหม่: ทุน = transactions 'เพิ่มทุน'/'ถอนทุน' เท่านั้น (source เดียว)
    // - เพิ่มทุน ทำผ่านปุ่ม "เพิ่มทุน" ใน Dashboard เท่านั้น (แยกขาดจากการซื้อของ)
    // - การซื้อของทุกอย่างใช้เงินบริษัท (ไม่ผูกหุ้นส่วน)
    const inv = {};
    const fromJobs = {};      // ทุนที่ระบุ jobId (data เก่า)
    const fromStock = {};     // (legacy - ไม่ใช้แล้ว คงไว้กัน UI พัง)
    const fromDeposit = {};   // ทุนทั่วไป (ผ่านปุ่มเพิ่มทุน)
    partners.forEach(p => {
      inv[p.id] = 0;
      fromJobs[p.id] = 0;
      fromStock[p.id] = 0;
      fromDeposit[p.id] = 0;
    });
    
    transactions.forEach(t => {
      if (!t.partnerId) return;
      
      // ทุนเข้า
      if (t.type === 'income' && (t.category === 'เพิ่มทุน' || t.category === 'ทุน')) {
        const amt = Number(t.amount || 0);
        if (t.jobId) fromJobs[t.partnerId] = (fromJobs[t.partnerId] || 0) + amt;
        else fromDeposit[t.partnerId] = (fromDeposit[t.partnerId] || 0) + amt;
        inv[t.partnerId] = (inv[t.partnerId] || 0) + amt;
      }
      
      // ถอนทุน
      if (t.type === 'expense' && (t.category === 'ถอนทุน' || t.category === 'คืนทุน')) {
        const amt = Number(t.amount || 0);
        fromDeposit[t.partnerId] = (fromDeposit[t.partnerId] || 0) - amt;
        inv[t.partnerId] = (inv[t.partnerId] || 0) - amt;
      }
    });
    
    return { inv, fromJobs, fromStock, fromDeposit };
  }, [partners, transactions]);

  // 💜 ปันผลสะสม — คำนวณจาก tx 'ปันผล' (source เดียว ตรวจสอบได้)
  const dividendStats = useMemo(() => {
    const byPartner = {};
    partners.forEach(p => { byPartner[p.id] = 0; });
    let total = 0;
    transactions.forEach(t => {
      if (t.type === 'expense' && t.category === 'ปันผล') {
        const amt = Number(t.amount || 0);
        total += amt;
        if (t.partnerId) byPartner[t.partnerId] = (byPartner[t.partnerId] || 0) + amt;
      }
    });
    return { total, byPartner };
  }, [partners, transactions]);

  const fmt = (n) => new Intl.NumberFormat('th-TH', { maximumFractionDigits: 2 }).format(Number(n) || 0);
  const fmt0 = (n) => new Intl.NumberFormat('th-TH', { maximumFractionDigits: 0 }).format(Math.round(Number(n) || 0));

  const resetData = async () => {
    if (!window.confirm('รีเซ็ตข้อมูลทั้งหมดกลับเป็นค่าเริ่มต้น?')) return;
    try {
      await Promise.all([
        window.storage.delete('dd5:jobs', true),
        window.storage.delete('dd5:stock', true),
        window.storage.delete('dd5:partners', true),
        window.storage.delete('dd5:transactions', true),
        window.storage.delete('dd5:customers', true),
        window.storage.delete('dd5:activity', true),
      ]);
      window.location.reload();
    } catch (e) { console.error(e); }
  };

  // === Export to Excel for Tax ===
  const exportToExcel = () => {
    if (!window.XLSX) {
      alert('ห้องสมุด Excel กำลังโหลด กรุณาลองใหม่อีกครั้งใน 2-3 วินาที');
      return;
    }
    const XLSX = window.XLSX;
    const wb = XLSX.utils.book_new();

    // ============== Helpers ==============
    const partnerName = (id) => (partners.find(p => p.id === id) || {}).name || '';
    
    // Style helpers (xlsx-js-style format)
    const styles = {
      title: { font: { bold: true, sz: 14, color: { rgb: 'FFFFFF' } }, fill: { fgColor: { rgb: 'D97706' } }, alignment: { horizontal: 'center', vertical: 'center' } },
      sectionHeader: { font: { bold: true, sz: 11, color: { rgb: '7B0000' } }, fill: { fgColor: { rgb: 'FCE4D6' } }, alignment: { horizontal: 'left' } },
      tableHeader: { font: { bold: true, sz: 11, color: { rgb: 'FFFFFF' } }, fill: { fgColor: { rgb: '305496' } }, alignment: { horizontal: 'center', vertical: 'center' }, border: { top: { style: 'thin' }, bottom: { style: 'thin' }, left: { style: 'thin' }, right: { style: 'thin' } } },
      cell: { font: { sz: 10 }, alignment: { vertical: 'center' }, border: { top: { style: 'thin', color: { rgb: 'CCCCCC' } }, bottom: { style: 'thin', color: { rgb: 'CCCCCC' } }, left: { style: 'thin', color: { rgb: 'CCCCCC' } }, right: { style: 'thin', color: { rgb: 'CCCCCC' } } } },
      cellMoney: { font: { sz: 10 }, alignment: { horizontal: 'right', vertical: 'center' }, numFmt: '#,##0.00', border: { top: { style: 'thin', color: { rgb: 'CCCCCC' } }, bottom: { style: 'thin', color: { rgb: 'CCCCCC' } }, left: { style: 'thin', color: { rgb: 'CCCCCC' } }, right: { style: 'thin', color: { rgb: 'CCCCCC' } } } },
      cellCenter: { font: { sz: 10 }, alignment: { horizontal: 'center', vertical: 'center' }, border: { top: { style: 'thin', color: { rgb: 'CCCCCC' } }, bottom: { style: 'thin', color: { rgb: 'CCCCCC' } }, left: { style: 'thin', color: { rgb: 'CCCCCC' } }, right: { style: 'thin', color: { rgb: 'CCCCCC' } } } },
      total: { font: { bold: true, sz: 11 }, fill: { fgColor: { rgb: 'FED7AA' } }, alignment: { horizontal: 'right' }, numFmt: '#,##0.00', border: { top: { style: 'medium' }, bottom: { style: 'medium' }, left: { style: 'medium' }, right: { style: 'medium' } } },
      income: { font: { sz: 10, bold: true, color: { rgb: '065F46' } }, fill: { fgColor: { rgb: 'D1FAE5' } }, alignment: { horizontal: 'right' }, numFmt: '#,##0.00' },
      expense: { font: { sz: 10, bold: true, color: { rgb: '991B1B' } }, fill: { fgColor: { rgb: 'FEE2E2' } }, alignment: { horizontal: 'right' }, numFmt: '#,##0.00' },
      profit: { font: { sz: 12, bold: true, color: { rgb: 'D97706' } }, fill: { fgColor: { rgb: 'FEF3C7' } }, alignment: { horizontal: 'right' }, numFmt: '#,##0.00', border: { top: { style: 'medium' }, bottom: { style: 'medium' }, left: { style: 'medium' }, right: { style: 'medium' } } },
    };

    const setCell = (ws, addr, value, style) => {
      ws[addr] = { v: value, t: typeof value === 'number' ? 'n' : 's', s: style };
    };

    const setRange = (ws, range) => {
      ws['!ref'] = range;
    };

    // ============== Sheet 1: ภาพรวม ==============
    const overview = {};
    overview['B2'] = { v: 'D.D. SOLUTION', t: 's', s: { font: { bold: true, sz: 18, color: { rgb: 'D97706' } } } };
    overview['B3'] = { v: 'รายงานสรุปธุรกิจ - Export โดย ' + currentUser.name + ' · ' + new Date().toLocaleDateString('th-TH'), t: 's', s: { font: { sz: 10, italic: true, color: { rgb: '78716C' } } } };

    // Section: เงินลงทุน
    setCell(overview, 'B5', '💰 เงินลงทุน', styles.sectionHeader);
    setCell(overview, 'C5', '', styles.sectionHeader);
    
    const totalInv = partners.reduce((s, p) => s + (actualInvestments.inv[p.id] || 0), 0);
    let r = 6;
    partners.forEach(p => {
      setCell(overview, `B${r}`, p.name, styles.cell);
      setCell(overview, `C${r}`, actualInvestments.inv[p.id] || 0, styles.cellMoney);
      r++;
    });
    setCell(overview, `B${r}`, 'เงินทุนรวม', { ...styles.total, alignment: { horizontal: 'left' } });
    setCell(overview, `C${r}`, totalInv, styles.total);
    r += 2;

    // Section: ผลประกอบการ
    setCell(overview, `B${r}`, '📊 ผลประกอบการ', styles.sectionHeader);
    setCell(overview, `C${r}`, '', styles.sectionHeader);
    r++;
    setCell(overview, `B${r}`, 'รายได้รวม', styles.cell);
    setCell(overview, `C${r}`, totalRevenue, styles.income);
    r++;
    setCell(overview, `B${r}`, 'รายจ่ายรวม', styles.cell);
    setCell(overview, `C${r}`, totalCost, styles.expense);
    r++;
    setCell(overview, `B${r}`, 'กำไรสุทธิ', { ...styles.profit, alignment: { horizontal: 'left' } });
    setCell(overview, `C${r}`, totalProfit, styles.profit);
    r += 2;

    // Section: สต๊อกคงเหลือ
    const stockRemaining = stock.filter(s => Number(s.qty) > 0);
    if (stockRemaining.length > 0) {
      setCell(overview, `B${r}`, '📦 สต๊อกคงเหลือ', styles.sectionHeader);
      setCell(overview, `C${r}`, '', styles.sectionHeader);
      r++;
      stockRemaining.forEach(s => {
        setCell(overview, `B${r}`, `${s.name} (${s.qty} ${s.unit || 'ชิ้น'})`, styles.cell);
        setCell(overview, `C${r}`, Number(s.qty) * Number(s.unitCost), styles.cellMoney);
        r++;
      });
      const totalStock = stockRemaining.reduce((s, i) => s + Number(i.qty) * Number(i.unitCost), 0);
      setCell(overview, `B${r}`, 'มูลค่าสต๊อกรวม', { ...styles.total, alignment: { horizontal: 'left' } });
      setCell(overview, `C${r}`, totalStock, styles.total);
      r += 2;
    }

    // Section: 💵 เงินสดในมือ (สมการเต็มตาม Dashboard)
    const ovStockVal = stock.filter(s => Number(s.qty) > 0).reduce((s, i) => s + Number(i.qty) * Number(i.unitCost), 0);
    const ovCash = totalInv + totalProfit - dividendStats.total - ovStockVal;
    setCell(overview, `B${r}`, '💵 เงินสดในมือ', styles.sectionHeader);
    setCell(overview, `C${r}`, '', styles.sectionHeader);
    r++;
    setCell(overview, `B${r}`, 'เงินทุนรวม', styles.cell);
    setCell(overview, `C${r}`, totalInv, styles.cellMoney);
    r++;
    setCell(overview, `B${r}`, '+ กำไรสะสม', styles.cell);
    setCell(overview, `C${r}`, totalProfit, styles.income);
    r++;
    if (dividendStats.total > 0) {
      setCell(overview, `B${r}`, '− ปันผลจ่ายแล้ว', styles.cell);
      setCell(overview, `C${r}`, dividendStats.total, styles.expense);
      r++;
    }
    setCell(overview, `B${r}`, '− มูลค่าสต๊อก', styles.cell);
    setCell(overview, `C${r}`, ovStockVal, styles.expense);
    r++;
    setCell(overview, `B${r}`, 'เงินสดคงเหลือ', { ...styles.profit, alignment: { horizontal: 'left' } });
    setCell(overview, `C${r}`, ovCash, styles.profit);

    overview['!ref'] = 'A1:D' + (r + 2);
    overview['!cols'] = [{ wch: 2 }, { wch: 35 }, { wch: 18 }, { wch: 15 }];
    overview['!rows'] = [{ hpt: 10 }, { hpt: 28 }];
    XLSX.utils.book_append_sheet(wb, overview, 'ภาพรวม');

    // ============== Sheet per Job ==============
    jobs.forEach((job, jobIdx) => {
      const ws = {};
      const sheetName = `งาน ${jobIdx + 1}`;
      const jobLabel = `${job.customer} (${job.date})`;

      // Title
      ws['B2'] = { v: 'D.D. SOLUTION', t: 's', s: { font: { bold: true, sz: 16, color: { rgb: 'D97706' } } } };
      ws['B3'] = { v: jobLabel, t: 's', s: { font: { sz: 11, italic: true } } };
      if (job.location) ws['B4'] = { v: '📍 ' + job.location, t: 's', s: { font: { sz: 9, color: { rgb: '78716C' } } } };

      // Section: รายจ่าย (ต้นทุน)
      setCell(ws, 'B6', 'รายจ่าย (ต้นทุน)', styles.sectionHeader);
      for (let c = 2; c <= 9; c++) setCell(ws, XLSX.utils.encode_cell({ r: 5, c }), '', styles.sectionHeader);

      // Table headers
      const headers = ['#', 'รายการ', 'หมวดหมู่', 'ผู้รับผิดชอบ', 'จำนวน', 'ราคา', 'VAT(7%)', 'จำนวนเงิน (฿)', 'หมายเหตุ'];
      headers.forEach((h, i) => {
        setCell(ws, XLSX.utils.encode_cell({ r: 6, c: i + 1 }), h, styles.tableHeader);
      });

      // Items
      let row = 7;
      let itemNum = 1;
      let totalCostAll = 0;
      const partnerCostMap = { 'อาม': 0, 'โฟน': 0, 'พ่อ': 0, 'สต๊อก': 0 };
      const categoryCostMap = {};

      Object.entries(job.costsByCategory || {}).forEach(([catId, items]) => {
        const catLabel = (COST_CATEGORIES.find(c => c.id === catId) || { label: catId }).label;
        items.forEach(item => {
          const amount = Number(item.amount || 0);
          const isStock = !!item.stockId;
          
          setCell(ws, `B${row}`, itemNum, styles.cellCenter);
          setCell(ws, `C${row}`, item.item || '', styles.cell);
          setCell(ws, `D${row}`, catLabel, styles.cell);
          setCell(ws, `E${row}`, isStock ? 'สต๊อก' : '', styles.cellCenter);
          setCell(ws, `F${row}`, item.qtyUsed || 1, styles.cellCenter);
          setCell(ws, `G${row}`, item.qtyUsed ? amount / item.qtyUsed : amount, styles.cellMoney);
          setCell(ws, `H${row}`, '', styles.cellCenter);
          setCell(ws, `I${row}`, amount, styles.cellMoney);
          setCell(ws, `J${row}`, isStock ? 'เบิกจากสต๊อก' : '', styles.cell);

          totalCostAll += amount;
          if (isStock) partnerCostMap['สต๊อก'] += amount;
          categoryCostMap[catLabel] = (categoryCostMap[catLabel] || 0) + amount;
          itemNum++;
          row++;
        });
      });

      // Investments map (who paid)
      Object.entries(job.investments || {}).forEach(([pid, amt]) => {
        const name = partnerName(pid);
        if (partnerCostMap.hasOwnProperty(name)) {
          partnerCostMap[name] = Number(amt);
        }
      });

      // ต้นทุนรวม row
      row++;
      setCell(ws, `H${row}`, 'ต้นทุนรวม', { ...styles.total, alignment: { horizontal: 'right' } });
      setCell(ws, `I${row}`, totalCostAll, styles.total);
      row += 2;

      // Section: ราคาขาย
      setCell(ws, `C${row}`, 'ราคาขาย', styles.cell);
      setCell(ws, `D${row}`, Number(job.originalPrice || job.salePrice || 0), styles.cellMoney);
      row++;
      if (job.discount) {
        setCell(ws, `C${row}`, 'ส่วนลด', styles.cell);
        setCell(ws, `D${row}`, Number(job.discount), styles.cellMoney);
        row++;
      }
      setCell(ws, `C${row}`, 'รายรับ', { ...styles.cell, font: { bold: true, sz: 10 } });
      setCell(ws, `D${row}`, Number(job.salePrice), { ...styles.income });
      row++;
      setCell(ws, `C${row}`, 'กำไร', { ...styles.profit, alignment: { horizontal: 'left' } });
      setCell(ws, `D${row}`, Number(job.salePrice) - totalCostAll, styles.profit);
      row += 2;

      // Section: แบ่งตามคน
      setCell(ws, `B${row}`, '👥 ผู้รับผิดชอบเงินทุน', styles.sectionHeader);
      setCell(ws, `C${row}`, '', styles.sectionHeader);
      setCell(ws, `D${row}`, '', styles.sectionHeader);
      row++;
      ['อาม', 'โฟน', 'พ่อ', 'สต๊อก'].forEach(name => {
        if (partnerCostMap[name] > 0) {
          setCell(ws, `C${row}`, name, styles.cell);
          setCell(ws, `D${row}`, partnerCostMap[name], styles.cellMoney);
          row++;
        }
      });
      const totalByPerson = Object.values(partnerCostMap).reduce((s, v) => s + v, 0);
      setCell(ws, `C${row}`, 'รวม', { ...styles.total, alignment: { horizontal: 'left' } });
      setCell(ws, `D${row}`, totalByPerson, styles.total);
      row += 2;

      // Section: แบ่งตามหมวด
      setCell(ws, `B${row}`, '📊 แยกตามหมวดหมู่', styles.sectionHeader);
      setCell(ws, `C${row}`, '', styles.sectionHeader);
      setCell(ws, `D${row}`, '', styles.sectionHeader);
      row++;
      Object.entries(categoryCostMap).forEach(([cat, amt]) => {
        setCell(ws, `C${row}`, cat, styles.cell);
        setCell(ws, `D${row}`, amt, styles.cellMoney);
        row++;
      });
      const totalByCat = Object.values(categoryCostMap).reduce((s, v) => s + v, 0);
      setCell(ws, `C${row}`, 'รวม', { ...styles.total, alignment: { horizontal: 'left' } });
      setCell(ws, `D${row}`, totalByCat, styles.total);

      ws['!ref'] = 'A1:K' + (row + 2);
      ws['!cols'] = [
        { wch: 2 },   // A
        { wch: 4 },   // B (#)
        { wch: 50 },  // C (รายการ)
        { wch: 14 },  // D (หมวดหมู่)
        { wch: 12 },  // E (ผู้รับผิดชอบ)
        { wch: 8 },   // F (จำนวน)
        { wch: 12 },  // G (ราคา)
        { wch: 10 },  // H (VAT)
        { wch: 14 },  // I (รวม)
        { wch: 22 },  // J (หมายเหตุ)
      ];
      
      // Merged cells for section headers
      ws['!merges'] = ws['!merges'] || [];
      
      XLSX.utils.book_append_sheet(wb, ws, sheetName);
    });

    // ============== Sheet: สต๊อก ==============
    const stockWs = {};
    stockWs['B2'] = { v: '📦 สต๊อกสินค้า', t: 's', s: { font: { bold: true, sz: 16, color: { rgb: 'D97706' } } } };
    stockWs['B3'] = { v: `อัพเดท: ${new Date().toLocaleDateString('th-TH')}`, t: 's', s: { font: { sz: 9, italic: true, color: { rgb: '78716C' } } } };

    const stockHeaders = ['ผู้รับผิดชอบ', 'รายการ', 'หมวด', 'ซื้อ', 'ใช้ไป', 'เหลือ', 'หน่วย', 'ราคา/หน่วย', 'มูลค่ารวม', 'หมายเหตุ'];
    stockHeaders.forEach((h, i) => {
      setCell(stockWs, XLSX.utils.encode_cell({ r: 4, c: i + 1 }), h, styles.tableHeader);
    });

    let sr = 6;
    let totalStockValue = 0;
    
    // คำนวณ "ใช้ไป" จริง: รวม qtyUsed จากทุกงานที่เบิก stockId นี้
    const usedByStockId = {};
    jobs.forEach(job => {
      Object.values(job.costsByCategory || {}).forEach(items => {
        (items || []).forEach(item => {
          if (item.stockId) {
            usedByStockId[item.stockId] = (usedByStockId[item.stockId] || 0) + Number(item.qtyUsed || item.qty || 0);
          }
        });
      });
    });
    
    // Active stock first
    [...stock].sort((a, b) => Number(b.qty) - Number(a.qty)).forEach(item => {
      const remaining = Number(item.qty);
      const used = usedByStockId[item.id] || 0;
      const bought = remaining + used;
      const value = remaining * Number(item.unitCost);
      const isHistory = remaining === 0;
      
      const cellStyle = isHistory ? { ...styles.cell, font: { sz: 9, color: { rgb: 'A8A29E' } } } : styles.cell;
      const moneyStyle = isHistory ? { ...styles.cellMoney, font: { sz: 9, color: { rgb: 'A8A29E' } } } : styles.cellMoney;
      
      setCell(stockWs, `B${sr}`, item.owner || 'บริษัท', cellStyle);
      setCell(stockWs, `C${sr}`, item.name, cellStyle);
      setCell(stockWs, `D${sr}`, (STOCK_CATEGORIES.find(c => c.id === item.category) || { label: item.category }).label, cellStyle);
      setCell(stockWs, `E${sr}`, bought, { ...styles.cellCenter, font: { sz: 10 } });
      setCell(stockWs, `F${sr}`, used, used > 0 ? { ...styles.cellCenter, font: { sz: 10, color: { rgb: '991B1B' } } } : { ...styles.cellCenter, font: { sz: 9, color: { rgb: 'A8A29E' } } });
      setCell(stockWs, `G${sr}`, remaining, isHistory ? { ...styles.cellCenter, font: { sz: 9, color: { rgb: 'A8A29E' } } } : { ...styles.cellCenter, font: { bold: true, sz: 10, color: { rgb: '059669' } } });
      setCell(stockWs, `H${sr}`, item.unit || 'ชิ้น', styles.cellCenter);
      setCell(stockWs, `I${sr}`, Number(item.unitCost), moneyStyle);
      setCell(stockWs, `J${sr}`, value, value > 0 ? { ...styles.cellMoney, font: { bold: true, sz: 10, color: { rgb: 'D97706' } } } : moneyStyle);
      setCell(stockWs, `K${sr}`, item.note || '', { ...cellStyle, font: { sz: 9 } });
      
      totalStockValue += value;
      sr++;
    });

    // Total
    sr++;
    setCell(stockWs, `B${sr}`, 'มูลค่าสต๊อกรวม', { ...styles.total, alignment: { horizontal: 'left' } });
    for (let c = 2; c <= 8; c++) setCell(stockWs, XLSX.utils.encode_cell({ r: sr - 1, c }), '', { ...styles.total, alignment: { horizontal: 'left' } });
    setCell(stockWs, `J${sr}`, totalStockValue, styles.total);

    stockWs['!ref'] = 'A1:L' + (sr + 1);
    stockWs['!cols'] = [
      { wch: 2 }, { wch: 14 }, { wch: 30 }, { wch: 12 }, { wch: 8 }, { wch: 8 },
      { wch: 8 }, { wch: 10 }, { wch: 12 }, { wch: 14 }, { wch: 30 },
    ];
    XLSX.utils.book_append_sheet(wb, stockWs, 'สต๊อก');

    // ============== Sheet: ผู้ลงทุน ==============
    const partnerWs = {};
    partnerWs['B2'] = { v: '👥 ผู้ลงทุน', t: 's', s: { font: { bold: true, sz: 16, color: { rgb: 'D97706' } } } };

    const partnerHeaders = ['ชื่อ', 'บทบาท', 'ลงทุนจากงาน', 'ลงทุนทั่วไป', 'รวมสะสม', '% สัดส่วน', 'ปันผลรับแล้ว', 'บัญชี'];
    partnerHeaders.forEach((h, i) => {
      setCell(partnerWs, XLSX.utils.encode_cell({ r: 3, c: i + 1 }), h, styles.tableHeader);
    });

    let pr = 5;
    const totalAllInv = partners.reduce((s, p) => s + (actualInvestments.inv[p.id] || 0), 0);
    partners.forEach(p => {
      const fromJobs = actualInvestments.fromJobs[p.id] || 0;
      const fromDeposit = actualInvestments.fromDeposit[p.id] || 0;
      const total = actualInvestments.inv[p.id] || 0;
      const pct = totalAllInv > 0 ? (total / totalAllInv * 100) : 0;
      const divReceived = dividendStats.byPartner[p.id] || 0;

      setCell(partnerWs, `B${pr}`, p.name, { ...styles.cell, font: { bold: true, sz: 11 } });
      setCell(partnerWs, `C${pr}`, p.role || '', { ...styles.cell, font: { sz: 9 } });
      setCell(partnerWs, `D${pr}`, fromJobs, styles.cellMoney);
      setCell(partnerWs, `E${pr}`, fromDeposit, styles.cellMoney);
      setCell(partnerWs, `F${pr}`, total, { ...styles.cellMoney, font: { bold: true, sz: 11, color: { rgb: 'D97706' } } });
      setCell(partnerWs, `G${pr}`, pct / 100, { ...styles.cellMoney, numFmt: '0.0%' });
      setCell(partnerWs, `H${pr}`, divReceived, { ...styles.cellMoney, font: { sz: 10, color: { rgb: '7C3AED' } } });
      setCell(partnerWs, `I${pr}`, p.bankAccount || '-', { ...styles.cell, font: { sz: 9 } });
      pr++;
    });
    setCell(partnerWs, `B${pr}`, 'รวม', { ...styles.total, alignment: { horizontal: 'left' } });
    setCell(partnerWs, `D${pr}`, partners.reduce((s, p) => s + (actualInvestments.fromJobs[p.id] || 0), 0), styles.total);
    setCell(partnerWs, `E${pr}`, partners.reduce((s, p) => s + (actualInvestments.fromDeposit[p.id] || 0), 0), styles.total);
    setCell(partnerWs, `F${pr}`, totalAllInv, styles.total);
    setCell(partnerWs, `G${pr}`, 1, { ...styles.total, numFmt: '0.0%' });
    setCell(partnerWs, `H${pr}`, dividendStats.total, styles.total);

    partnerWs['!ref'] = 'A1:I' + (pr + 1);
    partnerWs['!cols'] = [
      { wch: 2 }, { wch: 12 }, { wch: 28 }, { wch: 14 }, { wch: 14 }, { wch: 14 }, { wch: 10 }, { wch: 14 }, { wch: 35 },
    ];
    XLSX.utils.book_append_sheet(wb, partnerWs, 'ผู้ลงทุน');

    // ============== Sheet: การเงิน (ทุกรายการ — ตรวจสอบได้) ==============
    const finWs = {};
    finWs['B2'] = { v: '💵 รายรับ-รายจ่าย ทั้งหมด', t: 's', s: { font: { bold: true, sz: 16, color: { rgb: 'D97706' } } } };
    finWs['B3'] = { v: `${transactions.length} รายการ · Export โดย ${currentUser.name} · ${new Date().toLocaleDateString('th-TH')}`, t: 's', s: { font: { sz: 9, italic: true, color: { rgb: '78716C' } } } };

    const finHeaders = ['วันที่', 'ประเภท', 'หมวด', 'รายละเอียด', 'หุ้นส่วน', 'งาน', 'รายรับ (฿)', 'รายจ่าย (฿)', 'สร้างโดย'];
    finHeaders.forEach((h, i) => {
      setCell(finWs, XLSX.utils.encode_cell({ r: 4, c: i + 1 }), h, styles.tableHeader);
    });

    // สีพื้นตามประเภท (ตรงกับในแอป)
    const finCatFill = (t) => {
      if (t.type === 'income' && t.category === 'รายได้จากงาน') return 'D1FAE5';      // เขียว
      if (t.type === 'income' && (t.category === 'เพิ่มทุน' || t.category === 'ทุน')) return 'DBEAFE'; // น้ำเงิน
      if (t.type === 'expense' && t.category === 'ต้นทุนสต๊อก') return 'FEF3C7';      // เหลือง
      if (t.type === 'expense' && t.category === 'ต้นทุนงาน') return 'FEE2E2';        // แดง
      if (t.type === 'expense' && t.category === 'ปันผล') return 'EDE9FE';            // ม่วง violet
      if (t.type === 'expense' && (t.category === 'ถอนทุน' || t.category === 'คืนทุน')) return 'F3E8FF'; // ม่วง
      return 'FFFFFF';
    };
    const thinB = { top: { style: 'thin', color: { rgb: 'CCCCCC' } }, bottom: { style: 'thin', color: { rgb: 'CCCCCC' } }, left: { style: 'thin', color: { rgb: 'CCCCCC' } }, right: { style: 'thin', color: { rgb: 'CCCCCC' } } };

    let fr = 6;
    let finIn = 0, finOut = 0;
    [...transactions].sort((a, b) => (b.date || '').localeCompare(a.date || '')).forEach(t => {
      const fill = { fgColor: { rgb: finCatFill(t) } };
      const base = { font: { sz: 10 }, fill, border: thinB, alignment: { vertical: 'center' } };
      const partner = partners.find(p => p.id === t.partnerId);
      const job = jobs.find(j => j.id === t.jobId);
      const amt = Number(t.amount || 0);
      if (t.type === 'income') finIn += amt; else finOut += amt;

      setCell(finWs, `B${fr}`, t.date || '', { ...base, alignment: { horizontal: 'center', vertical: 'center' } });
      setCell(finWs, `C${fr}`, t.type === 'income' ? '↙ รับ' : '↗ จ่าย', { ...base, alignment: { horizontal: 'center', vertical: 'center' }, font: { sz: 10, bold: true, color: { rgb: t.type === 'income' ? '065F46' : '991B1B' } } });
      setCell(finWs, `D${fr}`, t.category || '', base);
      setCell(finWs, `E${fr}`, t.description || '', { ...base, alignment: { wrapText: true, vertical: 'center' } });
      setCell(finWs, `F${fr}`, partner?.name || '-', { ...base, alignment: { horizontal: 'center', vertical: 'center' } });
      setCell(finWs, `G${fr}`, job?.customer || '-', { ...base, font: { sz: 9 } });
      setCell(finWs, `H${fr}`, t.type === 'income' ? amt : '', { ...base, alignment: { horizontal: 'right', vertical: 'center' }, numFmt: '#,##0.00', font: { sz: 10, bold: true, color: { rgb: '065F46' } } });
      setCell(finWs, `I${fr}`, t.type === 'expense' ? amt : '', { ...base, alignment: { horizontal: 'right', vertical: 'center' }, numFmt: '#,##0.00', font: { sz: 10, bold: true, color: { rgb: '991B1B' } } });
      setCell(finWs, `J${fr}`, t.createdBy || '-', { ...base, font: { sz: 8, color: { rgb: '78716C' } } });
      fr++;
    });

    // สรุปท้ายตาราง
    fr++;
    setCell(finWs, `B${fr}`, 'รวมทั้งหมด', { ...styles.total, alignment: { horizontal: 'left' } });
    for (let c = 2; c <= 6; c++) setCell(finWs, XLSX.utils.encode_cell({ r: fr - 1, c }), '', styles.total);
    setCell(finWs, `H${fr}`, finIn, { ...styles.total, font: { bold: true, sz: 11, color: { rgb: '065F46' } } });
    setCell(finWs, `I${fr}`, finOut, { ...styles.total, font: { bold: true, sz: 11, color: { rgb: '991B1B' } } });
    setCell(finWs, `J${fr}`, '', styles.total);
    fr++;
    setCell(finWs, `B${fr}`, 'ส่วนต่าง (เข้า − ออก)', { ...styles.profit, alignment: { horizontal: 'left' } });
    setCell(finWs, `H${fr}`, finIn - finOut, styles.profit);

    finWs['!ref'] = 'A1:K' + (fr + 1);
    finWs['!cols'] = [
      { wch: 2 }, { wch: 11 }, { wch: 8 }, { wch: 13 }, { wch: 45 }, { wch: 9 }, { wch: 20 }, { wch: 13 }, { wch: 13 }, { wch: 16 },
    ];
    XLSX.utils.book_append_sheet(wb, finWs, 'การเงิน');

    // ============== Sheet: ลูกค้า ==============
    if (customers.length > 0) {
      const custWs = {};
      custWs['B2'] = { v: '👤 ลูกค้า', t: 's', s: { font: { bold: true, sz: 16, color: { rgb: 'D97706' } } } };

      const custHeaders = ['ชื่อ', 'เบอร์โทร', 'ที่อยู่', 'วันติดตั้ง', 'ระบบที่ติดตั้ง', 'รับประกัน', 'หมายเหตุ'];
      custHeaders.forEach((h, i) => {
        setCell(custWs, XLSX.utils.encode_cell({ r: 3, c: i + 1 }), h, styles.tableHeader);
      });

      let cr = 5;
      customers.forEach(c => {
        setCell(custWs, `B${cr}`, c.name || '', { ...styles.cell, font: { bold: true, sz: 11 } });
        setCell(custWs, `C${cr}`, c.phone || '', styles.cell);
        setCell(custWs, `D${cr}`, c.address || '', { ...styles.cell, alignment: { wrapText: true, vertical: 'top' } });
        setCell(custWs, `E${cr}`, c.installDate || '', styles.cellCenter);
        setCell(custWs, `F${cr}`, c.system || '', { ...styles.cell, font: { sz: 9 } });
        setCell(custWs, `G${cr}`, c.warranty || '', { ...styles.cell, font: { sz: 9 } });
        setCell(custWs, `H${cr}`, c.note || '', { ...styles.cell, font: { sz: 9, italic: true } });
        cr++;
      });

      custWs['!ref'] = 'A1:I' + (cr + 1);
      custWs['!cols'] = [
        { wch: 2 }, { wch: 22 }, { wch: 14 }, { wch: 40 }, { wch: 12 }, { wch: 35 }, { wch: 35 }, { wch: 25 },
      ];
      XLSX.utils.book_append_sheet(wb, custWs, 'ลูกค้า');
    }

    // ============== Sheet: บัญชี (รายรับ-รายจ่าย) ==============
    const txWs = {};
    txWs['B2'] = { v: '💰 บัญชีรายรับ-รายจ่าย', t: 's', s: { font: { bold: true, sz: 16, color: { rgb: 'D97706' } } } };
    txWs['B3'] = { v: 'สำหรับยื่นภาษีประจำปี', t: 's', s: { font: { sz: 10, italic: true, color: { rgb: '78716C' } } } };

    const txHeaders = ['วันที่', 'ประเภท', 'หมวดหมู่', 'รายละเอียด', 'จำนวน (฿)', 'งาน', 'คน'];
    txHeaders.forEach((h, i) => {
      setCell(txWs, XLSX.utils.encode_cell({ r: 4, c: i + 1 }), h, styles.tableHeader);
    });

    let tr = 6;
    const sortedTx = [...transactions].sort((a, b) => (a.date > b.date ? 1 : -1));
    let txIncome = 0, txExpense = 0;
    sortedTx.forEach(t => {
      const isIncome = t.type === 'income';
      setCell(txWs, `B${tr}`, t.date, styles.cellCenter);
      setCell(txWs, `C${tr}`, isIncome ? 'รายรับ' : 'รายจ่าย', { ...styles.cellCenter, font: { bold: true, sz: 10, color: { rgb: isIncome ? '065F46' : '991B1B' } } });
      setCell(txWs, `D${tr}`, t.category || '', styles.cell);
      setCell(txWs, `E${tr}`, t.description || '', { ...styles.cell, font: { sz: 9 } });
      setCell(txWs, `F${tr}`, Number(t.amount), isIncome ? styles.income : styles.expense);
      setCell(txWs, `G${tr}`, jobs.find(j => j.id === t.jobId)?.customer || '-', { ...styles.cellCenter, font: { sz: 9 } });
      setCell(txWs, `H${tr}`, partnerName(t.partnerId) || '-', { ...styles.cellCenter, font: { sz: 9 } });

      if (isIncome) txIncome += Number(t.amount);
      else txExpense += Number(t.amount);
      tr++;
    });

    tr++;
    setCell(txWs, `D${tr}`, 'รายรับรวม', { ...styles.total, alignment: { horizontal: 'right' } });
    setCell(txWs, `F${tr}`, txIncome, { ...styles.income, font: { bold: true, sz: 11, color: { rgb: '065F46' } } });
    tr++;
    setCell(txWs, `D${tr}`, 'รายจ่ายรวม', { ...styles.total, alignment: { horizontal: 'right' } });
    setCell(txWs, `F${tr}`, txExpense, { ...styles.expense, font: { bold: true, sz: 11, color: { rgb: '991B1B' } } });
    tr++;
    setCell(txWs, `D${tr}`, 'คงเหลือ (กระแสเงินสด)', { ...styles.total, alignment: { horizontal: 'right' } });
    setCell(txWs, `F${tr}`, txIncome - txExpense, styles.profit);

    txWs['!ref'] = 'A1:I' + (tr + 1);
    txWs['!cols'] = [
      { wch: 2 }, { wch: 12 }, { wch: 10 }, { wch: 16 }, { wch: 50 }, { wch: 14 }, { wch: 18 }, { wch: 12 },
    ];
    XLSX.utils.book_append_sheet(wb, txWs, 'บัญชี');

    // ============== Save ==============
    const fileName = `DD_Solution_${new Date().toISOString().split('T')[0]}.xlsx`;
    XLSX.writeFile(wb, fileName);
    logActivity('export', 'ระบบ', `ดาวน์โหลด Excel: ${fileName}`);
  };

  // ============== 📊 Export แฟ้มงาน (รายงานครบทุกมิติ ต่องาน 1 ไฟล์) ==============
  const exportJobToExcel = (job) => {
    if (!window.XLSX) { alert('ห้องสมุด Excel กำลังโหลด กรุณาลองใหม่ใน 2-3 วินาที'); return; }
    const XLSX = window.XLSX;
    const wb = XLSX.utils.book_new();
    const thin = { top: { style: 'thin', color: { rgb: 'CCCCCC' } }, bottom: { style: 'thin', color: { rgb: 'CCCCCC' } }, left: { style: 'thin', color: { rgb: 'CCCCCC' } }, right: { style: 'thin', color: { rgb: 'CCCCCC' } } };
    const S = {
      section: { font: { bold: true, sz: 11, color: { rgb: '7B0000' } }, fill: { fgColor: { rgb: 'FCE4D6' } } },
      th: { font: { bold: true, sz: 10, color: { rgb: 'FFFFFF' } }, fill: { fgColor: { rgb: '305496' } }, alignment: { horizontal: 'center', vertical: 'center' }, border: thin },
      cell: { font: { sz: 10 }, alignment: { vertical: 'center' }, border: thin },
      money: { font: { sz: 10 }, alignment: { horizontal: 'right', vertical: 'center' }, numFmt: '#,##0.00', border: thin },
      center: { font: { sz: 10 }, alignment: { horizontal: 'center', vertical: 'center' }, border: thin },
      total: { font: { bold: true, sz: 11 }, fill: { fgColor: { rgb: 'FED7AA' } }, alignment: { horizontal: 'right' }, numFmt: '#,##0.00', border: { top: { style: 'medium' }, bottom: { style: 'medium' }, left: { style: 'medium' }, right: { style: 'medium' } } },
      profit: { font: { sz: 12, bold: true, color: { rgb: 'D97706' } }, fill: { fgColor: { rgb: 'FEF3C7' } }, alignment: { horizontal: 'right' }, numFmt: '#,##0.00', border: { top: { style: 'medium' }, bottom: { style: 'medium' }, left: { style: 'medium' }, right: { style: 'medium' } } },
      green: { font: { sz: 10, bold: true, color: { rgb: '065F46' } }, alignment: { horizontal: 'right' }, numFmt: '#,##0.00', border: thin },
      red: { font: { sz: 10, bold: true, color: { rgb: '991B1B' } }, alignment: { horizontal: 'right' }, numFmt: '#,##0.00', border: thin },
    };
    const ws = {};
    const set = (addr, v, s) => { ws[addr] = { v, t: typeof v === 'number' ? 'n' : 's', s }; };
    let r = 2;

    // ===== Header =====
    set(`B${r}`, `D.D. SOLUTION — แฟ้มงาน`, { font: { bold: true, sz: 16, color: { rgb: 'D97706' } } }); r++;
    set(`B${r}`, `Export โดย ${currentUser.name} · ${new Date().toLocaleDateString('th-TH')}`, { font: { sz: 9, italic: true, color: { rgb: '78716C' } } }); r += 2;

    // ===== 1. ข้อมูลงาน =====
    set(`B${r}`, '📋 ข้อมูลงาน', S.section); set(`C${r}`, '', S.section); r++;
    const wfStep = (job.locked || job.status === 'completed') ? Math.max(Number(job.workflowStep || 0), 10) : Number(job.workflowStep || 1);
    const wfInfo = JOB_WORKFLOW_STEPS.find(s => s.id === wfStep) || {};
    const infoRows = [
      ['ลูกค้า', job.customer || '-'], ['เบอร์ติดต่อ', job.phone || '-'],
      ['สถานที่', job.location || '-'], ['วันที่', job.date || '-'],
      ['ประเภทงาน', job.type || '-'],
      ['สถานะ', job.status === 'completed' ? '✓ เสร็จ' : 'ดำเนินการ'],
      ['ขั้นตอน', `${wfStep}/${JOB_WORKFLOW_STEPS.length} ${wfInfo.label || ''}`],
    ];
    if (job.closedBy) infoRows.push(['ปิดงานโดย', `${job.closedBy} (${job.closedAt ? new Date(job.closedAt).toLocaleDateString('th-TH') : ''})`]);
    infoRows.forEach(([k, v]) => { set(`B${r}`, k, S.cell); set(`C${r}`, v, S.cell); r++; });
    r++;

    // ===== 2. สรุปการเงิน =====
    set(`B${r}`, '💰 สรุปการเงินงาน', S.section); set(`C${r}`, '', S.section); r++;
    let stockCost = 0, cashCost = 0;
    Object.values(job.costsByCategory || {}).forEach(items => (items || []).forEach(it => {
      const a = Number(it.amount || 0);
      if (it.stockId) stockCost += a; else cashCost += a;
    }));
    const sale = Number(job.salePrice || 0);
    const totalC = cashCost + stockCost;
    const svcLog = Array.isArray(job.serviceLog) ? job.serviceLog : [];
    const svcNet = svcLog.reduce((s, l) => s + Number(l.income || 0) - Number(l.cost || 0), 0);
    set(`B${r}`, 'ราคาขาย', S.cell); set(`C${r}`, sale, S.green); r++;
    set(`B${r}`, 'ต้นทุน — จ่ายจริง', S.cell); set(`C${r}`, cashCost, S.red); r++;
    set(`B${r}`, 'ต้นทุน — ของจากสต๊อก', S.cell); set(`C${r}`, stockCost, S.red); r++;
    set(`B${r}`, 'ต้นทุนรวม', S.cell); set(`C${r}`, totalC, S.total); r++;
    set(`B${r}`, `กำไรติดตั้ง (${sale > 0 ? ((sale - totalC) / sale * 100).toFixed(1) : 0}%)`, S.cell); set(`C${r}`, sale - totalC, S.profit); r++;
    if (svcLog.length > 0) {
      set(`B${r}`, `บริการหลังขายสุทธิ (${svcLog.length} ครั้ง)`, S.cell); set(`C${r}`, svcNet, svcNet >= 0 ? S.green : S.red); r++;
      set(`B${r}`, '🏆 กำไรระยะยาว', S.cell); set(`C${r}`, sale - totalC + svcNet, S.profit); r++;
    }
    r++;

    // ===== 3. ต้นทุนแยกหมวด =====
    set(`B${r}`, '🔧 รายการต้นทุนทั้งหมด', S.section); ['C','D','E'].forEach(c => set(`${c}${r}`, '', S.section)); r++;
    ['หมวด', 'รายการ', 'ที่มา', 'จำนวนเงิน (฿)'].forEach((h, i) => set(`${String.fromCharCode(66 + i)}${r}`, h, S.th)); r++;
    const CAT_LABELS = { panel: 'แผงโซล่า', inverter: 'อินเวอร์เตอร์', battery: 'แบตเตอรี่', wire: 'สายไฟ', material: 'วัสดุอื่นๆ', travel: 'ค่าเดินทาง', panel_box: 'ตู้คอนโทรล', labor: 'ค่าแรง', commission: 'ค่าคอม', other: 'อื่นๆ' };
    Object.entries(job.costsByCategory || {}).forEach(([cat, items]) => {
      (items || []).forEach(it => {
        set(`B${r}`, CAT_LABELS[cat] || cat, S.cell);
        set(`C${r}`, it.item || '-', S.cell);
        set(`D${r}`, it.stockId ? '📦 เบิกสต๊อก' : '🛒 ซื้อ/จ่าย', S.center);
        set(`E${r}`, Number(it.amount || 0), S.money);
        r++;
      });
    });
    set(`B${r}`, 'รวมต้นทุน', S.cell); set(`C${r}`, '', S.cell); set(`D${r}`, '', S.cell); set(`E${r}`, totalC, S.total); r += 2;

    // ===== 4. รายการเงินของงาน =====
    const jobTxs = transactions.filter(t => t.jobId === job.id).sort((a, b) => (a.date || '').localeCompare(b.date || ''));
    set(`B${r}`, `💵 รายการเงินของงาน (${jobTxs.length} รายการ)`, S.section); ['C','D','E','F'].forEach(c => set(`${c}${r}`, '', S.section)); r++;
    ['วันที่', 'หมวด', 'รายละเอียด', 'รับ (฿)', 'จ่าย (฿)', 'สร้างโดย'].forEach((h, i) => set(`${String.fromCharCode(66 + i)}${r}`, h, S.th)); r++;
    jobTxs.forEach(t => {
      set(`B${r}`, t.date || '', S.center);
      set(`C${r}`, t.category || '', S.cell);
      set(`D${r}`, t.description || '', S.cell);
      set(`E${r}`, t.type === 'income' ? Number(t.amount || 0) : '', S.green);
      set(`F${r}`, t.type === 'expense' ? Number(t.amount || 0) : '', S.red);
      set(`G${r}`, t.createdBy || '-', { font: { sz: 8, color: { rgb: '78716C' } }, border: thin });
      r++;
    });
    r++;

    // ===== 5. เอกสารของงาน =====
    const jobDocs = documents.filter(d => d.jobId === job.id || d.id === job.quotationId || d.jobChainId === job.quotationId);
    if (jobDocs.length > 0) {
      set(`B${r}`, `📄 เอกสารของงาน (${jobDocs.length} ฉบับ)`, S.section); ['C','D','E'].forEach(c => set(`${c}${r}`, '', S.section)); r++;
      ['เลขที่', 'ประเภท', 'วันที่', 'ยอด (฿)'].forEach((h, i) => set(`${String.fromCharCode(66 + i)}${r}`, h, S.th)); r++;
      const DOC_LABELS = { quotation: 'ใบเสนอราคา', invoice: 'ใบแจ้งหนี้', 'receipt-deposit': 'ใบเสร็จมัดจำ', 'receipt-final': 'ใบเสร็จ', receipt: 'ใบเสร็จ' };
      jobDocs.forEach(d => {
        set(`B${r}`, d.docNumber || '-', S.center);
        set(`C${r}`, DOC_LABELS[d.type] || d.type, S.cell);
        set(`D${r}`, d.date || '-', S.center);
        set(`E${r}`, Number(d.totalAmount || 0), S.money);
        r++;
      });
      r++;
    }

    // ===== 6. บันทึกงาน + บริการ =====
    if (svcLog.length > 0) {
      set(`B${r}`, `📋 บันทึกงาน + บริการหลังการขาย (${svcLog.length})`, S.section); ['C','D','E','F'].forEach(c => set(`${c}${r}`, '', S.section)); r++;
      ['วันที่', 'ประเภท', 'รายละเอียด', 'รับ (฿)', 'จ่าย (฿)', 'โดย'].forEach((h, i) => set(`${String.fromCharCode(66 + i)}${r}`, h, S.th)); r++;
      const SVC_L = { issue: '🐛 ปัญหา', feedback: '💬 ฟีดแบ็ก', clean: '🧽 ล้างแผง', repair: '🔧 ซ่อม', followup: '📞 ติดตาม', note: '📝 บันทึก' };
      [...svcLog].sort((a, b) => (a.date || '').localeCompare(b.date || '')).forEach(l => {
        set(`B${r}`, l.date || '', S.center);
        set(`C${r}`, SVC_L[l.type] || l.type, S.cell);
        set(`D${r}`, l.note || '', S.cell);
        set(`E${r}`, Number(l.income || 0) > 0 ? Number(l.income) : '', S.green);
        set(`F${r}`, Number(l.cost || 0) > 0 ? Number(l.cost) : '', S.red);
        set(`G${r}`, l.by || '-', { font: { sz: 8, color: { rgb: '78716C' } }, border: thin });
        r++;
      });
    }

    ws['!ref'] = `A1:H${r + 1}`;
    ws['!cols'] = [{ wch: 2 }, { wch: 16 }, { wch: 20 }, { wch: 40 }, { wch: 14 }, { wch: 14 }, { wch: 16 }, { wch: 4 }];
    const safeName = (job.customer || 'งาน').replace(/[\\/:*?"<>|]/g, '').slice(0, 30);
    XLSX.utils.book_append_sheet(wb, ws, 'แฟ้มงาน');
    const fileName = `DD_งาน_${safeName}_${job.date || ''}.xlsx`;
    XLSX.writeFile(wb, fileName);
    logActivity('export', 'งาน', `📊 Export แฟ้มงาน: ${job.customer} (${fileName})`);
  };

  if (loading) {
    return <div className="min-h-screen bg-stone-100 flex items-center justify-center"><Sun className="w-16 h-16 text-amber-500 animate-spin" /></div>;
  }

  return (
    <div className="min-h-screen bg-stone-100" style={{fontFamily: "'Sarabun', system-ui, sans-serif"}}>
      <style>{`
        
        .display-font { font-family: 'Bebas Neue', sans-serif; letter-spacing: 0.04em; }
        @keyframes slide-up { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
        .animate-slide-up { animation: slide-up 0.4s ease-out; }
        @keyframes fade-in { from { opacity: 0; } to { opacity: 1; } }
        .animate-fade-in { animation: fade-in 0.3s ease-out; }
      `}</style>

      <header className="text-white sticky top-0 z-40 shadow-lg" style={{background: 'linear-gradient(to right, #0d1f43, #1e3a5f)'}}>
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between gap-2">
          <div className="flex items-center gap-3 min-w-0">
            <img src="icons/icon-192.png" alt="DD" className="w-11 h-11 rounded-xl shadow-md flex-shrink-0" />
            <div className="min-w-0">
              <h1 className="display-font text-xl md:text-3xl">D.D. SOLUTION</h1>
              <p className="text-xs text-amber-200 truncate">{currentUser.icon} {currentUser.name} กำลังใช้งาน</p>
            </div>
          </div>
          <div className="flex items-center gap-1 flex-shrink-0">
            <button onClick={exportToExcel} className="hidden md:flex items-center gap-1 px-3 py-2 bg-emerald-600 hover:bg-emerald-700 rounded-lg text-sm font-medium transition-colors" title="Export Excel สำหรับยื่นภาษี">
              <Download className="w-4 h-4" /> Export
            </button>
            <button onClick={exportToExcel} className="md:hidden p-2 hover:bg-white/10 rounded-lg" title="Export Excel">
              <Download className="w-4 h-4 text-emerald-400" />
            </button>
            <button onClick={onLogout} className="p-2 hover:bg-white/10 rounded-lg" title="ออกจากระบบ">
              <LogOut className="w-4 h-4" />
            </button>
            <button onClick={resetData} className="text-stone-400 hover:text-red-400 p-2" title="รีเซ็ตข้อมูล">
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>
        <div className="max-w-7xl mx-auto px-2 flex overflow-x-auto">
          {[
            { id: 'dashboard', label: 'แดชบอร์ด', icon: BarChart3 },
            { id: 'sales', label: 'เสนอขาย', icon: TrendingUp },
            { id: 'catalog', label: 'แคตตาล็อกขาย', icon: DollarSign },
            { id: 'jobs', label: 'งาน', icon: Briefcase },
            { id: 'customers', label: 'ลูกค้า', icon: UserCircle },
            { id: 'stock', label: 'สต็อก', icon: Package },
            { id: 'partners', label: 'ผู้ลงทุน', icon: Users },
            { id: 'finance', label: 'การเงิน', icon: Wallet },
            { id: 'documents', label: 'งานเอกสาร', icon: Save },
            { id: 'activity', label: 'ประวัติ', icon: Activity },
            { id: 'help', label: 'วิธีใช้', icon: AlertCircle },
          ].map(tab => {
            const Icon = tab.icon;
            return (
              <button key={tab.id} onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-3 whitespace-nowrap border-b-2 transition-colors ${
                  activeTab === tab.id ? 'border-amber-400 text-amber-300 font-semibold' : 'border-transparent text-stone-300'
                }`}>
                <Icon className="w-4 h-4" /> {tab.label}
              </button>
            );
          })}
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-4 md:p-6">
        {activeTab === 'dashboard' && (
          <div className="space-y-5 animate-fade-in">
            {/* 💰 การ์ดเงินสดในมือ - ใหญ่เด่น */}
            {(() => {
              const totalInvestment = Object.values(actualInvestments.inv).reduce((s, v) => s + v, 0);
              const cashOnHand = totalInvestment + totalProfit - dividendStats.total - totalStockValue;
              return (
                <div className="rounded-3xl shadow-xl overflow-hidden" style={{background: 'linear-gradient(135deg, #0d1f43 0%, #1e3a5f 50%, #0d1f43 100%)'}}>
                  <div className="p-5 md:p-6 text-white">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-2">
                        <div className="bg-amber-400 text-stone-900 rounded-full p-2">
                          <Wallet className="w-5 h-5" />
                        </div>
                        <h2 className="display-font text-xl md:text-2xl">เงินสดในมือ</h2>
                      </div>
                      <span className="text-xs bg-white/10 px-2 py-1 rounded-full">อัพเดทอัตโนมัติ</span>
                    </div>
                    
                    <div className="text-4xl md:text-5xl font-bold text-amber-300 mb-1">
                      {fmt(cashOnHand)} <span className="text-2xl">฿</span>
                    </div>
                    <p className="text-stone-300 text-sm mb-4">เงินบริษัทที่จับได้จริง ณ ตอนนี้</p>
                    
                    {/* Breakdown */}
                    <div className="bg-white/5 backdrop-blur rounded-2xl p-3 space-y-1.5 text-sm">
                      <div className="flex justify-between text-stone-300">
                        <span>เงินทุนรวม</span>
                        <span className="font-mono">+ {fmt(totalInvestment)} ฿</span>
                      </div>
                      <div className="flex justify-between text-emerald-300">
                        <span>กำไรสะสม</span>
                        <span className="font-mono">+ {fmt(totalProfit)} ฿</span>
                      </div>
                      {dividendStats.total > 0 && (
                        <div className="flex justify-between text-violet-300">
                          <span>ปันผลจ่ายแล้ว</span>
                          <span className="font-mono">− {fmt(dividendStats.total)} ฿</span>
                        </div>
                      )}
                      <div className="flex justify-between text-orange-300">
                        <span>มูลค่าสต๊อก</span>
                        <span className="font-mono">− {fmt(totalStockValue)} ฿</span>
                      </div>
                      <div className="border-t border-white/20 pt-1.5 flex justify-between font-bold text-amber-300">
                        <span>คงเหลือ</span>
                        <span className="font-mono">{fmt(cashOnHand)} ฿</span>
                      </div>
                    </div>

                    {/* ปุ่มเพิ่มทุน/ถอนทุน/ปันผล */}
                    <div className="grid grid-cols-3 gap-2 mt-3">
                      <button
                        onClick={() => { setCapitalMode('deposit'); setShowCapitalModal(true); }}
                        className="bg-emerald-500 hover:bg-emerald-400 text-white font-medium py-2.5 rounded-xl flex items-center justify-center gap-1.5 transition-colors shadow-lg text-sm"
                      >
                        <ArrowDownLeft className="w-4 h-4" /> เพิ่มทุน
                      </button>
                      <button
                        onClick={() => { setCapitalMode('withdraw'); setShowCapitalModal(true); }}
                        className="bg-rose-500 hover:bg-rose-400 text-white font-medium py-2.5 rounded-xl flex items-center justify-center gap-1.5 transition-colors shadow-lg text-sm"
                      >
                        <ArrowUpRight className="w-4 h-4" /> ถอนทุน
                      </button>
                      <button
                        onClick={() => setShowDividendModal(true)}
                        className="bg-violet-500 hover:bg-violet-400 text-white font-medium py-2.5 rounded-xl flex items-center justify-center gap-1.5 transition-colors shadow-lg text-sm"
                      >
                        💜 ปันผล
                      </button>
                    </div>
                  </div>
                </div>
              );
            })()}

            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <StatCard icon={DollarSign} label="รายได้รวม" value={fmt0(totalRevenue)} suffix="฿" color="emerald" />
              <StatCard icon={TrendingDown} label="ต้นทุนรวม" value={fmt0(totalCost)} suffix="฿" color="rose" />
              <StatCard icon={TrendingUp} label="กำไรสุทธิ" value={fmt0(totalProfit)} suffix="฿" color="amber" highlight />
              <StatCard icon={Briefcase} label="งานเสร็จ" value={completedJobs} suffix="งาน" color="blue" />
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="bg-white rounded-2xl p-5 shadow-sm border border-stone-200">
                <div className="flex items-center gap-2 mb-4"><PieChart className="w-5 h-5 text-amber-600" /><h2 className="display-font text-xl text-stone-800">สัดส่วนการลงทุน</h2></div>
                <div className="space-y-3">
                  {partners.map(p => {
                    const inv = actualInvestments.inv[p.id] || 0;
                    const totalAll = Object.values(actualInvestments.inv).reduce((s, v) => s + v, 0);
                    const pct = totalAll > 0 ? (inv / totalAll * 100) : 0;
                    return (
                      <div key={p.id}>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="font-medium">{p.name}</span>
                          <span className="text-stone-500">{fmt(inv)} ฿ ({pct.toFixed(1)}%)</span>
                        </div>
                        <div className="h-2 bg-stone-100 rounded-full overflow-hidden">
                          <div className="h-full bg-gradient-to-r from-amber-400 to-orange-500 transition-all duration-500" style={{width: `${pct}%`}} />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
              <div className="bg-white rounded-2xl p-5 shadow-sm border border-stone-200">
                <div className="flex items-center gap-2 mb-4"><Package className="w-5 h-5 text-amber-600" /><h2 className="display-font text-xl text-stone-800">สต็อกคงเหลือ</h2></div>
                <div className="text-3xl font-bold text-amber-600 mb-1">{fmt0(totalStockValue)} ฿</div>
                <div className="text-sm text-stone-500 mb-3">{stock.filter(s => Number(s.qty) > 0).length} รายการมีในมือ · ประวัติ {stock.filter(s => Number(s.qty) === 0).length} รายการ</div>
                <button onClick={() => setActiveTab('stock')} className="text-sm text-amber-600 hover:underline">→ ดูรายละเอียด</button>
              </div>
            </div>
            <div className="bg-white rounded-2xl p-5 shadow-sm border border-stone-200">
              <h2 className="display-font text-xl text-stone-800 mb-3">งานล่าสุด</h2>
              <div className="space-y-2">
                {jobs.slice(-5).reverse().map(job => (
                  <div key={job.id} className="flex items-center justify-between p-3 bg-stone-50 rounded-xl">
                    <div className="min-w-0 flex-1">
                      <div className="font-medium truncate">{job.customer}</div>
                      <div className="text-xs text-stone-500">{job.date} · {job.type}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-semibold text-emerald-600">+{fmt0(job.profit)} ฿</div>
                      <div className="text-xs text-stone-400">ขาย {fmt0(job.salePrice)}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'sales' && (
          <div className="space-y-4">
          <QuickCostCalc />
          <SalesPresentation
            customers={customers}
            stock={stock}
            catalog={salesCatalog}
            companyInfo={companyInfo}
            onCreateQuotation={(data) => {
              // 1. ถ้าเป็นลูกค้าใหม่ → save customer ก่อน
              let customerId = data.selectedCustomerId || '';
              if (data.customerMode === 'new' && data.customerName) {
                const existing = customers.find(c => c.name === data.customerName && c.phone === data.customerPhone);
                if (existing) {
                  customerId = existing.id;
                } else {
                  const newCustomer = {
                    id: `cust-${Date.now()}`,
                    name: data.customerName,
                    phone: data.customerPhone,
                    address: data.customerAddress,
                    photos: [],
                    createdAt: new Date().toISOString(),
                  };
                  saveCustomers([...customers, newCustomer], 'add', `เพิ่มลูกค้า: ${data.customerName}`);
                  customerId = newCustomer.id;
                }
              }
              
              // 2. สร้าง quotation ใหม่
              const newDoc = {
                id: `doc-${Date.now()}`,
                type: 'quotation',
                docNumber: generateDocNumber('quotation', documents),
                docDate: new Date().toISOString().split('T')[0],
                validUntil: new Date(Date.now() + 14*86400000).toISOString().split('T')[0],
                customerId,
                customerName: data.customerName,
                customerPhone: data.customerPhone,
                customerAddress: data.customerAddress,
                items: data.items,
                subtotal: data.totalAmount,
                discount: 0,
                totalAmount: data.totalAmount,
                paymentTerms: '',
                depositPercent: 50,
                depositAmount: Math.round(data.totalAmount * 0.5),
                warrantyText: '', // ไม่ใส่ default - มี table รับประกันแล้ว
                notes: '',
                jobId: '', // ผูกกับงาน (ตอนสร้างงานจะ update ที่นี่)
                jobChainId: `doc-${Date.now()}`, // เป็น chain master
                jobStatus: 'active',
                status: 'active',
                linkedDocId: '',
                // === Snapshot จากการเสนอขาย (สำหรับสร้างงาน) ===
                equipmentSnapshot: data.equipmentSnapshot || null, // ข้อมูล inv/panel/bat ครบถ้วน
                createdAt: new Date().toISOString(),
              };
              newDoc.jobChainId = newDoc.id; // ตัวเองเป็น chain master
              
              saveDocuments([...documents, newDoc], 'add', 
                `สร้างใบเสนอราคา ${newDoc.docNumber} (${data.customerName}) จากการเสนอขาย`);
              
              alert(`✅ สร้างใบเสนอราคา ${newDoc.docNumber} เรียบร้อย!`);
              setActiveTab('documents');
            }}
            onSaveCustomer={(c) => saveCustomers([...customers, c], 'add', `เพิ่มลูกค้า: ${c.name}`)}
            onSaveCompany={async (data, action, details) => {
              await window.storage.set('dd5:company', JSON.stringify(data), true);
              setCompanyInfo(data);
              if (action) await logActivity(action, 'ข้อมูลบริษัท', details || 'แก้ไขข้อมูลบริษัท');
            }}
          />
          </div>
        )}

        {activeTab === 'catalog' && (
          <SalesCatalogManager 
            catalog={salesCatalog}
            stock={stock}
            companyInfo={companyInfo}
            onSaveCatalog={saveSalesCatalog}
            onSaveCompany={async (data, action, details) => {
              setCompanyInfo(data);
              try { await window.storage.set('dd5:company', JSON.stringify(data), true); } catch(e){}
              if (action) await logActivity(action, 'ข้อมูลบริษัท', details);
            }}
          />
        )}

        {activeTab === 'jobs' && (
          <div className="space-y-4 animate-fade-in">
            <div className="flex items-center justify-between flex-wrap gap-2">
              <div><h2 className="display-font text-3xl text-stone-800">รายการงาน</h2><p className="text-sm text-stone-500">{jobs.length} งาน</p></div>
              <div className="flex gap-2 flex-wrap">
                {(() => {
                  // หาใบเสนอราคา active ที่ยังไม่มี job
                  const availableQuotations = documents.filter(d => 
                    d.type === 'quotation' && 
                    d.jobStatus === 'active' &&
                    !d.jobId  // ยังไม่ผูกกับงาน
                  );
                  if (availableQuotations.length === 0) return null;
                  return (
                    <button onClick={() => setShowPickQuotation(true)}
                      className="flex items-center gap-2 bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2 rounded-xl font-medium shadow-sm">
                      🚀 จากใบเสนอราคา
                      <span className="bg-white/20 text-xs px-1.5 py-0.5 rounded-full">{availableQuotations.length}</span>
                    </button>
                  );
                })()}
                <button onClick={() => { setEditingItem(null); setShowJobModal(true); }} 
                  className="flex items-center gap-2 bg-amber-500 hover:bg-amber-600 text-white px-4 py-2 rounded-xl font-medium shadow-sm">
                  <Plus className="w-4 h-4" /> เพิ่มงาน
                </button>
              </div>
            </div>
            <div className="space-y-3">
              {jobs.map(job => (
                <JobCard key={job.id} job={job} partners={partners} fmt={fmt} fmt0={fmt0}
                  onEdit={() => { setEditingItem(job); setShowJobModal(true); }}
                  onExportExcel={() => exportJobToExcel(job)}
                  onDelete={() => {
                    const autoTxs = transactions.filter(t => t.id === `t-jobinc-${job.id}` || t.id === `t-jobcost-${job.id}` || (t.jobId === job.id && t.isService));
                    const txWarn = autoTxs.length > 0 ? `\n\n💰 รายการเงินอัตโนมัติของงานนี้ ${autoTxs.length} รายการจะถูกลบด้วย` : '';
                    if (window.confirm(`ลบงาน ${job.customer}?${txWarn}`)) {
                      saveJobs(jobs.filter(j => j.id !== job.id), 'delete', `ลบงาน: ${job.customer}`);
                      if (autoTxs.length > 0) {
                        const ids = new Set(autoTxs.map(t => t.id));
                        saveTransactions(transactions.filter(t => !ids.has(t.id)), 'delete', `🗑️ ลบรายการเงินของงาน ${job.customer} (${autoTxs.length} รายการ)`);
                      }
                    }
                  }}
                />
              ))}
            </div>
          </div>
        )}

        {activeTab === 'stock' && (
          <div className="space-y-4 animate-fade-in">
            <div className="flex items-center justify-between flex-wrap gap-2">
              <div><h2 className="display-font text-3xl text-stone-800">สต็อกสินค้า</h2><p className="text-sm text-stone-500">มูลค่ารวม: <span className="font-semibold text-amber-600">{fmt0(totalStockValue)} ฿</span></p></div>
              <div className="flex gap-2">
                <button onClick={() => downloadStockSummaryPNG(stock, totalStockValue)} title="บันทึกภาพสต๊อกล่าสุด (PNG)" className="flex items-center gap-2 px-3 py-2 rounded-xl font-medium border bg-white border-stone-200 hover:bg-amber-50 transition-colors">
                  <Camera className="w-4 h-4 text-amber-600" /> รูปสต๊อก
                </button>
                <button onClick={() => setShowHistory(!showHistory)} className={`flex items-center gap-2 px-3 py-2 rounded-xl font-medium border transition-colors ${showHistory ? 'bg-stone-200 border-stone-300' : 'bg-white border-stone-200'}`}>
                  {showHistory ? <EyeOff className="w-4 h-4" /> : <History className="w-4 h-4" />}
                  {showHistory ? 'ซ่อนประวัติ' : 'ดูประวัติ'}
                </button>
                <button onClick={() => { setEditingItem(null); setShowStockModal(true); }} className="flex items-center gap-2 bg-amber-500 hover:bg-amber-600 text-white px-4 py-2 rounded-xl font-medium shadow-sm">
                  <Plus className="w-4 h-4" /> เพิ่มสินค้า
                </button>
              </div>
            </div>

            {STOCK_CATEGORIES.map(cat => {
              const itemsInCat = stock.filter(s => s.category === cat.id);
              const activeItems = itemsInCat.filter(s => Number(s.qty) > 0);
              const historyItems = itemsInCat.filter(s => Number(s.qty) === 0);
              const visible = showHistory ? itemsInCat : activeItems;
              if (visible.length === 0) return null;
              return (
                <div key={cat.id} className="bg-white rounded-2xl p-4 shadow-sm border border-stone-200">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="display-font text-lg text-amber-700">{cat.label}</h3>
                    <span className="text-xs text-stone-500">{activeItems.length} รายการ {showHistory && historyItems.length > 0 && `· ประวัติ ${historyItems.length}`}</span>
                  </div>
                  <div className="space-y-2">
                    {visible.map(item => (
                      <StockRow key={item.id} item={item} fmt={fmt} fmt0={fmt0}
                        onEdit={() => { setEditingItem(item); setShowStockModal(true); }}
                        onDelete={() => { if (window.confirm(`ลบ ${item.name} ออกจากระบบ?`)) saveStock(stock.filter(s => s.id !== item.id), 'delete', `ลบสินค้า: ${item.name}`); }}
                      />
                    ))}
                  </div>
                </div>
              );
            })}

            {!showHistory && stock.filter(s => Number(s.qty) > 0).length === 0 && (
              <div className="bg-white rounded-2xl p-8 text-center shadow-sm border border-stone-200">
                <Package className="w-12 h-12 text-stone-300 mx-auto mb-2" />
                <p className="text-stone-500">ยังไม่มีของในสต็อก</p>
                <p className="text-xs text-stone-400 mt-1">กดปุ่ม "ดูประวัติ" เพื่อดูของที่เคยซื้อ</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'partners' && (
          <div className="space-y-4 animate-fade-in">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="display-font text-3xl text-stone-800">ผู้ลงทุน / ทีม</h2>
                <p className="text-sm text-stone-500">ลงทุนรวม {fmt(Object.values(actualInvestments.inv).reduce((s, v) => s + v, 0))} ฿</p>
              </div>
              <button onClick={() => { setEditingItem(null); setShowPartnerModal(true); }} className="flex items-center gap-2 bg-amber-500 hover:bg-amber-600 text-white px-4 py-2 rounded-xl font-medium shadow-sm">
                <Plus className="w-4 h-4" /> เพิ่มสมาชิก
              </button>
            </div>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {partners.map(p => {
                const actualInv = actualInvestments.inv[p.id] || 0;
                const fromJobs = actualInvestments.fromJobs[p.id] || 0;
                const fromStock = actualInvestments.fromStock[p.id] || 0;
                return (
                  <div key={p.id} className="bg-white rounded-2xl p-5 shadow-sm border border-stone-200 animate-slide-up">
                    <div className="flex items-start justify-between mb-3">
                      <div className="w-12 h-12 rounded-full bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center text-white display-font text-xl">{p.name.charAt(0)}</div>
                      <div className="flex gap-1">
                        <button onClick={() => { setEditingItem(p); setShowPartnerModal(true); }} className="p-1.5 hover:bg-stone-100 rounded-lg"><Edit2 className="w-3.5 h-3.5 text-stone-500" /></button>
                        <button onClick={() => { if (window.confirm(`ลบ ${p.name}?`)) savePartners(partners.filter(x => x.id !== p.id), 'delete', `ลบสมาชิก: ${p.name}`); }} className="p-1.5 hover:bg-red-50 rounded-lg"><Trash2 className="w-3.5 h-3.5 text-red-400" /></button>
                      </div>
                    </div>
                    <h3 className="font-bold text-lg text-stone-800">{p.name}</h3>
                    {p.fullName && <p className="text-sm text-stone-500">{p.fullName}</p>}
                    <p className="text-xs text-amber-600 mt-1 font-medium">{p.role}</p>
                    
                    <div className="mt-3 pt-3 border-t border-stone-100">
                      <div className="bg-rose-50 rounded-lg p-2 mb-2">
                        <div className="text-xs text-rose-600">ลงทุนรวม</div>
                        <div className="font-bold text-rose-700 text-lg">{fmt(actualInv)} ฿</div>
                      </div>
                      <div className="grid grid-cols-2 gap-1 text-xs mb-2">
                        <div className="bg-stone-50 rounded p-1.5">
                          <div className="text-stone-500">จากงาน</div>
                          <div className="font-medium text-stone-700">{fmt(fromJobs)}</div>
                        </div>
                        <div className="bg-amber-50 rounded p-1.5">
                          <div className="text-amber-600">จากสต๊อก</div>
                          <div className="font-medium text-amber-700">{fmt(fromStock)}</div>
                        </div>
                      </div>
                      <div className="bg-emerald-50 rounded-lg p-2">
                        <div className="text-xs text-emerald-600">ปันผลรับแล้ว</div>
                        <div className="font-bold text-emerald-700">{fmt0(dividendStats.byPartner[p.id] || 0)} ฿</div>
                      </div>
                    </div>
                    {p.bankAccount && <div className="mt-3 text-xs bg-stone-50 rounded-lg p-2 font-mono text-stone-600">🏦 {p.bankAccount}</div>}
                    {p.note && <div className="mt-2 text-xs text-stone-500">{p.note}</div>}
                  </div>
                );
              })}
            </div>
            <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4">
              <div className="flex gap-3">
                <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                <div className="text-sm text-stone-700">
                  <strong>ยอดลงทุน</strong> = (เงินที่ออกในแต่ละงาน) + (มูลค่าสต๊อกที่ตุนไว้ในชื่อตัวเอง)
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'finance' && (() => {
          // === Smart Categorization ===
          // P&L view (กำไร/ขาดทุน):
          //   รายรับ = เฉพาะรายได้จากลูกค้า (category: 'รายได้จากงาน')
          //   รายจ่าย = ต้นทุนงาน (รวมเบิกสต๊อก) แต่ไม่นับซื้อเข้าสต๊อก
          //
          // Cash Flow view (เงินสด):
          //   เข้า = ทุน + รายได้ลูกค้า
          //   ออก = ซื้อสต๊อก + ค่าใช้จ่ายเงินสด (ไม่นับเบิก เพราะของอยู่แล้ว)
          //
          // ALL view: ทุก transaction (ปัจจุบัน)
          
          // Helper: เช็คประเภท transaction
          const isCustomerIncome = (t) => t.type === 'income' && t.category === 'รายได้จากงาน';
          const isCapitalIn = (t) => t.type === 'income' && (t.category === 'เพิ่มทุน' || t.category === 'ทุน');
          const isStockBuy = (t) => t.type === 'expense' && t.category === 'ต้นทุนสต๊อก';
          const isStockUse = (t) => t.type === 'expense' && t.category === 'เบิกสต๊อก';
          const isJobCost = (t) => t.type === 'expense' && t.category === 'ต้นทุนงาน';
          const isCapitalOut = (t) => t.type === 'expense' && (t.category === 'ถอนทุน' || t.category === 'คืนทุน' || t.category === 'ปันผล');
          
          // P&L calculations
          const pnlIncome = transactions.filter(isCustomerIncome).reduce((s, t) => s + Number(t.amount || 0), 0);
          const pnlCashCost = transactions.filter(t => isJobCost(t) || isStockUse(t)).reduce((s, t) => s + Number(t.amount || 0), 0);
          // ของที่เบิกจากสต๊อกไปใช้ในงาน (ไม่มี tx เพราะจ่ายตอนซื้อเข้า) — ต้องนับเป็นต้นทุนเพื่อกำไรตรง Dashboard
          const pnlStockUsed = jobs.reduce((s, j) => {
            let v = 0;
            Object.values(j.costsByCategory || {}).forEach(items => (items || []).forEach(it => { if (it.stockId) v += Number(it.amount || 0); }));
            return s + v;
          }, 0);
          const pnlExpense = pnlCashCost + pnlStockUsed;
          const pnlProfit = pnlIncome - pnlExpense;
          
          // Cash Flow = ทุกรายการ (โครงสร้างใหม่: ทุก transaction คือเงินจริง)
          const cashIn = transactions.filter(t => t.type === 'income').reduce((s, t) => s + Number(t.amount || 0), 0);
          const cashOut = transactions.filter(t => t.type === 'expense').reduce((s, t) => s + Number(t.amount || 0), 0);
          const cashBalance = cashIn - cashOut;
          
          // Filter transactions ตาม tab
          const filteredTransactions = financeTab === 'pnl'
            ? transactions.filter(t => isCustomerIncome(t) || isJobCost(t) || isStockUse(t))
            : transactions; // เงินสด = ทุกรายการ (ทุกตัวคือเงินจริง)
          
          return (
          <div className="space-y-4 animate-fade-in">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="display-font text-3xl text-stone-800">รายรับ-รายจ่าย</h2>
                <p className="text-sm text-stone-500">{transactions.length} รายการ</p>
              </div>
              <button onClick={() => { setEditingItem(null); setShowTransactionModal(true); }}
                className="flex items-center gap-2 bg-amber-500 hover:bg-amber-600 text-white px-4 py-2 rounded-xl font-medium shadow-sm">
                <Plus className="w-4 h-4" /> เพิ่มรายการ
              </button>
            </div>

            {/* === 2 มุมมอง === */}
            <div className="bg-white rounded-2xl p-1 shadow-sm border border-stone-200 flex gap-1">
              <button onClick={() => setFinanceTab('cash')}
                className={`flex-1 py-2 px-3 rounded-xl text-sm font-medium transition-colors ${
                  financeTab === 'cash' ? 'bg-amber-600 text-white' : 'text-stone-600 hover:bg-stone-100'
                }`}>
                💵 เงินสด (ทุกรายการ)
              </button>
              <button onClick={() => setFinanceTab('pnl')}
                className={`flex-1 py-2 px-3 rounded-xl text-sm font-medium transition-colors ${
                  financeTab === 'pnl' ? 'bg-emerald-600 text-white' : 'text-stone-600 hover:bg-stone-100'
                }`}>
                💰 กำไร/ขาดทุน
              </button>
            </div>

            {/* === Summary Cards (เปลี่ยนตาม tab) === */}
            

            

            {financeTab === 'pnl' && (
              <>
                <div className="grid grid-cols-3 gap-3">
                  <div className="bg-emerald-500 text-white rounded-2xl p-4">
                    <div className="flex items-center gap-2 mb-1">
                      <ArrowDownLeft className="w-4 h-4" />
                      <span className="text-xs">รายได้จากลูกค้า</span>
                    </div>
                    <div className="display-font text-2xl">{fmt0(pnlIncome)}</div>
                  </div>
                  <div className="bg-rose-500 text-white rounded-2xl p-4">
                    <div className="flex items-center gap-2 mb-1">
                      <ArrowUpRight className="w-4 h-4" />
                      <span className="text-xs">ต้นทุนงานรวม</span>
                    </div>
                    <div className="display-font text-2xl">{fmt0(pnlExpense)}</div>
                    <div className="text-[10px] opacity-80 mt-0.5">จ่ายจริง {fmt0(pnlCashCost)} · จากสต๊อก {fmt0(pnlStockUsed)}</div>
                  </div>
                  <div className={`text-white rounded-2xl p-4 ${pnlProfit >= 0 ? 'bg-emerald-600' : 'bg-rose-600'}`}>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs">💰 กำไรสุทธิ</span>
                    </div>
                    <div className="display-font text-2xl">{fmt0(pnlProfit)}</div>
                    {Math.abs(pnlProfit - totalProfit) < 1 && <div className="text-[10px] opacity-80 mt-0.5">✓ ตรงแดชบอร์ด</div>}
                  </div>
                </div>
                <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-3 text-xs text-emerald-800">
                  <strong>💡 มุมมองกำไร/ขาดทุน (P&L):</strong> รายได้จากลูกค้า − ต้นทุนงานครบ (จ่ายจริง + ของที่เบิกจากสต๊อก). กำไรสุทธิตรงกับแดชบอร์ดเสมอ. ไม่นับทุนหุ้นส่วน/ปันผล/ซื้อของเข้าสต๊อก.
                </div>
              </>
            )}

            {financeTab === 'cash' && (
              <>
                <div className="grid grid-cols-3 gap-3">
                  <div className="bg-emerald-500 text-white rounded-2xl p-4">
                    <div className="flex items-center gap-2 mb-1">
                      <ArrowDownLeft className="w-4 h-4" />
                      <span className="text-xs">เงินเข้า</span>
                    </div>
                    <div className="display-font text-2xl">{fmt0(cashIn)}</div>
                    <div className="text-[10px] opacity-80 mt-1">ทุน + ลูกค้า</div>
                  </div>
                  <div className="bg-rose-500 text-white rounded-2xl p-4">
                    <div className="flex items-center gap-2 mb-1">
                      <ArrowUpRight className="w-4 h-4" />
                      <span className="text-xs">เงินออก</span>
                    </div>
                    <div className="display-font text-2xl">{fmt0(cashOut)}</div>
                    <div className="text-[10px] opacity-80 mt-1">ซื้อสต๊อก + ค่าใช้จ่าย</div>
                  </div>
                  <div className={`text-white rounded-2xl p-4 ${cashBalance >= 0 ? 'bg-amber-500' : 'bg-rose-600'}`}>
                    <div className="flex items-center gap-2 mb-1">
                      <Wallet className="w-4 h-4" />
                      <span className="text-xs">เงินในมือ</span>
                    </div>
                    <div className="display-font text-2xl">{fmt0(cashBalance)}</div>
                  </div>
                </div>
                <div className="bg-amber-50 border border-amber-200 rounded-xl p-3 text-xs text-amber-800">
                  <strong>💡 มุมมองเงินสด (Cash Flow):</strong> ทุน + รายได้ลูกค้า - ซื้อสต๊อก - ค่าใช้จ่าย. <strong>ไม่นับเบิกสต๊อก</strong> (ของอยู่แล้ว ไม่ได้จ่ายเงินใหม่).
                </div>
                
              </>
            )}

            {financeTab === 'cash' && (() => {
                  const totalInv = Object.values(actualInvestments.inv).reduce((s, v) => s + v, 0);
                  const expectedCash = totalInv + totalProfit - dividendStats.total - totalStockValue;
                  const diff = cashBalance - expectedCash;
                  if (Math.abs(diff) < 1) {
                    return (
                      <div className="bg-emerald-50 border border-emerald-200 rounded-xl px-3 py-2 text-xs text-emerald-700">
                        ✅ ตรงกับ "เงินสดในมือ" หน้าแดชบอร์ด ({fmt0(expectedCash)} ฿) — ทุกงานบันทึกเงินครบ
                      </div>
                    );
                  }
                  // วิเคราะห์: หางานที่กำไรนับแล้วแต่เงินจริงยังไม่ครบ
                  const pendingJobs = jobs.map(j => {
                    const inc = transactions.filter(t => t.type === 'income' && t.category === 'รายได้จากงาน' && t.jobId === j.id && !t.isService)
                      .reduce((s, t) => s + Number(t.amount || 0), 0);
                    const incomeGap = Number(j.salePrice || 0) - inc;
                    // ต้นทุนจ่ายจริง (ไม่รวมเบิกสต๊อก) ที่ยังไม่บันทึก
                    let cashCost = 0;
                    Object.values(j.costsByCategory || {}).forEach(items => (items || []).forEach(it => { if (!it.stockId) cashCost += Number(it.amount || 0); }));
                    const costRec = transactions.filter(t => t.type === 'expense' && t.category === 'ต้นทุนงาน' && t.jobId === j.id && !t.isService)
                      .reduce((s, t) => s + Number(t.amount || 0), 0);
                    const costGap = cashCost - costRec;
                    return { name: j.customer, incomeGap, costGap, net: incomeGap - costGap };
                  }).filter(x => Math.abs(x.net) > 0.5 || x.incomeGap > 0.5 || x.costGap > 0.5);
                  return (
                    <div className="bg-orange-50 border border-orange-300 rounded-xl px-3 py-2 text-xs text-orange-800 space-y-1">
                      <div>⚠️ ต่างจากแดชบอร์ด <strong>{fmt0(Math.abs(diff))} ฿</strong> — งานเสร็จแล้วแต่เงินยังไม่บันทึก:</div>
                      {pendingJobs.map((x, i) => (
                        <div key={i} className="pl-3">
                          📋 <strong>{x.name}</strong>:
                          {x.incomeGap > 0.5 && <> ค้างรับ {fmt0(x.incomeGap)} ฿</>}
                          {x.costGap > 0.5 && <> · ค้างบันทึกจ่าย {fmt0(x.costGap)} ฿</>}
                        </div>
                      ))}
                      <button onClick={() => {
                        let txList = [...transactions];
                        const allChanges = [];
                        jobs.forEach(j => {
                          const r = syncJobFinanceTxs(j, txList, currentUser.name);
                          txList = r.txs;
                          if (r.changes.length > 0) allChanges.push(`${j.customer}: ${r.changes.join(', ')}`);
                        });
                        if (allChanges.length === 0) { alert('✅ ไม่มีอะไรค้าง'); return; }
                        saveTransactions(txList, 'add', `💰 บันทึกเงินค้างจากงาน: ${allChanges.join(' / ')}`);
                        alert(`💰 บันทึกให้เรียบร้อย!\n\n${allChanges.join('\n')}\n\nยอดจะตรงแดชบอร์ดแล้ว ✅`);
                      }}
                        className="mt-1 bg-orange-500 hover:bg-orange-600 text-white text-xs font-bold px-3 py-1.5 rounded-lg">
                        💰 บันทึกเงินที่ค้างให้เลย (กดครั้งเดียวจบ)
                      </button>
                    </div>
                  );
                })()}

            {/* 🎨 Legend - ประเภทรายการ */}
            <div className="bg-white rounded-xl border border-stone-200 p-2.5 flex flex-wrap gap-2 text-[11px]">
              <span className="text-stone-400 font-medium">ประเภท:</span>
              <span className="flex items-center gap-1"><span className="w-4 h-4 rounded-full bg-emerald-100 flex items-center justify-center text-[9px]">💰</span> รายได้</span>
              <span className="flex items-center gap-1"><span className="w-4 h-4 rounded-full bg-blue-100 flex items-center justify-center text-[9px]">🏦</span> ทุนเข้า</span>
              <span className="flex items-center gap-1"><span className="w-4 h-4 rounded-full bg-amber-100 flex items-center justify-center text-[9px]">📦</span> ซื้อสต๊อก</span>
              <span className="flex items-center gap-1"><span className="w-4 h-4 rounded-full bg-rose-100 flex items-center justify-center text-[9px]">🔧</span> ต้นทุนงาน</span>
              <span className="flex items-center gap-1"><span className="w-4 h-4 rounded-full bg-purple-100 flex items-center justify-center text-[9px]">🏧</span> ถอนทุน</span>
              <span className="flex items-center gap-1"><span className="w-4 h-4 rounded-full bg-violet-100 flex items-center justify-center text-[9px]">💜</span> ปันผล</span>
            </div>

            {filteredTransactions.length === 0 ? (
              <div className="bg-white rounded-2xl p-8 text-center shadow-sm border border-stone-200">
                <Wallet className="w-12 h-12 text-stone-300 mx-auto mb-2" />
                <p className="text-stone-500">ไม่มีรายการในมุมมองนี้</p>
              </div>
            ) : (
              <div className="bg-white rounded-2xl shadow-sm border border-stone-200 overflow-hidden">
                {filteredTransactions.slice().sort((a, b) => b.date.localeCompare(a.date)).map(t => {
                  const partner = partners.find(p => p.id === t.partnerId);
                  const job = jobs.find(j => j.id === t.jobId);
                  // 🔒 รายการอัตโนมัติ (จากใบเสร็จ/สต๊อก/ปิดงาน/ปันผล/บริการ) = แสดงอย่างเดียว แก้ที่ต้นทาง
                  const isAuto = !!(t.sourceDocId || t.isService || t.auto ||
                    /^t-(rc|svc|close|div)-/.test(t.id || '') ||
                    (t.createdBy || '').includes('อัตโนมัติ') || (t.createdBy || '').includes('บันทึกงาน'));
                  
                  // 🎨 สีตามประเภทรายการ (เข้าใจง่าย)
                  const catStyle = (() => {
                    if (t.type === 'income' && t.category === 'รายได้จากงาน')
                      return { icon: '💰', bg: 'bg-emerald-100', text: 'text-emerald-700', badge: 'bg-emerald-50 text-emerald-700 border-emerald-200', label: 'รายได้' };
                    if (t.type === 'income' && (t.category === 'เพิ่มทุน' || t.category === 'ทุน'))
                      return { icon: '🏦', bg: 'bg-blue-100', text: 'text-blue-700', badge: 'bg-blue-50 text-blue-700 border-blue-200', label: 'ทุนเข้า' };
                    if (t.type === 'expense' && t.category === 'ต้นทุนสต๊อก')
                      return { icon: '📦', bg: 'bg-amber-100', text: 'text-amber-700', badge: 'bg-amber-50 text-amber-700 border-amber-200', label: 'ซื้อสต๊อก' };
                    if (t.type === 'expense' && t.category === 'ต้นทุนงาน')
                      return { icon: '🔧', bg: 'bg-rose-100', text: 'text-rose-700', badge: 'bg-rose-50 text-rose-700 border-rose-200', label: 'ต้นทุนงาน' };
                    if (t.type === 'expense' && t.category === 'ปันผล')
                      return { icon: '💜', bg: 'bg-violet-100', text: 'text-violet-700', badge: 'bg-violet-50 text-violet-700 border-violet-200', label: 'ปันผล' };
                    if (t.type === 'expense' && (t.category === 'ถอนทุน' || t.category === 'คืนทุน'))
                      return { icon: '🏧', bg: 'bg-purple-100', text: 'text-purple-700', badge: 'bg-purple-50 text-purple-700 border-purple-200', label: 'ถอนทุน' };
                    if (t.type === 'income')
                      return { icon: '📥', bg: 'bg-emerald-100', text: 'text-emerald-700', badge: 'bg-stone-50 text-stone-600 border-stone-200', label: t.category };
                    return { icon: '📤', bg: 'bg-rose-100', text: 'text-rose-700', badge: 'bg-stone-50 text-stone-600 border-stone-200', label: t.category };
                  })();
                  
                  return (
                    <div key={t.id} className="flex items-center gap-3 p-4 border-b border-stone-100 last:border-0 hover:bg-stone-50 transition-colors">
                      <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 text-lg ${catStyle.bg}`}>
                        {catStyle.icon}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="font-medium text-stone-800 truncate">{t.description}</span>
                          <span className={`text-[10px] px-1.5 py-0.5 rounded border font-medium whitespace-nowrap ${catStyle.badge}`}>
                            {catStyle.label}
                          </span>
                        </div>
                        <div className="text-xs text-stone-500 flex flex-wrap gap-1 mt-0.5">
                          <span>{t.date}</span>
                          {partner && <><span>·</span><span className="text-blue-600">👤 {partner.name}</span></>}
                          {job && <><span>·</span><span className="text-amber-600">📋 {job.customer}</span></>}
                        </div>
                        {/* Audit trail - ใครสร้าง/แก้ */}
                        {(t.createdBy || t.editedBy || isAuto) && (
                          <div className="text-[10px] text-stone-400 mt-0.5 flex flex-wrap gap-1">
                            {isAuto && <span className="bg-stone-100 text-stone-500 px-1.5 rounded">🤖 อัตโนมัติ</span>}
                            {t.createdBy && <span>✍️ สร้างโดย {t.createdBy}</span>}
                            {t.editedBy && (
                              <span className="text-orange-500">
                                ✏️ แก้ล่าสุดโดย {t.editedBy} ({t.editCount || 1} ครั้ง)
                              </span>
                            )}
                          </div>
                        )}
                      </div>
                      <div className={`font-bold whitespace-nowrap ${t.type === 'income' ? 'text-emerald-600' : 'text-rose-600'}`}>
                        {t.type === 'income' ? '+' : '-'}{fmt0(t.amount)} ฿
                      </div>
                      <div className="flex gap-1 items-center">
                        {isAuto ? (
                          <span className="text-stone-300 px-1.5 select-none" title="รายการอัตโนมัติ — ดึงมาแสดงอย่างเดียว แก้/ลบที่ต้นทาง (ใบเสร็จ/สต๊อก/งาน)">🔒</span>
                        ) : (
                          <>
                            <button onClick={() => { setEditingItem(t); setShowTransactionModal(true); }}
                              className="p-1.5 hover:bg-stone-100 rounded-lg">
                              <Edit2 className="w-3.5 h-3.5 text-stone-500" />
                            </button>
                            <button onClick={() => {
                              if (window.confirm(`ลบรายการนี้?\n\n"${t.description}"\n${t.type === 'income' ? '+' : '-'}${Number(t.amount).toLocaleString()} ฿\n\n⚠️ การลบจะถูกบันทึกในประวัติ`)) {
                                saveTransactions(transactions.filter(x => x.id !== t.id), 'delete', `🗑️ ลบ: ${t.description} (${t.type === 'income' ? '+' : '-'}${Number(t.amount).toLocaleString()} ฿)`);
                              }
                            }} className="p-1.5 hover:bg-red-50 rounded-lg">
                              <Trash2 className="w-3.5 h-3.5 text-red-400" />
                            </button>
                          </>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}

            <div className="bg-blue-50 border border-blue-200 rounded-2xl p-4">
              <div className="flex gap-3">
                <AlertCircle className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                <div className="text-sm text-stone-700">
                  <strong>หมวดหมู่ที่แนะนำ:</strong> รายได้จากงาน, ต้นทุนงาน, เงินกู้/ยืม, เงินคืน, ปันผล, ค่าใช้จ่ายทั่วไป (ที่ไม่ได้อยู่ในงาน)
                  <br />💡 รายการที่ผูกกับ "งาน" และ "คน" จะช่วยให้ติดตามว่าใครออกเงินอะไรไปบ้าง
                </div>
              </div>
            </div>

          </div>
          );
        })()}

        {activeTab === 'customers' && (
          <div className="space-y-4 animate-fade-in">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="display-font text-3xl text-stone-800">ลูกค้า</h2>
                <p className="text-sm text-stone-500">{customers.length} ราย · ติดตั้งสะสม {customers.length} ระบบ</p>
              </div>
              <div className="flex gap-2">
                <button onClick={() => {
                  // 🔄 ดึงลูกค้าจากงานทั้งหมด (ย้อนหลัง) — สร้างที่ยังไม่มี + เติมช่องว่างที่มีแล้ว
                  let created = 0, updated = 0;
                  let newList = [...customers];
                  const createdNames = [];
                  jobs.forEach(j => {
                    const name = (j.customer || '').trim();
                    if (!name) return;
                    const existing = newList.find(cu => cu.name.trim() === name || (cu.jobId && cu.jobId === j.id));
                    if (!existing) {
                      newList.push({
                        id: `cust-${Date.now()}-${Math.random().toString(36).slice(2,5)}`,
                        name, phone: j.phone || '', address: j.location || '', mapLink: '',
                        installDate: j.date || '', system: j.type || '', warranty: '',
                        jobId: j.id, note: '', photos: [],
                      });
                      created++; createdNames.push(name);
                    } else {
                      const patch = {};
                      if (!existing.phone && j.phone) patch.phone = j.phone;
                      if (!existing.address && j.location) patch.address = j.location;
                      if (!existing.system && j.type) patch.system = j.type;
                      if (!existing.installDate && j.date) patch.installDate = j.date;
                      if (!existing.jobId) patch.jobId = j.id;
                      if (Object.keys(patch).length > 0) {
                        newList = newList.map(cu => cu.id === existing.id ? { ...cu, ...patch } : cu);
                        updated++;
                      }
                    }
                  });
                  if (created === 0 && updated === 0) {
                    alert('✅ ลูกค้าจากทุกงานมีครบแล้ว ไม่มีอะไรต้องดึงเพิ่ม');
                    return;
                  }
                  saveCustomers(newList, 'add', `🔄 ดึงลูกค้าจากงาน: สร้างใหม่ ${created} ราย, เติมข้อมูล ${updated} ราย`);
                  alert(`🔄 ดึงจากงานเรียบร้อย!\n\n✨ สร้างใหม่ ${created} ราย${createdNames.length ? ':\n• ' + createdNames.join('\n• ') : ''}\n📝 เติมข้อมูลเพิ่ม ${updated} ราย\n\n💡 กดแก้ไขเพื่อเติมรูป/แผนที่/ประกัน หรือแก้ชื่อได้`);
                }}
                  className="flex items-center gap-2 bg-sky-50 hover:bg-sky-100 text-sky-700 border border-sky-200 px-3 py-2 rounded-xl font-medium text-sm">
                  🔄 ดึงจากงาน
                </button>
                <button onClick={() => { setEditingItem(null); setShowCustomerModal(true); }}
                  className="flex items-center gap-2 bg-amber-500 hover:bg-amber-600 text-white px-4 py-2 rounded-xl font-medium shadow-sm">
                  <Plus className="w-4 h-4" /> เพิ่มลูกค้า
                </button>
              </div>
            </div>
            
            <div className="grid md:grid-cols-2 gap-4">
              {customers.map(c => {
                const linkedJob = jobs.find(j => j.id === c.jobId);
                return (
                  <div key={c.id} className="bg-white rounded-2xl p-5 shadow-sm border border-stone-200 animate-slide-up">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-1 min-w-0">
                        <h3 className="font-bold text-lg text-stone-800 truncate">{c.name}</h3>
                        <p className="text-sm text-amber-700 font-medium mt-0.5">{c.system}</p>
                      </div>
                      <div className="flex gap-1 flex-shrink-0">
                        <button onClick={() => { setEditingItem(c); setShowCustomerModal(true); }} className="p-1.5 hover:bg-stone-100 rounded-lg">
                          <Edit2 className="w-3.5 h-3.5 text-stone-500" />
                        </button>
                        <button onClick={() => {
                          if (window.confirm(`ลบลูกค้า ${c.name}?`)) {
                            saveCustomers(customers.filter(x => x.id !== c.id), 'delete', `ลบลูกค้า: ${c.name}`);
                          }
                        }} className="p-1.5 hover:bg-red-50 rounded-lg">
                          <Trash2 className="w-3.5 h-3.5 text-red-400" />
                        </button>
                      </div>
                    </div>
                    
                    <div className="space-y-2 text-sm">
                      {c.phone && (
                        <a href={`tel:${c.phone}`} className="flex items-center gap-2 text-blue-600 hover:underline">
                          <Phone className="w-4 h-4" /> {c.phone}
                        </a>
                      )}
                      {c.address && (
                        <div className="flex items-start gap-2 text-stone-600">
                          <MapPin className="w-4 h-4 mt-0.5 flex-shrink-0" />
                          <span className="text-xs">{c.address}</span>
                        </div>
                      )}
                      {c.mapLink && (
                        <a href={c.mapLink} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 text-xs bg-blue-50 text-blue-600 px-2 py-1 rounded-lg hover:bg-blue-100">
                          🗺️ เปิด Google Maps
                        </a>
                      )}
                    </div>

                    <div className="grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-stone-100 text-xs">
                      <div>
                        <div className="text-stone-500">วันติดตั้ง</div>
                        <div className="font-medium">{c.installDate || '-'}</div>
                      </div>
                      {linkedJob && (
                        <div>
                          <div className="text-stone-500">งานเชื่อมโยง</div>
                          <div className="font-medium text-amber-600">{linkedJob.customer}</div>
                        </div>
                      )}
                    </div>

                    {c.warranty && (
                      <div className="mt-3 text-xs bg-emerald-50 text-emerald-700 rounded-lg p-2">
                        🛡️ {c.warranty}
                      </div>
                    )}
                    {c.note && <div className="mt-2 text-xs text-stone-500">💬 {c.note}</div>}

                    {/* 📸 Photo preview */}
                    {c.photos && c.photos.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-stone-100">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-xs font-medium text-stone-600">📸 ผลงาน ({c.photos.length} รูป)</span>
                        </div>
                        <div className="grid grid-cols-4 gap-1.5">
                          {c.photos.slice(0, 4).map((p, i) => (
                            <div
                              key={i}
                              className="relative aspect-square rounded-lg overflow-hidden bg-stone-100 cursor-pointer group"
                              onClick={() => { setEditingItem(c); setShowCustomerModal(true); }}
                            >
                              <img
                                src={p.thumb || p.url}
                                alt=""
                                className="w-full h-full object-cover transition-transform group-hover:scale-110"
                                loading="lazy"
                              />
                              {i === 3 && c.photos.length > 4 && (
                                <div className="absolute inset-0 bg-black/60 flex items-center justify-center text-white font-bold text-sm">
                                  +{c.photos.length - 4}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            {customers.length === 0 && (
              <div className="bg-white rounded-2xl p-8 text-center shadow-sm border border-stone-200">
                <UserCircle className="w-12 h-12 text-stone-300 mx-auto mb-2" />
                <p className="text-stone-500">ยังไม่มีข้อมูลลูกค้า</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'documents' && (() => {
          // Helper: หา jobChainId ของ doc (สำหรับ docs เก่าใช้ id ตัวเอง)
          const getChainId = (doc) => doc.jobChainId || doc.id;
          
          // Helper: หา doc ทั้งหมดของงาน (chain เดียวกัน)
          const getChainDocs = (chainId) => documents.filter(d => getChainId(d) === chainId);
          
          // Helper: หา quotation master ของ chain
          const getMaster = (chainId) => {
            const chainDocs = getChainDocs(chainId);
            return chainDocs.find(d => d.type === 'quotation') || chainDocs[0];
          };
          
          // Helper: หา jobStatus ของ chain (ดูจาก quotation master)
          const getChainStatus = (chainId) => {
            const master = getMaster(chainId);
            return master?.jobStatus || 'active';
          };

          // Helper: คำนวณยอดจ่ายในงาน
          const getChainPaid = (chainId) => {
            const chainDocs = getChainDocs(chainId);
            return chainDocs
              .filter(d => d.type === 'receipt-deposit' || d.type === 'receipt-final' || d.type === 'receipt')
              .reduce((sum, d) => sum + Number(d.totalAmount || 0), 0);
          };

          // === Actions ===
          
          // สร้างเอกสารใหม่จาก source โดยใช้ jobChainId เดียวกัน
          const cloneFromDoc = (sourceDoc, newType) => {
            const chainId = getChainId(sourceDoc);
            const isReceiptDeposit = newType === 'receipt-deposit';
            const isReceiptFinal = newType === 'receipt-final';
            
            // ถ้าเป็น RC มัดจำ: เอาเงินมัดจำจาก quotation มาเป็นยอด
            // ถ้าเป็น RC เต็ม: เอายอด "ค้างจ่าย" = ยอดเต็ม - มัดจำที่จ่ายไปแล้ว
            let totalAmount = sourceDoc.totalAmount;
            let items = sourceDoc.items.map(it => ({ ...it, id: `item-${Date.now()}-${Math.random().toString(36).slice(2,5)}` }));
            
            if (isReceiptDeposit && Number(sourceDoc.depositAmount || 0) > 0) {
              totalAmount = Number(sourceDoc.depositAmount);
              items = [{
                id: `item-${Date.now()}`,
                name: `เงินมัดจำสำหรับ ${sourceDoc.docNumber}`,
                qty: 1, unit: 'รายการ',
                unitPrice: totalAmount,
                amount: totalAmount,
              }];
            }
            
            // RC เต็ม: หักมัดจำที่จ่ายไปแล้วในงานนี้
            if (isReceiptFinal) {
              const chainDocs = getChainDocs(chainId);
              const depositPaid = chainDocs
                .filter(d => d.type === 'receipt-deposit')
                .reduce((sum, d) => sum + Number(d.totalAmount || 0), 0);
              
              const totalBill = Number(sourceDoc.totalAmount || 0);
              const remaining = totalBill - depositPaid;
              
              if (depositPaid > 0 && remaining > 0) {
                // มีจ่ายมัดจำมาแล้ว → RC เต็ม คิดเฉพาะส่วนค้าง
                totalAmount = remaining;
                items = [{
                  id: `item-${Date.now()}`,
                  name: `ชำระส่วนที่เหลือ (ยอดรวม ${totalBill.toLocaleString()} ฿ - มัดจำ ${depositPaid.toLocaleString()} ฿)`,
                  qty: 1, unit: 'รายการ',
                  unitPrice: totalAmount,
                  amount: totalAmount,
                }];
              }
              // ถ้าไม่เคยจ่ายมัดจำ → ใช้ยอดเต็มตามเดิม (ลูกค้าจ่ายครั้งเดียว)
            }
            
            const newDoc = {
              id: `doc-${Date.now()}`,
              type: newType,
              docNumber: generateDocNumber(newType, documents),
              docDate: new Date().toISOString().split('T')[0],
              validUntil: '',
              customerId: sourceDoc.customerId || '',
              customerName: sourceDoc.customerName || '',
              customerPhone: sourceDoc.customerPhone || '',
              customerAddress: sourceDoc.customerAddress || '',
              items,
              subtotal: items.reduce((s, it) => s + Number(it.amount || 0), 0),
              discount: 0,
              totalAmount,
              paymentTerms: sourceDoc.paymentTerms || '',
              depositPercent: 0,
              depositAmount: 0,
              warrantyText: newType === 'receipt-final' ? (sourceDoc.warrantyText || '') : '',
              notes: '',
              jobId: sourceDoc.jobId || '',
              jobChainId: chainId,           // ✨ เชื่อม chain
              jobStatus: 'active',
              status: 'active',               // legacy field
              linkedDocId: sourceDoc.id,
              createdAt: new Date().toISOString(),
            };
            
            const typeLabel = getDocTypeInfo(newType).label;
            saveDocuments([...documents, newDoc], 'add',
              `สร้าง${typeLabel} ${newDoc.docNumber} จาก ${sourceDoc.docNumber}`);
            setEditingItem(newDoc);
            setDefaultDocType(newType);
            setTimeout(() => setShowDocumentModal(true), 100);
          };

          // === สร้างงานจากใบเสนอราคา ===
          const createJobFromQuotation = (quotation) => {
            // ตรวจสอบไม่ให้สร้างซ้ำ
            if (quotation.jobId) {
              const existJob = jobs.find(j => j.id === quotation.jobId);
              if (existJob) {
                if (window.confirm(`ใบเสนอราคานี้มีงานอยู่แล้ว: ${existJob.customer || existJob.customerName}\n\nไปที่งานเลย?`)) {
                  setActiveTab('jobs');
                }
                return;
              }
            }
            
            const snap = quotation.equipmentSnapshot || {};
            const items = quotation.items || [];
            const itemDesc = items[0]?.name || '';
            
            // สร้าง job draft (format เดียวกับ PickQuotation)
            const draftJob = {
              date: new Date().toISOString().split('T')[0],
              customer: quotation.customerName || '',
              phone: quotation.customerPhone || '',
              location: quotation.customerAddress || '',
              type: snap.jobType || quotation.jobType || itemDesc.split('\n')[0] || '',
              salePrice: Number(quotation.totalAmount || 0),
              originalPrice: Number(quotation.totalAmount || 0),
              discount: 0,
              discountNote: '',
              status: 'pending',
              investments: {},
              costsByCategory: {},
              totalCost: snap.totalCost || quotation.expectedCost || 0,
              profit: snap.expectedProfit || quotation.expectedProfit || 0,
              note: `สร้างจากใบเสนอราคา ${quotation.docNumber}`,
              quotationId: quotation.id,  // ✨ เชื่อมกลับ
              docNumber: quotation.docNumber,
              expectedProfit: snap.expectedProfit || quotation.expectedProfit || 0,
              expectedCost: snap.totalCost || quotation.expectedCost || 0,
            };
            
            setEditingItem(draftJob);
            setActiveTab('jobs');
            setTimeout(() => setShowJobModal(true), 200);
          };

          // จบงาน — กระทำที่ chain → ทุกใบเข้า archive
          const closeChain = (chainId) => {
            const master = getMaster(chainId);
            const chainDocs = getChainDocs(chainId);
            const total = Number(master?.totalAmount || 0);
            const paid = getChainPaid(chainId);
            const unpaid = total - paid;
            
            // ค้นหา job ที่ผูกกับ chain นี้
            let linkedJob = jobs.find(j => 
              j.quotationId === master?.id || 
              j.quotationId === chainId ||
              (master?.jobId && j.id === master.jobId)
            );
            
            // ===== 📋 CLOSING CEREMONY: ตรวจสอบความครบถ้วน =====
            const checks = [];
            const autoActions = [];
            
            // ✓ Check 1: รายได้บันทึกครบยอดขายหรือยัง? (รองรับมัดจำบางส่วน)
            const incomeTx = linkedJob ? transactions.filter(t => 
              t.type === 'income' && t.category === 'รายได้จากงาน' && t.jobId === linkedJob.id && !t.isService
            ) : [];
            const incomeRecorded = incomeTx.reduce((s, t) => s + Number(t.amount || 0), 0);
            const salePrice = Number(linkedJob?.salePrice || master?.totalAmount || 0);
            const incomeShortfall = salePrice - incomeRecorded;
            
            if (linkedJob && incomeShortfall > 0.5) {
              checks.push(incomeRecorded > 0
                ? `⚠️ รายได้บันทึกแล้ว ${incomeRecorded.toLocaleString()} ฿ ขาดอีก ${incomeShortfall.toLocaleString()} ฿ → จะสร้างส่วนที่ขาดให้`
                : `⚠️ ยังไม่บันทึกรายได้ → จะสร้างให้ (+${salePrice.toLocaleString()} ฿)`);
              autoActions.push({
                kind: 'income',
                tx: {
                  id: `t-close-${Date.now()}-i`,
                  date: new Date().toISOString().split('T')[0],
                  type: 'income',
                  category: 'รายได้จากงาน',
                  amount: incomeShortfall,
                  description: incomeRecorded > 0
                    ? `${linkedJob.customer} - รับเงินส่วนที่เหลือ (ปิดงาน)`
                    : `${linkedJob.customer} - ${linkedJob.system || 'งานติดตั้ง'}`,
                  jobId: linkedJob.id,
                  partnerId: '',
                  createdBy: `${currentUser.name} (ปิดงานอัตโนมัติ)`,
                  createdAt: new Date().toISOString(),
                },
              });
            } else if (linkedJob && salePrice > 0) {
              checks.push(`✅ รายได้บันทึกครบ (${incomeRecorded.toLocaleString()} ฿)`);
              if (incomeRecorded > salePrice + 0.5) {
                checks.push(`⚠️ รายได้บันทึกเกินยอดขาย ${(incomeRecorded - salePrice).toLocaleString()} ฿ — ตรวจสอบรายการซ้ำใน Tab การเงิน`);
              }
            }
            
            // ✓ Check 2: ต้นทุนงานบันทึกหรือยัง? (ของที่จ่ายจริง ไม่นับเบิกสต๊อก)
            const jobCostTx = linkedJob ? transactions.filter(t => 
              t.type === 'expense' && t.category === 'ต้นทุนงาน' && t.jobId === linkedJob.id && !t.isService
            ) : [];
            const costRecorded = jobCostTx.reduce((s, t) => s + Number(t.amount || 0), 0);
            
            // คำนวณต้นทุนจริงที่ "จ่ายเงิน" (ไม่นับของจากสต๊อก)
            let cashCost = 0;
            let stockCost = 0;
            if (linkedJob?.costsByCategory) {
              Object.values(linkedJob.costsByCategory).forEach(items => {
                (items || []).forEach(item => {
                  const amt = Number(item.amount || 0);
                  if (item.stockId) stockCost += amt;
                  else cashCost += amt;
                });
              });
            }
            
            if (linkedJob && costRecorded === 0 && cashCost > 0) {
              checks.push(`⚠️ ยังไม่บันทึกต้นทุน → จะสร้างให้ (-${cashCost.toLocaleString()} ฿)`);
              autoActions.push({
                kind: 'expense',
                tx: {
                  id: `t-close-${Date.now()}-e`,
                  date: new Date().toISOString().split('T')[0],
                  type: 'expense',
                  category: 'ต้นทุนงาน',
                  amount: cashCost,
                  description: `ต้นทุนงาน ${linkedJob.customer} (จ่ายจริง ไม่รวมของจากสต๊อก)`,
                  jobId: linkedJob.id,
                  partnerId: '',
                  createdBy: `${currentUser.name} (ปิดงานอัตโนมัติ)`,
                  createdAt: new Date().toISOString(),
                },
              });
            } else if (costRecorded > 0) {
              checks.push(`✅ ต้นทุนบันทึกแล้ว (${costRecorded.toLocaleString()} ฿)`);
            }
            
            // ✓ Check 3: สายไฟม้วนใหม่ ของเหลือ
            const wireRemainings = [];
            if (linkedJob && linkedJob.costsByCategory?.wire) {
              linkedJob.costsByCategory.wire.forEach(item => {
                if (!item.stockId && Number(item.rollLength || 0) > 0) {
                  const remaining = Number(item.rollLength || 0) - Number(item.usedLength || 0);
                  const pricePerMeter = item.rollLength > 0 ? item.rollPrice / item.rollLength : 0;
                  if (remaining > 0) {
                    wireRemainings.push({
                      name: item.item,
                      remaining,
                      pricePerMeter,
                      unitCost: pricePerMeter,
                    });
                  }
                }
              });
            }
            if (wireRemainings.length > 0) {
              const wireList = wireRemainings.map(w => 
                `   • ${w.name}: ${w.remaining.toFixed(1)}m (${(w.remaining * w.unitCost).toLocaleString(undefined, {maximumFractionDigits: 0})} ฿)`
              ).join('\n');
              checks.push(`📦 ของเหลือจะเข้าสต๊อก:\n${wireList}`);
            }
            
            // ✓ Check 4: เงินค้าง
            if (unpaid > 0) {
              checks.push(`⚠️ ลูกค้าค้างจ่าย ${unpaid.toLocaleString()} ฿ (รับแล้ว ${paid.toLocaleString()}/${total.toLocaleString()})`);
            } else if (total > 0) {
              checks.push(`✅ รับเงินครบ (${paid.toLocaleString()} ฿)`);
            }
            
            // กำไรสรุป
            const totalCostAll = cashCost + stockCost;
            const profit = salePrice - totalCostAll;
            
            // ===== แสดงสรุปก่อนยืนยัน =====
            const summaryMsg = 
              `📋 สรุปก่อนปิดงาน — ${master?.customerName || linkedJob?.customer || '-'}\n` +
              `${'─'.repeat(36)}\n` +
              `💰 ราคาขาย:    ${salePrice.toLocaleString()} ฿\n` +
              `💸 ต้นทุนรวม:  ${totalCostAll.toLocaleString()} ฿\n` +
              (stockCost > 0 ? `   ├─ จากสต๊อก: ${stockCost.toLocaleString()} ฿\n   └─ จ่ายจริง:  ${cashCost.toLocaleString()} ฿\n` : '') +
              `📈 กำไร:       ${profit.toLocaleString()} ฿\n` +
              `${'─'.repeat(36)}\n` +
              checks.join('\n') +
              `\n${'─'.repeat(36)}\n` +
              `เอกสาร ${chainDocs.length} ฉบับจะถูกเก็บเข้าประวัติ\n` +
              `หลังปิดงาน ตัวเลขจะถูกล็อก\n\n` +
              `ยืนยันปิดงาน?`;
            
            if (!window.confirm(summaryMsg)) return;
            
            const closedAt = new Date().toISOString();
            
            // 1. สร้าง transactions ที่ขาด (รายได้/ต้นทุน)
            if (autoActions.length > 0) {
              const newTxs = [...transactions, ...autoActions.map(a => a.tx)];
              saveTransactions(newTxs, 'add', 
                `🔒 ปิดงาน ${master?.customerName}: สร้าง ${autoActions.length} รายการการเงินอัตโนมัติ`);
            }
            
            // 2. ปิดเอกสาร
            saveDocuments(
              documents.map(d => getChainId(d) === chainId ? { ...d, jobStatus: 'closed', status: 'closed', closedAt, closedBy: currentUser.name } : d),
              'edit',
              `🔒 ปิดงาน: ${master?.docNumber} (${master?.customerName}) โดย ${currentUser.name}`
            );
            
            // 3. อัพเดทสถานะงาน + ล็อก
            if (linkedJob) {
              saveJobs(
                jobs.map(j => j.id === linkedJob.id ? { ...j, status: 'completed', closedAt, closedBy: currentUser.name, locked: true, workflowStep: Math.max(Number(j.workflowStep || 0), 10) } : j),
                'edit',
                `🔒 ปิดงาน: ${linkedJob.customer} (กำไร ${profit.toLocaleString()} ฿)`
              );
            }
            
            // 4. บันทึกสายไฟเหลือเข้าสต๊อก
            if (wireRemainings.length > 0) {
              const newStock = [...stock];
              wireRemainings.forEach(w => {
                const existing = newStock.find(s => 
                  s.category === 'wire' && s.name === w.name
                );
                if (existing) {
                  const oldQty = Number(existing.qty || 0);
                  const oldCost = Number(existing.unitCost || 0);
                  const newQty = oldQty + w.remaining;
                  const newCost = newQty > 0 ? ((oldQty * oldCost) + (w.remaining * w.unitCost)) / newQty : w.unitCost;
                  existing.qty = newQty;
                  existing.unitCost = Number(newCost.toFixed(2));
                } else {
                  newStock.push({
                    id: `s-wire-${Date.now()}-${Math.random().toString(36).slice(2,5)}`,
                    name: w.name,
                    category: 'wire',
                    qty: w.remaining,
                    unit: 'เมตร',
                    unitCost: Number(w.unitCost.toFixed(2)),
                    partner: '',
                    note: `เหลือจากงาน ${master?.customerName || master?.docNumber}`,
                    createdAt: closedAt,
                  });
                }
              });
              saveStock(newStock, 'add', 
                `📦 ของเหลือเข้าสต๊อก ${wireRemainings.length} รายการ จากงาน ${master?.customerName}`);
            }
            
            // 5. แจ้งผลสรุป
            setTimeout(() => {
              let resultMsg = `✅ ปิดงานเรียบร้อย!\n\n📈 กำไรงานนี้: ${profit.toLocaleString()} ฿`;
              if (autoActions.length > 0) {
                resultMsg += `\n💰 สร้างรายการการเงินอัตโนมัติ ${autoActions.length} รายการ`;
              }
              if (wireRemainings.length > 0) {
                resultMsg += `\n📦 ของเหลือเข้าสต๊อก ${wireRemainings.length} รายการ`;
              }
              alert(resultMsg);
            }, 100);
          };

          // ยกเลิกงาน
          const cancelChain = (chainId) => {
            const master = getMaster(chainId);
            const chainDocs = getChainDocs(chainId);
            
            if (!window.confirm(`ยกเลิกงาน ${master?.docNumber || '-'}\n(${master?.customerName || '-'})\n\nเอกสารทั้งหมดในงานนี้ (${chainDocs.length} ฉบับ) จะเปลี่ยนสถานะเป็น "ยกเลิก"\n\nยืนยันยกเลิก?`)) return;
            
            const cancelledAt = new Date().toISOString();
            saveDocuments(
              documents.map(d => getChainId(d) === chainId ? { ...d, jobStatus: 'cancelled', status: 'cancelled', cancelledAt } : d),
              'edit',
              `ยกเลิกงาน: ${master?.docNumber} (${master?.customerName})`
            );
          };

          // เปิดงานใหม่ (จาก closed/cancelled กลับเป็น active)
          const reopenChain = (chainId) => {
            const master = getMaster(chainId);
            saveDocuments(
              documents.map(d => getChainId(d) === chainId ? { ...d, jobStatus: 'active', status: 'active' } : d),
              'edit',
              `เปิดงานใหม่: ${master?.docNumber}`
            );
          };

          // === Group documents by chain ===
          // จัดกลุ่มเอกสารตาม jobChainId
          const chainsMap = {};
          documents.forEach(doc => {
            const chainId = getChainId(doc);
            if (!chainsMap[chainId]) {
              chainsMap[chainId] = { chainId, docs: [], jobStatus: getChainStatus(chainId) };
            }
            chainsMap[chainId].docs.push(doc);
          });
          let chains = Object.values(chainsMap);

          // Filter
          if (docFilter === 'closed') {
            chains = chains.filter(c => c.jobStatus === 'closed');
          } else if (docFilter === 'cancelled') {
            chains = chains.filter(c => c.jobStatus === 'cancelled');
          } else if (docFilter === 'active') {
            chains = chains.filter(c => c.jobStatus === 'active');
          } else {
            // กรอง type → แสดง chain ที่มี doc ประเภทนั้นและ active
            chains = chains.filter(c => 
              c.jobStatus === 'active' && c.docs.some(d => d.type === docFilter)
            );
          }

          // Search
          if (docSearch.trim()) {
            const q = docSearch.toLowerCase();
            chains = chains.filter(c =>
              c.docs.some(d =>
                (d.customerName || '').toLowerCase().includes(q) ||
                (d.docNumber || '').toLowerCase().includes(q)
              )
            );
          }
          
          // Sort: ล่าสุดก่อน (ดูจาก master)
          chains.sort((a, b) => {
            const aMaster = getMaster(a.chainId);
            const bMaster = getMaster(b.chainId);
            return (aMaster?.createdAt || '') < (bMaster?.createdAt || '') ? 1 : -1;
          });

          // Counts (chain-based)
          const counts = {
            active: Object.values(chainsMap).filter(c => c.jobStatus === 'active').length,
            closed: Object.values(chainsMap).filter(c => c.jobStatus === 'closed').length,
            cancelled: Object.values(chainsMap).filter(c => c.jobStatus === 'cancelled').length,
            quotation: documents.filter(d => d.type === 'quotation' && getChainStatus(getChainId(d)) === 'active').length,
            invoice: documents.filter(d => d.type === 'invoice' && getChainStatus(getChainId(d)) === 'active').length,
            'receipt-deposit': documents.filter(d => d.type === 'receipt-deposit' && getChainStatus(getChainId(d)) === 'active').length,
            'receipt-final': documents.filter(d => (d.type === 'receipt-final' || d.type === 'receipt') && getChainStatus(getChainId(d)) === 'active').length,
          };

          return (
          <div className="space-y-4 animate-fade-in">
            <div className="flex items-center justify-between flex-wrap gap-2">
              <div>
                <h2 className="display-font text-3xl text-stone-800">งานเอกสาร</h2>
                <p className="text-sm text-stone-500">ใบเสนอราคา · ใบแจ้งหนี้ · ใบเสร็จรับเงิน</p>
              </div>
              <button onClick={() => setShowCompanySettings(true)}
                className="bg-stone-200 hover:bg-stone-300 text-stone-700 px-3 py-2 rounded-xl flex items-center gap-1 text-sm">
                ⚙️ ข้อมูลบริษัท
              </button>
            </div>

            {/* Quick Action Buttons */}
            <div className="bg-gradient-to-br from-stone-50 to-stone-100 rounded-2xl p-3 border border-stone-200">
              <p className="text-xs font-medium text-stone-600 mb-2 px-1">📝 สร้างเอกสารใหม่</p>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                <button onClick={() => { setEditingItem(null); setDefaultDocType('quotation'); setShowDocumentModal(true); }}
                  className="bg-white hover:bg-blue-50 border-2 border-blue-200 hover:border-blue-400 rounded-xl p-3 text-center transition-all active:scale-95">
                  <div className="text-2xl mb-1">📄</div>
                  <div className="text-xs font-bold text-blue-700">ใบเสนอราคา</div>
                  <div className="text-xs text-stone-400 mt-1">{counts.quotation} ฉบับ</div>
                </button>
                <button onClick={() => { setEditingItem(null); setDefaultDocType('invoice'); setShowDocumentModal(true); }}
                  className="bg-white hover:bg-amber-50 border-2 border-amber-200 hover:border-amber-400 rounded-xl p-3 text-center transition-all active:scale-95">
                  <div className="text-2xl mb-1">🧾</div>
                  <div className="text-xs font-bold text-amber-700">ใบแจ้งหนี้</div>
                  <div className="text-xs text-stone-400 mt-1">{counts.invoice} ฉบับ</div>
                </button>
                <button onClick={() => { setEditingItem(null); setDefaultDocType('receipt-deposit'); setShowDocumentModal(true); }}
                  className="bg-white hover:bg-cyan-50 border-2 border-cyan-200 hover:border-cyan-400 rounded-xl p-3 text-center transition-all active:scale-95">
                  <div className="text-2xl mb-1">💰</div>
                  <div className="text-xs font-bold text-cyan-700">RC มัดจำ</div>
                  <div className="text-xs text-stone-400 mt-1">{counts['receipt-deposit']} ฉบับ</div>
                </button>
                <button onClick={() => { setEditingItem(null); setDefaultDocType('receipt-final'); setShowDocumentModal(true); }}
                  className="bg-white hover:bg-emerald-50 border-2 border-emerald-200 hover:border-emerald-400 rounded-xl p-3 text-center transition-all active:scale-95">
                  <div className="text-2xl mb-1">✅</div>
                  <div className="text-xs font-bold text-emerald-700">RC เต็ม</div>
                  <div className="text-xs text-stone-400 mt-1">{counts['receipt-final']} ฉบับ</div>
                </button>
              </div>
            </div>

            {/* Search */}
            {documents.length > 0 && (
              <div className="relative">
                <input
                  type="text"
                  value={docSearch}
                  onChange={e => setDocSearch(e.target.value)}
                  placeholder="🔍 ค้นหาเอกสาร (ชื่อลูกค้า / เลขที่บิล)..."
                  className="w-full px-4 py-2.5 pr-10 border border-stone-300 rounded-xl bg-white focus:ring-2 focus:ring-amber-400 focus:border-transparent text-sm"
                />
                {docSearch && (
                  <button onClick={() => setDocSearch('')}
                    className="absolute right-2 top-1/2 -translate-y-1/2 p-1 hover:bg-stone-100 rounded">
                    <X className="w-4 h-4 text-stone-400" />
                  </button>
                )}
              </div>
            )}

            {/* Filter Tabs */}
            {documents.length > 0 && (
              <div className="flex gap-1.5 overflow-x-auto pb-1 -mx-1 px-1">
                {[
                  { id: 'active', label: '🔧 กำลังดำเนินการ', count: counts.active },
                  { id: 'quotation', label: '📄 ใบเสนอราคา', count: counts.quotation },
                  { id: 'invoice', label: '🧾 ใบแจ้งหนี้', count: counts.invoice },
                  { id: 'receipt-deposit', label: '💰 RC มัดจำ', count: counts['receipt-deposit'] },
                  { id: 'receipt-final', label: '✅ RC เต็ม', count: counts['receipt-final'] },
                  { id: 'closed', label: '📁 จบงานแล้ว', count: counts.closed },
                  { id: 'cancelled', label: '❌ ยกเลิก', count: counts.cancelled },
                ].map(f => (
                  <button key={f.id} onClick={() => setDocFilter(f.id)}
                    className={`flex-shrink-0 px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap transition-all ${
                      docFilter === f.id
                        ? 'bg-stone-800 text-white'
                        : 'bg-white border border-stone-200 text-stone-600 hover:bg-stone-50'
                    }`}>
                    {f.label} <span className="opacity-70">({f.count})</span>
                  </button>
                ))}
              </div>
            )}

            {/* Document List - Grouped by Chain */}
            {documents.length === 0 ? (
              <div className="bg-white rounded-2xl p-8 text-center shadow-sm border border-stone-200">
                <Save className="w-12 h-12 text-stone-300 mx-auto mb-2" />
                <p className="text-stone-500 mb-1">ยังไม่มีเอกสาร</p>
                <p className="text-xs text-stone-400">เริ่มจากกดปุ่มสร้างเอกสารด้านบน</p>
              </div>
            ) : chains.length === 0 ? (
              <div className="bg-white rounded-2xl p-8 text-center shadow-sm border border-stone-200">
                <p className="text-stone-500 text-sm">ไม่พบงานตามเงื่อนไขที่ค้นหา</p>
              </div>
            ) : (
              <div className="space-y-3">
                {chains.map(chain => {
                  const master = getMaster(chain.chainId);
                  if (!master) return null;
                  
                  const chainDocs = [...chain.docs].sort((a, b) => 
                    (a.createdAt || '') < (b.createdAt || '') ? -1 : 1
                  );
                  
                  // ถ้า filter เป็นประเภทเอกสาร → highlight เอกสารประเภทนั้น
                  const docTypeFilters = ['quotation', 'invoice', 'receipt-deposit', 'receipt-final'];
                  const isDocTypeFilter = docTypeFilters.includes(docFilter);
                  const isHighlighted = (doc) => {
                    if (!isDocTypeFilter) return false;
                    if (docFilter === 'receipt-final') return doc.type === 'receipt-final' || doc.type === 'receipt';
                    return doc.type === docFilter;
                  };
                  
                  const total = Number(master.totalAmount || 0);
                  const paid = getChainPaid(chain.chainId);
                  const unpaid = total - paid;
                  
                  const statusInfo = {
                    active: { label: '🔧 กำลังดำเนินการ', color: 'amber' },
                    closed: { label: '✅ จบงานแล้ว', color: 'emerald' },
                    cancelled: { label: '❌ ยกเลิก', color: 'rose' },
                  }[chain.jobStatus] || { label: '-', color: 'stone' };
                  
                  const isActive = chain.jobStatus === 'active';
                  const isCancelled = chain.jobStatus === 'cancelled';
                  const isClosedJob = chain.jobStatus === 'closed';
                  
                  // เช็คมีเอกสารประเภทไหนบ้างใน chain
                  const hasInvoice = chainDocs.some(d => d.type === 'invoice');
                  const hasReceiptDeposit = chainDocs.some(d => d.type === 'receipt-deposit');
                  const hasReceiptFinal = chainDocs.some(d => d.type === 'receipt-final' || d.type === 'receipt');
                  
                  return (
                    <div key={chain.chainId} className={`bg-white rounded-2xl shadow-sm border-2 animate-slide-up overflow-hidden ${
                      isCancelled ? 'border-rose-200 opacity-60' : 
                      isClosedJob ? 'border-emerald-200 opacity-70' : 
                      'border-amber-200'
                    }`}>
                      {/* Job Header */}
                      <div className={`p-4 ${
                        isCancelled ? 'bg-rose-50' : 
                        isClosedJob ? 'bg-emerald-50' : 
                        'bg-amber-50'
                      }`}>
                        <div className="flex items-start justify-between gap-2">
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 flex-wrap mb-1">
                              <span className={`text-xs px-2 py-0.5 rounded-full bg-${statusInfo.color}-100 text-${statusInfo.color}-700 font-medium border border-${statusInfo.color}-200`}>
                                {statusInfo.label}
                              </span>
                              <span className="text-xs text-stone-500">{chainDocs.length} เอกสาร</span>
                            </div>
                            <h3 className="font-bold text-lg text-stone-800 truncate">{master.customerName || '-'}</h3>
                            <div className="flex items-center gap-3 mt-1 text-xs">
                              <span className="text-stone-600">💰 ยอด: <strong>{fmt(total)} ฿</strong></span>
                              {paid > 0 && (
                                <span className="text-emerald-700">✓ จ่าย: <strong>{fmt(paid)} ฿</strong></span>
                              )}
                              {unpaid > 0 && isActive && (
                                <span className="text-rose-700">⚠ ค้าง: <strong>{fmt(unpaid)} ฿</strong></span>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* Doc List */}
                      <div className="divide-y divide-stone-100">
                        {chainDocs.map(doc => {
                          const typeInfo = getDocTypeInfo(doc.type);
                          const highlight = isHighlighted(doc);
                          return (
                            <div key={doc.id} className={`p-3 flex items-center gap-3 transition-colors ${
                              highlight 
                                ? 'bg-amber-100 hover:bg-amber-200 border-l-4 border-amber-500' 
                                : 'hover:bg-stone-50'
                            }`}>
                              <div className="text-2xl flex-shrink-0">{typeInfo.icon}</div>
                              <div className="flex-1 min-w-0">
                                <div className="flex items-center gap-2 flex-wrap">
                                  <span className={`text-xs px-1.5 py-0.5 rounded bg-${typeInfo.color}-100 text-${typeInfo.color}-700 font-medium`}>
                                    {typeInfo.shortLabel}
                                  </span>
                                  <span className="font-mono text-xs text-stone-600">{doc.docNumber}</span>
                                  {highlight && <span className="text-[10px] text-amber-700 font-bold">⭐ ค้นพบ</span>}
                                </div>
                                <div className="text-xs text-stone-500 mt-0.5">
                                  {doc.docDate} · {fmt(doc.totalAmount || 0)} ฿
                                </div>
                              </div>
                              <div className="flex gap-0.5 flex-shrink-0">
                                <button onClick={() => { setPreviewDoc(doc); setShowDocumentPreview(true); }}
                                  className="p-1.5 hover:bg-blue-50 rounded-lg" title="ดู/พิมพ์">
                                  <Eye className="w-4 h-4 text-blue-500" />
                                </button>
                                {isActive && (
                                  <button onClick={() => { setEditingItem(doc); setShowDocumentModal(true); }}
                                    className="p-1.5 hover:bg-stone-100 rounded-lg" title="แก้ไข">
                                    <Edit2 className="w-4 h-4 text-stone-500" />
                                  </button>
                                )}
                                <button onClick={() => {
                                  // เช็คว่ามี income ผูกกับใบเสร็จนี้ไหม
                                  const linkedTx = transactions.find(t => t.sourceDocId === doc.id);
                                  const txWarn = linkedTx
                                    ? `\n\n💰 รายการรายได้ที่ผูกอยู่ (+${Number(linkedTx.amount).toLocaleString()} ฿) จะถูกลบด้วย`
                                    : '';
                                  if (window.confirm(`ลบ ${typeInfo.label} ${doc.docNumber}?${txWarn}\n\n⚠️ การลบไม่สามารถกู้คืนได้ และจะถูกบันทึกในประวัติ`)) {
                                    saveDocuments(documents.filter(x => x.id !== doc.id), 'delete', `🗑️ ลบ ${typeInfo.label}: ${doc.docNumber}`);
                                    if (linkedTx) {
                                      saveTransactions(transactions.filter(t => t.id !== linkedTx.id), 'delete',
                                        `🗑️ ลบรายได้ที่ผูกกับใบเสร็จ ${doc.docNumber}: -${Number(linkedTx.amount).toLocaleString()} ฿`);
                                    }
                                  }
                                }} className="p-1.5 hover:bg-red-50 rounded-lg" title="ลบเอกสารนี้">
                                  <Trash2 className="w-4 h-4 text-red-400" />
                                </button>
                              </div>
                            </div>
                          );
                        })}
                      </div>

                      {/* Job Actions */}
                      {isActive && (
                        <div className="p-3 bg-stone-50 border-t border-stone-100 flex gap-1.5 flex-wrap">
                          {/* ปุ่มสร้างงาน — ถ้ายังไม่มี jobId */}
                          {!master.jobId && master.type === 'quotation' && (
                            <button onClick={() => createJobFromQuotation(master)}
                              className="text-xs bg-violet-500 hover:bg-violet-600 text-white border border-violet-600 px-3 py-1.5 rounded-lg font-medium">
                              🚀 สร้างงาน
                            </button>
                          )}
                          {master.jobId && (
                            <button onClick={() => { setActiveTab('jobs'); }}
                              className="text-xs bg-violet-50 hover:bg-violet-100 text-violet-700 border border-violet-200 px-3 py-1.5 rounded-lg font-medium">
                              📋 ดูงาน
                            </button>
                          )}
                          {!hasReceiptDeposit && Number(master.depositAmount || 0) > 0 && (
                            <button onClick={() => cloneFromDoc(master, 'receipt-deposit')}
                              className="text-xs bg-cyan-50 hover:bg-cyan-100 text-cyan-700 border border-cyan-200 px-3 py-1.5 rounded-lg font-medium">
                              💰 RC มัดจำ
                            </button>
                          )}
                          {!hasInvoice && (
                            <button onClick={() => cloneFromDoc(master, 'invoice')}
                              className="text-xs bg-amber-50 hover:bg-amber-100 text-amber-700 border border-amber-200 px-3 py-1.5 rounded-lg font-medium">
                              🧾 ใบแจ้งหนี้
                            </button>
                          )}
                          {!hasReceiptFinal && (
                            <button onClick={() => cloneFromDoc(master, 'receipt-final')}
                              className="text-xs bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 px-3 py-1.5 rounded-lg font-medium">
                              ✅ RC เต็ม
                            </button>
                          )}
                          <button onClick={() => {
                            const m = getMaster(chain.chainId);
                            const lj = jobs.find(j => j.quotationId === m?.id || j.quotationId === chain.chainId || (m?.jobId && j.id === m.jobId));
                            setCustomerGuide({ customerName: m?.customerName || '', systemType: lj?.type || '' });
                          }}
                            className="text-xs bg-sky-50 hover:bg-sky-100 text-sky-700 border border-sky-200 px-3 py-1.5 rounded-lg font-medium ml-auto">
                            📱 คู่มือลูกค้า
                          </button>
                          <button onClick={() => closeChain(chain.chainId)}
                            className="text-xs bg-emerald-500 hover:bg-emerald-600 text-white px-3 py-1.5 rounded-lg font-medium">
                            ✅ จบงาน
                          </button>
                          <button onClick={() => cancelChain(chain.chainId)}
                            className="text-xs bg-rose-100 hover:bg-rose-200 text-rose-700 px-3 py-1.5 rounded-lg font-medium">
                            ❌ ยกเลิก
                          </button>
                        </div>
                      )}
                      {(isClosedJob || isCancelled) && (
                        <div className="p-3 bg-stone-50 border-t border-stone-100 flex justify-between items-center">
                          <span className="text-xs text-stone-500">
                            {isClosedJob ? 'จบงานเมื่อ' : 'ยกเลิกเมื่อ'} {' '}
                            {(() => {
                              const date = master.closedAt || master.cancelledAt;
                              return date ? new Date(date).toLocaleDateString('th-TH') : '-';
                            })()}
                          </span>
                          <button onClick={() => reopenChain(chain.chainId)}
                            className="text-xs bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 px-3 py-1.5 rounded-lg font-medium">
                            🔓 เปิดงานใหม่
                          </button>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
          );
        })()}

        {activeTab === 'activity' && (
          <div className="space-y-4 animate-fade-in">
            <div>
              <h2 className="display-font text-3xl text-stone-800">ประวัติการแก้ไข</h2>
              <p className="text-sm text-stone-500">{activityLog.length} รายการ · เก็บล่าสุด 500 รายการ</p>
            </div>

            {activityLog.length === 0 ? (
              <div className="bg-white rounded-2xl p-8 text-center shadow-sm border border-stone-200">
                <Activity className="w-12 h-12 text-stone-300 mx-auto mb-2" />
                <p className="text-stone-500">ยังไม่มีประวัติ</p>
                <p className="text-xs text-stone-400 mt-1">ระบบจะบันทึกทุกการเพิ่ม/แก้/ลบ พร้อมชื่อคนทำ</p>
              </div>
            ) : (
              <div className="bg-white rounded-2xl shadow-sm border border-stone-200 overflow-hidden">
                {activityLog.map(log => {
                  const user = Object.values(USERS).find(u => u.id === log.userId);
                  const actionColors = {
                    add: 'bg-emerald-100 text-emerald-700',
                    edit: 'bg-blue-100 text-blue-700',
                    delete: 'bg-rose-100 text-rose-700',
                    export: 'bg-purple-100 text-purple-700',
                  };
                  const actionLabels = {
                    add: '+ เพิ่ม',
                    edit: '✎ แก้ไข',
                    delete: '× ลบ',
                    export: '↓ Export',
                  };
                  const date = new Date(log.timestamp);
                  return (
                    <div key={log.id} className="flex items-start gap-3 p-3 border-b border-stone-100 last:border-0 hover:bg-stone-50">
                      <div className="text-2xl flex-shrink-0">{user?.icon || '👤'}</div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="font-medium">{log.userName}</span>
                          <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${actionColors[log.action] || 'bg-stone-100 text-stone-600'}`}>
                            {actionLabels[log.action] || log.action}
                          </span>
                          <span className="text-xs text-amber-600 font-medium">{log.target}</span>
                        </div>
                        {log.details && <p className="text-sm text-stone-600 mt-0.5">{log.details}</p>}
                        <p className="text-xs text-stone-400 mt-0.5">
                          {date.toLocaleDateString('th-TH')} {date.toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit' })}
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}

            <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4">
              <div className="flex gap-3">
                <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                <div className="text-sm text-stone-700">
                  <strong>ระบบบันทึกอัตโนมัติ:</strong> ทุกการเพิ่ม/แก้/ลบ จะบันทึกพร้อมชื่อคนทำและเวลา
                  <br />💡 ใช้ตรวจสอบเวลาตัวเลขผิด → รู้ว่าใครเป็นคนแก้ตอนไหน
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'help' && (
          <div className="space-y-4 animate-fade-in max-w-3xl mx-auto">
            <div>
              <h2 className="display-font text-3xl text-stone-800">❓ คู่มือการใช้งาน</h2>
              <p className="text-sm text-stone-500">วิธีใช้ทุกฟังก์ชั่น เรียงตามขั้นตอนการทำงานจริง</p>
            </div>

            {/* === Flow Overview === */}
            <div className="bg-gradient-to-br from-amber-50 to-orange-50 border-2 border-amber-300 rounded-2xl p-4">
              <h3 className="font-bold text-amber-900 mb-2">🔄 ภาพรวมการทำงาน</h3>
              <div className="text-sm text-stone-700 space-y-1">
                <div className="flex items-center gap-2"><span className="bg-amber-200 text-amber-900 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">1</span> ใส่ทุน → <strong>แดชบอร์ด</strong> กดปุ่ม "เพิ่มทุน"</div>
                <div className="flex items-center gap-2"><span className="bg-amber-200 text-amber-900 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">2</span> ซื้อของตุน → <strong>สต็อก</strong> "+ เพิ่มสินค้า" (บันทึกรายจ่ายอัตโนมัติ)</div>
                <div className="flex items-center gap-2"><span className="bg-amber-200 text-amber-900 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">3</span> เสนอราคา → <strong>เสนอขาย</strong> สร้างใบเสนอราคา</div>
                <div className="flex items-center gap-2"><span className="bg-amber-200 text-amber-900 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">4</span> ลูกค้าตกลง → <strong>งานเอกสาร</strong> กด "🚀 สร้างงาน"</div>
                <div className="flex items-center gap-2"><span className="bg-amber-200 text-amber-900 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">5</span> ทำงาน + กรอกต้นทุน → <strong>งาน</strong> (เบิกสต๊อก / ซื้อหน้างาน)</div>
                <div className="flex items-center gap-2"><span className="bg-amber-200 text-amber-900 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">6</span> เก็บเงิน → เงินบันทึกแล้วตั้งแต่เซฟงาน ✨ ออกใบเสร็จให้ลูกค้าที่ <strong>งานเอกสาร</strong> (ยอดไม่ซ้ำ)</div>
                <div className="flex items-center gap-2"><span className="bg-amber-200 text-amber-900 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">7</span> ปิดงาน → กด "✅ จบงาน" (ระบบสรุป + บันทึกการเงินให้)</div>
              </div>
            </div>

            {/* === เงิน 4 ประเภท === */}
            <div className="bg-white rounded-2xl border border-stone-200 p-4">
              <h3 className="font-bold text-stone-800 mb-3">💡 เงิน 4 ประเภทที่ต้องเข้าใจ</h3>
              <div className="space-y-2">
                <div className="flex items-start gap-3 p-2 bg-blue-50 rounded-lg">
                  <span className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">🏦</span>
                  <div className="text-sm">
                    <strong className="text-blue-700">ทุนเข้า</strong> — หุ้นส่วนใส่เงินเข้าบริษัท
                    <div className="text-xs text-stone-500">ทำผ่านปุ่ม "เพิ่มทุน" ที่แดชบอร์ดเท่านั้น — แยกขาดจากการซื้อของ</div>
                  </div>
                </div>
                <div className="flex items-start gap-3 p-2 bg-emerald-50 rounded-lg">
                  <span className="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center flex-shrink-0">💰</span>
                  <div className="text-sm">
                    <strong className="text-emerald-700">รายได้</strong> — ลูกค้าจ่ายเงินค่างาน
                    <div className="text-xs text-stone-500">บันทึกเมื่อรับเงินจริง (มัดจำ + งวดสุดท้าย)</div>
                  </div>
                </div>
                <div className="flex items-start gap-3 p-2 bg-amber-50 rounded-lg">
                  <span className="w-8 h-8 rounded-full bg-amber-100 flex items-center justify-center flex-shrink-0">📦</span>
                  <div className="text-sm">
                    <strong className="text-amber-700">ซื้อสต๊อก</strong> — ซื้อของตุนไว้ (ยังไม่ใช้)
                    <div className="text-xs text-stone-500">เงินออก แต่ได้ของมาแทน (มูลค่าบริษัทไม่ลด)</div>
                  </div>
                </div>
                <div className="flex items-start gap-3 p-2 bg-rose-50 rounded-lg">
                  <span className="w-8 h-8 rounded-full bg-rose-100 flex items-center justify-center flex-shrink-0">🔧</span>
                  <div className="text-sm">
                    <strong className="text-rose-700">ต้นทุนงาน</strong> — ค่าของ+แรงที่จ่ายในงาน
                    <div className="text-xs text-stone-500">เฉพาะที่จ่ายเงินจริง (ของจากสต๊อกไม่นับซ้ำ)</div>
                  </div>
                </div>
                <div className="flex items-start gap-3 p-2 bg-violet-50 rounded-lg">
                  <span className="w-8 h-8 rounded-full bg-violet-100 flex items-center justify-center flex-shrink-0">💜</span>
                  <div className="text-sm">
                    <strong className="text-violet-700">ปันผล</strong> — แบ่งกำไรให้หุ้นส่วน
                    <div className="text-xs text-stone-500">กดปุ่ม "ปันผล" ที่แดชบอร์ด ใส่ก้อนเงิน ระบบแบ่งตาม % ทุนให้</div>
                  </div>
                </div>
              </div>
              <div className="mt-3 p-2 bg-stone-100 rounded-lg text-xs text-stone-600">
                ⚠️ <strong>"เบิกของจากสต๊อก" ไม่ใช่รายจ่าย</strong> — เงินจ่ายไปแล้วตอนซื้อเข้าสต๊อก ถ้านับอีกจะซ้ำ 2 รอบ
              </div>
            </div>

            {/* === สูตรเงินสด === */}
            <div className="bg-white rounded-2xl border border-stone-200 p-4">
              <h3 className="font-bold text-stone-800 mb-2">🧮 สูตรที่ระบบใช้ (ตรวจสอบเองได้)</h3>
              <div className="bg-stone-900 text-stone-100 rounded-xl p-3 font-mono text-sm space-y-1">
                <div><span className="text-amber-400">เงินสดในมือ</span> = ทุนรวม + กำไรสะสม − ปันผลจ่ายแล้ว − มูลค่าสต๊อก</div>
                <div><span className="text-emerald-400">กำไรสะสม</span> = Σ (ราคาขาย − ต้นทุนงาน)</div>
                <div><span className="text-blue-400">ทุนรวม</span> = Σ เพิ่มทุน − Σ ถอนทุน</div>
              </div>
              <div className="text-xs text-stone-500 mt-2">
                💡 ตรวจสอบ: Tab "การเงิน" → "💵 เงินสด" ต้องตรงกับ "เงินสดในมือ" ใน Dashboard
              </div>
            </div>

            {/* === วิธีใช้แต่ละหน้า === */}
            <div className="bg-white rounded-2xl border border-stone-200 p-4">
              <h3 className="font-bold text-stone-800 mb-3">📖 วิธีใช้แต่ละหน้า</h3>
              <div className="space-y-2">
                {[
                  { icon: '📊', title: 'แดชบอร์ด', desc: 'ภาพรวมเงิน • ปุ่ม "เพิ่มทุน/ถอนทุน" สำหรับหุ้นส่วน • ตัวเลขทุกตัวคำนวณอัตโนมัติ ห้ามแก้มือ' },
                  { icon: '📈', title: 'เสนอขาย', desc: 'Wizard 4 ขั้น: กรอกข้อมูลลูกค้า → เลือกแพ็คเกจ (ระบบแนะนำ 3 แบบ) → ปรับแต่ง → สร้างใบเสนอราคา • ราคาปัดขึ้นลงท้าย 999 อัตโนมัติ' },
                  { icon: '💲', title: 'แคตตาล็อกขาย', desc: 'รายการสินค้าสำหรับขาย (inverter/แผง/แบต/สายไฟ) • ตั้งราคาตลาด • ใช้ตอนสร้างใบเสนอราคา' },
                  { icon: '💼', title: 'งาน', desc: '🔄 ทุกงานมีขั้นตอน 11 ขั้น (ตกลงขาย → มัดจำ[เลือกได้] → สั่งของ → สำรวจ → เตรียมของ → ติดตั้ง → ทดสอบ → เก็บเงิน → ปิดงาน → ติดตาม) กดเลื่อนขั้นในงาน เห็น progress ที่การ์ด • ขั้นเตรียมของมี Checklist อุปกรณ์มาตรฐานให้ติ๊ก • กรอกต้นทุน: "📦 เบิกจากสต๊อก" หรือ "+ เพิ่มรายการ" • งานปิดแล้วล็อก 🔒' },
                  { icon: '👥', title: 'ลูกค้า', desc: 'ฐานข้อมูลลูกค้า — สร้างอัตโนมัติเมื่อบันทึกงาน (ชื่อ/เบอร์/ที่อยู่/ระบบ ผูกงานให้เลย) • เติมรูปหน้างาน แผนที่ ประกัน เพิ่มทีหลังได้' },
                  { icon: '📦', title: 'สต็อก', desc: '"+ เพิ่มสินค้า" → ☑ บันทึกรายจ่ายอัตโนมัติ (เงินบริษัทเสมอ) • ถ้าเงินบริษัทไม่พอ ให้หุ้นส่วนกด "เพิ่มทุน" ที่แดชบอร์ดก่อน แล้วค่อยซื้อ' },
                  { icon: '🤝', title: 'ผู้ลงทุน', desc: 'ทุนของแต่ละคน คำนวณจากรายการ "เพิ่มทุน" ในการเงิน • % สัดส่วนใช้แบ่งกำไร' },
                  { icon: '💵', title: 'การเงิน', desc: 'สมุดบัญชีกลาง 2 มุมมอง: 💵 เงินสด (ทุกรายการเงินจริง — ระบบเช็คให้ว่าตรงแดชบอร์ด แถบเขียว ✅) • 💰 กำไร/ขาดทุน (รวมของจากสต๊อก กำไรตรงแดชบอร์ด) • รายการอัตโนมัติ 🔒 แก้ที่ต้นทาง (งาน/สต๊อก) เลขตามเอง • รายการกรอกมือยังแก้ได้ มีชื่อคนแก้' },
                  { icon: '📄', title: 'งานเอกสาร', desc: 'ใบเสนอราคา → ใบแจ้งหนี้ → ใบเสร็จ (มัดจำ/เต็ม) • ออกใบเสร็จ = รายได้เข้าการเงินอัตโนมัติทันที (แก้/ลบใบเสร็จ รายได้ sync ตาม) • "🚀 สร้างงาน" จากใบเสนอ • "✅ จบงาน" = สรุปทุกอย่าง + เก็บส่วนที่ขาด + ล็อกงาน' },
                  { icon: '📜', title: 'ประวัติ', desc: 'ทุกการเพิ่ม/แก้/ลบ บันทึกพร้อมชื่อคนทำและเวลา • ใช้ตรวจสอบเมื่อตัวเลขผิด' },
                ].map((item, i) => (
                  <details key={i} className="border border-stone-100 rounded-lg overflow-hidden">
                    <summary className="cursor-pointer p-3 hover:bg-stone-50 font-medium text-sm flex items-center gap-2">
                      <span className="text-lg">{item.icon}</span> {item.title}
                    </summary>
                    <div className="px-3 pb-3 pt-1 text-sm text-stone-600 leading-relaxed">
                      {item.desc}
                    </div>
                  </details>
                ))}
              </div>
            </div>

            {/* === กฎเหล็ก === */}
            <div className="bg-rose-50 border-2 border-rose-200 rounded-2xl p-4">
              <h3 className="font-bold text-rose-900 mb-2">⚠️ กฎเหล็ก — เพื่อข้อมูลที่ถูกต้อง</h3>
              <ul className="text-sm text-stone-700 space-y-1.5">
                <li className="flex gap-2"><span>1.</span> <span><strong>เงินทุกบาทต้องมีรายการ</strong> — รับเงิน/จ่ายเงิน ต้องบันทึกในการเงินทันที (ระบบช่วยสร้างให้เกือบทุกจุดแล้ว)</span></li>
                <li className="flex gap-2"><span>2.</span> <span><strong>อย่าลบรายการเก่า</strong> — ถ้าผิด ให้แก้ไข (มีประวัติ) หรือสร้างรายการแก้ (เช่น คืนเงิน)</span></li>
                <li className="flex gap-2"><span>3.</span> <span><strong>งานปิดแล้วอย่าแก้</strong> — ตัวเลขถูกล็อก ถ้าแก้กำไรสะสมจะเพี้ยน</span></li>
                <li className="flex gap-2"><span>4.</span> <span><strong>ตรวจ Dashboard กับ Tab เงินสด ให้ตรงกัน</strong> — ถ้าไม่ตรง มีรายการขาด/เกิน</span></li>
                <li className="flex gap-2"><span>5.</span> <span><strong>ของเข้า-ออกสต๊อก ผ่านระบบเท่านั้น</strong> — อย่าแก้จำนวนมือถ้าไม่จำเป็น</span></li>
              </ul>
            </div>

            {/* === FAQ === */}
            <div className="bg-white rounded-2xl border border-stone-200 p-4">
              <h3 className="font-bold text-stone-800 mb-3">❓ คำถามที่พบบ่อย</h3>
              <div className="space-y-2">
                {[
                  { q: 'ตัวเลข Dashboard กับ Excel ไม่ตรงกัน?', a: 'เปิด Tab "การเงิน" → ดูแถบใต้สรุป: ✅ เขียว = ตรงแดชบอร์ด ข้อมูลครบ / ⚠️ แดง = บอกเลยว่าต่างกี่บาท ขาดฝั่งไหน → ไปดู "ประวัติ" ว่าใครแก้อะไรล่าสุด' },
                  { q: 'หุ้นส่วนเอาเงินส่วนตัวซื้อของ ต้องทำยังไง?', a: 'โครงสร้างใหม่: ห้ามจ่ายแทนตรงๆ! ให้ทำ 2 ขั้น → ① แดชบอร์ด กด "เพิ่มทุน" ใส่จำนวนเงิน (ทุนหุ้นส่วนเพิ่ม + เงินบริษัทเพิ่ม) → ② ค่อยซื้อของตามปกติ (ตัดจากเงินบริษัท) — แบบนี้ทุนกับการซื้อแยกขาด ตรวจสอบง่าย ไม่งง' },
                  { q: 'เบิกของจากสต๊อกไปใช้งาน นับเป็นรายจ่ายไหม?', a: 'ไม่นับ! เงินจ่ายไปแล้วตอนซื้อเข้าสต๊อก ระบบจะหักสต๊อกและใส่เป็นต้นทุนงานให้เอง (เห็นใน P&L แต่ไม่อยู่ใน Cash Flow)' },
                  { q: 'รับเงินลูกค้า ต้องบันทึกการเงินเองไหม?', a: 'ไม่ต้อง! แค่เซฟงาน (มีราคาขาย+ต้นทุน) → รายได้และต้นทุนจ่ายจริงเข้า Tab การเงินทันที 🔒 อัตโนมัติ • แก้ตัวเลขในงาน → การเงินปรับตามเอง • ใบเสร็จเป็นแค่เอกสารให้ลูกค้า (ออก/ไม่ออก ยอดไม่ซ้ำแน่นอน) • มัดจำที่เคยออกใบเสร็จไว้ ระบบหักให้เอง เหลือเท่าไหร่บันทึกเท่านั้น' },
                  { q: 'อยากดูว่าใครแก้ตัวเลข?', a: 'Tab "ประวัติ" เก็บทุกการเพิ่ม/แก้/ลบ 500 รายการล่าสุด พร้อมชื่อและเวลา • แต่ละรายการการเงินก็แสดง "สร้างโดย/แก้โดย" ด้วย' },
                  { q: 'ต้องกรอกลูกค้าซ้ำใน Tab ลูกค้าไหม?', a: 'ไม่ต้อง! บันทึกงาน → ระบบสร้างลูกค้าให้อัตโนมัติ (ชื่อ เบอร์ ที่อยู่ วันติดตั้ง ระบบ ผูกงานให้) → ไป Tab ลูกค้า เติมข้อมูลเพิ่ม (รูป, แผนที่, ประกัน) ทีหลังได้ • ถ้าลูกค้ามีอยู่แล้ว ระบบเติมเฉพาะช่องว่าง ไม่ทับของเดิม' },
                  { q: 'ลูกค้าถามวิธีดูแอป Deye Cloud ทำยังไง?', a: 'Tab งานเอกสาร → ที่งานนั้นกดปุ่ม "📱 คู่มือลูกค้า" → ได้คู่มือ 1 หน้า (ติดตั้งแอป, อ่านหน้าจอแบบดูลูกศร, เช็คประจำสัปดาห์, ปัญหาพบบ่อย, ช่องทางติดต่อเรา) → กด "🖨️ พิมพ์/บันทึก PDF" แนบให้ลูกค้าได้ทั้งกระดาษและอีเมล' },
                  { q: 'ลูกค้าแจ้งปัญหา / ทำงานล้างแผง-ซ่อม บันทึกที่ไหน?', a: 'เปิดงานนั้น → กล่อง "📋 บันทึกงาน + บริการหลังการขาย" → เลือกประเภท (🐛ปัญหา 💬ฟีดแบ็ก 🧽ล้างแผง 🔧ซ่อม 📞ติดตาม) ใส่รายละเอียด + รายรับ/ค่าใช้จ่ายถ้ามี → ระบบบันทึกการเงินให้อัตโนมัติ และการ์ดงานจะโชว์ "กำไรระยะยาว" = กำไรติดตั้ง + บริการสุทธิ ดูได้เลยว่างานนี้คุ้มไหมในระยะยาว • งานที่ปิดแล้วก็เพิ่มบันทึกบริการได้' },
                  { q: 'อยากเก็บรายงานงานแต่ละงานเป็นไฟล์ ทำไง?', a: 'การ์ดงาน → กดปุ่ม 📥 สีเขียว → ได้ Excel "แฟ้มงาน" 1 ไฟล์ครบทุกอย่างของงานนั้น: ข้อมูลงาน+เบอร์ / สรุปเงิน (ขาย-ต้นทุนแตกจ่ายจริง·สต๊อก-กำไร-กำไรระยะยาว) / ต้นทุนทุกชิ้นบอกที่มา / รายการเงินทุกตัวพร้อมชื่อคนสร้าง / เอกสารที่ออก / บันทึกบริการ • เก็บเข้าแฟ้มลูกค้าหรือส่งหุ้นส่วนดูได้เลย' },
                  { q: 'จะรู้ได้ไงว่างานไหนถึงขั้นตอนไหนแล้ว?', a: 'การ์ดงานทุกใบมีแถบ Progress บอกขั้น (เช่น "ขั้น 6/11: เตรียมของ") • เปิดงานเข้าไปเห็น Stepper 11 ขั้น พร้อมคำแนะนำแต่ละขั้น (มัดจำก่อนสั่งของ, ตั้ง CT clamp, ฯลฯ) กด "✓ เสร็จขั้นนี้" เพื่อเลื่อน • ขั้นสำรวจ-ติดตั้งมี Checklist ของให้ติ๊กกันลืม' },
                  { q: 'อยากแบ่งกำไรให้หุ้นส่วน ทำยังไง?', a: 'แดชบอร์ด → กดปุ่ม "💜 ปันผล" → ใส่ยอดรวมเป็นก้อน (เช่น 30,000) → ระบบแบ่งให้อัตโนมัติตาม % สัดส่วนทุนของแต่ละคน พร้อม preview ก่อนยืนยัน • ระบบเตือนถ้าเกินกำไรสะสม และบล็อกถ้าเงินสดไม่พอ • ไม่ต้องแบ่งทุกงาน — สะสมกำไรไว้ ปันผลเมื่อพร้อม' },
                  { q: 'สายไฟเหลือจากงาน หายไปไหน?', a: 'ตอนกด "จบงาน" สายไฟม้วนใหม่ที่ใช้ไม่หมด ระบบจะคำนวณที่เหลือและเพิ่มเข้าสต๊อกให้อัตโนมัติ (ราคาเฉลี่ยถ้ามีของเดิม)' },
                ].map((item, i) => (
                  <details key={i} className="border border-stone-100 rounded-lg overflow-hidden">
                    <summary className="cursor-pointer p-3 hover:bg-stone-50 text-sm font-medium">
                      {item.q}
                    </summary>
                    <div className="px-3 pb-3 pt-1 text-sm text-stone-600 leading-relaxed bg-stone-50/50">
                      {item.a}
                    </div>
                  </details>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>

      {showJobModal && (
        <JobModal job={editingItem} partners={partners} stock={stock} documents={documents} onUpdateStock={saveStock}
          onClose={() => { setShowJobModal(false); setEditingItem(null); }}
          onSave={(data) => {
            // เช็คว่าเป็น "แก้ไข" หรือ "เพิ่มใหม่" จาก id
            const isEditing = editingItem && editingItem.id;
            const jobId = isEditing ? editingItem.id : `job-${Date.now()}`;
            
            // ✨ บันทึกบริการใหม่ที่มีเงิน → สร้าง tx อัตโนมัติ (isService — ไม่ปนกับยอดติดตั้ง)
            const SVC_LABELS = { issue: '🐛 ปัญหา', feedback: '💬 ฟีดแบ็ก', clean: '🧽 ล้างแผง', repair: '🔧 ซ่อม', followup: '📞 ติดตามผล', note: '📝 บันทึก' };
            const newSvcTxs = [];
            const finalServiceLog = (data.serviceLog || []).map(l => {
              if (l._txCreated) return l;
              const updated = { ...l, by: l.by || currentUser.name };
              const label = SVC_LABELS[l.type] || '📝';
              const now = new Date().toISOString();
              if (Number(l.income) > 0) {
                newSvcTxs.push({
                  id: `t-svc-${Date.now()}-${Math.random().toString(36).slice(2,5)}`,
                  date: l.date, type: 'income', category: 'รายได้จากงาน',
                  amount: Number(l.income),
                  description: `บริการ: ${label} ${data.customer} — ${l.note}`,
                  jobId, partnerId: '', isService: true,
                  createdBy: `${currentUser.name} (บันทึกงาน)`, createdAt: now,
                });
              }
              if (Number(l.cost) > 0) {
                newSvcTxs.push({
                  id: `t-svc-${Date.now()}-${Math.random().toString(36).slice(2,5)}c`,
                  date: l.date, type: 'expense', category: 'ต้นทุนงาน',
                  amount: Number(l.cost),
                  description: `บริการ: ${label} ${data.customer} — ${l.note}`,
                  jobId, partnerId: '', isService: true,
                  createdBy: `${currentUser.name} (บันทึกงาน)`, createdAt: now,
                });
              }
              return (Number(l.income) > 0 || Number(l.cost) > 0) ? { ...updated, _txCreated: true } : updated;
            });
            const jobData = { ...data, serviceLog: finalServiceLog };
            
            if (isEditing) {
              saveJobs(jobs.map(j => j.id === editingItem.id ? { ...jobData, id: editingItem.id } : j), 'edit', `แก้ไข: ${data.customer}`);
            } else {
              const newJob = { ...jobData, id: jobId };
              saveJobs([...jobs, newJob], 'add', `เพิ่ม: ${data.customer} (${data.salePrice} ฿)`);
              // ถ้ามี quotationId → ผูก doc ↔ job (อัพเดทกลับ)
              if (data.quotationId) {
                saveDocuments(
                  documents.map(d => d.id === data.quotationId ? { ...d, jobId } : d),
                  'edit',
                  `เชื่อมงาน ${data.customer} กับใบเสนอราคา`
                );
              }
            }
            
            // ✨ เซฟงาน = บันทึกเงินทันที (รายได้ตามราคาขาย + ต้นทุนจ่ายจริง) — ใบเสร็จเป็นแค่เอกสาร
            const syncResult = syncJobFinanceTxs({ ...jobData, id: jobId }, [...transactions, ...newSvcTxs], currentUser.name);
            if (newSvcTxs.length > 0 || syncResult.changes.length > 0) {
              const parts = [];
              if (syncResult.changes.length > 0) parts.push(syncResult.changes.join(' · '));
              if (newSvcTxs.length > 0) parts.push(`บริการ ${newSvcTxs.length} รายการ`);
              saveTransactions(syncResult.txs, 'add',
                `💰 บันทึกเงินจากงาน ${data.customer}: ${parts.join(' · ')}`);
            }
            
            // ✨ Auto-sync ลูกค้าจากงาน → Tab ลูกค้า (เพิ่มข้อมูลทีหลังได้)
            if (data.customer && data.customer.trim()) {
              const custName = data.customer.trim();
              const existing = customers.find(cu => cu.name.trim() === custName || cu.jobId === jobId);
              if (!existing) {
                // ยังไม่มี → สร้างใหม่จากข้อมูลงาน
                const newCust = {
                  id: `cust-${Date.now()}`,
                  name: custName,
                  phone: data.phone || '',
                  address: data.location || '',
                  mapLink: '',
                  installDate: data.date || '',
                  system: data.type || '',
                  warranty: '',
                  jobId: jobId,
                  note: '',
                  photos: [],
                };
                saveCustomers([...customers, newCust], 'add', `👤 สร้างลูกค้าอัตโนมัติจากงาน: ${custName}`);
              } else {
                // มีแล้ว → เติมเฉพาะช่องที่ว่าง (ไม่ทับข้อมูลที่กรอกไว้)
                const patch = {};
                if (!existing.phone && data.phone) patch.phone = data.phone;
                if (!existing.address && data.location) patch.address = data.location;
                if (!existing.system && data.type) patch.system = data.type;
                if (!existing.installDate && data.date) patch.installDate = data.date;
                if (!existing.jobId) patch.jobId = jobId;
                if (Object.keys(patch).length > 0) {
                  saveCustomers(customers.map(cu => cu.id === existing.id ? { ...cu, ...patch } : cu), 'edit',
                    `👤 อัพเดทข้อมูลลูกค้าจากงาน: ${custName}`);
                }
              }
            }
            setShowJobModal(false); setEditingItem(null);
          }}
        />
      )}
      {showPickQuotation && (
        <PickQuotationModal
          documents={documents}
          fmt={fmt0}
          onClose={() => setShowPickQuotation(false)}
          onSelect={(quotation) => {
            // สร้าง job draft จาก quotation
            const snap = quotation.equipmentSnapshot || {};
            const items = quotation.items || [];
            const itemDesc = items[0]?.name || '';
            
            // คำนวณต้นทุนแยกหมวดเบื้องต้น (ถ้ามี snapshot)
            const draftJob = {
              date: new Date().toISOString().split('T')[0],
              customer: quotation.customerName || '',
              phone: quotation.customerPhone || '',
              location: quotation.customerAddress || '',
              type: snap.jobType || itemDesc.split('\n')[0] || '',
              salePrice: Number(quotation.totalAmount || 0),
              originalPrice: Number(quotation.totalAmount || 0),
              discount: 0,
              discountNote: '',
              status: 'pending',
              investments: {},
              costsByCategory: {},
              totalCost: snap.totalCost || 0,
              profit: snap.expectedProfit || 0,
              note: `สร้างจากใบเสนอราคา ${quotation.docNumber}`,
              quotationId: quotation.id,  // ✨ เชื่อมกลับ
              docNumber: quotation.docNumber,
              expectedProfit: snap.expectedProfit || 0,
              expectedCost: snap.totalCost || 0,
            };
            setEditingItem(draftJob);
            setShowPickQuotation(false);
            setShowJobModal(true);
          }}
        />
      )}
      {showStockModal && (
        <StockModal item={editingItem}
          onClose={() => { setShowStockModal(false); setEditingItem(null); }}
          onSave={(data, txOptions) => {
            const isEdit = !!editingItem;
            if (isEdit) {
              saveStock(stock.map(s => s.id === editingItem.id ? data : s), 'edit', `แก้ไข: ${data.name}`);
            } else {
              const newStockId = `stk-${Date.now()}`;
              saveStock([...stock, { ...data, id: newStockId }], 'add', `เพิ่ม: ${data.name} (${data.qty} ${data.unit})`);
              
              // ถ้าเลือก "บันทึกเป็นรายจ่าย" → สร้าง expense จากเงินบริษัท (โครงสร้างใหม่: ไม่ผูกหุ้นส่วน)
              if (txOptions && txOptions.createTransaction) {
                const totalCost = Number(data.qty || 0) * Number(data.unitCost || 0);
                const baseDate = data.purchaseDate || new Date().toISOString().split('T')[0];
                
                const newTx = {
                  id: `t-${Date.now()}-${Math.random().toString(36).slice(2,7)}`,
                  date: baseDate,
                  type: 'expense',
                  category: 'ต้นทุนสต๊อก',
                  amount: totalCost,
                  description: `ซื้อ ${data.name} ${data.qty} ${data.unit}${txOptions.note ? ' - ' + txOptions.note : ''}`,
                  jobId: '',
                  partnerId: '',
                  auto: true,
                  createdBy: `${currentUser.name} (สต๊อกอัตโนมัติ)`,
                  createdAt: new Date().toISOString(),
                };
                
                saveTransactions([...transactions, newTx], 'add',
                  `บันทึกซื้อ ${data.name} ${totalCost.toLocaleString()} ฿ (เงินบริษัท)`);
              }
            }
            setShowStockModal(false); setEditingItem(null);
          }}
        />
      )}
      {showPartnerModal && (
        <PartnerModal partner={editingItem}
          onClose={() => { setShowPartnerModal(false); setEditingItem(null); }}
          onSave={(data) => {
            if (editingItem) {
              savePartners(partners.map(p => p.id === editingItem.id ? data : p), 'edit', `แก้ไข: ${data.name}`);
            } else {
              savePartners([...partners, { ...data, id: `p-${Date.now()}` }], 'add', `เพิ่ม: ${data.name}`);
            }
            setShowPartnerModal(false); setEditingItem(null);
          }}
        />
      )}
      {showTransactionModal && (
        <TransactionModal tx={editingItem} partners={partners} jobs={jobs}
          onClose={() => { setShowTransactionModal(false); setEditingItem(null); }}
          onSave={(data) => {
            const now = new Date().toISOString();
            if (editingItem) {
              // เก็บประวัติแก้ไข: ใคร เมื่อไหร่
              const updated = {
                ...data,
                createdBy: editingItem.createdBy || null,
                createdAt: editingItem.createdAt || null,
                editedBy: currentUser.name,
                editedAt: now,
                editCount: (editingItem.editCount || 0) + 1,
              };
              saveTransactions(transactions.map(t => t.id === editingItem.id ? updated : t), 'edit', `แก้ไข: ${data.description} (${Number(data.amount).toLocaleString()} ฿)`);
            } else {
              const newTx = {
                ...data,
                id: `t-${Date.now()}`,
                createdBy: currentUser.name,
                createdAt: now,
              };
              saveTransactions([...transactions, newTx], 'add', `เพิ่ม: ${data.description} (${Number(data.amount).toLocaleString()} ฿)`);
            }
            setShowTransactionModal(false); setEditingItem(null);
          }}
        />
      )}
      {showCustomerModal && (
        <CustomerModal customer={editingItem} jobs={jobs}
          onClose={() => { setShowCustomerModal(false); setEditingItem(null); }}
          onSave={(data) => {
            if (editingItem) {
              saveCustomers(customers.map(c => c.id === editingItem.id ? data : c), 'edit', `แก้ไข: ${data.name}`);
            } else {
              saveCustomers([...customers, { ...data, id: `cust-${Date.now()}` }], 'add', `เพิ่ม: ${data.name}`);
            }
            setShowCustomerModal(false); setEditingItem(null);
          }}
        />
      )}
      {showCapitalModal && (
        <CapitalModal
          mode={capitalMode}
          partners={partners}
          actualInvestments={actualInvestments}
          cashOnHand={Object.values(actualInvestments.inv).reduce((s, v) => s + v, 0) + totalProfit - dividendStats.total - totalStockValue}
          fmt={fmt}
          onClose={() => setShowCapitalModal(false)}
          onSave={(data) => {
            const partner = partners.find(p => p.id === data.partnerId);
            const isDeposit = capitalMode === 'deposit';
            const tx = {
              id: `t-${Date.now()}`,
              date: data.date,
              type: isDeposit ? 'income' : 'expense',
              category: isDeposit ? 'เพิ่มทุน' : 'ถอนทุน',
              amount: Number(data.amount),
              description: `${isDeposit ? 'เพิ่มทุน' : 'ถอนทุน'} ${partner?.name || ''}${data.note ? ' - ' + data.note : ''}`,
              jobId: '',
              partnerId: data.partnerId,
              createdBy: currentUser.name,
              createdAt: new Date().toISOString(),
            };
            saveTransactions([...transactions, tx], 'add',
              `${isDeposit ? '➕ เพิ่มทุน' : '➖ ถอนทุน'} ${partner?.name}: ${fmt(data.amount)} ฿${data.note ? ' (' + data.note + ')' : ''}`);
            setShowCapitalModal(false);
          }}
        />
      )}
      {showDividendModal && (
        <DividendModal
          partners={partners}
          actualInvestments={actualInvestments}
          retainedProfit={totalProfit - dividendStats.total}
          cashOnHand={Object.values(actualInvestments.inv).reduce((s, v) => s + v, 0) + totalProfit - dividendStats.total - totalStockValue}
          fmt={fmt}
          onClose={() => setShowDividendModal(false)}
          onSave={(allocations, note) => {
            const now = new Date().toISOString();
            const date = now.split('T')[0];
            const newTxs = allocations.map((a, i) => ({
              id: `t-div-${Date.now()}-${i}`,
              date,
              type: 'expense',
              category: 'ปันผล',
              amount: a.amount,
              description: `ปันผล ${a.name} (${a.pct.toFixed(1)}%)${note ? ' - ' + note : ''}`,
              jobId: '',
              partnerId: a.partnerId,
              createdBy: currentUser.name,
              createdAt: now,
            }));
            const total = allocations.reduce((s, a) => s + a.amount, 0);
            saveTransactions([...transactions, ...newTxs], 'add',
              `💜 ปันผล ${total.toLocaleString()} ฿ แบ่ง ${allocations.length} คนตามสัดส่วนทุน${note ? ' (' + note + ')' : ''}`);
            setShowDividendModal(false);
          }}
        />
      )}
      {customerGuide && (
        <CustomerGuideModal
          customerName={customerGuide.customerName}
          systemType={customerGuide.systemType}
          companyInfo={companyInfo}
          onClose={() => setCustomerGuide(null)}
        />
      )}
      {showDocumentModal && (
        <DocumentModal
          doc={editingItem}
          defaultType={defaultDocType}
          documents={documents}
          customers={customers}
          jobs={jobs}
          companyInfo={companyInfo}
          onClose={() => { setShowDocumentModal(false); setEditingItem(null); }}
          onSave={(data) => {
            // ✨ Helper: หา job ที่ผูกกับเอกสารนี้ (ผ่าน chain)
            const findLinkedJob = (doc) => {
              const chainId = doc.jobChainId || doc.id;
              const master = documents.find(d => d.id === chainId) || doc;
              return jobs.find(j =>
                j.quotationId === master?.id ||
                j.quotationId === chainId ||
                (master?.jobId && j.id === master.jobId)
              );
            };
            const isReceipt = (d) => d.type === 'receipt-deposit' || d.type === 'receipt-final' || d.type === 'receipt';
            
            if (editingItem) {
              saveDocuments(documents.map(d => d.id === editingItem.id ? data : d), 'edit',
                `แก้ไขเอกสาร ${data.docNumber}`);
              
              // ถ้าแก้ใบเสร็จที่มี income ผูกอยู่ → sync จำนวนเงินให้ตรง (audit ครบ)
              if (isReceipt(data)) {
                const linkedTx = transactions.find(t => t.sourceDocId === data.id);
                if (linkedTx && Math.abs(Number(linkedTx.amount) - Number(data.totalAmount)) > 0.5) {
                  saveTransactions(transactions.map(t => t.id === linkedTx.id ? {
                    ...t,
                    amount: Number(data.totalAmount || 0),
                    description: `รับเงินตามใบเสร็จ ${data.docNumber} (${data.customerName})`,
                    editedBy: `${currentUser.name} (sync ใบเสร็จ)`,
                    editedAt: new Date().toISOString(),
                    editCount: (linkedTx.editCount || 0) + 1,
                  } : t), 'edit', `🔄 Sync รายได้ตามใบเสร็จ ${data.docNumber}: ${Number(data.totalAmount).toLocaleString()} ฿`);
                }
              }
            } else {
              saveDocuments([...documents, data], 'add',
                `สร้างเอกสาร ${data.docNumber} (${data.customerName})`);
              
              // ✨ ใบเสร็จ = เอกสารให้ลูกค้า — เงินบันทึกจากงานอยู่แล้ว ไม่สร้างซ้ำ
              if (isReceipt(data) && Number(data.totalAmount || 0) > 0) {
                const linkedJob = findLinkedJob(data);
                if (linkedJob) {
                  // งานนี้มีระบบเงินจากงานแล้ว → แค่ sync ให้ครบยอด (กันงานเก่าที่ยังไม่ sync) ไม่มีทางซ้ำ
                  const sr = syncJobFinanceTxs(linkedJob, transactions, currentUser.name);
                  if (sr.changes.length > 0) {
                    saveTransactions(sr.txs, 'add', `💰 บันทึกเงินงาน ${linkedJob.customer} (ตอนออกใบเสร็จ ${data.docNumber})`);
                  }
                } else {
                  // ใบเสร็จไม่ผูกงาน (ขายของ/บริการนอกระบบงาน) → สร้างรายได้ตามเดิม
                  const alreadyExists = transactions.some(t => t.sourceDocId === data.id);
                  if (!alreadyExists) {
                    const newTx = {
                      id: `t-rc-${Date.now()}`,
                      date: data.date || new Date().toISOString().split('T')[0],
                      type: 'income',
                      category: 'รายได้จากงาน',
                      amount: Number(data.totalAmount || 0),
                      description: `รับเงินตามใบเสร็จ ${data.docNumber} (${data.customerName})${data.type === 'receipt-deposit' ? ' — มัดจำ' : ''}`,
                      jobId: '',
                      partnerId: '',
                      sourceDocId: data.id,
                      auto: true,
                      createdBy: `${currentUser.name} (ใบเสร็จอัตโนมัติ)`,
                      createdAt: new Date().toISOString(),
                    };
                    saveTransactions([...transactions, newTx], 'add',
                      `💰 รับเงินจากใบเสร็จ ${data.docNumber}: +${Number(data.totalAmount).toLocaleString()} ฿`);
                  }
                }
              }
            }
            setShowDocumentModal(false); setEditingItem(null);
          }}
        />
      )}
      {showDocumentPreview && previewDoc && (
        <DocumentPreview
          doc={previewDoc}
          companyInfo={companyInfo}
          fmt={fmt}
          onClose={() => { setShowDocumentPreview(false); setPreviewDoc(null); }}
        />
      )}
      {showCompanySettings && (
        <CompanySettingsModal
          companyInfo={companyInfo}
          onClose={() => setShowCompanySettings(false)}
          onSave={(data) => {
            saveCompanyInfo(data);
            setShowCompanySettings(false);
          }}
        />
      )}
    </div>
  );
}

function StatCard({ icon: Icon, label, value, suffix, color, highlight }) {
  const colors = {
    emerald: 'from-emerald-400 to-emerald-600',
    rose: 'from-rose-400 to-rose-600',
    amber: 'from-amber-400 to-orange-500',
    blue: 'from-blue-400 to-blue-600',
  };
  return (
    <div className={`rounded-2xl p-4 shadow-sm ${highlight ? `bg-gradient-to-br ${colors[color]} text-white` : 'bg-white border border-stone-200'}`}>
      <div className="flex items-center gap-2 mb-2">
        <Icon className={`w-4 h-4 ${highlight ? 'text-white' : 'text-stone-500'}`} />
        <span className={`text-xs ${highlight ? 'text-white/80' : 'text-stone-500'}`}>{label}</span>
      </div>
      <div className={`display-font text-2xl md:text-3xl ${highlight ? 'text-white' : 'text-stone-800'}`}>
        {value}<span className="text-sm ml-1 opacity-70">{suffix}</span>
      </div>
    </div>
  );
}


const DD_LOGO_DATAURL = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAPAAAADwCAMAAAAJixmgAAAB/lBMVEX3+PMAAADV2NoYNlcMKkvY5eVxwrzzqFI1iJVPp6fj6Oh0h5VQZnkjPFYzVGsuSmMqQ1u3xcuWprAzeYlFWnBmeYmKmaZuubbDy9Dvtm6vu8NNnKKotbtJlps5kpt4ycLx2a/Y3uHU8+pKiJTz6MxoqauRyMev1tRWsa3tyI8gPGFUdIWhrbYxZXkcO2DP4t359NpWbYGT1c2z49ocQ1y46eSEkp12kpztnEcBHDwdRmOOt7pzmKTrrWORu8T34rlUVVi58egAHkFFSVBIoZ78s1oybIKHw7zqvYKHbFH205mJeGeBjprVpW11ZFO4hVDJikwHIj4+oJ1oW1CYdlVpam34xHwzcX6minDtzqO8lmrak048mKBccn5+0Ml9jKCSgW6reUy62+DGm25fYF5gXmFgb4Bmc3x4v8CCj6DxnD33oD7v38Dg3+D/9L8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADgnXxtAAAAgHRSTlP/AP////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////8AAAAAAAAAAAAAAAAAAAAAAAz3oMYAACXASURBVHja7Z35f9pItug1UlUM2iUkIbbYgIE4YDvek9jZ00lP0um5Pb3Pdre3b///j++cqpKQkABJYCe579VnpruNAde3zqmzqRbpD/+PNen/A99qk/Paf0RguUj7jwEsl21fM7BctX2NwPKm7asClrfTvhJgeZvtiweWt9++ZGD5dtoXCizfZvvygIv2vE+pOm+U3jWydFe4fQYXtrtuEAQaa/89cN1uO5RlGAJ6V8jS7eMeq2pfdmaBr3uWrSgKSTT40bY83Q9mDgzJWuwvA3hVD4E1bAOqZSiMTjlSjIeKaIby8OER+y/4nWEBdhuFfbvI0u3hUpWGrqZbnO7hQ+MhNoM1xIWGP7P/4uBEsTzNDfsrJf15gVfQym1NtxXCWB8ewf8VIcyFxkfjIWdHaNvTuvIq5s8HvIJ25psIe8Qk+JCTgNqa+tTXLsFYYUPjJSY25+bsTNK+u4r5MwEvm7dy17eg00dHyHrEaCzPD7ohVaW8RuU2U33CRuihUARrOpPV7RNLW8al1NFMJigwT5GGumE+abrJ3Yja4IJWLM1Z6qjvHDgfV57pBsHeIjAhth44VCrR1DA4Qe3gX6EQQ3dlulViaYu4qhyYbNqiIhPF1NqqVKGpqCMwI+BLcD5b/xyqW0SWtsarhv9sIS7+D2lDaYMWBh58CVg80G5ia466NWJpa7iaDVJRuFA2oxXMmiWmM2i2vzVkaSu8qoy4D1nnFH2mSttpXV0R36oYWr5i3wFwnqkKLCFdkEUobbFFA2mgYuear9sGzjPNM48I1bMvqbTlpgZmhGy5dHNkaVNe1TmJZpoVqNJtNNdkAwr/09vqpsTSZrxU1gyhzLeFm0CGpuVFX7cGnBVv12QmBebu5e3hYgtsonC9nm1GLG0mXoYLEvb70i03lf8tkLOfZ7xuATgr3rZJWEpPvNKW+fe9ChZbJ1ybrO4GQpaqy/eSDflDYril+76306o0lW1yxISs9ftViaWKvBTHm00qvYI2A/CjKsTUV3gO5uVEXlsFzqqzpWDthtizKh2vCgzBlzBe9qwisVSNN0B1RvFWCzSqA0uqjh4K1ZpWIpYq6bOGfxQk7Fbs9QbAMJOFWk8rzWOpir3SWX2KWMWM8/5eIeBH+4XNtUlgsJ+Cc6DliaXSvDQ0CQZ65KRYqPHo2c7eInsMvP97/L7WTnFX5bMeKJZTnlgqzdu2uUYFRXvX2mlFwvtWQMXArcd7sdBLAEuBKOVnY+uNgTPmmce0Srdw5/ZbO9+K/zwQ/xUB7z/bEWOxv7NzUMpai6quW5ZYKsk7489I7LCUidqJVfnZfhI4DkAetcqGIiFXtNLE5YBVlxeNLblU5w52hCCj+RwBtyKxxu8o3vomL94H6jaBs7zgA4lXMjNC+fE5++3/PEhIdn8nntNlJvDcIxvliaUyvFyfiV66b/EMBZ1+NAcWP+GvK8XWOrFKE0sleNso36dkWqFrB0KEQqYC+EBwtsTULt2mnNgtQSwV5qVtjOgs4lfqWktM0tbjA2a48Z+PxCh8qKLQkUNmxDNamLgwMHXw6b1dSb7cN/HZ20qwHbSqeKQFYma52nQLwOmvCNlQlp6/+3uP1gUWc4+0t1dlHmO/bKcosVSQt+8RloeW7c+3j6Mw6yD2uft7B9D29h+lfDO+4/GLqsRmUW8sFZzAJ4zXLF2pA8FGkv2WKe6LA5jOvLUOkG//271I6avlUB57AKUXnMbFgFWNuTybVpq8Owcxx4uYVjDH1nnvWdWprFosOPDVjYAXAg6mNoZcpT+PDuZcBzuZthf/pvWiouGS+UPGoBCxVID32OHLTboVO7TXElzf7uS0A/Gbg+olAUcpbqqLAMumUiofRIEd7KfV+nfui5cRp5NhsGrl7DXXQEuuDJxWaPR1RqmAY/8xmqQE8/4y+QriRLkDaJ/tPC4ZamrMpp4UUGqp4AQu6ZDQFD9OMx/sLG17CdoWt99lQ03uNQtM47XA/dCuZLCE+2l9EF1/sZxXpBAo2xaj3Ss/nSkzM8ZC/FEQOO2B9coGa/9DQlytFcBsGkeyfVHNePESiL7WbknrFDpAD0y0ivaTqej/aK0WMAs49h5X0eTUNC7km9YBc49kbvDYb/+g9WHlDMb2Atz1wQtpo8Z8ieL0ywIvKDQz+M7GTztbq4EPpM1byLObNUq9GpgGzPhpG3dmfzVvtYJHvm9aUOq1wOnxYRba2rwve5E9brUgT9rbx/ZiD7KmViuaxFtoFlthvzr8WAms8jFrVzVYoj3iUxjczf/KGqV9cEY7rBwSv78ycJvro1oGOB1Ds1nhbzptW6wCv8dhVbntXmq+72uXblessgXmfSzK8/Z4NTGVw1BWV9U/nFXEq4DVKVstVHXp1QHoL2sHKEdmVlzfs4zkYnjb1C8d3vtH34q3t5b7JjnQTTbLcNV8DvQx8yknJYAXq5Qlc4aFxBBaIqXRLCXiNAwbNz4IbjuxWPHRisnc1pMbCBTbl5dkEe0VxCuAeYxlbsOaSPJ3nNZ4+V8vu6HMjJYcdi99zxCdX+v5ZNYd25wONW04Ndnic03NdcYeLQqcXlG4URKcFY2CmzdQ6i8+fMCi1ocPL/7PI2k/vOTQ3uqn613U1hN3cnHxCtvF+MbEFRftXLvlLideDszLdvrmuI7H9BaXFD/a+2WxxvMB4ivZ1VG/V60XQV09HF+8ujg7Ze3sYnAxAjeUmXE6q731iwGnBMyzwo1jLOrjpDVncXqwGHKw+Llr8zBJXs5LtAugHd+717zH2vj01cUUXr5cGN41IpZWCphsLOCZwcyI3g33wSC9ePHh4Bdhi38BpX4BNkoNL3GfhNjI890yB0tuXp2d7gpYbM3mvdNXV/CLWbZsS7x+EeCUD+5uQ8Aqd4zcLuFOHvk44XNU2XE13eb+SeuGbRhj4uUIWQWFv3p1Nma4u7u7MfL41Q1ZTNW5iGfLDLW01ESTKnX3xYfWBNe/Oi7PqZ88+YEYuLdS10903QOPCi89YaK1ZIlOjiUXLK8xy4kniH7BeXebvWFvNxbz+OIqY2dYz3VaDlgEWe3N1Bkl15bOzgaSj5bE9+z0TjzcYal1XfBYwWBUf/v2eiCjkBdzFRm+ZiJ4R+egK+Zcs99f6IvLL7o83Prfa4GzUfRmAoZMCwZ60Kw/6OH4QYQ6oLLTdV2NWSjt2pkc08HgeCAbRBvUob2tTyQNi3EZAd8MThlk81wxHEk/nMv49HlGxMxH+0t0egkwS5PIbBPe75iszkb1B53e4IpYdDJqvh9PJmd0MIE56Upnk8n4fXNU7w00YtPrt4jcu8Z1Z+klBqpNQMAMd3cI8sU8sJkgPlGUMBtu2fI64IXCzqZpofYD+shJ/UH9fq0pmcA+qovWG/hPrEGTEcLvaxNHIddnPfypUxsN4KcUcVshwwum0M3dQ+jXVDOUYQJ4tDgJVGtFXiyt8Emb5P2XP6AQ3yPv/doEptXkrP6AtXqtRq+emLTJf4bxGEn6a33AxqNWq/WoY6TMJajK9Rk3y/fYQhYSA6PB3t09XzSuV/iuJcFHPjCf9/JG9gp4cfrW7td6g+kTT7qOASNgEC+Ox/37GOTI4x4KGNrwzEklpTqxJhM+g3cx0kBkYahHo917o6ZJFjyTzFeS0ZXAKZ/kbxh0hNCvK+AFOhDw9bFBAhrxwgsxcP3B3/AN76kNdrqOb2fEtM3GK7JBxDw7FRIeEkgehofCTO8eKs1/HB5OyWK8wOLLaa5nygUO2dpCt3q8YaOE3j9gvMDngghOGXCHvTC4JOaASRh+hlc6YIg9HJ8abz0W18qxzZpejMWErY92sQm3BE5qtNupD8mieWUaaoRFgbnJMqpvUwE/4g3Gdaau9+/XpemTvyOfGID79wcBB37ACHGSgxI7E67R0BpXAy1OTGW0WbGJ2p1bK/wJ//GPXiaFUO2s2VoATtloFqv4lXlhfI3js3qP0f2tNqYG6Z5FeLU5sHgBhDwamOiK7wsBjya4hEYYzS4hV2dxAB1jzmPq3U42Z/KXRlvSUifc3kChlWtar3Fp/q03cIlJ38/xODC3aOKlHr0BR33dqDVqnesJ7V+fGHEk7xIyOm0mCXvNFHEecHupTucAq+wxjV1ZozFIo4P3o56QHphZMGARLzYBPB+B2ngCVm7QbE4uqOOesHzCwvjjWEWHPk4C75pkeJoC7inKTMrTaZcuBc48D66u0cwnnDjHgwGdAHWHivmJXKLRK6bS9+OXGiMKPdQcyJ5M5YcnxD65eY7pi2HYvgdx1ngOjJ7J6iWn8ulhjgflDDmxRw4we+BfXaOZAQAJmVM8eGUwwAVtzqSWbMfglgajyCR3Rs3xAO2k+KA1dZ3Jv/3bjRUd+uGd3UsAg1eCLx82d0X7b9O8oL9LsksClgBTVqy0qmo0pKMgIJ2lfhD46qxQ5Ev0jAfOnV4PAhGdGMeT3mgE+QMdUEgpNHGqiX2oAe14NH7OYioTi7JEu0hp8Hh3CiNxDg651xtOD63cZ1+qkV31sQSYJUqLCUsZAbO9PTAVNZYNchJPC1xMjkDi8P9rzKPk42N54riXeFAPecLfNx074+ubYe35c8ykGx2IvSxCnp+mrRT430MufP79dneZomnqEuBs6u9WjrEg85k0m+OzwUCicldXRO7/hKW/pq5PfV4OMEx2ItGT16+xHGJj7/XJaFhrNBpNB8R23kO/3IA8+mK8AAzeuNk7NK3zc8tcFgKzlCnHMUn5YVblOBpiDpfypAim5mSAiy+IgvUNSxTeXwupo8oTw/Kmmtt2JpPnYJVvngNtrdGZwJhbYMThJ3jVPVvk5YWe3XvNZvOELDGvzHbm5IgZYIrTnVTNDFUDBIw+F6JmlgkeQ9xgTwbQ6DFm/5d4/I7QcrcLUxgaTO8mzFrQwOeA26iNYVKdd+qAa7LwYRwV7TJibkJ+vOxRkJmfQEj5U9ivHGTx4oXIBDu1CYQAzvHbepMn/5D9g6oHyhHxwWtNxtdgx972em/rteHkhOhjFOroOUb+KN9zHPqJcLrNTr0ZRZY8oAZeRfnBXaproFLfqbnA2bjSre6TwOcK4A5mhlc8LcACDoCxpB9CEcWAdLDXA0f8Z/Y78MdjCLbGnUZj6IDdMwWvYk5ii1XvgBFrckE3YaBG9cNVSbtLjLzoMgMs41NlElaNKiFr4HkfyxRYmMXrVXGDAIxqEGyOEq9h/NEEwbowiZ+PoAO94a/Ia3VO5xYav7eD0KINrZVFijDfE2eAnU3iStBolteyxAjToPExTxzSbAxYlHjEGNRqHcck03Gj44AjanR+xflrd3bHiTnLzQIj7gzx98qqvdosulScdcDqbJN6NAR0DpZyOAJI+KwLIcY4wctDSybhGFhkheMpMZ0btFio0O+gt8N62koJ4uGhec7s3t/ldYvziKuuAw42qWZ5kPO85+LlYeNAIzrX8SQa1V6bxzFwlAXDJDaux89BML0OGmhyWE8Z5l1WMqg3xMmJ9rozYbTc0CMD7G9gs2Tc09REAkGMee5VNIXn48CB/5wUOr75+blygy74EC0WUPVSwIy3PkTLDUGLv/7AH5dk1psK4FSc5W2wLstBp9S7z7UZ/zWWIak9W+RlKn1c/3Oat9aZwCS+ARfcq2HAoTTq9Qwv2mXlv3Rpwag+p3YpZYx09TgLn3sH0kjkuJj7nbk/2NEU7syzJQY8ih1S1MZ8o8EQFBrAINRqpnkf1NFQ+UU7d5wbay0AU6fywizVY6s3rujZSADXsOLOp/CDJFjtYg6ceLkxYls5G0KhhylgNM49dFQlHKaVlzBJedUOvWLMgfpGbHdw3OS1uRE1n1zRBfEy4GgOJ4ehNsbH3mb9fqMGkjTrc2AQL/jfIcaZaskeZcy0lGekqwSWGKw3hqx2YLqUXoNjasAUhsCrt8CFKv2EAyfHoTNx8dSsHvCCQivobsUTJIZbb5TuGLO/wRpgrapXAumYtV69xmJ260qGHHE0CJibSos3ttL36735S8Pnkyv44NNer8FccKPOiSElesCCDTRXl+WLaxm/JOV5pRJLs6ivB7KoqZiQ6cBM4yuKdPdY6hrEo29rtSwwWum3c95hc3KNcYJZB16MKc16IobEKWFWcJZutq6VBcYdaGWWKmmY7ppTLcAizSEmd/UHvUMWGhhoNCDOGuYDj+LoZDR2rvH0OxQrS4G5hBNx8/RcIYZTPtDNFKcZcNoNk3IrOy7ZOvToUF2T5bO9eu/Xp6wmh3+wTynku0n1rVEfQ8sGg22Onec3DNcagn2uNcRpxYe9eZZgsuJFlfJadnnLAnCfTcGwnK06PDyPjtJFtWbI9Rq8yEdBx7ocpvmT8Riyu+ZoQvGQFzoeO874uat5rMTytAHq/GvjHbqep+KreJXuvKqnDHM2M2WAS8cdGOs37zVH0Iaso+Y7wYwZzXm8hgfU/sa9dpzJRHZYycMPtKnJFyTCh2q8ooNT9RwNVNyiMuCsmuNYB1wh0DIhjgeHeQqZK7gOloQeNhgzCxxFZjM/TNqwEwdNs/+yDodgyRtcnYnVqY8U5c3HN4l3TCttfMwNtaScx0pKqelCbQh/h1Fme8hEcm4y5hrqNkr60DSfKjntKbyv1uvAOxpcvDA/Or36xSExPj3700/f//jjz9ihxulVlWiI16bDlcBM7Us+KKVYMz8ciuS8I6zOU0CpMer7PGXvYQX2MGqg97VhR6T/c9yn+DXNVzeE/ITLEn85+Bl5e+MLs8ISG1ECoCuA+2Glegdbb4c2ptMBM2PO5cemM5d1rddLeVY2Bj02JvCPd9x5v6uzgPJsrJAfdx63fvn0BhexdHqdi3EFu1UAmFYDlrqmmGzn3BsdDiMVBuWOqTk4TxSS7R17Mxg/XOVRh8j59Mwmbx63Dv7FYDKHkRoPhuWXqt8iMD83d37I/fABqLYZmdhzyzw8jHgbadZDU/hd5ng7HZYwjPHh06dPL9F8d/DFe/fOJnb5ft0mMJ54funruq5ZR5jpoPr2GodWwkA9tcxks54+Pef+G5+0KE8Rt8dTfpAnMf4zmpx3rFAJSQQTsfulzOHUGilAQ6l0+JydAs0bI8dAx/pgvPn+p08fyXlnng/uDq74DBnywiwmTRdO6dpiAWD+YGkTYMxQenOjBMDkp8f/9K//+scfX74xxKUW4t/Gmzc/fv/Tn/76+PHjnT8SzAfjBYWvBDCLqJnUm6eDQ1KyElMEmPlho/qZyZigsFLFLns8wLK6n3BDElA9/utf/wnan7DhfyApNvQ/3xMcprieA8BE67KsWAgYBgF8VTmzRZX1fniTkpbEty1PWRYren4GYjHefPzLs9Y334htWHNM3r7B1fFgn3q9BLCG0vSxgAkzmFcBJpOya+WObye0XFDoRnKV/ik1WdmHGC8//uUTkEXYCPrNN9HOrNYnAyLKXj0ap/FgSmzKtl1BSC6AIfgg5dYlFImlS2dLi5PGTC2iuniuKCe+Ie7bsV/ClP33T89a8/bp01/+9Mcf0apB7h9L+BTcksmXlb6rx4uUBlcl68fMApur00P++L9deQaT4T8SvKeDE1QXRzk6ehqlTYZhv3kJ7cf/BP+wbZ5NM/s0X351dmayU51kfJzWeyDUBeOvUpPYyVudtgDMKx5VH5aCDxolJXxxzWN+S7Fq71L5Q+o2Hhsz4mE0WfFzERoM/zASfPN0YpU73KqbffSQBS5b00ovzCYpjT69sHj1BL60IQJKCK1wYvFmelMt6MqqjBHVXKPHA7AFDq+nkEb8+viCK/omNa0s8M0Gz9JgzkwTwNhvbldZRTNuJk5FdkVc0tbVY5vVnKB5ipbImJ14IC6GpGxtIrubeBHY3WClNHw2scOGWSzu0sHcPk08YVist4Izw+As1uhXIxKNuYURWGTzz+D1drkZlt0JIOWsSiMVd5T6ySncPMUcVtQ/fUVpzImfLmxZvWL+NhYwzIRYkiCkYRRwNk9LWi22Jq67uky7SfYAf8CeO2HcNBY/KXAwzYuBD9N1UdUGqk4viivfDxIfDNFON/m64eb49PwHv4xJyYkst/r0MGWzJiCn+cCBubUbCZ3WpPmYBvjIv9eLfRIkgvMOwAfNkVhViaLXN4w7cp4Pk6qbhiHsODyNVqqfDtjuGn6LJVUdrAuYJhZ3IDM8B/dC42Zi+B3b4tPBFPdLUH4BJq6HV5Rfh6LZZZ4utVlZmq4B5n5Jq+aVFGvUFO16iIoSQ6mOTZK5oTsHhnzFhMRKBJC7bPH/fDSog5uEY59dRhRB7gpiKW+LVgUzDWJkbsA+P8+johLVzDmwliBC4Af1eqS1+CVO4oMqDUw7+px9ozLRVzfSWeB2+ZWHatQ5PbmT0k7yMuSJI5qc+oWJNbAhVvJHN1cmSQ8U+6A8gY9C5yZUnQ9EAZOCk3OdSvNCbSmrlehbV4ta0KXpbscCW2zSNUmFnMq1Sgu1IjZLCfPWeCzkS+WtVm4naOHmznfZKvZUlraBK2xWdj9edq3ltJrVUlVavbXxmktobrcAbsEpzIzRVF0PHGy4DY/fo1yuqWvVIhV7F1/hEawH5lse7K3dnhRfJV1qAKK2wR/OWcOTv5qWxVqbH2fxuVu45KTLLDCvAVx97cAByT/oUlqyO9z72oG9/Cmct6vFUTbcLf0lNO6FnSK7WnjlcoPdw19Ec3O88DJgvjhN/7qBc/ZpJYHTk5ifAEC/Zl7Kj8aixTZbcseUq9OOCJV9TXPDvF9o2uVM/kI0Ovf4ZWnZ+cq5Ot2OYl5DeU2INb/csZ06csYMvgiN9mlBYH6UVp6d1kViQz7+DHF+4oo4He/nS+Q8VuHqorxGH5xuhXCrr+ScuCQv3xLP9y4FS+qADPh7Yv/FPoqzDJ0sPu4uKOQrsjpRgRTbLn/PYECWHiguLTn0P//4Py86Hssgr998VJQ3nujuCUk8QYnqHUUibYzb856SmPzwNBm+7HV5D+kpS2z0MgnzAx6d/PDFZ/u58Frgl//+5oi/i88ZOQxDx9U5cqHdbcf55RUVho4/RjJhAEs/zHTyog55xcEl4iHidEm8Ju2/wFOvA/Lzy0gR9GQSzW8ZK+TJaT6wHAe3NAjKP7zlRjf/pGlp1cUOcq7x+9gSV1LM2A5tVh1JAYu4LikZOUx+lxyftUqjhbLxr+Uo1YkOXFJzPobHy3GLp+arTWazwxpg4Yq1XOA/fhMdZa+R73/j902lgfn27PhnVcNvs8T+G9nHn2w9FI+VGLCu8FvJwFzqKj6ZwQ/YGp6ELkrRKjv41ND5PJspiiYF8EWGn0W+zDNZ8srTloTZypQBUsA7j6jx/RvwTVlgln1Hq4yoFVk07GxbIQk7zoBVfJL7mn1ae608acuRyScy22COQxHa0cc0PrUVhXuG7IMwfHSzzGQtB3Zyz6VNA/8u6a/RKstZYD8xXj76aBAPM7f8TEJmytGOqxwY9+/44nMwRcRiemIcM6shs01+0cee4J8xoxJnjjvg09HplwIWZQBrJXALdPrlSwPn6iJwMA/HBVOoWTgrLeVIsVzHZadW0FzgmSTjTgrLDcRIysxaEttlB0Ey22DiRc9aN/dACousupxn2Zl4tJ03et4isPHbb29i4MvFUe5Hdsl24lUIR+KIEI8cwQcoV4RZdNYhlzC6X2HkOTB2hq8Qh5+R0FSOmPrhyHg5AiZL722Rlt6wpOeIeBF4yo5syAFOHlDFCt2W5gj1FjVvmU3yPp5vkQMcWwCu0lp8CG2fj5ApztsKs8CmsvL2JWnp+f+zHBGngfckm3DNzJ3D0Wi1+VRjN41784PBLHwDLQaMchVOjqOi2lIp+ca0gGdL7wKQ1lwall4KlgJ+Bgr620duJk/SwPywo2hytU1upKDPSWBIMViHBbC/AKxHf5HkAJtLgbl/WH691gpgPosvM8Dfx5dhWcQAm6Vl3RI/TH+WyJYtdhILDkxKpfGfYg5PxRM//NgisB+rNOXB91JgtiqVdNVCwFlDfbRQ+eCnPx48e/as9TtQGmxdoZwBnpFkMV9msmkzHUeF40ozZVos8/dhjQXfjm6ZAx/NVRr+AH6M31+GRsBfDkwVZc39aauAs5cAeIm0MfTIv3yMfq8nfkGZfI+iH2EK620K4Qd2Dd0QsWZhm0UN/cgGsSMoTJc5KyFhRQm6/XjS45y1XP4x4ZY48ILR8rmJVgsCLxL7i9c88IN98bGX5qEn/M0T6zj4L9zAdQNdSUdAPou4bRwCTdReROARSJFbksxEPDLjWSMeKa6yAxvldLwSBR45EuYiOll1Qd4q4GN+3KO1UPFI7G2IF6LqZDEdjjOPkO18YFZbZQ4rGSNiHojey+GWXDFBY3HqnzwR6Udk5bokE1qqWQl7SvbsjpXAiyLmxmf+2EVfXMcf7VDPVDzseXZEA7a70BJhvqPjGfiKyAKuRG2kbSJu2LeJiZJTcc+IkkweZJ99zOP61o0sBuhPN+GSjlCPVl7dKq2+EN5Kp4knJL0rML52wF/2iyiZS16+oYbtkGZqWrIjs9/FP/L3UDnxMSeu9sQvy8fpSlY2TZIL3+QRRx9xKh8mr+EwtbkU5dQvvvs8hVo977D0MleXRKfUHs3jLbXdbbPmhOlCvdqOWvi5Kvj8qqTpmjvF11w/JFbmfQ2P1ngWbcv9Da4fiq9JJ1/B01N+EeDaS+PXXCEWO2PtS+cVVz3SddfyrgUWlnord7bcYuOBvy3L5YEzdqu9wdW0d/a00Mh7XFjlGsB5+LF61XgoAtDLdPVejYqK2ioNWTxP6DL7ZMpV1z5qyAk5igFniPs6803+ylq/6KOX3sfdj+5oXvlA0ZhXsC9Zspl9uKKtXEjlsxArkyQVvNkyS8wuTD9a8XxMNSKZ6ElJqpLK4mf4/+JtSqkquzWXsOYvviX6hbfKYB2xEGu9QhcE5ovVVhgun5crbNvVZ1LbMy2Uk+zZnguRsfp323J1V/VQ2D8zlae65V3iv2zb58BYl1d1yTEsL5D8GQbX8CkImrXAsthg2e6qp9/Zi8PKAGenMS+7Lt0Jx0Skm7Lsw6CEXVW2A8j8tGPHglTIY6/PJPsSY1OeTWqS8x0w+LLsgeQg08ADdVVDVadTCI6B2SHucVsJpBm57LdZBd/1Vhno7K2lZe4fXma4lkVcssnSQCYH1IKwD73TdDa3IWVFRsOVujYoAffn0xOWKbLE03AQ2ERgmPAam8OBhAogdQ1phu9hn5KtVQuUMnemb3SlNmr1iYjccv+mF0sA7E1g+L7pccujmlLXFK9LNkPjKm1AnscnAogzCexzYBvtGLWlmbcGuG+T3KpOSeAsMS9i5j+OZ6apzTpkdVUscrVNVFvWZYc98Eajdem3Y7VUXUO61IVOAB2ukVANygcBgHEAIAdLALdzVVrmvNmcsOQt8TnEIuKy8pIhZoNxjgav2yp7NGJKOPNU3YDXsbLzBCVoRWtC8CGKLat4wM53NnNLuofOhaIxVhHYBXjV1LjeMGA9L7qlnNcOjwvylgCmjhjMHBm30RaFtulpJzNQaR0aUCmeF+gqCME0NeauNBJ7VQ+HoW17YNEklLBs255vHoNQ7e+Y/mu2jhZ8pgtgJ2/hWJ8XKGynqEKvAM4j5vFbnlb7LMAQT737DmVOVHVU7kyjp+F67GRVh78UhrHHhTexD4XiQ+It7DUVrfay+asYjlqYdwVwllhtZ+pVc+L16dTP1gbLznOCLzF/M6vAV/KuAs4l5sXFSsvH5a661YTBESW0dgn5lgQGYnEGyReQLM5W8FYEziGm0Za6z764UMR+Rkne1cC5xBZ/kPKZSyCsDnOkWE5J3jXAecSyyYn1z7i+mIolgWZIS/KuA84h7vd5lEnsz7bzxeEXohJPLs1bAVgUqze7fHob05f4/bzebQicS6wG4pnK51BrKp5jkRu1Au964HzitlAq4873gnTt6C9X4i0AnK/VoRfplXqXuGo0m0ynGm8R4FxiuS9KAsS+wyCkK1YxKn6/X423EHA+sTqL1lDqd1Sy7k/ZHzwi1hJ1LsBbDDifmMrROvi7ibsCQ/y5E7k6b0HgfGKZxn2wZreuzab4U0ZA5eq8RYGXEKthvM/Fu9UwZP539CXWqiBvYeAlxDJ1rXlXbg3XjxZZ2wHtb8RbHHgZsSpr8ZLv20EOp9EfUPxls7cwbwngZcQQhcT6Rryt+yhHrPtCFWovxS3MWwZ4uVpT14yRzWCL4abqetGCMHZ7xMa4JYGXC7kfT2Uwo/6WNFvW7BjXCvpbEG9p4KXEgBxYce8UL9g4FpHdWJcRV14q3XK8ZYGXE4M5mesfXmyxCTPQGvFXwSxZbqvK8pYGXonc757EUkE5a06VzCIM5rTsSpD+9nCrAK8gllUVl4InThKy9KAMtBq6vhXfdIC67LfpKtzSvFWAVxHLII25OvJjSW1Pm8nrqeWuptsJWCZcWaXyVnkrAa9Ghj46gacsnBlle37QdfK4VTnsBr5uKYQkP6OYmrNauFVwqwKvJgYx9x2ciGThyHBFsfF+Wt8XBwn4uu5ZtpJGZVvSPK0NXyJvn7cq8DpkYKahO03Ox5xjaUnebxVrGjj9NapcFXcD4HXEyKzK7eDEUhSiLGup0+NxX8NJ0AbTJ69vf7hz4ALIEHWqoN2udmIaSo44k9puWHhrD3yAyreIuxlwEWLurKgctgNtquOtywtnLRuW5Z1oaNBwcAp+4x8+E3BhZEaN3HLotLtudCCcO2u3HaYGxVk3w90YuAyyeFCTOA8NhqDfL/kF8ob93Ri4NPJmbePebgH4DpG30NetAN8R8lZ6uiXgO0DeUj+3BnzLyFvr5RaBb495m13cLvCtIG+3g9sG3jbz1nt3C8DbY76Nrt0O8DaYb6lftwa8EfQt9ulWgStB33J/bh24BPad9OSOgFeC32kP7hj487f/C62r3dEtXO+xAAAAAElFTkSuQmCC";

async function downloadJobSummaryPNG(job, partners) {
  try {
    let logo = null;
    try { logo = new Image(); logo.src = DD_LOGO_DATAURL; await logo.decode(); } catch(e) { logo = null; }
    try { if (document.fonts && document.fonts.ready) await Promise.race([document.fonts.ready, new Promise(function(r){setTimeout(r,1500);})]); } catch(e) {}

    const W = 1488, FOOTER_H = 112;
    const cv = document.createElement('canvas');
    cv.width = W; cv.height = 7000;
    const ctx = cv.getContext('2d');

    const INK='#0d1f43', INK2='#33415f', MUT='#6c768e', PAPER='#f5f2ea', LINE='#e7e1d2';
    const SUN='#f2a23d', SUND='#e07d18', TEAL='#3f97a0';
    const GRN='#059669', GRNB='#ecfdf5', ROSE='#e11d48', ROSEB='#fff1f2', AMB='#d97706', AMBB='#fffbeb';
    const FF = "'Sarabun','Anuphan',system-ui,'Noto Sans Thai',sans-serif";
    const font = (w, px) => w + ' ' + px + "px " + FF;
    const f0 = (n) => new Intl.NumberFormat('th-TH', { maximumFractionDigits: 0 }).format(Math.round(Number(n) || 0));
    const rr = (x, y, w, h, r) => {
      const rad = Math.max(0, Math.min(r, w/2, h/2));
      ctx.beginPath();
      ctx.moveTo(x+rad, y);
      ctx.arcTo(x+w, y, x+w, y+h, rad);
      ctx.arcTo(x+w, y+h, x, y+h, rad);
      ctx.arcTo(x, y+h, x, y, rad);
      ctx.arcTo(x, y, x+w, y, rad);
      ctx.closePath();
    };
    const wrap = (text, maxW) => {
      const arr = Array.from(text || ''); let lines = [], cur = '';
      for (const ch of arr) { const t = cur + ch; if (ctx.measureText(t).width > maxW && cur) { lines.push(cur); cur = ch; } else cur = t; }
      if (cur) lines.push(cur); return lines;
    };

    ctx.fillStyle = PAPER; ctx.fillRect(0, 0, W, 7000);
    ctx.textBaseline = 'alphabetic';

    // ===== HEADER =====
    ctx.fillStyle = INK; ctx.fillRect(0, 0, W, 300);
    if (logo) { try { ctx.drawImage(logo, 96, 62, 176, 176); } catch(e) {} }
    else { ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(184, 150, 88, 0, Math.PI*2); ctx.fill(); }
    ctx.textAlign = 'left';
    ctx.fillStyle = '#ffffff'; ctx.font = font('700', 54); ctx.fillText('D.D. Solution', 300, 138);
    ctx.fillStyle = '#9fd0d6'; ctx.font = font('500', 27); ctx.fillText('ระบบโซล่าเซลล์ครบวงจร · daddy solution', 300, 182);
    ctx.textAlign = 'right';
    ctx.fillStyle = '#ffffff'; ctx.font = font('600', 30); ctx.fillText('สรุปงาน', W-96, 120);
    const today = new Date().toLocaleDateString('th-TH', { day:'numeric', month:'short', year:'numeric' });
    ctx.fillStyle = '#aebbd2'; ctx.font = font('400', 23); ctx.fillText('ออกเอกสาร: ' + today, W-96, 158);
    ctx.font = font('600', 20);
    const tagT = 'เอกสารภายใน', tagW = ctx.measureText(tagT).width;
    ctx.fillStyle = 'rgba(242,162,61,0.20)'; rr(W-96-tagW-26, 178, tagW+26, 34, 9); ctx.fill();
    ctx.fillStyle = SUN; ctx.fillText(tagT, W-96-13, 201);

    // ===== JOB HEADER =====
    let y = 392;
    ctx.textAlign = 'left';
    ctx.fillStyle = INK; ctx.font = font('700', 46);
    const cust = job.customer || 'งาน';
    ctx.fillText(cust, 96, y);
    const titleW = ctx.measureText(cust).width;
    const done = job.status === 'completed';
    const stT = done ? '✓ เสร็จ' : '⏳ ดำเนินการ';
    ctx.font = font('600', 24);
    const stW = ctx.measureText(stT).width;
    ctx.fillStyle = done ? GRNB : AMBB; rr(96+titleW+26, y-30, stW+34, 42, 13); ctx.fill();
    ctx.fillStyle = done ? '#1c7a4a' : '#a5660f'; ctx.fillText(stT, 96+titleW+26+17, y-2);
    y += 52;
    ctx.fillStyle = MUT; ctx.font = font('400', 27);
    ctx.fillText((job.date || '') + '   ·   ' + (job.location || ''), 96, y);
    y += 44;
    ctx.fillStyle = SUND; ctx.font = font('600', 29);
    ctx.fillText(job.type || '', 96, y);
    if (job.phone) { y += 40; ctx.fillStyle = MUT; ctx.font = font('400', 25); ctx.fillText('โทร ' + job.phone, 96, y); }

    // ===== STAT CARDS =====
    y += 54;
    const sale = Number(job.salePrice)||0, cost = Number(job.totalCost)||0;
    const profit = (job.profit !== undefined && job.profit !== null) ? Number(job.profit) : (sale - cost);
    const margin = sale > 0 ? (profit/sale*100) : 0;
    const gap = 32, cardW = (1296 - 2*gap)/3, cardH = 188, cardY = y;
    const cards = [
      { x: 96, bg: GRNB, c: GRN, lbl: 'ยอดขาย', val: f0(sale)+' ฿', sub: '' },
      { x: 96+cardW+gap, bg: ROSEB, c: ROSE, lbl: 'ต้นทุนรวม', val: f0(cost)+' ฿', sub: '' },
      { x: 96+2*(cardW+gap), bg: AMBB, c: AMB, lbl: 'กำไร', val: f0(profit)+' ฿', sub: 'margin ' + margin.toFixed(1) + '%' },
    ];
    cards.forEach(c => {
      ctx.fillStyle = c.bg; rr(c.x, cardY, cardW, cardH, 20); ctx.fill();
      ctx.textAlign = 'left';
      ctx.fillStyle = c.c; ctx.font = font('600', 26); ctx.fillText(c.lbl, c.x+36, cardY+56);
      ctx.fillStyle = INK; ctx.font = font('700', 47);
      let vs = 47; while (ctx.measureText(c.val).width > cardW-64 && vs > 30) { vs -= 2; ctx.font = font('700', vs); }
      ctx.fillText(c.val, c.x+36, cardY+118);
      if (c.sub) { ctx.fillStyle = c.c; ctx.font = font('600', 24); ctx.fillText(c.sub, c.x+36, cardY+160); }
    });
    y = cardY + cardH + 56;

    // ===== COST BREAKDOWN =====
    const cbc = job.costsByCategory || {};
    let rows = Object.entries(cbc).map(([cid, items]) => {
      const list = items || [];
      const sub = list.reduce((s, it) => s + (Number(it.amount)||0), 0);
      const label = (typeof getCatLabel === 'function') ? getCatLabel(cid) : cid;
      return { cid, label, amount: sub, items: list };
    }).filter(r => r.amount > 0).sort((a, b) => b.amount - a.amount);

    const trunc = (text, maxW) => {
      if (ctx.measureText(text).width <= maxW) return text;
      let t = text;
      while (t.length > 1 && ctx.measureText(t + '\u2026').width > maxW) t = t.slice(0, -1);
      return t + '\u2026';
    };

    if (rows.length) {
      ctx.textAlign = 'left'; ctx.fillStyle = INK; ctx.font = font('700', 32);
      ctx.fillText('\u0e15\u0e49\u0e19\u0e17\u0e38\u0e19\u0e41\u0e22\u0e01\u0e2b\u0e21\u0e27\u0e14', 96, y);
      ctx.textAlign = 'right'; ctx.fillStyle = MUT; ctx.font = font('400', 24);
      ctx.fillText(rows.length + ' \u0e2b\u0e21\u0e27\u0e14', W-96, y);
      y += 38;
      const maxAmt = Math.max.apply(null, rows.map(r => r.amount));
      rows.forEach(r => {
        const isComm = r.cid === 'commission';
        ctx.textAlign = 'left'; ctx.fillStyle = INK; ctx.font = font('700', 26);
        ctx.fillText((isComm ? '\ud83c\udf81 ' : '') + r.label, 96, y+24);
        ctx.textAlign = 'right'; ctx.fillStyle = isComm ? SUND : INK; ctx.font = font('700', 26);
        ctx.fillText(f0(r.amount) + ' \u0e3f', W-96, y+24);
        ctx.fillStyle = '#ebe4d6'; rr(96, y+36, 1296, 10, 5); ctx.fill();
        const bw = Math.max(10, 1296 * (r.amount / maxAmt));
        ctx.fillStyle = isComm ? SUN : TEAL; rr(96, y+36, bw, 10, 5); ctx.fill();
        y += 56;
        (r.items || []).forEach(it => {
          const fromStock = !!it.stockId;
          const nm = (it.item && String(it.item).trim()) || '(\u0e44\u0e21\u0e48\u0e23\u0e30\u0e1a\u0e38\u0e0a\u0e37\u0e48\u0e2d)';
          ctx.textAlign = 'right'; ctx.font = font('500', 23); ctx.fillStyle = MUT;
          const amtTxt = f0(it.amount) + ' \u0e3f';
          const amtW = ctx.measureText(amtTxt).width;
          ctx.fillText(amtTxt, W-96, y+19);
          ctx.textAlign = 'left'; ctx.font = font('400', 23);
          ctx.fillStyle = fromStock ? '#1f8a70' : INK2;
          const prefix = fromStock ? '\ud83d\udce6 ' : '\u00b7  ';
          const maxNameW = (W-96) - 142 - amtW - 28;
          ctx.fillText(trunc(prefix + nm, maxNameW), 142, y+19);
          y += 33;
        });
        y += 18;
      });
    }

    // ===== INVESTORS =====
    const inv = Object.entries(job.investments || {}).filter(([k, v]) => Number(v) > 0);
    if (inv.length) {
      y += 24;
      ctx.textAlign = 'left'; ctx.fillStyle = INK; ctx.font = font('700', 30);
      ctx.fillText('เงินลงทุนหุ้นส่วน', 96, y);
      const hw = ctx.measureText('เงินลงทุนหุ้นส่วน').width;
      ctx.fillStyle = MUT; ctx.font = font('400', 20); ctx.fillText('  (ข้อมูลเดิม)', 96+hw, y);
      y += 26;
      let cx2 = 96; const chipH = 54;
      inv.forEach(([pid, amt]) => {
        const pr = (partners || []).find(pp => pp.id === pid);
        const nm = (pr && pr.name) || pid;
        ctx.font = font('600', 25);
        const nmw = ctx.measureText(nm).width;
        const amtTxt = '  ' + f0(amt);
        const amtw = ctx.measureText(amtTxt).width;
        const wpx = nmw + amtw + 40;
        if (cx2 + wpx > 96 + 1296) { cx2 = 96; y += chipH + 14; }
        ctx.fillStyle = '#eef3fb'; rr(cx2, y, wpx, chipH, 15); ctx.fill();
        ctx.textAlign = 'left'; ctx.fillStyle = INK; ctx.fillText(nm, cx2+20, y+35);
        ctx.fillStyle = TEAL; ctx.fillText(amtTxt, cx2+20+nmw, y+35);
        cx2 += wpx + 14;
      });
      y += chipH + 22;
    }

    // ===== NOTE =====
    if (job.note) {
      y += 6;
      ctx.font = font('400', 24);
      const lines = wrap('💬 ' + job.note, 1296 - 48).slice(0, 2);
      const boxH = 22 + lines.length * 34 + 10;
      ctx.fillStyle = '#fbf7ee'; rr(96, y, 1296, boxH, 14); ctx.fill();
      ctx.strokeStyle = LINE; ctx.lineWidth = 1.5; rr(96, y, 1296, boxH, 14); ctx.stroke();
      ctx.fillStyle = INK2; ctx.textAlign = 'left';
      lines.forEach((ln, i) => ctx.fillText(ln, 96+24, y+44+i*34));
      y += boxH + 20;
    }

    // ===== FOOTER + CROP TO CONTENT =====
    const contentBottom = Math.ceil(y);
    const finalH = Math.max(900, contentBottom + 44 + FOOTER_H);
    const out = document.createElement('canvas');
    out.width = W; out.height = finalH;
    const octx = out.getContext('2d');
    octx.fillStyle = PAPER; octx.fillRect(0, 0, W, finalH);
    octx.drawImage(cv, 0, 0, W, contentBottom, 0, 0, W, contentBottom);
    octx.fillStyle = INK; octx.fillRect(0, finalH-FOOTER_H, W, FOOTER_H);
    octx.fillStyle = SUN; octx.fillRect(0, finalH-FOOTER_H, W, 5);
    octx.textAlign = 'left'; octx.fillStyle = '#ffffff'; octx.font = font('700', 30);
    octx.fillText('D.D. Solution', 96, finalH-58);
    octx.fillStyle = '#9fb0cc'; octx.font = font('400', 22);
    octx.fillText('daddy solution \u00b7 \u0e42\u0e0b\u0e25\u0e48\u0e32\u0e40\u0e0b\u0e25\u0e25\u0e4c\u0e04\u0e23\u0e1a\u0e27\u0e07\u0e08\u0e23', 96, finalH-26);
    octx.textAlign = 'right'; octx.fillStyle = SUN; octx.font = font('600', 22);
    octx.fillText('\u0e40\u0e2d\u0e01\u0e2a\u0e32\u0e23\u0e2a\u0e23\u0e38\u0e1b\u0e20\u0e32\u0e22\u0e43\u0e19 \u2014 \u0e2a\u0e33\u0e2b\u0e23\u0e31\u0e1a\u0e2b\u0e38\u0e49\u0e19\u0e2a\u0e48\u0e27\u0e19', W-96, finalH-44);

    // ===== EXPORT =====
    const safe = (job.customer || 'job').replace(/[\\/:*?"<>|]/g, '').trim().slice(0, 40);
    out.toBlob((blob) => {
      if (!blob) { alert('\u0e2a\u0e23\u0e49\u0e32\u0e07\u0e20\u0e32\u0e1e\u0e44\u0e21\u0e48\u0e2a\u0e33\u0e40\u0e23\u0e47\u0e08'); return; }
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = '\u0e2a\u0e23\u0e38\u0e1b\u0e07\u0e32\u0e19_' + safe + '_' + (job.date || '') + '.png';
      document.body.appendChild(a); a.click();
      setTimeout(() => { URL.revokeObjectURL(url); a.remove(); }, 1500);
    }, 'image/png');
  } catch (err) {
    alert('สร้างภาพไม่สำเร็จ: ' + (err && err.message ? err.message : err));
  }
}

async function downloadStockSummaryPNG(stock, totalStockValue) {
  try {
    let logo = null;
    try { logo = new Image(); logo.src = DD_LOGO_DATAURL; await logo.decode(); } catch(e) { logo = null; }
    try { if (document.fonts && document.fonts.ready) await Promise.race([document.fonts.ready, new Promise(function(r){setTimeout(r,1500);})]); } catch(e) {}

    const W = 1488, FOOTER_H = 112;
    const cv = document.createElement('canvas');
    cv.width = W; cv.height = 8000;
    const ctx = cv.getContext('2d');

    const INK='#0d1f43', INK2='#33415f', MUT='#6c768e', PAPER='#f5f2ea', LINE='#e7e1d2';
    const SUN='#f2a23d', FOREST='#13543a', TEAL='#0f7a4f', TEALB='#e7f4ec';
    const font = (w, px) => w + ' ' + px + "px 'Sarabun','Anuphan',system-ui,'Noto Sans Thai',sans-serif";
    const f0 = (n) => new Intl.NumberFormat('th-TH', { maximumFractionDigits: 0 }).format(Math.round(Number(n) || 0));
    const f2 = (n) => new Intl.NumberFormat('th-TH', { maximumFractionDigits: 2 }).format(Number(n) || 0);
    const rr = (x, y, w, h, r) => { const rad = Math.max(0, Math.min(r, w/2, h/2)); ctx.beginPath(); ctx.moveTo(x+rad, y); ctx.arcTo(x+w, y, x+w, y+h, rad); ctx.arcTo(x+w, y+h, x, y+h, rad); ctx.arcTo(x, y+h, x, y, rad); ctx.arcTo(x, y, x+w, y, rad); ctx.closePath(); };
    const trunc = (text, maxW) => { if (ctx.measureText(text).width <= maxW) return text; let t = text; while (t.length > 1 && ctx.measureText(t + '\u2026').width > maxW) t = t.slice(0, -1); return t + '\u2026'; };
    const catLabel = (id) => { const arr = (typeof STOCK_CATEGORIES !== 'undefined' ? STOCK_CATEGORIES : []); const c = arr.find(x => x.id === id); return c ? c.label : ((typeof getCatLabel === 'function') ? getCatLabel(id) : id); };

    ctx.fillStyle = PAPER; ctx.fillRect(0, 0, W, 8000);
    ctx.textBaseline = 'alphabetic';

    // HEADER
    ctx.fillStyle = FOREST; ctx.fillRect(0, 0, W, 300);
    if (logo) { try { ctx.drawImage(logo, 96, 62, 176, 176); } catch(e) {} }
    else { ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(184, 150, 88, 0, Math.PI*2); ctx.fill(); }
    ctx.textAlign = 'left'; ctx.fillStyle = '#ffffff'; ctx.font = font('700', 54); ctx.fillText('D.D. Solution', 300, 138);
    ctx.fillStyle = '#a9e0c2'; ctx.font = font('500', 27); ctx.fillText('\u0e23\u0e30\u0e1a\u0e1a\u0e42\u0e0b\u0e25\u0e48\u0e32\u0e40\u0e0b\u0e25\u0e25\u0e4c\u0e04\u0e23\u0e1a\u0e27\u0e07\u0e08\u0e23 \u00b7 daddy solution', 300, 182);
    ctx.textAlign = 'right'; ctx.fillStyle = '#ffffff'; ctx.font = font('600', 30); ctx.fillText('\u0e2a\u0e23\u0e38\u0e1b\u0e2a\u0e15\u0e4a\u0e2d\u0e01', W-96, 120);
    const today = new Date().toLocaleDateString('th-TH', { day:'numeric', month:'short', year:'numeric' });
    ctx.fillStyle = '#aebbd2'; ctx.font = font('400', 23); ctx.fillText('\u0e13 \u0e27\u0e31\u0e19\u0e17\u0e35\u0e48 ' + today, W-96, 158);
    ctx.font = font('600', 20); const tagT = '\u0e40\u0e2d\u0e01\u0e2a\u0e32\u0e23\u0e20\u0e32\u0e22\u0e43\u0e19', tagW = ctx.measureText(tagT).width;
    ctx.fillStyle = 'rgba(242,162,61,0.20)'; rr(W-96-tagW-26, 178, tagW+26, 34, 9); ctx.fill();
    ctx.fillStyle = SUN; ctx.fillText(tagT, W-96-13, 201);

    // group active items by STOCK_CATEGORIES order
    const active = (stock || []).filter(s => Number(s.qty) > 0);
    const arr = (typeof STOCK_CATEGORIES !== 'undefined' ? STOCK_CATEGORIES : []);
    const seen = {}; let groups = [];
    arr.forEach(c => { const items = active.filter(s => s.category === c.id); if (items.length) { groups.push({ cid: c.id, label: c.label, items }); seen[c.id] = 1; } });
    active.forEach(s => { if (!seen[s.category]) { seen[s.category] = 1; groups.push({ cid: s.category, label: catLabel(s.category), items: active.filter(x => x.category === s.category) }); } });

    const grandValue = active.reduce((sum, s) => sum + Number(s.qty) * Number(s.unitCost), 0);
    const totalVal = (typeof totalStockValue === 'number' && totalStockValue > 0) ? totalStockValue : grandValue;

    // TITLE + SUMMARY CARD
    let y = 384;
    ctx.textAlign = 'left'; ctx.fillStyle = INK; ctx.font = font('700', 46);
    ctx.fillText('\u0e2a\u0e15\u0e4a\u0e2d\u0e01\u0e04\u0e07\u0e40\u0e2b\u0e25\u0e37\u0e2d', 96, y);
    y += 44;
    const cH = 150;
    ctx.fillStyle = TEALB; rr(96, y, 1296, cH, 20); ctx.fill();
    ctx.textAlign = 'left'; ctx.fillStyle = TEAL; ctx.font = font('600', 26); ctx.fillText('\u0e21\u0e39\u0e25\u0e04\u0e48\u0e32\u0e2a\u0e15\u0e4a\u0e2d\u0e01\u0e23\u0e27\u0e21', 136, y+58);
    ctx.fillStyle = INK; ctx.font = font('700', 60); ctx.fillText(f0(totalVal) + ' \u0e3f', 136, y+120);
    ctx.textAlign = 'right'; ctx.fillStyle = INK2; ctx.font = font('500', 26);
    ctx.fillText(active.length + ' \u0e23\u0e32\u0e22\u0e01\u0e32\u0e23 \u00b7 ' + groups.length + ' \u0e2b\u0e21\u0e27\u0e14', W-136, y+58);
    y += cH + 50;

    if (!groups.length) {
      ctx.textAlign = 'left'; ctx.fillStyle = MUT; ctx.font = font('400', 28);
      ctx.fillText('\u0e44\u0e21\u0e48\u0e21\u0e35\u0e2a\u0e15\u0e4a\u0e2d\u0e01\u0e04\u0e07\u0e40\u0e2b\u0e25\u0e37\u0e2d', 96, y); y += 40;
    }

    groups.forEach(g => {
      const catTotal = g.items.reduce((s, it) => s + Number(it.qty) * Number(it.unitCost), 0);
      ctx.textAlign = 'left'; ctx.fillStyle = INK; ctx.font = font('700', 30);
      ctx.fillText(g.label, 96, y+8);
      const lw = ctx.measureText(g.label).width;
      ctx.fillStyle = MUT; ctx.font = font('400', 22); ctx.fillText('  (' + g.items.length + ' \u0e23\u0e32\u0e22\u0e01\u0e32\u0e23)', 96+lw, y+8);
      ctx.textAlign = 'right'; ctx.fillStyle = TEAL; ctx.font = font('700', 28); ctx.fillText(f0(catTotal) + ' \u0e3f', W-96, y+8);
      y += 22;
      ctx.strokeStyle = LINE; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(96, y); ctx.lineTo(W-96, y); ctx.stroke();
      y += 16;
      g.items.forEach(it => {
        const qty = Number(it.qty) || 0, uc = Number(it.unitCost) || 0, unit = it.unit || '\u0e0a\u0e34\u0e49\u0e19';
        const total = qty * uc;
        ctx.textAlign = 'right'; ctx.font = font('700', 26); ctx.fillStyle = INK;
        const totalTxt = f0(total) + ' \u0e3f', totalW = ctx.measureText(totalTxt).width;
        ctx.fillText(totalTxt, W-96, y+26);
        ctx.textAlign = 'left'; ctx.font = font('600', 25); ctx.fillStyle = INK;
        const maxNameW = (W-96) - 96 - totalW - 40;
        ctx.fillText(trunc(it.name || '(\u0e44\u0e21\u0e48\u0e23\u0e30\u0e1a\u0e38)', maxNameW), 96, y+26);
        ctx.font = font('400', 22); ctx.fillStyle = MUT;
        const qtyStr = (it.category === 'wire') ? f2(qty) : f0(qty);
        ctx.fillText('\u0e04\u0e07\u0e40\u0e2b\u0e25\u0e37\u0e2d ' + qtyStr + ' ' + unit + '  \u00d7  ' + f2(uc) + ' \u0e3f/' + unit, 96, y+54);
        y += 70;
      });
      y += 20;
    });

    // FOOTER + CROP
    const contentBottom = Math.ceil(y);
    const finalH = Math.max(900, contentBottom + 44 + FOOTER_H);
    const out = document.createElement('canvas'); out.width = W; out.height = finalH;
    const octx = out.getContext('2d');
    octx.fillStyle = PAPER; octx.fillRect(0, 0, W, finalH);
    octx.drawImage(cv, 0, 0, W, contentBottom, 0, 0, W, contentBottom);
    octx.fillStyle = FOREST; octx.fillRect(0, finalH-FOOTER_H, W, FOOTER_H);
    octx.fillStyle = SUN; octx.fillRect(0, finalH-FOOTER_H, W, 5);
    octx.textAlign = 'left'; octx.fillStyle = '#ffffff'; octx.font = font('700', 30); octx.fillText('D.D. Solution', 96, finalH-58);
    octx.fillStyle = '#9fb0cc'; octx.font = font('400', 22); octx.fillText('daddy solution \u00b7 \u0e42\u0e0b\u0e25\u0e48\u0e32\u0e40\u0e0b\u0e25\u0e25\u0e4c\u0e04\u0e23\u0e1a\u0e27\u0e07\u0e08\u0e23', 96, finalH-26);
    octx.textAlign = 'right'; octx.fillStyle = SUN; octx.font = font('600', 22); octx.fillText('\u0e40\u0e2d\u0e01\u0e2a\u0e32\u0e23\u0e2a\u0e15\u0e4a\u0e2d\u0e01\u0e20\u0e32\u0e22\u0e43\u0e19 \u2014 \u0e2a\u0e33\u0e2b\u0e23\u0e31\u0e1a\u0e2b\u0e38\u0e49\u0e19\u0e2a\u0e48\u0e27\u0e19', W-96, finalH-44);

    out.toBlob((blob) => {
      if (!blob) { alert('\u0e2a\u0e23\u0e49\u0e32\u0e07\u0e20\u0e32\u0e1e\u0e44\u0e21\u0e48\u0e2a\u0e33\u0e40\u0e23\u0e47\u0e08'); return; }
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      const d = new Date(); const ds = d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0');
      a.href = url; a.download = '\u0e2a\u0e15\u0e4a\u0e2d\u0e01\u0e25\u0e48\u0e32\u0e2a\u0e38\u0e14_' + ds + '.png';
      document.body.appendChild(a); a.click();
      setTimeout(() => { URL.revokeObjectURL(url); a.remove(); }, 1500);
    }, 'image/png');
  } catch (err) {
    alert('\u0e2a\u0e23\u0e49\u0e32\u0e07\u0e20\u0e32\u0e1e\u0e44\u0e21\u0e48\u0e2a\u0e33\u0e40\u0e23\u0e47\u0e08: ' + (err && err.message ? err.message : err));
  }
}

function JobCard({ job, partners, fmt, fmt0, onEdit, onDelete, onExportExcel }) {
  const investmentEntries = Object.entries(job.investments || {});
  const isLocked = job.locked === true;
  // ขั้นตอนงาน: ล็อกแล้ว = ขั้น 10 (ปิดงาน) อย่างน้อย
  const wfStep = (isLocked || job.status === 'completed') ? Math.max(Number(job.workflowStep || 0), 10) : Number(job.workflowStep || 1);
  const wfInfo = JOB_WORKFLOW_STEPS.find(s => s.id === wfStep) || JOB_WORKFLOW_STEPS[0];
  const wfPct = Math.min(100, (wfStep / JOB_WORKFLOW_STEPS.length) * 100);
  return (
    <div className={`bg-white rounded-2xl p-5 shadow-sm border animate-slide-up ${isLocked ? 'border-stone-300 bg-stone-50/50' : 'border-stone-200'}`}>
      {/* 🔄 Workflow Progress */}
      <div className="mb-3 -mt-1">
        <div className="flex items-center justify-between text-xs mb-1">
          <span className="font-medium text-amber-700">{wfInfo.icon} ขั้น {wfStep}/{JOB_WORKFLOW_STEPS.length}: {wfInfo.label}</span>
          <span className="text-stone-400">{Math.round(wfPct)}%</span>
        </div>
        <div className="h-1.5 bg-stone-100 rounded-full overflow-hidden">
          <div className={`h-full rounded-full transition-all ${wfStep >= 10 ? 'bg-emerald-500' : 'bg-amber-400'}`} style={{ width: `${wfPct}%` }} />
        </div>
      </div>
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <h3 className="text-lg font-bold text-stone-800">{job.customer}</h3>
            <span className={`px-2 py-0.5 text-xs rounded-full font-medium ${job.status === 'completed' ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'}`}>
              {job.status === 'completed' ? '✓ เสร็จ' : '⏳ ดำเนินการ'}
            </span>
            {isLocked && (
              <span className="px-2 py-0.5 text-xs rounded-full font-medium bg-stone-200 text-stone-600" title={`ปิดงานโดย ${job.closedBy || '-'}`}>
                🔒 ปิดแล้ว
              </span>
            )}
          </div>
          <p className="text-sm text-stone-500">{job.date} · {job.location}</p>
          {job.phone && (
            <a href={`tel:${job.phone.replace(/[^0-9+]/g, '')}`} className="inline-flex items-center gap-1 text-sm text-blue-600 mt-0.5 hover:underline">
              📞 {job.phone}
            </a>
          )}
          <p className="text-sm text-amber-700 font-medium mt-1">{job.type}</p>
          {isLocked && job.closedBy && (
            <p className="text-[10px] text-stone-400 mt-0.5">🔒 ปิดงานโดย {job.closedBy} · {job.closedAt ? new Date(job.closedAt).toLocaleDateString('th-TH') : ''}</p>
          )}
        </div>
        <div className="flex gap-1">
          <button onClick={() => downloadJobSummaryPNG(job, partners)} title="📸 บันทึกภาพสรุปงาน (PNG · A4)"
            className="p-2 hover:bg-amber-50 rounded-lg"><Camera className="w-4 h-4 text-amber-600" /></button>
          <button onClick={onExportExcel} title="📊 Export แฟ้มงาน Excel — รายละเอียดครบทุกอย่างของงานนี้"
            className="p-2 hover:bg-emerald-50 rounded-lg"><Download className="w-4 h-4 text-emerald-600" /></button>
          <button onClick={() => {
            if (isLocked) {
              if (!window.confirm('🔒 งานนี้ปิดแล้ว ตัวเลขถูกล็อก\n\nการแก้ไขงานที่ปิดแล้วอาจทำให้ตัวเลขการเงินไม่ตรง\n\nต้องการเปิดดู/แก้ไขหรือไม่?')) return;
            }
            onEdit();
          }} className="p-2 hover:bg-stone-100 rounded-lg"><Edit2 className="w-4 h-4 text-stone-500" /></button>
          <button onClick={() => {
            if (isLocked) {
              alert('🔒 งานนี้ปิดแล้ว ไม่สามารถลบได้\n\nหากต้องการลบจริงๆ ให้ติดต่อผู้ดูแลระบบ');
              return;
            }
            onDelete();
          }} className="p-2 hover:bg-red-50 rounded-lg"><Trash2 className="w-4 h-4 text-red-400" /></button>
        </div>
      </div>
      <div className="grid grid-cols-3 gap-2 mb-3">
        <div className="bg-emerald-50 rounded-lg p-2 text-center"><div className="text-xs text-emerald-600">ยอดขาย</div><div className="font-bold text-emerald-700">{fmt0(job.salePrice)} ฿</div></div>
        <div className="bg-rose-50 rounded-lg p-2 text-center"><div className="text-xs text-rose-600">ต้นทุน</div><div className="font-bold text-rose-700">{fmt0(job.totalCost)} ฿</div></div>
        <div className="bg-amber-50 rounded-lg p-2 text-center"><div className="text-xs text-amber-600">กำไร</div><div className="font-bold text-amber-700">{fmt0(job.profit)} ฿</div></div>
      </div>
      {/* 📋 กำไรระยะยาว (รวมบริการหลังการขาย) */}
      {(() => {
        const svcLog = Array.isArray(job.serviceLog) ? job.serviceLog : [];
        if (svcLog.length === 0) return null;
        const svcNet = svcLog.reduce((s, l) => s + Number(l.income || 0) - Number(l.cost || 0), 0);
        const longTerm = Number(job.profit || 0) + svcNet;
        return (
          <div className="mb-3 flex items-center justify-between bg-sky-50 border border-sky-200 rounded-lg px-3 py-1.5 text-xs">
            <span className="text-sky-700">📋 บริการ {svcLog.length} ครั้ง · สุทธิ <span className={`font-mono font-bold ${svcNet >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>{svcNet >= 0 ? '+' : ''}{fmt0(svcNet)}</span></span>
            <span className="text-stone-600">กำไรระยะยาว: <span className={`font-bold font-mono ${longTerm >= 0 ? 'text-emerald-700' : 'text-rose-700'}`}>{fmt0(longTerm)} ฿</span></span>
          </div>
        );
      })()}
      {investmentEntries.length > 0 && (
        <div className="mb-3 p-3 bg-blue-50 rounded-lg border border-blue-100">
          <div className="text-xs font-medium text-blue-700 mb-1">💰 ใครออกเงินทุน <span className="text-stone-400 font-normal">(ข้อมูลเก่า — ปัจจุบันใช้เงินบริษัท)</span></div>
          <div className="flex flex-wrap gap-2">
            {investmentEntries.map(([pid, amt]) => {
              const partner = partners.find(p => p.id === pid);
              return (
                <div key={pid} className="text-xs bg-white px-2 py-1 rounded-md">
                  <span className="font-medium">{partner?.name || pid}</span>: <span className="text-blue-600 font-mono">{fmt(amt)}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}
      {job.costsByCategory && Object.keys(job.costsByCategory).length > 0 && (
        <details className="text-sm">
          <summary className="cursor-pointer text-stone-600 hover:text-amber-600 font-medium">ดูรายละเอียดต้นทุนแยกหมวด</summary>
          <div className="mt-2 space-y-2">
            {Object.entries(job.costsByCategory).map(([catId, items]) => {
              if (!items || items.length === 0) return null;
              const subtotal = items.reduce((s, it) => s + Number(it.amount || 0), 0);
              return (
                <div key={catId} className="bg-stone-50 rounded-lg p-2">
                  <div className="flex justify-between text-xs font-semibold text-amber-700 mb-1">
                    <span>{getCatLabel(catId)}</span><span>{fmt0(subtotal)} ฿</span>
                  </div>
                  <div className="space-y-0.5 pl-3">
                    {items.map((it, i) => (
                      <div key={i} className="flex justify-between text-xs text-stone-600">
                        <span>{it.item}</span><span className="font-mono">{fmt0(it.amount)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </details>
      )}
      {job.note && <div className="mt-3 text-sm text-stone-500 bg-stone-50 rounded-lg p-2">💬 {job.note}</div>}
    </div>
  );
}

function StockRow({ item, fmt, fmt0, onEdit, onDelete }) {
  const isHistory = Number(item.qty) === 0;
  const ownerColors = {
    'อาม': 'bg-blue-100 text-blue-700',
    'โฟน': 'bg-purple-100 text-purple-700',
    'พ่อ': 'bg-green-100 text-green-700',
    'บริษัท': 'bg-amber-100 text-amber-700',
  };
  // คำนวณ low-stock: ถ้าเป็นสายไฟและเหลือ < 20 ม. หรือของอื่นเหลือ < 5 ชิ้น
  const isLowStock = !isHistory && (
    (item.category === 'wire' && Number(item.qty) < 20) ||
    (item.category !== 'wire' && Number(item.qty) > 0 && Number(item.qty) < 3)
  );
  const stockValue = Number(item.qty) * Number(item.unitCost);
  
  return (
    <div className={`flex items-center gap-3 p-3 rounded-xl transition-colors ${isHistory ? 'bg-stone-50 opacity-60' : 'hover:bg-stone-50'}`}>
      <div className="flex-1 min-w-0">
        <div className="font-medium text-stone-800 truncate flex items-center gap-2 flex-wrap">
          {item.name}
          {item.owner && item.owner !== '-' && (
            <span className={`text-xs px-1.5 py-0.5 rounded font-medium ${ownerColors[item.owner] || 'bg-stone-200 text-stone-700'}`}>
              {item.owner}
            </span>
          )}
          {isLowStock && <span className="text-xs bg-orange-100 text-orange-700 px-1.5 py-0.5 rounded font-medium">⚠ เหลือน้อย</span>}
          {isHistory && <span className="text-xs bg-stone-200 px-1.5 py-0.5 rounded">ประวัติ</span>}
        </div>
        <div className="text-xs text-stone-500">
          {item.purchaseDate && <span>📅 {item.purchaseDate} · </span>}
          {item.supplier && `${item.supplier}`}
          {item.note && ` · ${item.note}`}
        </div>
      </div>
      <div className="text-center">
        <div className={`text-lg font-bold ${Number(item.qty) > 0 ? (isLowStock ? 'text-orange-600' : 'text-emerald-600') : 'text-stone-400'}`}>{fmt(item.qty)}</div>
        <div className="text-xs text-stone-400">{item.unit || 'ชิ้น'}</div>
      </div>
      <div className="text-right">
        <div className="font-semibold text-stone-700">{fmt(item.unitCost)} ฿</div>
        <div className="text-xs text-stone-400">/{item.unit || 'ชิ้น'}</div>
        {!isHistory && stockValue > 0 && (
          <div className="text-xs text-amber-600 font-medium mt-0.5">รวม {fmt0(stockValue)} ฿</div>
        )}
      </div>
      <div className="flex gap-1">
        <button onClick={onEdit} className="p-2 hover:bg-stone-200 rounded-lg"><Edit2 className="w-4 h-4 text-stone-500" /></button>
        <button onClick={onDelete} className="p-2 hover:bg-red-50 rounded-lg"><Trash2 className="w-4 h-4 text-red-400" /></button>
      </div>
    </div>
  );
}

function Modal({ title, children, onClose, wide }) {
  return (
    // ✨ ไม่ปิดเมื่อคลิกนอกกรอบ — กันข้อมูลที่กรอกอยู่หาย (ออกได้ทางปุ่ม ✕ เท่านั้น)
    <div className="fixed inset-0 bg-black/50 z-50 flex items-end md:items-center justify-center p-0 md:p-4 animate-fade-in">
      <div
        className={`bg-white w-full ${wide ? 'md:max-w-2xl' : 'md:max-w-lg'} md:rounded-2xl rounded-t-2xl shadow-xl max-h-[95vh] md:max-h-[90vh] overflow-hidden flex flex-col animate-slide-up`}
        onClick={(e) => e.stopPropagation()}
        style={{
          paddingTop: 'env(safe-area-inset-top)',
          paddingBottom: 'env(safe-area-inset-bottom)',
        }}
      >
        {/* Sticky Header */}
        <div className="sticky top-0 bg-white flex items-center justify-between p-4 border-b border-stone-200 z-10 flex-shrink-0">
          <h3 className="display-font text-xl text-stone-800">{title}</h3>
          <button
            onClick={onClose}
            className="p-3 hover:bg-stone-100 active:bg-stone-200 rounded-lg transition-colors"
            style={{ minWidth: '44px', minHeight: '44px' }}
            title="ปิด (Esc)"
            aria-label="ปิด"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        {/* Scrollable content */}
        <div className="overflow-y-auto p-4 flex-1" style={{WebkitOverflowScrolling: 'touch'}}>{children}</div>
      </div>
    </div>
  );
}

function Field({ label, children, hint }) {
  return (
    <div className="mb-3">
      <label className="block text-sm font-medium text-stone-700 mb-1">{label}</label>
      {children}
      {hint && <p className="text-xs text-stone-500 mt-1">{hint}</p>}
    </div>
  );
}

const inputCls = "w-full px-3 py-2 border border-stone-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400 focus:border-transparent";

function PickQuotationModal({ documents, fmt, onClose, onSelect }) {
  // หาใบเสนอราคา active ที่ยังไม่ผูก job
  const availableQuotations = documents
    .filter(d => d.type === 'quotation' && d.jobStatus === 'active' && !d.jobId)
    .sort((a, b) => (b.createdAt || '') > (a.createdAt || '') ? 1 : -1);
  
  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-end md:items-center justify-center md:p-4 animate-fade-in">
      <div className="bg-white w-full md:max-w-2xl md:rounded-2xl rounded-t-2xl shadow-xl max-h-[90vh] flex flex-col animate-slide-up">
        <div className="px-4 py-3 border-b border-stone-200 flex items-center justify-between">
          <h3 className="font-bold text-stone-800">🚀 เลือกใบเสนอราคา</h3>
          <button onClick={onClose} className="p-1 hover:bg-stone-100 rounded">
            <X className="w-5 h-5 text-stone-500" />
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-3">
          {availableQuotations.length === 0 ? (
            <div className="text-center py-8 text-stone-500">
              <div className="text-4xl mb-2">📭</div>
              <p>ไม่มีใบเสนอราคาที่ยังไม่ได้สร้างงาน</p>
            </div>
          ) : (
            <div className="space-y-2">
              {availableQuotations.map(q => {
                const snap = q.equipmentSnapshot || {};
                return (
                  <button key={q.id} onClick={() => onSelect(q)}
                    className="w-full text-left bg-white border-2 border-stone-200 hover:border-emerald-400 hover:bg-emerald-50 rounded-xl p-3 transition-all">
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 flex-wrap mb-1">
                          <span className="font-mono text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded">{q.docNumber}</span>
                          <span className="text-xs text-stone-500">{q.docDate}</span>
                        </div>
                        <h4 className="font-bold text-stone-800">{q.customerName || '-'}</h4>
                        {q.customerPhone && <p className="text-xs text-stone-500">📞 {q.customerPhone}</p>}
                        {snap.jobType && <p className="text-xs text-emerald-700 mt-1">⚡ {snap.jobType}</p>}
                      </div>
                      <div className="text-right flex-shrink-0">
                        <div className="text-lg font-bold text-amber-600">{fmt(q.totalAmount || 0)} ฿</div>
                        {snap.expectedProfit > 0 && (
                          <div className="text-xs text-emerald-600 font-medium">
                            กำไร ~{fmt(snap.expectedProfit)} ฿
                          </div>
                        )}
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>
          )}
        </div>
        <div className="px-4 py-3 border-t border-stone-200 bg-stone-50 text-xs text-stone-600">
          💡 เลือกใบเสนอราคา → ระบบจะ auto-fill ฟอร์มเพิ่มงานให้คุณ
        </div>
      </div>
    </div>
  );
}

function JobModal({ job, partners, stock = [], documents = [], onUpdateStock, onClose, onSave }) {
  const [form, setForm] = useState(job || {
    date: new Date().toISOString().split('T')[0],
    customer: '', location: '', type: '',
    salePrice: 0, originalPrice: 0, discount: 0, discountNote: '',
    status: 'pending', investments: {}, costsByCategory: {},
    totalCost: 0, profit: 0, note: ''
  });
  const [costsByCategory, setCostsByCategory] = useState(form.costsByCategory || {});
  // ✨ investments = data เก่า (read-only) — โครงสร้างใหม่ไม่กรอกแล้ว เก็บไว้เพื่อ backward compat
  const investments = form.investments || {};
  // 🔄 Workflow: ขั้นตอนงาน + checklist ของติดตั้ง
  const [workflowStep, setWorkflowStep] = useState(Number(form.workflowStep || 1));
  const [checklist, setChecklist] = useState(() => {
    if (Array.isArray(form.checklist) && form.checklist.length > 0) return form.checklist;
    // init จาก template มาตรฐาน
    const items = [];
    DEFAULT_INSTALL_CHECKLIST.forEach(g => g.items.forEach(it => items.push({ group: g.group, text: it, done: false })));
    return items;
  });
  const [newCheckItem, setNewCheckItem] = useState('');
  const wfCurrent = JOB_WORKFLOW_STEPS.find(s => s.id === workflowStep) || JOB_WORKFLOW_STEPS[0];
  // 📋 บันทึกงาน + บริการหลังการขาย (ปัญหา/ฟีดแบ็ก/ล้างแผง/ซ่อม) — เพิ่มได้แม้งานปิดแล้ว
  const [serviceLog, setServiceLog] = useState(Array.isArray(form.serviceLog) ? form.serviceLog : []);
  const [svc, setSvc] = useState({ date: new Date().toISOString().split('T')[0], type: 'note', note: '', income: '', cost: '' });
  const SVC_TYPES = [
    { id: 'issue', icon: '🐛', label: 'ปัญหา' },
    { id: 'feedback', icon: '💬', label: 'ฟีดแบ็ก' },
    { id: 'clean', icon: '🧽', label: 'ล้างแผง' },
    { id: 'repair', icon: '🔧', label: 'ซ่อม' },
    { id: 'followup', icon: '📞', label: 'ติดตามผล' },
    { id: 'note', icon: '📝', label: 'บันทึกทั่วไป' },
  ];
  const [stockPicker, setStockPicker] = useState(null); // { catId, mode: 'pick' | 'qty', stockId }
  const [pickQty, setPickQty] = useState('');
  // Track stock movements: { stockId: qtyUsed } - เก็บไว้เพื่อหักสต๊อกตอน save
  const [stockMovements, setStockMovements] = useState(() => {
    // ถ้าเป็นการแก้ไขงาน เริ่มจากของที่เคยเบิกแล้วเป็น 0 (ไม่หักซ้ำ)
    return {};
  });

  const update = (f, v) => setForm({...form, [f]: v});
  
  const addCostItem = (catId) => setCostsByCategory({...costsByCategory, [catId]: [...(costsByCategory[catId] || []), { item: '', amount: 0 }]});
  
  // เพิ่มรายการจากสต๊อก
  const addCostFromStock = (catId, stockItem, qty) => {
    const totalAmount = Number(qty) * Number(stockItem.unitCost);
    const newItem = {
      item: `${stockItem.name} × ${qty} ${stockItem.unit || 'ชิ้น'} (เบิกสต๊อก)`,
      amount: Number(totalAmount.toFixed(2)),
      stockId: stockItem.id,
      qtyUsed: Number(qty),
    };
    setCostsByCategory({
      ...costsByCategory,
      [catId]: [...(costsByCategory[catId] || []), newItem]
    });
    setStockMovements({
      ...stockMovements,
      [stockItem.id]: (stockMovements[stockItem.id] || 0) + Number(qty)
    });
    setStockPicker(null);
    setPickQty('');
  };
  
  const updateCostItem = (catId, i, field, val) => {
    const newItems = [...(costsByCategory[catId] || [])];
    newItems[i] = { ...newItems[i], [field]: val };
    setCostsByCategory({...costsByCategory, [catId]: newItems});
  };
  
  const removeCostItem = (catId, i) => {
    const item = (costsByCategory[catId] || [])[i];
    // ถ้าเป็นรายการเบิกสต๊อก คืนให้สต๊อก
    if (item && item.stockId) {
      setStockMovements({
        ...stockMovements,
        [item.stockId]: Math.max(0, (stockMovements[item.stockId] || 0) - Number(item.qtyUsed || 0))
      });
    }
    const newItems = (costsByCategory[catId] || []).filter((_, idx) => idx !== i);
    if (newItems.length === 0) {
      const { [catId]: _, ...rest } = costsByCategory;
      setCostsByCategory(rest);
    } else setCostsByCategory({...costsByCategory, [catId]: newItems});
  };

  const totalCost = useMemo(() => {
    return Object.values(costsByCategory).reduce((sum, items) => sum + (items || []).reduce((s, it) => s + Number(it.amount || 0), 0), 0);
  }, [costsByCategory]);

  const handleSave = () => {
    const profit = Number(form.salePrice || 0) - totalCost;
    // ✨ โครงสร้างใหม่: เงินบริษัทจ่ายทุกอย่าง — investments เก็บแค่ data เก่า (read-only legacy)
    const cleanInv = Object.entries(investments).reduce((acc, [k, v]) => {
      if (Number(v) > 0) acc[k] = Number(v);
      return acc;
    }, {});
    
    // หักสต๊อกตามที่เบิก
    if (Object.keys(stockMovements).length > 0 && onUpdateStock) {
      const newStock = stock.map(s => {
        if (stockMovements[s.id]) {
          return { ...s, qty: Math.max(0, Number(s.qty) - stockMovements[s.id]) };
        }
        return s;
      });
      onUpdateStock(newStock);
    }
    
    onSave({...form, costsByCategory, investments: cleanInv, totalCost, profit, workflowStep, checklist, serviceLog});
  };

  return (
    <Modal title={job ? 'แก้ไขงาน' : 'เพิ่มงานใหม่'} onClose={onClose} wide>
      {/* === 🔄 Workflow Stepper === */}
      <div className="mb-4 bg-gradient-to-br from-amber-50 to-orange-50 border-2 border-amber-200 rounded-2xl p-3">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-bold text-amber-900">🔄 ขั้นตอนงาน</span>
          <span className="text-xs text-stone-500">ขั้น {workflowStep}/{JOB_WORKFLOW_STEPS.length}</span>
        </div>
        {/* แถวปุ่มขั้นตอน — กดเลือกขั้นปัจจุบัน */}
        <div className="flex gap-1 overflow-x-auto pb-1 mb-2">
          {JOB_WORKFLOW_STEPS.map(s => {
            const isDone = s.id < workflowStep;
            const isCurrent = s.id === workflowStep;
            return (
              <button key={s.id} type="button"
                onClick={() => setWorkflowStep(s.id)}
                title={`${s.label}${s.optional ? ' (ข้ามได้)' : ''}`}
                className={`flex-shrink-0 w-9 h-9 rounded-full text-sm flex items-center justify-center border-2 transition-all ${
                  isCurrent ? 'bg-amber-500 border-amber-600 text-white scale-110 shadow-md' :
                  isDone ? 'bg-emerald-100 border-emerald-300' :
                  'bg-white border-stone-200 opacity-60'
                }`}>
                {isDone ? '✓' : s.icon}
              </button>
            );
          })}
        </div>
        {/* ขั้นปัจจุบัน + คำแนะนำ */}
        <div className="bg-white/70 rounded-xl p-2.5">
          <div className="font-medium text-sm text-stone-800 flex items-center gap-1.5">
            {wfCurrent.icon} {wfCurrent.label}
            {wfCurrent.optional && <span className="text-[10px] bg-stone-100 text-stone-500 px-1.5 py-0.5 rounded">ข้ามได้</span>}
          </div>
          <div className="text-xs text-stone-600 mt-1 leading-relaxed">{wfCurrent.hint}</div>
          {workflowStep < JOB_WORKFLOW_STEPS.length && (
            <button type="button"
              onClick={() => setWorkflowStep(workflowStep + 1)}
              className="mt-2 text-xs bg-amber-500 hover:bg-amber-600 text-white px-3 py-1.5 rounded-lg font-medium">
              ✓ เสร็จขั้นนี้ → ไปขั้นถัดไป
            </button>
          )}
        </div>
        {/* 📦 Checklist — โผล่ตอนขั้น 5-7 (สำรวจ/เตรียมของ/ติดตั้ง) */}
        {workflowStep >= 5 && workflowStep <= 7 && (
          <div className="mt-2 bg-white/70 rounded-xl p-2.5">
            {(() => {
              const doneCount = checklist.filter(i => i.done).length;
              const groups = [...new Set(checklist.map(i => i.group || 'อื่นๆ'))];
              return (
                <>
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-xs font-bold text-stone-700">📦 Checklist ของติดตั้ง</span>
                    <span className={`text-[11px] font-medium ${doneCount === checklist.length ? 'text-emerald-600' : 'text-amber-600'}`}>
                      {doneCount}/{checklist.length} {doneCount === checklist.length ? '✅ ครบ!' : ''}
                    </span>
                  </div>
                  <div className="max-h-44 overflow-y-auto space-y-1.5 pr-1">
                    {groups.map(g => (
                      <div key={g}>
                        <div className="text-[10px] font-bold text-amber-700 mb-0.5">{g}</div>
                        {checklist.map((item, idx) => (item.group || 'อื่นๆ') === g && (
                          <label key={idx} className="flex items-center gap-2 text-xs py-0.5 cursor-pointer hover:bg-amber-50 rounded px-1">
                            <input type="checkbox" checked={item.done}
                              onChange={() => setChecklist(checklist.map((it, i) => i === idx ? { ...it, done: !it.done } : it))}
                              className="w-3.5 h-3.5 rounded text-emerald-500 flex-shrink-0" />
                            <span className={item.done ? 'line-through text-stone-400' : 'text-stone-700'}>{item.text}</span>
                            <button type="button" onClick={(e) => { e.preventDefault(); setChecklist(checklist.filter((_, i) => i !== idx)); }}
                              className="ml-auto text-stone-300 hover:text-red-400 text-[10px] px-1">✕</button>
                          </label>
                        ))}
                      </div>
                    ))}
                  </div>
                  <div className="flex gap-1 mt-1.5">
                    <input value={newCheckItem} onChange={e => setNewCheckItem(e.target.value)}
                      onKeyDown={e => { if (e.key === 'Enter' && newCheckItem.trim()) { setChecklist([...checklist, { group: 'เพิ่มเอง', text: newCheckItem.trim(), done: false }]); setNewCheckItem(''); } }}
                      className="flex-1 text-xs border border-stone-200 rounded-lg px-2 py-1.5" placeholder="+ เพิ่มรายการ (Enter)" />
                  </div>
                </>
              );
            })()}
          </div>
        )}
      </div>

      {/* === Quotation Link Badge === */}
      {form.quotationId && (
        <div className="mb-3 bg-emerald-50 border-2 border-emerald-300 rounded-xl p-3">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-lg">🔗</span>
            <span className="font-bold text-emerald-800 text-sm">สร้างจากใบเสนอราคา</span>
            {form.docNumber && (
              <span className="font-mono text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded">{form.docNumber}</span>
            )}
          </div>
          <div className="text-xs text-emerald-700">
            ✓ ข้อมูลลูกค้า, ที่อยู่, ราคาขาย กรอกอัตโนมัติแล้ว
          </div>
        </div>
      )}
      
      <Field label="วันที่"><input type="date" value={form.date} onChange={e => update('date', e.target.value)} className={inputCls} /></Field>
      <Field label="ลูกค้า"><input value={form.customer} onChange={e => update('customer', e.target.value)} className={inputCls} placeholder="ชื่อลูกค้า" /></Field>
      <Field label="เบอร์ติดต่อ"><input type="tel" value={form.phone || ''} onChange={e => update('phone', e.target.value)} className={inputCls} placeholder="08x-xxx-xxxx" /></Field>
      <Field label="สถานที่"><input value={form.location} onChange={e => update('location', e.target.value)} className={inputCls} /></Field>
      <Field label="ประเภทงาน"><input value={form.type} onChange={e => update('type', e.target.value)} className={inputCls} placeholder="เช่น 5kW Hybrid" /></Field>
      <div className="grid grid-cols-2 gap-3">
        <Field label="ราคาขาย (฿)" hint={form.expectedProfit > 0 ? `💡 คาดกำไร: ~${(form.expectedProfit).toLocaleString()} ฿ (จากใบเสนอ)` : null}>
          <input type="number" value={form.salePrice} onChange={e => update('salePrice', Number(e.target.value))} className={inputCls} />
        </Field>
        <Field label="สถานะ">
          <select value={form.status} onChange={e => update('status', e.target.value)} className={inputCls}>
            <option value="pending">กำลังดำเนินการ</option>
            <option value="completed">เสร็จแล้ว</option>
          </select>
        </Field>
      </div>

      <div className="mt-4 mb-2">
        <div className="flex items-center justify-between mb-2">
          <label className="text-sm font-bold text-stone-700 block">📋 ต้นทุนแยกหมวด</label>
          {/* ปุ่มดึงข้อมูลจากใบเสนอราคา */}
          {(() => {
            const quotation = form.quotationId ? documents.find(d => d.id === form.quotationId) : null;
            const snap = quotation?.equipmentSnapshot;
            if (!snap) return null;
            
            return (
              <button 
                type="button"
                onClick={() => {
                  const newCosts = { ...costsByCategory };
                  const messages = [];
                  
                  // แผงโซล่า
                  if (snap.panel) {
                    const items = newCosts.panel || [];
                    const itemName = `${snap.panel.brand} ${snap.panel.model}`;
                    const qty = snap.panel.qty;
                    const unitPrice = snap.panel.costEach;
                    const itemAmount = snap.panel.total || (unitPrice * qty);
                    const exists = items.some(it => it.item === itemName);
                    if (!exists) {
                      newCosts.panel = [...items, { item: itemName, qty, unitPrice, amount: itemAmount }];
                      messages.push(`✓ แผงโซล่า: ${itemName} × ${qty} แผ่น`);
                    }
                  }
                  
                  // อินเวอร์เตอร์
                  if (snap.inverter) {
                    const items = newCosts.inverter || [];
                    const itemName = `${snap.inverter.brand} ${snap.inverter.model}`;
                    const itemAmount = snap.inverter.cost;
                    const exists = items.some(it => it.item === itemName);
                    if (!exists) {
                      newCosts.inverter = [...items, { item: itemName, qty: 1, unitPrice: itemAmount, amount: itemAmount }];
                      messages.push(`✓ อินเวอร์เตอร์: ${itemName}`);
                    }
                  }
                  
                  // แบตเตอรี่
                  if (snap.battery) {
                    const items = newCosts.battery || [];
                    const itemName = `${snap.battery.brand} ${snap.battery.model}`;
                    const itemAmount = snap.battery.cost;
                    const exists = items.some(it => it.item === itemName);
                    if (!exists) {
                      newCosts.battery = [...items, { item: itemName, qty: 1, unitPrice: itemAmount, amount: itemAmount }];
                      messages.push(`✓ แบตเตอรี่: ${itemName}`);
                    }
                  }
                  
                  if (messages.length === 0) {
                    alert('⚠️ ดึงไม่ได้ - รายการอาจมีอยู่แล้ว หรือใบเสนอราคาไม่มีข้อมูลอุปกรณ์');
                    return;
                  }
                  
                  setCostsByCategory(newCosts);
                  alert(`📥 ดึงข้อมูลจากใบเสนอราคาเรียบร้อย!\n\n${messages.join('\n')}\n\n💡 กดที่รายการเพื่อปรับแก้ชื่อ/ราคาได้`);
                }}
                className="text-xs bg-violet-500 hover:bg-violet-600 text-white px-3 py-1.5 rounded-lg font-medium flex items-center gap-1"
                title="ดึงรายการ inverter/แผง/แบต จากใบเสนอราคา"
              >
                📥 ดึงจากใบเสนอราคา
              </button>
            );
          })()}
        </div>
        {COST_CATEGORIES.map(cat => {
          const items = costsByCategory[cat.id] || [];
          const subtotal = items.reduce((s, it) => s + Number(it.amount || 0), 0);
          // เช็คว่าหมวดนี้มีของในสต๊อกไหม
          const stockInCat = stock.filter(s => s.category === cat.id && Number(s.qty) > 0);
          
          if (items.length === 0) {
            return (
              <button key={cat.id} onClick={() => addCostItem(cat.id)} className="text-xs bg-stone-100 hover:bg-amber-100 px-3 py-1.5 rounded-full mr-2 mb-2 inline-flex items-center gap-1 transition-colors">
                <Plus className="w-3 h-3" /> {cat.label}
                {stockInCat.length > 0 && <span className="ml-1 text-emerald-600">📦{stockInCat.length}</span>}
              </button>
            );
          }
          return (
            <div key={cat.id} className="border border-stone-200 rounded-xl p-3 mb-2">
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium text-amber-700">{cat.label}</span>
                <span className="text-sm font-mono">{subtotal.toFixed(2)} ฿</span>
              </div>
              {cat.id === 'commission' && (
                <div className="text-[11px] text-amber-700 bg-amber-50 rounded-lg px-2 py-1.5 mb-2 flex items-start gap-1.5">
                  <span>🎁</span><span>ค่าแนะนำให้คนที่แนะนำลูกค้ามา — เพิ่มได้หลายคน (กด "เพิ่มรายการ") · นับเป็นต้นทุน หักจากกำไรอัตโนมัติ</span>
                </div>
              )}
              {items.map((item, i) => {
                // หมวดที่มี qty × unitPrice
                const hasQtyPrice = (cat.id === 'panel' || cat.id === 'battery' || cat.id === 'inverter');
                const isWire = cat.id === 'wire';
                const qty = Number(item.qty || 0);
                const unitPrice = Number(item.unitPrice || 0);
                
                // === สายไฟ - ม้วนใหม่ ===
                // มี: ความยาวม้วน, ราคาม้วน, ใช้กี่เมตร
                // คำนวณ: ราคา/เมตร = ราคาม้วน ÷ ยาวม้วน
                //        amount   = ใช้ × ราคา/เมตร
                //        เหลือ    = ยาวม้วน - ใช้ (เก็บเข้าสต๊อกตอนจบงาน)
                if (isWire && !item.stockId) {
                  const rollLength = Number(item.rollLength || 0);
                  const rollPrice = Number(item.rollPrice || 0);
                  const usedLength = Number(item.usedLength || 0);
                  const pricePerMeter = rollLength > 0 ? rollPrice / rollLength : 0;
                  const remaining = rollLength - usedLength;
                  
                  return (
                    <div key={i} className="border border-stone-100 rounded-lg p-2 mb-2 bg-stone-50/50">
                      <div className="flex gap-2 mb-1.5">
                        <input value={item.item} onChange={e => updateCostItem(cat.id, i, 'item', e.target.value)} className={inputCls + " flex-1"} placeholder="เช่น Yasaki THW 10mm² สีดำ" />
                        <button onClick={() => removeCostItem(cat.id, i)} className="p-2 hover:bg-red-50 rounded-lg"><Trash2 className="w-4 h-4 text-red-400" /></button>
                      </div>
                      
                      {/* บรรทัด 1: ม้วน */}
                      <div className="flex gap-1.5 items-center text-xs mb-1">
                        <span className="text-stone-500 w-12">ม้วน:</span>
                        <input 
                          type="number" 
                          value={item.rollLength || ''} 
                          onChange={e => {
                            const newRollLength = Number(e.target.value);
                            const newPricePerM = newRollLength > 0 ? rollPrice / newRollLength : 0;
                            const newAmount = usedLength * newPricePerM;
                            const newItems = [...(costsByCategory[cat.id] || [])];
                            newItems[i] = { ...newItems[i], rollLength: newRollLength, amount: newAmount };
                            setCostsByCategory({...costsByCategory, [cat.id]: newItems});
                          }}
                          className={inputCls + " w-16 text-center"} 
                          placeholder="100"
                        />
                        <span className="text-stone-500 whitespace-nowrap">เมตร</span>
                        <span className="text-stone-400">×</span>
                        <input 
                          type="number" 
                          step="0.01"
                          value={item.rollPrice || ''} 
                          onChange={e => {
                            const newRollPrice = Number(e.target.value);
                            const newPricePerM = rollLength > 0 ? newRollPrice / rollLength : 0;
                            const newAmount = usedLength * newPricePerM;
                            const newItems = [...(costsByCategory[cat.id] || [])];
                            newItems[i] = { ...newItems[i], rollPrice: newRollPrice, amount: newAmount };
                            setCostsByCategory({...costsByCategory, [cat.id]: newItems});
                          }}
                          className={inputCls + " w-24 text-center"} 
                          placeholder="9,500"
                        />
                        <span className="text-stone-500 whitespace-nowrap">฿/ม้วน</span>
                        <span className="text-[10px] text-stone-400 ml-auto whitespace-nowrap">
                          ≈ {pricePerMeter.toFixed(2)} ฿/m
                        </span>
                      </div>
                      
                      {/* บรรทัด 2: ใช้ในงาน */}
                      <div className="flex gap-1.5 items-center text-xs">
                        <span className="text-stone-500 w-12">ใช้:</span>
                        <input 
                          type="number" 
                          step="0.1"
                          value={item.usedLength || ''} 
                          onChange={e => {
                            const newUsed = Number(e.target.value);
                            const newAmount = newUsed * pricePerMeter;
                            const newItems = [...(costsByCategory[cat.id] || [])];
                            newItems[i] = { ...newItems[i], usedLength: newUsed, amount: newAmount };
                            setCostsByCategory({...costsByCategory, [cat.id]: newItems});
                          }}
                          className={inputCls + " w-16 text-center"} 
                          placeholder="45"
                        />
                        <span className="text-stone-500 whitespace-nowrap">เมตร</span>
                        <span className="text-stone-400">=</span>
                        <span className="font-mono font-bold text-amber-700 text-sm flex-1 text-right">
                          {Number(item.amount || 0).toLocaleString(undefined, {maximumFractionDigits: 2})} ฿
                        </span>
                      </div>
                      
                      {/* แสดง คงเหลือ */}
                      {rollLength > 0 && usedLength > 0 && remaining >= 0 && (
                        <div className="text-[10px] text-emerald-700 mt-1 pt-1 border-t border-stone-200 flex items-center gap-1">
                          💡 เหลือ <strong>{remaining.toFixed(1)} เมตร</strong>
                          {remaining > 0 && <span className="text-stone-500">— จะบันทึกเข้าสต๊อกอัตโนมัติตอน "จบงาน"</span>}
                        </div>
                      )}
                      {rollLength > 0 && usedLength > rollLength && (
                        <div className="text-[10px] text-rose-600 mt-1 pt-1 border-t border-stone-200">
                          ⚠️ ใช้เกินม้วน! (เกิน {(usedLength - rollLength).toFixed(1)}m)
                        </div>
                      )}
                    </div>
                  );
                }
                
                if (hasQtyPrice && !item.stockId) {
                  return (
                    <div key={i} className="border border-stone-100 rounded-lg p-2 mb-2 bg-stone-50/50">
                      <div className="flex gap-2 mb-1.5">
                        <input value={item.item} onChange={e => updateCostItem(cat.id, i, 'item', e.target.value)} className={inputCls + " flex-1"} placeholder={cat.id === 'panel' ? 'เช่น Longi 640W' : cat.id === 'battery' ? 'เช่น Deye 16kWh' : 'เช่น Solis 8kW Hybrid'} />
                        <button onClick={() => removeCostItem(cat.id, i)} className="p-2 hover:bg-red-50 rounded-lg"><Trash2 className="w-4 h-4 text-red-400" /></button>
                      </div>
                      <div className="flex gap-1.5 items-center text-xs">
                        <input 
                          type="number" 
                          value={item.qty || ''} 
                          onChange={e => {
                            const newQty = Number(e.target.value);
                            const newAmount = newQty * unitPrice;
                            const newItems = [...(costsByCategory[cat.id] || [])];
                            newItems[i] = { ...newItems[i], qty: newQty, amount: newAmount };
                            setCostsByCategory({...costsByCategory, [cat.id]: newItems});
                          }}
                          className={inputCls + " w-16 text-center"} 
                          placeholder="0"
                        />
                        <span className="text-stone-500 whitespace-nowrap">{cat.id === 'panel' ? 'แผ่น' : 'ชุด'}</span>
                        <span className="text-stone-400">×</span>
                        <input 
                          type="number" 
                          step="0.01"
                          value={item.unitPrice || ''} 
                          onChange={e => {
                            const newPrice = Number(e.target.value);
                            const newAmount = qty * newPrice;
                            const newItems = [...(costsByCategory[cat.id] || [])];
                            newItems[i] = { ...newItems[i], unitPrice: newPrice, amount: newAmount };
                            setCostsByCategory({...costsByCategory, [cat.id]: newItems});
                          }}
                          className={inputCls + " w-24 text-center"} 
                          placeholder="ราคา/หน่วย"
                        />
                        <span className="text-stone-400">=</span>
                        <span className="font-mono font-bold text-amber-700 text-sm flex-1 text-right">
                          {Number(item.amount || 0).toLocaleString(undefined, {maximumFractionDigits: 2})} ฿
                        </span>
                      </div>
                    </div>
                  );
                }
                
                // แบบเดิมสำหรับหมวดอื่นๆ + รายการที่เบิกจากสต๊อก (ชื่อรายการบรรทัดบน / จำนวนเงินบรรทัดล่าง)
                return (
                  <div key={i} className={`border rounded-lg p-2 mb-2 ${item.stockId ? 'bg-emerald-50 border-emerald-100' : 'bg-stone-50/50 border-stone-100'}`}>
                    <div className="flex gap-2 mb-1.5 items-center">
                      {item.stockId && <span className="text-emerald-600 shrink-0" title="เบิกจากสต๊อก">📦</span>}
                      <input value={item.item} onChange={e => updateCostItem(cat.id, i, 'item', e.target.value)} className={inputCls + " flex-1"} placeholder={cat.id === 'commission' ? 'ชื่อคนแนะนำ / ผู้รับคอม' : (cat.id === 'labor' ? 'เช่น ค่าแรงช่าง...' : cat.id === 'equipment' ? 'เช่น ท่อไฟ, อุปกรณ์ติดตั้ง...' : 'ชื่อรายการ')} disabled={!!item.stockId} />
                      <button onClick={() => removeCostItem(cat.id, i)} className="p-2 hover:bg-red-50 rounded-lg shrink-0"><Trash2 className="w-4 h-4 text-red-400" /></button>
                    </div>
                    <div className="flex gap-1.5 items-center text-xs">
                      <span className="text-stone-500 whitespace-nowrap">จำนวนเงิน:</span>
                      <input type="number" step="0.01" value={item.amount} onChange={e => updateCostItem(cat.id, i, 'amount', Number(e.target.value))} className={inputCls + " flex-1 text-right"} placeholder="0" disabled={!!item.stockId} />
                      <span className="text-stone-500">฿</span>
                    </div>
                  </div>
                );
              })}
              <div className="flex gap-2 flex-wrap">
                <button onClick={() => addCostItem(cat.id)} className="text-xs text-amber-600 font-medium flex items-center gap-1 hover:bg-amber-50 px-2 py-1 rounded">
                  <Plus className="w-3 h-3" /> เพิ่มรายการ
                </button>
                {stockInCat.length > 0 && (
                  <button onClick={() => setStockPicker({ catId: cat.id, mode: 'pick' })} className="text-xs text-emerald-600 font-medium flex items-center gap-1 hover:bg-emerald-50 px-2 py-1 rounded">
                    📦 เบิกจากสต๊อก ({stockInCat.length})
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Stock Picker Modal */}
      {stockPicker && (
        <div className="fixed inset-0 bg-black/60 z-[60] flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-md max-h-[80vh] overflow-hidden flex flex-col" onClick={e => e.stopPropagation()}>
            <div className="p-4 border-b border-stone-200 flex items-center justify-between">
              <div>
                <h3 className="display-font text-lg text-stone-800">📦 เบิกจากสต๊อก</h3>
                <p className="text-xs text-stone-500">{getCatLabel(stockPicker.catId)}</p>
              </div>
              <button onClick={() => setStockPicker(null)} className="p-1 hover:bg-stone-100 rounded-lg"><X className="w-5 h-5" /></button>
            </div>
            <div className="overflow-y-auto p-4 flex-1">
              {stockPicker.mode === 'pick' && (
                <div className="space-y-2">
                  {stock.filter(s => s.category === stockPicker.catId && Number(s.qty) > 0).map(s => {
                    const usedAlready = stockMovements[s.id] || 0;
                    const available = Number(s.qty) - usedAlready;
                    return (
                      <button key={s.id} 
                        onClick={() => available > 0 && setStockPicker({ ...stockPicker, mode: 'qty', stockItem: s, available })}
                        disabled={available <= 0}
                        className={`w-full text-left p-3 rounded-xl border transition-colors ${available > 0 ? 'border-stone-200 hover:border-emerald-400 hover:bg-emerald-50' : 'border-stone-100 opacity-50 cursor-not-allowed'}`}>
                        <div className="font-medium text-stone-800">{s.name}</div>
                        <div className="text-xs text-stone-500 mt-1 flex justify-between">
                          <span>{s.unitCost.toFixed(2)} ฿/{s.unit || 'ชิ้น'}</span>
                          <span className={available > 0 ? 'text-emerald-600 font-medium' : 'text-stone-400'}>
                            เหลือ {available.toFixed(s.category === 'wire' ? 1 : 0)} {s.unit || 'ชิ้น'}
                            {usedAlready > 0 && <span className="text-amber-600"> (เบิกแล้ว {usedAlready})</span>}
                          </span>
                        </div>
                      </button>
                    );
                  })}
                </div>
              )}
              {stockPicker.mode === 'qty' && stockPicker.stockItem && (
                <div>
                  <div className="bg-stone-50 rounded-xl p-3 mb-3">
                    <div className="font-medium">{stockPicker.stockItem.name}</div>
                    <div className="text-xs text-stone-500 mt-1">
                      ราคา: {stockPicker.stockItem.unitCost.toFixed(2)} ฿/{stockPicker.stockItem.unit || 'ชิ้น'} ·
                      เหลือ {stockPicker.available.toFixed(stockPicker.stockItem.category === 'wire' ? 1 : 0)} {stockPicker.stockItem.unit || 'ชิ้น'}
                    </div>
                  </div>
                  <Field label={`จำนวนที่เบิก (${stockPicker.stockItem.unit || 'ชิ้น'})`}>
                    <input type="number" step="0.1" autoFocus value={pickQty}
                      onChange={e => setPickQty(e.target.value)}
                      max={stockPicker.available}
                      className={inputCls} placeholder={`สูงสุด ${stockPicker.available}`} />
                  </Field>
                  {Number(pickQty) > 0 && (
                    <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-3 mb-3">
                      <div className="flex justify-between text-sm">
                        <span>คำนวณราคา:</span>
                        <span className="font-bold text-emerald-700">
                          {(Number(pickQty) * stockPicker.stockItem.unitCost).toFixed(2)} ฿
                        </span>
                      </div>
                      <div className="text-xs text-stone-500 mt-1">
                        {pickQty} × {stockPicker.stockItem.unitCost.toFixed(2)}
                      </div>
                    </div>
                  )}
                  <div className="flex gap-2">
                    <button onClick={() => setStockPicker({ ...stockPicker, mode: 'pick' })}
                      className="flex-1 py-2 border border-stone-300 rounded-xl text-stone-600">
                      ← กลับ
                    </button>
                    <button 
                      onClick={() => {
                        if (Number(pickQty) > 0 && Number(pickQty) <= stockPicker.available) {
                          addCostFromStock(stockPicker.catId, stockPicker.stockItem, Number(pickQty));
                        }
                      }}
                      disabled={!(Number(pickQty) > 0 && Number(pickQty) <= stockPicker.available)}
                      className="flex-1 py-2 bg-emerald-500 hover:bg-emerald-600 disabled:bg-stone-300 text-white rounded-xl font-medium">
                      เบิก
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      <div className="bg-gradient-to-br from-amber-50 to-orange-50 border border-amber-200 rounded-xl p-3 mb-3">
        <div className="flex justify-between text-sm mb-1">
          <span>ยอดขาย:</span>
          <span className="font-bold">{new Intl.NumberFormat('th-TH').format(form.salePrice)} ฿</span>
        </div>
        <div className="flex justify-between text-sm mb-1">
          <span>ต้นทุนรวม:</span>
          <span className="font-bold text-rose-600">{totalCost.toFixed(2)} ฿</span>
        </div>
        <div className="flex justify-between text-base pt-1 border-t border-amber-300">
          <span className="font-bold">กำไร:</span>
          <span className="font-bold text-amber-700">{(Number(form.salePrice || 0) - totalCost).toFixed(2)} ฿</span>
        </div>
      </div>

      {/* === 📋 บันทึกงาน + บริการหลังการขาย === */}
      <details className="bg-sky-50 border-2 border-sky-200 rounded-2xl p-3 mb-3" open={serviceLog.length > 0}>
        <summary className="cursor-pointer font-bold text-sm text-sky-900 flex items-center justify-between">
          <span>📋 บันทึกงาน + บริการหลังการขาย {serviceLog.length > 0 && `(${serviceLog.length})`}</span>
          {(() => {
            const svcNet = serviceLog.reduce((s, l) => s + Number(l.income || 0) - Number(l.cost || 0), 0);
            return svcNet !== 0 ? (
              <span className={`text-xs font-mono ${svcNet >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
                บริการสุทธิ {svcNet >= 0 ? '+' : ''}{svcNet.toLocaleString()} ฿
              </span>
            ) : null;
          })()}
        </summary>
        <div className="mt-2 space-y-2">
          {serviceLog.length > 0 && (
            <div className="space-y-1.5 max-h-48 overflow-y-auto pr-1">
              {[...serviceLog].sort((a, b) => (b.date || '').localeCompare(a.date || '')).map((l) => {
                const t = SVC_TYPES.find(x => x.id === l.type) || SVC_TYPES[5];
                const origIdx = serviceLog.indexOf(l);
                return (
                  <div key={origIdx} className="bg-white rounded-lg p-2 text-xs flex items-start gap-2 border border-sky-100">
                    <span className="text-base flex-shrink-0">{t.icon}</span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-1.5 flex-wrap">
                        <span className="font-medium">{t.label}</span>
                        <span className="text-stone-400">{l.date}</span>
                        {l.by && <span className="text-stone-400">· {l.by}</span>}
                      </div>
                      <div className="text-stone-600 mt-0.5">{l.note}</div>
                      {(Number(l.income) > 0 || Number(l.cost) > 0) && (
                        <div className="mt-0.5 flex gap-2 font-mono">
                          {Number(l.income) > 0 && <span className="text-emerald-600">+{Number(l.income).toLocaleString()}</span>}
                          {Number(l.cost) > 0 && <span className="text-rose-600">−{Number(l.cost).toLocaleString()}</span>}
                          {l._txCreated && <span className="text-[10px] text-stone-400">(บันทึกการเงินแล้ว)</span>}
                        </div>
                      )}
                    </div>
                    {!l._txCreated && (
                      <button type="button" onClick={() => setServiceLog(serviceLog.filter((_, i) => i !== origIdx))}
                        className="text-stone-300 hover:text-red-400 px-1">✕</button>
                    )}
                  </div>
                );
              })}
            </div>
          )}
          <div className="bg-white rounded-xl p-2.5 border border-sky-200 space-y-2">
            <div className="flex gap-1.5 flex-wrap">
              {SVC_TYPES.map(t => (
                <button key={t.id} type="button" onClick={() => setSvc({ ...svc, type: t.id })}
                  className={`text-xs px-2 py-1 rounded-lg border ${svc.type === t.id ? 'bg-sky-500 text-white border-sky-600' : 'bg-stone-50 border-stone-200'}`}>
                  {t.icon} {t.label}
                </button>
              ))}
            </div>
            <div className="grid grid-cols-3 gap-1.5">
              <input type="date" value={svc.date} onChange={e => setSvc({ ...svc, date: e.target.value })} className="text-xs border border-stone-200 rounded-lg px-2 py-1.5" />
              <input type="number" value={svc.income} onChange={e => setSvc({ ...svc, income: e.target.value })} className="text-xs border border-stone-200 rounded-lg px-2 py-1.5" placeholder="รายรับ ฿ (ถ้ามี)" />
              <input type="number" value={svc.cost} onChange={e => setSvc({ ...svc, cost: e.target.value })} className="text-xs border border-stone-200 rounded-lg px-2 py-1.5" placeholder="ค่าใช้จ่าย ฿" />
            </div>
            <div className="flex gap-1.5">
              <input value={svc.note} onChange={e => setSvc({ ...svc, note: e.target.value })}
                className="flex-1 text-xs border border-stone-200 rounded-lg px-2 py-1.5" placeholder="รายละเอียด เช่น ล้างแผง 8 แผ่น เก็บ 1,500" />
              <button type="button"
                onClick={() => {
                  if (!svc.note.trim()) { alert('กรุณาใส่รายละเอียด'); return; }
                  setServiceLog([...serviceLog, { ...svc, income: Number(svc.income) || 0, cost: Number(svc.cost) || 0 }]);
                  setSvc({ date: new Date().toISOString().split('T')[0], type: svc.type, note: '', income: '', cost: '' });
                }}
                className="text-xs bg-sky-500 hover:bg-sky-600 text-white px-3 py-1.5 rounded-lg font-medium whitespace-nowrap">+ เพิ่ม</button>
            </div>
            <div className="text-[10px] text-stone-400">💡 รายรับ/ค่าใช้จ่าย จะบันทึกเข้าการเงินอัตโนมัติตอนกดบันทึกงาน · กำไรระยะยาว = กำไรติดตั้ง + บริการสุทธิ</div>
          </div>
        </div>
      </details>

      <Field label="หมายเหตุ"><textarea value={form.note} onChange={e => update('note', e.target.value)} className={inputCls} rows={2} /></Field>
      <button onClick={handleSave} className="w-full bg-amber-500 hover:bg-amber-600 text-white py-3 rounded-xl font-medium mt-4 flex items-center justify-center gap-2">
        <Save className="w-4 h-4" /> บันทึกงาน
      </button>
    </Modal>
  );
}

function StockModal({ item, onClose, onSave }) {
  const [form, setForm] = useState(item || {
    name: '', category: 'panel', qty: 0, unitCost: 0, supplier: '', owner: 'บริษัท', note: '',
    purchaseDate: new Date().toISOString().split('T')[0],
    unit: 'ชิ้น', perRoll: 0, rollPrice: 0
  });
  const update = (f, v) => setForm({...form, [f]: v});
  const isWire = form.category === 'wire';

  const handleRollChange = (perRoll, rollPrice) => {
    const updated = { ...form, perRoll, rollPrice };
    if (Number(perRoll) > 0 && Number(rollPrice) > 0) {
      updated.unitCost = Number(rollPrice) / Number(perRoll);
    }
    setForm(updated);
  };

  return (
    <Modal title={item ? 'แก้ไขสินค้า' : 'เพิ่มสินค้า'} onClose={onClose}>
      <Field label="ชื่อสินค้า"><input value={form.name} onChange={e => update('name', e.target.value)} className={inputCls} /></Field>
      <Field label="หมวดหมู่">
        <select value={form.category} onChange={e => {
          const cat = e.target.value;
          update('category', cat);
          if (cat === 'wire' && form.unit !== 'เมตร') update('unit', 'เมตร');
        }} className={inputCls}>
          {STOCK_CATEGORIES.map(c => <option key={c.id} value={c.id}>{c.label}</option>)}
        </select>
      </Field>
      <Field label="วันที่ซื้อ"><input type="date" value={form.purchaseDate || ''} onChange={e => update('purchaseDate', e.target.value)} className={inputCls} /></Field>

      {isWire ? (
        <>
          <Field label="ซื้อเป็นม้วน" hint="กรอกข้อมูลม้วนแล้วระบบจะคำนวณราคาต่อเมตรให้">
            <div className="grid grid-cols-2 gap-2">
              <input type="number" value={form.perRoll || ''} onChange={e => handleRollChange(Number(e.target.value), form.rollPrice)} className={inputCls} placeholder="ม้วนละกี่เมตร" />
              <input type="number" value={form.rollPrice || ''} onChange={e => handleRollChange(form.perRoll, Number(e.target.value))} className={inputCls} placeholder="ราคา/ม้วน (฿)" />
            </div>
          </Field>
          <Field label="คงเหลือ (เมตร)"><input type="number" step="0.1" value={form.qty} onChange={e => update('qty', Number(e.target.value))} className={inputCls} /></Field>
          <Field label="ราคา/เมตร (คำนวณอัตโนมัติ)"><input type="number" step="0.01" value={Number(form.unitCost).toFixed(2)} onChange={e => update('unitCost', Number(e.target.value))} className={inputCls} /></Field>
        </>
      ) : (
        <>
          <Field label="หน่วย">
            <select value={form.unit || 'ชิ้น'} onChange={e => update('unit', e.target.value)} className={inputCls}>
              <option>ชิ้น</option><option>เมตร</option><option>แผ่น</option><option>เครื่อง</option><option>ลูก</option><option>ตู้</option><option>อัน</option><option>ชุด</option>
            </select>
          </Field>
          <div className="grid grid-cols-2 gap-3">
            <Field label="จำนวนคงเหลือ"><input type="number" value={form.qty} onChange={e => update('qty', Number(e.target.value))} className={inputCls} /></Field>
            <Field label="ราคา/หน่วย (฿)"><input type="number" step="0.01" value={form.unitCost} onChange={e => update('unitCost', Number(e.target.value))} className={inputCls} /></Field>
          </div>
        </>
      )}

      <Field label="Supplier"><input value={form.supplier} onChange={e => update('supplier', e.target.value)} className={inputCls} /></Field>
      <Field label="ผู้รับผิดชอบ (เจ้าของเงิน)" hint="ใครเป็นคนออกเงินซื้อ - บริษัทคือใช้กำไร/เงินทุนรวม">
        <select value={form.owner || 'บริษัท'} onChange={e => update('owner', e.target.value)} className={inputCls}>
          <option>บริษัท</option>
          <option>อาม</option>
          <option>โฟน</option>
          <option>พ่อ</option>
          <option>-</option>
        </select>
      </Field>
      <Field label="หมายเหตุ"><input value={form.note} onChange={e => update('note', e.target.value)} className={inputCls} /></Field>

      {/* Sales Catalog Section */}
      {(form.category === 'inverter' || form.category === 'panel' || form.category === 'battery') && (
        <div className="bg-gradient-to-br from-amber-50 to-orange-50 border border-amber-200 rounded-xl p-3 my-3">
          <label className="flex items-center gap-2 cursor-pointer mb-2">
            <input type="checkbox" 
              checked={form.inSalesCatalog || false} 
              onChange={e => update('inSalesCatalog', e.target.checked)}
              className="w-5 h-5 rounded text-amber-500" />
            <span className="text-sm font-bold text-amber-700">
              ⭐ ใช้ใน "เสนอขาย" (Sales Presentation)
            </span>
          </label>
          {form.inSalesCatalog && (
            <div className="space-y-2 mt-3 pl-7">
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="text-xs text-stone-600">แบรนด์</label>
                  <input type="text" value={form.salesSpecs?.brand || ''}
                    onChange={e => update('salesSpecs', {...(form.salesSpecs || {}), brand: e.target.value})}
                    placeholder="เช่น Deye, Jinko" className="w-full px-2 py-1.5 border border-stone-300 rounded-lg text-sm" />
                </div>
                <div>
                  <label className="text-xs text-stone-600">รุ่น/Model</label>
                  <input type="text" value={form.salesSpecs?.model || ''}
                    onChange={e => update('salesSpecs', {...(form.salesSpecs || {}), model: e.target.value})}
                    placeholder="เช่น Hybrid 5kW" className="w-full px-2 py-1.5 border border-stone-300 rounded-lg text-sm" />
                </div>
              </div>
              {form.category === 'inverter' && (
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="text-xs text-stone-600">ขนาด (kW)</label>
                    <input type="number" step="0.1" value={form.salesSpecs?.size || ''}
                      onChange={e => update('salesSpecs', {...(form.salesSpecs || {}), size: Number(e.target.value)})}
                      placeholder="5" className="w-full px-2 py-1.5 border border-stone-300 rounded-lg text-sm" />
                  </div>
                  <div>
                    <label className="text-xs text-stone-600">ประเภท</label>
                    <select value={form.salesSpecs?.type || 'hybrid'}
                      onChange={e => update('salesSpecs', {...(form.salesSpecs || {}), type: e.target.value})}
                      className="w-full px-2 py-1.5 border border-stone-300 rounded-lg text-sm">
                      <option value="hybrid">Hybrid</option>
                      <option value="ongrid">On-grid</option>
                      <option value="offgrid">Off-grid</option>
                    </select>
                  </div>
                </div>
              )}
              {form.category === 'panel' && (
                <div>
                  <label className="text-xs text-stone-600">กำลัง (วัตต์)</label>
                  <input type="number" value={form.salesSpecs?.watt || ''}
                    onChange={e => update('salesSpecs', {...(form.salesSpecs || {}), watt: Number(e.target.value)})}
                    placeholder="725" className="w-full px-2 py-1.5 border border-stone-300 rounded-lg text-sm" />
                </div>
              )}
              {form.category === 'battery' && (
                <div>
                  <label className="text-xs text-stone-600">ความจุ (kWh)</label>
                  <input type="number" step="0.1" value={form.salesSpecs?.capacity || ''}
                    onChange={e => update('salesSpecs', {...(form.salesSpecs || {}), capacity: Number(e.target.value)})}
                    placeholder="16" className="w-full px-2 py-1.5 border border-stone-300 rounded-lg text-sm" />
                </div>
              )}
              <div>
                <label className="text-xs text-stone-600">ระดับ (Tier)</label>
                <select value={form.salesSpecs?.tier || 'standard'}
                  onChange={e => update('salesSpecs', {...(form.salesSpecs || {}), tier: e.target.value})}
                  className="w-full px-2 py-1.5 border border-stone-300 rounded-lg text-sm">
                  <option value="standard">Standard</option>
                  <option value="premium">Premium</option>
                </select>
              </div>
            </div>
          )}
        </div>
      )}

      {/* === Auto-create Transaction (เฉพาะตอนเพิ่มใหม่) === */}
      {!item && Number(form.qty) > 0 && Number(form.unitCost) > 0 && (
        <div className="bg-gradient-to-br from-blue-50 to-cyan-50 border border-blue-200 rounded-xl p-3 my-3">
          <label className="flex items-center gap-2 cursor-pointer mb-2">
            <input type="checkbox" 
              checked={form.createTransaction !== false} 
              onChange={e => update('createTransaction', e.target.checked)}
              className="w-5 h-5 rounded text-blue-500" />
            <span className="text-sm font-bold text-blue-700">
              💰 บันทึกเป็นรายจ่าย "ต้นทุนสต๊อก"
            </span>
          </label>
          {form.createTransaction !== false && (
            <div className="pl-7 space-y-2">
              <div className="text-xs text-blue-600">
                มูลค่า <strong>{(Number(form.qty || 0) * Number(form.unitCost || 0)).toLocaleString(undefined, {maximumFractionDigits: 2})} ฿</strong> — ดึงจากเงินบริษัท
              </div>
              <div className="text-[11px] text-stone-500 bg-stone-100 p-2 rounded">
                💡 การซื้อของใช้เงินบริษัทเสมอ — ถ้าเงินไม่พอ ให้หุ้นส่วนกด <strong>"เพิ่มทุน"</strong> ที่แดชบอร์ดก่อน
              </div>
              <Field label="หมายเหตุ (ไม่บังคับ)">
                <input value={form.txNote || ''} onChange={e => update('txNote', e.target.value)} className={inputCls} placeholder="เช่น ตุนไว้ขาย / ของสำหรับงาน X" />
              </Field>
            </div>
          )}
        </div>
      )}

      <button onClick={() => {
        // โครงสร้างใหม่: ซื้อของ = เงินบริษัทเสมอ (ไม่มี partnerId)
        const txOptions = (!item && form.createTransaction !== false && Number(form.qty) > 0 && Number(form.unitCost) > 0) ? {
          createTransaction: true,
          note: form.txNote || '',
        } : null;
        // ลบ field ชั่วคราวออกก่อน save
        const {createTransaction, txPartnerId, txNote, useAdvanced, ...cleanData} = form;
        onSave(cleanData, txOptions);
      }} className="w-full bg-amber-500 hover:bg-amber-600 text-white py-3 rounded-xl font-medium mt-4 flex items-center justify-center gap-2">
        <Save className="w-4 h-4" /> บันทึก
      </button>
    </Modal>
  );
}

function PartnerModal({ partner, onClose, onSave }) {
  const [form, setForm] = useState(partner || {
    name: '', fullName: '', role: '', bankAccount: '', totalReturn: 0, note: ''
  });
  const update = (f, v) => setForm({...form, [f]: v});
  return (
    <Modal title={partner ? 'แก้ไขสมาชิก' : 'เพิ่มสมาชิก'} onClose={onClose}>
      <Field label="ชื่อเล่น"><input value={form.name} onChange={e => update('name', e.target.value)} className={inputCls} /></Field>
      <Field label="ชื่อ-นามสกุล"><input value={form.fullName} onChange={e => update('fullName', e.target.value)} className={inputCls} /></Field>
      <Field label="บทบาท"><input value={form.role} onChange={e => update('role', e.target.value)} className={inputCls} /></Field>
      <Field label="เลขบัญชีธนาคาร"><input value={form.bankAccount} onChange={e => update('bankAccount', e.target.value)} className={inputCls} /></Field>
      <Field label="ปันผลสะสม (฿)" hint="ยอดลงทุนคำนวณจากงานอัตโนมัติ ไม่ต้องกรอก"><input type="number" value={form.totalReturn} onChange={e => update('totalReturn', Number(e.target.value))} className={inputCls} /></Field>
      <Field label="หมายเหตุ"><textarea value={form.note} onChange={e => update('note', e.target.value)} className={inputCls} rows={2} /></Field>
      <button onClick={() => onSave(form)} className="w-full bg-amber-500 hover:bg-amber-600 text-white py-3 rounded-xl font-medium mt-4 flex items-center justify-center gap-2">
        <Save className="w-4 h-4" /> บันทึก
      </button>
    </Modal>
  );
}

function TransactionModal({ tx, partners, jobs, onClose, onSave }) {
  const [form, setForm] = useState(tx || {
    date: new Date().toISOString().split('T')[0],
    type: 'income', category: '', amount: 0, description: '',
    jobId: '', partnerId: ''
  });
  const update = (f, v) => setForm({...form, [f]: v});

  const incomeCategories = ['รายได้จากงาน', 'เพิ่มทุน', 'เงินกู้/ยืม', 'เงินคืน', 'อื่นๆ (รายรับ)'];
  const expenseCategories = ['ต้นทุนงาน', 'ต้นทุนสต๊อก', 'ถอนทุน', 'ปันผล', 'ค่าใช้จ่ายทั่วไป', 'จ่ายคืนเงินกู้', 'อื่นๆ (รายจ่าย)'];
  const categories = form.type === 'income' ? incomeCategories : expenseCategories;
  
  // ✨ โครงสร้างใหม่: "ผูกกับคน" เฉพาะหมวดที่เกี่ยวกับหุ้นส่วนโดยตรง
  // หมวดซื้อของ/ต้นทุน = เงินบริษัท ไม่ต้องเลือกคน
  const partnerCategories = ['เพิ่มทุน', 'ทุน', 'ถอนทุน', 'คืนทุน', 'ปันผล'];
  const needsPartner = partnerCategories.includes(form.category);

  return (
    <Modal title={tx ? 'แก้ไขรายการ' : 'เพิ่มรายการ'} onClose={onClose}>
      <Field label="วันที่"><input type="date" value={form.date} onChange={e => update('date', e.target.value)} className={inputCls} /></Field>
      
      <Field label="ประเภท">
        <div className="grid grid-cols-2 gap-2">
          <button onClick={() => update('type', 'income')}
            className={`py-2 rounded-xl font-medium transition-colors ${form.type === 'income' ? 'bg-emerald-500 text-white' : 'bg-stone-100'}`}>
            ↙ รายรับ
          </button>
          <button onClick={() => update('type', 'expense')}
            className={`py-2 rounded-xl font-medium transition-colors ${form.type === 'expense' ? 'bg-rose-500 text-white' : 'bg-stone-100'}`}>
            ↗ รายจ่าย
          </button>
        </div>
      </Field>

      <Field label="หมวดหมู่">
        <select value={form.category} onChange={e => {
          const newCat = e.target.value;
          // เปลี่ยนหมวด: ถ้าไม่ใช่หมวดทุน → เคลียร์ partnerId (เงินบริษัท)
          if (!partnerCategories.includes(newCat)) {
            setForm({...form, category: newCat, partnerId: ''});
          } else {
            setForm({...form, category: newCat});
          }
        }} className={inputCls}>
          <option value="">-- เลือกหมวด --</option>
          {categories.map(c => <option key={c}>{c}</option>)}
        </select>
      </Field>

      <Field label="จำนวนเงิน (฿)"><input type="number" step="0.01" value={form.amount} onChange={e => update('amount', Number(e.target.value))} className={inputCls} /></Field>

      <Field label="รายละเอียด"><textarea value={form.description} onChange={e => update('description', e.target.value)} className={inputCls} rows={2} placeholder="เช่น โอนทุนให้พ่อ, ค่าน้ำมันลงเสนอราคา" /></Field>

      {/* ผูกกับคน — เฉพาะหมวดทุน/ปันผล (หมวดอื่นเป็นเงินบริษัท) */}
      {needsPartner ? (
        <Field label="หุ้นส่วน (จำเป็น)" hint="หมวดนี้ต้องระบุว่าเป็นทุน/ปันผลของใคร">
          <select value={form.partnerId} onChange={e => update('partnerId', e.target.value)} className={inputCls}>
            <option value="">-- เลือกหุ้นส่วน --</option>
            {partners.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
          </select>
        </Field>
      ) : (
        form.category && (
          <div className="text-[11px] text-stone-500 bg-stone-100 p-2 rounded-lg mb-3">
            🏢 หมวดนี้ใช้เงินบริษัท — ไม่ต้องเลือกหุ้นส่วน
          </div>
        )
      )}

      <Field label="ผูกกับงาน (optional)" hint="ถ้าเป็นรายการของงานใดงานหนึ่ง">
        <select value={form.jobId} onChange={e => update('jobId', e.target.value)} className={inputCls}>
          <option value="">-- ไม่ระบุ --</option>
          {jobs.map(j => <option key={j.id} value={j.id}>{j.customer} ({j.date})</option>)}
        </select>
      </Field>

      <button onClick={() => {
        // Validation: หมวดทุนต้องเลือกหุ้นส่วน
        if (needsPartner && !form.partnerId) {
          alert(`หมวด "${form.category}" ต้องเลือกหุ้นส่วน`);
          return;
        }
        onSave(form);
      }} className="w-full bg-amber-500 hover:bg-amber-600 text-white py-3 rounded-xl font-medium mt-4 flex items-center justify-center gap-2">
        <Save className="w-4 h-4" /> บันทึก
      </button>
    </Modal>
  );
}

function CustomerModal({ customer, jobs, onClose, onSave }) {
  const [form, setForm] = useState(customer || {
    name: '', phone: '', address: '', mapLink: '',
    installDate: new Date().toISOString().split('T')[0],
    system: '', warranty: '', jobId: '', note: '',
    photos: []
  });
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState({ current: 0, total: 0 });
  const [uploadError, setUploadError] = useState('');
  const [lightboxIndex, setLightboxIndex] = useState(-1);
  const fileInputRef = useRef(null);
  const update = (f, v) => setForm({...form, [f]: v});
  
  const photos = form.photos || [];
  const remainingSlots = MAX_PHOTOS_PER_CUSTOMER - photos.length;

  const handleFileSelect = async (e) => {
    const files = Array.from(e.target.files || []);
    if (files.length === 0) return;
    
    if (files.length > remainingSlots) {
      setUploadError(`เพิ่มได้อีก ${remainingSlots} รูปเท่านั้น (สูงสุด ${MAX_PHOTOS_PER_CUSTOMER} รูป/ลูกค้า)`);
      return;
    }
    
    setUploadError('');
    setUploading(true);
    setUploadProgress({ current: 0, total: files.length });
    
    const newPhotos = [...photos];
    
    for (let i = 0; i < files.length; i++) {
      try {
        setUploadProgress({ current: i + 1, total: files.length });
        const compressed = await compressImage(files[i]);
        const result = await uploadToImgBB(compressed);
        newPhotos.push({
          url: result.url,
          thumb: result.thumb,
          medium: result.medium,
          caption: '',
          uploadedAt: new Date().toISOString(),
        });
      } catch (err) {
        console.error('Upload error:', err);
        setUploadError(`อัพรูปที่ ${i + 1} ไม่สำเร็จ: ${err.message}`);
        break;
      }
    }
    
    setForm({...form, photos: newPhotos});
    setUploading(false);
    setUploadProgress({ current: 0, total: 0 });
    if (fileInputRef.current) fileInputRef.current.value = '';
  };
  
  const removePhoto = (idx) => {
    if (!window.confirm('ลบรูปนี้?')) return;
    setForm({...form, photos: photos.filter((_, i) => i !== idx)});
  };
  
  const updateCaption = (idx, caption) => {
    setForm({...form, photos: photos.map((p, i) => i === idx ? {...p, caption} : p)});
  };

  return (
    <Modal title={customer ? 'แก้ไขลูกค้า' : 'เพิ่มลูกค้า'} onClose={onClose} wide>
      <Field label="ชื่อ-สกุล / ชื่อบริษัท">
        <input value={form.name} onChange={e => update('name', e.target.value)} className={inputCls} placeholder="พี่เกรียงศักดิ์" />
      </Field>
      <Field label="เบอร์โทร">
        <input value={form.phone} onChange={e => update('phone', e.target.value)} className={inputCls} placeholder="08x-xxx-xxxx" type="tel" />
      </Field>
      <Field label="ที่อยู่">
        <textarea value={form.address} onChange={e => update('address', e.target.value)} className={inputCls} rows={2} />
      </Field>
      <Field label="ลิงก์ Google Maps" hint="คัดลอกลิงก์จาก Google Maps มาวางได้เลย">
        <input value={form.mapLink} onChange={e => update('mapLink', e.target.value)} className={inputCls} placeholder="https://maps.google.com/..." />
      </Field>
      <Field label="วันติดตั้ง">
        <input type="date" value={form.installDate || ''} onChange={e => update('installDate', e.target.value)} className={inputCls} />
      </Field>
      <Field label="ระบบที่ติดตั้ง">
        <input value={form.system} onChange={e => update('system', e.target.value)} className={inputCls} placeholder="5kW Hybrid + แบต 16kW" />
      </Field>
      <Field label="การรับประกัน">
        <input value={form.warranty} onChange={e => update('warranty', e.target.value)} className={inputCls} placeholder="แผง 30 ปี · Inverter 10 ปี · ติดตั้ง 5 ปี" />
      </Field>
      <Field label="ผูกกับงาน (optional)">
        <select value={form.jobId} onChange={e => update('jobId', e.target.value)} className={inputCls}>
          <option value="">-- ไม่ระบุ --</option>
          {jobs.map(j => <option key={j.id} value={j.id}>{j.customer} ({j.date})</option>)}
        </select>
      </Field>
      <Field label="หมายเหตุ">
        <textarea value={form.note} onChange={e => update('note', e.target.value)} className={inputCls} rows={2} />
      </Field>

      {/* 📸 รูปผลงาน */}
      <div className="mt-5 pt-5 border-t border-stone-200">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <span className="text-2xl">📸</span>
            <h3 className="font-bold text-stone-800">รูปผลงาน</h3>
            <span className={`px-2 py-0.5 text-xs rounded-full font-medium ${photos.length >= MAX_PHOTOS_PER_CUSTOMER ? 'bg-rose-100 text-rose-700' : 'bg-stone-100 text-stone-600'}`}>
              {photos.length}/{MAX_PHOTOS_PER_CUSTOMER}
            </span>
          </div>
        </div>

        {/* Photo Grid */}
        {photos.length > 0 && (
          <div className="grid grid-cols-3 sm:grid-cols-4 gap-2 mb-3">
            {photos.map((photo, idx) => (
              <div key={idx} className="relative aspect-square group rounded-lg overflow-hidden bg-stone-100 border border-stone-200">
                <img
                  src={photo.thumb || photo.url}
                  alt={photo.caption || `รูปที่ ${idx + 1}`}
                  className="w-full h-full object-cover cursor-pointer"
                  onClick={() => setLightboxIndex(idx)}
                  loading="lazy"
                />
                <button
                  type="button"
                  onClick={() => removePhoto(idx)}
                  className="absolute top-1 right-1 bg-red-500 hover:bg-red-600 text-white rounded-full w-6 h-6 flex items-center justify-center shadow-lg transition-all opacity-90 hover:opacity-100"
                  title="ลบรูปนี้"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
                <div className="absolute bottom-0 left-0 right-0 bg-black/60 text-white text-xs px-1.5 py-0.5 truncate">
                  {photo.caption || `รูปที่ ${idx + 1}`}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Upload button */}
        {photos.length < MAX_PHOTOS_PER_CUSTOMER && (
          <div>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              multiple
              onChange={handleFileSelect}
              disabled={uploading}
              className="hidden"
              id="photo-upload-input"
            />
            <label
              htmlFor="photo-upload-input"
              className={`flex flex-col items-center justify-center w-full p-4 border-2 border-dashed rounded-xl transition-colors cursor-pointer ${
                uploading
                  ? 'bg-amber-50 border-amber-300 cursor-wait'
                  : 'bg-stone-50 border-stone-300 hover:bg-amber-50 hover:border-amber-400'
              }`}
            >
              {uploading ? (
                <>
                  <div className="w-8 h-8 border-3 border-amber-500 border-t-transparent rounded-full animate-spin mb-2" />
                  <p className="text-sm text-stone-700 font-medium">
                    กำลังอัพโหลด {uploadProgress.current}/{uploadProgress.total}...
                  </p>
                  <p className="text-xs text-stone-500 mt-1">บีบอัดและอัพโหลดอัตโนมัติ</p>
                </>
              ) : (
                <>
                  <Plus className="w-8 h-8 text-stone-400 mb-2" />
                  <p className="text-sm text-stone-700 font-medium">เลือกรูป (เลือกหลายรูปได้)</p>
                  <p className="text-xs text-stone-500 mt-1">
                    เพิ่มได้อีก {remainingSlots} รูป · บีบอัดอัตโนมัติให้พอดีโพสต์ social media
                  </p>
                </>
              )}
            </label>
          </div>
        )}

        {/* Captions */}
        {photos.length > 0 && (
          <details className="mt-3">
            <summary className="text-sm text-stone-600 cursor-pointer hover:text-amber-600 select-none">
              ✏️ ใส่คำอธิบายรูป (optional)
            </summary>
            <div className="mt-2 space-y-2">
              {photos.map((photo, idx) => (
                <div key={idx} className="flex gap-2 items-center">
                  <img src={photo.thumb || photo.url} alt="" className="w-10 h-10 object-cover rounded flex-shrink-0" />
                  <input
                    type="text"
                    value={photo.caption || ''}
                    onChange={(e) => updateCaption(idx, e.target.value)}
                    placeholder={`คำอธิบายรูปที่ ${idx + 1}`}
                    className="flex-1 px-3 py-1.5 text-sm border border-stone-300 rounded-lg focus:ring-2 focus:ring-amber-400 focus:border-transparent"
                  />
                </div>
              ))}
            </div>
          </details>
        )}

        {uploadError && (
          <div className="bg-rose-100 border border-rose-300 text-rose-700 px-3 py-2 rounded-lg text-sm flex items-center gap-2 mt-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0" /> {uploadError}
          </div>
        )}

        {photos.length > 0 && (
          <p className="text-xs text-stone-500 mt-2">
            💡 คลิกรูปเพื่อดูใหญ่ · กดกากบาทเพื่อลบ · รูปทั้งหมดเก็บใน ImgBB (ฟรี)
          </p>
        )}
      </div>

      <button
        onClick={() => onSave(form)}
        disabled={uploading}
        className="w-full bg-amber-500 hover:bg-amber-600 disabled:bg-stone-300 text-white py-3 rounded-xl font-medium mt-4 flex items-center justify-center gap-2"
      >
        <Save className="w-4 h-4" /> {uploading ? 'รออัพรูปเสร็จก่อน...' : 'บันทึก'}
      </button>

      {/* Lightbox */}
      {lightboxIndex >= 0 && photos[lightboxIndex] && (
        <PhotoLightbox
          photos={photos}
          index={lightboxIndex}
          onClose={() => setLightboxIndex(-1)}
          onChange={setLightboxIndex}
        />
      )}
    </Modal>
  );
}

function PhotoLightbox({ photos, index, onClose, onChange }) {
  const photo = photos[index];
  const total = photos.length;

  useEffect(() => {
    const handleKey = (e) => {
      if (e.key === 'Escape') onClose();
      if (e.key === 'ArrowLeft' && index > 0) onChange(index - 1);
      if (e.key === 'ArrowRight' && index < total - 1) onChange(index + 1);
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [index, total, onChange, onClose]);

  return (
    <div className="fixed inset-0 bg-black/90 z-[100] flex items-center justify-center p-4 animate-fade-in" onClick={onClose}>
      <button
        onClick={onClose}
        className="absolute top-4 right-4 bg-white/10 hover:bg-white/20 text-white rounded-full w-10 h-10 flex items-center justify-center"
      >
        <X className="w-5 h-5" />
      </button>

      {index > 0 && (
        <button
          onClick={(e) => { e.stopPropagation(); onChange(index - 1); }}
          className="absolute left-4 top-1/2 -translate-y-1/2 bg-white/10 hover:bg-white/20 text-white rounded-full w-10 h-10 flex items-center justify-center text-xl"
        >‹</button>
      )}
      {index < total - 1 && (
        <button
          onClick={(e) => { e.stopPropagation(); onChange(index + 1); }}
          className="absolute right-4 top-1/2 -translate-y-1/2 bg-white/10 hover:bg-white/20 text-white rounded-full w-10 h-10 flex items-center justify-center text-xl"
        >›</button>
      )}

      <div className="max-w-5xl w-full max-h-[90vh] flex flex-col items-center" onClick={(e) => e.stopPropagation()}>
        <img
          src={photo.url}
          alt={photo.caption || `รูปที่ ${index + 1}`}
          className="max-h-[80vh] max-w-full object-contain rounded-lg"
        />
        <div className="mt-3 text-center text-white">
          {photo.caption && <p className="text-base mb-1">{photo.caption}</p>}
          <p className="text-sm text-stone-300">{index + 1} / {total}</p>
        </div>
      </div>
    </div>
  );
}


// 💜 Modal ปันผล — ใส่ก้อนเงิน แบ่งตามสัดส่วนทุนอัตโนมัติ
// 📱 คู่มือการใช้งานสำหรับลูกค้า — พิมพ์/บันทึก PDF แนบส่งได้ (กระดาษ + อีเมล)
function CustomerGuideModal({ customerName, systemType, companyInfo, onClose }) {
  const today = new Date();
  const thMonths = ['มกราคม','กุมภาพันธ์','มีนาคม','เมษายน','พฤษภาคม','มิถุนายน','กรกฎาคม','สิงหาคม','กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม'];
  const thDate = `${today.getDate()} ${thMonths[today.getMonth()]} ${today.getFullYear() + 543}`;
  
  const Section = ({ no, icon, title, children }) => (
    <div className="mb-4 break-inside-avoid">
      <div className="flex items-center gap-2 mb-1.5 border-b-2 border-amber-400 pb-1">
        <span className="w-6 h-6 rounded-full bg-amber-500 text-white text-xs font-bold flex items-center justify-center flex-shrink-0">{no}</span>
        <span className="font-bold text-stone-800">{icon} {title}</span>
      </div>
      <div className="text-sm text-stone-700 leading-relaxed pl-8">{children}</div>
    </div>
  );

  return (
    <div className="fixed inset-0 bg-black/70 z-50 flex items-start justify-center overflow-y-auto print:bg-white print:p-0 print:overflow-visible py-6 px-2">
      {/* Toolbar (ไม่พิมพ์) */}
      <div className="fixed top-0 left-0 right-0 bg-stone-900 text-white z-50 flex items-center justify-between gap-2 no-print print:hidden shadow-lg px-4 py-2.5">
        <span className="text-sm font-medium">📱 คู่มือลูกค้า — {customerName || '(ไม่ระบุชื่อ)'}</span>
        <div className="flex gap-2">
          <button onClick={() => window.print()} className="bg-amber-500 hover:bg-amber-400 text-stone-900 text-sm font-bold px-4 py-1.5 rounded-lg">
            🖨️ พิมพ์ / บันทึก PDF
          </button>
          <button onClick={onClose} className="bg-stone-700 hover:bg-stone-600 text-sm px-3 py-1.5 rounded-lg">✕ ปิด</button>
        </div>
      </div>

      {/* กระดาษ A4 */}
      <div className="bg-white w-full max-w-[210mm] shadow-2xl print:shadow-none mt-12 print:mt-0 p-8 print:p-6 rounded-xl print:rounded-none">
        {/* Header */}
        <div className="text-center border-b-4 border-amber-500 pb-3 mb-4">
          <div className="text-2xl font-bold text-amber-600">{companyInfo.name || 'D.D. Solution'}</div>
          {companyInfo.tagline && <div className="text-xs text-stone-500">{companyInfo.tagline}</div>}
          <div className="text-lg font-bold text-stone-800 mt-2">📱 คู่มือการใช้งานระบบโซล่าเซลล์</div>
          <div className="text-xs text-stone-500 mt-1">
            ลูกค้า: <strong className="text-stone-700">{customerName || '-'}</strong>
            {systemType && <> · ระบบ: <strong className="text-stone-700">{systemType}</strong></>}
            {' '}· วันที่ {thDate}
          </div>
        </div>

        <Section no="1" icon="📲" title="ติดตั้งแอปดูผลผลิตไฟฟ้า">
          <ul className="list-disc pl-4 space-y-0.5">
            <li>ดาวน์โหลดแอป <strong>"Deye Cloud"</strong> จาก App Store (iPhone) หรือ Play Store (Android)</li>
            <li>ทีมงานสร้างบัญชีและเชื่อมระบบให้เรียบร้อยแล้ว — เข้าสู่ระบบด้วยอีเมล/รหัสที่ทีมงานแจ้ง</li>
            <li>เปิดดูได้ทุกที่ที่มีอินเทอร์เน็ต ทั้งมือถือและแท็บเล็ต</li>
          </ul>
        </Section>

        <Section no="2" icon="📊" title="อ่านหน้าจอยังไง">
          <ul className="list-disc pl-4 space-y-0.5">
            <li><strong>ผลิตวันนี้ (kWh)</strong> — ไฟที่แผงผลิตได้วันนี้ ยิ่งแดดดียิ่งมาก</li>
            <li><strong>แผนภาพพลังงาน (Power flow)</strong> — ให้ดู<strong>ทิศทางลูกศร</strong>ว่าไฟวิ่งจากไหนไปไหน
              <span className="text-stone-500"> (ไม่ต้องสนใจเครื่องหมาย + / − ตัวเลข เพราะแต่ละรุ่นแสดงต่างกัน ลูกศรแม่นยำกว่า)</span></li>
            <li>กราฟรายวัน: เส้นโค้งสูงช่วง 10:00–15:00 = ปกติ (แดดแรงสุด)</li>
          </ul>
        </Section>

        <Section no="3" icon="✅" title="เช็คสุขภาพระบบ (สัปดาห์ละครั้ง)">
          <ul className="list-disc pl-4 space-y-0.5">
            <li>เปิดแอปดูยอด "ผลิตวันนี้" — วันแดดดีควรใกล้เคียงกันทุกสัปดาห์</li>
            <li>ถ้าผลิตตกลงเรื่อยๆ ทั้งที่แดดดี → แผงอาจสกปรก (ฝุ่น/ขี้นก ทำผลิตตก 5–15%)</li>
            <li>ช่วงหน้าฝน ฝนช่วยล้างแผงให้ฟรี — ผลิตตกเพราะเมฆเป็นเรื่องปกติ</li>
          </ul>
        </Section>

        <Section no="4" icon="⚠️" title="ปัญหาพบบ่อย — แบบไหนโทรหาเรา">
          <table className="w-full text-xs border-collapse">
            <tbody>
              <tr className="border-b border-stone-200">
                <td className="py-1 pr-2 font-medium w-1/2">แอปขึ้น "ออฟไลน์" แต่ไฟบ้านใช้ปกติ</td>
                <td className="py-1 text-stone-600">WiFi หลุด — รีสตาร์ทเราเตอร์ รอ 5 นาที ระบบยังผลิตไฟตามปกติ ไม่ต้องกังวล</td>
              </tr>
              <tr className="border-b border-stone-200">
                <td className="py-1 pr-2 font-medium">วันแดดดีแต่ผลิตเป็น 0 ทั้งวัน</td>
                <td className="py-1 text-rose-600 font-medium">📞 โทรหาเราทันที</td>
              </tr>
              <tr className="border-b border-stone-200">
                <td className="py-1 pr-2 font-medium">ไฟสถานะที่ตัวเครื่องเป็นสีแดง / มีรหัส Error</td>
                <td className="py-1 text-rose-600 font-medium">📞 ถ่ายรูปหน้าจอเครื่อง แล้วส่งให้เรา</td>
              </tr>
              <tr>
                <td className="py-1 pr-2 font-medium">อยากย้าย/เพิ่มอุปกรณ์ไฟฟ้าตัวใหญ่</td>
                <td className="py-1 text-stone-600">ปรึกษาเราก่อน เพื่อเช็คขนาดระบบ</td>
              </tr>
            </tbody>
          </table>
          <div className="mt-1.5 bg-rose-50 border border-rose-200 rounded px-2 py-1 text-xs text-rose-700 font-medium">
            🚫 ห้ามเปิดฝาเครื่อง ถอดสาย หรือซ่อมเองเด็ดขาด — อันตรายไฟฟ้าแรงสูง และทำให้ประกันสิ้นสุด
          </div>
        </Section>

        <Section no="5" icon="🤝" title="บริการหลังการขาย">
          <ul className="list-disc pl-4 space-y-0.5">
            <li><strong>ล้างแผง</strong> แนะนำปีละ 1–2 ครั้ง (โดยเฉพาะปลายหน้าแล้ง) — นัดทีมงานเราได้เลย</li>
            <li><strong>รับประกัน</strong> ตามใบรับประกันที่ได้รับ — เก็บคู่กับเอกสารชุดนี้</li>
            <li>มีคำถาม สงสัยตัวเลขในแอป ทักมาได้เสมอ ยินดีตอบทุกเรื่อง</li>
          </ul>
        </Section>

        {/* ติดต่อ */}
        <div className="mt-4 bg-amber-50 border-2 border-amber-300 rounded-xl p-3 text-center break-inside-avoid">
          <div className="font-bold text-stone-800 mb-1">📞 ติดต่อ {companyInfo.name || 'D.D. Solution'}</div>
          <div className="text-sm text-stone-700 flex flex-wrap justify-center gap-x-4 gap-y-0.5">
            {companyInfo.phone && <span>โทร: <strong>{companyInfo.phone}</strong></span>}
            {companyInfo.lineId && <span>LINE: <strong>{companyInfo.lineId}</strong></span>}
            {companyInfo.email && <span>อีเมล: <strong>{companyInfo.email}</strong></span>}
            {!companyInfo.phone && !companyInfo.lineId && !companyInfo.email && <span className="text-stone-400 text-xs">(ตั้งค่าเบอร์/LINE ได้ที่ ข้อมูลบริษัท ใน Tab งานเอกสาร)</span>}
          </div>
          <div className="text-xs text-stone-500 mt-1.5">ขอบคุณที่ไว้วางใจให้เราดูแลระบบโซล่าเซลล์ของคุณ ☀️</div>
        </div>
      </div>
    </div>
  );
}

function DividendModal({ partners, actualInvestments, retainedProfit, cashOnHand, fmt, onClose, onSave }) {
  const [amount, setAmount] = useState('');
  const [note, setNote] = useState('');
  
  const totalCapital = Object.values(actualInvestments.inv).reduce((s, v) => s + v, 0);
  const amt = Number(amount) || 0;
  
  // แบ่งตาม % ทุน — ปัดเป็นสตางค์ เศษให้คนถือหุ้นมากสุด (รวมพอดีก้อนเสมอ)
  const allocations = useMemo(() => {
    if (amt <= 0 || totalCapital <= 0) return [];
    const list = partners
      .map(p => ({ partnerId: p.id, name: p.name, capital: actualInvestments.inv[p.id] || 0 }))
      .filter(p => p.capital > 0)
      .map(p => ({
        ...p,
        pct: (p.capital / totalCapital) * 100,
        amount: Math.round((amt * p.capital / totalCapital) * 100) / 100,
      }));
    // ปรับเศษให้รวม = ก้อนพอดี
    const sumAlloc = list.reduce((s, a) => s + a.amount, 0);
    const diff = Math.round((amt - sumAlloc) * 100) / 100;
    if (Math.abs(diff) >= 0.01 && list.length > 0) {
      const biggest = list.reduce((m, a) => a.capital > m.capital ? a : m, list[0]);
      biggest.amount = Math.round((biggest.amount + diff) * 100) / 100;
    }
    return list;
  }, [amt, totalCapital, partners, actualInvestments]);
  
  const overProfit = amt > retainedProfit + 0.5;
  const overCash = amt > cashOnHand + 0.5;
  
  return (
    <Modal title="💜 ปันผลกำไร" onClose={onClose}>
      {/* สถานะเงิน */}
      <div className="bg-violet-50 border border-violet-200 rounded-xl p-3 mb-3 text-sm space-y-1">
        <div className="flex justify-between"><span className="text-stone-600">กำไรสะสมคงเหลือ (ปันผลได้)</span><span className="font-bold text-violet-700">{fmt(retainedProfit)} ฿</span></div>
        <div className="flex justify-between"><span className="text-stone-600">เงินสดในมือ</span><span className="font-mono text-stone-700">{fmt(cashOnHand)} ฿</span></div>
      </div>
      
      <Field label="ยอดปันผลรวม (฿)" hint="ใส่เป็นก้อน ระบบแบ่งให้ตามสัดส่วนทุน">
        <input type="number" step="0.01" value={amount} onChange={e => setAmount(e.target.value)}
          className={inputCls} placeholder="เช่น 30000" autoFocus />
      </Field>
      
      {/* Validation */}
      {amt > 0 && overCash && (
        <div className="bg-rose-50 border border-rose-200 rounded-lg p-2 text-xs text-rose-700 mb-2">
          ⛔ เกินเงินสดในมือ ({fmt(cashOnHand)} ฿) — เงินไม่พอจ่ายจริง
        </div>
      )}
      {amt > 0 && !overCash && overProfit && (
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-2 text-xs text-amber-700 mb-2">
          ⚠️ เกินกำไรสะสมคงเหลือ ({fmt(retainedProfit)} ฿) — ส่วนเกินจะกินเงินทุน ไม่แนะนำ
        </div>
      )}
      
      {/* Preview แบ่งตามสัดส่วน */}
      {allocations.length > 0 && (
        <div className="bg-white border border-stone-200 rounded-xl overflow-hidden mb-3">
          <div className="bg-violet-100 px-3 py-2 text-xs font-bold text-violet-800">แบ่งตามสัดส่วนทุน</div>
          {allocations.map(a => (
            <div key={a.partnerId} className="flex items-center justify-between px-3 py-2 border-t border-stone-100 text-sm">
              <div>
                <span className="font-medium text-stone-800">{a.name}</span>
                <span className="text-xs text-stone-400 ml-2">ทุน {fmt(a.capital)} ({a.pct.toFixed(1)}%)</span>
              </div>
              <span className="font-bold text-violet-700 font-mono">{fmt(a.amount)} ฿</span>
            </div>
          ))}
          <div className="flex justify-between px-3 py-2 border-t-2 border-violet-200 bg-violet-50 text-sm font-bold">
            <span>รวม</span>
            <span className="font-mono text-violet-800">{fmt(allocations.reduce((s, a) => s + a.amount, 0))} ฿</span>
          </div>
        </div>
      )}
      
      <Field label="หมายเหตุ (ไม่บังคับ)">
        <input value={note} onChange={e => setNote(e.target.value)} className={inputCls} placeholder="เช่น ปันผลครึ่งปีแรก 2569" />
      </Field>
      
      <button
        onClick={() => {
          if (amt <= 0 || allocations.length === 0) { alert('กรุณาใส่ยอดปันผล'); return; }
          if (overCash) { alert('เงินสดในมือไม่พอจ่ายปันผล'); return; }
          if (overProfit && !window.confirm(`⚠️ ยอดปันผลเกินกำไรสะสมคงเหลือ (${fmt(retainedProfit)} ฿)\nส่วนเกินจะกินเงินทุนบริษัท\n\nยืนยันปันผลต่อ?`)) return;
          const summary = allocations.map(a => `• ${a.name}: ${fmt(a.amount)} ฿ (${a.pct.toFixed(1)}%)`).join('\n');
          if (!window.confirm(`💜 ยืนยันปันผล ${fmt(amt)} ฿\n\n${summary}\n\nระบบจะสร้างรายการ "ปันผล" ${allocations.length} รายการ`)) return;
          onSave(allocations, note);
        }}
        className="w-full bg-violet-500 hover:bg-violet-600 text-white py-3 rounded-xl font-medium mt-2 flex items-center justify-center gap-2"
      >
        💜 ปันผล {amt > 0 ? fmt(amt) + ' ฿' : ''}
      </button>
    </Modal>
  );
}

function CapitalModal({ mode, partners, actualInvestments, cashOnHand, fmt, onClose, onSave }) {
  const isDeposit = mode === 'deposit';
  const [partnerId, setPartnerId] = useState(partners[0]?.id || '');
  const [amount, setAmount] = useState('');
  const [note, setNote] = useState('');
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [error, setError] = useState('');

  const partnerInv = (id) => actualInvestments.inv[id] || 0;
  const selectedInv = partnerInv(partnerId);
  const amt = Number(amount) || 0;

  // ตรวจสอบ
  let warning = '';
  let canSave = amt > 0;
  if (!isDeposit && amt > 0) {
    if (amt > selectedInv) {
      warning = `⚠ ถอนได้สูงสุด ${fmt(selectedInv)} ฿ (ทุนของคนนี้)`;
      canSave = false;
    } else if (amt > cashOnHand) {
      warning = `⚠ เงินสดบริษัทมีแค่ ${fmt(cashOnHand)} ฿ (ของส่วนใหญ่อยู่ในสต๊อก)`;
      canSave = false;
    }
  }

  const handleSubmit = () => {
    setError('');
    if (!partnerId) { setError('กรุณาเลือกผู้ลงทุน'); return; }
    if (amt <= 0) { setError('กรุณากรอกจำนวนเงิน'); return; }
    if (!isDeposit) {
      if (amt > selectedInv) { setError(`ถอนเกินทุนของคนนี้ (สูงสุด ${fmt(selectedInv)} ฿)`); return; }
      if (amt > cashOnHand) { setError(`ถอนเกินเงินสดในมือ (เหลือ ${fmt(cashOnHand)} ฿)`); return; }
    }
    onSave({ partnerId, amount: amt, note, date });
  };

  return (
    <Modal title={isDeposit ? '➕ เพิ่มทุน' : '➖ ถอนทุน'} onClose={onClose}>
      <div className="space-y-4">
        {/* ใครเพิ่ม/ถอน */}
        <div>
          <label className="block text-sm font-medium text-stone-700 mb-2">
            {isDeposit ? 'ใครเพิ่มทุน' : 'ใครถอนทุน'}
          </label>
          <div className="grid grid-cols-3 gap-2">
            {partners.map(p => {
              const inv = partnerInv(p.id);
              const selected = partnerId === p.id;
              return (
                <button
                  key={p.id}
                  type="button"
                  onClick={() => setPartnerId(p.id)}
                  className={`p-3 rounded-xl border-2 transition-all text-center ${
                    selected
                      ? (isDeposit ? 'border-emerald-500 bg-emerald-50' : 'border-rose-500 bg-rose-50')
                      : 'border-stone-200 bg-white hover:border-stone-300'
                  }`}
                >
                  <div className="font-bold text-stone-800">{p.name}</div>
                  <div className="text-xs text-stone-500 mt-0.5">
                    {isDeposit ? 'ทุนปัจจุบัน' : 'มี'} {fmt(inv)} ฿
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* วันที่ */}
        <div>
          <label className="block text-sm font-medium text-stone-700 mb-1">วันที่</label>
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            className="w-full px-3 py-2 border border-stone-300 rounded-lg focus:ring-2 focus:ring-amber-400 focus:border-transparent"
          />
        </div>

        {/* จำนวน */}
        <div>
          <label className="block text-sm font-medium text-stone-700 mb-1">
            จำนวน (บาท)
          </label>
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            placeholder="0"
            className={`w-full px-3 py-3 border-2 rounded-lg text-2xl font-bold text-right ${
              warning
                ? 'border-rose-400 bg-rose-50 text-rose-700'
                : (isDeposit ? 'border-emerald-300 focus:border-emerald-500' : 'border-rose-300 focus:border-rose-500')
            } focus:outline-none`}
            min="0"
            step="100"
          />
          {warning && (
            <p className="text-rose-600 text-sm mt-1.5 flex items-start gap-1">
              <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
              <span>{warning}</span>
            </p>
          )}
          {!isDeposit && !warning && amt > 0 && (
            <p className="text-stone-500 text-xs mt-1.5">
              จะเหลือทุน {fmt(selectedInv - amt)} ฿ · เงินสดเหลือ {fmt(cashOnHand - amt)} ฿
            </p>
          )}
        </div>

        {/* หมายเหตุ */}
        <div>
          <label className="block text-sm font-medium text-stone-700 mb-1">
            หมายเหตุ <span className="text-stone-400 font-normal">(ไม่บังคับ)</span>
          </label>
          <input
            type="text"
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder={isDeposit ? 'เช่น เติมทุนเพื่อซื้อแผง' : 'เช่น คืนเงินกู้'}
            className="w-full px-3 py-2 border border-stone-300 rounded-lg focus:ring-2 focus:ring-amber-400 focus:border-transparent"
          />
        </div>

        {/* Error */}
        {error && (
          <div className="bg-rose-100 border border-rose-300 text-rose-700 px-3 py-2 rounded-lg text-sm flex items-center gap-2">
            <AlertCircle className="w-4 h-4" /> {error}
          </div>
        )}

        {/* Buttons */}
        <div className="flex gap-2 pt-2">
          <button
            onClick={onClose}
            className="flex-1 px-4 py-3 bg-stone-100 hover:bg-stone-200 text-stone-700 rounded-xl font-medium transition-colors"
          >
            ยกเลิก
          </button>
          <button
            onClick={handleSubmit}
            disabled={!canSave}
            className={`flex-1 px-4 py-3 text-white rounded-xl font-medium transition-colors flex items-center justify-center gap-1.5 ${
              canSave
                ? (isDeposit ? 'bg-emerald-500 hover:bg-emerald-600' : 'bg-rose-500 hover:bg-rose-600')
                : 'bg-stone-300 cursor-not-allowed'
            }`}
          >
            <Save className="w-4 h-4" />
            {isDeposit ? 'เพิ่มทุน' : 'ถอนทุน'}
          </button>
        </div>
      </div>
    </Modal>
  );
}

// ============== SALES CATALOG MANAGER (แคตตาล็อกขาย) ==============
function SalesCatalogManager({ catalog, stock, companyInfo, onSaveCatalog, onSaveCompany }) {
  const [editing, setEditing] = useState(null); // null | 'new' | item
  const [filterCat, setFilterCat] = useState('all');
  
  // Helpers: หาสต็อกที่ตรงกับ catalog item
  const getStockMatch = (item) => {
    return (stock || []).filter(s => 
      s.qty > 0 && s.salesSpecs &&
      s.salesSpecs.brand === item.brand && 
      s.salesSpecs.model === item.model
    );
  };
  
  const filteredCatalog = catalog.filter(c => filterCat === 'all' || c.category === filterCat);
  
  const handleAdd = () => setEditing('new');
  const handleEdit = (item) => setEditing(item);
  const handleDelete = (item) => {
    if (!window.confirm(`ลบ "${item.brand} ${item.model}" ออกจากแคตตาล็อก?`)) return;
    onSaveCatalog(catalog.filter(c => c.id !== item.id), 'delete', `ลบ: ${item.brand} ${item.model}`);
  };
  const handleSave = (data) => {
    if (editing === 'new') {
      const newItem = { ...data, id: `sc-${Date.now()}` };
      onSaveCatalog([...catalog, newItem], 'add', `เพิ่ม: ${data.brand} ${data.model}`);
    } else {
      onSaveCatalog(catalog.map(c => c.id === editing.id ? { ...editing, ...data } : c), 'edit', `แก้ไข: ${data.brand} ${data.model}`);
    }
    setEditing(null);
  };
  const handleToggleActive = (item) => {
    onSaveCatalog(catalog.map(c => c.id === item.id ? { ...c, active: !c.active } : c), 'edit', `${item.active ? 'หยุดขาย' : 'เปิดขาย'}: ${item.brand} ${item.model}`);
  };
  
  return (
    <div className="space-y-4 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="display-font text-3xl text-stone-800">💰 แคตตาล็อกขาย</h2>
          <p className="text-sm text-stone-500">รายการสินค้าและราคาตลาดสำหรับเสนอลูกค้า</p>
        </div>
        <button onClick={handleAdd} className="flex items-center gap-2 bg-amber-500 hover:bg-amber-600 text-white px-4 py-2 rounded-xl font-medium shadow-sm">
          <Plus className="w-4 h-4" /> เพิ่ม
        </button>
      </div>

      {/* Margin Section */}
      <div className="bg-white rounded-2xl p-4 shadow-sm border border-stone-200">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-bold text-stone-800">💰 Margin (กำไรที่บวก)</h3>
        </div>
        
        <div className="grid grid-cols-3 gap-3">
          <div>
            <label className="text-xs text-stone-600 block mb-1">เล็ก (&lt;5kW)</label>
            <div className="flex items-center gap-1">
              <input type="number" value={companyInfo?.margins?.small ?? 25}
                onChange={e => onSaveCompany({...companyInfo, margins: {...(companyInfo?.margins || {}), small: Number(e.target.value) || 0}}, 'edit', `ปรับ margin เล็ก: ${e.target.value}%`)}
                className="w-full px-2 py-1.5 border border-stone-300 rounded-lg text-sm text-right" />
              <span className="text-stone-600 text-sm">%</span>
            </div>
          </div>
          <div>
            <label className="text-xs text-stone-600 block mb-1">กลาง (5-10kW)</label>
            <div className="flex items-center gap-1">
              <input type="number" value={companyInfo?.margins?.medium ?? 20}
                onChange={e => onSaveCompany({...companyInfo, margins: {...(companyInfo?.margins || {}), medium: Number(e.target.value) || 0}}, 'edit', `ปรับ margin กลาง: ${e.target.value}%`)}
                className="w-full px-2 py-1.5 border border-stone-300 rounded-lg text-sm text-right" />
              <span className="text-stone-600 text-sm">%</span>
            </div>
          </div>
          <div>
            <label className="text-xs text-stone-600 block mb-1">ใหญ่ (&gt;10kW)</label>
            <div className="flex items-center gap-1">
              <input type="number" value={companyInfo?.margins?.large ?? 15}
                onChange={e => onSaveCompany({...companyInfo, margins: {...(companyInfo?.margins || {}), large: Number(e.target.value) || 0}}, 'edit', `ปรับ margin ใหญ่: ${e.target.value}%`)}
                className="w-full px-2 py-1.5 border border-stone-300 rounded-lg text-sm text-right" />
              <span className="text-stone-600 text-sm">%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Hidden Costs Section */}
      <div className="bg-white rounded-2xl p-4 shadow-sm border-2 border-blue-200">
        <div className="flex items-center justify-between mb-3">
          <div>
            <h3 className="font-bold text-stone-800">🔧 ต้นทุนแฝงต่องานติดตั้ง</h3>
            <p className="text-xs text-stone-500">ค่าใช้จ่ายที่เกิดทุกงาน นอกเหนือจาก Inverter/แผง/แบต</p>
          </div>
          <button onClick={() => {
            const newItem = { id: `hc-${Date.now()}`, label: 'รายการใหม่', amount: 0, perJob: true };
            onSaveCompany({...companyInfo, hiddenCosts: [...(companyInfo?.hiddenCosts || []), newItem]}, 'add', 'เพิ่มต้นทุนแฝง');
          }} className="text-blue-600 hover:bg-blue-50 px-2 py-1 rounded-lg text-sm font-medium">
            + เพิ่ม
          </button>
        </div>
        
        <div className="space-y-2">
          {(companyInfo?.hiddenCosts || []).map((item, idx) => (
            <div key={item.id} className="flex items-center gap-2 bg-stone-50 rounded-lg p-2">
              <input type="checkbox" 
                checked={item.perJob !== false}
                onChange={e => {
                  const newCosts = [...companyInfo.hiddenCosts];
                  newCosts[idx] = {...item, perJob: e.target.checked};
                  onSaveCompany({...companyInfo, hiddenCosts: newCosts}, 'edit', `${e.target.checked ? 'เปิด' : 'ปิด'}: ${item.label}`);
                }}
                className="w-4 h-4 rounded text-blue-500" />
              <input type="text" value={item.label}
                onChange={e => {
                  const newCosts = [...companyInfo.hiddenCosts];
                  newCosts[idx] = {...item, label: e.target.value};
                  onSaveCompany({...companyInfo, hiddenCosts: newCosts}, null);
                }}
                className="flex-1 min-w-0 px-2 py-1 bg-transparent border-0 text-sm focus:bg-white focus:border focus:border-stone-300 rounded" />
              <div className="flex items-center gap-1">
                <input type="number" value={item.amount}
                  onChange={e => {
                    const newCosts = [...companyInfo.hiddenCosts];
                    newCosts[idx] = {...item, amount: Number(e.target.value) || 0};
                    onSaveCompany({...companyInfo, hiddenCosts: newCosts}, null);
                  }}
                  className="w-24 px-2 py-1 border border-stone-300 rounded-lg text-sm text-right" />
                <span className="text-stone-600 text-xs">฿</span>
              </div>
              <button onClick={() => {
                if (!window.confirm(`ลบ "${item.label}"?`)) return;
                onSaveCompany({...companyInfo, hiddenCosts: companyInfo.hiddenCosts.filter(c => c.id !== item.id)}, 'delete', `ลบ: ${item.label}`);
              }} className="p-1 hover:bg-rose-50 rounded">
                <Trash2 className="w-4 h-4 text-rose-500" />
              </button>
            </div>
          ))}
        </div>
        
        <div className="mt-3 pt-3 border-t border-stone-200 flex items-center justify-between">
          <span className="text-sm font-medium text-stone-700">💰 รวมต้นทุนแฝง/งาน</span>
          <span className="text-lg font-bold text-blue-700">{sumHiddenCosts(companyInfo).toLocaleString()} ฿</span>
        </div>
        <p className="text-xs text-stone-500 mt-2">
          💡 ระบบจะคิดต้นทุนแฝงนี้เพิ่มเข้าไปใน <strong>ทุกงาน</strong> นอกเหนือจากค่าอุปกรณ์
        </p>
      </div>

      {/* Stock note */}
      <div className="bg-amber-50 border border-amber-200 rounded-xl p-3 text-xs text-stone-600">
        💡 <strong>การใช้สต็อก:</strong> ระบบจะใช้<strong>ของในสต็อก</strong>ก่อน (ราคาทุนเดิม) → ที่เหลือใช้<strong>ราคาตลาด</strong> (ซื้อใหม่)
      </div>

      {/* Filter tabs */}
      <div className="flex gap-2 overflow-x-auto">
        {[
          { id: 'all', label: 'ทั้งหมด' },
          { id: 'inverter', label: '🔌 Inverter' },
          { id: 'panel', label: '☀️ แผง' },
          { id: 'battery', label: '🔋 แบต' },
          { id: 'wire', label: '🪢 สายไฟ' },
        ].map(f => (
          <button key={f.id} onClick={() => setFilterCat(f.id)}
            className={`px-3 py-1.5 rounded-full text-sm whitespace-nowrap ${filterCat === f.id ? 'bg-amber-500 text-white' : 'bg-stone-200 text-stone-600'}`}>
            {f.label}
          </button>
        ))}
      </div>

      {/* Catalog list */}
      <div className="space-y-2">
        {filteredCatalog.length === 0 ? (
          <div className="bg-white rounded-2xl p-6 text-center text-stone-500 border border-stone-200">
            ไม่มีสินค้า — กด ➕ เพื่อเพิ่ม
          </div>
        ) : filteredCatalog.map(item => {
          const stockMatch = getStockMatch(item);
          const stockTotal = stockMatch.reduce((sum, s) => sum + s.qty, 0);
          const stockUnitCost = stockMatch.length > 0 ? stockMatch[0].unitCost : null;
          const catIcon = item.category === 'inverter' ? '🔌' : item.category === 'panel' ? '☀️' : item.category === 'battery' ? '🔋' : '🪢';
          
          return (
            <div key={item.id} className={`bg-white rounded-2xl p-3 shadow-sm border-2 ${item.active === false ? 'border-stone-200 opacity-60' : 'border-amber-200'}`}>
              <div className="flex items-start justify-between gap-2">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="text-xl">{catIcon}</span>
                    <h3 className="font-bold text-stone-800">{item.brand} {item.model}</h3>
                    {item.active === false && <span className="text-xs bg-stone-200 text-stone-600 px-2 py-0.5 rounded-full">หยุดขาย</span>}
                  </div>
                  <div className="text-xs text-stone-500 mt-1">
                    {item.category === 'inverter' && `${item.size}kW · ${item.type}`}
                    {item.category === 'panel' && `${item.watt}W ต่อแผ่น`}
                    {item.category === 'battery' && `${item.capacity}kWh`}
                    {item.category === 'wire' && `${item.watt}mm² · ${item.wireType === 'pv' ? 'PV (DC)' : 'AC (เมน)'} · ${item.unit || 'm'}${item.forInvSize ? ` · ใช้กับ ${item.forInvSize}kW` : ''}`}
                  </div>
                  <div className="grid grid-cols-2 gap-2 mt-2">
                    <div className="bg-amber-50 rounded-lg p-2">
                      <div className="text-xs text-stone-500">ราคาตลาด {item.category === 'wire' ? `/${item.unit || 'm'}` : ''}</div>
                      <div className="font-bold text-amber-700">{item.marketPrice.toLocaleString()} ฿</div>
                    </div>
                    <div className={`rounded-lg p-2 ${stockTotal > 0 ? 'bg-emerald-50' : 'bg-stone-50'}`}>
                      <div className="text-xs text-stone-500">ในสต็อก</div>
                      {stockTotal > 0 ? (
                        <div>
                          <div className="font-bold text-emerald-700">{stockTotal} ชิ้น</div>
                          <div className="text-xs text-stone-500">@ {stockUnitCost?.toLocaleString()} ฿</div>
                        </div>
                      ) : (
                        <div className="text-stone-400">หมด</div>
                      )}
                    </div>
                  </div>
                </div>
                <div className="flex flex-col gap-1">
                  <button onClick={() => handleEdit(item)} className="p-2 hover:bg-stone-100 rounded-lg" title="แก้ไข">
                    <Edit2 className="w-4 h-4 text-stone-500" />
                  </button>
                  <button onClick={() => handleToggleActive(item)} className="p-2 hover:bg-stone-100 rounded-lg" title={item.active === false ? 'เปิดขาย' : 'หยุดขาย'}>
                    {item.active === false ? <Eye className="w-4 h-4 text-stone-500" /> : <EyeOff className="w-4 h-4 text-stone-500" />}
                  </button>
                  <button onClick={() => handleDelete(item)} className="p-2 hover:bg-stone-100 rounded-lg" title="ลบ">
                    <Trash2 className="w-4 h-4 text-rose-500" />
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {editing && (
        <CatalogItemModal item={editing === 'new' ? null : editing} onClose={() => setEditing(null)} onSave={handleSave} />
      )}
    </div>
  );
}

// ============== CATALOG ITEM MODAL ==============
function CatalogItemModal({ item, onClose, onSave }) {
  const [form, setForm] = useState(item || {
    category: 'panel', brand: '', model: '', marketPrice: 0,
    tier: 'standard', active: true,
    watt: 0, size: 0, capacity: 0, type: 'hybrid',
    unit: 'piece', wireType: 'ac', forInvSize: '',
  });
  const update = (f, v) => setForm({...form, [f]: v});
  const isInverter = form.category === 'inverter';
  const isPanel = form.category === 'panel';
  const isBattery = form.category === 'battery';
  const isWire = form.category === 'wire';
  
  const canSave = form.brand && form.model && form.marketPrice > 0 && 
    ((isInverter && form.size > 0) || 
     (isPanel && form.watt > 0) || 
     (isBattery && form.capacity > 0) ||
     (isWire && form.watt > 0));
  
  return (
    <Modal title={item ? 'แก้ไขสินค้า' : 'เพิ่มสินค้า'} onClose={onClose}>
      <Field label="ประเภท">
        <select value={form.category} onChange={e => update('category', e.target.value)} className={inputCls}>
          <option value="inverter">🔌 Inverter</option>
          <option value="panel">☀️ แผงโซล่าเซลล์</option>
          <option value="battery">🔋 แบตเตอรี่</option>
          <option value="wire">🪢 สายไฟ</option>
        </select>
      </Field>
      <div className="grid grid-cols-2 gap-3">
        <Field label="แบรนด์"><input value={form.brand} onChange={e => update('brand', e.target.value)} placeholder="Deye / Jinko / Yasaki" className={inputCls} /></Field>
        <Field label="รุ่น/Model"><input value={form.model} onChange={e => update('model', e.target.value)} placeholder="Hybrid 5kW / THW 10mm² ดำ" className={inputCls} /></Field>
      </div>
      
      {isInverter && (
        <div className="grid grid-cols-2 gap-3">
          <Field label="ขนาด (kW)"><input type="number" step="0.1" value={form.size || ''} onChange={e => update('size', Number(e.target.value))} className={inputCls} /></Field>
          <Field label="ประเภท">
            <select value={form.type || 'hybrid'} onChange={e => update('type', e.target.value)} className={inputCls}>
              <option value="hybrid">Hybrid</option>
              <option value="ongrid">On-grid</option>
              <option value="offgrid">Off-grid</option>
            </select>
          </Field>
        </div>
      )}
      {isPanel && (
        <Field label="กำลัง (วัตต์)"><input type="number" value={form.watt || ''} onChange={e => update('watt', Number(e.target.value))} placeholder="725" className={inputCls} /></Field>
      )}
      {isBattery && (
        <Field label="ความจุ (kWh)"><input type="number" step="0.1" value={form.capacity || ''} onChange={e => update('capacity', Number(e.target.value))} placeholder="16" className={inputCls} /></Field>
      )}
      {isWire && (
        <>
          <div className="grid grid-cols-2 gap-3">
            <Field label="ขนาด (mm²)" hint="6=PV, 10=AC 5kW, 16=AC 10kW">
              <input type="number" value={form.watt || ''} onChange={e => update('watt', Number(e.target.value))} placeholder="6 / 10 / 16" className={inputCls} />
            </Field>
            <Field label="ประเภทสาย">
              <select value={form.wireType || 'ac'} onChange={e => update('wireType', e.target.value)} className={inputCls}>
                <option value="pv">PV (DC)</option>
                <option value="ac">AC (เมน)</option>
              </select>
            </Field>
          </div>
          <Field label="ใช้กับ Inverter ขนาด" hint="ว่างเปล่า=ทุกขนาด, '<=5'=≤5kW, '>5'=>5kW">
            <input value={form.forInvSize || ''} onChange={e => update('forInvSize', e.target.value)} placeholder="<=5  หรือ  >5" className={inputCls} />
          </Field>
          <Field label="หน่วย">
            <select value={form.unit || 'm'} onChange={e => update('unit', e.target.value)} className={inputCls}>
              <option value="m">เมตร (m)</option>
              <option value="roll">ม้วน (roll)</option>
              <option value="piece">เส้น (piece)</option>
            </select>
          </Field>
        </>
      )}
      
      <Field label={isWire ? `ราคาต่อ${form.unit === 'm' ? 'เมตร' : form.unit === 'roll' ? 'ม้วน' : 'เส้น'} (฿)` : 'ราคาตลาด (฿)'} hint="ราคาที่ซื้อจากตลาดวันนี้ — ใช้เมื่อสต็อกหมด">
        <input type="number" value={form.marketPrice || ''} onChange={e => update('marketPrice', Number(e.target.value))} className={inputCls} />
      </Field>
      
      <Field label="ระดับ (Tier)">
        <select value={form.tier || 'standard'} onChange={e => update('tier', e.target.value)} className={inputCls}>
          <option value="standard">Standard</option>
          <option value="premium">Premium</option>
        </select>
      </Field>
      
      <label className="flex items-center gap-2 cursor-pointer mt-2">
        <input type="checkbox" checked={form.active !== false} onChange={e => update('active', e.target.checked)} className="w-5 h-5 rounded text-amber-500" />
        <span className="text-sm">เปิดขาย (แสดงให้ลูกค้าเลือก)</span>
      </label>
      
      <button onClick={() => onSave(form)} disabled={!canSave}
        className="w-full bg-amber-500 hover:bg-amber-600 disabled:bg-stone-300 text-white py-3 rounded-xl font-medium mt-4 flex items-center justify-center gap-2">
        <Save className="w-4 h-4" /> บันทึก
      </button>
    </Modal>
  );
}

// ============== QUICK COST CALC (⚡ คิดราคาไว) ==============
// สูตรถอดจากต้นทุนงานจริง (งาน 1 เกรียงศักดิ์ + งาน 2 หลักสี่)
// ใส่ 5 ช่อง → ราคาต่ำสุดไม่เข้าเนื้อ + ราคาเปิดเผื่อต่อรอง + โซนปิดแนะนำ
const QUICKCALC_DEFAULTS = {
  wireRate: 150,    // ค่าสาย PV คู่ + ท่อ ต่อเมตร
  acFixed: 3000,    // เหมาสาย AC + กราวด์ ต่องาน
  overhead: 10000,  // ตู้ Combiner + ช่างเสริม + เดินทาง + ข้าว + เบ็ดเตล็ด (จากงาน 2 = 9,652)
  warrantyPct: 3,   // กันเคลมประกัน % ของทุน
  openMk: 35,       // ราคาเปิด = ทุน × 1.35
  closeMk: 20,      // โซนปิดแนะนำเริ่มที่ ทุน × 1.20 (งาน 2 ปิดจริงที่ ×1.21)
};

function QuickCostCalc() {
  const [expanded, setExpanded] = useState(false);
  const [panel, setPanel] = useState('');
  const [inv, setInv] = useState('');
  const [batt, setBatt] = useState('');
  const [dist, setDist] = useState('');
  const [labor, setLabor] = useState('');
  const [showSettings, setShowSettings] = useState(false);
  const [showDetail, setShowDetail] = useState(false);
  const [cfg, setCfg] = useState(() => {
    try { return { ...QUICKCALC_DEFAULTS, ...JSON.parse(localStorage.getItem('dd-quickcalc') || '{}') }; }
    catch (e) { return { ...QUICKCALC_DEFAULTS }; }
  });
  const setCfgVal = (k, v) => {
    const next = { ...cfg, [k]: parseFloat(v) || 0 };
    setCfg(next);
    try { localStorage.setItem('dd-quickcalc', JSON.stringify(next)); } catch (e) {}
  };

  const n = (v) => parseFloat(v) || 0;
  const upK = (x) => Math.ceil(x / 1000) * 1000;
  const fmt = (x) => '฿' + Math.round(x).toLocaleString('th-TH');

  const wire = n(dist) * cfg.wireRate + cfg.acFixed;
  const cost = n(panel) + n(inv) + n(batt) + wire + n(labor) + cfg.overhead;
  const hasInput = n(panel) > 0 || n(inv) > 0;
  const floorPrice = upK(cost * (1 + cfg.warrantyPct / 100));
  const openPrice = roundUpTo999(cost * (1 + cfg.openMk / 100));
  const closeLo = upK(cost * (1 + cfg.closeMk / 100));
  const closeHi = upK(cost * (1 + cfg.closeMk / 100 + 0.05));

  const fields = [
    { label: '1. ราคาแผงรวม', value: panel, set: setPanel, unit: '฿', ph: 'เช่น 26,199' },
    { label: '2. Inverter', value: inv, set: setInv, unit: '฿', ph: 'เช่น 33,705' },
    { label: '3. แบต (ไม่มี = ว่าง)', value: batt, set: setBatt, unit: '฿', ph: '0' },
    { label: '4. ระยะแผง → ตู้', value: dist, set: setDist, unit: 'ม.', ph: 'เช่น 30' },
    { label: '5. ค่าเหมาติดตั้งแผง', value: labor, set: setLabor, unit: '฿', ph: 'เช่น 20,000' },
  ];
  const settings = [
    { key: 'wireRate', label: 'ค่าสาย/เมตร (PV คู่+ท่อ)' },
    { key: 'acFixed', label: 'เหมาสาย AC+กราวด์' },
    { key: 'overhead', label: 'Overhead ต่องาน' },
    { key: 'warrantyPct', label: 'กันเคลม %' },
    { key: 'openMk', label: 'ราคาเปิด markup %' },
    { key: 'closeMk', label: 'โซนปิด markup %' },
  ];

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-amber-200 overflow-hidden">
      <button onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between p-4 hover:bg-amber-50 transition-colors">
        <div className="flex items-center gap-2 text-left">
          <span className="text-xl">⚡</span>
          <div>
            <div className="font-bold text-stone-800 text-sm">คิดราคาไว</div>
            <div className="text-xs text-stone-500">ใส่ 5 ช่อง → ราคาต่ำสุดไม่เข้าเนื้อ + ราคาเปิด</div>
          </div>
        </div>
        <span className={`text-stone-400 transition-transform ${expanded ? 'rotate-180' : ''}`}>▾</span>
      </button>

      {expanded && (
        <div className="p-4 pt-0 space-y-3 animate-fade-in">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {fields.map((f, i) => (
              <div key={i} className={i === 4 ? 'sm:col-span-2' : ''}>
                <label className="text-xs font-semibold text-stone-500">{f.label}</label>
                <div className="relative mt-0.5">
                  <input type="number" inputMode="decimal" value={f.value} placeholder={f.ph}
                    onChange={(e) => f.set(e.target.value)}
                    className="w-full p-2.5 pr-10 border border-stone-300 rounded-xl text-lg font-bold focus:border-amber-500 focus:outline-none" />
                  <span className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-stone-400 font-semibold">{f.unit}</span>
                </div>
              </div>
            ))}
          </div>

          {hasInput && (
            <div className="space-y-2">
              <div className="grid grid-cols-2 gap-2">
                <div className="bg-emerald-50 border border-emerald-300 rounded-xl p-3">
                  <div className="text-[11px] font-bold text-emerald-700">🟢 ต่ำสุดไม่เข้าเนื้อ</div>
                  <div className="text-xl font-extrabold text-emerald-700">{fmt(floorPrice)}</div>
                  <div className="text-[10px] text-emerald-600">รวมกันเคลม {cfg.warrantyPct}% แล้ว</div>
                </div>
                <div className="bg-amber-50 border border-amber-300 rounded-xl p-3">
                  <div className="text-[11px] font-bold text-amber-700">🟠 ราคาเปิด (เผื่อต่อรอง)</div>
                  <div className="text-xl font-extrabold text-amber-700">{fmt(openPrice)}</div>
                  <div className="text-[10px] text-amber-600">กำไร {fmt(openPrice - cost)}</div>
                </div>
              </div>
              <div className="bg-sky-50 border border-sky-200 rounded-xl p-2.5 text-center text-sm">
                🎯 <span className="text-sky-700 font-bold">โซนปิดที่ดี: {fmt(closeLo)} – {fmt(closeHi)}</span>
                <span className="text-sky-600 text-xs"> (กำไร {fmt(closeLo - cost)}+)</span>
              </div>

              <button onClick={() => setShowDetail(!showDetail)}
                className="text-xs text-stone-500 underline">📋 {showDetail ? 'ซ่อน' : 'ดู'}ที่มาต้นทุน (ทุนรวม {fmt(cost)})</button>
              {showDetail && (
                <div className="bg-stone-50 rounded-xl p-3 text-xs space-y-1">
                  {[
                    ['แผง', n(panel)], ['Inverter', n(inv)], ['แบต', n(batt)],
                    [`สายไฟ+ท่อ (${n(dist)} ม. × ${cfg.wireRate} + AC ${cfg.acFixed.toLocaleString()})`, wire],
                    ['ค่าเหมาติดตั้งแผง', n(labor)], ['Overhead ต่องาน', cfg.overhead],
                  ].filter(([, v]) => v > 0).map(([k, v], i) => (
                    <div key={i} className="flex justify-between"><span className="text-stone-500">{k}</span><span className="font-bold">{fmt(v)}</span></div>
                  ))}
                  <div className="flex justify-between border-t border-stone-300 pt-1 text-amber-700 font-extrabold">
                    <span>ทุนรวม</span><span>{fmt(cost)}</span>
                  </div>
                  <div className="flex justify-between"><span className="text-stone-500">+ กันเคลม {cfg.warrantyPct}%</span><span className="font-bold">{fmt(cost * cfg.warrantyPct / 100)}</span></div>
                </div>
              )}
            </div>
          )}

          <button onClick={() => setShowSettings(!showSettings)}
            className="text-xs text-stone-400 underline">⚙️ {showSettings ? 'ซ่อน' : ''}ตั้งค่าสูตร</button>
          {showSettings && (
            <div className="grid grid-cols-2 gap-2 bg-stone-50 rounded-xl p-3">
              {settings.map((s) => (
                <div key={s.key}>
                  <label className="text-[10px] text-stone-500">{s.label}</label>
                  <input type="number" inputMode="decimal" value={cfg[s.key]}
                    onChange={(e) => setCfgVal(s.key, e.target.value)}
                    className="w-full p-1.5 border border-stone-300 rounded-lg text-sm font-bold focus:border-amber-500 focus:outline-none" />
                </div>
              ))}
              <div className="col-span-2 text-[10px] text-stone-400 leading-relaxed">
                ค่าเริ่มต้นถอดจากงานจริง: overhead งานหลักสี่ = 9,652฿ · งานหลักสี่ปิดที่ทุน ×1.21 (อยู่ในโซนแนะนำ) · ถ้าค่าเหมารวมสายแล้ว ใส่ระยะ = 0
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ============== SALES PRESENTATION (เสนอขาย) ==============
function SalesPresentation({ customers, stock, catalog, companyInfo, onCreateQuotation, onSaveCustomer, onSaveCompany }) {
  const [step, setStep] = useState(1);
  
  // Customer info
  const [customerMode, setCustomerMode] = useState('new');
  const [selectedCustomerId, setSelectedCustomerId] = useState('');
  const [customerName, setCustomerName] = useState('');
  const [customerPhone, setCustomerPhone] = useState('');
  const [customerAddress, setCustomerAddress] = useState('');
  
  // Usage info
  const [monthlyBill, setMonthlyBill] = useState(5000);
  const [usagePeriod, setUsagePeriod] = useState('mixed');
  const [region, setRegion] = useState('central');
  const [hasBattery, setHasBattery] = useState(false);
  
  // Electricity meter
  const [meterType, setMeterType] = useState('normal'); // 'normal' | 'tou'
  const normalRate = PRICING_CONFIG.electricityRate;
  const touOnPeak = PRICING_CONFIG.touOnPeak;
  const touOffPeak = PRICING_CONFIG.touOffPeak;
  const inflationRate = PRICING_CONFIG.electricityInflation;
  
  // Selection
  const [selectedPackage, setSelectedPackage] = useState(null);
  const [isCustom, setIsCustom] = useState(false);
  
  // Custom builder
  const [customInverter, setCustomInverter] = useState(null);
  const [customPanel, setCustomPanel] = useState(null);
  const [customPanelCount, setCustomPanelCount] = useState(0);
  const [customBattery, setCustomBattery] = useState(null);
  
  // Helper: build calc options
  const calcOpts = {
    region,
    meterType,
    electricityRate: normalRate,
    touRates: { onPeak: touOnPeak, offPeak: touOffPeak },
    inflation: inflationRate,
  };
  
  // Calculate packages
  const packages = recommendPackages({ monthlyBill, hasBattery, region, meterType, stock, catalog, companyInfo });
  
  // Get the active selection (package or custom)
  const getActiveSelection = () => {
    if (isCustom) {
      const inv = customInverter;
      const pan = customPanel;
      const cnt = customPanelCount;
      const bat = customBattery;
      if (!inv || !pan || cnt < 1) return null;
      
      // Smart cost (stock first → market)
      const invCost = calcSmartCost(inv, 1, stock);
      const panCost = calcSmartCost(pan, cnt, stock);
      const batCost = bat ? calcSmartCost(bat, 1, stock) : { cost: 0, fromStock: 0, fromMarket: 0, breakdown: [], total: 0 };
      const equipmentCost = invCost.cost + panCost.cost + batCost.cost;
      const installCost = sumHiddenCosts(companyInfo, inv.size); // ต้นทุนแฝงต่องาน (ตามขนาด)
      const grandCost = equipmentCost + installCost;
      const margin = getMargin(inv.size, companyInfo);
      const sellPriceRaw = applyMargin(grandCost, margin);
      const sellPrice = roundUpTo999(sellPriceRaw); // 🎯 ปัดขึ้น 999
      const totalKW = (pan.watt * cnt) / 1000;
      const roi = calculateROI({ kW: Math.min(totalKW, inv.size), ...calcOpts, mode: 'dream' });
      const breakEven = sellPrice / roi.yearlySavings;
      
      return {
        label: 'Custom',
        badge: '⚙️',
        inverter: inv, panel: pan, panelCount: cnt, battery: bat,
        costBreakdown: { invCost, panCost, batCost },
        equipmentCost, installCost,
        totalCost: grandCost, sellPrice, margin,
        profit: sellPrice - grandCost,
        totalKW: Math.round(totalKW * 100) / 100,
        roi,
        breakEven: Math.round(breakEven * 10) / 10,
      };
    }
    return selectedPackage;
  };
  
  const active = getActiveSelection();
  
  // ถ้าไม่มี equipment ใน stock ให้แจ้งเตือน
  if (!packages || packages === null) {
    return (
      <div className="bg-white rounded-2xl p-6 border border-amber-200 text-center space-y-3">
        <div className="text-4xl">⚠️</div>
        <h2 className="display-font text-2xl text-stone-800">ยังไม่มีอุปกรณ์ในแคตตาล็อก</h2>
        <p className="text-sm text-stone-600">
          ต้องเพิ่มสินค้าใน <strong>"สต็อก"</strong> และติ๊ก <strong>"ใช้สำหรับเสนอขาย"</strong> ก่อน
          <br />
          (ต้องมี <strong>Inverter</strong> และ <strong>แผงโซล่าเซลล์</strong> อย่างน้อย 1 รายการ)
        </p>
      </div>
    );
  }
  
  // ============ STEP 1: Customer Info ============
  if (step === 1) {
    return (
      <div className="space-y-4 animate-fade-in">
        <div>
          <h2 className="display-font text-3xl text-stone-800">🎤 เสนอขายโซล่าเซลล์</h2>
          <p className="text-sm text-stone-500">ขั้นที่ 1/4 — ข้อมูลลูกค้า</p>
        </div>
        
        <div className="flex gap-2">
          {[1,2,3,4].map(s => (
            <div key={s} className={`flex-1 h-1.5 rounded-full ${s <= step ? 'bg-amber-500' : 'bg-stone-200'}`} />
          ))}
        </div>

        <div className="bg-white rounded-2xl p-4 shadow-sm border border-stone-200 space-y-3">
          <h3 className="font-bold text-stone-800">👤 ลูกค้า</h3>
          <div className="grid grid-cols-2 gap-2">
            <button onClick={() => setCustomerMode('new')}
              className={`p-3 rounded-xl border-2 text-sm font-medium ${customerMode === 'new' ? 'border-amber-500 bg-amber-50 text-amber-700' : 'border-stone-200'}`}>
              ➕ ลูกค้าใหม่
            </button>
            <button onClick={() => setCustomerMode('existing')}
              className={`p-3 rounded-xl border-2 text-sm font-medium ${customerMode === 'existing' ? 'border-amber-500 bg-amber-50 text-amber-700' : 'border-stone-200'}`}>
              📋 ลูกค้าเก่า
            </button>
          </div>
          
          {customerMode === 'existing' ? (
            <select value={selectedCustomerId} onChange={e => {
              const c = customers.find(x => x.id === e.target.value);
              setSelectedCustomerId(e.target.value);
              if (c) {
                setCustomerName(c.name || '');
                setCustomerPhone(c.phone || '');
                setCustomerAddress(c.address || '');
              }
            }} className="w-full px-3 py-2 border border-stone-300 rounded-xl">
              <option value="">-- เลือกลูกค้า --</option>
              {customers.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
            </select>
          ) : (
            <>
              <input value={customerName} onChange={e => setCustomerName(e.target.value)}
                placeholder="ชื่อลูกค้า" className="w-full px-3 py-2 border border-stone-300 rounded-xl" />
              <input value={customerPhone} onChange={e => setCustomerPhone(e.target.value)}
                placeholder="เบอร์โทร" className="w-full px-3 py-2 border border-stone-300 rounded-xl" />
              <textarea value={customerAddress} onChange={e => setCustomerAddress(e.target.value)}
                placeholder="ที่อยู่" rows={2} className="w-full px-3 py-2 border border-stone-300 rounded-xl" />
            </>
          )}
        </div>

        <div className="bg-white rounded-2xl p-4 shadow-sm border border-stone-200 space-y-3">
          <h3 className="font-bold text-stone-800">💡 ข้อมูลการใช้ไฟ</h3>
          
          <div>
            <label className="block text-sm text-stone-600 mb-1">ค่าไฟเฉลี่ยต่อเดือน</label>
            <div className="flex items-center gap-2">
              <input type="number" value={monthlyBill}
                onChange={e => setMonthlyBill(Number(e.target.value) || 0)}
                className="flex-1 px-3 py-2 border border-stone-300 rounded-xl text-lg font-bold text-right" />
              <span className="font-medium text-stone-700">฿/เดือน</span>
            </div>
            <div className="text-xs text-stone-500 mt-1">
              ≈ {Math.round(monthlyBill / normalRate)} kWh/เดือน
            </div>
          </div>
          
          <div>
            <label className="block text-sm text-stone-600 mb-2">⏰ ใช้ไฟช่วงไหนมากที่สุด?</label>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              {[
                { id: 'day', label: '☀️ กลางวัน' },
                { id: 'evening', label: '🌆 เย็น-ค่ำ' },
                { id: 'night', label: '🌙 กลางคืน' },
                { id: 'mixed', label: '🔄 ทุกเวลา' },
              ].map(p => (
                <button key={p.id} onClick={() => {
                  setUsagePeriod(p.id);
                  if (p.id === 'day') setHasBattery(false);
                  else if (p.id === 'night' || p.id === 'evening') setHasBattery(true);
                }}
                  className={`p-2 rounded-xl border-2 text-xs font-medium ${usagePeriod === p.id ? 'border-amber-500 bg-amber-50 text-amber-700' : 'border-stone-200'}`}>
                  {p.label}
                </button>
              ))}
            </div>
          </div>
          
          <div>
            <label className="block text-sm text-stone-600 mb-2">📍 ภูมิภาค</label>
            <div className="grid grid-cols-2 gap-2">
              {Object.entries(SOLAR_REGIONS).map(([k, v]) => (
                <button key={k} onClick={() => setRegion(k)}
                  className={`p-2 rounded-xl border-2 text-xs ${region === k ? 'border-amber-500 bg-amber-50' : 'border-stone-200'}`}>
                  <div className="font-medium">{v.label}</div>
                  <div className="text-stone-500">{v.hours} ชม./วัน</div>
                </button>
              ))}
            </div>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-xl p-3">
            <label className="flex items-start gap-2 cursor-pointer">
              <input type="checkbox" checked={hasBattery} onChange={e => setHasBattery(e.target.checked)}
                className="w-5 h-5 rounded text-amber-500 mt-0.5 flex-shrink-0" />
              <span className="text-sm">
                <strong>🔋 อยากมีแบตเตอรี่</strong>
                <span className="block text-xs text-stone-500 mt-0.5">
                  เก็บประจุจากกลางวัน มาใช้งานกลางคืน เหมาะกับคนใช้งานกลางคืนเป็นหลัก, ไม่ปล่อยไฟย้อน
                </span>
              </span>
            </label>
          </div>
        </div>

        {/* Electricity Meter Type */}
        <div className="bg-white rounded-2xl p-4 shadow-sm border border-stone-200 space-y-3">
          <h3 className="font-bold text-stone-800">⚡ ประเภทมิเตอร์ไฟ</h3>
          <div className="grid grid-cols-2 gap-2">
            <button onClick={() => setMeterType('normal')}
              className={`p-3 rounded-xl border-2 text-left ${meterType === 'normal' ? 'border-amber-500 bg-amber-50' : 'border-stone-200'}`}>
              <div className="font-medium text-sm">🏠 มิเตอร์ปกติ</div>
              <div className="text-xs text-stone-500">{normalRate} ฿/หน่วย</div>
            </button>
            <button onClick={() => setMeterType('tou')}
              className={`p-3 rounded-xl border-2 text-left ${meterType === 'tou' ? 'border-amber-500 bg-amber-50' : 'border-stone-200'}`}>
              <div className="font-medium text-sm">⏰ TOU</div>
              <div className="text-xs text-stone-500">{touOnPeak}/{touOffPeak} ฿</div>
            </button>
          </div>
          
          {meterType === 'tou' && (
            <div className="bg-amber-50 border border-amber-200 rounded-xl p-3">
              <div className="text-xs text-amber-700 font-medium mb-1">⏰ Solar เหมาะกับ TOU มาก!</div>
              <div className="text-xs text-stone-600">
                • On-peak (จ-ศ 9:00-22:00): <strong>{touOnPeak} ฿/หน่วย</strong><br/>
                • Off-peak (อื่นๆ + ส-อา): <strong>{touOffPeak} ฿/หน่วย</strong><br/>
                • Solar ผลิตช่วงกลางวัน → ประหยัดอัตราแพง!
              </div>
            </div>
          )}
        </div>

        <button onClick={() => setStep(2)}
          disabled={!customerName || monthlyBill < 100}
          className="w-full bg-amber-500 hover:bg-amber-600 disabled:bg-stone-300 text-white py-3 rounded-xl font-medium">
          ถัดไป → ดูแพ็คเกจที่แนะนำ
        </button>
      </div>
    );
  }
  
  // ============ STEP 2: Package Recommendation ============
  if (step === 2) {
    return (
      <div className="space-y-4 animate-fade-in">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="display-font text-3xl text-stone-800">🎁 แพ็คเกจแนะนำ</h2>
            <p className="text-sm text-stone-500">ขั้นที่ 2/4 — สำหรับ {customerName}</p>
          </div>
          <button onClick={() => setStep(1)} className="text-sm text-stone-600 hover:text-stone-800">← กลับ</button>
        </div>
        
        <div className="flex gap-2">
          {[1,2,3,4].map(s => (
            <div key={s} className={`flex-1 h-1.5 rounded-full ${s <= step ? 'bg-amber-500' : 'bg-stone-200'}`} />
          ))}
        </div>

        <div className="space-y-3">
          {Object.entries(packages).map(([key, pkg]) => {
            const isBest = key === 'best';
            // คำนวณใหม่ด้วย calcOpts (รวม TOU) + dream mode (default แสดง)
            const realRoi = calculateROI({ kW: Math.min(pkg.totalKW, pkg.inverter.size), ...calcOpts, mode: 'dream' });
            const realBreakEven = pkg.sellPrice / realRoi.yearlySavings;
            
            return (
              <div key={key} className={`bg-white rounded-2xl shadow-sm border-2 overflow-hidden ${
                isBest ? 'border-amber-400' : 'border-stone-200'
              }`}>
                {isBest && (
                  <div className="bg-amber-400 text-white text-xs font-bold py-1 px-3 text-center">
                    ⭐ แนะนำที่สุด - คืนทุนเร็วสุด
                  </div>
                )}
                <div className="p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-2xl">{pkg.badge}</span>
                    <h3 className="font-bold text-lg text-stone-800">{pkg.label}</h3>
                  </div>
                  
                  <div className="space-y-1 text-sm text-stone-600 mb-3">
                    <div>🔌 {pkg.inverter.brand} {pkg.inverter.model}</div>
                    <div>☀️ {pkg.panel.brand} {pkg.panel.model} × {pkg.panelCount} แผ่น = {pkg.totalKW} kW</div>
                    <div>{pkg.battery ? `🔋 ${pkg.battery.brand} ${pkg.battery.model}` : '❌ ไม่มีแบตเตอรี่'}</div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-2 mb-3">
                    <div className="bg-amber-50 rounded-lg p-2 text-center">
                      <div className="text-xs text-stone-500">ราคา</div>
                      <div className="font-bold text-amber-700">{pkg.sellPrice.toLocaleString()} ฿</div>
                    </div>
                    <div className="bg-emerald-50 rounded-lg p-2 text-center">
                      <div className="text-xs text-stone-500">คืนทุน</div>
                      <div className="font-bold text-emerald-700">{realBreakEven.toFixed(1)} ปี</div>
                    </div>
                  </div>
                  
                  <button onClick={() => {
                    // อัพเดท ROI ของ package ด้วย calcOpts ปัจจุบัน
                    setSelectedPackage({ ...pkg, roi: realRoi, breakEven: Math.round(realBreakEven * 10) / 10 });
                    setIsCustom(false);
                    setStep(4);
                  }} className={`w-full py-2 rounded-xl font-medium text-sm ${
                    isBest ? 'bg-amber-500 hover:bg-amber-600 text-white' : 'bg-stone-100 hover:bg-stone-200 text-stone-700'
                  }`}>
                    เลือกแพ็คนี้ →
                  </button>
                </div>
              </div>
            );
          })}
        </div>

        <button onClick={() => {
          setIsCustom(true);
          setCustomInverter(packages.best.inverter);
          setCustomPanel(packages.best.panel);
          setCustomPanelCount(packages.best.panelCount);
          setCustomBattery(packages.best.battery);
          setStep(3);
        }} className="w-full p-4 bg-stone-100 hover:bg-stone-200 border-2 border-dashed border-stone-300 rounded-2xl text-stone-700 font-medium">
          ⚙️ ปรับแต่งเอง (Custom)
        </button>
      </div>
    );
  }
  
  // ============ STEP 3: Custom Builder ============
  if (step === 3) {
    // ดึง equipment จาก catalog (เฉพาะ active)
    const activeCatalog = (catalog || []).filter(c => c.active !== false);
    const inverters = activeCatalog.filter(c => c.category === 'inverter');
    const panels = activeCatalog.filter(c => c.category === 'panel');
    const batteries = activeCatalog.filter(c => c.category === 'battery');
    
    return (
      <div className="space-y-4 animate-fade-in">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="display-font text-3xl text-stone-800">⚙️ ปรับแต่งระบบ</h2>
            <p className="text-sm text-stone-500">ขั้นที่ 3/4 — เลือกอุปกรณ์เอง</p>
          </div>
          <button onClick={() => setStep(2)} className="text-sm text-stone-600 hover:text-stone-800">← กลับ</button>
        </div>
        
        <div className="flex gap-2">
          {[1,2,3,4].map(s => (
            <div key={s} className={`flex-1 h-1.5 rounded-full ${s <= step ? 'bg-amber-500' : 'bg-stone-200'}`} />
          ))}
        </div>

        <div className="bg-white rounded-2xl p-4 shadow-sm border border-stone-200">
          <h3 className="font-bold text-stone-800 mb-3">🔌 Inverter ({inverters.length} รุ่น)</h3>
          <div className="space-y-2">
            {inverters.map(inv => (
              <button key={inv.id} onClick={() => setCustomInverter(inv)}
                className={`w-full p-3 rounded-xl border-2 text-left ${
                  customInverter?.id === inv.id ? 'border-amber-500 bg-amber-50' : 'border-stone-200'
                }`}>
                <div className="font-medium">{inv.brand} {inv.model}</div>
                <div className="text-xs text-stone-500">ขนาด {inv.size}kW · {inv.type}</div>
              </button>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-2xl p-4 shadow-sm border border-stone-200">
          <h3 className="font-bold text-stone-800 mb-3">☀️ แผงโซล่าเซลล์ ({panels.length} รุ่น)</h3>
          <div className="space-y-2 mb-3">
            {panels.map(p => (
              <button key={p.id} onClick={() => {
                setCustomPanel(p);
                if (customInverter) {
                  setCustomPanelCount(Math.ceil(customInverter.size * 1100 / p.watt));
                }
              }}
                className={`w-full p-3 rounded-xl border-2 text-left ${
                  customPanel?.id === p.id ? 'border-amber-500 bg-amber-50' : 'border-stone-200'
                }`}>
                <div className="font-medium">{p.brand} {p.model}</div>
                <div className="text-xs text-stone-500">{p.watt}W ต่อแผ่น</div>
              </button>
            ))}
          </div>
          {customPanel && (
            <div className="bg-stone-50 rounded-xl p-3">
              <label className="block text-sm text-stone-600 mb-2">จำนวนแผ่น</label>
              <div className="flex items-center justify-center gap-3">
                <button onClick={() => setCustomPanelCount(Math.max(1, customPanelCount - 1))}
                  className="w-10 h-10 bg-stone-200 hover:bg-stone-300 rounded-full font-bold text-xl">−</button>
                <div className="text-center">
                  <div className="text-3xl font-bold text-amber-600">{customPanelCount}</div>
                  <div className="text-xs text-stone-500">= {((customPanel.watt * customPanelCount) / 1000).toFixed(2)} kW</div>
                </div>
                <button onClick={() => setCustomPanelCount(customPanelCount + 1)}
                  className="w-10 h-10 bg-stone-200 hover:bg-stone-300 rounded-full font-bold text-xl">+</button>
              </div>
              {customInverter && (
                <div className="text-xs text-center text-stone-500 mt-2">
                  💡 แนะนำ {Math.ceil(customInverter.size * 1100 / customPanel.watt)} แผ่น สำหรับ {customInverter.size}kW
                </div>
              )}
            </div>
          )}
        </div>

        <div className="bg-white rounded-2xl p-4 shadow-sm border border-stone-200">
          <h3 className="font-bold text-stone-800 mb-3">🔋 แบตเตอรี่ ({batteries.length} รุ่น)</h3>
          <button onClick={() => setCustomBattery(null)}
            className={`w-full p-3 rounded-xl border-2 text-left mb-2 ${
              customBattery === null ? 'border-amber-500 bg-amber-50' : 'border-stone-200'
            }`}>
            <div className="font-medium">❌ ไม่ใช้แบตเตอรี่</div>
            <div className="text-xs text-stone-500">เหมาะกับ on-grid / ใช้ไฟกลางวันเยอะ</div>
          </button>
          {batteries.map(bat => (
            <button key={bat.id} onClick={() => setCustomBattery(bat)}
              className={`w-full p-3 rounded-xl border-2 text-left ${
                customBattery?.id === bat.id ? 'border-amber-500 bg-amber-50' : 'border-stone-200'
              }`}>
              <div className="font-medium">{bat.brand} {bat.model}</div>
              <div className="text-xs text-stone-500">ความจุ {bat.capacity}kWh</div>
            </button>
          ))}
        </div>

        <button onClick={() => setStep(4)}
          disabled={!customInverter || !customPanel || customPanelCount < 1}
          className="w-full bg-amber-500 hover:bg-amber-600 disabled:bg-stone-300 text-white py-3 rounded-xl font-medium">
          ดูสรุปและการวิเคราะห์ →
        </button>
      </div>
    );
  }
  
  // ============ STEP 4: Closing Infographic ============
  if (step === 4 && active) {
    return (
      <SalesPresentationCloser
        active={active}
        customerName={customerName}
        customerPhone={customerPhone}
        customerAddress={customerAddress}
        customerMode={customerMode}
        selectedCustomerId={selectedCustomerId}
        region={region}
        meterType={meterType}
        monthlyBill={monthlyBill}
        electricityRate={meterType === 'tou' ? `On-peak ${touOnPeak} / Off-peak ${touOffPeak}` : `${normalRate} ฿/หน่วย`}
        inflationRate={inflationRate}
        companyInfo={companyInfo}
        stock={stock}
        catalog={catalog}
        calcOpts={calcOpts}
        onBack={() => setStep(2)}
        onCreateQuotation={onCreateQuotation}
        onSaveCustomer={onSaveCustomer}
        onSaveCompany={onSaveCompany}
      />
    );
  }
  
  return null;
}

// ============== SALES CLOSING INFOGRAPHIC ==============
// ============== Pro Mode Panel — โหมดเทคนิค (ซ่อน, ใส่ PIN เข้า) ==============
function ProModePanel({ active, totalKW, region, curMeterType, proFactors, setProFactors, proTilt, setProTilt, proDirection, setProDirection }) {
  // ========== ตั้งเวลา/วันที่สำหรับ Real-time check ==========
  const [now, setNow] = useState(new Date());
  const [customTime, setCustomTime] = useState(false);
  
  useEffect(() => {
    if (customTime) return;
    const t = setInterval(() => setNow(new Date()), 60000); // อัพเดททุกนาที
    return () => clearInterval(t);
  }, [customTime]);
  
  const hour = now.getHours() + now.getMinutes() / 60;
  const month = now.getMonth() + 1;
  
  // คำนวณกำลังผลิต ณ ขณะนั้น (kW)
  const currentProd = calculateCurrentProduction({
    kW: Math.min(totalKW, active.inverter.size),
    hour, month,
    direction: proDirection,
    tilt: proTilt,
    factors: proFactors,
  });
  
  const seasonFactor = getSeasonFactor(month);
  const dirFactor = PANEL_DIRECTIONS[proDirection]?.factor || 1.0;
  const tiltFactor = getTiltFactor(proTilt);
  
  // List ของ factors ที่กดเปิด/ปิดได้
  const factorList = [
    { key: 'pr', label: 'Performance Ratio', desc: 'ประสิทธิภาพระบบ', impact: '-27%', color: 'rose' },
    { key: 'degradation', label: 'Degradation', desc: 'การเสื่อมของแผง 0.6%/ปี', impact: '-0.6%/ปี', color: 'rose' },
    { key: 'dust', label: 'ฝุ่น/สิ่งสกปรก', desc: 'แผงไม่สะอาด', impact: '-5%', color: 'amber' },
    { key: 'shade', label: 'เงาบัง', desc: 'ต้นไม้/อาคาร/สิ่งกีดขวาง', impact: '-15%', color: 'amber' },
    { key: 'heatLoss', label: 'อุณหภูมิสูง', desc: 'แผงร้อนทำงานแย่ลง', impact: '-8%', color: 'amber' },
    { key: 'cableLoss', label: 'Loss ในสาย', desc: 'การสูญเสียในสายไฟ', impact: '-3%', color: 'amber' },
    { key: 'inverterEff', label: 'ประสิทธิภาพ Inverter', desc: 'แปลง DC→AC ไม่ 100%', impact: '-4%', color: 'amber' },
  ];
  
  return (
    <div className="bg-blue-50 border-2 border-blue-300 rounded-2xl p-4 space-y-3 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="font-bold text-blue-800 text-base">🔧 โหมดเทคนิค</h3>
          <p className="text-xs text-blue-600">ปรับปัจจัยต่างๆ ดูผลแบบจริง</p>
        </div>
      </div>
      
      {/* === Real-time Production === */}
      <div className="bg-white rounded-xl p-3">
        <div className="flex items-center justify-between mb-2">
          <div className="text-sm font-medium text-stone-700">⚡ กำลังผลิต ณ ตอนนี้</div>
          <button onClick={() => setCustomTime(!customTime)} 
            className="text-xs text-blue-600 hover:underline">
            {customTime ? '🕐 ใช้เวลาปัจจุบัน' : '⏱️ ตั้งเวลาเอง'}
          </button>
        </div>
        
        {/* แสดงเวลาที่ใช้คำนวณ */}
        {customTime ? (
          <div className="flex gap-2 mb-2">
            <input type="time" 
              value={`${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`}
              onChange={e => {
                const [h, m] = e.target.value.split(':').map(Number);
                const d = new Date(now);
                d.setHours(h, m);
                setNow(d);
              }}
              className="flex-1 px-2 py-1 border rounded-lg text-sm" />
            <select 
              value={month}
              onChange={e => {
                const d = new Date(now);
                d.setMonth(parseInt(e.target.value) - 1);
                setNow(d);
              }}
              className="px-2 py-1 border rounded-lg text-sm">
              {['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.'].map((m, i) => (
                <option key={i+1} value={i+1}>{m}</option>
              ))}
            </select>
          </div>
        ) : (
          <div className="text-xs text-stone-500 mb-2">
            🕐 {now.toLocaleString('th-TH', { hour: '2-digit', minute: '2-digit', day: '2-digit', month: 'short' })}
          </div>
        )}
        
        <div className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-lg p-3 text-center border border-amber-200">
          <div className="text-3xl font-bold text-amber-700">
            {currentProd.toFixed(2)} <span className="text-lg">kW</span>
          </div>
          <div className="text-xs text-stone-600 mt-1">
            ({((currentProd / active.inverter.size) * 100).toFixed(0)}% ของ Inverter {active.inverter.size}kW)
          </div>
        </div>
        
        <div className="text-xs text-stone-600 mt-2 grid grid-cols-2 gap-x-2 gap-y-1">
          <div>🌅 ช่วงเวลา: <strong>{hour.toFixed(1)} น.</strong></div>
          <div>📅 ฤดู: <strong>{(seasonFactor * 100).toFixed(0)}%</strong></div>
          <div>🧭 ทิศ: <strong>{(dirFactor * 100).toFixed(0)}%</strong></div>
          <div>📐 มุม: <strong>{(tiltFactor * 100).toFixed(0)}%</strong></div>
        </div>
        
        <p className="text-xs text-blue-600 italic mt-2">
          💡 เทียบกับค่าใน inverter จริง — ถ้าน้อยกว่ามาก อาจมีปัญหา
        </p>
      </div>
      
      {/* === ทิศการติดตั้ง === */}
      <div className="bg-white rounded-xl p-3">
        <div className="text-sm font-medium text-stone-700 mb-2">🧭 ทิศที่แผงหันไป</div>
        <div className="grid grid-cols-4 gap-1">
          {Object.entries(PANEL_DIRECTIONS).map(([key, dir]) => (
            <button key={key} onClick={() => setProDirection(key)}
              className={`p-2 rounded-lg border text-xs transition-all ${
                proDirection === key 
                  ? 'border-blue-500 bg-blue-100 font-bold' 
                  : 'border-stone-200 hover:border-stone-400'
              }`}>
              <div className="text-base">{dir.icon}</div>
              <div className="text-[10px]">{dir.label}</div>
              <div className="text-[10px] text-stone-500">{(dir.factor * 100).toFixed(0)}%</div>
            </button>
          ))}
        </div>
      </div>
      
      {/* === มุมแผง === */}
      <div className="bg-white rounded-xl p-3">
        <div className="flex items-center justify-between mb-2">
          <div className="text-sm font-medium text-stone-700">📐 มุมเอียงแผง</div>
          <div className="text-sm font-bold text-blue-700">{proTilt}° ({(tiltFactor * 100).toFixed(0)}%)</div>
        </div>
        <input type="range" min={0} max={90} value={proTilt}
          onChange={e => setProTilt(parseInt(e.target.value))}
          className="w-full" />
        <div className="flex justify-between text-[10px] text-stone-500 mt-1">
          <span>0°</span>
          <span className="text-emerald-600 font-medium">10-15° (ดีที่สุด)</span>
          <span>90°</span>
        </div>
      </div>
      
      {/* === ปัจจัยลบ Toggle === */}
      <div className="bg-white rounded-xl p-3">
        <div className="text-sm font-medium text-stone-700 mb-2">⚙️ ปัจจัยที่ส่งผลต่อการผลิต</div>
        <div className="space-y-1.5">
          {factorList.map(f => (
            <label key={f.key} 
              className={`flex items-center justify-between p-2 rounded-lg cursor-pointer transition-all ${
                proFactors[f.key] ? 'bg-rose-50 border border-rose-200' : 'bg-stone-50 hover:bg-stone-100'
              }`}>
              <div className="flex items-center gap-2 flex-1">
                <input type="checkbox" 
                  checked={proFactors[f.key]}
                  onChange={e => setProFactors({...proFactors, [f.key]: e.target.checked})}
                  className="w-4 h-4 accent-rose-500" />
                <div>
                  <div className="text-xs font-medium">{f.label}</div>
                  <div className="text-[10px] text-stone-500">{f.desc}</div>
                </div>
              </div>
              <div className={`text-xs font-bold ${proFactors[f.key] ? 'text-rose-600' : 'text-stone-400'}`}>
                {f.impact}
              </div>
            </label>
          ))}
        </div>
      </div>
      
      {/* === References === */}
      <div className="bg-white rounded-xl p-3 text-[10px] text-stone-500 space-y-1">
        <p className="font-bold text-stone-700 text-xs">📚 ที่มา (อ้างอิงงานวิจัย):</p>
        <p>• PSH ทฤษฎี: World Bank/SolarGIS — เฉลี่ยไทย 5.06 kWh/m²/วัน</p>
        <p>• Performance Ratio 71-85%: RMUTSB Academic Journal 2021</p>
        <p>• Degradation 0.5%/ปี: NREL (ปรับ 0.6% สำหรับเขตร้อน)</p>
        <p>• ทิศ/มุม: ประเทศไทยอยู่ใต้เส้นศูนย์สูตร → optimal มุม 10-15° หันใต้</p>
      </div>
    </div>
  );
}

function SalesPresentationCloser({ active: initialActive, customerName, customerPhone, customerAddress, customerMode, selectedCustomerId, region, meterType, monthlyBill, electricityRate, inflationRate, companyInfo, stock, catalog, calcOpts, onBack, onCreateQuotation, onSaveCustomer, onEdit, onSaveCompany }) {
  const [animateStep, setAnimateStep] = useState(0);
  // ลูกค้าเปลี่ยนมิเตอร์ได้ในหน้านี้ (เริ่มจากที่เซลส์เลือก)
  const [curMeterType, setCurMeterType] = useState(meterType || 'normal');
  const [showMeterCompare, setShowMeterCompare] = useState(false);
  
  // Pro Mode (ซ่อน) - ใส่ PIN 1234 เพื่อเปิด
  const [showProModal, setShowProModal] = useState(false);
  const [proPinInput, setProPinInput] = useState('');
  const [proPinError, setProPinError] = useState(false);
  const [proModeOpen, setProModeOpen] = useState(false);
  const [editFreebies, setEditFreebies] = useState(false);
  
  // Pro Mode factors (toggle ได้)
  const [proFactors, setProFactors] = useState({
    pr: false,           // ใช้ Performance Ratio 73%
    degradation: false,  // หัก degradation 0.6%/ปี
    dust: false,         // ฝุ่น -5%
    shade: false,        // เงา -15%
    heatLoss: false,     // อุณหภูมิสูง -8%
    cableLoss: false,    // loss ในสาย -3%
    inverterEff: false,  // ประสิทธิภาพ inverter -4%
  });
  const [proTilt, setProTilt] = useState(15);          // มุมแผง (องศา)
  const [proDirection, setProDirection] = useState('S'); // ทิศ
  
  const handleProPinSubmit = () => {
    if (proPinInput === '1234') {
      setProModeOpen(true);
      setShowProModal(false);
      setProPinInput('');
      setProPinError(false);
    } else {
      setProPinError(true);
      setTimeout(() => setProPinError(false), 1500);
    }
  };
  
  // Equipment state — ลูกค้าเล่นเปลี่ยนได้ในหน้านี้
  const [curInverter, setCurInverter] = useState(initialActive.inverter);
  const [curPanel, setCurPanel] = useState(initialActive.panel);
  const [curPanelCount, setCurPanelCount] = useState(initialActive.panelCount);
  const [curBattery, setCurBattery] = useState(initialActive.battery);
  const [customSellPrice, setCustomSellPrice] = useState(null); // null = ใช้ราคา auto
  
  // ดึง catalog (เฉพาะ active)
  const activeCatalog = (catalog || []).filter(c => c.active !== false);
  const inverters = activeCatalog.filter(c => c.category === 'inverter');
  const panels = activeCatalog.filter(c => c.category === 'panel');
  const batteries = activeCatalog.filter(c => c.category === 'battery');
  
  // คำนวณ active ใหม่ทุกครั้งที่เปลี่ยน equipment (smart cost: stock first → market)
  const active = useMemo(() => {
    if (!curInverter || !curPanel || curPanelCount < 1) return initialActive;
    const invCost = calcSmartCost(curInverter, 1, stock || []);
    const panCost = calcSmartCost(curPanel, curPanelCount, stock || []);
    const batCost = curBattery ? calcSmartCost(curBattery, 1, stock || []) : { cost: 0, fromStock: 0, fromMarket: 0, breakdown: [], total: 0 };
    const equipmentCost = invCost.cost + panCost.cost + batCost.cost;
    const installCost = sumHiddenCosts(companyInfo, curInverter.size); // ต้นทุนแฝงต่องาน (ตามขนาด)
    const grandCost = equipmentCost + installCost;
    const margin = getMargin(curInverter.size, companyInfo);
    const autoSellPriceRaw = applyMargin(grandCost, margin);
    const autoSellPrice = roundUpTo999(autoSellPriceRaw); // 🎯 ปัดขึ้น 999
    const sellPrice = customSellPrice != null ? customSellPrice : autoSellPrice;
    const totalKW = (curPanel.watt * curPanelCount) / 1000;
    
    // Pro Mode: คำนวณตามจริง ใช้ factors ที่เลือกไว้
    let roi;
    if (proModeOpen) {
      // base PSH (theoretical)
      const regionData = SOLAR_REGIONS[region] || SOLAR_REGIONS.central;
      let effectivePSH = regionData.theoreticalPSH || regionData.hours || 5.0;
      
      // คูณ factor ทีละตัวที่ toggle ไว้
      if (proFactors.pr) effectivePSH *= regionData.pr || 0.73;       // -27%
      if (proFactors.dust) effectivePSH *= 0.95;                       // -5%
      if (proFactors.shade) effectivePSH *= 0.85;                      // -15%
      if (proFactors.heatLoss) effectivePSH *= 0.92;                   // -8%
      if (proFactors.cableLoss) effectivePSH *= 0.97;                  // -3%
      if (proFactors.inverterEff) effectivePSH *= 0.96;                // -4%
      
      // ทิศและมุม
      const dirFactor = PANEL_DIRECTIONS[proDirection]?.factor || 1.0;
      const tiltFactor = getTiltFactor(proTilt);
      effectivePSH *= dirFactor * tiltFactor;
      
      // คำนวณ ROI ด้วย effective PSH
      const effKW = Math.min(totalKW, curInverter.size);
      const monthlyKwh = effKW * effectivePSH * 30;
      const yearlyKwh = monthlyKwh * 12;
      
      // อัตราค่าไฟ
      let effectiveRate;
      if (curMeterType === 'tou') {
        const onPeakPct = 0.95;
        effectiveRate = (PRICING_CONFIG.touOnPeak * onPeakPct) + (PRICING_CONFIG.touOffPeak * (1 - onPeakPct));
      } else {
        effectiveRate = PRICING_CONFIG.electricityRate;
      }
      
      const degradation = proFactors.degradation ? PANEL_DEGRADATION_RATE : 0;
      const cumProfit = (years) => {
        let total = 0;
        for (let y = 1; y <= years; y++) {
          const yearProd = yearlyKwh * Math.pow(1 - degradation, y - 1);
          total += yearProd * effectiveRate;
        }
        return Math.round(total);
      };
      
      roi = {
        monthlyKwh: Math.round(monthlyKwh),
        yearlyKwh: Math.round(yearlyKwh),
        monthlySavings: Math.round(monthlyKwh * effectiveRate),
        yearlySavings: Math.round(yearlyKwh * effectiveRate),
        effectiveRate,
        peakHours: effectivePSH,
        pr: regionData.pr,
        degradation,
        profit5: cumProfit(5),
        profit10: cumProfit(10),
        profit20: cumProfit(20),
        profit30: cumProfit(30),
      };
    } else {
      // โหมดปกติ (แสดงตัวเลขแบบ dream เหมือนเดิม)
      roi = calculateROI({ kW: Math.min(totalKW, curInverter.size), ...(calcOpts || {}), meterType: curMeterType, mode: 'dream' });
    }
    
    const breakEven = sellPrice / roi.yearlySavings;
    const actualMargin = Math.round(((sellPrice / grandCost) - 1) * 100);
    
    return {
      label: initialActive.label,
      badge: initialActive.badge,
      inverter: curInverter, panel: curPanel, panelCount: curPanelCount, battery: curBattery,
      costBreakdown: { invCost, panCost, batCost },
      equipmentCost, installCost,
      totalCost: grandCost,
      sellPrice,
      margin: actualMargin,
      profit: sellPrice - grandCost,
      totalKW: Math.round(totalKW * 100) / 100,
      roi,
      breakEven: Math.round(breakEven * 10) / 10,
    };
  }, [curInverter, curPanel, curPanelCount, curBattery, customSellPrice, companyInfo, calcOpts, initialActive, stock, curMeterType, proModeOpen, proFactors, proTilt, proDirection, region]);
  
  useEffect(() => {
    const timers = [];
    for (let i = 1; i <= 6; i++) {
      timers.push(setTimeout(() => setAnimateStep(i), i * 400));
    }
    return () => timers.forEach(clearTimeout);
  }, []);
  
  const { roi, sellPrice, breakEven, totalKW, inverter, panel, panelCount, battery, profit, margin, totalCost, equipmentCost, installCost } = active;
  
  const compareBank = calculateInvestmentComparison(sellPrice, 30, PRICING_CONFIG.comparisonRates.bank);
  const compareStock = calculateInvestmentComparison(sellPrice, 30, PRICING_CONFIG.comparisonRates.stock);
  const compareGold = calculateInvestmentComparison(sellPrice, 30, PRICING_CONFIG.comparisonRates.gold);
  
  const handleCreateQuotation = () => {
    const itemDescription = `ระบบโซล่าเซลล์ ${totalKW} kW
- ${inverter.brand} ${inverter.model} × 1 ชุด
- ${panel.brand} ${panel.model} × ${panelCount} แผ่น
${battery ? `- ${battery.brand} ${battery.model} × 1 ลูก` : ''}
- พร้อมติดตั้งและรับประกัน`;
    
    // === Snapshot สำหรับสร้างงานทีหลัง ===
    const equipmentSnapshot = {
      inverter: { id: inverter.id, brand: inverter.brand, model: inverter.model, size: inverter.size, cost: inverter.marketPrice },
      panel: { id: panel.id, brand: panel.brand, model: panel.model, watt: panel.watt, qty: panelCount, costEach: panel.marketPrice, total: panel.marketPrice * panelCount },
      battery: battery ? { id: battery.id, brand: battery.brand, model: battery.model, capacity: battery.capacity, cost: battery.marketPrice } : null,
      totalKW,
      jobType: `${totalKW}kW ${inverter.type === 'hybrid' ? 'Hybrid' : inverter.type === 'ongrid' ? 'On-grid' : 'Off-grid'}${battery ? ` + แบต ${battery.capacity}kWh` : ''}`,
      equipmentCost,
      installCost,
      totalCost,
      expectedProfit: profit,
      margin,
      meterType: curMeterType,
    };
    
    onCreateQuotation({
      customerName, customerPhone, customerAddress,
      customerMode, selectedCustomerId,
      items: [{
        id: `item-${Date.now()}`,
        name: itemDescription,
        qty: 1, unit: 'ชุด',
        unitPrice: sellPrice, amount: sellPrice,
      }],
      totalAmount: sellPrice,
      equipmentSnapshot,
      expectedProfit: profit,
      expectedCost: totalCost,
      jobType: equipmentSnapshot.jobType,
    });
  };

  const AnimatedNumber = ({ value, suffix = '', show, duration = 600 }) => {
    const [display, setDisplay] = useState(show ? 0 : value);
    const prevValueRef = useRef(0);
    
    useEffect(() => {
      if (!show) return;
      const startValue = prevValueRef.current;
      const targetValue = value;
      const startTime = Date.now();
      
      const tick = () => {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = Math.round(startValue + (targetValue - startValue) * eased);
        setDisplay(current);
        if (progress < 1) requestAnimationFrame(tick);
        else prevValueRef.current = targetValue;
      };
      tick();
    }, [show, value, duration]);
    
    return <>{display.toLocaleString()}{suffix}</>;
  };

  return (
    <div className="space-y-4 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="display-font text-3xl text-stone-800">🎯 ข้อเสนอพิเศษ</h2>
          <p className="text-sm text-stone-500">สำหรับ {customerName}</p>
        </div>
        <div className="flex items-center gap-2">
          {/* ปุ่มลับ Pro Mode */}
          {!proModeOpen ? (
            <button onClick={() => setShowProModal(true)} 
              className="text-stone-300 hover:text-stone-500 text-xs"
              title="โหมดเทคนิค">
              🔧
            </button>
          ) : (
            <button onClick={() => { setProModeOpen(false); }} 
              className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200"
              title="ปิดโหมดเทคนิค">
              🔧 Pro
            </button>
          )}
          <button onClick={onBack} className="text-sm text-stone-600 hover:text-stone-800">← กลับ</button>
        </div>
      </div>

      {/* Meter Type Toggle — ลูกค้าเลือก Normal vs TOU ได้ */}
      <div className="bg-white rounded-2xl p-3 shadow-sm border border-stone-200">
        <div className="flex items-center justify-between mb-2">
          <div className="text-sm font-medium text-stone-700">⚡ ประเภทมิเตอร์ไฟ</div>
          <button onClick={() => setShowMeterCompare(!showMeterCompare)}
            className="text-xs text-blue-600 hover:underline">
            {showMeterCompare ? 'ซ่อน' : '🤔 เปรียบเทียบ'}
          </button>
        </div>
        <div className="grid grid-cols-2 gap-2">
          <button onClick={() => setCurMeterType('normal')}
            className={`p-2.5 rounded-xl border-2 text-left transition-all ${
              curMeterType === 'normal' ? 'border-amber-500 bg-amber-50' : 'border-stone-200 hover:border-stone-300'
            }`}>
            <div className="font-medium text-sm">🏠 มิเตอร์ปกติ</div>
            <div className="text-xs text-stone-500 mt-0.5">{PRICING_CONFIG.electricityRate} ฿/หน่วย ทั้งวัน</div>
          </button>
          <button onClick={() => setCurMeterType('tou')}
            className={`p-2.5 rounded-xl border-2 text-left transition-all ${
              curMeterType === 'tou' ? 'border-amber-500 bg-amber-50' : 'border-stone-200 hover:border-stone-300'
            }`}>
            <div className="font-medium text-sm">⏰ มิเตอร์ TOU</div>
            <div className="text-xs text-stone-500 mt-0.5">{PRICING_CONFIG.touOnPeak}/{PRICING_CONFIG.touOffPeak} ฿</div>
          </button>
        </div>
        
        {/* Comparison panel */}
        {showMeterCompare && (
          <div className="mt-3 grid grid-cols-2 gap-2 text-xs">
            <div className="bg-stone-50 rounded-lg p-2.5 space-y-1">
              <div className="font-bold text-stone-700">🏠 มิเตอร์ปกติ</div>
              <div className="text-emerald-700">
                ✅ <strong>ข้อดี</strong>
                <ul className="ml-3 mt-0.5 space-y-0.5 text-stone-600">
                  <li>• คิดอัตราเดียวทั้งวัน ง่าย</li>
                  <li>• ไม่ต้องปรับพฤติกรรม</li>
                  <li>• ไม่มีค่าใช้จ่ายเปลี่ยนมิเตอร์</li>
                </ul>
              </div>
              <div className="text-rose-700 mt-1.5">
                ❌ <strong>ข้อเสีย</strong>
                <ul className="ml-3 mt-0.5 space-y-0.5 text-stone-600">
                  <li>• ใช้ไฟมาก = แพงขึ้นแบบขั้นบันได</li>
                  <li>• ไม่ได้ส่วนลดช่วง off-peak</li>
                </ul>
              </div>
              <div className="bg-amber-100 text-amber-800 rounded p-1.5 mt-1.5">
                <strong>👤 เหมาะกับ:</strong> บ้านที่ใช้ไฟกลางวันเยอะ (WFH, แม่บ้าน, มีคนอยู่บ้านตลอด)
              </div>
            </div>
            
            <div className="bg-blue-50 rounded-lg p-2.5 space-y-1">
              <div className="font-bold text-blue-700">⏰ มิเตอร์ TOU</div>
              <div className="text-emerald-700">
                ✅ <strong>ข้อดี</strong>
                <ul className="ml-3 mt-0.5 space-y-0.5 text-stone-600">
                  <li>• Off-peak ถูกกว่า {(PRICING_CONFIG.electricityRate - PRICING_CONFIG.touOffPeak).toFixed(2)} ฿/หน่วย</li>
                  <li>• เหมาะมากกับ Solar (ผลิตช่วง peak)</li>
                  <li>• คุ้มถ้าบริหารการใช้ไฟได้</li>
                </ul>
              </div>
              <div className="text-rose-700 mt-1.5">
                ❌ <strong>ข้อเสีย</strong>
                <ul className="ml-3 mt-0.5 space-y-0.5 text-stone-600">
                  <li>• On-peak (จ-ศ 9-22น.) แพงกว่า {(PRICING_CONFIG.touOnPeak - PRICING_CONFIG.electricityRate).toFixed(2)} ฿/หน่วย</li>
                  <li>• ค่าเปลี่ยนมิเตอร์ ~6,700 ฿</li>
                  <li>• ค่าบริการรายเดือน ~312 ฿</li>
                </ul>
              </div>
              <div className="bg-blue-100 text-blue-800 rounded p-1.5 mt-1.5">
                <strong>👤 เหมาะกับ:</strong> บ้านที่ทำงานนอกบ้าน + มีโซล่า + ใช้ไฟกลางคืน/เสาร์อาทิตย์เยอะ + ชาร์จรถ EV
              </div>
            </div>
          </div>
        )}
        
        {curMeterType === 'tou' && (
          <div className="mt-2 bg-amber-50 border border-amber-200 rounded-lg p-2 text-xs">
            <strong className="text-amber-700">💡 Solar + TOU = คู่หูสุดคุ้ม!</strong>
            <span className="text-stone-600 ml-1">Solar ผลิตช่วง on-peak (กลางวัน) = ลดอัตราที่แพงสุด</span>
          </div>
        )}
      </div>
      
      {/* PIN Modal */}
      {showProModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl p-5 max-w-sm w-full" onClick={e => e.stopPropagation()}>
            <h3 className="font-bold text-lg mb-1">🔧 โหมดเทคนิค (Pro)</h3>
            <p className="text-xs text-stone-500 mb-3">ใส่รหัสผ่านเพื่อเข้าโหมดคำนวณตามจริง</p>
            <input type="password" value={proPinInput} 
              onChange={e => setProPinInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleProPinSubmit()}
              placeholder="••••" maxLength={4}
              autoFocus
              className={`w-full px-4 py-3 text-center text-2xl tracking-widest border-2 rounded-xl outline-none ${
                proPinError ? 'border-rose-500 bg-rose-50 animate-pulse' : 'border-stone-300 focus:border-blue-500'
              }`} />
            {proPinError && <p className="text-xs text-rose-600 mt-2 text-center">รหัสผ่านไม่ถูกต้อง</p>}
            <div className="flex gap-2 mt-3">
              <button onClick={() => setShowProModal(false)} className="flex-1 py-2 text-stone-600 rounded-xl hover:bg-stone-100">ยกเลิก</button>
              <button onClick={handleProPinSubmit} className="flex-1 py-2 bg-blue-500 text-white rounded-xl hover:bg-blue-600">เข้าโหมด</button>
            </div>
          </div>
        </div>
      )}
      
      {/* Pro Mode Panel — แสดงเมื่อปลดล็อค */}
      {proModeOpen && (
        <ProModePanel 
          active={active}
          totalKW={totalKW}
          region={region}
          curMeterType={curMeterType}
          proFactors={proFactors} setProFactors={setProFactors}
          proTilt={proTilt} setProTilt={setProTilt}
          proDirection={proDirection} setProDirection={setProDirection}
        />
      )}
      
      {/* === 🏆 Hero Badge === */}
      {active.label?.includes('คุ้มสุด') && (
        <div className={`bg-gradient-to-r from-amber-500 via-yellow-400 to-amber-500 rounded-xl p-3 text-white text-center shadow-lg animate-fade-in`}>
          <div className="text-base font-bold">🏆 ชุดขายดี อันดับ 1</div>
          {companyInfo?.saleSlogan && (
            <div className="text-xs opacity-90 mt-0.5">⭐⭐⭐⭐⭐ "{companyInfo.saleSlogan}"</div>
          )}
        </div>
      )}
      
      <div className={`sticky top-2 z-20 bg-gradient-to-br from-amber-400 via-orange-400 to-orange-500 rounded-3xl p-5 text-white shadow-2xl text-center transition-all duration-700 ${animateStep >= 1 ? 'scale-100 opacity-100' : 'scale-90 opacity-0'}`}
        key="price-card-sticky">
        <div className="text-4xl mb-1">{active.badge}</div>
        <div className="text-xs opacity-90">{active.label}</div>
        <div className="bg-white/20 rounded-2xl p-3 backdrop-blur mt-2">
          <div className="text-xs opacity-90">ราคาทั้งหมด</div>
          <div className="text-5xl font-bold mt-1 tabular-nums tracking-tight">
            <AnimatedNumber value={sellPrice} show={animateStep >= 1} duration={600} />
            <span className="text-2xl ml-1 opacity-80">฿</span>
          </div>
          <div className="text-xs opacity-90 mt-1">
            ≈ <AnimatedNumber value={Math.round(sellPrice / Math.max(totalKW, 0.1))} show={animateStep >= 1} duration={600} /> ฿/kW
          </div>
        </div>
        <div className="grid grid-cols-3 gap-1 mt-3 text-xs">
          <div className="bg-white/10 rounded-lg py-1">🔌 {inverter.size}kW</div>
          <div className="bg-white/10 rounded-lg py-1">☀️ {panelCount} แผ่น</div>
          <div className="bg-white/10 rounded-lg py-1">{battery ? `🔋 ${battery.capacity}kWh` : '❌ ไม่มีแบต'}</div>
        </div>
      </div>

      {/* Equipment Builder — ลูกค้าปรับเองได้ */}
      <div className="bg-gradient-to-br from-white to-amber-50 rounded-2xl p-4 shadow-sm border-2 border-amber-300">
        <div className="text-center mb-3">
          <div className="text-3xl mb-1">👇</div>
          <h3 className="font-bold text-stone-800 text-lg">ลองเล่นปรับดูได้เลย!</h3>
          <p className="text-xs text-stone-500 mt-1">ตัวเลขด้านบนจะอัพเดททันที — ดูว่าแบบไหนเหมาะกับคุณ</p>
        </div>
        
        <div className="space-y-3">
          {/* Inverter selector */}
          <div>
            <label className="text-xs font-medium text-stone-600 mb-1 block">🔌 Inverter</label>
            <select 
              value={curInverter?.id || ''}
              onChange={e => {
                const inv = inverters.find(i => i.id === e.target.value);
                if (inv) setCurInverter(inv);
              }}
              className="w-full px-3 py-3 border-2 border-stone-200 rounded-xl text-sm font-medium bg-white focus:border-amber-500 focus:outline-none">
              {inverters.map(inv => (
                <option key={inv.id} value={inv.id}>
                  {inv.brand} {inv.model} ({inv.size}kW · {inv.type === 'hybrid' ? 'Hybrid' : inv.type === 'ongrid' ? 'On-grid' : 'Off-grid'})
                </option>
              ))}
            </select>
          </div>
          
          {/* Panel selector */}
          <div>
            <label className="text-xs font-medium text-stone-600 mb-1 block">☀️ แผงโซล่าเซลล์</label>
            <select
              value={curPanel?.id || ''}
              onChange={e => {
                const p = panels.find(x => x.id === e.target.value);
                if (p) setCurPanel(p);
              }}
              className="w-full px-3 py-3 border-2 border-stone-200 rounded-xl text-sm font-medium bg-white focus:border-amber-500 focus:outline-none mb-2">
              {panels.map(p => (
                <option key={p.id} value={p.id}>
                  {p.brand} {p.model} ({p.watt}W)
                </option>
              ))}
            </select>
            {/* Panel count */}
            <div className="bg-stone-50 rounded-xl p-3">
              <div className="flex items-center justify-between">
                <span className="text-xs text-stone-600">จำนวนแผ่น</span>
                <span className="text-xs text-stone-500">= {((curPanel?.watt || 0) * curPanelCount / 1000).toFixed(2)} kW</span>
              </div>
              <div className="flex items-center justify-center gap-3 mt-2">
                <button onClick={() => setCurPanelCount(Math.max(1, curPanelCount - 1))}
                  className="w-10 h-10 bg-stone-200 hover:bg-stone-300 rounded-full font-bold text-xl">−</button>
                <div className="text-3xl font-bold text-amber-600 min-w-[60px] text-center">{curPanelCount}</div>
                <button onClick={() => setCurPanelCount(curPanelCount + 1)}
                  className="w-10 h-10 bg-stone-200 hover:bg-stone-300 rounded-full font-bold text-xl">+</button>
              </div>
              {curInverter && curPanel && (
                <div className="text-xs text-center text-stone-500 mt-1">
                  💡 แนะนำ {Math.ceil(curInverter.size * 1100 / curPanel.watt)} แผ่น สำหรับ {curInverter.size}kW
                </div>
              )}
            </div>
          </div>
          
          {/* Battery selector */}
          <div>
            <label className="text-xs font-medium text-stone-600 mb-1 block">🔋 แบตเตอรี่</label>
            <select
              value={curBattery?.id || 'none'}
              onChange={e => {
                if (e.target.value === 'none') setCurBattery(null);
                else {
                  const b = batteries.find(x => x.id === e.target.value);
                  if (b) setCurBattery(b);
                }
              }}
              className="w-full px-3 py-3 border-2 border-stone-200 rounded-xl text-sm font-medium bg-white focus:border-amber-500 focus:outline-none">
              <option value="none">❌ ไม่ใช้แบตเตอรี่</option>
              {batteries.map(b => (
                <option key={b.id} value={b.id}>
                  🔋 {b.brand} {b.model} ({b.capacity}kWh)
                </option>
              ))}
            </select>
            {curBattery === null && (
              <p className="text-xs text-stone-500 mt-1 ml-1">เหมาะกับ on-grid / ใช้กลางวันเยอะ</p>
            )}
          </div>
        </div>
      </div>

      {/* Energy Production */}
      <div className={`bg-white rounded-2xl p-4 shadow-sm border border-emerald-200 transition-all duration-700 ${animateStep >= 2 ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'}`}>
        <div className="flex items-center gap-2 mb-3">
          <span className="text-2xl">⚡</span>
          <h3 className="font-bold text-stone-800">ผลผลิตและประหยัดค่าไฟ</h3>
          {meterType === 'tou' && <span className="text-xs bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full">TOU</span>}
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div className="bg-emerald-50 rounded-xl p-3 text-center">
            <div className="text-xs text-stone-600">ผลิตไฟต่อเดือน</div>
            <div className="text-2xl font-bold text-emerald-700">
              <AnimatedNumber value={roi.monthlyKwh} show={animateStep >= 2} />
            </div>
            <div className="text-xs text-stone-500">kWh</div>
          </div>
          <div className="bg-amber-50 rounded-xl p-3 text-center">
            <div className="text-xs text-stone-600">ประหยัดต่อเดือน</div>
            <div className="text-2xl font-bold text-amber-700">
              <AnimatedNumber value={roi.monthlySavings} show={animateStep >= 2} />
            </div>
            <div className="text-xs text-stone-500">฿</div>
          </div>
        </div>
        <div className="text-center text-sm text-stone-600 mt-2">
          = <strong className="text-amber-700"><AnimatedNumber value={roi.yearlySavings} show={animateStep >= 2} duration={600} /> ฿/ปี</strong>
        </div>
      </div>

      {/* Break Even */}
      <div className={`bg-white rounded-2xl p-4 shadow-sm border border-blue-200 transition-all duration-700 ${animateStep >= 3 ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'}`}>
        <div className="flex items-center gap-2 mb-3">
          <span className="text-2xl">🎯</span>
          <h3 className="font-bold text-stone-800">จุดคุ้มทุน</h3>
        </div>
        <div className="text-center">
          <div className="text-4xl font-bold text-blue-600 tabular-nums tracking-tight transition-all duration-300">{breakEven} ปี</div>
          <div className="text-xs text-stone-500 mt-1">หลังจากนั้น = กำไรล้วน!</div>
        </div>
        <div className="mt-3 bg-stone-100 rounded-full h-3 overflow-hidden">
          <div className="h-full bg-gradient-to-r from-amber-400 to-emerald-500 rounded-full transition-all duration-700" 
               style={{ width: animateStep >= 3 ? `${Math.min(100, (breakEven/30)*100)}%` : '0%' }} />
        </div>
        <div className="flex justify-between text-xs text-stone-500 mt-1">
          <span>เริ่ม</span>
          <span>30 ปี (อายุระบบ)</span>
        </div>
      </div>

      {/* 30-Year Profit Bars */}
      <div className={`bg-white rounded-2xl p-4 shadow-sm border border-emerald-200 transition-all duration-700 ${animateStep >= 4 ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'}`}>
        <div className="flex items-center gap-2 mb-3">
          <span className="text-2xl">💎</span>
          <h3 className="font-bold text-stone-800">กำไรในระยะยาว</h3>
        </div>
        <div className="space-y-2">
          {[
            { years: 5, value: roi.profit5 - sellPrice, color: 'stone' },
            { years: 10, value: roi.profit10 - sellPrice, color: 'amber' },
            { years: 20, value: roi.profit20 - sellPrice, color: 'orange' },
            { years: 30, value: roi.profit30 - sellPrice, color: 'emerald' },
          ].map((d, idx) => {
            const max = roi.profit30 - sellPrice;
            const pct = max > 0 ? (d.value / max) * 100 : 0;
            return (
              <div key={d.years}>
                <div className="flex items-center justify-between text-xs mb-1">
                  <span className="font-medium text-stone-700">{d.years} ปี</span>
                  <span className={`font-bold text-${d.color}-700 tabular-nums`}>
                    {d.value > 0 ? '+' : ''}<AnimatedNumber value={d.value} show={animateStep >= 4} duration={600} /> ฿
                  </span>
                </div>
                <div className="h-6 bg-stone-100 rounded-lg overflow-hidden">
                  <div className={`h-full bg-${d.color}-400 rounded-lg transition-all duration-700 flex items-center justify-end px-2`}
                       style={{ width: animateStep >= 4 ? `${Math.max(0, pct)}%` : '0%', transitionDelay: animateStep >= 4 ? `${idx * 100}ms` : '0ms' }}>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Investment Comparison */}
      <div className={`bg-white rounded-2xl p-4 shadow-sm border border-amber-200 transition-all duration-700 ${animateStep >= 5 ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'}`}>
        <div className="flex items-center gap-2 mb-3">
          <span className="text-2xl">🏆</span>
          <h3 className="font-bold text-stone-800">เทียบกับการลงทุนอื่น (30 ปี)</h3>
        </div>
        <p className="text-xs text-stone-500 mb-3">หากนำเงิน <AnimatedNumber value={sellPrice} show={animateStep >= 5} duration={600} /> ฿ ไปลงทุนแบบอื่น</p>
        
        {(() => {
          const solarProfit = roi.profit30 - sellPrice;
          const max = Math.max(solarProfit, compareBank, compareStock, compareGold);
          const items = [
            { icon: '💰', label: 'เงินฝาก', rate: '1.5%', value: compareBank, color: 'stone' },
            { icon: '🥇', label: 'ทอง',     rate: '6%',   value: compareGold, color: 'yellow' },
            { icon: '📈', label: 'หุ้น',    rate: '7%',   value: compareStock, color: 'blue' },
            { icon: '☀️', label: 'Solar (this)', rate: '', value: solarProfit, color: 'emerald', winner: true },
          ];
          return (
            <div className="space-y-2">
              {items.map((it, idx) => {
                const pct = max > 0 ? (it.value / max) * 100 : 0;
                return (
                  <div key={it.label}>
                    <div className="flex items-center justify-between text-xs mb-1">
                      <span className={`font-medium ${it.winner ? 'text-emerald-700' : 'text-stone-700'}`}>
                        {it.icon} {it.label} {it.rate}
                      </span>
                      <span className={`font-bold tabular-nums ${it.winner ? 'text-emerald-700 text-base' : 'text-stone-600'}`}>
                        +<AnimatedNumber value={it.value} show={animateStep >= 5} duration={600} /> ฿ {it.winner && '🏆'}
                      </span>
                    </div>
                    <div className="h-5 bg-stone-100 rounded-lg overflow-hidden">
                      <div className={`h-full ${it.winner ? 'bg-gradient-to-r from-amber-400 to-emerald-500' : `bg-${it.color}-300`} transition-all duration-700`}
                           style={{ width: animateStep >= 5 ? `${Math.max(2, pct)}%` : '0%', transitionDelay: animateStep >= 5 ? `${idx * 100}ms` : '0ms' }} />
                    </div>
                  </div>
                );
              })}
            </div>
          );
        })()}
      </div>

      {/* === 🛡️ ตารางรับประกัน === */}
      {(companyInfo?.warranty?.length > 0) && (
        <div className={`bg-white rounded-2xl shadow-sm border-2 border-emerald-200 overflow-hidden transition-all duration-700 ${animateStep >= 4 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
          <div className="bg-gradient-to-r from-emerald-500 to-teal-500 px-4 py-2 text-white">
            <h3 className="font-bold text-sm">🛡️ รับประกันคุณภาพทุกชิ้น</h3>
          </div>
          <div className="p-3 grid grid-cols-2 gap-2">
            {companyInfo.warranty.map(w => (
              <div key={w.id} className="flex items-center justify-between bg-emerald-50 rounded-lg px-3 py-2">
                <div className="flex items-center gap-2">
                  <span className="text-base">{w.icon}</span>
                  <span className="text-xs text-stone-700">{w.label}</span>
                </div>
                <span className="font-bold text-emerald-700 text-sm whitespace-nowrap">
                  {w.years >= 99 ? 'ตลอด' : `${w.years} ปี`}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* === 🔧 สเปคที่ใส่ใจ === */}
      {(companyInfo?.specs?.length > 0) && (
        <div className={`bg-white rounded-2xl shadow-sm border border-stone-200 overflow-hidden transition-all duration-700 delay-100 ${animateStep >= 4 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
          <div className="bg-gradient-to-r from-stone-700 to-stone-800 px-4 py-2 text-white">
            <h3 className="font-bold text-sm">🔧 สเปคที่ใส่ใจ</h3>
          </div>
          <div className="p-3 space-y-1.5">
            {companyInfo.specs.map(s => (
              <div key={s.id} className="flex items-start gap-2 text-xs">
                <span className="text-emerald-600 mt-0.5">✓</span>
                <div className="flex-1">
                  <span className="text-stone-700 font-medium">{s.label}: </span>
                  <span className="text-stone-500">{s.value}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* === 🎁 ของแถม === */}
      {(companyInfo?.freebies?.length > 0) && (
        <div className={`bg-gradient-to-br from-rose-50 to-amber-50 rounded-2xl shadow-sm border-2 border-rose-200 overflow-hidden transition-all duration-700 delay-200 ${animateStep >= 4 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
          <div className="bg-gradient-to-r from-rose-500 to-pink-500 px-4 py-2 text-white flex items-center justify-between">
            <h3 className="font-bold text-sm">🎁 ของแถมพิเศษ! ฟรี!</h3>
            <button
              onClick={() => setEditFreebies(!editFreebies)}
              className="text-[10px] bg-white/20 hover:bg-white/30 px-2 py-0.5 rounded transition-colors"
              title="แก้ไขของแถม"
            >
              {editFreebies ? '✓ เสร็จ' : '✏️ แก้ไข'}
            </button>
          </div>
          <div className="p-3 grid grid-cols-1 gap-1.5">
            {/* Edit Mode: แสดงทุกตัว + edit ได้ */}
            {editFreebies ? (
              <>
                {(companyInfo?.freebies || []).map((f, idx) => (
                  <div key={f.id} className={`flex items-center gap-2 rounded-lg px-3 py-2 text-xs ${f.active !== false ? 'bg-white/80' : 'bg-stone-100/60 opacity-60'}`}>
                    <input 
                      type="checkbox" 
                      checked={f.active !== false}
                      onChange={(e) => {
                        const newFreebies = [...(companyInfo.freebies || [])];
                        newFreebies[idx] = { ...newFreebies[idx], active: e.target.checked };
                        if (onSaveCompany) {
                          onSaveCompany({...companyInfo, freebies: newFreebies}, 'edit', `${e.target.checked ? 'เปิด' : 'ปิด'} ของแถม: ${f.label}`);
                        }
                      }}
                      className="w-4 h-4 accent-rose-500 cursor-pointer"
                    />
                    <span className="text-base">{f.icon}</span>
                    <input
                      type="text"
                      value={f.label}
                      onChange={(e) => {
                        const newFreebies = [...(companyInfo.freebies || [])];
                        newFreebies[idx] = { ...newFreebies[idx], label: e.target.value };
                        if (onSaveCompany) {
                          onSaveCompany({...companyInfo, freebies: newFreebies}, null);
                        }
                      }}
                      className="flex-1 bg-transparent border-b border-stone-300 focus:border-rose-500 outline-none text-stone-700 font-medium px-1"
                    />
                    <button
                      onClick={() => {
                        if (window.confirm(`ลบของแถม "${f.label}"?`)) {
                          const newFreebies = (companyInfo.freebies || []).filter((_, i) => i !== idx);
                          if (onSaveCompany) {
                            onSaveCompany({...companyInfo, freebies: newFreebies}, 'delete', `ลบของแถม: ${f.label}`);
                          }
                        }
                      }}
                      className="text-rose-500 hover:bg-rose-100 rounded p-1"
                    >
                      🗑️
                    </button>
                  </div>
                ))}
                {/* ปุ่มเพิ่มของแถม */}
                <button
                  onClick={() => {
                    const newItem = { 
                      id: `f-${Date.now()}-${Math.random().toString(36).slice(2,5)}`, 
                      icon: '🎁', 
                      label: 'ของแถมใหม่', 
                      active: true 
                    };
                    if (onSaveCompany) {
                      onSaveCompany({...companyInfo, freebies: [...(companyInfo.freebies || []), newItem]}, 'add', 'เพิ่มของแถม');
                    }
                  }}
                  className="flex items-center justify-center gap-1 bg-white/60 hover:bg-rose-100 border-2 border-dashed border-rose-300 rounded-lg px-3 py-2 text-xs text-rose-600 font-medium"
                >
                  ➕ เพิ่มของแถม
                </button>
              </>
            ) : (
              /* โหมดปกติ: แสดงเฉพาะ active */
              (companyInfo?.freebies || []).filter(f => f.active !== false).map(f => (
                <div key={f.id} className="flex items-center gap-2 bg-white/60 rounded-lg px-3 py-2 text-xs">
                  <span className="text-base">{f.icon}</span>
                  <span className="text-stone-700 font-medium">{f.label}</span>
                  <span className="ml-auto text-rose-600 font-bold text-[10px]">ฟรี!</span>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Disclaimer (ดูเป็นมืออาชีพ) */}
      <div className="bg-stone-50 border border-stone-200 rounded-xl p-3 text-xs text-stone-500">
        <p>⚠️ <strong>หมายเหตุ:</strong> ตัวเลขประมาณการจาก:</p>
        <ul className="ml-4 mt-1 space-y-0.5">
          <li>• ค่าไฟ: {electricityRate}</li>
          <li>• ผลิตไฟ {SOLAR_REGIONS[region]?.theoreticalPSH || SOLAR_REGIONS[region]?.hours} ชม./วัน ({SOLAR_REGIONS[region]?.label})</li>
          <li>• ค่าจริงอาจแตกต่างตามสภาพอากาศและการใช้งาน</li>
        </ul>
      </div>

      {/* Action Buttons */}
      <div className="sticky bottom-2 bg-white p-2 rounded-2xl shadow-lg border border-stone-200">
        <button onClick={handleCreateQuotation}
          className="w-full px-4 py-3 bg-amber-500 hover:bg-amber-600 text-white rounded-xl font-medium">
          📄 สร้างใบเสนอราคา
        </button>
      </div>
    </div>
  );
}

// ============== DOCUMENT MODAL (สร้าง/แก้ไขเอกสาร) ==============
function DocumentModal({ doc, defaultType = 'quotation', documents, customers, jobs, companyInfo, onClose, onSave }) {
  const isEdit = !!doc;
  const [form, setForm] = useState(doc || {
    id: `doc-${Date.now()}`,
    type: defaultType,
    docNumber: '',
    docDate: new Date().toISOString().split('T')[0],
    validUntil: new Date(Date.now() + 14 * 86400000).toISOString().split('T')[0],
    customerId: '',
    customerName: '',
    customerPhone: '',
    customerAddress: '',
    items: [{ id: 'item-1', name: '', qty: 1, unit: 'ชุด', unitPrice: 0, amount: 0 }],
    subtotal: 0,
    discount: 0,
    totalAmount: 0,
    paymentTerms: '',
    depositPercent: 0,
    depositAmount: 0,
    warrantyText: '', // ไม่ใส่ default - มี table รับประกันแล้ว
    notes: '',
    jobId: '',
    status: 'active',
    linkedDocId: '',
    createdAt: new Date().toISOString(),
  });

  // Auto-generate doc number when type changes
  useEffect(() => {
    if (!isEdit && (!form.docNumber || form.docNumber === '')) {
      setForm(f => ({ ...f, docNumber: generateDocNumber(f.type, documents) }));
    }
  }, [form.type, isEdit]);

  const update = (f, v) => setForm({...form, [f]: v});
  
  const updateItem = (idx, field, value) => {
    const newItems = [...form.items];
    newItems[idx] = { ...newItems[idx], [field]: value };
    if (field === 'qty' || field === 'unitPrice') {
      newItems[idx].amount = (Number(newItems[idx].qty) || 0) * (Number(newItems[idx].unitPrice) || 0);
    }
    const subtotal = newItems.reduce((s, it) => s + Number(it.amount || 0), 0);
    const discount = Number(form.discount || 0);
    setForm({ ...form, items: newItems, subtotal, totalAmount: subtotal - discount });
  };

  const addItem = () => {
    setForm({ ...form, items: [...form.items, { id: `item-${Date.now()}`, name: '', qty: 1, unit: 'ชุด', unitPrice: 0, amount: 0 }] });
  };

  const removeItem = (idx) => {
    if (form.items.length === 1) return;
    const newItems = form.items.filter((_, i) => i !== idx);
    const subtotal = newItems.reduce((s, it) => s + Number(it.amount || 0), 0);
    setForm({ ...form, items: newItems, subtotal, totalAmount: subtotal - Number(form.discount || 0) });
  };

  const updateDiscount = (v) => {
    const discount = Number(v) || 0;
    setForm({ ...form, discount, totalAmount: form.subtotal - discount });
  };

  const selectCustomer = (id) => {
    const c = customers.find(x => x.id === id);
    if (!c) {
      setForm({ ...form, customerId: '', customerName: '', customerPhone: '', customerAddress: '' });
      return;
    }
    setForm({
      ...form, customerId: id,
      customerName: c.name || '', customerPhone: c.phone || '', customerAddress: c.address || ''
    });
  };

  const selectJob = (id) => {
    const j = jobs.find(x => x.id === id);
    if (!j) { setForm({...form, jobId: ''}); return; }
    
    // Auto-fill จากงาน
    const itemName = `ระบบโซล่าเซลล์ ${j.type || ''} พร้อมติดตั้ง${j.location ? ` (${j.location})` : ''}`;
    const newItem = {
      id: `item-${Date.now()}`,
      name: itemName,
      qty: 1, unit: 'ชุด',
      unitPrice: Number(j.salePrice || 0),
      amount: Number(j.salePrice || 0),
    };
    setForm({
      ...form, jobId: id,
      items: [newItem],
      subtotal: Number(j.salePrice || 0),
      discount: Number(j.discount || 0),
      totalAmount: Number(j.salePrice || 0) - Number(j.discount || 0),
    });
  };

  const typeOptions = [
    { id: 'quotation', label: '📄 ใบเสนอราคา', color: 'blue' },
    { id: 'invoice', label: '🧾 ใบแจ้งหนี้', color: 'amber' },
    { id: 'receipt-deposit', label: '💰 RC มัดจำ', color: 'cyan' },
    { id: 'receipt-final', label: '✅ RC เต็ม', color: 'emerald' },
  ];

  const [submitError, setSubmitError] = useState('');

  const handleSubmit = () => {
    setSubmitError('');
    if (!form.customerName || !form.customerName.trim()) {
      setSubmitError('กรุณากรอกชื่อลูกค้า');
      // scroll up to show error
      setTimeout(() => {
        const errEl = document.getElementById('doc-error-msg');
        errEl?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 100);
      return;
    }
    if (!form.docNumber || !form.docNumber.trim()) {
      setSubmitError('กรุณากรอกเลขที่เอกสาร');
      return;
    }
    if (!form.items || form.items.length === 0 || form.items.every(i => !i.name)) {
      setSubmitError('กรุณาเพิ่มอย่างน้อย 1 รายการ');
      return;
    }
    if (!Number(form.totalAmount) || Number(form.totalAmount) <= 0) {
      setSubmitError('กรุณากรอกราคาในรายการ');
      return;
    }
    onSave(form);
  };

  return (
    <Modal title={isEdit ? 'แก้ไขเอกสาร' : 'สร้างเอกสารใหม่'} onClose={onClose} wide>
      {/* Type Selector */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-stone-700 mb-2">ประเภทเอกสาร</label>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          {typeOptions.map(opt => (
            <button
              key={opt.id}
              type="button"
              onClick={() => {
                const newType = opt.id;
                const newDocNumber = isEdit ? form.docNumber : generateDocNumber(newType, documents);
                setForm({...form, type: newType, docNumber: newDocNumber});
              }}
              className={`p-2 rounded-xl border-2 text-xs font-medium transition-all ${
                form.type === opt.id ? `border-${opt.color}-500 bg-${opt.color}-50 text-${opt.color}-700` : 'border-stone-200 bg-white'
              }`}
            >
              {opt.label}
            </button>
          ))}
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-3">
        <Field label="เลขที่เอกสาร">
          <input value={form.docNumber} onChange={e => update('docNumber', e.target.value)} className={inputCls} placeholder="QT2026/05-001" />
        </Field>
        <Field label="วันที่">
          <input type="date" value={form.docDate} onChange={e => update('docDate', e.target.value)} className={inputCls} />
        </Field>
      </div>

      {form.type === 'quotation' && (
        <Field label="ใช้ได้ถึง" hint="ใบเสนอราคามีอายุการใช้งาน">
          <input type="date" value={form.validUntil} onChange={e => update('validUntil', e.target.value)} className={inputCls} />
        </Field>
      )}

      {/* Customer */}
      <div className="mt-4 pt-4 border-t border-stone-200">
        <Field label="ลูกค้า (เลือกจากรายการหรือกรอกใหม่)">
          <select value={form.customerId} onChange={e => selectCustomer(e.target.value)} className={inputCls}>
            <option value="">-- กรอกข้อมูลใหม่ --</option>
            {customers.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
        </Field>
        <Field label="ชื่อลูกค้า">
          <input value={form.customerName} onChange={e => update('customerName', e.target.value)} className={inputCls} placeholder="คุณ..." />
        </Field>
        <Field label="เบอร์โทร">
          <input value={form.customerPhone} onChange={e => update('customerPhone', e.target.value)} className={inputCls} placeholder="08x-xxx-xxxx" />
        </Field>
        <Field label="ที่อยู่">
          <textarea value={form.customerAddress} onChange={e => update('customerAddress', e.target.value)} className={inputCls} rows={2} />
        </Field>
      </div>

      {/* Job link (optional) */}
      <Field label="ผูกกับงาน (optional - autofill ราคา)">
        <select value={form.jobId} onChange={e => selectJob(e.target.value)} className={inputCls}>
          <option value="">-- ไม่ระบุ --</option>
          {jobs.map(j => <option key={j.id} value={j.id}>{j.customer} ({j.date}) - {j.salePrice?.toLocaleString()} ฿</option>)}
        </select>
      </Field>

      {/* Items */}
      <div className="mt-4 pt-4 border-t border-stone-200">
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-bold text-stone-800">📋 รายการ</h3>
          <button type="button" onClick={addItem} className="text-sm bg-amber-100 hover:bg-amber-200 text-amber-700 px-2 py-1 rounded-lg flex items-center gap-1">
            <Plus className="w-3.5 h-3.5" /> เพิ่ม
          </button>
        </div>
        <div className="space-y-2">
          {form.items.map((item, idx) => (
            <div key={item.id} className="bg-stone-50 rounded-xl p-3 space-y-2">
              <div className="flex gap-2">
                <input
                  value={item.name}
                  onChange={e => updateItem(idx, 'name', e.target.value)}
                  placeholder={`รายการที่ ${idx + 1}`}
                  className="flex-1 px-2 py-1.5 border border-stone-300 rounded-lg text-sm"
                />
                {form.items.length > 1 && (
                  <button onClick={() => removeItem(idx)} className="p-1.5 hover:bg-red-50 rounded-lg">
                    <Trash2 className="w-4 h-4 text-red-400" />
                  </button>
                )}
              </div>
              <div className="grid grid-cols-3 gap-1.5">
                <div>
                  <label className="text-xs text-stone-500 ml-1">จำนวน (ชุด)</label>
                  <input type="number" value={item.qty} onChange={e => updateItem(idx, 'qty', e.target.value)}
                    placeholder="1" className="w-full px-2 py-1.5 border border-stone-300 rounded-lg text-sm mt-0.5" />
                </div>
                <div>
                  <label className="text-xs text-stone-500 ml-1">ราคา (บาท)</label>
                  <input type="number" value={item.unitPrice} onChange={e => updateItem(idx, 'unitPrice', e.target.value)}
                    placeholder="0" className="w-full px-2 py-1.5 border border-stone-300 rounded-lg text-sm mt-0.5" />
                </div>
                <div>
                  <label className="text-xs text-stone-500 ml-1">รวม</label>
                  <div className="px-2 py-1.5 bg-amber-50 border border-amber-200 rounded-lg text-sm text-right font-medium text-amber-700 mt-0.5">
                    {Number(item.amount || 0).toLocaleString()}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Totals */}
      <div className="mt-4 bg-stone-50 rounded-xl p-3 space-y-2">
        <div className="flex justify-between text-sm">
          <span className="text-stone-600">รวมทั้งหมด</span>
          <span className="font-mono font-medium">{form.subtotal.toLocaleString()} ฿</span>
        </div>
        <div className="flex justify-between items-center text-sm">
          <span className="text-stone-600">ส่วนลด</span>
          <input type="number" value={form.discount} onChange={e => updateDiscount(e.target.value)}
            className="px-2 py-1 border border-stone-300 rounded-lg text-right w-32 text-sm" placeholder="0" />
        </div>
        <div className="border-t border-stone-300 pt-2 flex justify-between items-center">
          <span className="font-bold text-stone-800">ยอดสุทธิ</span>
          <span className="font-bold text-2xl text-amber-600">
            {Number(form.totalAmount || 0).toLocaleString()} ฿
          </span>
        </div>
      </div>

      {/* เงินมัดจำ (เฉพาะใบเสนอราคา) */}
      {form.type === 'quotation' && (
        <div className="mt-4 bg-blue-50 border border-blue-200 rounded-xl p-3">
          <label className="block text-sm font-medium text-blue-700 mb-2">💳 เงินมัดจำ</label>
          
          {/* Input ตัวเลขเงินมัดจำตรงๆ */}
          <div className="bg-white rounded-lg p-2 mb-2">
            <div className="flex items-center gap-2">
              <input
                type="number"
                value={form.depositAmount || 0}
                onChange={e => {
                  const amt = Number(e.target.value) || 0;
                  const pct = form.totalAmount > 0 ? Math.round((amt / form.totalAmount) * 100) : 0;
                  setForm({...form, depositAmount: amt, depositPercent: pct});
                }}
                placeholder="0"
                className="flex-1 px-3 py-2 border-2 border-blue-300 rounded-lg text-lg font-bold text-right text-blue-700 focus:outline-none focus:border-blue-500"
              />
              <span className="text-blue-700 font-medium">฿</span>
            </div>
            <div className="text-xs text-stone-500 mt-1 text-right">
              คิดเป็น {form.depositPercent || 0}% ของยอดสุทธิ {Number(form.totalAmount || 0).toLocaleString()} ฿
            </div>
          </div>

          {/* Quick % buttons */}
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs text-stone-500">เลือกแบบเร็ว:</span>
            <div className="flex gap-1 flex-wrap">
              {[0, 30, 50, 70, 100].map(pct => {
                const calcAmt = Math.round(form.totalAmount * pct / 100);
                return (
                  <button
                    key={pct}
                    type="button"
                    onClick={() => setForm({...form, depositPercent: pct, depositAmount: calcAmt})}
                    className={`px-3 py-1 rounded-lg text-xs font-medium transition-all ${
                      Number(form.depositPercent) === pct
                        ? 'bg-blue-500 text-white'
                        : 'bg-white border border-blue-200 text-blue-700 hover:bg-blue-100'
                    }`}
                  >
                    {pct === 0 ? 'ไม่มี' : pct === 100 ? 'จ่ายครบ' : `${pct}%`}
                  </button>
                );
              })}
            </div>
          </div>

          {/* แสดงสรุป */}
          {Number(form.depositAmount || 0) > 0 && Number(form.depositAmount || 0) < Number(form.totalAmount || 0) && (
            <div className="bg-white rounded-lg p-2 grid grid-cols-2 gap-2 text-xs">
              <div className="bg-amber-50 rounded p-1.5 border border-amber-200">
                <div className="text-stone-500">มัดจำ</div>
                <div className="font-bold text-amber-700">{Number(form.depositAmount).toLocaleString()} ฿</div>
              </div>
              <div className="bg-stone-50 rounded p-1.5 border border-stone-200">
                <div className="text-stone-500">คงเหลือ</div>
                <div className="font-bold text-stone-700">{(form.totalAmount - form.depositAmount).toLocaleString()} ฿</div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Payment Terms */}
      <Field label="เงื่อนไขการชำระเงิน (เพิ่มเติม)" hint="ระบุรายละเอียดเพิ่มได้">
        <textarea value={form.paymentTerms} onChange={e => update('paymentTerms', e.target.value)}
          className={inputCls} rows={2}
          placeholder="เช่น โอนภายใน 7 วันหลังได้รับใบแจ้งหนี้" />
      </Field>

      {form.type === 'quotation' && (
        <Field label="การรับประกัน">
          <textarea value={form.warrantyText} onChange={e => update('warrantyText', e.target.value)}
            className={inputCls} rows={3} placeholder="แผงโซล่าเซลล์: 25 ปี..." />
        </Field>
      )}

      <Field label="หมายเหตุเพิ่มเติม">
        <textarea value={form.notes} onChange={e => update('notes', e.target.value)} className={inputCls} rows={2} />
      </Field>

      {submitError && (
        <div id="doc-error-msg" className="bg-rose-100 border border-rose-300 text-rose-700 px-3 py-2 rounded-lg text-sm flex items-center gap-2 mt-3">
          <AlertCircle className="w-4 h-4 flex-shrink-0" /> {submitError}
        </div>
      )}

      <div className="flex gap-2 mt-4 sticky bottom-0 bg-white pt-2 -mx-4 px-4 pb-1 border-t border-stone-100">
        <button onClick={onClose}
          className="flex-1 px-4 py-3 bg-stone-100 hover:bg-stone-200 text-stone-700 rounded-xl font-medium transition-colors">
          ยกเลิก
        </button>
        <button onClick={handleSubmit}
          className="flex-[2] bg-amber-500 hover:bg-amber-600 text-white py-3 rounded-xl font-medium flex items-center justify-center gap-2">
          <Save className="w-4 h-4" /> {isEdit ? 'อัพเดทเอกสาร' : 'สร้างเอกสาร'}
        </button>
      </div>
    </Modal>
  );
}

// ============== DOCUMENT PREVIEW (พิมพ์/Export PDF) ==============
function DocumentPreview({ doc, companyInfo, fmt, onClose }) {
  const typeLabel = {
    quotation: 'ใบเสนอราคา',
    invoice: 'ใบแจ้งหนี้',
    'receipt-deposit': 'ใบเสร็จรับเงิน (มัดจำ)',
    'receipt-final': 'ใบเสร็จรับเงิน (เต็มจำนวน)',
    receipt: 'ใบเสร็จรับเงิน',
  }[doc.type] || 'เอกสาร';
  const typeLabelEn = {
    quotation: 'Quotation',
    invoice: 'Invoice',
    'receipt-deposit': 'Deposit Receipt',
    'receipt-final': 'Final Receipt',
    receipt: 'Receipt',
  }[doc.type] || 'Document';

  const formatThaiDate = (s) => {
    if (!s) return '-';
    const d = new Date(s);
    const day = d.getDate();
    const months = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
                    'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'];
    return `${day} ${months[d.getMonth()]} ${d.getFullYear() + 543}`;
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="fixed inset-0 bg-black/70 z-50 flex items-start justify-center overflow-y-auto print:bg-white print:p-0 print:overflow-visible"
         style={{ 
           paddingTop: 'calc(70px + env(safe-area-inset-top))',
           paddingBottom: 'max(20px, env(safe-area-inset-bottom))',
           paddingLeft: '12px',
           paddingRight: '12px',
         }}>
      {/* Print styles */}
      <style>{`
        @media print {
          body * { visibility: hidden; }
          .print-area, .print-area * { visibility: visible; }
          .print-area { 
            position: absolute; 
            left: 0; 
            top: 0; 
            width: 100%; 
            font-size: 11px;
            line-height: 1.3;
          }
          .print-area h1 { font-size: 22px !important; }
          .print-area h2 { font-size: 16px !important; }
          .print-area h3 { font-size: 13px !important; }
          .print-area .mb-4 { margin-bottom: 8px !important; }
          .print-area .mb-3 { margin-bottom: 6px !important; }
          .print-area .p-4 { padding: 8px !important; }
          .print-area .p-3 { padding: 6px !important; }
          .print-area .py-3 { padding-top: 6px !important; padding-bottom: 6px !important; }
          .no-print { display: none !important; }
          @page { 
            size: A4 portrait; 
            margin: 0.7cm; 
          }
          /* ป้องกันแบ่งหน้ากลาง section */
          .print-area > div { page-break-inside: avoid; }
          /* ใช้ background colors ตอนพิมพ์ */
          * {
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
          }
        }
      `}</style>

      {/* Top Action Bar - safe-area for iPhone notch */}
      <div className="fixed top-0 left-0 right-0 bg-stone-900 text-white z-50 flex items-center justify-between gap-2 no-print print:hidden shadow-lg"
           style={{ 
             paddingTop: 'max(12px, env(safe-area-inset-top))',
             paddingBottom: '12px',
             paddingLeft: 'max(12px, env(safe-area-inset-left))',
             paddingRight: 'max(12px, env(safe-area-inset-right))',
           }}>
        <button onClick={onClose} 
          className="bg-stone-700 hover:bg-stone-600 active:bg-stone-500 text-white px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-1.5 flex-shrink-0"
          style={{ minHeight: '44px' }} 
          title="ปิด">
          ← กลับ
        </button>
        <div className="text-xs sm:text-sm flex-1 min-w-0 truncate">
          <span className="opacity-60">ตัวอย่าง:</span> <span className="font-medium">{doc.docNumber}</span>
        </div>
        <button onClick={handlePrint} 
          className="bg-amber-500 hover:bg-amber-600 active:bg-amber-700 text-white px-4 py-2 rounded-lg text-sm flex items-center gap-1.5 font-medium flex-shrink-0"
          style={{ minHeight: '44px' }}>
          🖨️ <span className="hidden sm:inline">พิมพ์ / </span>PDF
        </button>
      </div>

      {/* Floating Back Button (มุมล่างขวา - กันกรณี scroll ลึก) */}
      <button onClick={onClose}
        className="fixed bg-stone-800 hover:bg-stone-700 active:bg-stone-900 text-white rounded-full shadow-2xl flex items-center justify-center z-50 no-print print:hidden transition-transform active:scale-95"
        style={{ 
          bottom: 'max(20px, env(safe-area-inset-bottom))',
          right: 'max(20px, env(safe-area-inset-right))',
          width: '56px',
          height: '56px',
        }}
        title="ปิด">
        <span className="text-2xl">✕</span>
      </button>

      {/* Document */}
      <div className="bg-white shadow-xl mb-8 print:mt-0 print:shadow-none print-area max-w-full" 
           style={{ 
             width: '210mm', 
             maxWidth: '100%',
             minHeight: '297mm', 
             fontFamily: "'Sarabun', sans-serif" 
           }}>
        <div className="p-6 print:p-5">
          {/* Header */}
          <div className="flex items-start justify-between pb-3 border-b-4 border-amber-500 mb-4">
            <div className="flex items-center gap-3">
              <img src="icons/icon-192.png" alt="DD" className="w-16 h-16" />
              <div>
                <h1 className="text-3xl font-bold text-stone-800" style={{ letterSpacing: '0.02em' }}>
                  {companyInfo.name || 'D.D. Solution'}
                </h1>
                <p className="text-sm text-stone-500">{companyInfo.subName || 'Daddy Solution'}</p>
                {companyInfo.tagline && <p className="text-xs text-stone-500 mt-1">{companyInfo.tagline}</p>}
              </div>
            </div>
            <div className="text-right">
              <h2 className="text-2xl font-bold text-amber-600">{typeLabel}</h2>
              <p className="text-sm text-stone-500 italic">{typeLabelEn}</p>
              <div className="mt-2 inline-block bg-stone-100 px-3 py-1 rounded">
                <p className="text-xs text-stone-500">เลขที่</p>
                <p className="font-mono font-bold text-stone-800">{doc.docNumber}</p>
              </div>
            </div>
          </div>

          {/* Date Info */}
          <div className="grid grid-cols-2 gap-4 mb-6 text-sm">
            <div>
              <span className="text-stone-500">วันที่: </span>
              <span className="font-medium">{formatThaiDate(doc.docDate)}</span>
            </div>
            {doc.type === 'quotation' && doc.validUntil && (
              <div>
                <span className="text-stone-500">ใช้ได้ถึง: </span>
                <span className="font-medium">{formatThaiDate(doc.validUntil)}</span>
              </div>
            )}
          </div>

          {/* Customer Info */}
          <div className="grid grid-cols-2 gap-6 mb-6">
            <div className="border border-stone-200 rounded-lg p-4">
              <p className="text-xs text-stone-500 mb-1 uppercase">จาก / From</p>
              <p className="font-bold text-stone-800">{companyInfo.name}</p>
              {companyInfo.subName && <p className="text-sm text-stone-600">{companyInfo.subName}</p>}
              {companyInfo.address && <p className="text-xs text-stone-500 mt-1 whitespace-pre-line">{companyInfo.address}</p>}
              {companyInfo.phone && <p className="text-xs text-stone-600 mt-1">📞 {companyInfo.phone}</p>}
              {companyInfo.lineId && <p className="text-xs text-stone-600">💬 LINE: {companyInfo.lineId}</p>}
              {companyInfo.email && <p className="text-xs text-stone-600">✉️ {companyInfo.email}</p>}
              {companyInfo.taxId && <p className="text-xs text-stone-600">เลขผู้เสียภาษี: {companyInfo.taxId}</p>}
            </div>
            <div className="border border-stone-200 rounded-lg p-4">
              <p className="text-xs text-stone-500 mb-1 uppercase">ถึง / To</p>
              <p className="font-bold text-stone-800">{doc.customerName}</p>
              {doc.customerAddress && <p className="text-xs text-stone-600 mt-1 whitespace-pre-line">{doc.customerAddress}</p>}
              {doc.customerPhone && <p className="text-xs text-stone-600 mt-1">📞 {doc.customerPhone}</p>}
            </div>
          </div>

          {/* Items Table */}
          <table className="w-full mb-3 border-collapse">
            <thead>
              <tr className="bg-stone-800 text-white">
                <th className="text-left px-2 py-1.5 text-xs font-medium" style={{ width: '36px' }}>ลำดับ</th>
                <th className="text-left px-2 py-1.5 text-xs font-medium">รายการ</th>
                <th className="text-center px-2 py-1.5 text-xs font-medium" style={{ width: '70px' }}>จำนวน</th>
                <th className="text-right px-2 py-1.5 text-xs font-medium" style={{ width: '110px' }}>ราคา (บาท)</th>
              </tr>
            </thead>
            <tbody>
              {doc.items.map((item, idx) => (
                <tr key={item.id} className="border-b border-stone-200">
                  <td className="px-2 py-1.5 text-xs text-center">{idx + 1}</td>
                  <td className="px-2 py-1.5 text-xs">{item.name}</td>
                  <td className="px-2 py-1.5 text-xs text-center">{item.qty}</td>
                  <td className="px-2 py-1.5 text-xs text-right font-mono font-medium">{Number(item.amount || 0).toLocaleString()}</td>
                </tr>
              ))}
              {/* Empty rows minimal */}
              {[...Array(Math.max(0, 2 - doc.items.length))].map((_, i) => (
                <tr key={`empty-${i}`} className="border-b border-stone-100"><td colSpan={4} className="px-2 py-1.5 text-xs">&nbsp;</td></tr>
              ))}
            </tbody>
          </table>

          {/* Totals */}
          <div className="flex justify-end mb-6">
            <table className="w-1/2">
              <tbody>
                <tr>
                  <td className="p-2 text-sm text-stone-600">รวมทั้งหมด</td>
                  <td className="p-2 text-sm text-right font-mono">{Number(doc.subtotal || 0).toLocaleString()} ฿</td>
                </tr>
                {Number(doc.discount || 0) > 0 && (
                  <tr>
                    <td className="p-2 text-sm text-stone-600">ส่วนลด</td>
                    <td className="p-2 text-sm text-right font-mono text-rose-600">- {Number(doc.discount).toLocaleString()} ฿</td>
                  </tr>
                )}
                <tr className="border-t-2 border-stone-800 bg-amber-50">
                  <td className="p-2 font-bold text-stone-800">ยอดสุทธิ</td>
                  <td className="p-2 text-right font-mono font-bold text-xl text-amber-600">
                    {Number(doc.totalAmount || 0).toLocaleString()} ฿
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* === 🛡️ รับประกัน + 🔧 สเปค + 🎁 ของแถม (Compact 3-column for A4) === */}
          {doc.type === 'quotation' && (companyInfo?.warranty?.length > 0 || companyInfo?.specs?.length > 0 || companyInfo?.freebies?.filter(f => f.active !== false).length > 0) && (
            <div className="mb-3 grid grid-cols-3 gap-2 text-[10px] leading-tight">
              {/* รับประกัน */}
              {companyInfo?.warranty?.length > 0 && (
                <div className="border border-emerald-300 rounded overflow-hidden">
                  <div className="bg-emerald-500 text-white px-2 py-1 text-[10px] font-bold">🛡️ รับประกัน</div>
                  <div className="p-1.5 space-y-0.5">
                    {companyInfo.warranty.map(w => (
                      <div key={w.id} className="flex items-center justify-between gap-1">
                        <span className="text-stone-700 truncate">{w.icon} {w.label}</span>
                        <span className="font-bold text-emerald-700 whitespace-nowrap">
                          {w.years >= 99 ? 'ตลอด' : `${w.years} ปี`}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {/* สเปค */}
              {companyInfo?.specs?.length > 0 && (
                <div className="border border-stone-300 rounded overflow-hidden">
                  <div className="bg-stone-700 text-white px-2 py-1 text-[10px] font-bold">🔧 สเปค</div>
                  <div className="p-1.5 space-y-0.5">
                    {companyInfo.specs.map(s => (
                      <div key={s.id} className="flex items-start gap-1">
                        <span className="text-emerald-600 font-bold">✓</span>
                        <div className="flex-1 min-w-0">
                          <div className="font-medium text-stone-700 truncate">{s.label}</div>
                          <div className="text-stone-500 text-[9px] leading-tight">{s.value}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {/* ของแถม */}
              {companyInfo?.freebies?.filter(f => f.active !== false).length > 0 && (
                <div className="border-2 border-rose-300 rounded overflow-hidden bg-gradient-to-br from-rose-50 to-amber-50">
                  <div className="bg-gradient-to-r from-rose-500 to-pink-500 text-white px-2 py-1 text-[10px] font-bold">🎁 ของแถมฟรี!</div>
                  <div className="p-1.5 space-y-0.5">
                    {companyInfo.freebies.filter(f => f.active !== false).map(f => (
                      <div key={f.id} className="flex items-center gap-1">
                        <span>{f.icon}</span>
                        <span className="text-stone-700 flex-1 truncate">{f.label}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Deposit Info (เฉพาะใบเสนอราคา) */}
          {doc.type === 'quotation' && Number(doc.depositAmount || 0) > 0 && Number(doc.depositAmount || 0) < Number(doc.totalAmount || 0) && (
            <div className="border-l-4 border-amber-500 bg-amber-50 p-3 mb-4">
              <p className="text-xs font-bold text-amber-700 mb-2">💳 เงื่อนไขการชำระเงิน</p>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div className="bg-white rounded-lg p-2 border border-amber-200">
                  <div className="text-xs text-stone-500">เงินมัดจำ{doc.depositPercent ? ` (${doc.depositPercent}%)` : ''}</div>
                  <div className="font-bold text-amber-700 text-base">
                    {Number(doc.depositAmount).toLocaleString()} ฿
                  </div>
                  <div className="text-xs text-stone-500 mt-0.5">ตอนยืนยันสั่งซื้อ</div>
                </div>
                <div className="bg-white rounded-lg p-2 border border-amber-200">
                  <div className="text-xs text-stone-500">ส่วนที่เหลือ{doc.depositPercent ? ` (${100 - doc.depositPercent}%)` : ''}</div>
                  <div className="font-bold text-stone-700 text-base">
                    {(doc.totalAmount - doc.depositAmount).toLocaleString()} ฿
                  </div>
                  <div className="text-xs text-stone-500 mt-0.5">หลังติดตั้งเสร็จ</div>
                </div>
              </div>
            </div>
          )}

          {doc.paymentTerms && (
            <div className="border-l-4 border-blue-500 bg-blue-50 p-3 mb-4">
              <p className="text-xs font-bold text-blue-700 mb-1">📋 เงื่อนไขเพิ่มเติม</p>
              <pre className="text-xs text-blue-800 whitespace-pre-wrap font-sans">{doc.paymentTerms}</pre>
            </div>
          )}

          {/* Bank Info */}
          {companyInfo.bankAccounts && companyInfo.bankAccounts.length > 0 && (
            <div className="bg-stone-50 border border-stone-200 rounded-lg p-3 mb-4">
              <p className="text-xs font-bold text-stone-700 mb-2">📲 ชำระโดยโอนเข้าบัญชี</p>
              {companyInfo.bankAccounts.map((acc, i) => (
                <div key={i} className="text-xs text-stone-600">
                  • <span className="font-medium">{acc.bank}</span> เลขที่ <span className="font-mono">{acc.number}</span> ชื่อ <span className="font-medium">{acc.name}</span>
                </div>
              ))}
            </div>
          )}

          {/* Notes */}
          {doc.notes && (
            <div className="text-xs text-stone-500 italic mb-4">
              <p className="font-bold mb-1">หมายเหตุ:</p>
              <pre className="whitespace-pre-wrap font-sans">{doc.notes}</pre>
            </div>
          )}

          {/* Signatures */}
          <div className="grid grid-cols-2 gap-8 mt-12 pt-4">
            <div className="text-center">
              <div className="h-12 border-b border-stone-400"></div>
              <p className="text-xs text-stone-500 mt-1">
                ({doc.type === 'receipt' ? 'ผู้รับเงิน' : 'ผู้เสนอราคา'})
              </p>
              <p className="text-xs text-stone-400">วันที่ ___________________</p>
            </div>
            <div className="text-center">
              <div className="h-12 border-b border-stone-400"></div>
              <p className="text-xs text-stone-500 mt-1">(ผู้รับ / ลูกค้า)</p>
              <p className="text-xs text-stone-400">วันที่ ___________________</p>
            </div>
          </div>

          {/* Footer */}
          <div className="text-center text-xs text-stone-400 mt-8 pt-4 border-t border-stone-200">
            ขอบคุณที่ไว้วางใจ {companyInfo.name} · เอกสารสร้างโดยระบบอัตโนมัติ
          </div>
        </div>
      </div>
    </div>
  );
}

// ============== COMPANY SETTINGS MODAL ==============
function CompanySettingsModal({ companyInfo, onClose, onSave }) {
  const [form, setForm] = useState(companyInfo || DEFAULT_COMPANY_INFO);
  const update = (f, v) => setForm({...form, [f]: v});

  const updateBank = (idx, field, value) => {
    const newBanks = [...(form.bankAccounts || [])];
    newBanks[idx] = { ...newBanks[idx], [field]: value };
    setForm({...form, bankAccounts: newBanks});
  };

  const addBank = () => {
    setForm({...form, bankAccounts: [...(form.bankAccounts || []), { bank: '', number: '', name: '' }]});
  };

  const removeBank = (idx) => {
    setForm({...form, bankAccounts: form.bankAccounts.filter((_, i) => i !== idx)});
  };

  return (
    <Modal title="⚙️ ข้อมูลบริษัท" onClose={onClose} wide>
      <p className="text-sm text-stone-500 mb-4">ข้อมูลนี้จะแสดงบนใบเสนอราคา / ใบแจ้งหนี้ / ใบเสร็จ</p>

      <Field label="ชื่อบริษัท">
        <input value={form.name || ''} onChange={e => update('name', e.target.value)} className={inputCls} placeholder="D.D. Solution" />
      </Field>
      <Field label="ชื่อรอง / Sub-name">
        <input value={form.subName || ''} onChange={e => update('subName', e.target.value)} className={inputCls} placeholder="Daddy Solution" />
      </Field>
      <Field label="คำอธิบายธุรกิจ">
        <input value={form.tagline || ''} onChange={e => update('tagline', e.target.value)} className={inputCls} placeholder="ติดตั้งโซล่าเซลล์ครบวงจร" />
      </Field>
      <Field label="ที่อยู่บริษัท">
        <textarea value={form.address || ''} onChange={e => update('address', e.target.value)} className={inputCls} rows={2} placeholder="ที่อยู่..." />
      </Field>
      <Field label="เบอร์โทรศัพท์">
        <input value={form.phone || ''} onChange={e => update('phone', e.target.value)} className={inputCls} placeholder="089-xxx-xxxx" />
      </Field>
      <Field label="LINE ID">
        <input value={form.lineId || ''} onChange={e => update('lineId', e.target.value)} className={inputCls} placeholder="@ddsolution" />
      </Field>
      <Field label="Email">
        <input value={form.email || ''} onChange={e => update('email', e.target.value)} className={inputCls} type="email" />
      </Field>
      <Field label="เลขประจำตัวผู้เสียภาษี (ถ้ามี)">
        <input value={form.taxId || ''} onChange={e => update('taxId', e.target.value)} className={inputCls} />
      </Field>

      {/* Bank Accounts */}
      <div className="mt-4 pt-4 border-t border-stone-200">
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-bold text-stone-800">💳 บัญชีรับโอน</h3>
          <button type="button" onClick={addBank} className="text-sm bg-amber-100 hover:bg-amber-200 text-amber-700 px-2 py-1 rounded-lg flex items-center gap-1">
            <Plus className="w-3.5 h-3.5" /> เพิ่ม
          </button>
        </div>
        <div className="space-y-2">
          {(form.bankAccounts || []).map((acc, idx) => (
            <div key={idx} className="bg-stone-50 rounded-xl p-3 grid grid-cols-12 gap-1.5 items-center">
              <input value={acc.bank} onChange={e => updateBank(idx, 'bank', e.target.value)}
                placeholder="ธนาคาร" className="col-span-3 px-2 py-1.5 border border-stone-300 rounded-lg text-sm" />
              <input value={acc.number} onChange={e => updateBank(idx, 'number', e.target.value)}
                placeholder="เลขบัญชี" className="col-span-4 px-2 py-1.5 border border-stone-300 rounded-lg text-sm" />
              <input value={acc.name} onChange={e => updateBank(idx, 'name', e.target.value)}
                placeholder="ชื่อบัญชี" className="col-span-4 px-2 py-1.5 border border-stone-300 rounded-lg text-sm" />
              <button onClick={() => removeBank(idx)} className="col-span-1 p-1.5 hover:bg-red-50 rounded-lg flex items-center justify-center">
                <Trash2 className="w-4 h-4 text-red-400" />
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Default warranty */}
      <Field label="การรับประกัน (default)" hint="แต่ละบรรทัด = 1 ข้อ">
        <textarea
          value={(form.defaultWarranty || []).join('\n')}
          onChange={e => update('defaultWarranty', e.target.value.split('\n').filter(Boolean))}
          className={inputCls} rows={4}
          placeholder="แผงโซล่าเซลล์: 25 ปี" />
      </Field>

      {/* Sales Settings */}
      <div className="bg-gradient-to-br from-amber-50 to-orange-50 border border-amber-200 rounded-xl p-3 my-3">
        <h3 className="font-bold text-amber-800 text-sm mb-2">💰 ตั้งค่าการเสนอขาย</h3>
        <p className="text-xs text-stone-600 mb-3">ปรับ % กำไรที่บวกจากต้นทุนของแต่ละขนาดงาน</p>
        
        <div className="grid grid-cols-3 gap-2 mb-3">
          <div>
            <label className="text-xs text-stone-600">เล็ก (&lt;5kW)</label>
            <div className="flex items-center gap-1">
              <input type="number" 
                value={form.margins?.small ?? 25}
                onChange={e => update('margins', {...(form.margins || {}), small: Number(e.target.value) || 0})}
                className="w-full px-2 py-1.5 border border-stone-300 rounded-lg text-sm text-right" />
              <span className="text-stone-600 text-sm">%</span>
            </div>
          </div>
          <div>
            <label className="text-xs text-stone-600">กลาง (5-10kW)</label>
            <div className="flex items-center gap-1">
              <input type="number"
                value={form.margins?.medium ?? 20}
                onChange={e => update('margins', {...(form.margins || {}), medium: Number(e.target.value) || 0})}
                className="w-full px-2 py-1.5 border border-stone-300 rounded-lg text-sm text-right" />
              <span className="text-stone-600 text-sm">%</span>
            </div>
          </div>
          <div>
            <label className="text-xs text-stone-600">ใหญ่ (&gt;10kW)</label>
            <div className="flex items-center gap-1">
              <input type="number"
                value={form.margins?.large ?? 15}
                onChange={e => update('margins', {...(form.margins || {}), large: Number(e.target.value) || 0})}
                className="w-full px-2 py-1.5 border border-stone-300 rounded-lg text-sm text-right" />
              <span className="text-stone-600 text-sm">%</span>
            </div>
          </div>
        </div>
        
        <div>
          <label className="text-xs text-stone-600">💼 ค่าติดตั้ง (% ของวัสดุ)</label>
          <div className="flex items-center gap-1">
            <input type="number"
              value={form.installCostPct ?? 10}
              onChange={e => update('installCostPct', Number(e.target.value) || 0)}
              className="w-full px-2 py-1.5 border border-stone-300 rounded-lg text-sm text-right" />
            <span className="text-stone-600 text-sm">%</span>
          </div>
          <p className="text-xs text-stone-500 mt-1">ระบบจะบวก % นี้เข้ากับต้นทุนวัสดุก่อนคำนวณ margin</p>
        </div>
        
        <div className="bg-white rounded-lg p-2 mt-3 text-xs">
          <strong>ตัวอย่าง:</strong> ต้นทุนวัสดุ 100,000 ฿ + ติดตั้ง {form.installCostPct ?? 10}% = {(100000 * (1 + (form.installCostPct ?? 10)/100)).toLocaleString()} ฿ → margin {form.margins?.medium ?? 20}% = ขาย {Math.round(100000 * (1 + (form.installCostPct ?? 10)/100) * (1 + (form.margins?.medium ?? 20)/100)).toLocaleString()} ฿
        </div>
      </div>

      <button onClick={() => onSave(form)} className="w-full bg-amber-500 hover:bg-amber-600 text-white py-3 rounded-xl font-medium mt-4 flex items-center justify-center gap-2">
        <Save className="w-4 h-4" /> บันทึก
      </button>
    </Modal>
  );
}

// ============== RENDER APP ==============
try {
  const root = ReactDOM.createRoot(document.getElementById('root'));
  root.render(React.createElement(App));
  // บอก error catcher ว่า render สำเร็จแล้ว (กัน false alarm จอขาว)
  window.__appLoaded = true;
  // ซ่อน splash เมื่อ render เสร็จ
  setTimeout(() => { const s = document.getElementById('splash'); if (s) s.style.display = 'none'; }, 100);
} catch (err) {
  window.__appLoaded = false;
  if (window.onerror) window.onerror(err.message, 'app.js', 0, 0, err);
  throw err;
}
