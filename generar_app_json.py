#!/usr/bin/env python3
"""
Variante con datos externos.

Reparto de archivos:
  datos/episodios.json  -> lista de los 227 capitulos y cuantas palabras trae
                           cada uno. Necesario de entrada para pintar la rejilla.
  datos/lexico.json     -> las 5.307 palabras, con su episodio de debut y los
                           indices de capitulos donde aparecen. Permite que la
                           busqueda global y el filtro "solo nuevas" funcionen
                           sin descargar las diez temporadas.
  datos/t01.json .. t10 -> frecuencia por episodio. Se descarga solo la
                           temporada que se consulta y queda en cache.
"""
import csv, json
from collections import defaultdict
from pathlib import Path

filas = list(csv.DictReader(open("salida_v5/_consolidado.csv", encoding="utf-8-sig")))

def orden(ep):
    return (int(ep[1:3]), int(ep.split("E")[1].split("-")[0]))

por_ep = defaultdict(list)
for r in filas:
    por_ep[r["episodio"]].append(r)
eps = sorted(por_ep, key=orden)
pos_ep = {e: k for k, e in enumerate(eps)}

idx, lexico, aparece, debut = {}, [], defaultdict(list), {}
frec_temp = defaultdict(dict)

for e in eps:                                   # recorrido cronologico
    for r in por_ep[e]:
        l = r["lema"]
        if l not in idx:
            idx[l] = len(lexico)
            lexico.append([l, r["pos"], r["ipa"], r["espanol"], r["forma_estandar"],
                           r["idioma_origen"], int(r["frec_total"])])
            debut[idx[l]] = pos_ep[e]
        aparece[idx[l]].append(pos_ep[e])
        frec_temp[orden(e)[0]].setdefault(e, []).append([idx[l], int(r["frec_episodio"])])

destino = Path("/mnt/user-data/outputs/app")
(destino / "datos").mkdir(parents=True, exist_ok=True)

def escribir(nombre, obj):
    p = destino / "datos" / nombre
    p.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return p.stat().st_size

pesos = {}
pesos["episodios.json"] = escribir("episodios.json",
    [{"id": e, "t": orden(e)[0], "n": orden(e)[1], "c": len(por_ep[e])} for e in eps])
plano = "\n".join("\t".join(str(c) for c in fila) for fila in lexico)
pesos["lexico.json"] = escribir("lexico.json",
    {"l": plano, "d": [debut[i] for i in range(len(lexico))]})
pesos["ubicaciones.json"] = escribir("ubicaciones.json",
    [aparece[i] for i in range(len(lexico))])
for t in range(1, 11):
    pesos[f"t{t:02d}.json"] = escribir(f"t{t:02d}.json", frec_temp[t])

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Léxico de Friends · vocabulario por episodio</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&family=Gentium+Book+Plus:wght@400;700&display=swap" rel="stylesheet">
<link rel="preload" as="fetch" href="datos/lexico.json" crossorigin>
<style>
:root{
  --tinta:#231A2B; --ciruela:#412A4C; --ciruela-claro:#5E4270;
  --papel:#F3F1F5; --tarjeta:#FFFFFF; --linea:#DED8E4;
  --ambar:#C97A05; --verde:#1F6B4C; --tenue:#7C7188;
  --display:"Bricolage Grotesque",system-ui,sans-serif;
  --texto:"IBM Plex Sans",system-ui,sans-serif;
  --dato:"IBM Plex Mono",ui-monospace,monospace;
  --fonetica:"Gentium Book Plus","Charis SIL",Georgia,serif;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:var(--papel);color:var(--tinta);font-family:var(--texto);font-size:15px;line-height:1.5}
