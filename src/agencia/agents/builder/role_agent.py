"""
RoleAgent — Agente superior de rol.

Cada RoleAgent:
  1. Define un dominio y un conjunto de capacidades.
  2. Posee una SubAgentFactory interna para crear neuronas/tools.
  3. Puede detectar gaps de capacidad vs. lo que se le pide.
  4. Genera subagentes internos para cubrir esos gaps.
  5. El TeamDirector NO ve ni selecciona estos subagentes.
"""

from __future__ import annotations

from typing import Any

from agencia.agents.builder.sub_agent_factory import SubAgentFactory


class RoleAgent:
    """
    Clase base para todos los roles de la agencia.

    Subclases concretas deben sobrescribir al menos:
      - ``capacidades``  (set de strings que describe lo que sabe hacer)
      - ``ejecutar()``   (lógica principal del rol)
    """

    nombre: str = "BaseRole"
    dominio: str = "general"
    capacidades: set[str] = set()

    def __init__(self) -> None:
        self.factory = SubAgentFactory(owner_role=self.nombre)
        self._resultados: list[dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Gap Detection
    # ------------------------------------------------------------------

    def detectar_gaps(self, requerimientos: set[str]) -> set[str]:
        """
        Compara los requerimientos pedidos contra las capacidades del rol.
        Devuelve el conjunto de capacidades faltantes (gaps).
        """
        caps_actuales = self.capacidades | {
            s.nombre for s in self.factory.listar()
        }
        return requerimientos - caps_actuales

    # ------------------------------------------------------------------
    # Internal Sub-Agent Generation
    # ------------------------------------------------------------------

    def generar_subagente(self, gap: str) -> None:
        """
        Crea un subagente interno (neurona/tool) para cubrir un gap.

        La implementación base crea un placeholder.  Las subclases pueden
        sobrescribir esto para generar lógica especializada.
        """
        def _placeholder(**kwargs: Any) -> dict:
            return {"status": "generated", "gap": gap, "input": kwargs}

        self.factory.crear(
            nombre=gap,
            descripcion=f"Subagente auto-generado para cubrir: {gap}",
            fn=_placeholder,
        )

    def cubrir_gaps(self, requerimientos: set[str]) -> set[str]:
        """
        Detecta y cubre todos los gaps generando subagentes internos.
        Devuelve el conjunto de gaps que fueron cubiertos.
        """
        gaps = self.detectar_gaps(requerimientos)
        for gap in gaps:
            self.generar_subagente(gap)
        return gaps

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def ejecutar(self, orden: str, contexto: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Procesa una orden dentro del dominio del rol.

        Las subclases deben sobrescribir este método con su lógica real.
        """
        resultado = {
            "role": self.nombre,
            "dominio": self.dominio,
            "orden": orden,
            "status": "completado",
            "capacidades_usadas": list(self.capacidades),
        }
        self._resultados.append(resultado)
        return resultado

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def info(self) -> dict[str, Any]:
        """Metadata pública del rol (visible para el TeamDirector)."""
        return {
            "nombre": self.nombre,
            "dominio": self.dominio,
            "capacidades": sorted(self.capacidades),
        }

    def __repr__(self) -> str:
        return f"RoleAgent({self.nombre!r}, dominio={self.dominio!r})"
RoleAgent – a specialised agent bound to a named role.

Each RoleAgent only has access to its own pre-registered tools/sub-agents.
It **cannot** execute arbitrary scripts or call tools outside its scope.
"""
from __future__ import annotations

import logging
from typing import Any, Callable

logger = logging.getLogger(__name__)


class RoleAgent:
    """An agent that is scoped to a single *role* (e.g. ``strategy``, ``tech``).

    Parameters
    ----------
    role:
        Short slug that identifies this role (e.g. ``"strategy"``).
    description:
        Human-readable description of the role's purpose.
    handler:
        Callable that performs the role's work.
        Signature: ``(goal: str, context: dict) -> dict``
    """

    def __init__(
        self,
        role: str,
        description: str,
        handler: Callable[..., dict[str, Any]],
    ) -> None:
        self.role = role
        self.description = description
        self._handler = handler

    def execute(self, goal: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Run the role handler with the given *goal* and optional *context*."""
        ctx = context or {}
        logger.info("RoleAgent[%s] executing goal: %s", self.role, goal)
        return self._handler(goal, ctx)

    def __repr__(self) -> str:
        return f"RoleAgent(role={self.role!r})"
