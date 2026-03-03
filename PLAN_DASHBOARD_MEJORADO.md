# PLAN: Dashboard Mejorado con CRUD Completo de Agentes

## 🎯 Objetivo

Reemplazar el dashboard actual (dashboard_web.py) con una versión mejorada que permita:
1. **CRUD completo** de agentes (crear, leer, actualizar, eliminar)
2. **Mejor visual** - Agentes organizados por categorías en tarjetas
3. **Edición inline** de propiedades sin tocar archivos JSON
4. **Gestión de categorías** - Crear nuevas categorías, renombrar, etc.
5. **Mejor UX** - Validación, confirmaciones, feedback visual

---

## 📋 Cambios Principales

### 1️⃣ Reescribir dashboard_web.py

**Nuevo Layout:**
```
┌─ HEADER: Status, Filtros ─────────────────┐
├─ ESTADÍSTICAS: Cards por categoría ───────┤
├─ TABS:                                     │
│  ├─ [Panel Agentes] (nuevo)               │
│  ├─ [Crear Agente] (nuevo)                │
│  ├─ [Admin Panel] (nuevo)                 │
│  ├─ [Ejecutar] (existente)                │
│  ├─ [Proyectos] (existente)               │
│  └─ [Logs] (existente)                    │
└─────────────────────────────────────────┘
```

**Nuevas Funciones JS:**

Panel Agentes:
- `cargarAgentesPorCategoria(cat)` - Obtiene agentes de una categoría
- `mostrarAgenteComoTarjeta(agente)` - Renderiza tarjeta de agente
- `abrirModalEditar(nombreAgente)` - Modal para editar propiedades
- `guardarCambiosAgente(nombre, datos)` - POST a /agentes/{nombre}
- `eliminarAgente(nombre, confirmar)` - DELETE a /agentes/{nombre}

Crear Agente:
- `crearNuevoAgente(form_data)` - POST a /agentes con validación

Admin Panel:
- `crearCategoria(nombre)` - POST a /categorias
- `renombrarCategoria(viejo, nuevo)` - PATCH a /categorias/{nombre}
- `eliminarCategoria(nombre)` - DELETE a /categorias/{nombre}
- `mostrarEstadisticas()` - GET a /estadisticas/por-categoria

**Mejoras de UX:**
- Modal elegante para editar agentes
- Confirmaciones antes de eliminar
- Toast notifications para feedback
- Carga con spinners
- Validación de entrada
- Escape HTML para prevenir XSS

---

### 2️⃣ Agregar Endpoints en api_agencia.py

**CRUD de Agentes:**
```python
@app.get("/agentes")
def obtener_agentes(categoria: str = None, salud: str = None):
    """Obtener agentes con filtros opcionales"""
    # Retorna: {agentes: [{nombre, desc, salud, categoria, ...}]}

@app.get("/agentes/{nombre}")
def obtener_agente(nombre: str):
    """Obtener un agente específico"""
    # Retorna: {nombre, desc, categoria, salud, tecnologia, ordenes, ...}

@app.post("/agentes")
def crear_agente(req: CreateAgenteRequest):
    """Crear nuevo agente"""
    # POST {nombre, descripcion, categoria, tecnologias, ordenes}
    # Valida: nombre único, categoría válida, desc min 15 chars
    # Guarda en habilidades.json
    # Retorna: {status: ok, mensaje, agente}

@app.patch("/agentes/{nombre}")
def editar_agente(nombre: str, req: UpdateAgenteRequest):
    """Editar propiedades de un agente"""
    # PATCH {descripcion?, categoria?, tecnologias?, ordenes?}
    # Solo actualiza campos proporcionados
    # Retorna: {status: ok, mensaje, agente_actualizado}

@app.delete("/agentes/{nombre}")
def eliminar_agente(nombre: str, confirmar: bool = True):
    """Eliminar un agente"""
    # DELETE /agentes/{nombre}?confirmar=true
    # También intenta eliminar el archivo .py si existe
    # Retorna: {status: ok, mensaje}
```

