import pandas as pd


class MatrizLCI:
    COLUNAS_OBRIGATORIAS = [
        "processo",
        "energia_solar_sej",
        "energia_quimica_sej",
        "biomassa_sej",
        "produto"
    ]

    def __init__(self, caminho_arquivo: str):
        self.caminho_arquivo = caminho_arquivo
        self.dados_matriz = None
        self.lista_processos = []

    def carregar(self):
        """Carrega o arquivo CSV ou Excel e armazena os dados."""
        try:
            if self.caminho_arquivo.endswith(".csv"):
                self.dados_matriz = pd.read_csv(self.caminho_arquivo)
            elif self.caminho_arquivo.endswith((".xlsx", ".xls")):
                self.dados_matriz = pd.read_excel(self.caminho_arquivo)
            else:
                raise ValueError(
                    f"Formato não suportado. Use CSV ou Excel."
                )
            self.validar()
            self.lista_processos = self.dados_matriz["processo"].tolist()
            return True

        except FileNotFoundError:
            raise FileNotFoundError(
                f"Arquivo não encontrado: {self.caminho_arquivo}"
            )
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Erro ao carregar arquivo: {str(e)}")

    def validar(self):
        """Valida a estrutura e os dados da matriz carregada."""
        if self.dados_matriz is None:
            raise ValueError("Nenhum dado carregado para validar.")

        # Verifica colunas obrigatórias
        colunas_ausentes = [
            col for col in self.COLUNAS_OBRIGATORIAS
            if col not in self.dados_matriz.columns
        ]
        if colunas_ausentes:
            raise ValueError(
                f"Colunas obrigatórias ausentes: {', '.join(colunas_ausentes)}"
            )

        # Verifica valores nulos nas colunas numéricas
        colunas_numericas = [
            "energia_solar_sej",
            "energia_quimica_sej",
            "biomassa_sej"
        ]
        for coluna in colunas_numericas:
            if self.dados_matriz[coluna].isnull().any():
                raise ValueError(
                    f"A coluna '{coluna}' contém valores nulos."
                )

        # Verifica se há pelo menos um processo
        if len(self.dados_matriz) == 0:
            raise ValueError("A matriz não contém nenhum processo.")

        # Verifica se os valores numéricos são não negativos
        for coluna in colunas_numericas:
            if (self.dados_matriz[coluna] < 0).any():
                raise ValueError(
                    f"A coluna '{coluna}' contém valores negativos inválidos."
                )

    def obter_matriz(self) -> pd.DataFrame:
        """Retorna a matriz validada como DataFrame."""
        if self.dados_matriz is None:
            raise ValueError(
                "Matriz não carregada. Execute carregar() primeiro."
            )
        return self.dados_matriz

    def obter_resumo(self) -> str:
        """Retorna um resumo textual dos dados carregados."""
        if self.dados_matriz is None:
            return "Nenhum dado carregado."

        total_processos = len(self.dados_matriz)
        total_colunas = len(self.dados_matriz.columns)
        processos = ", ".join(self.lista_processos)

        return (
            f"Processos carregados : {total_processos}\n"
            f"Colunas identificadas: {total_colunas}\n"
            f"Processos            : {processos}"
        )