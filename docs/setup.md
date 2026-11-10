# Setup and first baseline

## Local starter

Use Python 3.11+ to run the README checks. No training dependencies are needed.
Optional editable install: `python -m pip install -e .`.

## University GPU server

1. Confirm the assigned GPU model, VRAM, CUDA driver, job limits, and disk quota.
2. Use an isolated environment and follow the current
   [LeRobot RoboCasa guide](https://huggingface.co/docs/lerobot/main/robocasa).
   The integration has version-sensitive dependencies; do not assume a generic
   `pip install robocasa` or the newest version of every package is compatible.
3. Install RoboCasa, robosuite, and LeRobot outside this repository or under the
   ignored `third_party/` directory. Record each Git commit and `pip freeze`.
4. Download the checkpoint named in the configuration and the required assets.
   Match camera names, image processing, robot embodiment, action normalization,
   coordinate frames, and control frequency to the checkpoint's integration.
5. Run the documented `CloseFridge` evaluation with one episode first. Verify
   headless rendering on the assigned GPU. Save a video and task success flag.
6. Run a small fixed-seed batch. Measure rollout time and GPU memory before
   allocating a full training run. An available checkpoint does not guarantee
   competence on this task or on your installed environment version.

Use upstream evaluation commands until they work; the local JSON is our study
configuration, not an upstream LeRobot configuration. A translation adapter is
still required.

## Implementing the residual wrapper

- Keep the VLA frozen; it still needs inference during simulation rollouts.
- Let TD3's action represent the bounded residual. The wrapper composes it with
  the base action and executes the result in the environment.
- Store the residual action in TD3's replay buffer when using this formulation;
  never silently train a critic on combined actions while the actor emits residuals.
- Include the base action and necessary execution state in the RL observation.
- Respect action chunks and control cadence. Do not add arbitrary continuous
  corrections to discrete mode switches. Specify rotation composition explicitly.
- Check zero-residual equivalence before training, and log clipping frequency.
- Fault injection affects only the intended sensor stream; retain clean state
  privately for reward, scoring, and fault diagnostics.

No exact library lockfile is supplied yet: generate one from the first working
server installation. Do not commit credentials or downloaded weights.
