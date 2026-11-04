# Local model guardrails benchmark

Original scenarios and Qwen/GPT-OSS records recovered from talks branch `agent-authority-talks` commit `43b8ae1`. The model evaluates each scenario in bare and guarded modes; bars distinguish fully correct completion from correct state without the terminal `done` call, as in the original chart.

LFM: LiquidAI LFM3-Audio-2B Q4_K_M GGUF, cached model snapshot `02355c1a141e464a064f2ab2c276638dbcb7f38a`, llama.cpp 0.8.0 build 11960, local laptop, 32768 context, native tool calling. Same scenario code, no parallel tool calls, temperature 0.6, seeds 1000–1009, 10 trials per mode per scenario. Guardrails source is Agentware commit `5858214`, the latest guardrails commit before the October 19 runs; the exact original working-tree revision is not recorded and could have differed. Qwen has four trials per coding mode and five per access mode; GPT-OSS has ten. Hardware and model runtimes differ, so timing is not directly comparable. Small sample sizes mean results are illustrative, not a model leaderboard.

Regenerate the chart with Python 3.10+ and matplotlib, setting `AGENTWARE_SRC` to a compatible Agentware Python source directory: `python graph.py`. Run the benchmarks using `probe.py` and the model server as in the original scripts; save each scenario's JSONL under `runs/`.

## Enhanced recovery experiment

`--mode enhanced` is an opt-in harness condition. It uses Agentware Python 0.16.0 source at `961c026f46a16b42c9ca670a855de44158519`, confirmed identical to upstream main on November 4, 2026. Agentware's guardrails facade is adapted from Forge's design; the Python package does not declare Forge as a runtime dependency. The harness adds strict argument checks, literal-only Python-style call rescue, bounded diagnostic nudges on errors, repeated-test detection, and truncation of older tool-result content. Original `bare` and `guarded` behavior remains available. Compaction preserves tool-call/result messages and the original task but is not a hard context-size guarantee.

For example, with a local llama.cpp server already running:

```sh
AGENTWARE_SRC=/path/to/Agentware/python/src \
LLM_BASE_URL=http://127.0.0.1:18191/v1 LLM_MODEL=lfm3-audio-2b \
python3 probe.py 3 --scenario coding:1 --no-parallel --mode enhanced
```

`lfm-enhanced-*.jsonl` files are exploratory trials, separate from the original chart. The `final` files use the current code; earlier enhanced files predate the latest diagnostic and compaction changes. In the final one-trial checks, neither task completed; nudges and coding-result compaction were triggered. This is not enough data to measure an improvement.

**Access scenario limitation:** its task text does not specify that the mock's verifier requires an `http_api` connector. If the model creates the same-named connector with a different kind, the mock exposes no tool to update or remove it. Treat the access scores in the existing comparison cautiously. Correcting the task and adding repair tools changes the benchmark; rerun all models before comparing corrected results.

## Corrected access scenario (v2)

Run with `--scenario access_provisioning_v2`. It specifies the CRM connector kind and adds simulated `list_connectors` and `update_connector` tools. An update preserves the connector ID and invalidates old authorization checks; the agent must verify all three decisions again. The original `kei_provisioning` remains unchanged, and its results cannot be mixed with v2.

A single LFM enhanced-mode smoke test reached `done` but scored 0.25/1.0: a completed tool sequence does not imply the intended access policy is correct. This is a workflow check, not a benchmark estimate. The `success` field means the `done` call was accepted; use `success && accuracy == 1.0` for fully correct completion.

### Partial-progress comparison

The generic `access_provisioning_v2` task explicitly says to add Alice and not Bob. A three-trial LFM comparison of this task is saved in `runs/lfm-access-v2-final-comparison.jsonl`. The mean `state_score` was 1.00 bare, 0.25 guarded, and 0.25 enhanced; no run reached an accepted `done` call. This small sample does **not** demonstrate an improvement from guardrails. In the bare runs the final state scored 1.00 despite incomplete termination; in guarded and enhanced runs the prerequisite retry limit stopped progress. The earlier v2 smoke and comparison files used different task wording or nudge settings and must not be pooled with these results. The graph of the original three-model results predates this corrected scenario.

## Progress-aware harness comparison

The opt-in `progress` mode keeps the original modes unchanged, removes only the unnecessary policy-before-membership prerequisite for the generic simulated access task, and bounds retries while resetting the harness retry counter on a successful tool action. Its task-specific checklist is built from observed tool results and invalidates authorization checks after a state-changing call. If the model stops with the observed checklist complete, it prompts the model to call `done`; it never calls the tool for the model. Old tool results can be compacted without breaking tool-call/result pairs. Detailed traces are opt-in (`--trace PATH`) and contain raw synthetic tool arguments and results; do not use this trace option for sensitive data.

Three matched trials per mode are in `runs/lfm-progress-final.jsonl`, with detailed synthetic traces in `runs/lfm-progress-final-traces.jsonl`. In this exploratory single-task sample, mean final-state scores were bare 100%, basic 25%, progress-aware 100%; fully correct completions were 0/3, 0/3, and 3/3, respectively. These modes differ in several ways at once, so the result does not isolate which individual change helped. The observed repeated trajectories do not establish statistical independence or general performance. Regenerate `progress-comparison.png` with `python progress_graph.py` (requires matplotlib and numpy).

## Matched three-model head-to-head

On 2026-11-04, reran the same generic `access_provisioning_v2` task with bare, basic (`guarded`), and progress-aware harnesses: three trials per model/mode, seeds 1000–1002, temperature 0.6, one tool call at a time, and 30-turn limit. Qwen3.8-27B ran via the already-loaded `pedrogpt` llama.cpp server; GPT-OSS-20B MXFP4 and LFM3-Audio-2B Q4_K_M ran locally via llama.cpp 0.8.0 (build 11960). Models have different hardware and serving settings; these scores are not a speed comparison. Guardrails use Agentware source at `961c026f46a16b42c9ca670a855de44158519`.

| Model | Bare state / finished | Basic state / finished | Progress-aware state / finished |
|---|---|---|---|
| Qwen3.8-27B | 100% / 3 of 3 | 75% / 2 of 3 | 100% / 3 of 3 |
| GPT-OSS-20B | 100% / 3 of 3 | 67% / 1 of 3 | 100% / 3 of 3 |
| LFM3-Audio-2B | 100% / 0 of 3 | 25% / 0 of 3 | 100% / 3 of 3 |

State is the mean of four mock-state criteria; finished means the terminal call was accepted and state score was 1.0. Progress-aware mode is a task-specific harness using observed simulated tool results to build a checklist, with more flexible prerequisites and finish nudges. It combines several changes, so this experiment cannot attribute the result to a single feature. Three trials on one task are exploratory, especially where trajectories repeat. See `runs/h2h-{qwen,gpt-oss,lfm}.jsonl` and corresponding `-traces.jsonl` for synthetic raw records. Generate the widescreen figure with `python head_to_head_graph.py`.

The optional legacy `analytics` scenario requires a private local CSV export and is not part of the public connector benchmark.
