# backend/analyzer_official.py
import requests
import json
import time
from collections import Counter
from typing import List, Dict
from pathlib import Path
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_DIR = Path(__file__).resolve().parent
CACHE = BASE_DIR / "official_cache.json"
CACHE_EXPIRY_HOURS = int(os.getenv("CACHE_EXPIRY_HOURS", "24"))

class OfficialResults:
    def __init__(self, cache_path: Path = CACHE):
        self.cache_path = Path(cache_path)
        self.results: List[List[int]] = []
        self._load_cache()

    def _load_cache(self):
        if self.cache_path.exists():
            file_mod_time = self.cache_path.stat().st_mtime
            if (time.time() - file_mod_time) > (CACHE_EXPIRY_HOURS * 3600):
                try:
                    self.cache_path.unlink()
                except OSError:
                    pass
                self.results = []
                return
            try:
                data = self.cache_path.read_text(encoding="utf-8")
                self.results = json.loads(data) if data else []
            except Exception:
                self.results = []
        else:
            self.results = []

    def _save_cache(self):
        try:
            self.cache_path.write_text(json.dumps(self.results, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

    def refresh(self, start_from: int = 1, limit_check: int = 200) -> List[List[int]]:
        url_base = "https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena"
        headers = {'User-Agent': 'Mozilla/5.0'}
        new_data = []
        start = start_from if start_from else (len(self.results) + 1)
        for concurso in range(start, start + limit_check):
            try:
                r = requests.get(f"{url_base}/{concurso}", headers=headers, timeout=10, verify=False)
                if r.status_code == 404:
                    break
                if r.status_code != 200:
                    continue
                data = r.json()
                dezenas = data.get("dezenasSorteadasOrdemSorteio") or []
                if dezenas:
                    new_data.append([int(x) for x in dezenas])
                time.sleep(0.5)
            except Exception:
                continue

        if new_data:
            self.results.extend(new_data)
            self._save_cache()
        return self.results

    def get_all(self) -> List[List[int]]:
        if not self.results:
            self.refresh(start_from=1, limit_check=100)
        else:
            self.refresh()
        return self.results

    def freq_map(self) -> Dict[int, int]:
        flat = [n for draw in self.get_all() for n in draw]
        return dict(self.static_counter(flat))

    @staticmethod
    def static_counter(flat_results: List[int]) -> Counter:
        counter = Counter(flat_results)
        for i in range(1, 61):
            counter.setdefault(i, 0)
        return counter

    def top_n(self, n=10):
        fm = self.freq_map()
        return sorted(fm.items(), key=lambda x: x[1], reverse=True)[:n]

    def bottom_n(self, n=10):
        fm = self.freq_map()
        return sorted(fm.items(), key=lambda x: x[1])[:n]

    def probabilities(self):
        fm = self.freq_map()
        total = sum(fm.values()) or 1
        return {num: round(cnt / total, 8) for num, cnt in fm.items()}
