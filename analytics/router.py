# analytics/generator.py
import random
from typing import List
from analytics.frequency import frequency_analysis
from analytics.patterns import analyze_patterns
from analytics.region_map import region_weight

NUMBERS = list(range(1, 61))

def generate_balanced_game(
    historical_draws: List[List[int]],
    region: str | None = None
) -> dict:
    """
    Gera um jogo balanceado com base em estatística.
    Não realiza previsão.
    """

    freq = frequency_analysis(historical_draws)

    weights = []
    for n in NUMBERS:
        base_weight = freq.get(n, 1)
        if region:
            base_weight *= region_weight(region)
        weights.append(base_weight)

    for _ in range(100):
        game = sorted(set(random.choices(NUMBERS, weights=weights, k=6)))
        if len(game) != 6:
            continue

        patterns = analyze_patterns(game)

        # Regras estatísticas simples e seguras
        if 2 <= patterns["pares"] <= 4 and 120 <= patterns["soma_total"] <= 210:
            return {
                "numeros": game,
                "analise": patterns
            }

    # fallback seguro
    game = sorted(random.sample(NUMBERS, 6))
    return {
        "numeros": game,
        "analise": analyze_patterns(game)
    }
