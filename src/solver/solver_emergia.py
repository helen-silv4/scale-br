import pandas as pd

from src.solver.estrategias_emergia import (
    EstrategiaEmergia,
    RegraCoProdutor,
    RegraFeedback,
    RegraCaminhoMultiplo,
)


class SolverEmergia:
    """
    Padrão GoF: Strategy — as regras da álgebra emergética são injetadas
    via construtor, permitindo substituição sem modificar esta classe.
    """

    def __init__(
        self,
        matriz: pd.DataFrame,
        transformadores: dict,
        estrategias: list[EstrategiaEmergia] = None,
    ):
        self.matriz = matriz
        self.transformadores = transformadores
        self.resultados = {}
        # Estratégias padrão aplicadas sequencialmente; substituíveis por injeção.
        self.estrategias: list[EstrategiaEmergia] = estrategias or [
            RegraCoProdutor(),
            RegraFeedback(),
            RegraCaminhoMultiplo(),
        ]

    def calcular(self) -> dict:
        """Aplica as estratégias sequencialmente a cada processo da matriz."""
        self.resultados = {}

        for _, linha in self.matriz.iterrows():
            processo = linha["processo"]
            emergia_solar = linha["energia_solar_sej"]
            emergia_quimica = linha["energia_quimica_sej"]
            emergia_biomassa = linha["biomassa_sej"]

            transformador = self.transformadores.get(processo, 1.0)
            emergia_base = emergia_solar + emergia_quimica + emergia_biomassa

            emergia = emergia_base
            for estrategia in self.estrategias:
                emergia = estrategia.aplicar(emergia, emergia_base=emergia_base)

            self.resultados[processo] = emergia * transformador

        return self.resultados

    # ── Métodos legados mantidos para compatibilidade com os testes existentes ──

    def aplicar_regra_coproduto(self, emergia: float) -> float:
        """Regra dos co-produtos — delega à estratégia RegraCoProdutor."""
        return RegraCoProdutor().aplicar(emergia)

    def aplicar_regra_feedback(
        self, emergia: float, fator_feedback: float = 1.05
    ) -> float:
        """Regra do feedback — delega à estratégia RegraFeedback."""
        return RegraFeedback(fator=fator_feedback).aplicar(emergia)

    def aplicar_caminho_multiplo(
        self, emergia_feedback: float, emergia_base: float
    ) -> float:
        """Caminhos múltiplos — delega à estratégia RegraCaminhoMultiplo."""
        return RegraCaminhoMultiplo().aplicar(
            emergia_feedback, emergia_base=emergia_base
        )

    def exibir_resultados(self) -> str:
        """Formata os resultados para exibição na interface gráfica."""
        if not self.resultados:
            return "Nenhum resultado calculado. Execute calcular() primeiro."

        linhas = ["Resultados do Cálculo de Emergia", "=" * 45]
        for processo, emergia in self.resultados.items():
            linhas.append(f"{processo:<20} {emergia:.4e} sej")
        linhas.append("=" * 45)
        linhas.append(f"Total de processos analisados: {len(self.resultados)}")
        return "\n".join(linhas)