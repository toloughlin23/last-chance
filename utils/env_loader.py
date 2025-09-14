import os
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

try:
    from dotenv import find_dotenv, load_dotenv
except Exception:
    # If python-dotenv is not installed, the loader will be a no-op.
    def load_dotenv(*args, **kwargs):  # type: ignore
        return False
    def find_dotenv(*args, **kwargs):  # type: ignore
        return ""


def _candidate_env_paths(project_root: Path) -> Iterable[Path]:
    """Ordered list of .env locations we support.

    - Service-scoped first (do not override project .env)
    - Then project-level variants
    """
    yield project_root / "polygon" / ".env"
    yield project_root / "alpaca" / ".env"
    # Common project-level variants (do not override values already set)
    yield project_root / ".env"
    yield project_root / ".env.local"
    yield project_root / ".env.development"
    yield project_root / ".env.dev"


def load_env_from_known_locations() -> Dict[str, str]:
    """Load environment variables from known provider-specific .env files.

    Order: polygon/.env, alpaca/.env, then project .env (later files do not override earlier values).
    Returns loaded environment variables for verification.
    """
    # utils/ is a direct child of project root
    project_root = Path(__file__).resolve().parent.parent
    loaded_vars = {}
    
    # 1) Load nearest .env discovered by python-dotenv as a safety-net
    auto_path = find_dotenv(usecwd=True)
    if auto_path:
        load_dotenv(dotenv_path=auto_path, override=False)

    # 2) Load our explicit, ordered candidates (later files do not override)
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


def require_env_or_raise(keys: Iterable[str]) -> None:
    """Strictly require the provided env keys, raising with a helpful message.

    This prevents silent misconfiguration and shows which paths we searched.
    """
    ok, missing = require_env(keys)
    if ok:
        return
    project_root = Path(__file__).resolve().parent.parent
    searched: List[str] = [str(p) for p in _candidate_env_paths(project_root)]
    auto = find_dotenv(usecwd=True)
    if auto:
        searched.insert(0, auto)
    raise RuntimeError(
        "Missing required env keys: " + ", ".join(missing.keys()) +
        "\nSearched .env locations (no override):\n - " + "\n - ".join(searched)
    )
