import pytest
from src.dados.matriz_lci import MatrizLCI


class TestMatrizLCI:

    def test_carregar_csv_valido(self, tmp_path):
        csv = tmp_path / "teste.csv"
        csv.write_text(
            "processo,energia_solar_sej,energia_quimica_sej,biomassa_sej,produto\n"
            "Agricultura,1.50e+15,2.30e+14,8.70e+14,graos\n"
        )
        matriz = MatrizLCI(str(csv))
        assert matriz.carregar() is True
        assert len(matriz.dados_matriz) == 1
        assert "Agricultura" in matriz.lista_processos

    def test_carregar_formato_invalido(self, tmp_path):
        arquivo = tmp_path / "teste.txt"
        arquivo.write_text("conteudo qualquer")
        with pytest.raises(ValueError, match="Formato não suportado"):
            MatrizLCI(str(arquivo)).carregar()

    def test_validar_colunas_ausentes(self, tmp_path):
        csv = tmp_path / "teste.csv"
        csv.write_text(
            "processo,energia_solar_sej\n"
            "Agricultura,1.50e+15\n"
        )
        with pytest.raises(ValueError, match="Colunas obrigatórias ausentes"):
            MatrizLCI(str(csv)).carregar()

    def test_carregar_arquivo_inexistente(self):
        with pytest.raises(FileNotFoundError):
            MatrizLCI("nao_existe.csv").carregar()

    def test_obter_matriz_sem_carregar(self):
        with pytest.raises(ValueError, match="Matriz não carregada"):
            MatrizLCI("qualquer.csv").obter_matriz()

    def test_obter_resumo(self, tmp_path):
        csv = tmp_path / "teste.csv"
        csv.write_text(
            "processo,energia_solar_sej,energia_quimica_sej,biomassa_sej,produto\n"
            "Agricultura,1.50e+15,2.30e+14,8.70e+14,graos\n"
            "Transporte,3.20e+14,9.10e+13,0,combustivel\n"
        )
        matriz = MatrizLCI(str(csv))
        matriz.carregar()
        resumo = matriz.obter_resumo()
        assert "2" in resumo
        assert "Agricultura" in resumo
        assert "Transporte" in resumo

    def test_validar_valores_negativos(self, tmp_path):
        csv = tmp_path / "teste.csv"
        csv.write_text(
            "processo,energia_solar_sej,energia_quimica_sej,biomassa_sej,produto\n"
            "Agricultura,-1.50e+15,2.30e+14,8.70e+14,graos\n"
        )
        with pytest.raises(ValueError, match="valores negativos"):
            MatrizLCI(str(csv)).carregar()

    def test_validar_matriz_vazia(self, tmp_path):
        csv = tmp_path / "teste.csv"
        csv.write_text(
            "processo,energia_solar_sej,energia_quimica_sej,biomassa_sej,produto\n"
        )
        with pytest.raises(ValueError, match="nenhum processo"):
            MatrizLCI(str(csv)).carregar()
