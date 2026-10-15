"""Načtení a základní kontrola config.yaml."""
from pathlib import Path

import yaml

REQUIRED = ["paths", "reconstructions", "roi", "extraction", "robustness", "clinical"]
KNOWN_RECONSTRUCTIONS = {"conventional", "VMI40", "VMI80", "VMI120",
                         "CaSupp25", "CaSupp50", "CaSupp75", "CaSupp100"}


def load(path):
    path = Path(path)
    if not path.exists():
        raise SystemExit(f"Konfigurace {path} neexistuje.")
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    missing = [key for key in REQUIRED if key not in cfg]
    if missing:
        raise SystemExit(f"V {path} chybí sekce: {', '.join(missing)}")
    unknown = set(cfg["reconstructions"]) - KNOWN_RECONSTRUCTIONS
    if unknown:
        raise SystemExit(f"Neznámé rekonstrukce v configu: {', '.join(sorted(unknown))}")
    return cfg
