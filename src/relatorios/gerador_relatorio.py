import io
import tempfile
import os
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fpdf import FPDF
from fpdf.enums import XPos, YPos


class GeradorRelatorio:

    _COR_AZUL    = (0, 102, 204)
    _COR_AZUL_BG = (235, 245, 255)
    _COR_BRANCO  = (255, 255, 255)
    _COR_CINZA   = (120, 120, 120)

    def __init__(
        self,
        resultados: dict,
        caminho_saida: str,
        figura: plt.Figure | None = None,
    ):
        self.resultados = resultados
        self.caminho_saida = caminho_saida
        self.figura = figura
        self.pdf = FPDF()

    def gerar(self) -> None:
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()

        self._gerar_cabecalho()
        self._gerar_informacoes()
        self._gerar_tabela_resultados()
        self._gerar_grafico()
        self._gerar_rodape()

        self.exportar_pdf()

    def _linha(self, x2: int = 200) -> None:
        self.pdf.set_draw_color(*self._COR_AZUL)
        self.pdf.line(10, self.pdf.get_y(), x2, self.pdf.get_y())

    def _gerar_cabecalho(self) -> None:
        self.pdf.set_font("Helvetica", style="B", size=16)
        self.pdf.cell(
            0, 10, "SCALE-BR",
            new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C"
        )
        self.pdf.set_font("Helvetica", size=11)
        self.pdf.cell(
            0, 7,
            "Sistema para Calculo de Emergia baseado em Inventarios do Ciclo de Vida",
            new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C"
        )
        self.pdf.ln(5)
        self.pdf.set_line_width(0.8)
        self._linha()
        self.pdf.ln(8)

    def _gerar_informacoes(self) -> None:
        self.pdf.set_font("Helvetica", style="B", size=12)
        self.pdf.cell(
            0, 8, "Informacoes da Analise",
            new_x=XPos.LMARGIN, new_y=YPos.NEXT
        )
        self.pdf.ln(2)

        self.pdf.set_font("Helvetica", size=10)
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        for linha in [
            f"Data e hora do calculo : {agora}",
            f"Total de processos     : {len(self.resultados)}",
            "Metodo                 : Algebra emergetica (TDD)",
            "Unidade                : sej (emergia solar joule)",
        ]:
            self.pdf.cell(
                0, 7, linha,
                new_x=XPos.LMARGIN, new_y=YPos.NEXT
            )
        self.pdf.ln(6)

    def _gerar_tabela_resultados(self) -> None:
        self.pdf.set_font("Helvetica", style="B", size=12)
        self.pdf.cell(
            0, 8, "Resultados do Calculo de Emergia",
            new_x=XPos.LMARGIN, new_y=YPos.NEXT
        )
        self.pdf.ln(3)

        # cabeçalho da tabela
        self.pdf.set_fill_color(*self._COR_AZUL)
        self.pdf.set_text_color(*self._COR_BRANCO)
        self.pdf.set_font("Helvetica", style="B", size=10)
        self.pdf.cell(90, 9, "Processo", border=1, fill=True)
        self.pdf.cell(
            100, 9, "Emergia Total (sej)", border=1, fill=True,
            new_x=XPos.LMARGIN, new_y=YPos.NEXT
        )

        # linhas da tabela
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.set_font("Helvetica", size=10)
        for i, (processo, emergia) in enumerate(self.resultados.items()):
            fill = i % 2 == 0
            self.pdf.set_fill_color(
                *(self._COR_AZUL_BG if fill else self._COR_BRANCO)
            )
            self.pdf.cell(90, 8, str(processo), border=1, fill=fill)
            self.pdf.cell(
                100, 8, f"{emergia:.4e}", border=1, fill=fill,
                new_x=XPos.LMARGIN, new_y=YPos.NEXT
            )

        self.pdf.ln(6)

        # linha de total
        total = sum(self.resultados.values())
        self.pdf.set_font("Helvetica", style="B", size=10)
        self.pdf.set_fill_color(*self._COR_AZUL)
        self.pdf.set_text_color(*self._COR_BRANCO)
        self.pdf.cell(90, 9, "TOTAL", border=1, fill=True)
        self.pdf.cell(
            100, 9, f"{total:.4e} sej", border=1, fill=True,
            new_x=XPos.LMARGIN, new_y=YPos.NEXT
        )
        self.pdf.set_text_color(0, 0, 0)

    def _gerar_grafico(self) -> None:
        self.pdf.ln(10)
        self.pdf.set_font("Helvetica", style="B", size=12)
        self.pdf.cell(
            0, 8, "Visualizacao dos Fluxos de Emergia",
            new_x=XPos.LMARGIN, new_y=YPos.NEXT
        )
        self.pdf.ln(3)

        # Usa a figura passada ou gera uma nova
        figura = self.figura or self._gerar_figura_padrao()

        # salva temporariamente como PNG e insere no PDF
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        try:
            figura.savefig(tmp.name, format="png", dpi=150, bbox_inches="tight")
            tmp.close()
            self.pdf.image(tmp.name, x=15, w=180)
        finally:
            os.unlink(tmp.name)
            if self.figura is None:
                plt.close(figura)

        self.pdf.ln(6)

    def _gerar_figura_padrao(self) -> plt.Figure:
        processos = list(self.resultados.keys())
        valores = list(self.resultados.values())

        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor("#f0f0f0")
        ax.set_facecolor("#ffffff")
        ax.bar(processos, valores, color="#1f6aa5", edgecolor="#145280", linewidth=0.8)
        ax.set_ylabel("Emergia (sej)", fontsize=12)
        ax.set_title("Fluxos de Emergia por Processo", fontsize=14, pad=10)
        ax.yaxis.grid(True, color="#cccccc", linewidth=0.5, linestyle="--")
        ax.set_axisbelow(True)
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f"{x:.2e}")
        )
        plt.xticks(rotation=15, ha="right")
        fig.tight_layout()
        return fig

    def _gerar_rodape(self) -> None:
        self.pdf.ln(10)
        self.pdf.set_line_width(0.5)
        self._linha()
        self.pdf.ln(4)
        self.pdf.set_font("Helvetica", style="I", size=9)
        self.pdf.set_text_color(*self._COR_CINZA)
        self.pdf.cell(
            0, 6,
            "Relatorio gerado automaticamente pelo SCALE-BR - UNIP 2026",
            new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C"
        )

    def exportar_pdf(self) -> None:
        self.pdf.output(self.caminho_saida)
