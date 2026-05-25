<h1 align="center">SCALE-BR</h1>

**Sistema desktop para cálculo de emergia a partir de Inventários do Ciclo de Vida (LCI).**

O SCALE-BR permite importar matrizes LCI, aplicar as regras da álgebra emergética, visualizar os fluxos de emergia por processo e exportar relatórios em PDF com gráfico embutido. A interface gráfica foi desenvolvida em CustomTkinter e oferece alternância entre tema claro e escuro.

## 🌱 O que o projeto faz

- **Importa matrizes LCI** em CSV ou Excel com validação automática.
- **Calcula emergia** aplicando as três regras da álgebra emergética: co-produtos, feedback e caminhos múltiplos.
- **Campos dinâmicos** de transformadores emergéticos (um campo por processo carregado).
- **Preenche valores padrão da literatura** com um clique (Odum, 1996).
- **Visualiza gráficos** de fluxos de emergia por processo com matplotlib.
- **Exporta relatórios em PDF** com tabela de resultados e gráfico embutido.
- **Salva e carrega projetos** em JSON preservando arquivo LCI, transformadores e resultados.
- **Alterna tema claro/escuro** na interface.
- **Limpa o projeto** sem fechar a aplicação.

<p align="center">
  <img alt="Interface do SCALE-BR em execução" src="assets/preview.gif" width="100%">
</p>

<br>

## 🛠️ Requisitos

- Python **3.10 ou superior**
- Windows, macOS ou Linux
- Dependências listadas em [`requirements.txt`](requirements.txt)

<br>

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

<br>

## 🎯 Como executar

```bash
python main.py
```

Ao iniciar, a aplicação exibe uma tela de splash e abre a janela principal centralizada na tela.

<br>

## ✨ Como usar

1. **Importe a matriz LCI** \
   Clique em **Selecionar arquivo (CSV/Excel)** e escolha sua planilha. Use [`docs/matriz_lci_exemplo.csv`](docs/matriz_lci_exemplo.csv) como modelo.

2. **Defina os transformadores** \
   Os campos aparecem dinamicamente, um por processo. Preencha manualmente ou clique em **Usar valores padrão da literatura**.

3. **Execute o cálculo** \
   Clique em **Executar cálculo de emergia** para gerar a tabela de resultados e o gráfico de fluxos.

4. **Exporte o relatório** \
   Clique em **Gerar relatório PDF** para exportar um PDF com a tabela de resultados e o gráfico embutido.

5. **Salve ou carregue o projeto** \
   Salve o estado atual em JSON e retome depois com **Carregar projeto**.

6. **Limpe o projeto** \
   Clique em **✕ Limpar** para reiniciar a interface sem fechar a aplicação.

<br>

## 📋 Formato da matriz LCI

A matriz deve conter, no mínimo, as colunas abaixo:

| Coluna | Descrição |
|---|---|
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

Arquivo de referência: [`docs/matriz_lci_exemplo.csv`](docs/matriz_lci_exemplo.csv) (4 processos) e [`docs/matriz_lci_completa.csv`](docs/matriz_lci_completa.csv) (10 processos).

<br>

## 🏗️ Estrutura do projeto

```text
scale-br/
├── main.py                          # Ponto de entrada da aplicação
├── pytest.ini                       # Configuração do pytest e cobertura
├── .coveragerc                      # Exclusão da GUI da cobertura de testes
├── assets/
│   ├── preview.gif                  # GIF de demonstração da interface
│   └── scale_br.ico                 # Ícone da aplicação
├── docs/
│   ├── matriz_lci_exemplo.csv       # Matriz LCI com 4 processos
│   └── matriz_lci_completa.csv      # Matriz LCI com 10 processos
├── src/
│   ├── dados/
│   │   └── matriz_lci.py            # Leitura e validação da matriz LCI
│   ├── gui/
│   │   ├── comandos.py              # Padrão Command para ações da interface
│   │   ├── janela_principal.py      # Janela principal da aplicação
│   │   └── tela_splash.py           # Tela de abertura
│   ├── relatorios/
│   │   └── gerador_relatorio.py     # Geração de PDF com gráfico embutido
│   └── solver/
│       ├── estrategias_emergia.py   # Padrão Strategy com regras emergéticas
│       └── solver_emergia.py        # Orquestração do cálculo de emergia
└── testes/
    ├── conftest.py                  # Fixtures compartilhadas entre testes
    ├── test_matriz_lci.py           # Testes de carregamento e validação
    ├── test_solver_emergia.py       # Testes das regras emergéticas
    ├── test_gerador_relatorio.py    # Testes de geração de PDF
    ├── test_integracao.py           # Fluxo completo LCI → Solver → Relatório
    └── test_desempenho.py           # Desempenho com até 100 processos
```

<br>

## 🧩 Padrões de projeto

| Padrão | Onde aparece | Finalidade |
|---|---|---|
| **Singleton** | `JanelaPrincipal`, `TelaSplash` | Garante uma única instância das janelas durante toda a execução |
| **Strategy** | `EstrategiaEmergia` e subclasses | Permite substituir regras de cálculo sem alterar o solver |
| **Command** | `Comando`, `ComandoLimparProjeto` | Encapsula ações da interface e reduz acoplamento com a janela |

<br>

## 🧪 Testes

O conjunto de testes cobre validação de dados, regras de cálculo, geração de PDF com e sem gráfico, integração ponta a ponta e desempenho. A cobertura atual é de **90%**.

```bash
# Executar todos os testes
pytest

# Executar com relatório de cobertura detalhado
pytest --cov=src --cov-report=term-missing
```

| Arquivo | O que cobre |
|---|---|
| `conftest.py` | Fixtures compartilhadas entre todos os testes |
| `test_matriz_lci.py` | Carregamento, validação, valores negativos e matriz vazia |
| `test_solver_emergia.py` | Regras emergéticas, transformadores e estratégias injetadas |
| `test_gerador_relatorio.py` | PDF com e sem gráfico matplotlib embutido |
| `test_integracao.py` | Fluxo completo: importar → calcular → exportar → salvar → carregar |
| `test_desempenho.py` | Até 100 processos dentro dos limites de tempo do RNF01 |

<br>

## 🛠️ Tecnologias

| Biblioteca | Uso |
|---|---|
| **CustomTkinter** | Interface gráfica moderna com suporte a tema claro/escuro |
| **pandas** | Leitura e validação da matriz LCI em CSV e Excel |
| **matplotlib** | Geração de gráficos de fluxo de emergia |
| **fpdf2** | Geração de relatórios técnicos em PDF |
| **Pillow** | Suporte a ícone e manipulação de imagens |
| **pytest + pytest-cov** | Testes automatizados com relatório de cobertura |

<br>

## 📌 Observações

- Os arquivos em `docs/` servem como base para novas análises e podem ser editados livremente.
- O relatório PDF inclui automaticamente o gráfico de fluxos exibido na interface. Se o cálculo ainda não foi executado, um gráfico padrão é gerado.
- Projetos salvos em JSON preservam o caminho do arquivo LCI, os transformadores configurados e os resultados calculados.
- A GUI não é contabilizada na cobertura de testes pois depende de interação humana; os demais módulos atingem 90% de cobertura.