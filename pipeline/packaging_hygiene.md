# Packaging hygiene

Objetivo: manter os próximos zips limpos, previsíveis e sem ruído técnico.

## Não incluir

- `__pycache__/`
- `*.pyc`
- `*.pyo`
- caches temporários de ferramentas
- artefatos locais acidentais

## Antes de empacotar

1. rode `python scripts/check_packaging_hygiene.py`
2. confirme que o relatório final está limpo
3. se houver ruído removível, a checagem faz a limpeza antes da varredura final
4. gere o zip a partir da árvore já saneada

## Observação

Hygiene de empacotamento melhora revisão, diff entre pacotes e segurança na futura fusão final.

## Observação prática

`py_compile` e imports locais podem gerar bytecode temporário. A checagem de hygiene desta base remove esse ruído antes da varredura final e registra o que foi saneado no relatório.
