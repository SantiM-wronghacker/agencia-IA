"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Dashboard web de la Agencia Santi. Muestra en tiempo real el estado
             de todos los agentes, permite ejecutarlos desde el navegador, ve logs
             en vivo y estadísticas. Se sirve desde localhost:8080.
TECNOLOGÍA: http.server (stdlib), HTML/CSS/JS embebido
"""



import os
import json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
PUERTO    = 8080
API_URL   = "http://localhost:8000"
API_KEY   = "santi-agencia-2026"

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Agencia Santi — Control</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', sans-serif; background: #0d1117; color: #e6edf3; }
  header { background: #161b22; border-bottom: 1px solid #30363d; padding: 14px 24px;
           display: flex; justify-content: space-between; align-items: center; }
  header h1 { font-size: 1.1rem; color: #58a6ff; }
  .badge { background: #238636; color: #fff; padding: 3px 10px;
           border-radius: 20px; font-size: 0.75rem; }
  .badge.warn { background: #9e6a03; }
  .badge.err  { background: #da3633; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px,1fr));
          gap: 16px; padding: 20px; }
  .card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 18px; }
  .card h3 { font-size: 0.8rem; color: #8b949e; text-transform: uppercase;
             letter-spacing: .5px; margin-bottom: 8px; }
  .card .num { font-size: 2rem; font-weight: 700; color: #58a6ff; }
  .card .sub { font-size: 0.8rem; color: #8b949e; margin-top: 4px; }
  .tabs { display: flex; gap: 4px; padding: 0 20px; border-bottom: 1px solid #30363d; }
  .tab { padding: 10px 18px; cursor: pointer; font-size: 0.85rem;
         border-bottom: 2px solid transparent; color: #8b949e; }
  .tab.active { color: #58a6ff; border-color: #58a6ff; }
  .panel { display: none; padding: 20px; }
  .panel.active { display: block; }
  table { width: 100%; border-collapse: collapse; font-size: 0.83rem; }
  th { background: #161b22; color: #8b949e; padding: 10px 14px;
       text-align: left; border-bottom: 1px solid #30363d; position: sticky; top: 0; }
  td { padding: 9px 14px; border-bottom: 1px solid #21262d; }
  tr:hover td { background: #1c2128; }
  .dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 6px; }
  .dot.ok   { background: #3fb950; }
  .dot.warn { background: #d29922; }
  .dot.err  { background: #f85149; }
  .area-tag { background: #1f3a5f; color: #79c0ff; padding: 2px 8px;
              border-radius: 4px; font-size: 0.75rem; }
  input, select, textarea {
    background: #0d1117; border: 1px solid #30363d; color: #e6edf3;
    padding: 8px 12px; border-radius: 6px; font-size: 0.85rem; width: 100%; }
  button { background: #238636; color: #fff; border: none; padding: 9px 20px;
           border-radius: 6px; cursor: pointer; font-size: 0.85rem; }
  button:hover { background: #2ea043; }
  button.sec { background: #21262d; border: 1px solid #30363d; }
  button.sec:hover { background: #30363d; }
  .row { display: flex; gap: 12px; margin-bottom: 12px; align-items: flex-end; }
  .field { flex: 1; }
  .field label { display: block; font-size: 0.78rem; color: #8b949e; margin-bottom: 5px; }
  #output-box { background: #0d1117; border: 1px solid #30363d; border-radius: 6px;
                padding: 16px; min-height: 120px; font-family: monospace;
                font-size: 0.82rem; white-space: pre-wrap; margin-top: 16px;
                color: #3fb950; max-height: 400px; overflow-y: auto; }
  #log-box { background: #0d1117; border: 1px solid #30363d; border-radius: 6px;
             padding: 14px; height: 420px; overflow-y: auto; font-family: monospace;
             font-size: 0.78rem; }
  .log-line { margin-bottom: 3px; }
  .log-line.ok   { color: #3fb950; }
  .log-line.warn { color: #d29922; }
  .log-line.err  { color: #f85149; }
  .log-line.info { color: #8b949e; }
  #search { margin-bottom: 14px; }
  .spinner { display: inline-block; width: 14px; height: 14px;
             border: 2px solid #30363d; border-top-color: #58a6ff;
             border-radius: 50%; animation: spin .7s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }
  footer { text-align: center; color: #30363d; font-size: 0.75rem; padding: 20px; }
  .chat-box { display: flex; flex-direction: column; height: 460px; }
  .chat-msgs { flex: 1; overflow-y: auto; padding: 14px; background: #0d1117;
               border: 1px solid #30363d; border-radius: 6px; margin-bottom: 12px; }
  .msg { margin-bottom: 12px; }
  .msg .quien { font-size: 0.75rem; color: #8b949e; margin-bottom: 4px; }
  .msg .texto { background: #1c2128; padding: 10px 14px; border-radius: 6px;
                font-size: 0.85rem; white-space: pre-wrap; }
  .msg.user .texto { background: #1f3a5f; }
  .chat-input { display: flex; gap: 10px; }
  .chat-input input { flex: 1; }
</style>
</head>
<body>

<header>
  <h1>[FABRICA] Agencia Santi — Torre de Control</h1>
  <div style="display:flex;gap:10px;align-items:center">
    <span id="api-status" class="badge warn">Conectando...</span>
    <span style="font-size:0.75rem;color:#8b949e" id="last-update">—</span>
  </div>
</header>

<!-- STATS -->
<div class="grid" id="stats-grid">
  <div class="card"><h3>Agentes Totales</h3><div class="num" id="s-total">—</div><div class="sub">registrados en habilidades.json</div></div>
  <div class="card"><h3>Saludables</h3><div class="num" id="s-ok">—</div><div class="sub">estado OK</div></div>
  <div class="card"><h3>Areas</h3><div class="num" id="s-areas">—</div><div class="sub">categorias activas</div></div>
  <div class="card"><h3>Log Size</h3><div class="num" id="s-log">—</div><div class="sub">registro_noche.txt</div></div>
</div>

<!-- TABS -->
<div class="tabs">
  <div class="tab active" onclick="tab('agentes')">Agentes</div>
  <div class="tab" onclick="tab('ejecutar')">Ejecutar</div>
  <div class="tab" onclick="tab('clawbot')">Clawbot</div>
  <div class="tab" onclick="tab('logs')">Logs en vivo</div>
</div>

<!-- PANEL: AGENTES -->
<div class="panel active" id="panel-agentes">
  <input id="search" type="text" placeholder="Buscar agente..." oninput="filtrarAgentes(this.value)">
  <div style="overflow-x:auto">
    <table>
      <thead><tr><th>Archivo</th><th>Area</th><th>Descripcion</th><th>Salud</th><th>Accion</th></tr></thead>
      <tbody id="tabla-agentes"></tbody>
    </table>
  </div>
</div>

<!-- PANEL: EJECUTAR -->
<div class="panel" id="panel-ejecutar">
  <div class="row">
    <div class="field">
      <label>Agente</label>
      <select id="sel-agente"><option value="">Cargando...</option></select>
    </div>
    <div class="field">
      <label>Parametros (separados por espacio)</label>
      <input id="inp-params" type="text" placeholder="ej: 2000000 10 20">
    </div>
    <button onclick="ejecutarAgente()">> Ejecutar</button>
  </div>
  <div id="output-box">El output aparecera aqui...</div>
</div>

<!-- PANEL: CLAWBOT -->
<div class="panel" id="panel-clawbot">
  <div class="chat-box">
    <div class="chat-msgs" id="chat-msgs">
      <div class="msg">
        <div class="quien">Sistema</div>
        <div class="texto">Clawbot listo. Escribe tu consulta en lenguaje natural.
Ejemplo: "Analiza depa de 2M en Polanco, hipoteca 20 años al 10%"</div>
      </div>
    </div>
    <div class="chat-input">
      <input id="chat-input" type="text" placeholder="Escribe tu consulta..."
             onkeydown="if(event.key==='Enter') enviarConsulta()">
      <button onclick="enviarConsulta()">Enviar</button>
    </div>
  </div>
</div>

<!-- PANEL: LOGS -->
<div class="panel" id="panel-logs">
  <div style="display:flex;gap:10px;margin-bottom:12px">
    <button onclick="cargarLog()">Actualizar</button>
    <button class="sec" onclick="document.getElementById('log-box').innerHTML=''">Limpiar vista</button>
    <label style="display:flex;align-items:center;gap:6px;font-size:0.83rem">
      <input type="checkbox" id="auto-refresh" checked onchange="toggleAutoLog(this)"> Auto-refresh 5s
    </label>
  </div>
  <div id="log-box"></div>
</div>

<footer>Agencia Santi API — localhost:8000 &bull; Dashboard — localhost:8080</footer>

<script>
const API = 'http://localhost:8000';
const KEY = 'santi-agencia-2026';
const H   = { 'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json' };

let todosAgentes = [];
let logTimer = null;

// -- Tabs --------------------------------------
function tab(nombre) {
  document.querySelectorAll('.tab').forEach((t,i) => {
    const panels = ['agentes','ejecutar','clawbot','logs'];
    t.classList.toggle('active', panels[i] === nombre);
  });
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.getElementById('panel-' + nombre).classList.add('active');
  if (nombre === 'logs') cargarLog();
}

// -- Fetch con manejo de errores ---------------
async function api(ruta, opts={}) {
  try {
    const r = await fetch(API + ruta, { headers: H, ...opts });
    return await r.json();
  } catch(e) {
    return null;
  }
}

// -- Estado del sistema ------------------------
async function actualizarStatus() {
  const data = await api('/status');
  if (!data) {
    document.getElementById('api-status').className = 'badge err';
    document.getElementById('api-status').textContent = 'Sin conexion';
    return;
  }
  document.getElementById('api-status').className = 'badge';
  document.getElementById('api-status').textContent = 'Online';
  document.getElementById('s-total').textContent = data.agentes?.total ?? '—';
  document.getElementById('s-ok').textContent    = data.agentes?.saludables ?? '—';
  document.getElementById('s-log').textContent   = (data.log_size_mb ?? '—') + ' MB';
  document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
}

// -- Tabla de agentes --------------------------
async function cargarAgentes() {
  const [ag, ar] = await Promise.all([api('/agentes'), api('/areas')]);
  if (!ag) return;
  document.getElementById('s-areas').textContent = ar ? ar.total_areas : '—';
  todosAgentes = ag.agentes || [];

  // Llenar selector
  const sel = document.getElementById('sel-agente');
  sel.innerHTML = todosAgentes.map(a =>
    `<option value="${a.archivo}">${a.archivo} [${a.area}]</option>`
  ).join('');

  renderTabla(todosAgentes);
}

function renderTabla(agentes) {
  const tbody = document.getElementById('tabla-agentes');
  tbody.innerHTML = agentes.map(a => `
    <tr>
      <td style="font-family:monospace;font-size:0.8rem">${a.archivo}</td>
      <td><span class="area-tag">${a.area}</span></td>
      <td style="color:#8b949e;font-size:0.8rem">${(a.descripcion||'').slice(0,80)}</td>
      <td><span class="dot ok"></span>OK</td>
      <td><button class="sec" style="padding:4px 10px;font-size:0.75rem"
          onclick="ejecutarRapido('${a.archivo}')">></button></td>
    </tr>
  `).join('');
}

function filtrarAgentes(q) {
  const f = q.toLowerCase();
  renderTabla(todosAgentes.filter(a =>
    a.archivo.toLowerCase().includes(f) ||
    (a.area||'').toLowerCase().includes(f) ||
    (a.descripcion||'').toLowerCase().includes(f)
  ));
}

function ejecutarRapido(archivo) {
  document.getElementById('sel-agente').value = archivo;
  tab('ejecutar');
  ejecutarAgente();
}

// -- Ejecutar agente ---------------------------
async function ejecutarAgente() {
  const agente = document.getElementById('sel-agente').value;
  const params = document.getElementById('inp-params').value;
  const box    = document.getElementById('output-box');
  if (!agente) return;
  box.textContent = 'Ejecutando ' + agente + '...';
  const data = await api('/ejecutar', {
    method: 'POST',
    body: JSON.stringify({ agente, params })
  });
  if (!data) { box.textContent = 'Error: no se pudo conectar a la API'; return; }
  box.textContent = data.exito
    ? data.output
    : 'ERROR: ' + data.output;
  box.style.color = data.exito ? '#3fb950' : '#f85149';
}

// -- Clawbot -----------------------------------
async function enviarConsulta() {
  const inp     = document.getElementById('chat-input');
  const msgs    = document.getElementById('chat-msgs');
  const mensaje = inp.value.trim();
  if (!mensaje) return;
  inp.value = '';

  // Mensaje del usuario
  msgs.innerHTML += `<div class="msg user">
    <div class="quien">Tu</div>
    <div class="texto">${mensaje}</div>
  </div>`;

  // Spinner
  const id = 'msg-' + Date.now();
  msgs.innerHTML += `<div class="msg" id="${id}">
    <div class="quien">Clawbot</div>
    <div class="texto"><span class="spinner"></span> Procesando...</div>
  </div>`;
  msgs.scrollTop = msgs.scrollHeight;

  const data = await api('/consulta', {
    method: 'POST',
    body: JSON.stringify({ mensaje })
  });

  const el = document.getElementById(id);
  if (el) {
    el.querySelector('.texto').textContent = data?.respuesta || 'Sin respuesta';
  }
  msgs.scrollTop = msgs.scrollHeight;
}

// -- Logs en vivo ------------------------------
async function cargarLog() {
  const data = await api('/status');
  if (!data) return;
  const box = document.getElementById('log-box');
  const lineas = data.ultimas_actividades || [];
  box.innerHTML = lineas.map(l => {
    let cls = 'info';
    if (l.includes('OK') || l.includes('completado')) cls = 'ok';
    else if (l.includes('WARN') || l.includes('fallo')) cls = 'warn';
    else if (l.includes('ERROR') || l.includes('critico')) cls = 'err';
    return `<div class="log-line ${cls}">${l}</div>`;
  }).join('');
  box.scrollTop = box.scrollHeight;
}

function toggleAutoLog(cb) {
  if (cb.checked) {
    logTimer = setInterval(cargarLog, 5000);
  } else {
    clearInterval(logTimer);
  }
}

// -- Inicializar -------------------------------
(async () => {
  await actualizarStatus();
  await cargarAgentes();
  setInterval(actualizarStatus, 30000);
  logTimer = setInterval(cargarLog, 5000);
})();
</script>
</body>
</html>"""

class DashboardHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass
    def do_GET(self):
        body = HTML.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

def iniciar_dashboard():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Dashboard en http://localhost:{PUERTO}")
    srv = HTTPServer(("0.0.0.0", PUERTO), DashboardHandler)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.server_close()

if __name__ == "__main__":
    iniciar_dashboard()