# Research protocol (draft)

## Scope and hypotheses

Simulation-only evaluation of a frozen VLA with a learned residual controller.
The first task is CloseFridge; two additional tasks remain to be selected.

- H1: At matched error magnitude, persistent position bias is more damaging than
  independent position jitter for an object-conditioned residual.
- H2: A temporal consistency gate reduces harmful corrections compared with a
  tuned confidence threshold without eliminating clean-condition gains.

These hypotheses are untested. Generic residual learning, confidence gating, and
memory are established concepts; the study must demonstrate a specific finding.

## Fault model

The starter implements position faults in meters, in a caller-defined common
frame. It does not estimate objects from RGB and does not corrupt orientation.
Add a validity mask and observation age when integrating it. A missing position
must not become an apparent object at the world origin.

Jitter and bias use the same fixed Euclidean offset norm during the same active
window. Jitter resamples its direction each step; bias retains one direction.
Freeze retains the last pre-fault observation. Its error depends on actual motion
and is not automatically magnitude-matched. Dropout is a contiguous missing-data
window. Pilot values are placeholders, not measured tracker specifications.

For each fault schedule, pair methods on initial state and seed. Evaluate both
time-based faults and matched task-phase triggers when available. Log realized
errors because methods can visit different states. Test unseen durations and
magnitudes after tuning. A tracking freeze on a static object may be harmless.

Faulted simulator state is a synthetic sensor abstraction. If claiming realistic
vision-tracker robustness later, add measured or rendered tracking failures.

## Baselines and controls

1. Frozen VLA.
2. Residual TD3 trained with documented noise/dropout augmentation.
3. Same residual plus tuned confidence gating.
4. Same residual plus the proposed temporal gate.
5. Add a simple temporal filtering baseline before a novelty claim.

Use identical information access and execution budgets. Confidence is not yet
implemented: specify and calibrate a signal available at deployment, never an
oracle flag revealing the injected fault. Temporal checks cannot necessarily
detect a stable bias; test that limitation explicitly.

Tune thresholds on validation data, not test trajectories. Disjoint seeds alone
are insufficient: reserve object/layout variants and fault settings too. Train
multiple independent residual seeds and report uncertainty at the episode and
training-run level, not by treating video frames as independent samples.

## Metrics

- Task success including failures and timeouts in the denominator.
- Completion time for successes, alongside failure/timeout counts.
- Recovery after valid tracking returns.
- Suppression rate and clean-performance loss.
- Harmful corrections: branch identical saved simulator and policy states into
  base-only and residual rollouts, with matched disturbances. Record cases where
  the base succeeds and the corrected rollout fails. Reset action queues, RNGs,
  and recurrent/gate state when branching; this is an analysis tool, not oracle
  information for the deployed policy.

Do not equate a reduction in motion with improved safety. No hardware readiness
or general safety guarantee follows from these experiments.

## Run records

Store under ignored `runs/<run-id>/`: configuration, upstream Git revisions,
package versions, GPU details, checkpoint revision, wall time, seeds, episode
outcomes, and selected videos. Export small aggregate tables to Git only after
review. Never substitute illustrative numbers for measured results.