**Gestión de Categorías:**
```python
@app.get("/categorias")
def obtener_categorias():
    """Obtener todas las categorías con conteo"""
    # Retorna: {categorias: [CEREBRO, FINANZAS, REAL ESTATE, HERRAMIENTAS, ...]}

@app.post("/categorias")
def crear_categoria(req: CreateCategoriaRequest):
    """Crear nueva categoría"""
    # POST {nombre: "NUEVA_CATEGORIA"}
    # Retorna: {status: ok, mensaje, categoria}

@app.patch("/categorias/{nombre}")
def renombrar_categoria(nombre: str, req: RenameCategoriaRequest):
    """Renombrar categoría y reasignar agentes"""
    # PATCH {nuevo_nombre: "NOMBRE_NUEVO"}
    # Retorna: {status: ok, mensaje, agentes_reasignados: N}

@app.delete("/categorias/{nombre}")
def eliminar_categoria(nombre: str, reasignar_a: str):
    """Eliminar categoría"""
    # DELETE /categorias/{nombre}?reasignar_a=HERRAMIENTAS
    # Reasigna todos los agentes a otra categoría
    # Retorna: {status: ok, mensaje, agentes_reasignados: N}
```

**Estadísticas:**
```python
@app.get("/estadisticas/por-categoria")
def estadisticas_por_categoria():
    """Obtener stats detalladas"""
    # Retorna:
    # {
    #   categorias: {
    #     CEREBRO: {total: 45, ok: 45, con_web: 0, tecnologias: {...}},
    #     FINANZAS: {total: 74, ok: 74, con_web: 0, ...},
    #     ...
    #   }
    # }
```

**Validaciones:**
- Nombre de agente: solo .py, sin caracteres especiales
- Descripción: mínimo 15 caracteres
- Categoría: debe existir en la lista
- Tecnologías: validar contra lista conocida

---

### 3️⃣ Pydantic Models (en api_agencia.py)

```python
class CreateAgenteRequest(BaseModel):
    nombre: str  # ej: "agente_test.py"
    descripcion: str  # min 15 chars
    categoria: str  # debe existir
    tecnologias: List[str] = []
    ordenes: List[str] = []

class UpdateAgenteRequest(BaseModel):
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    tecnologias: Optional[List[str]] = None
    ordenes: Optional[List[str]] = None

class CreateCategoriaRequest(BaseModel):
    nombre: str

class RenameCategoriaRequest(BaseModel):
    nuevo_nombre: str
```

---

## 🗂️ Archivos a Modificar

| Archivo | Cambio | Impacto |
|---------|--------|--------|
| `dashboard_web.py` | Reescribir completamente | +2500 líneas (nuevo HTML/CSS/JS) |
| `api_agencia.py` | Agregar 10 endpoints nuevos + validaciones | +400 líneas |
| `habilidades.json` | Sin cambios (se actualiza dinámicamente) | — |
| `sistema_maestro.py` | Posible ajuste menor para recargar habilidades.json | Mínimo |

---

## ✅ Validación Después de Implementar

1. **Endpoints funcionan:**
   ```bash
   curl http://localhost:8000/agentes
   curl -X POST http://localhost:8000/agentes \
     -H "Content-Type: application/json" \
     -d '{"nombre":"test.py","descripcion":"Agente de prueba para testing del sistema","categoria":"HERRAMIENTAS","tecnologias":["Python"],"ordenes":["test"]}'
   ```

2. **Dashboard UI:**
   - Abrir http://localhost:8080
   - Tab "Panel Agentes" → Ver agentes por categoría
   - Clickear "Editar" en una tarjeta
   - Cambiar descripción, guardar
   - Verificar habilidades.json se actualizó
   - Crear nuevo agente
   - Crear nueva categoría
   - Eliminar agente (con confirmación)

3. **Persistencia:**
   - Los cambios del dashboard reflejan en habilidades.json
   - Dashboard se recarga correctamente después de cambios
   - Sistema maestro reconoce los nuevos agentes

---

## 🎯 Orden de Implementación

1. **Paso 1:** Agregar endpoints en api_agencia.py (CRUD)
2. **Paso 2:** Reescribir dashboard_web.py con nuevo layout
3. **Paso 3:** Conectar funciones JS a los endpoints
4. **Paso 4:** Validar y testear
5. **Paso 5:** Documentar cambios

---

## 📊 Estimación de Tiempo

- Endpoints API: ~1 hora
- Dashboard reescritura: ~1.5 horas
- Testing y refinement: ~30 min
- **Total: ~3 horas**

---

## ✨ Beneficios

✅ Control total del catálogo de agentes desde el dashboard
✅ No necesita editar archivos JSON manualmente
✅ Crear nuevas categorías dinámicamente
✅ Mejor visual y UX
✅ Validación integrada
✅ Feedback visual en tiempo real
✅ Sistema 100% editable y extensible