header{background:var(--ciruela);color:#F6F1F8;padding:18px 22px}
.cab{display:flex;gap:18px;align-items:baseline;flex-wrap:wrap;max-width:1400px;margin:0 auto}
h1{font-family:var(--display);font-weight:800;font-size:22px;letter-spacing:-.02em;margin:0}
h1 span{font-weight:400;opacity:.65}
.totales{font-family:var(--dato);font-size:12px;opacity:.7;margin-left:auto}
.marco{max-width:1400px;margin:0 auto;padding:22px;display:grid;grid-template-columns:180px 1fr;gap:22px;align-items:start}
@media(max-width:860px){.marco{grid-template-columns:1fr;padding:14px;gap:14px}}
.temporadas{position:sticky;top:16px;display:flex;flex-direction:column;gap:4px}
@media(max-width:860px){.temporadas{position:static;flex-direction:row;overflow-x:auto;padding-bottom:6px}}
.temp{appearance:none;border:1px solid transparent;background:transparent;text-align:left;
  padding:9px 12px;border-radius:8px;cursor:pointer;font:inherit;color:var(--tinta);
  display:flex;justify-content:space-between;gap:10px;white-space:nowrap}
.temp:hover{background:#E7E2EC}
.temp[aria-current="true"]{background:var(--tinta);color:#F6F1F8}
.temp b{font-family:var(--display);font-weight:600}
.temp i{font-family:var(--dato);font-size:11px;font-style:normal;opacity:.6}
.rejilla{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:18px;min-height:38px}
.epi{width:42px;height:38px;border:1px solid var(--linea);background:var(--tarjeta);border-radius:7px;
  cursor:pointer;font-family:var(--dato);font-size:12px;color:var(--tinta);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1px;padding:0;
  transition:transform .12s ease}
.epi u{text-decoration:none;font-size:9px;opacity:.5}
.epi:hover{transform:translateY(-2px);border-color:var(--ciruela-claro)}
.epi[aria-current="true"]{background:var(--tinta);color:#F6F1F8;border-color:var(--tinta)}
.controles{background:var(--tarjeta);border:1px solid var(--linea);border-radius:12px;padding:14px;margin-bottom:16px}
.fila{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.buscador{flex:1 1 260px;position:relative}
.buscador input{width:100%;padding:10px 12px 10px 34px;border:1px solid var(--linea);border-radius:9px;font:inherit;background:var(--papel)}
.buscador input:focus{outline:2px solid var(--ciruela-claro);outline-offset:1px}
.buscador::before{content:"⌕";position:absolute;left:12px;top:8px;font-size:17px;color:var(--tenue)}
select{padding:9px 10px;border:1px solid var(--linea);border-radius:9px;font:inherit;background:var(--papel)}
.chip{appearance:none;border:1px solid var(--linea);background:var(--papel);border-radius:999px;
  padding:6px 12px;font:inherit;font-size:13px;cursor:pointer;color:var(--tinta)}
.chip[aria-pressed="true"]{background:var(--tinta);color:#F6F1F8;border-color:var(--tinta)}
.chip:focus-visible,.epi:focus-visible,.temp:focus-visible{outline:2px solid var(--ambar);outline-offset:2px}
.panel{background:var(--tarjeta);border:1px solid var(--linea);border-radius:12px;overflow:hidden}
.titulo{padding:14px 16px;border-bottom:1px solid var(--linea);display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.titulo h2{font-family:var(--display);font-size:18px;margin:0;font-weight:600}
.titulo .sub{font-family:var(--dato);font-size:12px;color:var(--tenue)}
table{width:100%;border-collapse:collapse}
th{font-family:var(--dato);font-size:11px;text-transform:uppercase;letter-spacing:.06em;
  color:var(--tenue);text-align:left;padding:9px 16px;border-bottom:1px solid var(--linea);font-weight:500}
td{padding:10px 16px;border-bottom:1px solid #EFEBF2;vertical-align:top}
tbody tr:hover{background:#FAF8FB}
.lema{font-weight:600;font-size:16px}
.pos{font-family:var(--dato);font-size:11px;color:var(--tenue)}
.ipa{font-family:var(--fonetica);font-size:15px;color:var(--ciruela-claro);white-space:nowrap}
.es{color:var(--verde)}
.nota{display:block;font-size:12px;color:var(--tenue);margin-top:2px}
.marca{display:inline-block;font-family:var(--dato);font-size:10px;text-transform:uppercase;
  letter-spacing:.04em;padding:2px 6px;border-radius:5px;margin-left:6px;vertical-align:2px}
.m-nueva{background:#E8F1EC;color:var(--verde)}
.m-col{background:#FBF0DC;color:var(--ambar)}
.m-ext{background:#EDE7F3;color:var(--ciruela-claro)}
.num{font-family:var(--dato);font-size:13px;text-align:right;white-space:nowrap}
.decir{appearance:none;border:1px solid var(--linea);background:var(--tarjeta);
  width:26px;height:26px;border-radius:50%;cursor:pointer;color:var(--ciruela-claro);
  font-size:13px;line-height:1;padding:0;margin-left:8px;vertical-align:1px;
  transition:background .12s ease,color .12s ease}
.decir:hover{background:var(--ciruela);color:#F6F1F8;border-color:var(--ciruela)}
.decir:focus-visible{outline:2px solid var(--ambar);outline-offset:2px}
.decir[data-sonando="1"]{background:var(--ambar);color:#fff;border-color:var(--ambar)}
body.sin-voz .decir{display:none}
.barra{display:block;height:3px;background:var(--ambar);border-radius:2px;margin-top:4px;min-width:2px;opacity:.75}
.aviso{padding:48px 16px;text-align:center;color:var(--tenue)}
.aviso b{display:block;color:var(--tinta);font-weight:600;margin-bottom:6px}
.aviso code{font-family:var(--dato);font-size:13px;background:var(--papel);padding:2px 6px;border-radius:5px}
.cargando{display:inline-block;width:9px;height:9px;border-radius:50%;background:var(--ambar);
  margin-right:7px;animation:latido 1s ease-in-out infinite}
@keyframes latido{0%,100%{opacity:.25}50%{opacity:1}}
footer{max-width:1400px;margin:0 auto;padding:8px 22px 40px;color:var(--tenue);font-size:12px}
kbd{font-family:var(--dato);font-size:11px;border:1px solid var(--linea);border-bottom-width:2px;
  border-radius:4px;padding:1px 5px;background:var(--tarjeta)}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style>
</head>
<body>
<header>
  <div class="cab">
    <h1>Léxico de Friends <span>· vocabulario por episodio</span></h1>
    <div class="totales" id="totales"><span class="cargando"></span>cargando</div>
  </div>
</header>

<div class="marco">
  <nav class="temporadas" id="temporadas" aria-label="Temporadas"></nav>
  <main>
    <div class="rejilla" id="rejilla" aria-label="Episodios"></div>
    <div class="controles">
      <div class="fila">
        <div class="buscador">
          <input id="q" type="search" placeholder="Buscar en inglés o español…"
                 aria-label="Buscar palabra" autocomplete="off">
        </div>
        <select id="orden" aria-label="Ordenar">
          <option value="frec">Más frecuentes primero</option>
          <option value="alfa">Alfabético</option>
          <option value="total">Frecuencia en toda la serie</option>
        </select>
        <select id="cat" aria-label="Categoría gramatical">
          <option value="">Todas las categorías</option>
          <option value="NOUN">Sustantivos</option>
          <option value="VERB">Verbos</option>
          <option value="ADJ">Adjetivos</option>
          <option value="ADV">Adverbios</option>
        </select>
        <button class="chip" id="f-nuevas" aria-pressed="false">Solo nuevas</button>
        <button class="chip" id="f-col" aria-pressed="false">Coloquiales</button>
        <button class="chip" id="f-ext" aria-pressed="false">Extranjerismos</button>
      </div>
    </div>
    <section class="panel">
      <div class="titulo">
        <h2 id="titulo">—</h2><span class="sub" id="subtitulo"></span>
      </div>
      <div id="contenido"><p class="aviso"><span class="cargando"></span>Cargando el vocabulario…</p></div>
    </section>
  </main>
</div>

<footer>
  <kbd>←</kbd> <kbd>→</kbd> cambian de episodio · <kbd>/</kbd> va al buscador.
  Filtro de vocabulario básico: Zipf ≤ 4,3.
</footer>

<script>
const $ = s => document.querySelector(s);
const [L_LEMA,L_POS,L_IPA,L_ES,L_STD,L_IDI,L_TOT] = [0,1,2,3,4,5,6];

let EPS = [], LEX = [], DEBUT = [], DONDE = null;
const cacheTemp = new Map();          /* temporada -> {episodio: [[lema,frec]]} */
const estado = { ep:null, temp:1, q:"", orden:"frec", cat:"",
                 nuevas:false, col:false, ext:false };

const IDIOMAS = {frances:"fr-FR", italiano:"it-IT", aleman:"de-DE", espanol:"es-ES"};
const sintesis = window.speechSynthesis;
let voces = [];
function cargarVoces(){ voces = sintesis ? sintesis.getVoices() : []; }
if(sintesis){
  cargarVoces();
  sintesis.addEventListener?.("voiceschanged", cargarVoces);
} else {
  document.body.classList.add("sin-voz");   /* sin soporte, se ocultan los botones */
}

function pronunciar(palabra, idioma, boton){
  if(!sintesis) return;
  sintesis.cancel();
  const frase = new SpeechSynthesisUtterance(palabra);
  frase.lang = idioma;
  frase.rate = 0.9;
  const raiz = idioma.slice(0,2);
  const voz = voces.find(v => v.lang === idioma) || voces.find(v => v.lang.startsWith(raiz));
  if(voz) frase.voice = voz;
  if(boton){
    boton.dataset.sonando = "1";
    frase.onend = frase.onerror = () => delete boton.dataset.sonando;
  }
  sintesis.speak(frase);
}

const esc = s => s.replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

async function traer(ruta){
  const r = await fetch(ruta);
  if(!r.ok) throw new Error(`${ruta} respondió ${r.status}`);
  return r.json();
}

async function temporada(t){
  if(!cacheTemp.has(t)) cacheTemp.set(t, await traer(`datos/t${String(t).padStart(2,"0")}.json`));
  return cacheTemp.get(t);
}

/* ---------- navegación ---------- */
function pintarTemporadas(){
  const cont = $("#temporadas"); cont.innerHTML = "";
  for(let t=1;t<=10;t++){
    const deT = EPS.filter(e=>e.t===t);
    const b = document.createElement("button");
    b.className="temp"; b.type="button";
    b.setAttribute("aria-current", t===estado.temp);
    b.innerHTML = `<b>Temporada ${t}</b><i>${deT.length}</i>`;
    b.onclick = () => irA(deT[0].id);
    cont.appendChild(b);
  }
}

function pintarRejilla(){
  const cont = $("#rejilla"); cont.innerHTML = "";
  const maxC = Math.max(...EPS.map(e=>e.c));
  EPS.filter(e=>e.t===estado.temp).forEach(e=>{
    const b = document.createElement("button");
    b.className="epi"; b.type="button";
    b.setAttribute("aria-current", e.id===estado.ep);
    b.title = `${e.id} · ${e.c} palabras`;
    const d = 0.45 + 0.55*(e.c/maxC);
    b.innerHTML = `<span style="opacity:${d.toFixed(2)}">${String(e.n).padStart(2,"0")}</span><u>${e.c}</u>`;
    b.onclick = () => irA(e.id);
    cont.appendChild(b);
  });
}

async function irA(id){
  estado.ep = id;
  estado.temp = EPS.find(e=>e.id===id).t;
  location.hash = id;
  pintarTemporadas(); pintarRejilla();
  await pintarTabla();
}

/* ---------- tabla ---------- */
async function filasVisibles(){
  const q = estado.q.trim().toLowerCase();
  let base;
  if(q){
    /* las ubicaciones solo se descargan la primera vez que se busca */
    if(!DONDE) DONDE = await traer("datos/ubicaciones.json");
    base = [];
    for(let i=0;i<LEX.length;i++){
      const L = LEX[i];
      if(L[L_LEMA].includes(q) || L[L_ES].toLowerCase().includes(q))
        base.push({i, f:L[L_TOT], eps:DONDE[i].map(k=>EPS[k].id)});
    }
  } else {
    const datos = await temporada(estado.temp);
    base = (datos[estado.ep]||[]).map(([i,f])=>({i,f,eps:null}));
  }
  const posEp = EPS.findIndex(e=>e.id===estado.ep);
  return base.filter(({i})=>{
    const L = LEX[i];
    if(estado.cat && L[L_POS]!==estado.cat) return false;
    if(estado.col && !L[L_STD]) return false;
    if(estado.ext && !L[L_IDI]) return false;
    if(estado.nuevas && DEBUT[i]!==posEp) return false;
    return true;
  }).sort((a,b)=>{
    if(estado.orden==="alfa")  return LEX[a.i][L_LEMA].localeCompare(LEX[b.i][L_LEMA]);
    if(estado.orden==="total") return LEX[b.i][L_TOT]-LEX[a.i][L_TOT];
    return b.f-a.f || LEX[a.i][L_LEMA].localeCompare(LEX[b.i][L_LEMA]);
  });
}

async function pintarTabla(){
  const q = estado.q.trim();
  let filas;
  try { filas = await filasVisibles(); }
  catch(err){
    $("#contenido").innerHTML = `<p class="aviso"><b>No se pudieron cargar los datos</b>
      ${esc(err.message)}. Comprueba que la carpeta <code>datos/</code> esté junto al HTML.</p>`;
    return;
  }
  const ep = EPS.find(e=>e.id===estado.ep);
  $("#titulo").textContent = q ? `Resultados de “${q}”` : ep.id;
  $("#subtitulo").textContent = q
      ? `${filas.length} palabra${filas.length===1?"":"s"} en las 10 temporadas`
      : `${filas.length} de ${ep.c} palabras · temporada ${ep.t}, episodio ${ep.n}`;

  if(!filas.length){
    $("#contenido").innerHTML = `<p class="aviso"><b>Ningún resultado</b>
      Prueba a quitar algún filtro o a buscar otra palabra.</p>`;
    return;
  }
  const posEp = EPS.findIndex(e=>e.id===estado.ep);
  const maxF = Math.max(...filas.map(f=>f.f));
  $("#contenido").innerHTML = `<table><thead><tr>
      <th>Palabra</th><th>Fonética</th><th>Español</th>
      <th class="num">${q?"Total en la serie":"En el episodio"}</th><th class="num">Serie</th>
    </tr></thead><tbody>${filas.map(({i,f,eps})=>{
    const L = LEX[i];
    const marcas =
      (DEBUT[i]===posEp && !q ? '<span class="marca m-nueva">nueva</span>' : "") +
      (L[L_STD] ? '<span class="marca m-col">coloquial</span>' : "") +
      (L[L_IDI] ? `<span class="marca m-ext">${esc(L[L_IDI])}</span>` : "");
    const nota  = L[L_STD] ? `<span class="nota">forma estándar: ${esc(L[L_STD])}</span>` : "";
    const donde = eps ? `<span class="nota">${eps.slice(0,6).join(" · ")}${eps.length>6?" …":""}</span>` : "";
    return `<tr>
      <td><span class="lema">${esc(L[L_LEMA])}</span>${marcas}
          <span class="nota pos">${L[L_POS]}</span>${donde}</td>
      <td class="ipa">${esc(L[L_IPA])}<button class="decir" type="button"
          data-p="${esc(L[L_LEMA])}" data-l="${IDIOMAS[L[L_IDI]]||"en-US"}"
          aria-label="Escuchar ${esc(L[L_LEMA])}" title="Escuchar">&#9654;</button></td>
      <td><span class="es">${esc(L[L_ES])||"—"}</span>${nota}</td>
      <td class="num">${f}<span class="barra" style="width:${Math.max(6,100*f/maxF)}%"></span></td>
      <td class="num">${L[L_TOT]}</td></tr>`;
  }).join("")}</tbody></table>`;
}

/* ---------- eventos ---------- */
$("#q").addEventListener("input", e => { estado.q = e.target.value; pintarTabla(); });
$("#orden").addEventListener("change", e => { estado.orden = e.target.value; pintarTabla(); });
$("#cat").addEventListener("change", e => { estado.cat = e.target.value; pintarTabla(); });
[["#f-nuevas","nuevas"],["#f-col","col"],["#f-ext","ext"]].forEach(([sel,clave])=>{
  $(sel).addEventListener("click", e => {
    estado[clave] = !estado[clave];
    e.currentTarget.setAttribute("aria-pressed", estado[clave]);
    pintarTabla();
  });
});
$("#contenido").addEventListener("click", e => {
  const b = e.target.closest(".decir");
  if(b) pronunciar(b.dataset.p, b.dataset.l, b);
});
document.addEventListener("keydown", e => {
  if(e.target.tagName==="INPUT"||e.target.tagName==="SELECT"){ if(e.key==="Escape") e.target.blur(); return; }
  if(e.key==="/"){ e.preventDefault(); $("#q").focus(); return; }
  const k = EPS.findIndex(x=>x.id===estado.ep);
  if(e.key==="ArrowRight" && k<EPS.length-1) irA(EPS[k+1].id);
  if(e.key==="ArrowLeft"  && k>0)            irA(EPS[k-1].id);
});

/* ---------- arranque ---------- */
(async () => {
  try {
    const [eps, lex] = await Promise.all([traer("datos/episodios.json"), traer("datos/lexico.json")]);
    EPS = eps; DEBUT = lex.d;
    LEX = lex.l.split("\\n").map(r => { const c = r.split("\\t"); c[6] = +c[6]; return c; });
    $("#totales").textContent =
      `${LEX.length.toLocaleString("es")} palabras · ${EPS.length} episodios · 10 temporadas`;
    const inicial = EPS.find(e=>e.id===location.hash.slice(1)) || EPS[0];
    await irA(inicial.id);
  } catch(err){
    $("#totales").textContent = "";
    $("#contenido").innerHTML = `<p class="aviso"><b>No se pudieron cargar los datos</b>
      ${esc(err.message)}.<br>Si has abierto el archivo con doble clic, el navegador bloquea
      la lectura de <code>datos/</code>. Sirve la carpeta con
      <code>python3 -m http.server</code> y entra en <code>localhost:8000</code>.</p>`;
  }
})();
</script>
</body>
</html>
"""

(destino / "index.html").write_text(HTML, encoding="utf-8")
peso_html = (destino / "index.html").stat().st_size
print(f"index.html            : {peso_html/1024:6.1f} KB")
for k, v in pesos.items():
    print(f"datos/{k:18s}: {v/1024:6.1f} KB")
print(f"TOTAL                 : {(peso_html+sum(pesos.values()))/1024:6.1f} KB")
print(f"carga inicial (html+episodios+lexico+t01): "
      f"{(peso_html+pesos['episodios.json']+pesos['lexico.json']+pesos['t01.json'])/1024:.1f} KB")
print(f"  (ubicaciones.json se descarga al primer uso del buscador)")
