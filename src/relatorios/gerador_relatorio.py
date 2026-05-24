from fpdf import FPDF
from datetime import datetime


class GeradorRelatorio:

    def __init__(self, resultados: dict, caminho_saida: str):
        self.resultados = resultados
        self.caminho_saida = caminho_saida
        self.pdf = FPDF()

    def gerar(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()

        self._gerar_cabecalho()
        self._gerar_informacoes()
        self._gerar_tabela_resultados()
        self._gerar_rodape()

        self.exportar_pdf()

    def _gerar_cabecalho(self):
        self.pdf.set_font("Helvetica", style="B", size=16)
        self.pdf.cell(0, 10, "SCALE-BR", ln=True, align="C")

        self.pdf.set_font("Helvetica", style="", size=11)
        self.pdf.cell(
            0, 7,
            "Sistema para Calculo de Emergia baseado em Inventarios do Ciclo de Vida",
            ln=True, align="C"
        )

        self.pdf.ln(5)
        self.pdf.set_draw_color(0, 102, 204)
        self.pdf.set_line_width(0.8)
        self.pdf.line(10, self.pdf.get_y(), 200, self.pdf.get_y())
        self.pdf.ln(8)

    def _gerar_informacoes(self):
        self.pdf.set_font("Helvetica", style="B", size=12)
        self.pdf.cell(0, 8, "Informacoes da Analise", ln=True)
        self.pdf.ln(2)

        self.pdf.set_font("Helvetica", size=10)
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.pdf.cell(0, 7, f"Data e hora do calculo : {agora}", ln=True)
        self.pdf.cell(0, 7, f"Total de processos     : {len(self.resultados)}", ln=True)
        self.pdf.cell(0, 7, "Metodo                 : Algebra emergetica (TDD)", ln=True)
        self.pdf.cell(0, 7, "Unidade                : sej (emergia solar joule)", ln=True)
        self.pdf.ln(6)

    def _gerar_tabela_resultados(self):
        self.pdf.set_font("Helvetica", style="B", size=12)
        self.pdf.cell(0, 8, "Resultados do Calculo de Emergia", ln=True)
        self.pdf.ln(3)

        self.pdf.set_fill_color(0, 102, 204)
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("Helvetica", style="B", size=10)
        self.pdf.cell(90, 9, "Processo", border=1, fill=True)
        self.pdf.cell(100, 9, "Emergia Total (sej)", border=1, fill=True, ln=True)

        self.pdf.set_text_color(0, 0, 0)
        self.pdf.set_font("Helvetica", size=10)

        for i, (processo, emergia) in enumerate(self.resultados.items()):
            fill = i % 2 == 0
            self.pdf.set_fill_color(235, 245, 255) if fill else self.pdf.set_fill_color(255, 255, 255)
            self.pdf.cell(90, 8, str(processo), border=1, fill=fill)
            self.pdf.cell(100, 8, f"{emergia:.4e}", border=1, fill=fill, ln=True)

        self.pdf.ln(6)

        total = sum(self.resultados.values())
        self.pdf.set_font("Helvetica", style="B", size=10)
        self.pdf.set_fill_color(0, 102, 204)
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.cell(90, 9, "TOTAL", border=1, fill=True)
        self.pdf.cell(100, 9, f"{total:.4e} sej", border=1, fill=True, ln=True)
        self.pdf.set_text_color(0, 0, 0)

    def _gerar_rodape(self):
        self.pdf.ln(10)
        self.pdf.set_draw_color(0, 102, 204)
        self.pdf.set_line_width(0.5)
        self.pdf.line(10, self.pdf.get_y(), 200, self.pdf.get_y())
        self.pdf.ln(4)

        self.pdf.set_font("Helvetica", style="I", size=9)
        self.pdf.set_text_color(120, 120, 120)
        self.pdf.cell(
            0, 6,
            "Relatorio gerado automaticamente pelo SCALE-BR - UNIP 2026",
            ln=True, align="C"
        )

    def exportar_pdf(self):
        self.pdf.output(self.caminho_saida)