import pandas as pd


class SolverEmergia:

    def __init__(self, matriz: pd.DataFrame, transformadores: dict):
        self.matriz = matriz
        self.transformadores = transformadores
        self.resultados = {}

    def calcular(self) -> dict:
        """Orquestra a aplicação sequencial das regras da álgebra emergética."""
        self.resultados = {}

        for _, linha in self.matriz.iterrows():
            processo = linha["processo"]

            emergia_solar = linha["energia_solar_sej"]
            emergia_quimica = linha["energia_quimica_sej"]
            emergia_biomassa = linha["biomassa_sej"]

            # Aplica transformador se informado pelo usuário
            transformador = self.transformadores.get(processo, 1.0)

            # Soma base das energias
            emergia_base = emergia_solar + emergia_quimica + emergia_biomassa

            # Aplica as três regras sequencialmente
            emergia_coproduto = self.aplicar_regra_coproduto(emergia_base)
            emergia_feedback = self.aplicar_regra_feedback(emergia_coproduto)
            emergia_final = self.aplicar_caminho_multiplo(
                emergia_feedback, emergia_base
            )

            # Aplica o transformador emergético
            self.resultados[processo] = emergia_final * transformador

        return self.resultados

    def aplicar_regra_coproduto(self, emergia: float) -> float:
        """
        Regra dos co-produtos: a emergia total do processo é atribuída
        integralmente a cada co-produto, sem divisão entre eles.
        """
        return emergia

    def aplicar_regra_feedback(self, emergia: float, fator_feedback: float = 1.05) -> float:
        """
        Regra do feedback: fluxos de retroalimentação são incorporados
        por meio de um fator de expansão do sistema.
        O fator padrão de 1.05 representa 5% de retroalimentação.
        """
        return emergia * fator_feedback

    def aplicar_caminho_multiplo(self, emergia_feedback: float, emergia_base: float) -> float:
        """
        Regra dos caminhos múltiplos: quando um fluxo percorre caminhos
        paralelos, seleciona-se apenas o maior valor, evitando dupla contagem.
        """
        return max(emergia_feedback, emergia_base)

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