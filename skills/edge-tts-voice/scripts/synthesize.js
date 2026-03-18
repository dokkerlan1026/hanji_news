#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { EdgeTTS } = require('../node_modules/node-edge-tts');

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error('Usage: node synthesize.js <output.mp3> <text> [voice] [rate]');
    process.exit(1);
  }

  const output = path.resolve(args[0]);
  const text = args[1];
  const voice = args[2] || 'zh-TW-HsiaoChenNeural';
  const rate = args[3] || '+0%';

  fs.mkdirSync(path.dirname(output), { recursive: true });
  const tts = new EdgeTTS({ voice, lang: voice.startsWith('zh-TW') ? 'zh-TW' : 'zh-CN', rate });
  await tts.ttsPromise(text, output);
  console.log(output);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
