# Scoring Rules

## Faixa

- 9.0 a 10.0 = Sugiro Ban
- 7.0 a 8.9 = Difícil
- 4.5 a 6.9 = Médio
- 1.0 a 4.4 = Fácil

## Pesos

- lane phase pressure: 40%
- gold diff @15: 25%
- kill threat: 20%
- matchup winrate pressure: 15%

## Implementação

A regra central está em `utils/scoring.py`.

Sempre que o score mudar:
1. recalcule os componentes
2. atualize `identity.score`
3. atualize `identity.difficulty`
4. rode `python scripts/validate_data.py`
5. rode `python scripts/build_indexes.py`
