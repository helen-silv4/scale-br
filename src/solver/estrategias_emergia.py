from abc import ABC, abstractmethod


class EstrategiaEmergia(ABC):
    """
    Padrão GoF: Strategy — interface comum para as regras da álgebra emergética.
    Permite que diferentes regras sejam injetadas e trocadas sem alterar o solver.
    """

    @abstractmethod
    def aplicar(self, emergia: float, **kwargs) -> float:
        """Aplica a regra emergética ao valor recebido e retorna o resultado."""
        pass

    @property
    @abstractmethod
    def nome(self) -> str:
        """Nome legível da estratégia, usado em logs e relatórios."""
        pass


class RegraCoProdutor(EstrategiaEmergia):
    """
    Regra dos co-produtos: a emergia total do processo é atribuída
    integralmente a cada co-produto, sem divisão entre eles.
    """

    def aplicar(self, emergia: float, **kwargs) -> float:
        return emergia

    @property
    def nome(self) -> str:
        return "Co-produto"


class RegraFeedback(EstrategiaEmergia):
    """
    Regra do feedback: fluxos de retroalimentação são incorporados
    por meio de um fator de expansão do sistema.
    O fator padrão de 1.05 representa 5 % de retroalimentação.
    """

    def __init__(self, fator: float = 1.05):
        self.fator = fator

    def aplicar(self, emergia: float, **kwargs) -> float:
        return emergia * self.fator

    @property
    def nome(self) -> str:
        return f"Feedback (×{self.fator})"


class RegraCaminhoMultiplo(EstrategiaEmergia):
    """
    Regra dos caminhos múltiplos: quando um fluxo percorre caminhos
    paralelos, seleciona-se apenas o maior valor, evitando dupla contagem.
    Requer o kwarg 'emergia_base' para comparação.
    """

    def aplicar(self, emergia: float, **kwargs) -> float:
        emergia_base = kwargs.get("emergia_base", emergia)
        return max(emergia, emergia_base)

    @property
    def nome(self) -> str:
        return "Caminho Múltiplo"