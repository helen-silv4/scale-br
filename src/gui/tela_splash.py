import os
import customtkinter as ctk

CAMINHO_ICONE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "scale_br.ico"
)


class TelaSplash:
    """
    Padrão GoF: Singleton — garante uma única instância da tela de splash
    durante a inicialização. Apresenta logo, nome do sistema e indicador
    de progresso enquanto a janela principal é carregada em segundo plano.
    """

    _instancia = None

    def __new__(cls, *args, **kwargs):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self, parent, ao_fechar, duracao_ms: int = 2500):
        if getattr(self, "_inicializado", False):
            return
        self._inicializado = True

        self.parent = parent
        self.ao_fechar = ao_fechar
        self.duracao_ms = duracao_ms

        self.janela = ctk.CTkToplevel(parent)
        self.janela.title("SCALE-BR")
        self.janela.overrideredirect(True)
        self.janela.attributes("-topmost", True)
        # CTkToplevel define seu ícone padrão via after_idle (~200ms);
        # aplicamos o nosso depois para que apareça na barra de tarefas
        # e em Alt+Tab.
        self.janela.after(300, self._aplicar_icone)

        largura, altura = 540, 340
        x = (self.janela.winfo_screenwidth() - largura) // 2
        y = (self.janela.winfo_screenheight() - altura) // 2
        self.janela.geometry(f"{largura}x{altura}+{x}+{y}")

        self._construir()

    def _construir(self):
        moldura = ctk.CTkFrame(
            self.janela, corner_radius=12, fg_color="#1f6aa5", border_width=2,
            border_color="#145280",
        )
        moldura.pack(fill="both", expand=True, padx=2, pady=2)

        ctk.CTkLabel(
            moldura,
            text="🌱",
            font=ctk.CTkFont(size=78),
            text_color="white",
        ).pack(pady=(40, 6))

        ctk.CTkLabel(
            moldura,
            text="SCALE-BR",
            font=ctk.CTkFont(size=38, weight="bold"),
            text_color="white",
        ).pack()

        ctk.CTkLabel(
            moldura,
            text="Sistema para Cálculo de Emergia",
            font=ctk.CTkFont(size=15),
            text_color="#d8e8f5",
        ).pack(pady=(4, 0))

        ctk.CTkLabel(
            moldura,
            text="baseado em Inventários do Ciclo de Vida",
            font=ctk.CTkFont(size=13),
            text_color="#b8d2e8",
        ).pack(pady=(0, 0))

        self.barra = ctk.CTkProgressBar(
            moldura,
            mode="indeterminate",
            width=380,
            height=10,
            progress_color="white",
            fg_color="#145280",
        )
        self.barra.pack(pady=(28, 4))
        self.barra.start()

        ctk.CTkLabel(
            moldura,
            text="Carregando...",
            font=ctk.CTkFont(size=13),
            text_color="#d8e8f5",
        ).pack(pady=(2, 0))

    def _aplicar_icone(self):
        try:
            self.janela.iconbitmap(CAMINHO_ICONE)
        except Exception:
            pass

    def exibir(self):
        """Agenda o fechamento automático e devolve o controle ao mainloop."""
        self.janela.after(self.duracao_ms, self._fechar)

    def _fechar(self):
        try:
            self.barra.stop()
        except Exception:
            pass
        self.janela.destroy()
        self.ao_fechar()
