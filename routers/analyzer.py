import json
from collections import Counter

def calculate_probabilities(entries):
    all_numbers = []

    for e in entries:
        # CORREÇÃO: e.numbers agora é uma string JSON que precisa ser decodificada
        try:
            numbers = json.loads(e.numbers)
            all_numbers.extend(numbers)
        except AttributeError:
            # Caso e.numbers não exista ou não seja string (Fallback de segurança)
            print(f"Erro ao processar entrada: {e}")
        except json.JSONDecodeError:
            print(f"Erro ao decodificar JSON: {e.numbers}")

    counter = Counter(all_numbers)

    probability = {
        "most_common": counter.most_common(6),
        "least_common": counter.most_common()[-6:]
    }

    return probability