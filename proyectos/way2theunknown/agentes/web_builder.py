"""
AREA: WEB
DESCRIPCION: Genera sitio web completo para Way2TheUnknown respetando paleta de colores oficial.
             Crea index.html, destinos.html y servicios.html con CSS/JS vanilla, responsive.
TECNOLOGIA: Python stdlib (pathlib, json, os, sys)
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Paleta oficial de way2theunknown.com
PALETA = {
    "verde_oscuro":  "#647D63",
    "verde_claro":   "#A9C5A0",
    "negro":         "#1A1A1A",
    "gris_oscuro":   "#333333",
    "gris_claro":    "#D9D9D9",
    "beige":         "#E1D9C8",
    "beige_claro":   "#ece6da",
    "blanco_hueso":  "#faf9f7",
    "blanco":        "#ffffff",
    "naranja":       "#f7630c",
    "naranja_dorado":"#f5a524",
}

CSS_BASE = f"""
:root {{
  --verde:       {PALETA['verde_oscuro']};
  --verde-claro: {PALETA['verde_claro']};
  --negro:       {PALETA['negro']};
  --gris:        {PALETA['gris_oscuro']};
  --beige:       {PALETA['beige']};
  --beige-claro: {PALETA['beige_claro']};
  --blanco:      {PALETA['blanco_hueso']};
  --naranja:     {PALETA['naranja']};
  --dorado:      {PALETA['naranja_dorado']};
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',Georgia,sans-serif;background:var(--blanco);color:var(--negro)}}
a{{text-decoration:none;color:inherit}}

/* NAV */
nav{{background:rgba(250,249,247,0.95);backdrop-filter:blur(8px);
     border-bottom:1px solid var(--gris-claro,#D9D9D9);
     padding:16px 40px;display:flex;justify-content:space-between;align-items:center;
     position:sticky;top:0;z-index:100}}
.logo{{font-size:1.35rem;font-weight:700;color:var(--verde);letter-spacing:1px}}
.logo span{{color:var(--naranja)}}
.nav-links{{display:flex;gap:28px;list-style:none}}
.nav-links a{{font-size:.9rem;color:var(--gris);font-weight:500;transition:color .2s}}
.nav-links a:hover{{color:var(--verde)}}
.nav-cta{{background:var(--verde);color:var(--blanco) !important;
          padding:9px 22px;border-radius:25px;font-weight:600 !important}}
.nav-cta:hover{{background:#4a6349 !important}}

/* HERO */
.hero{{background:linear-gradient(135deg,var(--beige) 0%,var(--beige-claro) 60%,var(--verde-claro) 100%);
       padding:100px 40px;text-align:center;min-height:70vh;display:flex;
       flex-direction:column;justify-content:center;align-items:center}}
.hero h1{{font-size:3rem;font-weight:800;color:var(--verde);margin-bottom:16px;line-height:1.15}}
.hero h1 span{{color:var(--naranja)}}
.hero p{{font-size:1.15rem;color:var(--gris);max-width:580px;margin:0 auto 32px;line-height:1.7}}
.btn{{display:inline-block;padding:14px 32px;border-radius:30px;font-size:1rem;
      font-weight:600;cursor:pointer;border:none;transition:all .25s}}
.btn-primary{{background:var(--verde);color:#fff}}
.btn-primary:hover{{background:#4a6349;transform:translateY(-2px)}}
.btn-secondary{{background:transparent;border:2px solid var(--verde);color:var(--verde);margin-left:12px}}
.btn-secondary:hover{{background:var(--verde);color:#fff}}

/* SECCIONES */
section{{padding:80px 40px;max-width:1200px;margin:0 auto}}
.section-title{{text-align:center;margin-bottom:48px}}
.section-title h2{{font-size:2rem;color:var(--verde);margin-bottom:10px}}
.section-title p{{color:var(--gris);font-size:1rem}}

/* GRID DESTINOS */
.destinos-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px}}
.destino-card{{background:#fff;border-radius:14px;overflow:hidden;
               box-shadow:0 4px 16px rgba(0,0,0,.07);transition:transform .25s,box-shadow .25s}}
.destino-card:hover{{transform:translateY(-5px);box-shadow:0 8px 28px rgba(0,0,0,.12)}}
.destino-img{{height:180px;background:var(--verde-claro);display:flex;align-items:center;
              justify-content:center;font-size:3rem}}
.destino-body{{padding:20px}}
.destino-body h3{{font-size:1.1rem;color:var(--negro);margin-bottom:6px}}
.destino-body p{{font-size:.85rem;color:var(--gris);margin-bottom:14px;line-height:1.5}}
.destino-price{{font-size:1.1rem;font-weight:700;color:var(--verde)}}
.destino-price span{{font-size:.78rem;color:var(--gris);font-weight:400}} 
.tag{{background:var(--beige);color:var(--verde);font-size:.72rem;
      padding:3px 10px;border-radius:12px;font-weight:600}}

/* STATS */
.stats-bar{{background:var(--verde);padding:48px 40px}}
.stats-inner{{max-width:1000px;margin:0 auto;display:grid;
              grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:32px;text-align:center}}
.stat h3{{font-size:2.5rem;font-weight:800;color:var(--dorado)}}
.stat p{{color:rgba(255,255,255,.8);font-size:.9rem;margin-top:4px}}

/* FORM */
.form-box{{background:#fff;border-radius:16px;padding:40px;
           box-shadow:0 4px 24px rgba(0,0,0,.08);max-width:700px;margin:0 auto}}
.form-row{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}}
.form-group{{display:flex;flex-direction:column;gap:6px}}
.form-group label{{font-size:.85rem;color:var(--gris);font-weight:600}}
.form-group input,.form-group select,.form-group textarea{{
  border:1.5px solid var(--gris-claro,#D9D9D9);border-radius:8px;
  padding:11px 14px;font-size:.9rem;color:var(--negro);
  background:#fff;transition:border .2s}}
.form-group input:focus,.form-group select:focus,.form-group textarea:focus{{
  outline:none;border-color:var(--verde)}}
.form-group textarea{{resize:vertical;min-height:90px}}
.fee-box{{background:var(--beige);border-radius:10px;padding:16px;margin:16px 0;
          font-size:.88rem;color:var(--gris)}}
.fee-box strong{{color:var(--verde)}}

/* FOOTER */
footer{{background:var(--negro);color:rgba(255,255,255,.7);
        padding:48px 40px;text-align:center}}
footer .logo{{color:var(--verde-claro);font-size:1.4rem;font-weight:700;margin-bottom:12px}}
footer p{{font-size:.85rem;line-height:1.8}}
footer a{{color:var(--naranja)}}

/* RESPONSIVE */
@media(max-width:768px){{
  .hero h1{{font-size:2rem}}
  .nav-links{{display:none}}
  section{{padding:48px 20px}}
  .form-row{{grid-template-columns:1fr}}
}}
"""

NAV = lambda activo: f"""
<nav>
  <div class="logo">Way2The<span>Unknown</span></div>
  <ul class="nav-links">
    <li><a href="index.html" {'style="color:var(--verde)"' if activo=='inicio' else ''}>Inicio</a></li>
    <li><a href="destinos.html" {'style="color:var(--verde)"' if activo=='destinos' else ''}>Destinos</a></li>
    <li><a href="servicios.html" {'style="color:var(--verde)"' if activo=='servicios' else ''}>Servicios</a></li>
    <li><a href="servicios.html" class="nav-cta">Cotizar Ahora</a></li>
  </ul>
</nav>"""

FOOTER = """
<footer>
  <div class="logo">Way2TheUnknown</div>
  <p>Agencia de viajes especializada en destinos únicos &amp; experiencias memorables<br>
  México · <a href="mailto:hola@way2theunknown.com">hola@way2theunknown.com</a> · Fee: 8% sobre el viaje</p>
  <p style="margin-top:16px;font-size:.75rem;color:rgba(255,255,255,.4)">
    © 2026 Way2TheUnknown — Generado por Agencia Santi IA
  </p>
</footer>"""

def generar_index():
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Way2TheUnknown — Descubre el Mundo</title>
<style>{CSS_BASE}</style>
</head>
<body>
{NAV('inicio')}

<div class="hero">
  <h1>Viaja hacia lo <span>Desconocido</span></h1>
  <p>Agencia boutique especializada en experiencias únicas. Destinos exclusivos, itinerarios personalizados y el mejor precio garantizado con solo el 8% de fee.</p>
  <div>
    <a href="destinos.html" class="btn btn-primary">Ver Destinos</a>
    <a href="servicios.html" class="btn btn-secondary">Cotizar Gratis</a>
  </div>
</div>

<div class="stats-bar">
  <div class="stats-inner">
    <div class="stat"><h3>500+</h3><p>Viajeros felices</p></div>
    <div class="stat"><h3>45</h3><p>Destinos disponibles</p></div>
    <div class="stat"><h3>8%</h3><p>Fee transparente</p></div>
    <div class="stat"><h3>24/7</h3><p>Soporte en viaje</p></div>
  </div>
</div>

<section>
  <div class="section-title">
    <h2>Destinos Destacados</h2>
    <p>Los favoritos de nuestros viajeros este 2026</p>
  </div>
  <div class="destinos-grid">
    <div class="destino-card">
      <div class="destino-img">🗻</div>
      <div class="destino-body">
        <span class="tag">Asia</span>
        <h3>Japón Clásico</h3>
        <p>Tokyo, Kioto y Osaka. Tradición y modernidad en perfecta armonía.</p>
        <div class="destino-price">Desde $42,000 MXN <span>/ persona</span></div>
      </div>
    </div>
    <div class="destino-card">
      <div class="destino-img">🏖️</div>
      <div class="destino-body">
        <span class="tag">México</span>
        <h3>Riviera Maya</h3>
        <p>Cancún, Tulum y Playa del Carmen. El Caribe mexicano en su máximo esplendor.</p>
        <div class="destino-price">Desde $18,000 MXN <span>/ persona</span></div>
      </div>
    </div>
    <div class="destino-card">
      <div class="destino-img">🏰</div>
      <div class="destino-body">
        <span class="tag">Europa</span>
        <h3>Gran Tour Europa</h3>
        <p>París, Roma, Barcelona y Amsterdam. La esencia del viejo continente.</p>
        <div class="destino-price">Desde $68,000 MXN <span>/ persona</span></div>
      </div>
    </div>
  </div>
  <div style="text-align:center;margin-top:36px">
    <a href="destinos.html" class="btn btn-primary">Ver Todos los Destinos</a>
  </div>
</section>
{FOOTER}
</body></html>"""

def generar_destinos():
    destinos = [
        ("🗻","Japón Clásico","Asia","Tokyo, Kioto, Osaka, Hiroshima y Nara. 12 días de cultura, gastronomía y tradición.","$42,000","12 días"),
        ("🏖️","Riviera Maya","México","Cancún, Tulum, Playa del Carmen y Coba. El Caribe mexicano con cenotes incluidos.","$18,000","7 días"),
        ("🏰","Gran Tour Europa","Europa","París, Roma, Barcelona, Amsterdam y Praga. El mejor de Europa en 15 días.","$68,000","15 días"),
        ("🦁","Safari Kenya","África","Masai Mara, Amboseli y Lago Nakuru. La gran migración y los Big Five.","$85,000","10 días"),
        ("🗽","Nueva York","EEUU","Manhattan, Brooklyn, museos y shows de Broadway. La ciudad que nunca duerme.","$35,000","8 días"),
        ("🌸","Bali & Lombok","Asia","Templos, arrozales, playas cristalinas y cultura balinesa auténtica.","$38,000","10 días"),
        ("🏔️","Patagonia","Sudamérica","Torres del Paine, El Calafate y Ushuaia. El fin del mundo te espera.","$55,000","11 días"),
        ("🐪","Marruecos","África","Marrakech, Fez, el Sahara y la costa atlántica. Arabia al alcance de México.","$32,000","9 días"),
    ]
    cards = ""
    for emoji, nombre, region, desc, precio, duracion in destinos:
        cards += f"""
    <div class="destino-card">
      <div class="destino-img">{emoji}</div>
      <div class="destino-body">
        <span class="tag">{region}</span>
        <h3>{nombre}</h3>
        <p>{desc}</p>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:12px">
          <div class="destino-price">Desde {precio} MXN</div>
          <a href="servicios.html" class="btn btn-primary" style="padding:8px 18px;font-size:.82rem">Cotizar</a>
        </div>
        <div style="font-size:.78rem;color:var(--gris);margin-top:8px">⏱ {duracion}</div>
      </div>
    </div>"""

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Destinos — Way2TheUnknown</title>
<style>{CSS_BASE}</style>
</head>
<body>
{NAV('destinos')}
<div style="background:var(--beige);padding:60px 40px;text-align:center">
  <h1 style="font-size:2.4rem;color:var(--verde);margin-bottom:10px">Nuestros Destinos</h1>
  <p style="color:var(--gris);font-size:1rem">45 destinos disponibles · Paquetes personalizados · Fee 8%</p>
</div>
<section>
  <div class="destinos-grid">{cards}</div>
</section>
{FOOTER}
</body></html>"""

def generar_servicios():
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cotizar — Way2TheUnknown</title>
<style>{CSS_BASE}</style>
</head>
<body>
{NAV('servicios')}
<div style="background:var(--beige);padding:60px 40px;text-align:center">
  <h1 style="font-size:2.4rem;color:var(--verde);margin-bottom:10px">Cotiza tu Viaje</h1>
  <p style="color:var(--gris)">Sin compromisos · Respuesta en 24 horas · Fee 8% transparente</p>
</div>
<section>
  <div class="form-box">
    <h2 style="color:var(--verde);margin-bottom:24px;font-size:1.4rem">Solicita tu Cotización</h2>
    <div class="form-row">
      <div class="form-group"><label>Nombre completo</label><input type="text" placeholder="Tu nombre"></div>
      <div class="form-group"><label>Email</label><input type="email" placeholder="tu@email.com"></div>
    </div>
    <div class="form-row">
      <div class="form-group"><label>Destino deseado</label>
        <select>
          <option value="">Selecciona un destino</option>
          <option>Japón Clásico</option><option>Riviera Maya</option>
          <option>Gran Tour Europa</option><option>Safari Kenya</option>
          <option>Nueva York</option><option>Bali & Lombok</option>
          <option>Patagonia</option><option>Marruecos</option>
          <option>Destino personalizado</option>
        </select>
      </div>
      <div class="form-group"><label>Número de personas</label>
        <select>
          <option>1 persona</option><option>2 personas</option>
          <option>3-4 personas</option><option>5 o más</option>
        </select>
      </div>
    </div>
    <div class="form-row">
      <div class="form-group"><label>Fecha de salida</label><input type="date"></div>
      <div class="form-group"><label>Presupuesto total (MXN)</label>
        <select>
          <option>Menos de $20,000</option><option>$20,000 - $40,000</option>
          <option>$40,000 - $80,000</option><option>Más de $80,000</option>
        </select>
      </div>
    </div>
    <div class="form-group" style="margin-bottom:16px">
      <label>¿Qué buscas en este viaje?</label>
      <textarea placeholder="Aventura, descanso, cultura, gastronomía, luna de miel..."></textarea>
    </div>
    <div class="fee-box">
      <strong>Nuestro modelo transparente:</strong> Cobramos solo el <strong>8% de fee</strong> sobre el costo total del viaje. Sin sorpresas, sin costos ocultos. Lo que cotizamos es lo que pagas.
    </div>
    <button class="btn btn-primary" style="width:100%;padding:16px;font-size:1rem" onclick="alert('¡Gracias! Nos pondremos en contacto en menos de 24 horas.')">
      Solicitar Cotización Gratuita
    </button>
  </div>
</section>
{FOOTER}
</body></html>"""

def main():
    instruccion = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "generar_todo"
    
    # Directorio de salida: sitio_web dentro del proyecto
    proyecto_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sitio_dir = os.path.join(proyecto_dir, "sitio_web")
    os.makedirs(sitio_dir, exist_ok=True)
    os.makedirs(os.path.join(sitio_dir, "css"), exist_ok=True)
    os.makedirs(os.path.join(sitio_dir, "js"), exist_ok=True)
    os.makedirs(os.path.join(sitio_dir, "assets"), exist_ok=True)
    
    archivos = {
        "index.html": generar_index(),
        "destinos.html": generar_destinos(),
        "servicios.html": generar_servicios(),
    }
    
    creados = []
    for nombre, contenido in archivos.items():
        ruta = os.path.join(sitio_dir, nombre)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        creados.append(ruta)
        print(f"✓ Creado: {ruta}")
    
    # JS básico
    js = """// Way2TheUnknown — Funciones básicas
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll para links internos
    document.querySelectorAll('a[href^="#"]').forEach(a => {
        a.addEventListener('click', e => {
            e.preventDefault();
            document.querySelector(a.getAttribute('href'))?.scrollIntoView({behavior:'smooth'});
        });
    });
    // Highlight nav activo
    const path = window.location.pathname.split('/').pop();
    document.querySelectorAll('.nav-links a').forEach(a => {
        if(a.getAttribute('href') === path) a.style.color = 'var(--verde)';
    });
});
"""
    with open(os.path.join(sitio_dir, "js", "funciones.js"), "w", encoding="utf-8") as f:
        f.write(js)
    
    print(f"\n✅ Sitio web generado en: {sitio_dir}")
    print(f"   Archivos: {', '.join(archivos.keys())}")
    print(f"   Abre: file:///{sitio_dir.replace(chr(92), '/')}/index.html")
    return sitio_dir

if __name__ == "__main__":
    main()
