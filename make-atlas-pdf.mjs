import PDFDocument from 'pdfkit';
import fs from 'node:fs';

const outPath = process.argv[2] || 'atlas-comparison.pdf';

const rows = [
  { model:'CJ',  stockPayload:'1,730', atlasPayload:'2,052', stockClimb:'60+ min', atlasClimb:'≤32 min', stockAlt:'FL350', atlasAlt:'FL410', stockBurn:'900', atlasBurn:'600–650', stockRange:'1,100', atlasRange:'1,400' },
  { model:'CJ1', stockPayload:'1,730', atlasPayload:'2,052', stockClimb:'60+ min', atlasClimb:'≤32 min', stockAlt:'FL320', atlasAlt:'FL410', stockBurn:'900', atlasBurn:'600–650', stockRange:'1,099', atlasRange:'1,440' },
  { model:'CJ1+',stockPayload:'1,730', atlasPayload:'2,052', stockClimb:'60+ min', atlasClimb:'≤32 min', stockAlt:'FL350', atlasAlt:'FL410', stockBurn:'900', atlasBurn:'600–650', stockRange:'1,099', atlasRange:'1,520' },
  { model:'CJ2', stockPayload:'1,490', atlasPayload:'2,211', stockClimb:'40+ min', atlasClimb:'≤30 min', stockAlt:'FL400', atlasAlt:'FL450', stockBurn:'900', atlasBurn:'680–700', stockRange:'1,200', atlasRange:'1,650' },
  { model:'CJ2+',stockPayload:'1,270', atlasPayload:'1,591', stockClimb:'40+ min', atlasClimb:'≤30 min', stockAlt:'FL400', atlasAlt:'FL450', stockBurn:'920', atlasBurn:'680–700', stockRange:'1,200', atlasRange:'1,650' },
  { model:'CJ3', stockPayload:'2,325', atlasPayload:'2,645', stockClimb:'30 min',  atlasClimb:'≤25 min', stockAlt:'FL450', atlasAlt:'FL450', stockBurn:'875', atlasBurn:'680',     stockRange:'1,650', atlasRange:'1,900' },
  { model:'CJ3+',stockPayload:'2,135', atlasPayload:'2,455', stockClimb:'30 min',  atlasClimb:'≤25 min', stockAlt:'FL450', atlasAlt:'FL450', stockBurn:'875', atlasBurn:'680',     stockRange:'1,650', atlasRange:'1,900' },
  { model:'M2',  stockPayload:'1,500', atlasPayload:'1,823', stockClimb:'30 min',  atlasClimb:'≤22 min', stockAlt:'FL410', atlasAlt:'FL410', stockBurn:'790', atlasBurn:'690',     stockRange:'1,550', atlasRange:'1,700' },
];

const doc = new PDFDocument({ size: 'LETTER', margins: { top: 48, bottom: 48, left: 48, right: 48 } });
doc.pipe(fs.createWriteStream(outPath));

// Title
const title = 'Cessna Citation — Stock vs ATLAS (Quick Specs)';
doc.font('Helvetica-Bold').fontSize(16).fillColor('#0b1220').text(title);
doc.moveDown(0.25);
doc.font('Helvetica').fontSize(9).fillColor('#475569')
  .text('One-line-per-model summary • Metrics pulled from “Specs OEM vs ATLAS” PDFs in volocchio/Sales • Units as shown in source docs.');
doc.moveDown(1);

// Table layout
const pageWidth = doc.page.width - doc.page.margins.left - doc.page.margins.right;
const startX = doc.page.margins.left;
let y = doc.y;

const cols = [
  { key:'model',       label:'Model', w:0.07, align:'left' },
  { key:'stockPayload',label:'Stock\nPayload (lb)', w:0.10, align:'right' },
  { key:'atlasPayload',label:'ATLAS\nPayload (lb)', w:0.10, align:'right' },
  { key:'stockClimb',  label:'Stock\nTime-to-climb', w:0.10, align:'left' },
  { key:'atlasClimb',  label:'ATLAS\nTime-to-climb', w:0.10, align:'left' },
  { key:'stockAlt',    label:'Stock\nInit climb alt', w:0.09, align:'left' },
  { key:'atlasAlt',    label:'ATLAS\nInit climb alt', w:0.09, align:'left' },
  { key:'stockBurn',   label:'Stock\nBlock burn (pph)', w:0.10, align:'right' },
  { key:'atlasBurn',   label:'ATLAS\nBlock burn (pph)', w:0.10, align:'right' },
  { key:'stockRange',  label:'Stock\nRange (nm)', w:0.08, align:'right' },
  { key:'atlasRange',  label:'ATLAS\nRange (nm)', w:0.08, align:'right' },
];

const colWidths = cols.map(c => Math.round(c.w * pageWidth));
// Adjust rounding drift
let drift = pageWidth - colWidths.reduce((a,b)=>a+b,0);
colWidths[colWidths.length-1] += drift;

const rowH = 22;
const headH = 34;

function drawRow(cells, y, h, isHeader=false){
  let x = startX;
  // background
  if(isHeader){
    doc.save();
    doc.rect(startX, y, pageWidth, h).fill('#f8fafc');
    doc.restore();
  }

  // grid + text
  doc.lineWidth(0.5).strokeColor('#e2e8f0');
  for(let i=0;i<cols.length;i++){
    const w = colWidths[i];
    doc.rect(x, y, w, h).stroke();

    const { align } = cols[i];
    const text = String(cells[i] ?? '');

    doc.fillColor(isHeader ? '#0f172a' : '#0f172a');
    doc.font(isHeader ? 'Helvetica-Bold' : (i===0 ? 'Helvetica-Bold' : 'Helvetica'));
    doc.fontSize(isHeader ? 8.5 : 9);

    const pad = 4;
    const tx = x + pad;
    const tw = w - pad*2;

    doc.text(text, tx, y + 6, { width: tw, align, lineBreak: true });

    x += w;
  }
}

// Header
const headCells = cols.map(c => c.label);
drawRow(headCells, y, headH, true);
y += headH;

// Body rows
for(const r of rows){
  const cells = cols.map(c => r[c.key]);
  drawRow(cells, y, rowH, false);
  y += rowH;
}

doc.moveDown(1);
doc.font('Helvetica').fontSize(8.5).fillColor('#475569')
  .text('Note: “Block fuel burn / range” are shown in the source PDFs as representative profiles (e.g., MCT with reserve).');

doc.fontSize(8).text(`Generated (UTC): ${new Date().toISOString().replace('T',' ').replace(/\..*/,'')}`);

doc.end();

console.log(outPath);
