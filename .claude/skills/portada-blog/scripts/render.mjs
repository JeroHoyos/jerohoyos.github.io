#!/usr/bin/env node
// HTML → PNG con Chrome/Edge sin ventana (sin dependencias).
//   node render.mjs <entrada.html> <salida.png> [--w 1600] [--h 686] [--espera 4000]
import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, statSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { pathToFileURL } from 'node:url';

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args.splice(i, 2)[1] : d; };
const W = +opt('--w', 1600), H = +opt('--h', 686), WAIT = +opt('--espera', 4000);
const [input, output] = args;
if (!input || !output) { console.error('uso: node render.mjs <entrada.html> <salida.png> [--w 1600] [--h 686]'); process.exit(1); }

const CANDIDATES = [
  process.env.CHROME,
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser',
].filter(Boolean);
const chrome = CANDIDATES.find(p => existsSync(p));
if (!chrome) { console.error('No encontré Chrome ni Edge. Indica la ruta con la variable CHROME.'); process.exit(1); }

const out = resolve(output);
mkdirSync(dirname(out), { recursive: true });
execFileSync(chrome, [
  '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--force-device-scale-factor=1',
  `--window-size=${W},${H}`, `--virtual-time-budget=${WAIT}`, '--default-background-color=050505ff',
  `--screenshot=${out}`, pathToFileURL(resolve(input)).href,
], { stdio: 'ignore', timeout: 60000 });

if (!existsSync(out) || statSync(out).size < 1000) { console.error('No se generó la imagen.'); process.exit(1); }
console.log(`✓ ${output} (${W}×${H}, ${Math.round(statSync(out).size / 1024)} KB)`);
