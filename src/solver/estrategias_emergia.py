from abc import ABC, abstractmethod


class EstrategiaEmergia(ABC):

    @abstractmethod
    def aplicar(self, emergia: float, **kwargs) -> float:
        ...

    @property
    @abstractmethod
    def nome(self) -> str:
        ...

class RegraCoProdutor(EstrategiaEmergia):

    def aplicar(self, emergia: float, **kwargs) -> float:
        return emergia

    @property
    def nome(self) -> str:
        return "Co-produto"

class RegraFeedback(EstrategiaEmergia):

    def __init__(self, fator: float = 1.05):
        self.fator = fator

    def aplicar(self, emergia: float, **kwargs) -> float:
        return emergia * self.fator

    @property
    def nome(self) -> str:
        return f"Feedback (×{self.fator})"

class RegraCaminhoMultiplo(EstrategiaEmergia):

    def aplicar(self, emergia: float, **kwargs) -> float:
        emergia_base = kwargs.get("emergia_base", emergia)
        return max(emergia, emergia_base)

    @property
    def nome(self) -> str:
        return "Caminho Múltiplo"
