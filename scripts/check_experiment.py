"""Validate an experiment plan without importing simulation or ML packages."""

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from vla_rl.experiment import validate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path)
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        count = validate(config)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))
    print(f"Valid plan: {config['task']} / {config['base_policy']}")
    print(f"Planned test episodes: {count} (before replication across training seeds)")
    print("Configuration check only. No VLA, simulator, or RL training was executed.")


if __name__ == "__main__":
    main()
