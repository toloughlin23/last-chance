from pathlib import Path
from typing import Iterable
import os

try:
    from dotenv import load_dotenv
except Exception:
    # If python-dotenv is not installed, the loader will be a no-op.
    def load_dotenv(*args, **kwargs):  # type: ignore
        return False


def _candidate_env_paths(project_root: Path) -> Iterable[Path]:
    yield project_root / "polygon" / ".env"
    yield project_root / "alpaca" / ".env"
    yield project_root / ".env"


def load_env_from_known_locations() -> None:
    """Load environment variables from known provider-specific .env files.

    Order: polygon/.env, alpaca/.env, then project .env (later files do not override earlier values).
    """
    # utils/ is a direct child of project root
    project_root = Path(__file__).resolve().parent.parent
    for dotenv_path in _candidate_env_paths(project_root):
        if dotenv_path.exists():
            load_dotenv(dotenv_path=dotenv_path, override=False)
