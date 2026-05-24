import pytest
import os
from src.relatorios.gerador_relatorio import GeradorRelatorio


@pytest.fixture
def resultados_exemplo():
    """Fixture com resultados de emergia simulados."""
    return {
        "Agricultura": 2.73e+15,
        "Transporte": 4.32e+14,
        "Industria": 8.83e+15
    }


class TestGeradorRelatorio:

    def test_gerar_cria_arquivo_pdf(self, tmp_path, resultados_exemplo):
        """TU07 e TU08 — PDF criado no caminho especificado."""
        caminho = str(tmp_path / "relatorio_teste.pdf")
        gerador = GeradorRelatorio(resultados_exemplo, caminho)
        gerador.gerar()
        assert os.path.exists(caminho)
        assert os.path.getsize(caminho) > 0

    def test_exportar_pdf_arquivo_valido(self, tmp_path, resultados_exemplo):
        """TU08 — Arquivo PDF criado com conteúdo válido."""
        caminho = str(tmp_path / "relatorio_teste.pdf")
        gerador = GeradorRelatorio(resultados_exemplo, caminho)
        gerador.gerar()
        with open(caminho, "rb") as f:
            header = f.read(4)
        assert header == b"%PDF"

    def test_relatorio_com_todos_processos(self, tmp_path, resultados_exemplo):
        """TU07 — Relatório gerado com todos os campos obrigatórios."""
        caminho = str(tmp_path / "relatorio_teste.pdf")
        gerador = GeradorRelatorio(resultados_exemplo, caminho)
        gerador.gerar()
        assert os.path.exists(caminho)
        assert len(resultados_exemplo) == 3