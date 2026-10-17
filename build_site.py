#!/usr/bin/env python3
# 构建 刷题网站/index.html：读取 data.json，把题库数据内嵌进单文件应用。
# 数据更新时：重跑提取脚本生成 data.json，再运行本脚本即可重建网站。
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, 'data.json'), encoding='utf-8'))

TEMPLATE = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#2f6fd6">
<title>信创理论题库刷题</title>
<style>
  :root{ --blue:#2f6fd6; --blue-d:#24529f; --blue-l:#eaf1fc; --green:#1e9e58; --green-l:#e6f6ee;
         --red:#d64545; --red-l:#fdeeee; --amber:#e8990c; --amber-l:#fdf3e0;
         --bg:#f1f3f8; --card:#fff; --line:#e4e8f0; --text:#232a3b; --muted:#7c8597; }
  *{ box-sizing:border-box; -webkit-tap-highlight-color:transparent; }
  html,body{ overscroll-behavior:none; }
  body{ margin:0; background:var(--bg); color:var(--text); font-size:15px; padding-bottom:env(safe-area-inset-bottom);
        font-family:system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif; }
  button{ font-family:inherit; }
  .opt,.btn,.star,.seg,.tab-item,.iwbtn,.chin{ touch-action:manipulation; }

  /* ===== 顶部：应用头 + 工具行 ===== */
  .topwrap{ position:sticky; top:0; z-index:20; box-shadow:0 1px 8px rgba(24,44,90,.10); }
  .appbar{ display:flex; align-items:center; gap:10px; padding:10px 14px;
           background:linear-gradient(135deg,#2f6fd6,#4b8bf5 70%,#5f9bff); color:#fff; }
  .brand{ font-weight:800; font-size:16.5px; letter-spacing:.5px; display:flex; align-items:center; gap:7px; }
  .brand .logo{ width:24px; height:24px; border-radius:7px; background:rgba(255,255,255,.22);
                display:flex; align-items:center; justify-content:center; font-size:14px; }
  .appactions{ margin-left:auto; display:flex; gap:8px; }
  .hbtn{ position:relative; border:none; background:rgba(255,255,255,.18); color:#fff; border-radius:10px;
         padding:7px 11px; font-size:14px; cursor:pointer; }
  .hbtn .bub{ background:#fff; color:var(--blue-d); border-radius:999px; font-weight:800; font-size:12px;
              padding:0 6px; margin-left:4px; }
  .toolbar{ background:var(--card); padding:9px 12px 10px; }
  .seg{ display:flex; background:#edf1f7; border-radius:11px; padding:3px; gap:2px; }
  .seg button{ flex:1; border:none; background:transparent; padding:8px 2px; border-radius:9px;
               font-size:14px; color:var(--muted); cursor:pointer; font-weight:600; }
  .seg button.on{ background:#fff; color:var(--blue-d); box-shadow:0 1px 4px rgba(24,44,90,.14); }
  .picks{ display:flex; gap:7px; margin-top:8px; }
  .selwrap{ position:relative; }
  .selwrap::after{ content:'▾'; position:absolute; right:9px; top:50%; transform:translateY(-54%);
                   color:var(--muted); font-size:12px; pointer-events:none; }
  select{ appearance:none; -webkit-appearance:none; border:1px solid var(--line); background:#f8fafd;
          border-radius:10px; padding:9px 24px 9px 10px; font-size:14px; color:var(--text); max-width:220px;
          outline:none; }
  select:focus{ border-color:var(--blue); }
  .searchwrap{ flex:1; position:relative; }
  .searchwrap::before{ content:'🔍'; position:absolute; left:9px; top:50%; transform:translateY(-52%); font-size:12px; opacity:.7; }
  .searchwrap input{ width:100%; border:1px solid var(--line); background:#f8fafd; border-radius:10px;
                     padding:9px 10px 9px 29px; font-size:16px; color:var(--text); outline:none; min-width:0; }
  .searchwrap input:focus{ border-color:var(--blue); }

  /* ===== 主体 ===== */
  .wrap{ max-width:820px; margin:0 auto; padding:10px 12px calc(86px + env(safe-area-inset-bottom)); }
  @media (min-width:641px){ .wrap{ padding-bottom:20px; } }
  .stats{ display:flex; flex-wrap:wrap; gap:5px 6px; align-items:center; margin:2px 2px 9px;
          color:var(--muted); font-size:13px; }
  .stats b{ color:var(--text); }
  .statchip{ display:inline-flex; align-items:center; gap:4px; background:#fff; border:1px solid var(--line);
             border-radius:999px; padding:3px 10px; font-size:12.5px; }
  .statchip.hero{ background:var(--blue-l); border-color:#d7e4fa; color:var(--blue-d); font-weight:600; }
  .statchip.link{ cursor:pointer; }
  .statchip.link:hover{ border-color:var(--blue); }
  .bar{ height:5px; background:var(--line); border-radius:99px; overflow:hidden; margin:0 2px 10px; }
  .bar i{ display:block; height:100%; background:linear-gradient(90deg,#2f6fd6,#5f9bff); border-radius:99px; }

  .card{ background:var(--card); border:1px solid var(--line); border-radius:16px; padding:16px;
         box-shadow:0 1px 3px rgba(20,40,80,.05); }
  .meta{ display:flex; flex-wrap:wrap; gap:6px; align-items:center; margin-bottom:10px; }
  .chin{ display:inline-block; padding:3px 10px; border-radius:999px; font-size:12px; }
  .chin.bank{ background:var(--blue-l); color:var(--blue-d); font-weight:600; }
  .chin.gray{ background:#eef1f6; color:var(--muted); }
  .chin.fixed{ background:var(--green-l); color:var(--green); font-weight:600; }
  .chin.warn{ background:var(--amber-l); color:var(--amber); font-weight:600; }
  .star{ font-size:21px; cursor:pointer; color:#c6ccda; background:none; border:none; padding:0 4px; line-height:1; }
  .star.on{ color:#f5b301; }
  .stem{ font-weight:650; font-size:16px; line-height:1.7; white-space:pre-wrap; }
  .opts{ display:flex; flex-direction:column; gap:9px; margin-top:14px; }
  .opt{ display:flex; gap:10px; align-items:flex-start; padding:12px 13px; border:1.5px solid var(--line);
        border-radius:12px; cursor:pointer; background:#fafbfd; line-height:1.55; font-size:15px; text-align:left; }
  .opt .letter{ font-weight:800; color:var(--blue-d); min-width:18px; }
  .opt.sel{ border-color:var(--blue); background:var(--blue-l); }
  .opt.ok{ border-color:var(--green); background:var(--green-l); } .opt.ok .letter{ color:var(--green); }
  .opt.bad{ border-color:var(--red); background:var(--red-l); } .opt.bad .letter{ color:var(--red); }
  .locked .opt{ cursor:default; }
  .verdict{ margin-top:13px; padding:11px 13px; border-radius:11px; font-weight:700; }
  .verdict.ok{ background:var(--green-l); color:var(--green); }
  .verdict.bad{ background:var(--red-l); color:var(--red); }
  .why{ margin-top:10px; padding:12px 14px; border-radius:11px; background:#f6f8fb; color:#3a4358;
        line-height:1.75; font-size:14px; white-space:pre-wrap; }
  .multi-note{ margin-top:10px; color:var(--muted); font-size:13px; }
  .nav{ margin:14px 0 4px; }
  .navbtns{ display:flex; gap:10px; }
  .navbtns .btn{ flex:1; }
  .jrow{ display:flex; gap:6px; align-items:center; justify-content:center; color:var(--muted);
         font-size:13px; margin-top:10px; }
  .nav input[type=number]{ width:74px; font-size:16px; padding:8px; border:1px solid var(--line);
                           border-radius:10px; outline:none; }
  .nav input[type=number]:focus{ border-color:var(--blue); }
  .btn{ padding:10px 14px; border:1px solid var(--line); border-radius:11px; background:#fff; cursor:pointer;
        font-size:14.5px; color:var(--text); }
  .btn:hover{ border-color:var(--blue); color:var(--blue-d); }
  .btn.primary{ background:var(--blue); border-color:var(--blue); color:#fff; font-weight:650; }
  .btn.danger{ color:var(--red); border-color:#f2caca; }
  .btn:disabled{ opacity:.4; cursor:default; }

  /* ===== 底部标签栏（手机） ===== */
  .tabbar{ position:fixed; left:0; right:0; bottom:0; z-index:25; display:flex; justify-content:space-around;
           background:rgba(255,255,255,.96); backdrop-filter:blur(10px); border-top:1px solid var(--line);
           padding:6px 4px calc(6px + env(safe-area-inset-bottom)); }
  .tab-item{ flex:1; border:none; background:none; display:flex; flex-direction:column; align-items:center;
             gap:2px; font-size:11.5px; color:var(--muted); cursor:pointer; padding:4px 0; border-radius:10px; }
  .tab-item .ic{ font-size:19px; line-height:1; }
  .tab-item.on{ color:var(--blue-d); font-weight:700; }
  .tab-item{ position:relative; }
  .tbub{ position:absolute; top:-2px; left:calc(50% + 6px); background:var(--red); color:#fff; font-size:10.5px;
         font-weight:800; border-radius:999px; padding:1px 5.5px; line-height:1.5; }
  .tbub.amber{ background:var(--amber); }
  .tbub.zero{ display:none; }

  /* ===== 抽屉面板（错题/收藏/设置/统计） ===== */
  .mask{ position:fixed; inset:0; background:rgba(15,25,48,.48); z-index:40; display:none; }
  .mask.open{ display:block; }
  .panel{ position:absolute; left:0; right:0; bottom:0; max-height:88%; background:var(--bg);
          border-radius:18px 18px 0 0; display:flex; flex-direction:column; padding-bottom:env(safe-area-inset-bottom);
          animation:up .18s ease; }
  @keyframes up{ from{ transform:translateY(40px); opacity:.4; } to{ transform:none; opacity:1; } }
  .grab{ width:42px; height:4.5px; border-radius:99px; background:#cfd6e2; margin:9px auto 2px; }
  .phead{ display:flex; align-items:center; gap:8px; padding:6px 14px 10px; flex-wrap:wrap; }
  .phead .ttl{ font-size:16.5px; font-weight:800; display:flex; align-items:center; gap:7px; }
  .phead .cnt{ background:var(--blue-l); color:var(--blue-d); border-radius:999px; font-size:12.5px;
               font-weight:800; padding:2px 9px; }
  .phead .sp{ flex:1; }
  .pbody{ overflow:auto; padding:2px 12px calc(14px + env(safe-area-inset-bottom)); }
  .pgroup{ margin:10px 4px 3px; color:var(--muted); font-size:12.5px; font-weight:700;
           display:flex; align-items:center; gap:6px; }
  .pgroup::after{ content:''; flex:1; height:1px; background:var(--line); }
  .item{ display:flex; gap:10px; align-items:center; background:#fff; border:1px solid var(--line);
         border-radius:13px; padding:12px 12px; margin:7px 1px; cursor:pointer; }
  .item[data-kind="wrong"]{ border-left:4px solid var(--red); }
  .item[data-kind="star"]{ border-left:4px solid var(--amber); }
  .item .info{ flex:1; min-width:0; }
  .item .meta{ color:var(--muted); font-size:12px; margin-bottom:3px; }
  .item .t{ font-size:14px; line-height:1.55; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }
  .item .go{ color:#c3cad8; font-size:17px; flex:none; }
  .iwbtn{ flex:none; border:none; background:var(--red-l); color:var(--red); border-radius:9px;
          padding:7px 9px; font-size:12.5px; font-weight:700; cursor:pointer; }
  .item[data-kind="star"] .iwbtn{ background:#fdf1de; color:var(--amber); }
  .two{ display:flex; gap:8px; margin-top:2px; }
  .two .btn{ flex:1; }
  .chips{ display:flex; flex-direction:column; gap:2px; padding:2px 4px; }
  .row{ display:flex; align-items:center; justify-content:space-between; gap:10px; padding:13px 6px;
        border-bottom:1px solid var(--line); font-size:15px; }
  .row:last-child{ border-bottom:none; }
  .row .hint{ display:block; color:var(--muted); font-size:12.5px; margin-top:3px; font-weight:400; }
  .sw{ position:relative; width:46px; height:27px; flex:none; }
  .sw input{ opacity:0; width:100%; height:100%; position:absolute; margin:0; cursor:pointer; z-index:2; }
  .sw .kn{ position:absolute; inset:0; background:#d5dbe6; border-radius:99px; transition:.15s; }
  .sw .kn::after{ content:''; position:absolute; top:3px; left:3px; width:21px; height:21px; background:#fff;
                  border-radius:50%; transition:.15s; box-shadow:0 1px 3px rgba(0,0,0,.25); }
  .sw input:checked + .kn{ background:var(--green); }
  .sw input:checked + .kn::after{ left:22px; }
  .statcard{ background:#fff; border:1px solid var(--line); border-radius:13px; padding:13px 14px; margin:8px 1px; }
  .statcard .nm{ font-weight:700; font-size:14.5px; display:flex; justify-content:space-between; }
  .statcard .nm span{ color:var(--muted); font-weight:500; font-size:12.5px; }
  .sbar{ height:7px; background:#eef1f6; border-radius:99px; margin-top:9px; overflow:hidden; }
  .sbar i{ display:block; height:100%; border-radius:99px; }
  .sbar.done i{ background:var(--blue); } .sbar.acc i{ background:var(--green); }
  .srow{ display:flex; gap:8px; align-items:center; font-size:12px; color:var(--muted); margin-top:5px; }
  .srow .lbl{ width:30px; flex:none; }
  .srow .sbar{ flex:1; margin:0; }
  .empty-big{ text-align:center; padding:44px 10px 30px; color:var(--muted); }
  .empty-big .em{ font-size:44px; display:block; margin-bottom:10px; }
  @media (min-width:641px){
    .tabbar{ display:none; }
    .wrap{ padding-bottom:20px; }
    .panel{ left:50%; right:auto; bottom:auto; top:50%; transform:translate(-50%,-50%); width:680px;
            max-height:84%; border-radius:16px; padding-bottom:14px; animation:pop .15s ease; }
    @keyframes pop{ from{ transform:translate(-50%,-48%); opacity:.35; } to{ transform:translate(-50%,-50%); opacity:1; } }
    .grab{ display:none; }
  }
  @media (max-width:640px){
    .appbar{ padding:9px 12px; }
    .toolbar{ padding:9px 10px 10px; }
    .picks select{ max-width:none; }
    .picks .selwrap{ flex:1.35; } .picks .selwrap:nth-child(2){ flex:1; }
    .stem{ font-size:16px; }
  }
</style>
</head>
<body>

<header class="topwrap">
  <div class="appbar">
    <div class="brand"><span class="logo">📘</span>信创理论题库</div>
    <div class="appactions">
      <button class="hbtn" id="hStar">⭐<span class="bub" id="hStarN">0</span></button>
      <button class="hbtn" id="hWrong">📕<span class="bub" id="hWrongN">0</span></button>
      <button class="hbtn" id="hSet">⚙️</button>
    </div>
  </div>
  <div class="toolbar">
    <div class="seg" id="modeSeg">
      <button data-m="seq">顺序</button>
      <button data-m="random">随机</button>
      <button data-m="wrong">错题</button>
      <button data-m="star">收藏</button>
    </div>
    <div class="picks">
      <div class="selwrap"><select id="bankSel"></select></div>
      <div class="selwrap"><select id="typeSel">
        <option value="all">全部题型</option><option value="单选">单选题</option>
        <option value="多选">多选题</option><option value="判断">判断题</option>
      </select></div>
      <div class="searchwrap"><input id="search" type="search" placeholder="搜题干 / 选项关键词"></div>
    </div>
  </div>
</header>

<main class="wrap">
  <div class="stats" id="stats"></div>
  <div class="card" id="card"></div>
  <div class="nav">
    <div class="navbtns">
      <button class="btn" id="prevBtn">← 上一题</button>
      <button class="btn primary" id="nextBtn">下一题 →</button>
    </div>
    <div class="jrow">跳到第 <input type="number" id="jumpNo" min="1"> 题 <button class="btn" id="jumpBtn">跳转</button></div>
  </div>
</main>

<nav class="tabbar" id="tabbar">
  <button class="tab-item on" data-tab="quiz"><span class="ic">📖</span>刷题</button>
  <button class="tab-item" data-tab="wrong"><span class="ic">📕</span>错题本<span class="tbub" id="nWrong">0</span></button>
  <button class="tab-item" data-tab="star"><span class="ic">⭐</span>收藏集<span class="tbub amber" id="nStar">0</span></button>
  <button class="tab-item" data-tab="set"><span class="ic">⚙️</span>设置</button>
</nav>

<div class="mask" id="sheetWrong">
  <div class="panel">
    <div class="grab"></div>
    <div class="phead">
      <span class="ttl">📕 错题集 <span class="cnt" id="wHeadN">0</span></span><span class="sp"></span>
      <button class="btn" id="wClose">✕ 关闭</button>
    </div>
    <div class="pbody">
      <div class="two">
        <button class="btn primary" id="wRetry">▶ 一键重刷全部错题</button>
        <button class="btn danger" id="wClear">清空错题</button>
      </div>
      <div id="wList"></div>
    </div>
  </div>
</div>

<div class="mask" id="sheetStar">
  <div class="panel">
    <div class="grab"></div>
    <div class="phead">
      <span class="ttl">⭐ 收藏集 <span class="cnt" id="sHeadN">0</span></span><span class="sp"></span>
      <button class="btn" id="sClose">✕ 关闭</button>
    </div>
    <div class="pbody">
      <div class="two">
        <button class="btn primary" id="sRetry">▶ 一键重刷全部收藏</button>
        <button class="btn danger" id="sClear">清空收藏</button>
      </div>
      <div id="sList"></div>
    </div>
  </div>
</div>

<div class="mask" id="sheetSet">
  <div class="panel">
    <div class="grab"></div>
    <div class="phead"><span class="ttl">⚙️ 设置</span><span class="sp"></span>
      <button class="btn" id="setClose">✕ 关闭</button></div>
    <div class="pbody">
      <div class="chips">
        <div class="row"><span>背题模式<span class="hint">直接显示答案与解析，不判分</span></span>
          <label class="sw"><input type="checkbox" id="revealChk"><span class="kn"></span></label></div>
        <div class="row"><span>答对自动下一题<span class="hint">答错时停留在当前题便于看解析</span></span>
          <label class="sw"><input type="checkbox" id="autoNext"><span class="kn"></span></label></div>
      </div>
      <button class="btn danger" id="resetBtn" style="width:100%;margin-top:14px;">🗑 重置全部进度（清空答题与收藏记录）</button>
    </div>
  </div>
</div>

<div class="mask" id="sheetStats">
  <div class="panel">
    <div class="grab"></div>
    <div class="phead"><span class="ttl">📊 全库统计</span><span class="sp"></span>
      <button class="btn" id="tClose">✕ 关闭</button></div>
    <div class="pbody"><div id="statsBody"></div></div>
  </div>
</div>

<script>
const RAW = __DATA__;
const BANKS = [
  {k:'all', n:'全部题库'},
  {k:'y26', n:'2026 理论'},
  {k:'y25linux', n:'2025 Linux'},
  {k:'y25sec', n:'2025 安全配置'},
  {k:'y25base', n:'2025 计算机基础'},
];
const TYPE_NAME = {'单选':'单选题','多选':'多选题','判断':'判断题'};
const LS = 'szq_v1';
const LT = 'ABCDEF';
let S = {answered:{}, starred:{}, autoNext:true, reveal:false, orders:{}, pos:{}};
try{ const saved = JSON.parse(localStorage.getItem(LS)||'{}'); S = Object.assign(S, saved); }catch(e){}
S.orders = {}; // 每次打开都重新洗牌，保证覆盖所有题
const save = () => localStorage.setItem(LS, JSON.stringify(S));
const qid = q => q.k + ':' + q.s;

const st = { bank:'y26', type:'all', mode:'random', search:'', list:[], idx:0, sel:new Set(), graded:null };

const QMAP = {}; RAW.forEach(q => QMAP[qid(q)] = q);
const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const shuffled = a => { const x=a.slice(); for(let i=x.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [x[i],x[j]]=[x[j],x[i]]; } return x; };
const wrongIds = () => Object.keys(S.answered).filter(id => S.answered[id] === 0);
const starIds  = () => Object.keys(S.starred).filter(id => S.starred[id]);

function buildBankSel(){
  const counts = {};
  RAW.forEach(q => counts[q.k] = (counts[q.k]||0)+1);
  BANKS.forEach(b => b.total = b.k==='all' ? RAW.length : (counts[b.k]||0));
  const sel = document.getElementById('bankSel');
  sel.innerHTML = BANKS.map(b=>`<option value="${b.k}">${b.n}（${b.total}）</option>`).join('');
  sel.value = st.bank;
}
function setMode(m){
  st.mode = m;
  document.querySelectorAll('#modeSeg button').forEach(b => b.classList.toggle('on', b.dataset.m === m));
  rebuild();
}
function baseList(){
  let xs = RAW.filter(q => (st.bank==='all'||q.k===st.bank) && (st.type==='all'||q.t===st.type));
  const kw = st.search.trim().toLowerCase();
  if(kw) xs = xs.filter(q => (q.q+' '+q.o.join(' ')).toLowerCase().includes(kw));
  return xs;
}
function scopeKey(){ return st.bank+'|'+st.type+'|'+st.search; }
function rebuild(keepIdx){
  const scope = scopeKey();
  let xs = baseList();
  if(st.mode==='wrong') xs = xs.filter(q => S.answered[qid(q)] === 0);
  else if(st.mode==='star') xs = xs.filter(q => S.starred[qid(q)]);
  else if(st.mode==='random'){
    // 洗牌 + 未刷过的排前面：不会因为顺序固定而只刷到开头几题
    const un = xs.filter(q => !(qid(q) in S.answered));
    const dn = xs.filter(q => (qid(q) in S.answered));
    xs = shuffled(un).concat(shuffled(dn));
  }
  st.list = xs;
  if(keepIdx) st.idx = Math.min(st.idx, Math.max(xs.length-1,0));
  else if(st.mode==='seq') st.idx = Math.min((S.pos && S.pos[scope])||0, Math.max(xs.length-1,0));
  else st.idx = 0;
  S.pos = S.pos || {}; S.pos[scope + '|' + st.mode] = st.idx;
  save();
  render();
}
function cur(){ return st.list[st.idx]; }
const bankName = k => BANKS.find(b=>b.k===k).n;
function scopedStats(){
  const ids = st.list.map(qid);
  const done = ids.filter(id => id in S.answered);
  const ok = done.filter(id => S.answered[id] === 1).length;
  return {total:st.list.length, done:done.length, ok, rate: done.length?Math.round(100*ok/done.length):null};
}
const MODE_TAG = {seq:'顺序模式', random:'随机模式', wrong:'错题重刷', star:'收藏重刷'};
function renderStats(){
  const s = scopedStats();
  let bits = [`<span class="statchip hero"><b>${bankName(st.bank)}</b></span>`,
              st.type!=='all'?`<span class="statchip">${TYPE_NAME[st.type]}</span>`:'',
              `<span class="statchip">${MODE_TAG[st.mode]} · 已刷 <b>${s.done}</b>/${s.total} · 答对 <b>${s.ok}</b>${s.rate!==null?' · 正确率 <b>'+s.rate+'%</b>':''}</span>`];
  if(st.search.trim()) bits.push(`<button class="statchip link" id="clearKw">「${esc(st.search.trim())}」✕</button>`);
  bits.push(`<span class="statchip link" id="toStats">📊 全库统计 ›</span>`);
  document.getElementById('stats').innerHTML = bits.filter(Boolean).join(' ');
}
function render(){
  renderStats();
  refreshCounts();
  const card = document.getElementById('card');
  const q = cur();
  if(!q){
    const msg = st.mode==='wrong' ? ['🎉','错题本是空的，太棒了！']
              : st.mode==='star'  ? ['⭐','还没有收藏的题目，刷题时点题目旁的 ☆ 收藏。']
              : ['🔍','没有匹配的题目。'];
    card.innerHTML = `<div class="empty-big"><span class="em">${msg[0]}</span>${msg[1]}</div>`;
    document.getElementById('prevBtn').disabled = true;
    document.getElementById('nextBtn').disabled = true;
    return;
  }
  const aid = qid(q), shown = S.reveal;
  const picked = [...st.sel];
  const graded = st.graded;
  let h = `<div class="meta"><span class="chin bank">${bankName(q.k)}</span>
    <span class="chin gray">第 ${q.s} 题</span><span class="chin gray">${TYPE_NAME[q.t]}</span>
    ${q.d===2?'<span class="chin fixed">已修正 · 平台原答案有误</span>':q.d===1?'<span class="chin warn">存疑题 · 看解析</span>':''}
    <button class="star ${S.starred[aid]?'on':''}" id="starNow">${S.starred[aid]?'★':'☆'}</button></div>
    <div class="stem">${esc(q.q)}</div><div class="opts">`;
  const ansSet = new Set(q.a.split(''));
  q.o.forEach((t,i)=>{
    const L = LT[i];
    let cls = 'opt';
    if(!graded && !shown && picked.includes(L)) cls += ' sel';
    if(graded || shown){
      if(ansSet.has(L)) cls += ' ok';
      else if(picked.includes(L)) cls += ' bad';
    }
    h += `<div class="${cls}" data-l="${L}"><span class="letter">${L}.</span><span>${esc(t)}</span></div>`;
  });
  h += '</div>';
  if(q.t==='多选' && !graded && !shown && picked.length)
    h += `<div class="multi-note">已选 ${picked.join('、')}（<button class="btn primary" id="submitBtn">提交答案</button>）</div>`;
  if(graded){
    const right = graded === 'ok';
    h += `<div class="verdict ${right?'ok':'bad'}">${right?'✅ 回答正确':'❌ 回答错误'}　正确答案：${q.a.split('').join('、')}</div>`;
    h += `<div class="why">📝 ${esc(q.n)||'（本题暂无解析）'}</div>`;
  } else if(shown){
    h += `<div class="why">📖 答案：${q.a.split('').join('、')}　📝 ${esc(q.n)||'（本题暂无解析）'}</div>`;
  } else if(q.t==='多选'){
    h += `<div class="multi-note">多选题：点选后提交</div>`;
  }
  card.innerHTML = h;
  card.classList.toggle('locked', !!graded || shown);
  const noList = st.list.length===0;
  document.getElementById('prevBtn').disabled = noList || st.idx<=0;
  document.getElementById('nextBtn').disabled = noList || st.idx>=st.list.length-1;
  document.getElementById('jumpNo').value = q.s;
  document.getElementById('starNow').onclick = toggleStar;
  const sb = document.getElementById('submitBtn');
  if(sb) sb.onclick = gradeMulti;
  if(graded==='ok' && document.getElementById('autoNext').checked){
    setTimeout(()=>{ if(st.graded==='ok') step(1); }, 700);
  }
  if(!graded && !shown){
    card.querySelectorAll('.opt').forEach(el => el.onclick = ()=>{
      const L = el.dataset.l;
      if(q.t==='多选'){ toggleSel(L); render(); } else { gradeSingle(L); }
    });
  } else {
    card.querySelectorAll('.opt').forEach(el => el.onclick = null);
  }
}
function toggleSel(L){ if(st.sel.has(L)) st.sel.delete(L); else st.sel.add(L); }
function gradeSingle(L){ const q = cur(); if(!q) return; st.sel = new Set([L]); finishGrade(); }
function gradeMulti(){ const q = cur(); if(!q || !st.sel.size) return; finishGrade(); }
function finishGrade(){
  const q = cur(); if(!q) return;
  const picked = [...st.sel].sort().join('');
  const right = picked === q.a.split('').sort().join('');
  st.graded = right ? 'ok' : 'bad';
  S.answered[qid(q)] = right ? 1 : 0;
  save(); render();
}
function step(d){
  const ni = st.idx + d;
  if(ni<0 || ni>=st.list.length) return;
  st.idx = ni; st.sel = new Set(); st.graded = null;
  S.pos = S.pos || {}; S.pos[scopeKey()+'|'+st.mode] = st.idx; save();
  window.scrollTo({top:0});
  render();
}
function jumpTo(no){
  const i = st.list.findIndex(q=>q.s===no);
  if(i>=0){ st.idx=i; st.sel=new Set(); st.graded=null; window.scrollTo({top:0}); render(); }
}
function toggleStar(){
  const q = cur(); if(!q) return;
  const id = qid(q);
  if(S.starred[id]) delete S.starred[id]; else S.starred[id]=1;
  save(); render();
}
function refreshCounts(){
  const nw = wrongIds().length, ns = starIds().length;
  document.getElementById('nWrong').textContent = nw; document.getElementById('nWrong').classList.toggle('zero', !nw);
  document.getElementById('hWrongN').textContent = nw;
  document.getElementById('nStar').textContent = ns; document.getElementById('nStar').classList.toggle('zero', !ns);
  document.getElementById('hStarN').textContent = ns;
  document.getElementById('wHeadN').textContent = nw;
  document.getElementById('sHeadN').textContent = ns;
}
/* ===== 抽屉 ===== */
const openSheet  = id => document.getElementById(id).classList.add('open');
const closeSheet = id => document.getElementById(id).classList.remove('open');
function renderBook(kind){
  const ids = kind==='wrong' ? wrongIds() : starIds();
  const el = document.getElementById(kind==='wrong' ? 'wList' : 'sList');
  const emptyTxt = kind==='wrong' ? '错题本是空的，太棒了！' : '还没有收藏的题目，刷题时点题目旁的 ☆ 收藏。';
  if(!ids.length){ el.innerHTML = `<div class="empty-big"><span class="em">${kind==='wrong'?'🎉':'⭐'}</span>${emptyTxt}</div>`; return; }
  const byBank = {};
  ids.forEach(id => { const q = QMAP[id]; if(q){ (byBank[q.k] = byBank[q.k] || []).push(q); } });
  el.innerHTML = BANKS.filter(b=>byBank[b.k]).map(b =>
    `<div class="pgroup">${b.n}（${byBank[b.k].length}）</div>` +
    byBank[b.k].map(q => `
      <div class="item" data-jump="${qid(q)}" data-kind="${kind}">
        <div class="info"><div class="meta">第 ${q.s} 题 · ${TYPE_NAME[q.t]}${q.d===2?' · 已修正':q.d===1?' · 存疑':''}</div>
          <div class="t">${esc(q.q)}</div></div>
        <span class="go">›</span>
        <button class="iwbtn" data-rm="${qid(q)}" data-kind="${kind}">${kind==='wrong'?'移出':'✕'}</button>
      </div>`).join('')
  ).join('');
}
function stripJump(id, mode){
  const q = QMAP[id]; if(!q) return;
  st.bank = q.k; st.type = q.t; st.mode = mode; st.search = '';
  document.getElementById('bankSel').value = st.bank;
  document.getElementById('typeSel').value = st.type;
  document.getElementById('search').value = '';
  document.querySelectorAll('#modeSeg button').forEach(b => b.classList.toggle('on', b.dataset.m === mode));
  st.sel = new Set(); st.graded = null; st.idx = 0;
  rebuild();
  const i = st.list.findIndex(x => qid(x) === id);
  if(i>=0){ st.idx = i; S.pos = S.pos || {}; S.pos[scopeKey()+'|'+st.mode] = st.idx; save(); }
  window.scrollTo({top:0}); render();
}
function renderStatsSheet(){
  const per = BANKS.filter(b=>b.k!=='all').map(b => {
    const qs = RAW.filter(q=>q.k===b.k);
    const done = qs.filter(q => qid(q) in S.answered);
    const ok = done.filter(q => S.answered[qid(q)]===1).length;
    return {n:b.n, total:qs.length, done:done.length, ok, acc: done.length?Math.round(100*ok/done.length):null};
  });
  const ALL = per.reduce((a,x)=>({done:a.done+x.done, ok:a.ok+x.ok}), {done:0,ok:0});
  const all = {n:'全部题库', total:RAW.length, done:ALL.done, ok:ALL.ok, acc: ALL.done?Math.round(100*ALL.ok/ALL.done):null};
  const card = x => `
    <div class="statcard">
      <div class="nm">${x.n}<span>${x.done}/${x.total} 题 · 正确率 ${x.acc===null?'—':x.acc+'%'}</span></div>
      <div class="srow"><span class="lbl">已刷</span><div class="sbar done"><i style="width:${x.total?Math.round(100*x.done/x.total):0}%"></i></div></div>
      <div class="srow"><span class="lbl">正确</span><div class="sbar acc"><i style="width:${x.acc===null?0:x.acc}%"></i></div></div>
    </div>`;
  document.getElementById('statsBody').innerHTML = card(all) + card(per[0]) + card(per[1]) + card(per[2]) + card(per[3]);
}
/* ===== 事件 ===== */
document.getElementById('modeSeg').addEventListener('click', e => {
  if(e.target.dataset.m) setMode(e.target.dataset.m);
});
document.getElementById('bankSel').onchange = e => { st.bank=e.target.value; st.idx=0; st.sel=new Set(); st.graded=null; rebuild(); };
document.getElementById('typeSel').onchange = e => { st.type=e.target.value; st.idx=0; st.sel=new Set(); st.graded=null; rebuild(); };
document.getElementById('search').oninput = e => { st.search=e.target.value; st.idx=0; st.sel=new Set(); st.graded=null; rebuild(); };
document.getElementById('autoNext').onchange = e => { S.autoNext=e.target.checked; save(); };
document.getElementById('revealChk').onchange = e => { S.reveal=e.target.checked; save(); st.sel=new Set(); st.graded=null; render(); };
document.getElementById('resetBtn').onclick = () => {
  if(!confirm('确定清空全部答题记录和收藏吗？')) return;
  S.answered={}; S.starred={}; S.pos={}; save();
  st.idx=0; st.sel=new Set(); st.graded=null; rebuild();
};
document.getElementById('prevBtn').onclick = () => step(-1);
document.getElementById('nextBtn').onclick = () => step(1);
document.getElementById('jumpBtn').onclick = () => { const v=parseInt(document.getElementById('jumpNo').value); if(v) jumpTo(v); };
document.getElementById('jumpNo').onkeydown = e => { if(e.key==='Enter') jumpTo(parseInt(e.target.value)); };
document.getElementById('stats').addEventListener('click', e => {
  if(e.target.id==='clearKw'){ st.search=''; document.getElementById('search').value=''; rebuild(); }
  if(e.target.id==='toStats'){ renderStatsSheet(); openSheet('sheetStats'); }
});
document.getElementById('hWrong').onclick = () => { renderBook('wrong'); openSheet('sheetWrong'); };
document.getElementById('hStar').onclick  = () => { renderBook('star'); openSheet('sheetStar'); };
document.getElementById('hSet').onclick   = () => openSheet('sheetSet');
document.querySelectorAll('#tabbar .tab-item').forEach(t => t.onclick = () => {
  const tab = t.dataset.tab;
  if(tab==='quiz'){ window.scrollTo({top:0}); render(); }
  if(tab==='wrong'){ renderBook('wrong'); openSheet('sheetWrong'); }
  if(tab==='star'){ renderBook('star'); openSheet('sheetStar'); }
  if(tab==='set'){ openSheet('sheetSet'); }
});
document.getElementById('wClose').onclick = () => closeSheet('sheetWrong');
document.getElementById('sClose').onclick = () => closeSheet('sheetStar');
document.getElementById('setClose').onclick = () => closeSheet('sheetSet');
document.getElementById('tClose').onclick = () => closeSheet('sheetStats');
['sheetWrong','sheetStar','sheetSet','sheetStats'].forEach(id => {
  document.getElementById(id).addEventListener('click', e => { if(e.target.id===id) closeSheet(id); });
});
document.getElementById('wRetry').onclick = () => {
  st.bank='all'; st.type='all'; st.search=''; setMode('wrong');
  document.getElementById('bankSel').value='all'; document.getElementById('typeSel').value='all';
  document.getElementById('search').value=''; closeSheet('sheetWrong'); window.scrollTo({top:0});
};
document.getElementById('wClear').onclick = () => {
  if(!confirm('清空全部错题记录吗？这些题会回到“未刷”状态。')) return;
  wrongIds().forEach(id => delete S.answered[id]); save(); renderBook('wrong'); render();
};
document.getElementById('sRetry').onclick = () => {
  st.bank='all'; st.type='all'; st.search=''; setMode('star');
  document.getElementById('bankSel').value='all'; document.getElementById('typeSel').value='all';
  document.getElementById('search').value=''; closeSheet('sheetStar'); window.scrollTo({top:0});
};
document.getElementById('sClear').onclick = () => {
  if(!confirm('清空全部收藏吗？')) return;
  starIds().forEach(id => delete S.starred[id]); save(); renderBook('star'); render();
};
document.getElementById('wList').addEventListener('click', e => {
  const rm = e.target.closest('[data-rm]');
  if(rm){ delete S.answered[rm.dataset.rm]; save(); renderBook('wrong'); render(); return; }
  const it = e.target.closest('[data-jump]');
  if(it){ stripJump(it.dataset.jump, 'wrong'); closeSheet('sheetWrong'); }
});
document.getElementById('sList').addEventListener('click', e => {
  const rm = e.target.closest('[data-rm]');
  if(rm){ delete S.starred[rm.dataset.rm]; save(); renderBook('star'); render(); return; }
  const it = e.target.closest('[data-jump]');
  if(it){ stripJump(it.dataset.jump, 'star'); closeSheet('sheetStar'); }
});
document.addEventListener('keydown', e => {
  if(e.key==='Escape'){ ['sheetWrong','sheetStar','sheetSet','sheetStats'].forEach(closeSheet); return; }
  if(['INPUT','SELECT','TEXTAREA'].includes(e.target.tagName)) return;
  if(document.querySelector('.mask.open')) return;
  if(e.key==='ArrowLeft') step(-1);
  else if(e.key==='ArrowRight') step(1);
  else if(e.key==='Enter' && st.graded) step(1);
  else if(/^[1-6]$/.test(e.key)){
    const q = cur(); if(!q || st.graded || S.reveal) return;
    const i = parseInt(e.key)-1;
    if(!q.o[i]) return;
    if(q.t==='多选'){ toggleSel(LT[i]); render(); } else gradeSingle(LT[i]);
  }
});
document.getElementById('autoNext').checked = !!S.autoNext;
document.getElementById('revealChk').checked = !!S.reveal;
buildBankSel();
document.querySelectorAll('#modeSeg button').forEach(b => b.classList.toggle('on', b.dataset.m === st.mode));
rebuild();
</script>
</body>
</html>
'''

html = TEMPLATE.replace('__DATA__', json.dumps(data, ensure_ascii=False).replace('<', '\\u003c'))
out = os.path.join(HERE, 'index.html')
open(out, 'w', encoding='utf-8').write(html)
print('已生成', out, '大小 %.1f KB' % (os.path.getsize(out)/1024))
