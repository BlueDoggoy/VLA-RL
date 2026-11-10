"""Synthetic position-sensor faults, not a camera tracker or SE(3) pose model.

Positions must use meters in one consistent coordinate frame. Bias and jitter
have exactly the same Euclidean error magnitude at every active step; only
their temporal persistence differs. Freeze error depends on object motion.
Create a new injector with the same seed for each paired rollout.
"""

from dataclasses import dataclass
from math import isfinite, sqrt
from random import Random

KINDS = {"clean", "jitter", "bias", "freeze", "dropout"}


@dataclass(frozen=True)
class FaultSpec:
    kind: str
    magnitude_m: float = 0.0
    start_step: int = 0
    duration_steps: int = 1

    def __post_init__(self):
        if self.kind not in KINDS:
            raise ValueError(f"Unknown fault kind: {self.kind}")
        if not isfinite(self.magnitude_m) or self.magnitude_m < 0:
            raise ValueError("magnitude_m must be finite and nonnegative")
        if type(self.start_step) is not int or self.start_step < 0:
            raise ValueError("start_step must be a nonnegative integer")
        if type(self.duration_steps) is not int or self.duration_steps <= 0:
            raise ValueError("duration_steps must be a positive integer")


class PositionFault:
    """Call once per control step in increasing order; dropout returns None.

Freeze retains the last pre-fault position. If the fault starts on the first
observation, it retains that first observation instead. Do not encode missing
observations as a physical zero position; propagate a validity mask downstream.
"""

    def __init__(self, spec: FaultSpec, seed: int):
        self.spec = spec
        self.rng = Random(seed)
        self.bias = self._offset()
        self.last_position = None
        self.last_step = -1

    def _offset(self):
        vector = [self.rng.gauss(0, 1) for _ in range(3)]
        length = sqrt(sum(x * x for x in vector))
        if length == 0:
            return (self.spec.magnitude_m, 0.0, 0.0)
        return tuple(x * self.spec.magnitude_m / length for x in vector)

    def apply(self, position, step: int):
        point = tuple(float(x) for x in position)
        if len(point) != 3 or not all(isfinite(x) for x in point):
            raise ValueError("position must contain three finite coordinates")
        if type(step) is not int or step <= self.last_step:
            raise ValueError("step must be a nonnegative, strictly increasing integer")
        self.last_step = step
        active = self.spec.start_step <= step < (
            self.spec.start_step + self.spec.duration_steps
        )
        if not active or self.spec.kind == "clean":
            self.last_position = point
            return point
        if self.spec.kind == "dropout":
            return None
        if self.spec.kind == "freeze":
            if self.last_position is None:
                self.last_position = point
            return self.last_position
        offset = self.bias if self.spec.kind == "bias" else self._offset()
        self.last_position = point
        return tuple(x + delta for x, delta in zip(point, offset))
