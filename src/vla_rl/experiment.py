"""Validate a planned experiment; this module does not run robot simulation."""

from .faults import FaultSpec


def validate(config):
    for field in ("task", "base_policy"):
        if not isinstance(config[field], str) or not config[field].strip():
            raise ValueError(f"{field} must be a nonempty string")
    sets = []
    for split in ("train", "validation", "test"):
        seeds = config["seed_sets"][split]
        if not seeds or any(type(s) is not int or s < 0 for s in seeds):
            raise ValueError(f"{split} seeds must be nonnegative integers")
        if len(set(seeds)) != len(seeds):
            raise ValueError(f"Duplicate seeds in {split}")
        sets.append(set(seeds))
    if any(sets[i] & sets[j] for i in range(3) for j in range(i + 1, 3)):
        raise ValueError("Training, validation, and test seeds must be disjoint")
    episodes = config["evaluation_episodes_per_seed"]
    if type(episodes) is not int or episodes <= 0:
        raise ValueError("evaluation_episodes_per_seed must be a positive integer")
    methods = config["methods"]
    if not methods or any(not isinstance(m, str) or not m for m in methods):
        raise ValueError("methods must contain nonempty names")
    if len(set(methods)) != len(methods):
        raise ValueError("methods must be unique")
    if not config["faults"]:
        raise ValueError("At least one fault condition is required")
    for fault in config["faults"]:
        FaultSpec(**fault)
    return episodes * len(sets[2]) * len(methods) * len(config["faults"])
