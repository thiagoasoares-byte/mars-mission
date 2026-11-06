[![pipeline](https://github.com/thiagoasoares-byte/mars-mission/actions/workflows/pipeline.yml/badge.svg)](https://github.com/thiagoasoares-byte/mars-mission/actions/workflows/pipeline.yml)

# Thiago Alves Soares 2502664

# Missão Marte: ECLSS

Suíte de testes automatizados para o módulo de controle e monitoramento do Habitat de Marte (Environmental Control and Life Support System).

## 1. Estrutura

| Caminho | Conteúdo |
|---|---|
| `src/gerenciador_recursos.py` | Regras de estoque, consumo, emergência e racionamento |
| `src/servico_telemetria.py` | Comunicação com a estação na Terra |
| `web/painel.html` | Painel web de consulta e solicitação de oxigênio extra |
| `tests/` | Pytest, mocks, Selenium headless e BDD |
| `.github/workflows/pipeline.yml` | Pipeline de CI no GitHub Actions |

## 2. Executando localmente

Requisitos: Python 3.10+ e Google Chrome instalado (usado pelo Selenium em modo headless).

### 2.1 Clonar o repositório

```bash
git clone https://github.com/thiagoasoares-byte/projeto-missao-marte.git
cd projeto-missao-marte
```

### 2.2 Instalar os requisitos

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2.3 Rodar a suíte

```bash
pytest
```

Com relatório de cobertura:

```bash
pytest --cov=src --cov-report=term-missing
```

Em caso de falha nos testes E2E, a captura de tela é salva em `screenshots/`.
