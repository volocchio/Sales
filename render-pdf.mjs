import puppeteer from 'puppeteer';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const inFile = process.argv[2] || path.join(__dirname, 'atlas-comparison.html');
const outFile = process.argv[3] || path.join(__dirname, 'atlas-comparison.pdf');

const browser = await puppeteer.launch({
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
});

try {
  const page = await browser.newPage();
  const url = inFile.startsWith('http') ? inFile : 'file://' + path.resolve(inFile);
  await page.goto(url, { waitUntil: 'networkidle0' });

  await page.pdf({
    path: outFile,
    format: 'Letter',
    printBackground: true,
    margin: { top: '0.6in', right: '0.6in', bottom: '0.6in', left: '0.6in' },
  });

  console.log(outFile);
} finally {
  await browser.close();
}
