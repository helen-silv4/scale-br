import json
import os

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import customtkinter as ctk
from tkinter import filedialog, messagebox

from src.dados.matriz_lci import MatrizLCI
from src.solver.solver_emergia import SolverEmergia
from src.relatorios.gerador_relatorio import GeradorRelatorio
from src.gui.comandos import ComandoLimparProjeto

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

CAMINHO_ICONE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "scale_br.ico"
)

TRANSFORMADORES_PADRAO = {
    "agricultura": 1.5e+15,
    "soja":        1.5e+15,
    "milho":       1.32e+15,
    "transporte":  3.2e+14,
    "rodoviario":  3.2e+14,
    "ferroviario": 1.85e+14,
    "industria":   6.8e+15,
    "alimentos":   6.8e+15,
    "textil":      5.45e+15,
    "tratamento":  2.9e+14,
    "agua":        2.9e+14,
    "esgoto":      1.75e+14,
    "energia":     4.2e+13,
    "solar":       4.2e+13,
    "biomassa":    3.6e+14,
    "combustivel": 5.4e+04,
}


class JanelaPrincipal:

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("SCALE-BR")
        largura, altura = 1180, 820
        x = (self.janela.winfo_screenwidth() - largura) // 2
        y = (self.janela.winfo_screenheight() - altura) // 2
        self.janela.geometry(f"{largura}x{altura}+{x}+{y}")
        self.janela.resizable(True, True)
        try:
            self.janela.iconbitmap(CAMINHO_ICONE)
        except Exception:
            pass

        self.caminho_arquivo = None
        self.matriz = None
        self.solver = None
        self.relatorio = None
        self.campos_transformadores = {}
        self.canvas_grafico = None
        self.figura_grafico = None
        self.eixo_grafico = None
        self.secao_resultados_visivel = False
        self.secao_transf_visivel = False
        self.modo_escuro = False

        self._construir_interface()

    # construção da interface

    def _construir_interface(self):
        ctk.CTkLabel(
            self.janela,
            text="SCALE-BR",
            font=ctk.CTkFont(size=26, weight="bold"),
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            self.janela,
            text="Sistema para Cálculo de Emergia baseado em Inventários do Ciclo de Vida",
            font=ctk.CTkFont(size=16),
            text_color="gray",
        ).pack(pady=(0, 8))

        frame_topo = ctk.CTkFrame(self.janela, fg_color="transparent")
        frame_topo.pack(anchor="ne", padx=24, pady=(0, 10))

        self.btn_tema = ctk.CTkButton(
            frame_topo,
            text="🌙  Modo escuro",
            command=self._alternar_tema,
            width=150, height=34,
            fg_color="gray30", hover_color="gray20",
            font=ctk.CTkFont(size=15),
            corner_radius=6,
        )
        self.btn_tema.pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            frame_topo,
            text="✕  Sair",
            command=self.janela.destroy,
            width=110, height=34,
            fg_color="#8B1A1A", hover_color="#6B1010",
            font=ctk.CTkFont(size=15),
            corner_radius=6,
        ).pack(side="left")

        self.frame_principal = ctk.CTkScrollableFrame(self.janela, corner_radius=0)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self._construir_area_importacao(self.frame_principal)
        self._construir_area_transformadores(self.frame_principal)
        self._construir_area_resultados(self.frame_principal)
        self._construir_area_visualizacao(self.frame_principal)
        self._construir_area_exportacao(self.frame_principal)

    def _construir_area_importacao(self, pai):
        frame = ctk.CTkFrame(pai, corner_radius=10)
        frame.pack(fill="x", pady=8)

        ctk.CTkLabel(
            frame,
            text="Importação de Matriz LCI",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(anchor="w", padx=15, pady=(12, 5))

        frame_arquivo = ctk.CTkFrame(frame, fg_color="transparent")
        frame_arquivo.pack(fill="x", padx=15, pady=5)

        self.lbl_arquivo = ctk.CTkLabel(
            frame_arquivo,
            text="Nenhum arquivo selecionado",
            text_color="gray",
            font=ctk.CTkFont(size=15),
        )
        self.lbl_arquivo.pack(side="left", expand=True, fill="x")

        ctk.CTkButton(
            frame_arquivo,
            text="Selecionar arquivo (CSV/Excel)",
            command=self.importar_lci,
            width=260, height=36,
            font=ctk.CTkFont(size=15),
        ).pack(side="right")

        ctk.CTkButton(
            frame_arquivo,
            text="✕  Limpar",
            command=self._limpar_projeto,
            width=130, height=36,
            fg_color="gray40", hover_color="gray30",
            font=ctk.CTkFont(size=15),
        ).pack(side="right", padx=(0, 8))

        self.txt_resumo = ctk.CTkTextbox(
            frame, height=90,
            font=ctk.CTkFont(size=15, family="Courier")
        )
        self.txt_resumo.pack(fill="x", padx=15, pady=(5, 15))
        self.txt_resumo.configure(state="disabled")

    def _construir_area_transformadores(self, pai):
        self.frame_transformadores = ctk.CTkFrame(pai, corner_radius=10)
        self.frame_transformadores.pack(fill="x", pady=8)

        ctk.CTkLabel(
            self.frame_transformadores,
            text="Transformadores Emergéticos (sej/J)",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(anchor="w", padx=15, pady=(12, 5))

        ctk.CTkLabel(
            self.frame_transformadores,
            text=(
                "O transformador emergético indica a quantidade de emergia solar (sej) necessária\n"
                "para gerar uma unidade de energia de cada processo. Valores da literatura científica.\n"
                "Se deixado em branco, o sistema usa o valor padrão de 1.0 (sem amplificação)."
            ),
            text_color="gray",
            font=ctk.CTkFont(size=15),
            justify="left",
        ).pack(anchor="w", padx=15, pady=(0, 8))

        ctk.CTkButton(
            self.frame_transformadores,
            text="📋  Usar valores padrão da literatura",
            command=self._preencher_valores_padrao,
            width=320, height=36,
            fg_color="gray40", hover_color="gray30",
            font=ctk.CTkFont(size=15),
        ).pack(anchor="w", padx=15, pady=(0, 10))

        self.frame_campos_transf = ctk.CTkFrame(
            self.frame_transformadores, fg_color="transparent"
        )
        self.frame_campos_transf.pack(fill="x", padx=15, pady=(0, 10))

        ctk.CTkButton(
            self.frame_transformadores,
            text="▶  Executar cálculo de emergia",
            command=self.executar_calculo,
            font=ctk.CTkFont(size=17, weight="bold"),
            height=46, corner_radius=8,
        ).pack(pady=(0, 15), padx=15, fill="x")

        self.frame_transformadores.configure(height=0)

    def _construir_area_resultados(self, pai):
        self.frame_resultados = ctk.CTkFrame(pai, corner_radius=10)
        self.frame_resultados.pack_forget()

        ctk.CTkLabel(
            self.frame_resultados,
            text="Resultados",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(anchor="w", padx=15, pady=(12, 5))

        self.txt_resultados = ctk.CTkTextbox(
            self.frame_resultados, height=220,
            font=ctk.CTkFont(size=15, family="Courier")
        )
        self.txt_resultados.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.txt_resultados.configure(state="disabled")

    def _construir_area_visualizacao(self, pai):
        self.frame_visualizacao = ctk.CTkFrame(pai, corner_radius=10)
        self.frame_visualizacao.pack_forget()

        ctk.CTkLabel(
            self.frame_visualizacao,
            text="Visualização de Fluxos de Emergia",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(anchor="w", padx=15, pady=(12, 5))

        self.frame_grafico = ctk.CTkFrame(
            self.frame_visualizacao, fg_color="transparent"
        )
        self.frame_grafico.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def _construir_area_exportacao(self, pai):
        self.frame_exportacao = ctk.CTkFrame(pai, corner_radius=10)
        self.frame_exportacao.pack(fill="x", pady=8)

        ctk.CTkLabel(
            self.frame_exportacao,
            text="Exportação e Projeto",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(anchor="w", padx=15, pady=(12, 8))

        frame_botoes = ctk.CTkFrame(self.frame_exportacao, fg_color="transparent")
        frame_botoes.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkButton(
            frame_botoes,
            text="📄  Gerar relatório PDF",
            command=self.exportar_relatorio,
            width=220, height=36,
            font=ctk.CTkFont(size=15),
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            frame_botoes,
            text="💾  Salvar projeto",
            command=self.salvar_projeto,
            width=180, height=36,
            fg_color="gray40", hover_color="gray30",
            font=ctk.CTkFont(size=15),
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            frame_botoes,
            text="📂  Carregar projeto",
            command=self.carregar_projeto,
            width=190, height=36,
            fg_color="gray40", hover_color="gray30",
            font=ctk.CTkFont(size=15),
        ).pack(side="left")

    # helpers de UI

    def _atualizar_textbox(self, textbox, texto: str):
        """Método unificado para atualizar qualquer CTkTextbox."""
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("end", texto)
        textbox.configure(state="disabled")

    def _exibir_resumo(self, texto: str):
        self._atualizar_textbox(self.txt_resumo, texto)

    def _exibir_resultado(self, texto: str):
        self._atualizar_textbox(self.txt_resultados, texto)

    def _revelar_secoes_resultado(self):
        if not self.secao_resultados_visivel:
            self.frame_resultados.pack(
                fill="both", expand=True, pady=8,
                before=self.frame_exportacao
            )
            self.frame_visualizacao.pack(
                fill="both", expand=True, pady=8,
                before=self.frame_exportacao
            )
            self.janela.geometry("1180x980")
            self.secao_resultados_visivel = True

    def _revelar_transformadores(self):
        if not self.secao_transf_visivel:
            self.frame_transformadores.configure(height=-1)
            self.secao_transf_visivel = True

    def _cores_tema(self) -> dict:
        """Retorna paleta de cores conforme o tema ativo."""
        if self.modo_escuro:
            return {
                "fundo": "#2b2b2b", "area": "#333333",
                "texto": "white",   "grade": "#444444",
                "barra": "#1f6aa5", "borda": "#4a9de2",
            }
        return {
            "fundo": "#f0f0f0", "area": "#ffffff",
            "texto": "#1a1a1a", "grade": "#cccccc",
            "barra": "#1f6aa5", "borda": "#145280",
        }

    def _alternar_tema(self):
        self.modo_escuro = not self.modo_escuro
        if self.modo_escuro:
            ctk.set_appearance_mode("dark")
            self.btn_tema.configure(text="☀  Modo claro")
        else:
            ctk.set_appearance_mode("light")
            self.btn_tema.configure(text="🌙  Modo escuro")
        if self.secao_resultados_visivel:
            self.janela.after_idle(self._atualizar_grafico)

    def _atualizar_campos_transformadores(self):
        for widget in self.frame_campos_transf.winfo_children():
            widget.destroy()
        self.campos_transformadores = {}

        for processo in self.matriz.lista_processos:
            linha = ctk.CTkFrame(self.frame_campos_transf, fg_color="transparent")
            linha.pack(fill="x", pady=3)

            ctk.CTkLabel(
                linha, text=f"{processo}:",
                width=200, anchor="w",
                font=ctk.CTkFont(size=15),
            ).pack(side="left", padx=(0, 8))

            entrada = ctk.CTkEntry(
                linha, width=240, height=34,
                placeholder_text="ex: 1.5e+15 (opcional)",
                font=ctk.CTkFont(size=15),
            )
            entrada.pack(side="left")

            ctk.CTkLabel(
                linha, text="sej/J",
                text_color="gray",
                font=ctk.CTkFont(size=14),
            ).pack(side="left", padx=(6, 0))

            self.campos_transformadores[processo] = entrada

    def _coletar_transformadores(self) -> dict:
        return {
            processo: float(entrada.get().strip())
            for processo, entrada in self.campos_transformadores.items()
            if entrada.get().strip()
        }

    def _preencher_valores_padrao(self):
        if not self.campos_transformadores:
            messagebox.showwarning(
                "Atenção", "Carregue um arquivo LCI antes de usar valores padrão."
            )
            return

        preenchidos = 0
        for processo, entrada in self.campos_transformadores.items():
            chave = processo.lower()
            valor = next(
                (v for k, v in TRANSFORMADORES_PADRAO.items()
                 if k in chave or chave in k),
                None,
            )
            if valor:
                entrada.delete(0, "end")
                entrada.insert(0, f"{valor:.2e}")
                preenchidos += 1

        if preenchidos == 0:
            messagebox.showinfo(
                "Valores padrão",
                "Nenhum processo correspondeu aos valores padrão da literatura.\n"
                "Preencha os transformadores manualmente.",
            )
        else:
            messagebox.showinfo(
                "Valores padrão",
                f"{preenchidos} transformador(es) preenchido(s) com valores da literatura.\n"
                "Você pode editar os valores antes de executar o cálculo.",
            )

    def _atualizar_grafico(self):
        if not self.solver or not self.solver.resultados:
            return

        processos = list(self.solver.resultados.keys())
        valores = list(self.solver.resultados.values())
        cores = self._cores_tema()

        if self.figura_grafico is None or self.eixo_grafico is None:
            self.figura_grafico, self.eixo_grafico = plt.subplots(figsize=(8, 3.5))
            self.canvas_grafico = FigureCanvasTkAgg(
                self.figura_grafico, master=self.frame_grafico
            )
            self.canvas_grafico.get_tk_widget().pack(fill="both", expand=True)

        fig, ax = self.figura_grafico, self.eixo_grafico
        ax.clear()
        fig.patch.set_facecolor(cores["fundo"])
        ax.set_facecolor(cores["area"])
        ax.bar(processos, valores, color=cores["barra"],
               edgecolor=cores["borda"], linewidth=0.8)
        ax.set_ylabel("Emergia (sej)", color=cores["texto"], fontsize=13)
        ax.set_title("Fluxos de Emergia por Processo",
                     color=cores["texto"], fontsize=15, pad=10)
        ax.tick_params(colors=cores["texto"], labelsize=12)
        ax.yaxis.get_offset_text().set_color(cores["texto"])
        ax.yaxis.grid(True, color=cores["grade"], linewidth=0.5, linestyle="--")
        ax.set_axisbelow(True)
        for spine in ax.spines.values():
            spine.set_edgecolor(cores["grade"])
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f"{x:.2e}")
        )
        plt.xticks(rotation=15, ha="right")
        fig.tight_layout()
        self.canvas_grafico.draw_idle()

    # ações principais

    def _limpar_projeto(self):
        ComandoLimparProjeto(self).executar()

    def importar_lci(self):
        caminho = filedialog.askopenfilename(
            title="Selecionar arquivo LCI",
            filetypes=[
                ("Arquivos compatíveis", "*.csv *.xlsx *.xls"),
                ("CSV", "*.csv"),
                ("Excel", "*.xlsx *.xls"),
            ],
        )
        if not caminho:
            return
        try:
            self.matriz = MatrizLCI(caminho)
            self.matriz.carregar()
            self.caminho_arquivo = caminho
            self.lbl_arquivo.configure(text=caminho, text_color="black")
            self._exibir_resumo(self.matriz.obter_resumo())
            self._atualizar_campos_transformadores()
            self._revelar_transformadores()
        except Exception as e:
            messagebox.showerror("Erro ao carregar arquivo", str(e))

    def executar_calculo(self):
        if not self.matriz:
            messagebox.showwarning(
                "Atenção", "Selecione um arquivo LCI antes de calcular."
            )
            return
        try:
            self.solver = SolverEmergia(
                self.matriz.obter_matriz(),
                self._coletar_transformadores()
            )
            self.solver.calcular()
            self._exibir_resultado(self.solver.exibir_resultados())
            self._revelar_secoes_resultado()
            self._atualizar_grafico()
        except ValueError:
            messagebox.showerror(
                "Erro", "Os transformadores devem ser valores numéricos."
            )
        except Exception as e:
            messagebox.showerror("Erro no cálculo", str(e))

    def exportar_relatorio(self):
        if not self.solver or not self.solver.resultados:
            messagebox.showwarning(
                "Atenção", "Execute o cálculo antes de gerar o relatório."
            )
            return
        try:
            caminho = filedialog.asksaveasfilename(
                title="Salvar relatório",
                defaultextension=".pdf",
                filetypes=[("PDF", "*.pdf")],
                initialfile="relatorio_scale_br.pdf",
            )
            if caminho:
                self.relatorio = GeradorRelatorio(
                    self.solver.resultados,
                    caminho,
                    figura=self.figura_grafico  # passa o gráfico da interface
                )
                self.relatorio.gerar()
                messagebox.showinfo(
                    "Sucesso", f"Relatório gerado com sucesso!\n{caminho}"
                )
        except Exception as e:
            messagebox.showerror("Erro ao gerar relatório", str(e))

    def salvar_projeto(self):
        if not self.matriz:
            messagebox.showwarning(
                "Atenção", "Carregue um arquivo LCI antes de salvar."
            )
            return
        try:
            caminho = filedialog.asksaveasfilename(
                title="Salvar projeto",
                defaultextension=".json",
                filetypes=[("Projeto SCALE-BR", "*.json")],
                initialfile="projeto_scale_br.json",
            )
            if not caminho:
                return
            projeto = {
                "caminho_arquivo": self.caminho_arquivo,
                "transformadores": self._coletar_transformadores(),
                "resultados": self.solver.resultados if self.solver else {},
            }
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(projeto, f, ensure_ascii=False, indent=2)
            messagebox.showinfo(
                "Sucesso", f"Projeto salvo com sucesso!\n{caminho}"
            )
        except Exception as e:
            messagebox.showerror("Erro ao salvar projeto", str(e))

    def carregar_projeto(self):
        try:
            caminho = filedialog.askopenfilename(
                title="Carregar projeto",
                filetypes=[("Projeto SCALE-BR", "*.json")],
            )
            if not caminho:
                return
            with open(caminho, "r", encoding="utf-8") as f:
                projeto = json.load(f)

            self.matriz = MatrizLCI(projeto["caminho_arquivo"])
            self.matriz.carregar()
            self.caminho_arquivo = projeto["caminho_arquivo"]
            self.lbl_arquivo.configure(
                text=self.caminho_arquivo, text_color="black"
            )
            self._exibir_resumo(self.matriz.obter_resumo())
            self._atualizar_campos_transformadores()
            self._revelar_transformadores()

            for processo, valor in projeto["transformadores"].items():
                if processo in self.campos_transformadores:
                    self.campos_transformadores[processo].insert(0, f"{float(valor):.2e}")

            if projeto["resultados"]:
                self.solver = SolverEmergia(
                    self.matriz.obter_matriz(),
                    projeto["transformadores"]
                )
                self.solver.resultados = projeto["resultados"]
                self._exibir_resultado(self.solver.exibir_resultados())
                self._revelar_secoes_resultado()
                self._atualizar_grafico()

            messagebox.showinfo("Sucesso", "Projeto carregado com sucesso!")

        except FileNotFoundError:
            messagebox.showerror(
                "Erro",
                "Arquivo LCI original não encontrado no caminho salvo.",
            )
        except Exception as e:
            messagebox.showerror("Erro ao carregar projeto", str(e))

    def iniciar(self):
        self.janela.mainloop()
