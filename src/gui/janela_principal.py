import customtkinter as ctk
from tkinter import filedialog, messagebox
from src.dados.matriz_lci import MatrizLCI


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
        self.solver = None
        self.relatorio = None

        self._construir_interface()

    def _construir_interface(self):
        # Título principal
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

        # Frame principal com scroll
        frame_principal = ctk.CTkScrollableFrame(self.janela, corner_radius=0)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self._construir_area_importacao(frame_principal)
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

        # Linha do arquivo
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

        # Resumo dos dados carregados
        self.txt_resumo = ctk.CTkTextbox(frame, height=70, font=ctk.CTkFont(size=11, family="Courier"))
        self.txt_resumo.pack(fill="x", padx=15, pady=(5, 10))
        self.txt_resumo.configure(state="disabled")

        # Transformadores
        frame_transf = ctk.CTkFrame(frame, corner_radius=8)
        frame_transf.pack(fill="x", padx=15, pady=(0, 10))

        ctk.CTkLabel(
            frame_transf,
            text="Transformadores emergéticos (sej/J)",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", padx=12, pady=(10, 5))

        frame_entradas = ctk.CTkFrame(frame_transf, fg_color="transparent")
        frame_entradas.pack(fill="x", padx=12, pady=(0, 10))

        ctk.CTkLabel(frame_entradas, text="Processo 1:").pack(side="left", padx=(0, 5))
        self.entrada_transf1 = ctk.CTkEntry(frame_entradas, width=130, placeholder_text="ex: 1.5e+05")
        self.entrada_transf1.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(frame_entradas, text="Processo 2:").pack(side="left", padx=(0, 5))
        self.entrada_transf2 = ctk.CTkEntry(frame_entradas, width=130, placeholder_text="ex: 3.2e+04")
        self.entrada_transf2.pack(side="left")

        ctk.CTkButton(
            frame,
            text="▶  Executar cálculo de emergia",
            command=self.executar_calculo,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=40,
            corner_radius=8
        ).pack(pady=(0, 15), padx=15, fill="x")

    def _construir_area_resultados(self, pai):
        frame = ctk.CTkFrame(pai, corner_radius=10)
        frame.pack(fill="both", expand=True, pady=8)

        ctk.CTkLabel(
            frame,
            text="2. Resultados",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=15, pady=(12, 5))

        self.txt_resultados = ctk.CTkTextbox(
            frame,
            height=180,
            font=ctk.CTkFont(size=11, family="Courier")
        )
        self.txt_resultados.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.txt_resultados.configure(state="disabled")

    def _construir_area_exportacao(self, pai):
        frame = ctk.CTkFrame(pai, corner_radius=10)
        frame.pack(fill="x", pady=8)

        ctk.CTkLabel(
            frame,
            text="3. Exportação e Projeto",
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
                self.lbl_arquivo.configure(text=caminho, text_color="white")
                self._exibir_resumo(self.matriz.obter_resumo())
            except Exception as e:
                messagebox.showerror("Erro ao carregar arquivo", str(e))

    def executar_calculo(self):
        if not self.caminho_arquivo:
            messagebox.showwarning("Atenção", "Selecione um arquivo LCI antes de calcular.")
            return
        self._exibir_resultado("Cálculo executado com sucesso!\n(integração com SolverEmergia em desenvolvimento)")

    def exportar_relatorio(self):
        messagebox.showinfo("Exportação", "Geração de relatório em desenvolvimento.")

    def salvar_projeto(self):
        messagebox.showinfo("Salvar", "Funcionalidade em desenvolvimento.")

    def carregar_projeto(self):
        messagebox.showinfo("Carregar", "Funcionalidade em desenvolvimento.")

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