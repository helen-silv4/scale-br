import sys
from src.gui.janela_principal import JanelaPrincipal
from src.gui.tela_splash import TelaSplash


def main() -> None:
    try:
        app = JanelaPrincipal()
        app.janela.withdraw()

        TelaSplash(
            parent=app.janela,
            ao_fechar=app.janela.deiconify,
            duracao_ms=2500,
        ).exibir()

        app.iniciar()

    except Exception as e:
        import tkinter.messagebox as mb
        mb.showerror(
            "Erro ao iniciar o SCALE-BR",
            f"Ocorreu um erro inesperado ao iniciar a aplicação:\n\n{e}"
        )
        sys.exit(1)

if __name__ == "__main__":
    main()