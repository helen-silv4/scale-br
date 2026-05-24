from abc import ABC, abstractmethod


class Comando(ABC):
    @abstractmethod
    def executar(self) -> None:
        ...

class ComandoLimparProjeto(Comando):


    def __init__(self, janela):
        self.janela = janela

    def executar(self) -> None:
        j = self.janela

        # estado de domínio
        j.caminho_arquivo = None
        j.matriz = None
        j.solver = None
        j.relatorio = None

        # área de importação
        j.lbl_arquivo.configure(
            text="Nenhum arquivo selecionado", text_color="gray"
        )
        j._atualizar_textbox(j.txt_resumo, "")

        # área de transformadores
        for widget in j.frame_campos_transf.winfo_children():
            widget.destroy()
        j.campos_transformadores = {}
        j.frame_transformadores.configure(height=0)
        j.secao_transf_visivel = False

        # área de resultados
        j._atualizar_textbox(j.txt_resultados, "")
        j.frame_resultados.pack_forget()

        # área de visualização
        if j.canvas_grafico:
            j.canvas_grafico.get_tk_widget().destroy()
            j.canvas_grafico = None
        if j.figura_grafico:
            j.figura_grafico.clear()
            j.figura_grafico = None
            j.eixo_grafico = None
        j.frame_visualizacao.pack_forget()
        j.secao_resultados_visivel = False

        # restaura geometria inicial
        j.janela.geometry("1180x820")
