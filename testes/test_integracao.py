import json
import os
import pytest

from src.dados.matriz_lci import MatrizLCI
from src.solver.solver_emergia import SolverEmergia
from src.solver.estrategias_emergia import RegraCoProdutor
from src.relatorios.gerador_relatorio import GeradorRelatorio


class TestIntegracao:

    def test_ti01_fluxo_completo_importacao_calculo_relatorio(
        self, tmp_path, csv_padrao
    ):
        matriz = MatrizLCI(str(csv_padrao))
        assert matriz.carregar() is True
        assert len(matriz.lista_processos) == 3

        solver = SolverEmergia(matriz.obter_matriz(), {})
        resultados = solver.calcular()
        assert len(resultados) == 3
        assert all(v > 0 for v in resultados.values())

        caminho_pdf = str(tmp_path / "relatorio_ti01.pdf")
        GeradorRelatorio(resultados, caminho_pdf).gerar()
        assert os.path.exists(caminho_pdf)
        with open(caminho_pdf, "rb") as f:
            assert f.read(4) == b"%PDF"

    def test_ti02_transformadores_modificam_resultado(self, csv_padrao):
        matriz = MatrizLCI(str(csv_padrao))
        matriz.carregar()
        df = matriz.obter_matriz()

        solver_sem = SolverEmergia(df, {})
        solver_com = SolverEmergia(df, {"Agricultura": 2.0})

        assert solver_com.calcular()["Agricultura"] == pytest.approx(
            solver_sem.calcular()["Agricultura"] * 2.0, rel=1e-3
        )

    def test_ti03_validacao_bloqueia_arquivo_invalido(self, tmp_path):
        csv = tmp_path / "invalido.csv"
        csv.write_text("processo,energia_solar_sej\nAgricultura,1.50e+15\n")
        with pytest.raises(ValueError, match="Colunas obrigatórias ausentes"):
            MatrizLCI(str(csv)).carregar()

    def test_ti04_ciclo_salvar_carregar_preserva_resultados(
        self, tmp_path, csv_padrao
    ):
        matriz = MatrizLCI(str(csv_padrao))
        matriz.carregar()
        solver = SolverEmergia(matriz.obter_matriz(), {"Agricultura": 1.5})
        resultados_originais = solver.calcular()

        arquivo_projeto = tmp_path / "projeto.json"
        projeto = {
            "caminho_arquivo": str(csv_padrao),
            "transformadores": {"Agricultura": 1.5},
            "resultados": resultados_originais,
        }
        with open(arquivo_projeto, "w") as f:
            json.dump(projeto, f)

        with open(arquivo_projeto, "r") as f:
            projeto_carregado = json.load(f)

        assert projeto_carregado["resultados"]["Agricultura"] == pytest.approx(
            resultados_originais["Agricultura"], rel=1e-3
        )
        assert set(projeto_carregado["resultados"].keys()) == set(
            resultados_originais.keys()
        )

    def test_ti05_estrategia_simples_produz_resultado_menor(self, csv_padrao):
        matriz = MatrizLCI(str(csv_padrao))
        matriz.carregar()
        df = matriz.obter_matriz()

        resultado_simples  = SolverEmergia(df, {}, estrategias=[RegraCoProdutor()]).calcular()
        resultado_completo = SolverEmergia(df, {}).calcular()

        for processo in resultado_simples:
            assert resultado_completo[processo] >= resultado_simples[processo]

    def test_ti06_relatorio_com_grafico_integrado(self, tmp_path, csv_padrao):
        matriz = MatrizLCI(str(csv_padrao))
        matriz.carregar()
        resultados = SolverEmergia(matriz.obter_matriz(), {}).calcular()

        caminho_sem = str(tmp_path / "sem_grafico.pdf")
        caminho_com = str(tmp_path / "com_grafico.pdf")

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.bar(list(resultados.keys()), list(resultados.values()))

        GeradorRelatorio(resultados, caminho_sem).gerar()
        GeradorRelatorio(resultados, caminho_com, figura=fig).gerar()
        plt.close(fig)

        assert os.path.getsize(caminho_sem) > 10_000
        assert os.path.getsize(caminho_com) > 10_000
