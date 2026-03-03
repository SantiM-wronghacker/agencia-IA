# Catálogo de Agentes - Agencia IA

## Resumen

| Categoría | Total | Modelo IA | Descripción |
|-----------|-------|-----------|-------------|
| Cerebro | 51 | Claude | Orquestación, routing, memoria, RAG |
| Finanzas | 73 | GPT-4o | Análisis financiero, cálculos, proyecciones |
| Herramientas | 158 | Groq | Generadores, analizadores, formateadores |
| Contabilidad | 21 | GPT-4o | Facturación, impuestos, estados financieros |
| Legal | 16 | GPT-4o | Contratos, compliance, regulaciones |
| Operaciones | 17 | Groq | Inventario, producción, logística |
| Real Estate | 20 | Groq | Inmuebles, valuaciones, hipotecas |
| Ventas | 24 | Mistral | Pipeline, leads, cotizaciones |
| RRHH | 17 | Mistral | Nómina, contratación, evaluación |
| Marketing | 18 | Mistral | Campañas, SEO, contenido, redes |
| Educación | - | Claude | Cursos, exámenes, planes de estudio |
| Salud | - | Claude | Diagnósticos, recetas, tratamientos |
| Seguros | - | Mistral | Pólizas, siniestros, cotizaciones |
| Tecnología | - | Groq | APIs, cloud, infraestructura |
| Turismo | - | Mistral | Itinerarios, destinos, paquetes |
| Restaurantes | - | Groq | Menús, costos, recetas |
| Logística | - | Groq | Envíos, rutas, tracking |
| Micro Tareas | - | Cerebras | Tareas rápidas y simples |

## Categorías Principales

### Finanzas (73 agentes)

Agentes especializados en análisis financiero, cálculos de ROI, proyecciones, nómina, impuestos y más.

**Ejemplos:**
- `calculadora_roi` - Calcula retorno de inversión
- `analizador_flujo_caja` - Analiza flujo de efectivo
- `calculadora_nomina` - Cálculo de nómina mexicana
- `calculadora_isr_basica` - Cálculo de ISR

### Legal (16 agentes)

Agentes para generación de contratos, análisis de riesgo legal y compliance.

**Ejemplos:**
- `generador_contrato_laboral` - Genera contratos laborales
- `generador_nda` - Genera acuerdos de confidencialidad
- `analizador_riesgo_legal` - Analiza riesgos legales

### Herramientas (158 agentes)

La categoría más grande. Generadores, analizadores, formateadores y monitores de propósito general.

**Ejemplos:**
- `generador_cotizacion` - Genera cotizaciones
- `formateador_moneda_mx` - Formatea montos en pesos MXN
- `validador_rfc_mexico` - Valida RFC mexicano

## Cómo Usar un Agente

```python
from src.agencia.core.base_agent import BaseAgent
from src.agencia.core.agent_registry import registry

# Buscar agentes por categoría
agentes_finanzas = registry.find_by_category("finanzas")

# Buscar por capacidad
agentes_roi = registry.find_by_capability("roi")

# Ejecutar un agente
resultado = agente.run({"query": "Calcular ROI de $100,000 inversión"})
```
