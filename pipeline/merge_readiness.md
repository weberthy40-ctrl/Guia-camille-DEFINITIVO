# Merge readiness and principal-line integrity

A linha principal prepara o projeto para a futura consolidação dos pacotes aprovados, sem executar merge agora.

## Estratégia oficial

- **Base principal**: sistema, integração, Home, Entenda a Campeã, Learning estrutural, i18n, pipeline, integridade e readiness.
- **Paralelo 1**: matchups.
- **Paralelo 2**: conteúdo premium da Camille fora das matchups.
- **Controle**: validação dos pacotes e decisão final de fusão.

## O que esta etapa faz

- fortalece validação e integridade
- confirma fallback seguro do bundle de learning
- melhora a hygiene de empacotamento
- adiciona smoke check sistêmico leve
- gera relatórios úteis para pré-fusão e pré-deploy

## O que esta etapa não faz

- não refina matchups
- não produz conteúdo premium novo
- não faz merge manual
- não substitui revisão humana final

## Comandos recomendados

```bash
python scripts/validate_data.py
python scripts/build_indexes.py
python scripts/check_missing_assets.py
python scripts/check_i18n.py
python scripts/check_integrity.py
python scripts/check_packaging_hygiene.py
python scripts/smoke_check.py
```

## Relatórios-chave

- `data/meta/learning_bundle_status.json`
- `data/meta/learning_integrity_report.json`
- `data/meta/expected_files_manifest.json`
- `data/meta/merge_readiness_report.json`
- `data/meta/packaging_hygiene_report.json`
- `data/meta/smoke_check_report.json`

## Regras finais

- não sobrescrever a base oficial por conta própria
- não assumir que checks automatizados substituem revisão humana
- comparar arquivo por arquivo na fusão final
- preservar o melhor de cada linha aprovada


## Consistência de relatórios

- `packaging_hygiene_report.json` é a fonte de verdade da hygiene de empacotamento desta rodada
- `merge_readiness_report.json` replica esse estado para evitar drift entre relatórios
- se a hygiene remover ruído técnico durante a checagem, o readiness já reflete o estado final saneado
