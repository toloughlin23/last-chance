import io
import requests
import pandas as pd
from typing import List


class SP500Client:
    WIKI_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    def fetch_symbols(self) -> List[str]:
        resp = requests.get(self.WIKI_URL, timeout=30)
        resp.raise_for_status()
        # Parse HTML tables and pick the first that contains a 'Symbol' column
        tables = pd.read_html(io.StringIO(resp.text))
        for tbl in tables:
            cols = [str(c).strip().lower() for c in tbl.columns]
            if any(c.startswith("symbol") for c in cols):
                symbol_col = [c for c in tbl.columns if str(c).strip().lower().startswith("symbol")][0]
                syms = [str(s).strip().upper().replace(" \u2013 ", "-") for s in tbl[symbol_col].tolist()]
                # Clean common artifacts (e.g., '.' separators kept for class shares like BRK.B)
                cleaned = [s.replace("\u200a", "").replace(" ", "").replace("/WS", "") for s in syms]
                # Remove non-alphanumeric except . and -
                filtered: List[str] = []
                for s in cleaned:
                    keep = ''.join(ch for ch in s if ch.isalnum() or ch in ['.', '-'])
                    if keep:
                        filtered.append(keep)
                # Deduplicate preserving order
                seen = set()
                ordered = []
                for s in filtered:
                    if s not in seen:
                        seen.add(s)
                        ordered.append(s)
                return ordered
        return []

