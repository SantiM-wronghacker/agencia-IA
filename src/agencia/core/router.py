"""
Agencia IA - Dynamic Router

Routes tasks to the appropriate agent based on category, capability,
or semantic similarity. Includes load balancing and automatic fallback.
"""

import logging
import random
from typing import Any, Optional

from src.agencia.core.agent_registry import AgentRegistry, AgentRecord

logger = logging.getLogger("agencia.router")

# Category keywords for routing
CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "finanzas": [
        "finanzas", "dinero", "inversión", "presupuesto", "contabilidad",
        "impuesto", "isr", "iva", "nómina", "balance", "flujo", "caja",
        "roi", "rendimiento", "crédito", "deuda", "capital",
    ],
    "legal": [
        "legal", "contrato", "ley", "regulación", "demanda", "abogado",
        "nda", "poder", "constitutiva", "acta", "notarial",
    ],
    "ventas": [
        "venta", "cliente", "prospecto", "pipeline", "cierre", "lead",
        "cotización", "propuesta", "comisión", "script",
    ],
    "marketing": [
        "marketing", "campaña", "seo", "ads", "redes", "contenido",
        "email", "newsletter", "copy", "landing", "brand",
    ],
    "recursos_humanos": [
        "rrhh", "empleado", "contratación", "nómina", "vacante",
        "desempeño", "capacitación", "onboarding", "clima",
    ],
    "tecnologia": [
        "código", "api", "cloud", "stack", "devops", "servidor",
        "bug", "deploy", "software", "infraestructura",
    ],
    "operaciones": [
        "operación", "logística", "inventario", "almacén", "producción",
        "cadena", "proveedor", "mantenimiento",
    ],
    "salud": [
        "salud", "médico", "paciente", "diagnóstico", "tratamiento",
        "receta", "clínico", "dosis", "consulta",
    ],
    "educacion": [
        "educación", "curso", "estudiante", "examen", "plan de estudio",
        "temario", "calificación", "aprendizaje",
    ],
    "real_estate": [
        "inmueble", "propiedad", "renta", "hipoteca", "plusvalía",
        "terreno", "departamento", "avalúo",
    ],
    "restaurantes": [
        "restaurante", "platillo", "menú", "cocina", "receta",
        "food cost", "mesa", "comensal",
    ],
    "seguros": [
        "seguro", "póliza", "prima", "siniestro", "cobertura",
        "aseguradora", "beneficiario",
    ],
    "turismo": [
        "viaje", "turismo", "destino", "hotel", "vuelo",
        "itinerario", "paquete", "tour",
    ],
    "logistica": [
        "envío", "transporte", "ruta", "entrega", "carga",
        "paquetería", "tracking", "almacén",
    ],
    "cerebro": [
        "router", "memoria", "rag", "orquestador", "sistema",
        "evolución", "diagnóstico", "agente",
    ],
    "herramientas": [
        "herramienta", "generador", "analizador", "formateador",
        "conversor", "validador", "calculadora",
    ],
    "contabilidad": [
        "factura", "cfdi", "sat", "fiscal", "tributario",
        "estado de resultados", "balance general",
    ],
}


class DynamicRouter:
    """Routes tasks to the best available agent."""

    def __init__(self, registry: AgentRegistry):
        self.registry = registry

    def route_by_category(self, category: str) -> list[AgentRecord]:
        """Find agents by category name."""
        agents = self.registry.find_by_category(category)
        if not agents:
            logger.warning("no_agents_in_category", extra={"category": category})
        return agents

    def route_by_capability(self, capability: str) -> list[AgentRecord]:
        """Find agents by capability."""
        agents = self.registry.find_by_capability(capability)
        if not agents:
            logger.warning(
                "no_agents_with_capability", extra={"capability": capability}
            )
        return agents

    def route_semantic(self, query: str) -> Optional[AgentRecord]:
        """Route based on semantic analysis of the query text."""
        query_lower = query.lower()
        scores: dict[str, int] = {}

        for category, keywords in CATEGORY_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in query_lower)
            if score > 0:
                scores[category] = score

        if not scores:
            logger.info("no_semantic_match", extra={"query": query[:100]})
            return None

        best_category = max(scores, key=lambda k: scores[k])
        agents = self.registry.find_by_category(best_category)
        active = [a for a in agents if a.status == "active"]

        if not active:
            logger.warning(
                "no_active_agents",
                extra={"category": best_category},
            )
            return None

        selected = random.choice(active)
        logger.info(
            "semantic_route",
            extra={
                "query": query[:100],
                "category": best_category,
                "agent": selected.name,
                "score": scores[best_category],
            },
        )
        return selected

    def route_with_fallback(
        self, query: str, preferred_category: Optional[str] = None
    ) -> Optional[AgentRecord]:
        """Route with automatic fallback if primary agent is unavailable."""
        if preferred_category:
            agents = self.route_by_category(preferred_category)
            active = [a for a in agents if a.status == "active"]
            if active:
                return random.choice(active)

        result = self.route_semantic(query)
        if result:
            return result

        cerebro = self.registry.find_by_category("cerebro")
        active_cerebro = [a for a in cerebro if a.status == "active"]
        if active_cerebro:
            return active_cerebro[0]

        all_agents = self.registry.list_all()
        active_all = [a for a in all_agents if a.status == "active"]
        if active_all:
            return random.choice(active_all)

        return None

    def get_stats(self) -> dict[str, Any]:
        """Get routing statistics."""
        return self.registry.get_health_summary()
