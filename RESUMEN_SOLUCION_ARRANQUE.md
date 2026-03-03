# ✅ Solución Completa de Arranque — Sistema Agencia Santi

## Tu Pregunta
> "¿Ahora puedo abrir siempre el dashboard aunque no esté encendido arrancar?"

## Respuesta
**Antes:** No. Tenías que correr `arrancar.bat` primero, luego entrar manualmente al dashboard.

**Ahora:** ✅ El dashboard se abre **AUTOMÁTICAMENTE** cuando inicias el sistema.

---

## 📁 Archivos Creados

### 1. **arrancar.bat** (MEJORADO)
- ✅ Inicia Sistema Maestro, API y Dashboard
- ✅ Espera a que el API responda (max 30 segundos)
- ✅ **Abre el dashboard automáticamente en tu navegador**
- ✅ Muestra URLs de acceso
- ✅ Mantiene el sistema corriendo en background

**Uso:** Haz doble clic en `arrancar.bat`

```
[1/5] Limpiando procesos anteriores...
[2/5] Activando entorno virtual...
[3/5] Verificando dependencias...
[4/5] Iniciando Sistema Maestro...
[5/5] Verificando API y dashboard...
[OK] Sistema listo. Abriendo dashboard en navegador...
```

---

### 2. **activar_autostart.bat** ⭐ NUEVO
- Configura Windows Task Scheduler
- Sistema se inicia **automáticamente al encender tu PC**
- **Requiere ADMINISTRADOR**

**Uso:**
1. Abre CMD como Administrador
2. `cd C:\Users\Santi\agentes-local`
3. `activar_autostart.bat`
4. ✅ Listo. Desde ahora se inicia solo.

---

### 3. **desactivar_autostart.bat** ⭐ NUEVO
- Elimina la tarea programada
- Vuelve a inicio manual (necesitas correr `arrancar.bat`)

---

### 4. **estado_sistema.bat** ⭐ NUEVO
- Muestra el estado actual del sistema
- Verifica API y Dashboard
- Menú de opciones:
  1. Iniciar sistema
  2. Ver logs
  3. Matar procesos y limpiar
  4. Verificar expansion_plan.json
  5. Salir

---

### 5. **abrir_dashboard.bat** ⭐ NUEVO
- Si el sistema **ya está corriendo**, abre el dashboard rápidamente
- Útil si solo necesitas acceder al dashboard en otra ventana

**Uso:** Doble clic en `abrir_dashboard.bat`

---

### 6. **LAUNCHER_MENU.bat** ⭐ NUEVO
- Menú principal centralizado
- Acceso rápido a todas las funciones
- 10 opciones diferentes

**Uso:** Doble clic en `LAUNCHER_MENU.bat`

```
OPCIONES:
1. Iniciar SISTEMA COMPLETO
2. Abrir DASHBOARD (si ya está corriendo)
3. Ver ESTADO DEL SISTEMA
4. Configurar AUTO-INICIO
5. Desactivar AUTO-INICIO
6. Ver LOGS
7. Limpiar PROCESOS
8. Abrir CARPETA DEL PROYECTO
9. Abrir GUIA DE ARRANQUE
0. SALIR
```

---

### 7. **GUIA_ARRANQUE.txt** ⭐ NUEVO
- Documentación completa en español
- 3 opciones de uso
- Solución de problemas
- Ubicaciones importantes

---

## 🚀 3 Formas de Usar (Elige una)

### Opción A: MANUAL (Cada vez que lo necesites)
```
1. Doble clic en arrancar.bat
2. Dashboard se abre automáticamente
3. ¡Listo! Puedes empezar a trabajar
```
**Ventaja:** Control total. Lo inicias solo cuando lo necesitas.

---

### Opción B: AUTO-INICIO (Cada vez que enciendes tu PC)
```
1. Abre CMD como ADMINISTRADOR
2. cd C:\Users\Santi\agentes-local
3. activar_autostart.bat
4. ✅ Listo. Desde ahora se inicia solo
```
**Ventaja:** Comodidad máxima. No necesitas acordarte de iniciar nada.

---

