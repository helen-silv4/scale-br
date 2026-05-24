import time
import pytest
import pandas as pd

from src.dados.matriz_lci import MatrizLCI
from src.solver.solver_emergia import SolverEmergia
from src.relatorios.gerador_relatorio import GeradorRelatorio


def _gerar_matriz_sintetica(n: int) -> pd.DataFrame:
    return pd.DataFrame({
        "processo": [f"Processo_{i:03d}" for i in range(n)],
        "energia_solar_sej": [1.5e15] * n,
        "energia_quimica_sej": [2.3e14] * n,
        "biomassa_sej": [8.7e14] * n,
        "produto": [f"produto_{i}" for i in range(n)],
    })

class TestDesempenho:

    def test_td01_100_processos_dentro_do_limite_de_5_segundos(self):
        matriz = _gerar_matriz_sintetica(100)
        solver = SolverEmergia(matriz, {})

        inicio = time.perf_counter()
        resultados = solver.calcular()
        duracao = time.perf_counter() - inicio

        assert len(resultados) == 100
        assert duracao < 5.0, (
            f"Cálculo de 100 processos levou {duracao:.3f}s — limite é 5s (RNF01)"
        )

    def test_td02_50_processos_abaixo_de_2_segundos(self):
        matriz = _gerar_matriz_sintetica(50)
        solver = SolverEmergia(matriz, {})

        inicio = time.perf_counter()
        solver.calcular()
        duracao = time.perf_counter() - inicio

        assert duracao < 2.0, (
            f"Cálculo de 50 processos levou {duracao:.3f}s — esperado < 2s"
        )

    def test_td03_carregamento_csv_100_linhas_abaixo_de_3_segundos(self, tmp_path):
        csv = tmp_path / "grande.csv"
        linhas = [
            "processo,energia_solar_sej,energia_quimica_sej,biomassa_sej,produto"
        ]
        for i in range(100):
            linhas.append(
                f"Processo_{i:03d},1.5e+15,2.3e+14,8.7e+14,produto_{i}"
            )
        csv.write_text("\n".join(linhas))

        inicio = time.perf_counter()
        matriz = MatrizLCI(str(csv))
        matriz.carregar()
        duracao = time.perf_counter() - inicio

        assert len(matriz.lista_processos) == 100
        assert duracao < 3.0, (
            f"Carregamento de CSV com 100 linhas levou {duracao:.3f}s — esperado < 3s"
        )

    def test_td04_geracao_de_relatorio_100_processos_abaixo_de_5_segundos(
        self, tmp_path
    ):
        resultados = {
            f"Processo_{i:03d}": 1.5e15 * (i + 1) for i in range(100)
        }
        caminho = str(tmp_path / "relatorio_desempenho.pdf")

        inicio = time.perf_counter()
        GeradorRelatorio(resultados, caminho).gerar()
        duracao = time.perf_counter() - inicio

        assert duracao < 5.0, (
            f"Geração do PDF com 100 processos levou {duracao:.3f}s — esperado < 5s"
        )

    def test_td05_calculo_multiplas_execucoes_consistente(self):
        matriz = _gerar_matriz_sintetica(20)
        referencia = SolverEmergia(matriz.copy(), {}).calcular()

        for _ in range(9):
            resultado = SolverEmergia(matriz.copy(), {}).calcular()
            for processo in referencia:
                assert resultado[processo] == pytest.approx(
                    referencia[processo], rel=1e-9
                )