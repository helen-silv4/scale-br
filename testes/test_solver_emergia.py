import pytest
import pandas as pd
from src.solver.solver_emergia import SolverEmergia


@pytest.fixture
def matriz_exemplo():
    return pd.DataFrame({
        "processo": ["Agricultura", "Transporte", "Industria"],
        "energia_solar_sej": [1.50e+15, 3.20e+14, 6.80e+15],
        "energia_quimica_sej": [2.30e+14, 9.10e+13, 1.40e+15],
        "biomassa_sej": [8.70e+14, 0, 2.10e+14],
        "produto": ["graos", "combustivel", "manufaturado"]
    })


class TestSolverEmergia:

    def test_calcular_retorna_resultados(self, matriz_exemplo):
        solver = SolverEmergia(matriz_exemplo, {})
        resultados = solver.calcular()
        assert len(resultados) == 3
        assert "Agricultura" in resultados
        assert "Transporte" in resultados
        assert "Industria" in resultados

    def test_regra_coproduto(self):
        solver = SolverEmergia(pd.DataFrame(), {})
        emergia = 1.50e+15
        resultado = solver.aplicar_regra_coproduto(emergia)
        assert resultado == emergia

    def test_regra_feedback(self):
        solver = SolverEmergia(pd.DataFrame(), {})
        emergia = 1.00e+15
        resultado = solver.aplicar_regra_feedback(emergia)
        assert resultado > emergia
        assert resultado == pytest.approx(1.05e+15, rel=1e-3)

    def test_caminho_multiplo_seleciona_maior(self):
        solver = SolverEmergia(pd.DataFrame(), {})
        assert solver.aplicar_caminho_multiplo(1.0e+15, 2.0e+15) == 2.0e+15
        assert solver.aplicar_caminho_multiplo(3.0e+15, 1.0e+15) == 3.0e+15

    def test_transformador_aplicado(self, matriz_exemplo):
        transformadores = {"Agricultura": 2.0}
        solver_sem = SolverEmergia(matriz_exemplo, {})
        solver_com = SolverEmergia(matriz_exemplo, transformadores)
        resultado_sem = solver_sem.calcular()
        resultado_com = solver_com.calcular()
        assert resultado_com["Agricultura"] == pytest.approx(
            resultado_sem["Agricultura"] * 2.0, rel=1e-3
        )

    def test_exibir_resultados_sem_calculo(self):
        solver = SolverEmergia(pd.DataFrame(), {})
        saida = solver.exibir_resultados()
        assert "Nenhum resultado calculado" in saida