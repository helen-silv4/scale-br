import json
import customtkinter as ctk
from tkinter import filedialog, messagebox

from src.dados.matriz_lci import MatrizLCI
from src.solver.solver_emergia import SolverEmergia
from src.relatorios.gerador_relatorio import GeradorRelatorio

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class JanelaPrincipal:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("SCALE-BR — Sistema para Cálculo de Emergia")
        self.janela.geometry("1000x780")
        self.janela.resizable(True, True)

        self.caminho_arquivo = None
        self.matriz = None
        self.solver = None
        self.relatorio = None
        self.campos_transformadores = {}

        self._construir_interface()

    def _construir_interface(self):
        ctk.CTkLabel(
            self.janela,
            text="SCALE-BR — Sistema para Cálculo de Emergia",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            self.janela,
            text="Sistema para Cálculo de Emergia baseado em Inventários do Ciclo de Vida",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(pady=(0, 15))

        frame_principal = ctk.CTkScrollableFrame(self.janela, corner_radius=0)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self._construir_area_importacao(frame_principal)
        self._construir_area_transformadores(frame_principal)
        self._construir_area_resultados(frame_principal)
        self._construir_area_exportacao(frame_principal)

    def _construir_area_importacao(self, pai):
        frame = ctk.CTkFrame(pai, corner_radius=10)
        frame.pack(fill="x", pady=8)

        ctk.CTkLabel(
            frame,
            text="1. Importação de Matriz LCI",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=15, pady=(12, 5))

        frame_arquivo = ctk.CTkFrame(frame, fg_color="transparent")
        frame_arquivo.pack(fill="x", padx=15, pady=5)

        self.lbl_arquivo = ctk.CTkLabel(
            frame_arquivo,
            text="Nenhum arquivo selecionado",
            text_color="gray",
            font=ctk.CTkFont(size=11)
        )
        self.lbl_arquivo.pack(side="left", expand=True, fill="x")

        ctk.CTkButton(
            frame_arquivo,
            text="Selecionar arquivo (CSV/Excel)",
            command=self.importar_lci,
            width=220
        ).pack(side="right")

        self.txt_resumo = ctk.CTkTextbox(
            frame, height=70,
            font=ctk.CTkFont(size=11, family="Courier")
        )
        self.txt_resumo.pack(fill="x", padx=15, pady=(5, 15))
        self.txt_resumo.configure(state="disabled")

    def _construir_area_transformadores(self, pai):
        self.frame_transformadores = ctk.CTkFrame(pai, corner_radius=10)
        self.frame_transformadores.pack(fill="x", pady=8)

        ctk.CTkLabel(
            self.frame_transformadores,
            text="2. Transformadores Emergéticos (sej/J)",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=15, pady=(12, 5))

        # Texto explicativo
        ctk.CTkLabel(
            self.frame_transformadores,
            text="O transformador emergético indica a quantidade de emergia solar (sej) necessária\n"
                 "para gerar uma unidade de energia de cada processo. Valores da literatura científica.\n"
                 "Se deixado em branco, o sistema usa o valor padrão de 1.0 (sem amplificação).",
            text_color="gray",
            font=ctk.CTkFont(size=11),
            justify="left"
        ).pack(anchor="w", padx=15, pady=(0, 8))

        # Botão valores padrão
        ctk.CTkButton(
            self.frame_transformadores,
            text="📋  Usar valores padrão da literatura",
            command=self._preencher_valores_padrao,
            width=260,
            fg_color="gray40",
            hover_color="gray30",
            font=ctk.CTkFont(size=11)
        ).pack(anchor="w", padx=15, pady=(0, 10))

        self.frame_campos_transf = ctk.CTkFrame(
            self.frame_transformadores,
            fg_color="transparent"
        )
        self.frame_campos_transf.pack(fill="x", padx=15, pady=(0, 10))

        ctk.CTkButton(
            self.frame_transformadores,
            text="▶  Executar cálculo de emergia",
            command=self.executar_calculo,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=40,
            corner_radius=8
        ).pack(pady=(0, 15), padx=15, fill="x")

        self.frame_transformadores.configure(height=0)
        self.secao_transf_visivel = False

    def _preencher_valores_padrao(self):
        """Preenche os transformadores com valores padrão da literatura."""
        if not self.campos_transformadores:
            messagebox.showwarning(
                "Atenção", "Carregue um arquivo LCI antes de usar valores padrão."
            )
            return

        # Valores de referência da literatura emergética (Odum, 1996)
        valores_padrao = {
            "agricultura": 1.5e+15,
            "transporte": 3.2e+14,
            "industria": 6.8e+15,
            "tratamento": 2.9e+14,
            "energia": 1.7e+05,
            "biomassa": 3.6e+04,
            "combustivel": 5.4e+04,
            "agua": 4.8e+04,
        }

        preenchidos = 0
        for processo, entrada in self.campos_transformadores.items():
            chave = processo.lower()
            # Busca correspondência parcial no nome do processo
            valor = None
            for padrao, val in valores_padrao.items():
                if padrao in chave or chave in padrao:
                    valor = val
                    break

            if valor:
                entrada.delete(0, "end")
                entrada.insert(0, f"{valor:.2e}")
                preenchidos += 1

        if preenchidos == 0:
            messagebox.showinfo(
                "Valores padrão",
                "Nenhum processo correspondeu aos valores padrão da literatura.\n"
                "Preencha os transformadores manualmente."
            )
        else:
            messagebox.showinfo(
                "Valores padrão",
                f"{preenchidos} transformador(es) preenchido(s) com valores da literatura.\n"
                "Você pode editar os valores antes de executar o cálculo."
            )

    def _atualizar_campos_transformadores(self):
        """Cria dinamicamente um campo por processo carregado."""
        for widget in self.frame_campos_transf.winfo_children():
            widget.destroy()
        self.campos_transformadores = {}

        for processo in self.matriz.lista_processos:
            linha = ctk.CTkFrame(self.frame_campos_transf, fg_color="transparent")
            linha.pack(fill="x", pady=3)

            ctk.CTkLabel(
                linha,
                text=f"{processo}:",
                width=160,
                anchor="w",
                font=ctk.CTkFont(size=11)
            ).pack(side="left", padx=(0, 8))

            entrada = ctk.CTkEntry(
                linha,
                width=200,
                placeholder_text="ex: 1.5e+15 (opcional)"
            )
            entrada.pack(side="left")

            ctk.CTkLabel(
                linha,
                text="sej/J",
                text_color="gray",
                font=ctk.CTkFont(size=10)
            ).pack(side="left", padx=(6, 0))

            self.campos_transformadores[processo] = entrada

    def _construir_area_resultados(self, pai):
        frame = ctk.CTkFrame(pai, corner_radius=10)
        frame.pack(fill="both", expand=True, pady=8)

        ctk.CTkLabel(
            frame,
            text="3. Resultados",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=15, pady=(12, 5))

        self.txt_resultados = ctk.CTkTextbox(
            frame, height=180,
            font=ctk.CTkFont(size=11, family="Courier")
        )
        self.txt_resultados.pack(
            fill="both", expand=True, padx=15, pady=(0, 15)
        )
        self.txt_resultados.configure(state="disabled")

    def _construir_area_exportacao(self, pai):
        frame = ctk.CTkFrame(pai, corner_radius=10)
        frame.pack(fill="x", pady=8)

        ctk.CTkLabel(
            frame,
            text="4. Exportação e Projeto",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=15, pady=(12, 8))

        frame_botoes = ctk.CTkFrame(frame, fg_color="transparent")
        frame_botoes.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkButton(
            frame_botoes,
            text="📄  Gerar relatório PDF",
            command=self.exportar_relatorio,
            width=190
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            frame_botoes,
            text="💾  Salvar projeto",
            command=self.salvar_projeto,
            width=150,
            fg_color="gray40",
            hover_color="gray30"
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            frame_botoes,
            text="📂  Carregar projeto",
            command=self.carregar_projeto,
            width=160,
            fg_color="gray40",
            hover_color="gray30"
        ).pack(side="left")

    # ── Métodos de ação ──────────────────────────────────────────────

    def importar_lci(self):
        caminho = filedialog.askopenfilename(
            title="Selecionar arquivo LCI",
            filetypes=[("Arquivos compatíveis", "*.csv *.xlsx *.xls"),
                       ("CSV", "*.csv"),
                       ("Excel", "*.xlsx *.xls")]
        )
        if caminho:
            try:
                self.matriz = MatrizLCI(caminho)
                self.matriz.carregar()
                self.caminho_arquivo = caminho
                self.lbl_arquivo.configure(text=caminho, text_color="black")
                self._exibir_resumo(self.matriz.obter_resumo())
                self._atualizar_campos_transformadores()
                if not self.secao_transf_visivel:
                    self.frame_transformadores.configure(height=-1)
                    self.secao_transf_visivel = True
            except Exception as e:
                messagebox.showerror("Erro ao carregar arquivo", str(e))

    def executar_calculo(self):
        if not self.matriz:
            messagebox.showwarning(
                "Atenção", "Selecione um arquivo LCI antes de calcular."
            )
            return
        try:
            transformadores = {}
            for processo, entrada in self.campos_transformadores.items():
                valor = entrada.get().strip()
                if valor:
                    transformadores[processo] = float(valor)

            self.solver = SolverEmergia(
                self.matriz.obter_matriz(), transformadores
            )
            self.solver.calcular()
            self._exibir_resultado(self.solver.exibir_resultados())

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
                initialfile="relatorio_scale_br.pdf"
            )
            if caminho:
                self.relatorio = GeradorRelatorio(
                    self.solver.resultados, caminho
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
                initialfile="projeto_scale_br.json"
            )
            if caminho:
                transformadores = {}
                for processo, entrada in self.campos_transformadores.items():
                    valor = entrada.get().strip()
                    if valor:
                        transformadores[processo] = float(valor)

                projeto = {
                    "caminho_arquivo": self.caminho_arquivo,
                    "transformadores": transformadores,
                    "resultados": self.solver.resultados if self.solver else {}
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
                filetypes=[("Projeto SCALE-BR", "*.json")]
            )
            if caminho:
                with open(caminho, "r", encoding="utf-8") as f:
                    projeto = json.load(f)

                # Recarrega o arquivo LCI
                self.matriz = MatrizLCI(projeto["caminho_arquivo"])
                self.matriz.carregar()
                self.caminho_arquivo = projeto["caminho_arquivo"]
                self.lbl_arquivo.configure(
                    text=self.caminho_arquivo, text_color="black"
                )
                self._exibir_resumo(self.matriz.obter_resumo())
                self._atualizar_campos_transformadores()

                # Restaura os transformadores
                for processo, valor in projeto["transformadores"].items():
                    if processo in self.campos_transformadores:
                        self.campos_transformadores[processo].insert(
                            0, str(valor)
                        )

                # Restaura os resultados se existirem
                if projeto["resultados"]:
                    self.solver = SolverEmergia(
                        self.matriz.obter_matriz(),
                        projeto["transformadores"]
                    )
                    self.solver.resultados = projeto["resultados"]
                    self._exibir_resultado(self.solver.exibir_resultados())

                messagebox.showinfo("Sucesso", "Projeto carregado com sucesso!")

        except FileNotFoundError:
            messagebox.showerror(
                "Erro",
                "Arquivo LCI original não encontrado no caminho salvo."
            )
        except Exception as e:
            messagebox.showerror("Erro ao carregar projeto", str(e))

    def _exibir_resumo(self, texto):
        self.txt_resumo.configure(state="normal")
        self.txt_resumo.delete("1.0", "end")
        self.txt_resumo.insert("end", texto)
        self.txt_resumo.configure(state="disabled")

    def _exibir_resultado(self, texto):
        self.txt_resultados.configure(state="normal")
        self.txt_resultados.delete("1.0", "end")
        self.txt_resultados.insert("end", texto)
        self.txt_resultados.configure(state="disabled")

    def iniciar(self):
        self.janela.mainloop()