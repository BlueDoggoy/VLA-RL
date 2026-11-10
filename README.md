# VLA-RL

Evaluating Residual Reinforcement Learning for Robust Household Manipulation

Residual reinforcement learning can improve a pretrained vision-language-action
(VLA) policy. This project investigates when those corrections fail, particularly
when object tracking produces persistent errors.

**Research question:** At comparable pose-error magnitude, do persistent tracking
errors cause more harmful residual corrections than independent noise, and can
a temporal consistency check mitigate that effect?

## Status

Project initialization only. This repository includes an experiment protocol,
configuration validator, deterministic synthetic position-fault generator, and
tests. **It does not yet run a robot, load a VLA, or train TD3. No experimental
results or novelty claims are established.**

## Quick start

Python 3.11 or newer; the starter uses only the standard library.

```bash
python scripts/check_experiment.py configs/close_fridge.json
python -m unittest discover -s tests -v
```

On Windows, use `py -3.11` instead of `python` if needed. A successful check prints
the proposed evaluation count; it does not execute simulation episodes.

## Planned stack

| Component | Starting choice |
| --- | --- |
| Physics and tasks | MuJoCo through RoboCasa |
| Robot | RoboCasa's compatible PandaOmron configuration |
| Frozen base policy | RoboCasa-trained SmolVLA, subject to baseline verification |
| Residual learner | TD3 via Stable-Baselines3 |
| First task | `CloseFridge` |
| Proposed extension | Temporal consistency gating of residual corrections |

The first milestone is a recorded baseline rollout. Choose the remaining two
tasks only after verifying environment assets and checkpoint competence. These
are adapted tasks, not an exact reproduction of the reference paper's FR3 scenes.

## Repository layout

```text
configs/                 Experiment settings
docs/                    Research protocol, setup, and milestones
scripts/                 Lightweight entry points
src/vla_rl/              Experiment validation and synthetic tracking faults
tests/                   Determinism and fault-semantics checks
```

Large checkpoints, downloaded datasets, videos, and generated runs are ignored.
Record download locations and exact upstream revisions instead of copying them
into Git. No upstream model or dataset licenses are overridden by this project.

## Getting started as a team

1. Read [setup](docs/setup.md) and reproduce one base-policy rollout on the server.
2. Follow [milestones](docs/milestones.md), keeping model and environment versions fixed.
3. Use the [research protocol](docs/research_protocol.md) to separate tuning from evaluation.
4. Commit small changes with the commands, configuration, and validation used.

## Related work and reusable sources

- [Object-Centric Residual RL (Kim et al., 2026)](https://arxiv.org/abs/2606.18953):
  object-pose-based residual TD3 over a frozen VLA; the main base VLA is GR00T-N1.5.
- [VLaRL (Saito et al., 2026)](https://arxiv.org/abs/2609.30868):
  subsequent work using VLA latents and sim-to-real latent alignment.
- [Uncertainty-calibrated VLA gating](https://pmc.ncbi.nlm.nih.gov/articles/PMC13210885/):
  related intervention and fallback research.
- [RoboCasa](https://github.com/robocasa/robocasa)
- [LeRobot RoboCasa integration](https://huggingface.co/docs/lerobot/main/robocasa)
- [SmolVLA RoboCasa checkpoint](https://huggingface.co/lerobot/smolvla_robocasa)
- [Stable-Baselines3 TD3](https://stable-baselines3.readthedocs.io/en/master/modules/td3.html)

The proposed contribution must be assessed against these and other related works.
Running residual RL on additional tasks is not, by itself, a new method.
