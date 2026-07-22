/* MiniPOV WiFi – Web Editor */

const ROWS = 8;
let width = 64;
let pixels = []; // width x 8, true = LED on
let paintValue = true;
let isPainting = false;

const gridWrap = document.getElementById('gridWrap');
const preview = document.getElementById('preview');
const ctx = preview.getContext('2d');
const statusEl = document.getElementById('status');
const messageEl = document.getElementById('message');

// 5x7 bitmap font (ASCII 32–126, simplified subset)
const FONT5x7 = {
  ' ': [0,0,0,0,0,0,0],
  '!': [4,4,4,4,0,4,0],
  'A': [0,14,17,17,31,17,17],
  'B': [0,30,17,30,17,17,30],
  'C': [0,14,17,16,16,17,14],
  'D': [0,30,17,17,17,17,30],
  'E': [0,31,16,30,16,16,31],
  'F': [0,31,16,30,16,16,16],
  'G': [0,14,17,16,19,17,14],
  'H': [0,17,17,31,17,17,17],
  'I': [0,14,4,4,4,4,14],
  'J': [0,7,2,2,2,18,12],
  'K': [0,17,18,20,24,18,17],
  'L': [0,16,16,16,16,16,31],
  'M': [0,17,27,21,17,17,17],
  'N': [0,17,25,21,19,17,17],
  'O': [0,14,17,17,17,17,14],
  'P': [0,30,17,17,30,16,16],
  'Q': [0,14,17,17,21,18,13],
  'R': [0,30,17,17,30,18,17],
  'S': [0,14,17,16,14,1,30],
  'T': [0,31,4,4,4,4,4],
  'U': [0,17,17,17,17,17,14],
  'V': [0,17,17,17,17,10,4],
  'W': [0,17,17,17,21,21,10],
  'X': [0,17,17,10,4,10,17],
  'Y': [0,17,17,10,4,4,4],
  'Z': [0,31,1,2,4,8,31],
  '0': [0,14,17,19,21,17,14],
  '1': [0,4,12,4,4,4,14],
  '2': [0,14,17,1,2,4,31],
  '3': [0,30,1,14,1,17,14],
  '4': [0,2,6,10,18,31,2],
  '5': [0,31,16,30,1,17,14],
  '6': [0,14,16,30,17,17,14],
  '7': [0,31,1,2,4,4,4],
  '8': [0,14,17,14,17,17,14],
  '9': [0,14,17,17,15,1,14],
};

function initPixels(w) {
  width = Math.max(8, Math.min(256, w));
  pixels = Array.from({ length: width }, () => Array(ROWS).fill(false));
}

function columnBytes() {
  const data = [];
  for (let x = 0; x < width; x++) {
    let byte = 0;
    for (let y = 0; y < ROWS; y++) {
      if (pixels[x][y]) byte |= 1 << y;
    }
    data.push(byte);
  }
  return data;
}

function fromColumnBytes(data) {
  width = data.length;
  initPixels(width);
  for (let x = 0; x < width; x++) {
    const byte = data[x];
    for (let y = 0; y < ROWS; y++) {
      pixels[x][y] = !!(byte & (1 << y));
    }
  }
}

function buildGrid() {
  gridWrap.innerHTML = '';
  const grid = document.createElement('div');
  grid.id = 'pixelGrid';
  grid.style.gridTemplateColumns = `repeat(${width}, 24px)`;

  for (let y = 0; y < ROWS; y++) {
    for (let x = 0; x < width; x++) {
      const cell = document.createElement('div');
      cell.className = 'pixel' + (pixels[x][y] ? ' on' : '');
      cell.dataset.x = x;
      cell.dataset.y = y;
      cell.addEventListener('mousedown', (e) => {
        e.preventDefault();
        isPainting = true;
        paintValue = !pixels[x][y];
        setPixel(x, y, paintValue);
      });
      cell.addEventListener('mouseenter', () => {
        if (isPainting) setPixel(x, y, paintValue);
      });
      grid.appendChild(cell);
    }
  }
  gridWrap.appendChild(grid);
}

