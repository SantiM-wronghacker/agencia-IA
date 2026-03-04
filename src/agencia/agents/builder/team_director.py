"""
TeamDirector — Director / Team Builder de la agencia.

REGLA NO NEGOCIABLE:
  El Director SOLO puede seleccionar y coordinar ROLES (RoleAgents).
  NO puede seleccionar microagentes, neuronas ni agentes legacy.
  Los subagentes quedan encapsulados dentro de cada RoleAgent.

Flujo:
  1. Recibe un brief del cliente (dict o JSON).
  2. Extrae los requerimientos del brief.
  3. Selecciona los RoleAgents necesarios del RoleRegistry.
  4. Cada RoleAgent detecta y cubre sus propios gaps internamente.
  5. Ejecuta la cadena de roles y sintetiza el resultado.
"""

from __future__ import annotations

import json
import os
from typing import Any

from agencia.agents.builder.role_agent import RoleAgent
from agencia.agents.builder.role_registry import RoleRegistry


class TeamDirector:
    """
    Orquestador principal de la agencia.

    Opera EXCLUSIVAMENTE con RoleAgents registrados en el RoleRegistry.
    """

    def __init__(self, registry: RoleRegistry) -> None:
        self._registry = registry

    # ------------------------------------------------------------------
    # Brief Loading
    # ------------------------------------------------------------------

    @staticmethod
    def cargar_brief(path: str) -> dict[str, Any]:
        """Carga un brief de cliente desde un archivo JSON."""
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ------------------------------------------------------------------
    # Role Selection  (SOLO roles, nunca microagentes)
    # ------------------------------------------------------------------

    def seleccionar_roles(
        self, requerimientos: set[str]
    ) -> list[RoleAgent]:
        """
        Selecciona los RoleAgents cuyas capacidades cubren los
        requerimientos del brief.

        Solo devuelve ROLES del registry — nunca microagentes.
        """
        seleccionados: list[RoleAgent] = []
        cubiertos: set[str] = set()

        for req in sorted(requerimientos):
            if req in cubiertos:
                continue
            candidatos = self._registry.buscar_por_capacidad(req)
            if candidatos:
                role = candidatos[0]
                if role not in seleccionados:
                    seleccionados.append(role)
                cubiertos |= role.capacidades
            else:
                # No hay rol con esa capacidad — se seleccionan todos
                # los roles del dominio más cercano y se les pide cubrir gaps
                pass  # handled in armar_equipo

        return seleccionados

    def _roles_faltantes(
        self, requerimientos: set[str], equipo: list[RoleAgent]
    ) -> set[str]:
        """Requerimientos que ningún rol del equipo cubre."""
        cubiertos: set[str] = set()
        for role in equipo:
            cubiertos |= role.capacidades
        return requerimientos - cubiertos

    # ------------------------------------------------------------------
    # Team Assembly
    # ------------------------------------------------------------------

    def armar_equipo(
        self, brief: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Dado un brief de cliente, arma el equipo de roles y prepara
        la ejecución.

        Retorna un dict con:
          - equipo: lista de info de cada rol seleccionado
          - gaps_cubiertos: gaps que los roles cubrieron internamente
          - requerimientos: set original
        """
        requerimientos = set(brief.get("requerimientos", []))
        equipo = self.seleccionar_roles(requerimientos)

        gaps_cubiertos_total: dict[str, list[str]] = {}

        for role in equipo:
            gaps = role.cubrir_gaps(requerimientos)
            if gaps:
                gaps_cubiertos_total[role.nombre] = sorted(gaps)

        # Si aún quedan requerimientos sin cubrir, buscar roles adicionales
        faltantes = self._roles_faltantes(requerimientos, equipo)
        for role in self._registry.listar():
            if role in equipo:
                continue
            overlap = faltantes & role.capacidades
            if overlap:
                equipo.append(role)
                gaps = role.cubrir_gaps(requerimientos)
                if gaps:
                    gaps_cubiertos_total[role.nombre] = sorted(gaps)
                faltantes -= role.capacidades

        return {
            "cliente": brief.get("cliente", "desconocido"),
            "requerimientos": sorted(requerimientos),
            "equipo": [r.info() for r in equipo],
            "gaps_cubiertos": gaps_cubiertos_total,
        }

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def ejecutar_equipo(
        self,
        brief: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Flujo completo:
          1. Armar equipo de roles.
          2. Cada rol ejecuta la orden del brief.
          3. Recopilar resultados.
        """
        plan = self.armar_equipo(brief)
        orden = brief.get("orden", brief.get("objetivo", ""))
        contexto = brief.get("contexto", {})

        resultados: list[dict[str, Any]] = []
        for role_info in plan["equipo"]:
            role = self._registry.obtener(role_info["nombre"])
            if role is None:
                continue
            resultado = role.ejecutar(orden, contexto)
            resultados.append(resultado)

        return {
            "cliente": plan["cliente"],
            "orden": orden,
            "equipo": plan["equipo"],
            "gaps_cubiertos": plan["gaps_cubiertos"],
            "resultados": resultados,
            "status": "completado",
        }

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    def ejecutar_desde_archivo(self, path: str) -> dict[str, Any]:
        """Carga un brief JSON y ejecuta el equipo."""
        brief = self.cargar_brief(path)
        return self.ejecutar_equipo(brief)
