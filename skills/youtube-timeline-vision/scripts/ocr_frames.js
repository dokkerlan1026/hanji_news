#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const Tesseract = require('/home/andy/.openclaw/workspace/.local/lib/youtube-vision/node_modules/tesseract.js');

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error('Usage: node ocr_frames.js <frames_dir> <output_json>');
    process.exit(1);
  }

  const [framesDir, outputJson] = args;
  const files = fs.readdirSync(framesDir)
    .filter(f => /\.(jpg|jpeg|png)$/i.test(f))
    .sort();

  const results = [];
  for (const file of files) {
    const imagePath = path.join(framesDir, file);
    const { data } = await Tesseract.recognize(imagePath, 'eng');
    const text = (data.text || '').replace(/\s+/g, ' ').trim();
    results.push({ file, text });
  }

  fs.writeFileSync(outputJson, JSON.stringify(results, null, 2));
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
