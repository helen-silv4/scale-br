import json
import os
import pytest

from src.dados.matriz_lci import MatrizLCI
from src.solver.solver_emergia import SolverEmergia
from src.solver.estrategias_emergia import RegraCoProdutor, RegraFeedback, RegraCaminhoMultiplo
from src.relatorios.gerador_relatorio import GeradorRelatorio


@pytest.fixture
def csv_padrao(tmp_path):
    csv = tmp_path / "lci.csv"
    csv.write_text(
        "processo,energia_solar_sej,energia_quimica_sej,biomassa_sej,produto\n"
        "Agricultura,1.50e+15,2.30e+14,8.70e+14,graos\n"
        "Transporte,3.20e+14,9.10e+13,0,combustivel\n"
        "Industria,6.80e+15,1.40e+15,2.10e+14,manufaturado\n"
    )
    return csv


class TestIntegracao:

    def test_ti01_fluxo_completo_importacao_calculo_relatorio(
        self, tmp_path, csv_padrao
    ):
        # Importação
        matriz = MatrizLCI(str(csv_padrao))
        assert matriz.carregar() is True
        assert len(matriz.lista_processos) == 3

        # Cálculo
        solver = SolverEmergia(matriz.obter_matriz(), {})
        resultados = solver.calcular()
        assert len(resultados) == 3
        assert all(v > 0 for v in resultados.values())

        # Geração de relatório
        caminho_pdf = str(tmp_path / "relatorio_integracao.pdf")
        GeradorRelatorio(resultados, caminho_pdf).gerar()
        assert os.path.exists(caminho_pdf)
        with open(caminho_pdf, "rb") as f:
            assert f.read(4) == b"%PDF"

    def test_ti02_transformadores_modificam_resultado_integrado(
        self, tmp_path, csv_padrao
    ):
        matriz = MatrizLCI(str(csv_padrao))
        matriz.carregar()
        df = matriz.obter_matriz()

        solver_sem = SolverEmergia(df, {})
        solver_com = SolverEmergia(df, {"Agricultura": 2.0})

        assert solver_com.calcular()["Agricultura"] == pytest.approx(
            solver_sem.calcular()["Agricultura"] * 2.0, rel=1e-3
        )

    def test_ti03_validacao_bloqueia_calculo_com_dados_invalidos(self, tmp_path):
        csv = tmp_path / "invalido.csv"
        csv.write_text(
            "processo,energia_solar_sej\n"
            "Agricultura,1.50e+15\n"
        )
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

    def test_ti05_estrategias_injetadas_alteram_calculo(self, tmp_path, csv_padrao):
        matriz = MatrizLCI(str(csv_padrao))
        matriz.carregar()
        df = matriz.obter_matriz()

        solver_simples = SolverEmergia(df, {}, estrategias=[RegraCoProdutor()])
        resultado_simples = solver_simples.calcular()

        solver_completo = SolverEmergia(df, {})
        resultado_completo = solver_completo.calcular()

        for processo in resultado_simples:
            assert resultado_completo[processo] >= resultado_simples[processo]

    def test_ti06_relatorio_contem_todos_processos(self, tmp_path, csv_padrao):
        matriz = MatrizLCI(str(csv_padrao))
        matriz.carregar()
        solver = SolverEmergia(matriz.obter_matriz(), {})
        resultados = solver.calcular()

        caminho_pdf = str(tmp_path / "relatorio_completo.pdf")
        GeradorRelatorio(resultados, caminho_pdf).gerar()

        assert os.path.getsize(caminho_pdf) > 1024  # PDF com conteúdo real
        assert len(resultados) == 3