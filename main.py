from src.gui.janela_principal import JanelaPrincipal
from src.gui.tela_splash import TelaSplash

if __name__ == "__main__":
    app = JanelaPrincipal()
    app.janela.withdraw()

    TelaSplash(
        parent=app.janela,
        ao_fechar=app.janela.deiconify,
        duracao_ms=2500,
    ).exibir()

    app.iniciar()