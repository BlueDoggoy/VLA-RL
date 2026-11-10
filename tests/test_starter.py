import copy
import json
from math import dist
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vla_rl.experiment import validate
from vla_rl.faults import FaultSpec, PositionFault


class FaultTests(unittest.TestCase):
    def test_bias_and_jitter_have_matched_error_norm(self):
        outputs = {}
        for kind in ("bias", "jitter"):
            injector = PositionFault(FaultSpec(kind, 0.01, 0, 5), 42)
            outputs[kind] = [injector.apply((0, 0, 0), i) for i in range(5)]
            for point in outputs[kind]:
                self.assertAlmostEqual(dist(point, (0, 0, 0)), 0.01)
        self.assertEqual(len(set(outputs["bias"])), 1)
        self.assertGreater(len(set(outputs["jitter"])), 1)

    def test_reproducible_paired_faults(self):
        spec = FaultSpec("jitter", 0.02, 1, 3)
        a, b = PositionFault(spec, 7), PositionFault(spec, 7)
        self.assertEqual([a.apply((1, 2, 3), i) for i in range(6)],
                         [b.apply((1, 2, 3), i) for i in range(6)])

    def test_freeze_retains_pre_fault_sample_then_recovers(self):
        f = PositionFault(FaultSpec("freeze", 0, 1, 2), 0)
        self.assertEqual([f.apply((i, 0, 0), i) for i in range(4)],
                         [(0, 0, 0), (0, 0, 0), (0, 0, 0), (3, 0, 0)])

    def test_dropout_window(self):
        f = PositionFault(FaultSpec("dropout", 0, 1, 2), 0)
        self.assertEqual([f.apply((1, 0, 0), i) for i in range(4)],
                         [(1, 0, 0), None, None, (1, 0, 0)])

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            FaultSpec("bias", float("nan"))
        with self.assertRaises(ValueError):
            FaultSpec("bias", 0, -1)
        f = PositionFault(FaultSpec("clean"), 0)
        with self.assertRaises(ValueError):
            f.apply((0, 0), 0)
        f.apply((0, 0, 0), 0)
        with self.assertRaises(ValueError):
            f.apply((0, 0, 0), 0)


class ExperimentTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((ROOT / "configs/close_fridge.json").read_text())

    def test_plan_count(self):
        self.assertEqual(validate(self.config), 1200)

    def test_split_leakage_rejected(self):
        bad = copy.deepcopy(self.config)
        bad["seed_sets"]["test"] = [0]
        with self.assertRaises(ValueError):
            validate(bad)

    def test_empty_faults_rejected(self):
        self.config["faults"] = []
        with self.assertRaises(ValueError):
            validate(self.config)


if __name__ == "__main__":
    unittest.main()
