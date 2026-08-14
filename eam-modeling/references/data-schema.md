# Data schema and audit

## Minimum fields

For ordinary choice/RT EAMs, resolve:

| Role | Typical names | Requirement |
|---|---|---|
| Participant | `subjects`, `subject`, `participant`, `id` | Required for hierarchical analysis |
| Response | `R`, `response`, `choice`, `keypress` | Required |
| Response time | `rt`, `RT`, `response_time` | Required; convert once to seconds |
| Stimulus/correct response | `S`, `stimulus`, `target`, `correct` | Usually required for accuracy or match coding |
| Trial order | `trial`, `trial_number`, `t` | Required for dynamic and RL models |
| Condition | experiment-specific factors | Required when parameters vary by manipulation |

For RL-EAMs additionally resolve action/symbol identity, received outcome/reward, which symbol the feedback belongs to, block/session resets, and counterfactual feedback structure.

## Audit sequence

1. Preserve the original file and record its absolute path, size, modification time, and hash.
2. Confirm rows represent trials and identify any repeated-measures or long-format expansion.
3. Inspect column classes, missingness, unique levels, and numeric ranges.
4. Verify participant-by-condition trial counts and empty cells.
5. Verify response levels and their connection to boundaries or accumulators.
6. Determine RT units from documentation; use magnitude only as a provisional clue.
7. Inspect RT quantiles globally and by participant, response class, and condition.
8. Identify task-imposed deadlines, censoring, truncation, contaminant processes, and practice trials.
9. Check trial order and reset points before computing learning or dynamic covariates.
10. Save an explicit mapping and exclusion ledger.

## Coding rules

- Convert identifiers and experimental categories to factors intentionally.
- Set reference levels before constructing the EMC2 design.
- Keep observed response `R` distinct from latent response `lR`.
- Define correctness or accumulator match as a function, then inspect it on representative rows.
- Do not assume alphabetical factor order has scientific meaning.
- Avoid a user column named `trials` when EMC2 reserves it internally.
- Carry lower/upper truncation or censoring values into the design rather than only deleting rows.

## Blocking ambiguities

Pause before fitting when any of these remain unresolved:

- milliseconds versus seconds;
- response key versus semantic choice;
- correct response cannot be reconstructed;
- trial order or learning reset points are missing;
- the same row is duplicated for reasons not understood;
- exclusion rules would remove a material fraction of data;
- a condition has too few responses or no errors for intended parameters;
- participant identifiers are reused across groups or sessions.

