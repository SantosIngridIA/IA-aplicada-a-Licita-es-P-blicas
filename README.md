# IA aplicada a Licitações Públicas

Projeto em desenvolvimento para facilitar a leitura, organização e pesquisa de editais públicos com apoio de programação e, em etapas futuras, inteligência artificial.

## Problema que queremos resolver

Editais podem ser longos e difíceis de comparar. A proposta é transformar documentos públicos em informações mais fáceis de localizar, sempre permitindo conferir o resultado no texto original.

## MVP

A primeira versão cria uma base pesquisável a partir de PDFs:

- lê arquivos PDF de uma pasta;
- extrai o texto disponível;
- registra nome do arquivo, número de páginas, quantidade de caracteres e texto extraído;
- exporta os resultados para CSV, que pode ser aberto no Excel.

Esta etapa **não interpreta juridicamente o edital**, não decide se uma empresa está apta e não substitui a conferência humana. PDFs digitalizados como imagem podem exigir OCR, que será avaliado em uma etapa posterior.

## Requisitos

- Python 3.10 ou superior
- PDFs de editais salvos localmente para processamento

## Instalação (Windows / PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

## Como usar

Coloque PDFs em `data/raw/` e execute:

```powershell
licita-ai index data/raw --output data/processed/editais.csv
```

Também é possível apontar para outra pasta:

```powershell
licita-ai index "C:\caminho\para\editais" --output resultado.csv
```

O CSV é salvo em UTF-8 com BOM e separador ponto e vírgula para facilitar a abertura no Excel em português. A coluna `texto` contém o texto extraído; você pode usar a busca do Excel para localizar termos.

## Estrutura do projeto

```
.
├── data/
│   ├── raw/                 # PDFs locais; não são enviados ao Git
│   └── processed/           # CSVs gerados; não são enviados ao Git
├── docs/
│   └── roadmap.md
├── src/
│   └── licita_ai/
│       ├── __init__.py
│       └── cli.py
├── .gitignore
├── pyproject.toml
└── README.md
```

## Próximas etapas

Veja o [roadmap](docs/roadmap.md). A evolução será feita em pequenos passos, começando pela qualidade da extração antes de adicionar filtros, resumo ou recursos de IA.

## Cuidados com os dados

Use documentos públicos e respeite os termos das fontes consultadas. Os PDFs e CSVs processados ficam fora do Git por padrão. Confira qualquer informação extraída diretamente no edital original.
