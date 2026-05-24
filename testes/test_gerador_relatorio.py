import os
import matplotlib.pyplot as plt
from src.relatorios.gerador_relatorio import GeradorRelatorio


class TestGeradorRelatorio:

    def test_gerar_cria_arquivo_pdf(self, tmp_path, resultados_exemplo):
        caminho = str(tmp_path / "relatorio.pdf")
        GeradorRelatorio(resultados_exemplo, caminho).gerar()
        assert os.path.exists(caminho)
        assert os.path.getsize(caminho) > 0

    def test_exportar_pdf_cabecalho_valido(self, tmp_path, resultados_exemplo):
        caminho = str(tmp_path / "relatorio.pdf")
        GeradorRelatorio(resultados_exemplo, caminho).gerar()
        with open(caminho, "rb") as f:
            assert f.read(4) == b"%PDF"

    def test_relatorio_com_multiplos_processos(self, tmp_path, resultados_exemplo):
        caminho = str(tmp_path / "relatorio.pdf")
        GeradorRelatorio(resultados_exemplo, caminho).gerar()
        assert os.path.getsize(caminho) > 1024
        assert len(resultados_exemplo) == 3

    def test_relatorio_com_figura_matplotlib(self, tmp_path, resultados_exemplo):
        fig, ax = plt.subplots()
        ax.bar(
            list(resultados_exemplo.keys()),
            list(resultados_exemplo.values())
        )
        caminho = str(tmp_path / "relatorio_com_grafico.pdf")
        GeradorRelatorio(resultados_exemplo, caminho, figura=fig).gerar()
        plt.close(fig)
        assert os.path.exists(caminho)
        assert os.path.getsize(caminho) > 1024

    def test_relatorio_sem_figura_gera_grafico_padrao(self, tmp_path, resultados_exemplo):
        caminho = str(tmp_path / "relatorio_padrao.pdf")
        GeradorRelatorio(resultados_exemplo, caminho).gerar()
        assert os.path.exists(caminho)
        assert os.path.getsize(caminho) > 1024
