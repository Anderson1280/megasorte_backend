# analytics/frequency.py
from collections import Counter
from typing import List

def frequency_analysis(draws: List[List[int]]) -> dict:
    """
    Recebe uma lista de sorteios (ex: [[1,2,3,4,5,6], ...])
    Retorna frequência absoluta de cada número
    """
    counter = Counter()
    for draw in draws:
        counter.update(draw)

    return dict(sorted(counter.items()))
