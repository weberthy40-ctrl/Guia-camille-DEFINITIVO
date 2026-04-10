# Data Rules

## Princípios

- Todo matchup é modelado como **Campeão X vs Camille no top**.
- `identity.role_bucket` deve bater com a pasta do arquivo.
- O schema deve ser estável; campos novos devem ser adicionados sem remover os atuais.
- Quando faltar conteúdo especialista, usar placeholders claros e seguros.
- Evitar hardcode de texto de interface fora de `translations/`.

## Convenções

- arquivos: `snake_case.json`
- champion slug: minúsculo e sem espaços
- score: decimal entre 1.0 e 10.0
- difficulty: `suggest_ban`, `hard`, `medium`, `easy`
- localizações de conteúdo textual longo: preferencialmente em objetos localizáveis

## Fluxo de atualização

1. editar JSON
2. validar dados
3. rebuild dos índices
4. checar assets
5. revisar UI
