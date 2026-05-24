# SCALE-BR

**Sistema desktop para cálculo de emergia a partir de Inventários do Ciclo de Vida (LCI).**

O SCALE-BR ajuda a importar matrizes LCI, aplicar regras da álgebra emergética, visualizar os fluxos por processo e gerar relatórios em PDF. A aplicação usa uma interface gráfica em CustomTkinter e foi pensada para deixar o fluxo de análise mais simples, desde a planilha de entrada até a exportação dos resultados.

---

## 🌱 O que o projeto faz

- **Importa matrizes LCI** em CSV ou Excel.
- **Valida automaticamente** colunas obrigatórias e valores da matriz.
- **Calcula emergia** com regras clássicas da álgebra emergética.
- **Permite transformadores customizados** por processo.
- **Mostra gráficos** dos fluxos de emergia com matplotlib.
- **Alterna tema claro/escuro** na interface.
- **Exporta relatórios em PDF** com tabela de resultados.
- **Salva e carrega projetos** em JSON.
- **Preenche valores padrão da literatura** com um clique.

<p align="center">
  <img alt="gif snake-game" src="assets/preview.gif" width="100%">
</p>

---

## ️️🛠️ Requisitos

- Python **3.10 ou superior**
- Windows, macOS ou Linux
- Dependências listadas em [`requirements.txt`](requirements.txt)

---

## 🚀 Instalação

Clone o repositório, crie um ambiente virtual e instale as dependências:

```bash
git clone https://github.com/helen-silv4/scale-br
cd scale-br

python -m venv .venv
```

Ative o ambiente virtual:

```bash
# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

Instale os pacotes:

```bash
pip install -r requirements.txt
```

---

## ▶️ Como executar

```bash
python main.py
```

Ao iniciar, a aplicação exibe uma tela de splash e depois abre a janela principal centralizada.

---

## ✨ Como usar

1. **Importe a matriz LCI**
   Clique em **Selecionar arquivo (CSV/Excel)** e escolha sua planilha. Você pode usar [`docs/matriz_lci_exemplo.csv`](docs/matriz_lci_exemplo.csv) como modelo.

2. **Defina os transformadores**
   Preencha os valores em `sej/J` para cada processo ou use a opção **Usar valores padrão da literatura**.

3. **Execute o cálculo**
   Clique em **Executar cálculo de emergia** para gerar a tabela de resultados e o gráfico.

4. **Exporte ou salve**
   Gere um relatório em PDF ou salve o projeto em JSON para continuar depois.

5. **Limpe o projeto**
   Reinicie a interface sem fechar a aplicação.

---

## 📋 Formato da matriz LCI

A matriz deve conter, no mínimo, as colunas abaixo:

| Coluna | Descrição |
| --- | --- |
| `processo` | Nome do processo analisado |
| `energia_solar_sej` | Emergia solar em `sej` |
| `energia_quimica_sej` | Emergia química em `sej` |
| `biomassa_sej` | Emergia da biomassa em `sej` |
| `produto` | Identificador do produto gerado |

Exemplo:

```csv
processo,energia_solar_sej,energia_quimica_sej,biomassa_sej,produto
Agricultura,1.50e+15,2.30e+14,8.70e+14,graos
Transporte,3.20e+14,9.10e+13,0,combustivel
Industria,6.80e+15,1.40e+15,2.10e+14,manufaturado
Tratamento,2.90e+14,4.50e+13,1.20e+14,agua_tratada
```

Arquivo de referência: [`docs/matriz_lci_exemplo.csv`](docs/matriz_lci_exemplo.csv).

---

## 🏗️ Estrutura do projeto

```text
scale-br/
├── main.py                         # Ponto de entrada da aplicação
├── assets/
│   ├── scale_br.ico                # Ícone da aplicação
│   └── gerar_icone.py              # Script para regenerar o ícone
├── docs/
│   └── matriz_lci_exemplo.csv      # Matriz LCI de exemplo
├── src/
│   ├── dados/
│   │   └── matriz_lci.py           # Leitura e validação da matriz LCI
│   ├── gui/
│   │   ├── comandos.py             # Ações da interface
│   │   ├── janela_principal.py     # Janela principal
│   │   └── tela_splash.py          # Tela de splash
│   ├── relatorios/
│   │   └── gerador_relatorio.py    # Geração de PDF
│   └── solver/
│       ├── estrategias_emergia.py  # Regras emergéticas
│       └── solver_emergia.py       # Orquestração do cálculo
└── testes/                         # Testes automatizados com pytest
```

---

## 🧩 Padrões de projeto

| Padrão | Onde aparece | Finalidade |
| --- | --- | --- |
| **Singleton** | `JanelaPrincipal`, `TelaSplash` | Mantém uma única instância das janelas principais |
| **Strategy** | `EstrategiaEmergia` e subclasses | Permite trocar regras de cálculo sem alterar o solver |
| **Command** | `Comando`, `ComandoLimparProjeto` | Encapsula ações da interface e reduz acoplamento |

---

## 🧪 Testes

O conjunto de testes cobre validação de dados, regras de cálculo, geração de relatório, integração e desempenho.

```bash
# Executar todos os testes
pytest

# Executar com relatório de cobertura
pytest --cov=src --cov-report=term-missing
```

Arquivos principais:

- `test_matriz_lci.py`: validação da matriz LCI.
- `test_solver_emergia.py`: regras emergéticas e cálculo.
- `test_gerador_relatorio.py`: geração de PDF.
- `test_integracao.py`: fluxo completo LCI → Solver → Relatório.
- `test_desempenho.py`: desempenho com até 100 processos em até 5 segundos.

---

## 🛠️ Tecnologias

- **CustomTkinter**: interface gráfica moderna sobre Tk.
- **pandas**: leitura e manipulação da matriz LCI.
- **matplotlib**: visualização dos fluxos de emergia.
- **fpdf2**: geração de relatórios em PDF.
- **Pillow**: manipulação do ícone da aplicação.
- **pytest**: testes automatizados.

---

## 📌 Observações

- O arquivo [`docs/matriz_lci_exemplo.csv`](docs/matriz_lci_exemplo.csv) pode ser usado como base para novas análises.
- O relatório em PDF é gerado a partir dos resultados calculados na interface.
- Projetos salvos em JSON preservam arquivo LCI, transformadores e resultados.


