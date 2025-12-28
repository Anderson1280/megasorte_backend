from typing import List

def analyze_patterns(numbers: List[int]) -> dict:
    pares = sum(1 for n in numbers if n % 2 == 0)
    impares = len(numbers) - pares
    soma = sum(numbers)
    # Verifica se há números em sequência (ex: 10, 11)
    sequencia = any(numbers[i] + 1 == numbers[i + 1] for i in range(len(numbers) - 1))

    return {
        "pares": pares,
        "impares": impares,
        "soma_total": soma,
        "possui_sequencia": sequencia
    }

# Definindo um valor padrão para region_weight para evitar o erro de importação no app.py
region_weight = {}