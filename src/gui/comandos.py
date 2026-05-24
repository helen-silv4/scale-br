from abc import ABC, abstractmethod


class Comando(ABC):
    """
    Padrão GoF: Command — encapsula uma operação da interface como objeto,
    desacoplando o invocador (botão) da implementação concreta e permitindo
    extensões futuras (histórico, desfazer, registro de auditoria).
    """

    @abstractmethod
    def executar(self) -> None:
        ...


class ComandoLimparProjeto(Comando):
    """
    Retorna a interface ao estado inicial: descarta o arquivo LCI importado,
    os transformadores informados e os resultados calculados, e oculta as
    seções dependentes (Resultados e Visualização).
    """

    def __init__(self, janela):
        self.janela = janela

    def executar(self) -> None:
        j = self.janela

        # Estado de domínio
        j.caminho_arquivo = None
        j.matriz = None
        j.solver = None
        j.relatorio = None

        # Área de importação
        j.lbl_arquivo.configure(
            text="Nenhum arquivo selecionado", text_color="gray"
        )
        j.txt_resumo.configure(state="normal")
        j.txt_resumo.delete("1.0", "end")
        j.txt_resumo.configure(state="disabled")

        # Área de transformadores
        for widget in j.frame_campos_transf.winfo_children():
            widget.destroy()
        j.campos_transformadores = {}
        j.frame_transformadores.configure(height=0)
        j.secao_transf_visivel = False

        # Área de resultados
        j.txt_resultados.configure(state="normal")
        j.txt_resultados.delete("1.0", "end")
        j.txt_resultados.configure(state="disabled")
        j.frame_resultados.pack_forget()

        # Área de visualização (gráfico)
        if j.canvas_grafico:
            j.canvas_grafico.get_tk_widget().destroy()
            j.canvas_grafico = None
        j.frame_visualizacao.pack_forget()
        j.secao_resultados_visivel = False

        # Restaura geometria inicial
        j.janela.geometry("1180x820")
