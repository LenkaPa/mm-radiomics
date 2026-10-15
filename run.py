"""Jediný vstupní bod pipeline mm-radiomics.

    python run.py --config config.yaml            # celý běh
    python run.py --config config.yaml --check    # jen kontrola vstupů
    python run.py --config config.yaml --step report
"""
import argparse
import sys

from mmrad import clinical, config, extract, inventory, report, robustness

STEPS = {
    "inventory": inventory.run,
    "extract": extract.run,
    "robustness": robustness.run,
    "clinical": clinical.run,
    "report": report.run,
}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Radiomická pipeline pro Spinal-Multiple-Myeloma-SEG")
    parser.add_argument("--config", default="config.yaml", help="cesta ke konfiguraci (výchozí config.yaml)")
    parser.add_argument("--check", action="store_true", help="jen zkontroluje vstupy, nic nepočítá")
    parser.add_argument("--step", choices=list(STEPS), help="spustí jen jeden krok")
    args = parser.parse_args(argv)

    cfg = config.load(args.config)

    if args.check:
        inventory.run(cfg, check_only=True)
        return 0

    steps = [args.step] if args.step else list(STEPS)
    for name in steps:
        print(f"== krok: {name}")
        STEPS[name](cfg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