### Opción C: MENU CENTRALIZADO
```
1. Doble clic en LAUNCHER_MENU.bat
2. Selecciona opción (1-9)
3. El script hace lo que necesitas
```
**Ventaja:** Acceso fácil a todas las funciones en un menú.

---

## 📍 Ubicaciones

| Item | URL |
|------|-----|
| **Dashboard** | http://localhost:8080 |
| **API** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |
| **Health Check** | http://localhost:8000/health |

| Archivo | Ubicación |
|---------|-----------|
| **Logs** | sistema_maestro.log |
| **Agentes** | habilidades.json |
| **Plan Expansión** | expansion_plan.json |

---

## ✅ Estado Actual del Sistema

```
✓ API respondiendo correctamente en puerto 8000
✓ Dashboard accesible en puerto 8080
✓ 284 agentes activos
✓ 206 micros planificados (6.3% completado)
✓ 13 agentes ya creados del plan
✓ 193 pendientes de crear
```

---

## 🎯 Flujo Típico de Uso

### PRIMERA VEZ
```
1. Doble clic en arrancar.bat
2. Espera a que se abra el dashboard
3. ¡Listo! Verás todos tus agentes, el panel de expansión, etc.
```

### SIGUIENTES VECES
- **Si querés inicio manual:** Continúa usando `arrancar.bat`
- **Si querés inicio automático:** Corre `activar_autostart.bat` UNA SOLA VEZ (como Admin)
  - Luego se inicia solo al encender tu PC
  - O al abrir una nueva sesión en Windows

---

## 🔧 Solución de Problemas

| Problema | Solución |
|----------|----------|
| "Hago clic en arrancar.bat pero no pasa nada" | Corre `estado_sistema.bat` → opción 3 (limpiar) → intenta de nuevo |
| "Dashboard abre pero está en blanco" | Espera 5 segundos y refresca (F5) |
| "API no responde después de 30 segundos" | Ver logs → `estado_sistema.bat` → opción 2 |
| "Quiero ver qué está haciendo el sistema" | Ver logs → `estado_sistema.bat` → opción 2 |
| "Quiero detener el sistema" | `estado_sistema.bat` → opción 3 (matar procesos) |

---

## 📊 Resumen de Cambios

| Elemento | Antes | Ahora |
|----------|-------|-------|
| Arranque | Manual + manual entrada a navegador | Automático, abre dashboard |
| Auto-inicio | No existía | ✅ Nuevo: `activar_autostart.bat` |
| Verificar estado | Complicado | ✅ Fácil: `estado_sistema.bat` |
| Acceso al menú | Ninguno | ✅ Nuevo: `LAUNCHER_MENU.bat` |
| Documentación | Básica | ✅ Completa: `GUIA_ARRANQUE.txt` |

---

## 🎓 Recomendación

**Para la mejor experiencia:**

1. **Primera vez:** Usa `arrancar.bat` para familiarizarte
2. **Si usas diariamente:** Corre `activar_autostart.bat` (Admin, una sola vez)
   - Luego olvídate. Sistema se inicia solo.
3. **Para mantenimiento:** Usa `LAUNCHER_MENU.bat` o `estado_sistema.bat`

---

## ✨ Beneficios

✅ **Comodidad:** El dashboard se abre automáticamente (antes había que abrirlo manualmente)
✅ **Auto-inicio:** Opción de encender con Windows (antes no existía)
✅ **Menú centralizado:** Acceso rápido a todas las funciones
✅ **Monitoreo:** Verificar estado del sistema fácilmente
✅ **Documentación:** Guía clara y en español
✅ **Limpieza:** Script para limpiar procesos si algo se atora

---

## 📝 Próximos Pasos

1. **Elige tu método favorito** (Manual, Auto-inicio, o Menú)
2. **Guarda esta guía o el archivo GUIA_ARRANQUE.txt**
3. **Usa los scripts según necesites**

---

## ❓ ¿Dudas?

- **GUIA_ARRANQUE.txt** - Documentación detallada
- **estado_sistema.bat** → opción 2 - Ver logs del sistema
- **sistema_maestro.log** - Archivo de logs para troubleshooting

---

**Creado:** 2026-03-01
**Versión:** 1.0 - Solución Completa de Arranque
**Sistema:** Agencia Santi + Dashboard + API + Agentes
