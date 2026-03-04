"""Rol de Tecnología — desarrollo, infraestructura, datos."""

from __future__ import annotations

from typing import Any

from agencia.agents.builder.role_agent import RoleAgent


class TechRole(RoleAgent):
    nombre = "Tecnologia"
    dominio = "tecnologia"
    capacidades = {
        "desarrollo",
        "infraestructura",
        "datos",
        "seguridad_ti",
        "automatizacion",
    }

    def ejecutar(self, orden: str, contexto: dict[str, Any] | None = None) -> dict[str, Any]:
        resultado = {
            "role": self.nombre,
            "dominio": self.dominio,
            "orden": orden,
            "status": "completado",
            "entregables": ["arquitectura_sistema", "plan_desarrollo", "infra_config"],
            "subagentes_internos": self.factory.to_dict()["subagents"],
        }
        self._resultados.append(resultado)
        return resultado
