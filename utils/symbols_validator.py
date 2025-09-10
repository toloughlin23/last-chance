from typing import List

from services.snapshot_client import SnapshotClient


def filter_symbols_present_on_polygon(symbols: List[str], chunk_size: int = 50) -> List[str]:
    if not symbols:
        return []
    client = SnapshotClient()
    present: set[str] = set()
    for i in range(0, len(symbols), chunk_size):
        chunk = symbols[i:i + chunk_size]
        try:
            # fetch_trading_halts returns only symbols present in Polygon snapshot response
            halted_map = client.fetch_trading_halts(chunk)
            present.update(halted_map.keys())
        except Exception:
            continue
    # Preserve original order
    return [s for s in symbols if s in present]

