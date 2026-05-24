from __future__ import annotations

import pandas as pd

from src.solver.estrategias_emergia import (
    EstrategiaEmergia,
    RegraCoProdutor,
    RegraFeedback,
    RegraCaminhoMultiplo,
)

_ESTRATEGIAS_PADRAO = [
    RegraCoProdutor(),
    RegraFeedback(),
    RegraCaminhoMultiplo(),
]


class SolverEmergia:

    def __init__(
        self,
        matriz: pd.DataFrame,
        transformadores: dict,
        estrategias: list[EstrategiaEmergia] | None = None,
    ):
        self.matriz = matriz
        self.transformadores = transformadores
        self.resultados: dict[str, float] = {}
        self.estrategias = estrategias if estrategias is not None else _ESTRATEGIAS_PADRAO

    def calcular(self) -> dict[str, float]:
        self.resultados = {}

        for _, linha in self.matriz.iterrows():
            processo = linha["processo"]
            emergia_base = (
                linha["energia_solar_sej"]
                + linha["energia_quimica_sej"]
                + linha["biomassa_sej"]
            )
            transformador = self.transformadores.get(processo, 1.0)

            emergia = emergia_base
            for estrategia in self.estrategias:
                emergia = estrategia.aplicar(emergia, emergia_base=emergia_base)

            self.resultados[processo] = emergia * transformador

        return self.resultados

    def aplicar_regra_coproduto(self, emergia: float) -> float:
        return RegraCoProdutor().aplicar(emergia)

    def aplicar_regra_feedback(
        self, emergia: float, fator_feedback: float = 1.05
    ) -> float:
        return RegraFeedback(fator=fator_feedback).aplicar(emergia)

    def aplicar_caminho_multiplo(
        self, emergia_feedback: float, emergia_base: float
    ) -> float:
        return RegraCaminhoMultiplo().aplicar(
            emergia_feedback, emergia_base=emergia_base
        )

    def exibir_resultados(self) -> str:
        if not self.resultados:
            return "Nenhum resultado calculado. Execute calcular() primeiro."

        separador = "=" * 45
        linhas = ["Resultados do Cálculo de Emergia", separador]
        for processo, emergia in self.resultados.items():
            linhas.append(f"{processo:<20} {emergia:.4e} sej")
        linhas += [separador, f"Total de processos analisados: {len(self.resultados)}"]
        return "\n".join(linhas)
