from pathlib import Path
from typing import Iterable, Dict, Tuple
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


def load_env_from_known_locations() -> Dict[str, str]:
    """Load environment variables from known provider-specific .env files.

    Order: polygon/.env, alpaca/.env, then project .env (later files do not override earlier values).
    Returns loaded environment variables for verification.
    """
    # utils/ is a direct child of project root
    project_root = Path(__file__).resolve().parent.parent
    loaded_vars = {}
    
    for dotenv_path in _candidate_env_paths(project_root):
        if dotenv_path.exists():
            result = load_dotenv(dotenv_path=dotenv_path, override=False)
            if result:
                # Read the file to get loaded variables
                try:
                    with open(dotenv_path, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#') and '=' in line:
                                key, value = line.split('=', 1)
                                loaded_vars[key.strip()] = value.strip()
                except Exception as e:
                    print(f"Warning: Could not read {dotenv_path}: {e}")
    
    return loaded_vars

def require_env(keys: Iterable[str]) -> Tuple[bool, Dict[str, str]]:
    """Validate required environment variables are present.

    Returns (ok, missing_map). ok=False if any missing.
    """
    missing: Dict[str, str] = {}
    for key in keys:
        if not os.getenv(key):
            missing[key] = "MISSING"
    return (len(missing) == 0, missing)
