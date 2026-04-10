# Pre-merge and pre-deploy checklist

## Antes da fusão final

- validar base principal (`validate_data`, `build_indexes`, `check_missing_assets`, `check_i18n`, `check_integrity`)
- rodar `check_packaging_hygiene` e confirmar que o estado final do relatório está limpo
- rodar `smoke_check`
- confirmar que a base principal não invadiu escopo dos paralelos
- revisar manualmente os pacotes aprovados da paralela 1 e 2
- comparar arquivo por arquivo antes de qualquer consolidação
- confirmar quais conflitos exigem decisão humana

## Antes de pensar em deploy

- garantir que a fusão final já foi aprovada
- revisar Home, Entenda a Campeã, Matchups e Learning manualmente
- validar PT-BR e EN no fluxo principal
- confirmar integridade dos assets críticos
- confirmar que nenhum placeholder estrutural crítico sobrou
- conferir logs básicos e startup da aplicação

## Não automatizar cegamente

- escolha final entre versões concorrentes de arquivos
- aprovação de conteúdo premium
- avaliação qualitativa do learning final
- avaliação qualitativa das matchups finais
- decisão de readiness real para produção
