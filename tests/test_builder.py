"""
Tests para el sistema Agencia Builder.

Valida:
  - SubAgentFactory: crear, listar, buscar, eliminar subagentes.
  - RoleAgent: gap detection, cubrir gaps, ejecución.
  - RoleRegistry: registro, búsqueda por dominio/capacidad.
  - TeamDirector: selección de roles (SOLO roles), armado de equipo,
    ejecución completa, carga de brief.
  - Regla no negociable: el Director no accede a subagentes internos.
"""

import json
import os
import tempfile

import pytest

from agencia.agents.builder.sub_agent_factory import SubAgent, SubAgentFactory
from agencia.agents.builder.role_agent import RoleAgent
from agencia.agents.builder.role_registry import RoleRegistry
from agencia.agents.builder.team_director import TeamDirector
from agencia.agents.builder.roles import (
    ALL_ROLES,
    StrategyRole,
    FinanceRole,
    LegalRole,
    MarketingRole,
    TechRole,
    OperationsRole,
)


# =====================================================================
# SubAgentFactory
# =====================================================================


class TestSubAgentFactory:
    def test_crear_subagente(self):
        factory = SubAgentFactory(owner_role="TestRole")
        sub = factory.crear("calc", "calcula cosas", lambda x: x * 2)
        assert sub.nombre == "calc"
        assert sub.ejecutar(5) == 10
        assert len(factory) == 1

    def test_listar_subagentes(self):
        factory = SubAgentFactory(owner_role="TestRole")
        factory.crear("a", "desc a", lambda: "a")
        factory.crear("b", "desc b", lambda: "b")
        assert len(factory.listar()) == 2

    def test_buscar_por_nombre(self):
        factory = SubAgentFactory(owner_role="TestRole")
        factory.crear("buscame", "desc", lambda: 42)
        found = factory.buscar_por_nombre("buscame")
        assert found is not None
        assert found.nombre == "buscame"
        assert factory.buscar_por_nombre("inexistente") is None

    def test_eliminar_subagente(self):
        factory = SubAgentFactory(owner_role="TestRole")
        sub = factory.crear("temp", "temporal", lambda: None)
        assert factory.eliminar(sub.id) is True
        assert len(factory) == 0
        assert factory.eliminar("fake_id") is False

    def test_to_dict(self):
        factory = SubAgentFactory(owner_role="MiRol")
        factory.crear("n1", "desc1", lambda: 1)
        d = factory.to_dict()
        assert d["owner_role"] == "MiRol"
        assert len(d["subagents"]) == 1
        assert d["subagents"][0]["nombre"] == "n1"


# =====================================================================
# RoleAgent
# =====================================================================


class TestRoleAgent:
    def test_detectar_gaps_sin_gaps(self):
        role = StrategyRole()
        gaps = role.detectar_gaps({"planificacion", "roadmap"})
        assert gaps == set()

    def test_detectar_gaps_con_gaps(self):
        role = StrategyRole()
        gaps = role.detectar_gaps({"planificacion", "machine_learning"})
        assert "machine_learning" in gaps

    def test_cubrir_gaps(self):
        role = StrategyRole()
        cubiertos = role.cubrir_gaps({"planificacion", "machine_learning"})
        assert "machine_learning" in cubiertos
        # Ahora ya no debería haber gap
        assert role.detectar_gaps({"machine_learning"}) == set()
        assert len(role.factory) == 1

    def test_ejecutar_base(self):
        role = StrategyRole()
        result = role.ejecutar("hacer plan")
        assert result["status"] == "completado"
        assert result["role"] == "Estrategia"

    def test_info_no_expone_subagentes(self):
        role = FinanceRole()
        role.cubrir_gaps({"algo_nuevo"})
        info = role.info()
        # info() solo muestra nombre, dominio, capacidades — NO subagentes
        assert "subagentes" not in info
        assert info["nombre"] == "Finanzas"

    def test_factory_es_interna(self):
        role = TechRole()
        role.cubrir_gaps({"quantum_computing"})
        # La factory existe, pero el Director no debería usarla
        assert len(role.factory) == 1
        sub = role.factory.listar()[0]
        assert sub.nombre == "quantum_computing"


# =====================================================================
# RoleRegistry
# =====================================================================


class TestRoleRegistry:
    def _registry_lleno(self) -> RoleRegistry:
        reg = RoleRegistry()
        for cls in ALL_ROLES:
            reg.registrar_clase(cls)
        return reg

    def test_registrar_y_listar(self):
        reg = self._registry_lleno()
        assert len(reg) == 6

    def test_obtener_por_nombre(self):
        reg = self._registry_lleno()
        assert reg.obtener("Finanzas") is not None
        assert reg.obtener("NoExiste") is None

    def test_buscar_por_dominio(self):
        reg = self._registry_lleno()
        legales = reg.buscar_por_dominio("legal")
        assert len(legales) == 1
        assert legales[0].nombre == "Legal"

    def test_buscar_por_capacidad(self):
        reg = self._registry_lleno()
        con_roi = reg.buscar_por_capacidad("roi")
        assert any(r.nombre == "Finanzas" for r in con_roi)

    def test_dominios_disponibles(self):
        reg = self._registry_lleno()
        doms = reg.dominios_disponibles()
        assert "finanzas" in doms
        assert "legal" in doms
        assert "tecnologia" in doms

    def test_contains(self):
        reg = self._registry_lleno()
        assert "Marketing" in reg
        assert "Inexistente" not in reg


