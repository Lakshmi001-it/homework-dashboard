"""
Homework Dashboard  -  © All rights reserved to LK
--------------------------------------------------
Run locally:
    pip install -r requirements.txt
    python app.py
Then open  http://localhost:8000
"""

from flask import Flask, Response

app = Flask(__name__)

INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Homework Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Noto+Sans:wght@400;600;700;800&family=Noto+Sans+Kannada:wght@400;700&family=Noto+Sans+Devanagari:wght@400;700&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<style>
:root{
  --ink:#1e1b4b; --muted:#64748b; --line:#e2e8f0;
  --indigo:#4f46e5; --violet:#7c3aed; --pink:#ec4899; --orange:#f97316;
  --emerald:#10b981; --sky:#0ea5e9; --red:#e11d48;
  --page-h:296mm; --page-margin:0.5mm;
}
*{box-sizing:border-box}
html,body{margin:0}
body{
  font-family:'Poppins',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
  color:var(--ink); min-height:100vh; display:flex; flex-direction:column;
  background:linear-gradient(135deg,#eef2ff 0%,#fdf2f8 50%,#ecfeff 100%);
  background-attachment:fixed;
}
button,input,select,textarea{font:inherit;color:inherit}
:focus-visible{outline:3px solid #a5b4fc;outline-offset:2px}

/* ---------- top bar ---------- */
.topbar{
  background:linear-gradient(100deg,var(--indigo),var(--violet) 55%,var(--pink));
  color:#fff; padding:18px 24px;
}
.topbar-in{max-width:1380px;margin:0 auto;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.logo{width:46px;height:46px;border-radius:14px;background:rgba(255,255,255,.2);display:grid;place-items:center;font-size:24px}
.topbar h1{margin:0;font-size:1.45rem;font-weight:700;letter-spacing:-.01em}
.topbar p{margin:2px 0 0;font-size:.82rem;opacity:.9}

/* ---------- layout ---------- */
.layout{
  max-width:1500px;margin:22px auto;padding:0 20px;width:100%;
  display:grid;grid-template-columns:minmax(420px,1.6fr) minmax(300px,1fr);gap:22px;align-items:start;flex:1;
}
@media (max-width:980px){.layout{grid-template-columns:1fr}}
.card{background:#fff;border-radius:20px;box-shadow:0 8px 30px rgba(79,70,229,.10);padding:18px}
.dash-head{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-bottom:14px}
.dash-head h2{margin:0;font-size:1.12rem}
.saved{font-size:.72rem;color:var(--emerald);font-weight:600}
.reset-row{display:flex;gap:8px}

.btn{
  border:0;border-radius:12px;padding:10px 16px;font-weight:600;font-size:.88rem;cursor:pointer;
  display:inline-flex;align-items:center;justify-content:center;gap:8px;transition:transform .12s,box-shadow .12s,filter .12s;
}
.btn:hover{transform:translateY(-1px);filter:brightness(1.05)}
.btn:disabled{opacity:.6;cursor:wait;transform:none}
.btn-sm{padding:7px 12px;font-size:.78rem;border-radius:10px}
.btn-ghost-orange{background:#fff7ed;color:#c2410c;border:1.5px solid #fdba74}
.btn-ghost-red{background:#fff1f2;color:#be123c;border:1.5px solid #fda4af}
.btn-add{background:linear-gradient(90deg,var(--sky),var(--indigo));color:#fff}
.btn-print{background:linear-gradient(90deg,var(--indigo),var(--violet));color:#fff;box-shadow:0 6px 16px rgba(79,70,229,.35)}
.btn-pdf{background:linear-gradient(90deg,#059669,var(--emerald));color:#fff;box-shadow:0 6px 16px rgba(16,185,129,.35)}
.btn-share{background:linear-gradient(90deg,var(--orange),var(--pink));color:#fff;box-shadow:0 6px 16px rgba(249,115,22,.35)}

.section{border:1.5px solid var(--line);border-radius:16px;padding:14px;margin-bottom:14px;position:relative;overflow:hidden}
.section::before{content:"";position:absolute;left:0;top:0;bottom:0;width:5px;background:var(--accent,var(--indigo))}
.s-school{--accent:var(--indigo)} .s-hw{--accent:var(--pink)} .s-notice{--accent:var(--orange)}
.section h3{margin:0 0 10px 4px;font-size:.95rem;color:var(--accent)}
.sec-head{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:10px}
.sec-head h3{margin:0 0 0 4px}

label.lbl{display:block;font-size:.74rem;font-weight:600;color:var(--muted);margin:0 0 4px 2px}
.req{color:var(--red)}
.field{margin-bottom:10px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
@media (max-width:420px){.grid2{grid-template-columns:1fr}}
input[type=text],input[type=date],select,textarea{
  width:100%;border:1.5px solid var(--line);border-radius:11px;background:#f8fafc;padding:9px 11px;font-size:.9rem;
  transition:border-color .15s,background .15s;
}
input:focus,select:focus,textarea:focus{border-color:var(--indigo);background:#fff;outline:none;box-shadow:0 0 0 3px rgba(99,102,241,.18)}
.invalid{border-color:var(--red)!important;background:#fff1f2!important}
.err{display:none;color:var(--red);font-size:.72rem;margin:3px 0 0 2px;font-weight:500}
.invalid + .err{display:block}
.date-wrap{display:flex;gap:6px}
.today-btn{border:1.5px solid var(--line);background:#fff;border-radius:11px;padding:0 10px;font-size:.74rem;font-weight:600;color:var(--indigo);cursor:pointer;white-space:nowrap}

.subj{
  display:grid;grid-template-columns:170px 1fr 42px;gap:8px;align-items:start;
  background:#fafafe;border:1.5px solid var(--line);border-left:5px solid var(--c,#6366f1);border-radius:12px;padding:8px;margin-bottom:8px;
}
@media (max-width:520px){.subj{grid-template-columns:1fr 38px}.subj .s-name{grid-column:1/2}.subj .s-body{grid-column:1/-1;order:3}}
.subj .s-name{font-weight:600}
.subj textarea{resize:none;min-height:40px;line-height:1.4;overflow:hidden}
.del{border:0;background:#fff1f2;color:var(--red);border-radius:10px;height:38px;cursor:pointer;font-size:1rem}
.del:hover{background:#ffe4e6}
.empty-list{color:var(--muted);font-size:.85rem;padding:8px 4px}

.switch{display:flex;align-items:center;gap:10px;cursor:pointer;font-weight:600;font-size:.9rem;margin-bottom:10px}
.switch input{width:20px;height:20px;accent-color:var(--orange);cursor:pointer}
.notice-body.off{opacity:.55}
.notice-body textarea{min-height:76px;resize:vertical}
.notice-body textarea:disabled{background:#f1f5f9;cursor:not-allowed}

.actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:4px}
.actions .btn{flex:1 1 120px;padding:12px 14px}
.hint{font-size:.72rem;color:var(--muted);margin:10px 2px 0;line-height:1.5}

/* ---------- preview column ---------- */
.preview-col{position:sticky;top:14px}
@media (max-width:980px){.preview-col{position:static}}
.preview-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;gap:8px;flex-wrap:wrap}
.preview-head h2{margin:0;font-size:1.05rem}
.pill{background:#eef2ff;color:var(--indigo);font-size:.72rem;font-weight:600;border-radius:999px;padding:4px 10px}
.preview-wrap{background:linear-gradient(160deg,#c7d2fe,#fbcfe8);border-radius:14px;padding:14px;display:flex;justify-content:center;overflow:hidden}
#scalerBox{position:relative}
#scaler{width:210mm;height:var(--page-h);transform-origin:top left}

/* ---------- the A4 sheet ---------- */
#page{
  width:210mm;height:var(--page-h);padding:var(--page-margin);background:#fff;position:relative;
  box-shadow:0 10px 30px rgba(30,27,75,.3);color:#000;
  font-family:'Noto Sans','Noto Sans Kannada','Noto Sans Devanagari',Arial,sans-serif;
}
#sheets{height:100%;display:flex;flex-direction:column}
.slot{flex:1 1 0;min-height:0;display:flex;align-items:center;padding:2mm 4mm;border-bottom:1px dashed #777}
.slot:last-child{border-bottom:0}
.leaflet{position:relative;width:100%;overflow:hidden}
.wm{
  position:absolute;left:0;top:0;width:100%;height:100%;display:flex;align-items:center;justify-content:center;
  font-family:Georgia,'Times New Roman',serif;font-weight:800;letter-spacing:.22em;padding-left:.22em;
  color:#000;opacity:.25;white-space:nowrap;z-index:0;pointer-events:none;user-select:none;
}
.lf{position:relative;z-index:1}
.sch{text-align:center;font-weight:800;font-size:1.45em;line-height:1.15}
.adr{text-align:center;font-size:.85em;font-weight:500;color:#333;line-height:1.2}
.meta{display:flex;justify-content:space-between;font-weight:700;font-size:1em;margin:.45em 0 .4em;padding:.1em 0}
.hw{width:100%;border-collapse:collapse;table-layout:fixed}
.hw th,.hw td{border:1.5px solid #000;padding:.22em .5em;text-align:left;vertical-align:top;line-height:1.3}
.hw th{font-weight:800}
.hw th:first-child,.hw td:first-child{width:22%}
.hw td:first-child{font-weight:600}
.hw td:last-child{white-space:pre-wrap;overflow-wrap:anywhere}
.notice{margin-top:.5em;border:1.5px solid #000;background:#fff8dc;padding:.25em .5em .4em}
.notice .nt{font-weight:800;text-decoration:underline;font-size:1em}
.notice .nb{white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.3}
.sign{margin-top:1.3em;font-weight:800;display:flex;align-items:flex-end;gap:.5em}
.sign .line{display:inline-block;width:16em;max-width:60%;border-bottom:1.5px solid #000;height:1.7em}
.ph{color:#aaa}
.empty{margin:auto;text-align:center;color:#94a3b8;font-family:'Poppins',sans-serif;font-size:14px;padding:0 30px}
.empty b{display:block;font-size:16px;color:#64748b;margin-bottom:4px}
#measure{position:absolute;left:-99999px;top:0;visibility:hidden;pointer-events:none}
#measure .slot{flex:none}

/* ---------- footer, toast, dialog ---------- */
footer{text-align:center;padding:18px 10px 24px;font-size:.88rem;color:var(--ink)}
.toast{
  position:fixed;left:50%;bottom:26px;transform:translate(-50%,30px);background:var(--ink);color:#fff;border-radius:12px;
  padding:11px 18px;font-size:.85rem;opacity:0;pointer-events:none;transition:.25s;z-index:50;max-width:90vw;text-align:center;
}
.toast.show{opacity:1;transform:translate(-50%,0)}
dialog{border:0;border-radius:20px;padding:22px;max-width:360px;width:90vw;box-shadow:0 20px 60px rgba(30,27,75,.4)}
dialog::backdrop{background:rgba(30,27,75,.45)}
dialog h3{margin:0 0 4px}
dialog p{margin:0 0 14px;color:var(--muted);font-size:.85rem}
dialog .btn{width:100%;margin-bottom:8px;padding:12px}
.btn-cancel{background:#f1f5f9;color:var(--ink)}

/* ---------- print ---------- */
@page{size:A4;margin:0}
@media print{
  html,body{background:#fff!important}
  .no-print{display:none!important}
  .layout{display:block!important;margin:0!important;padding:0!important;max-width:none!important}
  .preview-col{position:static!important;padding:0!important;box-shadow:none!important;background:none!important;border-radius:0!important}
  .preview-wrap{padding:0!important;background:none!important;border-radius:0!important;display:block!important;overflow:visible!important}
  #scalerBox{width:auto!important;height:auto!important}
  #scaler{transform:none!important}
  #page{box-shadow:none!important;margin:0!important;break-after:avoid;page-break-after:avoid;overflow:hidden}
  #page,#page *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
</style>
</head>
<body>

<header class="topbar no-print">
  <div class="topbar-in">
    <div class="logo">📝</div>
    <div>
      <h1>Homework Dashboard</h1>
      <p>Enter the day's homework class-wise, preview the A4 sheet, then print, save as PDF or share.</p>
    </div>
  </div>
</header>

<main class="layout">

  <!-- ===================== EDITOR ===================== -->
  <section class="card no-print" aria-label="Homework editor">
    <div class="dash-head">
      <div>
        <h2>Homework Dashboard</h2>
        <span class="saved" id="saved">Changes save automatically</span>
      </div>
      <div class="reset-row">
        <button class="btn btn-sm btn-ghost-orange" id="resetClass" title="Clear homework of the selected class">↺ Reset Class</button>
        <button class="btn btn-sm btn-ghost-red" id="resetAll" title="Clear everything">⟲ Reset All</button>
      </div>
    </div>

    <div class="section s-school">
      <h3>School &amp; class</h3>
      <div class="grid2">
        <div class="field">
          <label class="lbl" for="school">School name <span class="req">*</span></label>
          <input type="text" id="school" placeholder="e.g. SN Public School" autocomplete="off" maxlength="80">
          <div class="err">School name is required</div>
        </div>
        <div class="field">
          <label class="lbl" for="address">School address <span class="req">*</span></label>
          <input type="text" id="address" placeholder="e.g. Kanakapura" autocomplete="off" maxlength="120">
          <div class="err">School address is required</div>
        </div>
      </div>
      <div class="grid2">
        <div class="field" style="margin-bottom:0">
          <label class="lbl" for="cls">Class</label>
          <select id="cls"></select>
        </div>
        <div class="field" style="margin-bottom:0">
          <label class="lbl" for="date">Date</label>
          <div class="date-wrap">
            <input type="date" id="date">
            <button type="button" class="today-btn" id="todayBtn" title="Use today's date">Today</button>
          </div>
        </div>
      </div>
    </div>

    <div class="section s-hw">
      <div class="sec-head">
        <h3>Daily homework</h3>
        <button class="btn btn-sm btn-add" id="addSubject">+ Add subject</button>
      </div>
      <div id="subjects"></div>
    </div>

    <div class="section s-notice">
      <h3>Special notice</h3>
      <label class="switch"><input type="checkbox" id="noticeOn"> Enable special notice</label>
      <div class="notice-body off" id="noticeWrap">
        <textarea id="noticeBody" placeholder="Special notice for students and parents…" disabled></textarea>
      </div>
    </div>

    <div class="actions">
      <button class="btn btn-print" id="btnPrint">🖨 Print</button>
      <button class="btn btn-pdf" id="btnPdf">⬇ Download PDF</button>
      <button class="btn btn-share" id="btnShare">↗ Share</button>
    </div>
    <p class="hint">
      Browsers can't tell whether a printer is connected, so <b>Download PDF</b> saves the sheet directly.
      When printing, choose <b>A4</b>, <b>Margins: None</b>, <b>Scale: 100%</b> and turn off <i>Headers and footers</i>.
    </p>
  </section>

  <!-- ===================== PREVIEW ===================== -->
  <section class="card preview-col" aria-label="Preview">
    <div class="preview-head no-print">
      <h2>Live preview</h2>
      <span class="pill" id="info">A4</span>
    </div>
    <div class="preview-wrap" id="previewWrap">
      <div id="scalerBox">
        <div id="scaler">
          <div id="page"><div id="sheets"></div></div>
        </div>
      </div>
    </div>
  </section>
</main>

<footer class="no-print"><b>© All Rights Reserved to LK</b></footer>

<div id="measure"></div>
<div class="toast" id="toast" role="status"></div>

<dialog id="shareDlg">
  <h3>Share homework sheet</h3>
  <p>Choose the format to share.</p>
  <button class="btn btn-pdf" data-share="pdf">PDF file</button>
  <button class="btn btn-share" data-share="image">Image (PNG)</button>
  <button class="btn btn-cancel" id="shareCancel">Cancel</button>
</dialog>

<script>
(() => {
'use strict';
const $ = (s, r = document) => r.querySelector(s);
const STORE_KEY = 'lk_homework_dashboard_v1';
const TTL = 24 * 60 * 60 * 1000;                      // keep saved data for 24 hours
const CLASSES = ['M1','M2','M3', ...Array.from({length:10}, (_, i) => String(i + 1))];
const DEFAULT_SUBJECTS = ['English','Kannada','Hindi','Mathematics','EVS'];
const COLORS = ['#6366f1','#ec4899','#f59e0b','#10b981','#0ea5e9','#8b5cf6','#f43f5e'];
const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const PX_PER_MM = 96 / 25.4;
const PAGE_W_MM = 210, PAGE_H_MM = 296, MARGIN_MM = 0.5;

const uid = () => Math.random().toString(36).slice(2, 10);
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

function todayISO() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
}
function fmtDate(iso) {
  const [y, m, d] = (iso || '').split('-').map(Number);
  if (!y) return '';
  return `${String(d).padStart(2,'0')} ${MONTHS[m-1]} ${y}`;
}

/* ---------------- state + autosave ---------------- */
function newClassData() {
  return { subjects: DEFAULT_SUBJECTS.map(n => ({ id: uid(), name: n, body: '' })), notice: { on: false, body: '' } };
}
function defaultState() {
  return { school: '', address: '', cls: 'M1', date: todayISO(), dateEdited: false, classes: {} };
}
let state = defaultState();
const cur = () => state.classes[state.cls] || (state.classes[state.cls] = newClassData());

function load() {
  try {
    const raw = localStorage.getItem(STORE_KEY);
    if (!raw) return;
    const o = JSON.parse(raw);
    if (!o || !o.savedAt || Date.now() - o.savedAt > TTL) { localStorage.removeItem(STORE_KEY); return; }
    state = Object.assign(defaultState(), o.state);
    if (!state.dateEdited || !state.date) state.date = todayISO();
    if (!CLASSES.includes(state.cls)) state.cls = 'M1';
  } catch (e) { /* ignore corrupt data */ }
}
let saveTimer;
function save() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(() => {
    try {
      localStorage.setItem(STORE_KEY, JSON.stringify({ savedAt: Date.now(), state }));
      $('#saved').textContent = '✓ Autosaved at ' + new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
    } catch (e) { $('#saved').textContent = 'Autosave unavailable in this browser'; }
  }, 200);
}
let previewTimer;
function changed() { save(); clearTimeout(previewTimer); previewTimer = setTimeout(refreshPreview, 120); }

/* ---------------- toast ---------------- */
let toastTimer;
function toast(msg) {
  const t = $('#toast'); t.textContent = msg; t.classList.add('show');
  clearTimeout(toastTimer); toastTimer = setTimeout(() => t.classList.remove('show'), 3200);
}

/* ---------------- editor rendering ---------------- */
function autosize(ta) { ta.style.height = 'auto'; ta.style.height = Math.max(40, ta.scrollHeight + 2) + 'px'; }

function renderSubjects() {
  const list = $('#subjects'); list.innerHTML = '';
  const subs = cur().subjects;
  if (!subs.length) { list.innerHTML = '<div class="empty-list">No subjects yet. Use “+ Add subject”.</div>'; return; }
  subs.forEach((s, i) => {
    const row = document.createElement('div');
    row.className = 'subj'; row.style.setProperty('--c', COLORS[i % COLORS.length]);
    row.innerHTML = '<input type="text" class="s-name" placeholder="Subject name" maxlength="40" aria-label="Subject name">' +
      '<textarea class="s-body" rows="1" placeholder="Homework details (Enter for a new line)" aria-label="Homework details"></textarea>' +
      '<button class="del" title="Delete subject" aria-label="Delete subject">🗑</button>';
    const n = $('.s-name', row), b = $('.s-body', row);
    n.value = s.name; b.value = s.body;
    n.addEventListener('input', () => { s.name = n.value; changed(); });
    b.addEventListener('input', () => { s.body = b.value; autosize(b); changed(); });
    $('.del', row).addEventListener('click', () => {
      if ((s.body.trim()) && !confirm(`Delete "${s.name || 'this subject'}" and its homework?`)) return;
      cur().subjects = cur().subjects.filter(x => x.id !== s.id);
      renderSubjects(); changed();
    });
    list.appendChild(row); autosize(b);
  });
}
function renderNotice() {
  const n = cur().notice;
  $('#noticeOn').checked = n.on;
  $('#noticeBody').value = n.body;
  $('#noticeBody').disabled = !n.on;
  $('#noticeWrap').classList.toggle('off', !n.on);
}
function renderEditor() {
  $('#school').value = state.school;
  $('#address').value = state.address;
  $('#cls').value = state.cls;
  $('#date').value = state.date;
  renderSubjects(); renderNotice(); markFields(false);
}

/* ---------------- validation ---------------- */
function markFields(force) {
  ['#school', '#address'].forEach(sel => {
    const el = $(sel);
    el.classList.toggle('invalid', (force || el.dataset.touched === '1') && !el.value.trim());
  });
}
const hasHomework = () => cur().subjects.some(s => s.body.trim());
function guard() {
  markFields(true);
  if (!state.school.trim()) { $('#school').focus(); toast('School name is required'); return false; }
  if (!state.address.trim()) { $('#address').focus(); toast('School address is required'); return false; }
  if (!hasHomework()) { toast('Enter homework for at least one subject first'); return false; }
  clearTimeout(previewTimer); refreshPreview();
  return true;
}

/* ---------------- preview / layout engine ---------------- */
function watermarkText(name) {
  const words = (name || '').trim().split(/\s+/).filter(w => /[\p{L}\p{N}]/u.test(w));
  if (!words.length) return 'SCHOOL';
  if (words.length === 1) return words[0].toUpperCase().slice(0, 10);
  // initials of the first 4 words; a short all-caps word such as "SN" is kept whole
  return words.slice(0, 4).map(w => /^[A-Z]{2,3}$/.test(w) ? w : (w.match(/[\p{L}\p{N}]/u) || [''])[0]).join('').toUpperCase().slice(0, 8);
}

function leafletHTML(fs, wmPx) {
  const d = cur();
  const rows = d.subjects.filter(s => s.body.trim());
  const body = rows.map(s => `<tr><td>${esc(s.name.trim() || '—')}</td><td>${esc(s.body.replace(/\s+$/,''))}</td></tr>`).join('');
  const notice = d.notice.on
    ? `<div class="notice"><div class="nt">SPECIAL NOTICE:</div><div class="nb">${esc(d.notice.body.replace(/\s+$/,''))}</div></div>` : '';
  const school = state.school.trim(), addr = state.address.trim();
  return `<div class="leaflet" style="font-size:${fs}px">
    <div class="wm"${wmPx ? ` style="font-size:${wmPx}px"` : ''}>${esc(watermarkText(state.school))}</div>
    <div class="lf">
      <div class="sch${school ? '' : ' ph'}">${esc(school || 'School name')}</div>
      <div class="adr${addr ? '' : ' ph'}">${esc(addr || 'School address')}</div>
      <div class="meta"><span>Class: ${esc(state.cls)}</span><span>Date: ${esc(fmtDate(state.date))}</span></div>
      <table class="hw"><thead><tr><th>Subject</th><th>Homework Details</th></tr></thead><tbody>${body}</tbody></table>
      ${notice}
      <div class="sign"><span>Class Teacher Sign:</span><span class="line"></span></div>
    </div></div>`;
}

function refreshPreview() {
  const sheets = $('#sheets');
  if (!hasHomework()) {
    sheets.innerHTML = '<div class="empty"><b>Nothing to preview yet</b>Type homework against a subject and the A4 sheet appears here.</div>';
    $('#info').textContent = 'A4';
    return;
  }
  const availH = sheets.clientHeight;
  const meas = $('#measure');
  meas.style.width = sheets.clientWidth + 'px';
  const slotH = fs => { meas.innerHTML = `<div class="slot">${leafletHTML(fs)}</div>`; return meas.firstChild.offsetHeight; };

  // 1) pick a font size, 2) fit as many leaflets as possible, 3) enlarge text while the count stays the same
  let fs = 11.5, h = slotH(fs), n = Math.floor(availH / h);
  if (n < 1) {
    while (fs > 6 && (h = slotH(fs)) > availH - 1) fs -= 0.25;
    n = 1;
  } else {
    let best = fs;
    for (let f = fs + 0.25; f <= 16; f += 0.25) {
      if (slotH(f) * n <= availH - 1) best = f; else break;
    }
    fs = best;
  }
  h = slotH(fs);
  const L = watermarkText(state.school).length;
  const leafW = sheets.clientWidth - 8 * PX_PER_MM;
  const wmPx = Math.floor(Math.min((h - 4 * PX_PER_MM) * 0.62, fs * 7, (leafW * 0.82) / (L * 1.1)));

  let html = '';
  for (let i = 0; i < n; i++) html += `<div class="slot">${leafletHTML(fs, wmPx)}</div>`;
  sheets.innerHTML = html;
  meas.innerHTML = '';
  $('#info').textContent = h > availH ? 'Too long for one A4 page – shorten the homework'
    : `A4 · ${n} set${n > 1 ? 's' : ''} per page`;
}

function fitPreview() {
  const wrap = $('#previewWrap');
  const cs = getComputedStyle(wrap);
  const avail = wrap.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
  const pw = PAGE_W_MM * PX_PER_MM, ph = PAGE_H_MM * PX_PER_MM;
  const s = Math.min(1, avail / pw);
  $('#scaler').style.transform = `scale(${s})`;
  $('#scalerBox').style.width = pw * s + 'px';
  $('#scalerBox').style.height = ph * s + 'px';
}

/* ---------------- output: print / pdf / image / share ---------------- */
const fileBase = () => `Homework_Class-${state.cls}_${state.date}`;
function setBusy(b) { document.querySelectorAll('.actions .btn').forEach(x => x.disabled = b); }

async function renderCanvas() {
  if (document.fonts && document.fonts.ready) await document.fonts.ready;
  return html2canvas($('#page'), {
    scale: 2.5, backgroundColor: '#ffffff', useCORS: true, logging: false,
    onclone: doc => {
      doc.getElementById('scaler').style.transform = 'none';
      doc.getElementById('scalerBox').style.cssText = 'width:auto;height:auto';
    }
  });
}
async function makePDF() {
  const canvas = await renderCanvas();
  const { jsPDF } = window.jspdf;
  const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
  pdf.addImage(canvas.toDataURL('image/jpeg', 0.95), 'JPEG', 0, 0, PAGE_W_MM, PAGE_H_MM);
  return pdf;
}
function download(blob, name) {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = name;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 4000);
}

function doPrint() {
  if (!guard()) return;
  const t = document.title; document.title = fileBase();
  window.print();
  setTimeout(() => { document.title = t; }, 800);
}
async function doPdf() {
  if (!guard()) return;
  setBusy(true); toast('Creating PDF…');
  try { const pdf = await makePDF(); pdf.save(fileBase() + '.pdf'); toast('PDF saved'); }
  catch (e) { console.error(e); toast('Could not create the PDF. Please try again.'); }
  finally { setBusy(false); }
}
async function doShare(kind) {
  $('#shareDlg').close(); setBusy(true); toast('Preparing file…');
  try {
    let blob, name, type;
    if (kind === 'pdf') { blob = (await makePDF()).output('blob'); name = fileBase() + '.pdf'; type = 'application/pdf'; }
    else { const c = await renderCanvas(); blob = await new Promise(r => c.toBlob(r, 'image/png')); name = fileBase() + '.png'; type = 'image/png'; }
    const file = new File([blob], name, { type });
    if (navigator.canShare && navigator.canShare({ files: [file] })) {
      await navigator.share({ files: [file], title: `Homework – Class ${state.cls}`, text: `Homework for Class ${state.cls} (${fmtDate(state.date)})` });
    } else {
      download(blob, name); toast('Sharing isn’t supported in this browser, so the file was downloaded.');
    }
  } catch (e) {
    if (e && e.name !== 'AbortError') { console.error(e); toast('Could not share. Try Download PDF instead.'); }
  } finally { setBusy(false); }
}

/* ---------------- wiring ---------------- */
function init() {
  $('#cls').innerHTML = CLASSES.map(c => `<option value="${c}">${c}</option>`).join('');
  load(); renderEditor();

  [['#school', 'school'], ['#address', 'address']].forEach(([sel, key]) => {
    const el = $(sel);
    el.addEventListener('input', () => { state[key] = el.value; markFields(false); changed(); });
    el.addEventListener('blur', () => { el.dataset.touched = '1'; markFields(false); });
  });
  $('#cls').addEventListener('change', e => { state.cls = e.target.value; renderSubjects(); renderNotice(); refreshPreview(); save(); });
  $('#date').addEventListener('change', e => {
    state.date = e.target.value || todayISO();
    state.dateEdited = state.date !== todayISO();
    e.target.value = state.date; changed();
  });
  $('#todayBtn').addEventListener('click', () => {
    state.date = todayISO(); state.dateEdited = false; $('#date').value = state.date; changed();
  });
  $('#addSubject').addEventListener('click', () => {
    cur().subjects.push({ id: uid(), name: '', body: '' });
    renderSubjects(); save();
    const names = document.querySelectorAll('#subjects .s-name'); names[names.length - 1].focus();
  });
  $('#noticeOn').addEventListener('change', e => {
    cur().notice.on = e.target.checked; renderNotice();
    if (e.target.checked) $('#noticeBody').focus();
    changed();
  });
  $('#noticeBody').addEventListener('input', e => { cur().notice.body = e.target.value; changed(); });

  $('#resetClass').addEventListener('click', () => {
    if (!confirm(`Reset all homework and the special notice for Class ${state.cls}?`)) return;
    state.classes[state.cls] = newClassData(); renderSubjects(); renderNotice(); refreshPreview(); save();
    toast(`Class ${state.cls} reset`);
  });
  $('#resetAll').addEventListener('click', () => {
    if (!confirm('Reset everything, including school details and all classes?')) return;
    state = defaultState();
    try { localStorage.removeItem(STORE_KEY); } catch (e) {}
    document.querySelectorAll('#school,#address').forEach(el => delete el.dataset.touched);
    renderEditor(); refreshPreview(); $('#saved').textContent = 'Changes save automatically';
    toast('Everything reset');
  });

  $('#btnPrint').addEventListener('click', doPrint);
  $('#btnPdf').addEventListener('click', doPdf);
  $('#btnShare').addEventListener('click', () => { if (guard()) $('#shareDlg').showModal(); });
  $('#shareDlg').addEventListener('click', e => {
    const k = e.target.dataset && e.target.dataset.share;
    if (k) doShare(k);
    if (e.target === $('#shareDlg')) $('#shareDlg').close();
  });
  $('#shareCancel').addEventListener('click', () => $('#shareDlg').close());

  new ResizeObserver(fitPreview).observe($('#previewWrap'));
  window.addEventListener('resize', fitPreview);
  fitPreview(); refreshPreview();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(refreshPreview);
}
init();
})();
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return Response(INDEX_HTML, mimetype="text/html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