function setPixel(x, y, on) {
  pixels[x][y] = on;
  const cell = gridWrap.querySelector(`.pixel[data-x="${x}"][data-y="${y}"]`);
  if (cell) cell.classList.toggle('on', on);
  drawPreviewStatic();
}

function drawPreviewStatic() {
  const scale = 4;
  preview.width = width * scale;
  preview.height = ROWS * scale;
  ctx.fillStyle = '#000';
  ctx.fillRect(0, 0, preview.width, preview.height);
  for (let x = 0; x < width; x++) {
    for (let y = 0; y < ROWS; y++) {
      if (pixels[x][y]) {
        ctx.fillStyle = '#ff2244';
        ctx.fillRect(x * scale, y * scale, scale - 1, scale - 1);
      }
    }
  }
}

let previewFrame = 0;
let previewTimer = null;

function startPreviewAnim() {
  if (previewTimer) clearInterval(previewTimer);
  const speed = parseInt(document.getElementById('speedInput').value, 10) || 1200;
  previewTimer = setInterval(() => {
    const scale = 4;
    preview.width = 64 * scale;
    preview.height = ROWS * scale;
    ctx.fillStyle = '#111';
    ctx.fillRect(0, 0, preview.width, preview.height);

    const offset = previewFrame % width;
    for (let sx = 0; sx < 64; sx++) {
      const px = (offset + sx) % width;
      for (let y = 0; y < ROWS; y++) {
        if (pixels[px][y]) {
          ctx.fillStyle = '#ff2244';
          ctx.fillRect(sx * scale, y * scale, scale - 1, scale - 1);
        }
      }
    }
    previewFrame++;
  }, Math.max(5, speed / 80));
}

function showMessage(text, type = '') {
  messageEl.textContent = text;
  messageEl.className = 'message ' + type;
}

function formatRemaining(ms) {
  const sec = Math.ceil(ms / 1000);
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return m > 0 ? `${m}:${String(s).padStart(2, '0')} min` : `${s} s`;
}

async function loadStatus() {
  try {
    const res = await fetch('/api/status');
    const data = await res.json();
    let txt = `Verbunden · ${data.ip} · ${data.width} Spalten`;
    if (data.wifiRemainingMs) {
      txt += ` · WiFi aus in ${formatRemaining(data.wifiRemainingMs)}`;
    }
    statusEl.textContent = txt;
    statusEl.className = 'status ok';
    document.getElementById('speedInput').value = data.columnUs;
    document.getElementById('displayEnabled').checked = data.display;
  } catch {
    statusEl.textContent = 'Nicht verbunden – FLASH-Taste drücken, dann MiniPOV-WiFi wählen';
    statusEl.className = 'status err';
  }
}

async function stopWifi() {
  try {
    await fetch('/api/wifi/stop', { method: 'POST' });
    showMessage('WiFi beendet – Batterie sparen. Zum Konfigurieren FLASH-Taste drücken.', 'success');
  } catch {
    showMessage('WiFi konnte nicht beendet werden.', 'error');
  }
}

async function loadPattern() {
  try {
    const res = await fetch('/api/pattern');
    const data = await res.json();
    fromColumnBytes(data.data);
    document.getElementById('widthInput').value = width;
    document.getElementById('speedInput').value = data.columnUs || 1200;
    buildGrid();
    drawPreviewStatic();
    showMessage('Muster vom Gerät geladen.', 'success');
  } catch {
    showMessage('Laden fehlgeschlagen.', 'error');
  }
}