# =====================================================================
# TeamDirector
# =====================================================================


class TestTeamDirector:
    def _director(self) -> TeamDirector:
        reg = RoleRegistry()
        for cls in ALL_ROLES:
            reg.registrar_clase(cls)
        return TeamDirector(registry=reg)

    def test_seleccionar_roles_solo_roles(self):
        director = self._director()
        roles = director.seleccionar_roles({"roi", "contratos"})
        # Solo debe devolver RoleAgents, nunca subagentes
        for r in roles:
            assert isinstance(r, RoleAgent)
        nombres = {r.nombre for r in roles}
        assert "Finanzas" in nombres
        assert "Legal" in nombres

    def test_armar_equipo(self):
        director = self._director()
        brief = {
            "cliente": "Test Corp",
            "requerimientos": ["planificacion", "roi", "contratos"],
        }
        plan = director.armar_equipo(brief)
        assert plan["cliente"] == "Test Corp"
        assert len(plan["equipo"]) >= 3  # Estrategia, Finanzas, Legal

    def test_armar_equipo_con_gaps(self):
        director = self._director()
        brief = {
            "cliente": "Test Corp",
            "requerimientos": ["planificacion", "blockchain"],
        }
        plan = director.armar_equipo(brief)
        # "blockchain" no es capacidad nativa de ningún rol,
        # pero algún rol debe cubrirlo internamente
        assert len(plan["gaps_cubiertos"]) > 0

    def test_ejecutar_equipo(self):
        director = self._director()
        brief = {
            "cliente": "Acme",
            "objetivo": "Lanzar producto",
            "orden": "Crear plan de lanzamiento",
            "requerimientos": ["planificacion", "presupuesto", "campanas"],
        }
        resultado = director.ejecutar_equipo(brief)
        assert resultado["status"] == "completado"
        assert resultado["cliente"] == "Acme"
        assert len(resultado["resultados"]) >= 3

    def test_director_no_accede_subagentes(self):
        """
        REGLA NO NEGOCIABLE: el Director no tiene método para acceder
        a los subagentes internos de un RoleAgent.
        """
        director = self._director()
        assert not hasattr(director, "subagentes")
        assert not hasattr(director, "factory")
        assert not hasattr(director, "crear_subagente")

    def test_cargar_brief_json(self):
        brief_data = {
            "cliente": "JSON Test",
            "orden": "test order",
            "requerimientos": ["planificacion"],
        }
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(brief_data, f)
            tmp_path = f.name
        try:
            loaded = TeamDirector.cargar_brief(tmp_path)
            assert loaded["cliente"] == "JSON Test"
        finally:
            os.unlink(tmp_path)

    def test_ejecutar_desde_archivo(self):
        director = self._director()
        brief_data = {
            "cliente": "File Corp",
            "orden": "plan completo",
            "requerimientos": ["roi", "seo"],
        }
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(brief_data, f)
            tmp_path = f.name
        try:
            resultado = director.ejecutar_desde_archivo(tmp_path)
            assert resultado["status"] == "completado"
            assert resultado["cliente"] == "File Corp"
        finally:
            os.unlink(tmp_path)


# =====================================================================
# Integration: Client Brief → Team → Execution
# =====================================================================


class TestIntegration:
    def test_ejemplo_brief_completo(self):
        """Carga el brief de ejemplo y ejecuta el flujo completo."""
        brief_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "clients",
            "ejemplo",
            "brief.json",
        )
        if not os.path.exists(brief_path):
            pytest.skip("brief de ejemplo no encontrado")

        reg = RoleRegistry()
        for cls in ALL_ROLES:
            reg.registrar_clase(cls)

        director = TeamDirector(registry=reg)
        resultado = director.ejecutar_desde_archivo(brief_path)

        assert resultado["status"] == "completado"
        assert resultado["cliente"] == "Mi Empresa"
        assert len(resultado["resultados"]) >= 1

    def test_gap_detection_y_generacion(self):
        """Un rol detecta gaps y genera subagentes internos sin
        que el Director intervenga."""
        role = FinanceRole()
        gaps = role.cubrir_gaps({"roi", "cripto_analisis", "nft_valuacion"})
        # roi ya existe, los otros 2 son gaps
        assert "cripto_analisis" in gaps
        assert "nft_valuacion" in gaps
        # Los subagentes fueron creados internamente
        assert len(role.factory) == 2
        sub = role.factory.buscar_por_nombre("cripto_analisis")
        assert sub is not None
        # El subagente es ejecutable
        result = sub.ejecutar(dato="test")
        assert result["gap"] == "cripto_analisis"
