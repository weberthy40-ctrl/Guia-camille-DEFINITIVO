# Camille Guide Base — Principal Line

Base estrutural da **linha principal** do projeto Camille. Esta linha é responsável por sistema, integração, páginas principais, learning em nível de sistema, i18n, pipeline, integridade e preparação para a fusão final.

## Escopo da linha principal

A linha principal deve focar em:
- estrutura geral do projeto
- integração segura
- Home
- Entenda a Campeã
- Learning em nível de sistema
- PT-BR / EN
- pipeline / validação / integridade
- readiness para fusão final
- readiness de deploy no momento certo

A linha principal **não deve**:
- refinar matchup por matchup
- competir com a linha paralela 1 de matchups
- competir com a linha paralela 2 de conteúdo premium da Camille
- fazer merge manual antes da etapa final

## Estrutura principal

```text
project_root/
  app.py
  requirements.txt
  render.yaml
  README.md
  data/
    champions/
    matchups/
    learning/
    meta/
  translations/
  templates/
  static/
  pipeline/
  scripts/
  utils/
```

## Linhas de trabalho

- **Principal**: sistema, integração, Home, Entenda a Campeã, Learning estrutural, i18n, pipeline, integridade, readiness.
- **Paralelo 1**: matchups.
- **Paralelo 2**: conteúdo premium da Camille fora das matchups.
- **Controle**: validação dos pacotes e estratégia de fusão final.

## Rodar localmente

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
python scripts/validate_data.py
python scripts/build_indexes.py
python scripts/check_missing_assets.py
python scripts/check_i18n.py
python scripts/check_display_i18n.py
python scripts/check_integrity.py
python scripts/check_packaging_hygiene.py
python scripts/smoke_check.py
python app.py
```

## Rotas

- `/` home
- `/guide` Entenda a Campeã
- `/matchups` visão geral dos matchups
- `/matchups/<role>/<champion_slug>` detalhe do matchup
- `/learning` central de aprendizado

## Internacionalização

A base usa arquivos em `translations/` e fallback seguro para `pt-BR`.

- idioma atual via query string: `?lang=pt-BR` ou `?lang=en`
- fallback automático para `pt-BR`
- aliases simples aceitos: `pt`, `pt-br`, `en-us`, `en-gb`
- chaves ficam centralizadas nos JSONs de tradução

## Dados e manutenção

### Matchups na linha principal

A rota de matchups continua existindo e depende dos índices/meta do projeto, mas o **refino de conteúdo matchup por matchup pertence à linha paralela 1**.

A linha principal só deve:
- manter a navegação funcionando
- manter índices/meta íntegros
- manter compatibilidade estrutural
- preparar a base para a fusão final

### Como atualizar score/índices com segurança

A regra central está em `utils/scoring.py`.

Passos:
1. validar dados
2. rebuildar índices
3. checar assets
4. rodar integrity/smoke

```bash
python scripts/validate_data.py
python scripts/build_indexes.py
python scripts/check_missing_assets.py
python scripts/check_integrity.py
python scripts/smoke_check.py
```

## Pipeline disponível

### 1. Validar dados

```bash
python scripts/validate_data.py
```

Valida:
- JSON malformado
- champion core / learning / meta
- schema base de matchup
- consistência básica de score e dificuldade
- consistência entre pasta e `role_bucket`
- chaves essenciais de tradução

### 2. Reindexar matchups e meta estrutural

```bash
python scripts/build_indexes.py
```

Atualiza:
- `data/meta/matchups_overview.json`
- `data/meta/roles_index.json`
- `data/meta/learning_bundle_status.json`
- `data/meta/expected_files_manifest.json`

### 3. Checar assets ausentes

```bash
python scripts/check_missing_assets.py
```

Gera:
- `data/meta/assets_report.json`

### 4. Checar i18n

```bash
python scripts/check_i18n.py
python scripts/check_display_i18n.py
```

Gera:
- `data/meta/i18n_report.json`

### 5. Checar integridade de bundle e readiness

```bash
python scripts/check_integrity.py
```

Gera:
- `data/meta/learning_integrity_report.json`
- `data/meta/merge_readiness_report.json`

### 6. Checar hygiene de empacotamento

```bash
python scripts/check_packaging_hygiene.py
```

Gera:
- `data/meta/packaging_hygiene_report.json`

### 7. Smoke check sistêmico leve

```bash
python scripts/smoke_check.py
```

Gera:
- `data/meta/smoke_check_report.json`


## Hygiene de empacotamento

- não incluir `__pycache__/`, `*.pyc`, `*.pyo` e caches temporários no zip
- rodar `python scripts/check_packaging_hygiene.py` antes de empacotar
- se `py_compile` ou execuções locais gerarem bytecode, limpe a árvore antes de criar o zip final

## Pré-fusão e pré-deploy

Antes de qualquer fusão final ou preparação real de deploy, consulte:
- `pipeline/merge_readiness.md`
- `pipeline/premerge_predeploy_checklist.md`
- `pipeline/packaging_hygiene.md`

## Deploy no Render

O projeto está preparado para Render, mas o deploy final só deve acontecer depois da revisão humana dos pacotes aprovados e da consolidação final.

## Regra de ouro

Não fazer merge manual no meio do caminho.
Guardar os zips separados.
Só consolidar no final, após revisão completa dos pacotes aprovados.