async function savePattern() {
  const body = {
    width,
    columnUs: parseInt(document.getElementById('speedInput').value, 10) || 1200,
    data: columnBytes(),
  };
  try {
    const res = await fetch('/api/pattern', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error('save failed');
    showMessage('Muster gespeichert – jetzt schwenken!', 'success');
  } catch {
    showMessage('Speichern fehlgeschlagen.', 'error');
  }
}

async function setDisplayEnabled(enabled) {
  const form = new FormData();
  form.append('enabled', enabled ? '1' : '0');
  await fetch('/api/display', { method: 'POST', body: form });
}

function renderText() {
  const text = document.getElementById('textInput').value.toUpperCase();
  if (!text) return;

  const cols = [];
  const space = [0, 0, 0, 0, 0, 0, 0];

  for (const ch of text) {
    const glyph = FONT5x7[ch] || space;
    for (let row = 0; row < 7; row++) {
      if (!cols[row]) cols[row] = [];
      for (let bit = 0; bit < 5; bit++) {
        cols[row].push((glyph[row] >> (4 - bit)) & 1);
      }
      cols[row].push(0); // letter spacing
    }
  }

  // Transpose to column-major (POV format)
  const colCount = cols[0]?.length || 0;
  initPixels(colCount + 4);
  for (let x = 0; x < width; x++) {
    for (let y = 0; y < ROWS; y++) {
      pixels[x][y] = false;
    }
  }
  for (let x = 0; x < colCount; x++) {
    for (let y = 0; y < 7; y++) {
      pixels[x][y] = cols[y][x] === 1;
    }
  }

  document.getElementById('widthInput').value = width;
  buildGrid();
  drawPreviewStatic();
  showMessage(`Text „${text}" eingefügt.`, 'success');
}

function loadImage(file) {
  const img = new Image();
  img.onload = () => {
    const off = document.createElement('canvas');
    off.width = Math.min(256, Math.max(8, Math.round(img.width * (ROWS / img.height))));
    off.height = ROWS;
    const octx = off.getContext('2d');
    octx.drawImage(img, 0, 0, off.width, off.height);
    const id = octx.getImageData(0, 0, off.width, off.height);

    initPixels(off.width);
    for (let x = 0; x < off.width; x++) {
      for (let y = 0; y < ROWS; y++) {
        const i = (y * off.width + x) * 4;
        const lum = 0.299 * id.data[i] + 0.587 * id.data[i + 1] + 0.114 * id.data[i + 2];
        pixels[x][y] = lum > 128;
      }
    }
    document.getElementById('widthInput').value = width;
    buildGrid();
    drawPreviewStatic();
    showMessage('Bild importiert.', 'success');
  };
  img.src = URL.createObjectURL(file);
}

// Tabs
document.querySelectorAll('.tab').forEach((tab) => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach((t) => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach((c) => c.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById('tab-' + tab.dataset.tab).classList.add('active');
  });
});

document.getElementById('widthInput').addEventListener('change', (e) => {
  const w = parseInt(e.target.value, 10) || 64;
  const old = pixels;
  initPixels(w);
  for (let x = 0; x < Math.min(width, old.length); x++) {
    for (let y = 0; y < ROWS; y++) pixels[x][y] = old[x][y];
  }
  buildGrid();
  drawPreviewStatic();
});

document.getElementById('btnClear').addEventListener('click', () => {
  initPixels(width);
  buildGrid();
  drawPreviewStatic();
});

document.getElementById('btnInvert').addEventListener('click', () => {
  for (let x = 0; x < width; x++) {
    for (let y = 0; y < ROWS; y++) pixels[x][y] = !pixels[x][y];
  }
  buildGrid();
  drawPreviewStatic();
});

document.getElementById('btnRenderText').addEventListener('click', renderText);
document.getElementById('btnLoad').addEventListener('click', loadPattern);
document.getElementById('btnSave').addEventListener('click', savePattern);
document.getElementById('btnWifiOff').addEventListener('click', stopWifi);

document.getElementById('imageInput').addEventListener('change', (e) => {
  if (e.target.files[0]) loadImage(e.target.files[0]);
});

document.getElementById('displayEnabled').addEventListener('change', (e) => {
  setDisplayEnabled(e.target.checked);
});

document.getElementById('speedInput').addEventListener('change', startPreviewAnim);

document.addEventListener('mouseup', () => { isPainting = false; });

// Init
initPixels(64);
buildGrid();
drawPreviewStatic();
startPreviewAnim();
loadStatus();
loadPattern();
setInterval(loadStatus, 5000);
