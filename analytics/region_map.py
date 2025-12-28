# analytics/patterns.py
from typing import List

def analyze_patterns(numbers: List[int]) -> dict:
    pares = sum(1 for n in numbers if n % 2 == 0)
    impares = len(numbers) - pares
    soma = sum(numbers)
    sequencia = any(numbers[i] + 1 == numbers[i + 1] for i in range(len(numbers) - 1))

    return {
        "pares": pares,
        "impares": impares,
        "soma_total": soma,
        "possui_sequencia": sequencia
    }
