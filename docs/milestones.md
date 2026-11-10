# Milestones

## 1. Baseline integration
- [ ] Confirm server access, GPU allocation, and deadline.
- [ ] Pin a working RoboCasa/LeRobot/checkpoint combination.
- [ ] Run CloseFridge and save one actual robot rollout video.
- [ ] Establish repeatable nonzero base-policy success.

## 2. Residual learning
- [ ] Implement action and observation adapters.
- [ ] Verify zero-residual rollouts match the base policy.
- [ ] Train TD3 on one task and check learning against the frozen baseline.
- [ ] Measure throughput and budget repeated seeds.

## 3. Tracking-fault study
- [ ] Integrate the synthetic position faults and validity/age fields.
- [ ] Measure independent versus persistent errors under matched conditions.
- [ ] Define a non-oracle confidence baseline and simple filter.
- [ ] Implement the temporal gate only after establishing a baseline failure.

## 4. Evidence and delivery
- [ ] Finalize two additional tasks with working assets and base-policy support.
- [ ] Complete held-out evaluation and paired intervention analysis.
- [ ] Review closest literature before claiming novelty.
- [ ] Produce one method figure, failure curves, and a compact results table.
- [ ] Write the three-page paper and record a presentation demonstration.

Suggested ownership: one person owns environment/VLA integration, one owns
residual learning and gating, and one owns evaluation and reproducibility. For
two people, share evaluation and writing. Complete one end-to-end task before
expanding to three.
