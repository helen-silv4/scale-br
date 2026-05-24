import pytest
import pandas as pd
from src.solver.solver_emergia import SolverEmergia
from src.solver.estrategias_emergia import RegraCoProdutor, RegraFeedback


class TestSolverEmergia:

    def test_calcular_retorna_todos_processos(self, matriz_exemplo):
        resultados = SolverEmergia(matriz_exemplo, {}).calcular()
        assert len(resultados) == 3
        assert set(resultados.keys()) == {"Agricultura", "Transporte", "Industria"}

    def test_calcular_valores_positivos(self, matriz_exemplo):
        resultados = SolverEmergia(matriz_exemplo, {}).calcular()
        assert all(v > 0 for v in resultados.values())

    def test_regra_coproduto_preserva_emergia(self):
        solver = SolverEmergia(pd.DataFrame(), {})
        emergia = 1.50e+15
        assert solver.aplicar_regra_coproduto(emergia) == emergia

    def test_regra_feedback_expande_emergia(self):
        solver = SolverEmergia(pd.DataFrame(), {})
        emergia = 1.00e+15
        resultado = solver.aplicar_regra_feedback(emergia)
        assert resultado > emergia
        assert resultado == pytest.approx(1.05e+15, rel=1e-3)

    def test_regra_feedback_fator_customizado(self):
        solver = SolverEmergia(pd.DataFrame(), {})
        assert solver.aplicar_regra_feedback(1.0e+15, fator_feedback=2.0) == pytest.approx(2.0e+15)

    def test_caminho_multiplo_seleciona_maior(self):
        solver = SolverEmergia(pd.DataFrame(), {})
        assert solver.aplicar_caminho_multiplo(1.0e+15, 2.0e+15) == 2.0e+15
        assert solver.aplicar_caminho_multiplo(3.0e+15, 1.0e+15) == 3.0e+15

    def test_transformador_multiplica_resultado(self, matriz_exemplo):
        solver_sem = SolverEmergia(matriz_exemplo, {})
        solver_com = SolverEmergia(matriz_exemplo, {"Agricultura": 2.0})
        r_sem = solver_sem.calcular()
        r_com = solver_com.calcular()
        assert r_com["Agricultura"] == pytest.approx(r_sem["Agricultura"] * 2.0, rel=1e-3)
        assert r_com["Transporte"] == pytest.approx(r_sem["Transporte"], rel=1e-3)

    def test_estrategia_injetada_substitui_padrao(self, matriz_exemplo):
        solver = SolverEmergia(matriz_exemplo, {}, estrategias=[RegraCoProdutor()])
        resultados = solver.calcular()
        assert all(v > 0 for v in resultados.values())

    def test_exibir_resultados_sem_calculo(self):
        saida = SolverEmergia(pd.DataFrame(), {}).exibir_resultados()
        assert "Nenhum resultado calculado" in saida

    def test_exibir_resultados_apos_calculo(self, matriz_exemplo):
        solver = SolverEmergia(matriz_exemplo, {})
        solver.calcular()
        saida = solver.exibir_resultados()
        assert "Agricultura" in saida
        assert "sej" in saida
