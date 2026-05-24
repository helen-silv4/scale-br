import pandas as pd


class MatrizLCI:

    COLUNAS_OBRIGATORIAS = [
        "processo",
        "energia_solar_sej",
        "energia_quimica_sej",
        "biomassa_sej",
        "produto",
    ]

    COLUNAS_NUMERICAS = [
        "energia_solar_sej",
        "energia_quimica_sej",
        "biomassa_sej",
    ]

    def __init__(self, caminho_arquivo: str):
        self.caminho_arquivo = caminho_arquivo
        self.dados_matriz = None
        self.lista_processos = []

    def carregar(self) -> bool:
        try:
            if self.caminho_arquivo.endswith(".csv"):
                self.dados_matriz = pd.read_csv(self.caminho_arquivo)
            elif self.caminho_arquivo.endswith((".xlsx", ".xls")):
                self.dados_matriz = pd.read_excel(self.caminho_arquivo)
            else:
                raise ValueError("Formato não suportado. Use CSV ou Excel.")

            self.validar()
            self.lista_processos = self.dados_matriz["processo"].tolist()
            return True

        except FileNotFoundError:
            raise FileNotFoundError(
                f"Arquivo não encontrado: {self.caminho_arquivo}"
            )
        except ValueError:
            raise
        except Exception as e:
            raise RuntimeError(f"Erro inesperado ao carregar arquivo: {e}") from e

    def validar(self) -> None:
        if self.dados_matriz is None:
            raise ValueError("Nenhum dado carregado para validar.")

        if len(self.dados_matriz) == 0:
            raise ValueError("A matriz não contém nenhum processo.")

        colunas_ausentes = [
            col for col in self.COLUNAS_OBRIGATORIAS
            if col not in self.dados_matriz.columns
        ]
        if colunas_ausentes:
            raise ValueError(
                f"Colunas obrigatórias ausentes: {', '.join(colunas_ausentes)}"
            )

        for coluna in self.COLUNAS_NUMERICAS:
            if self.dados_matriz[coluna].isnull().any():
                raise ValueError(
                    f"A coluna '{coluna}' contém valores nulos."
                )
            if (self.dados_matriz[coluna] < 0).any():
                raise ValueError(
                    f"A coluna '{coluna}' contém valores negativos inválidos."
                )

    def obter_matriz(self) -> pd.DataFrame:
        if self.dados_matriz is None:
            raise ValueError(
                "Matriz não carregada. Execute carregar() primeiro."
            )
        return self.dados_matriz

    def obter_resumo(self) -> str:
        if self.dados_matriz is None:
            return "Nenhum dado carregado."

        processos = ", ".join(self.lista_processos)
        return (
            f"Processos carregados : {len(self.dados_matriz)}\n"
            f"Colunas identificadas: {len(self.dados_matriz.columns)}\n"
            f"Processos            : {processos}"
        )
