# Self-Hosting Agents Talk TODOs

Post–AI Builder Day revision work:

- [ ] Build a multistep agent web UI; a streamed chat response is not enough.
- [ ] Pick one bounded demo job with at least three tool calls and a machine-checkable result.
- [ ] Show task state, tool arguments, tool results, retries, token counts, and verification in the UI.
- [ ] Record the full web-agent run over Tailscale to the home RTX 5090.
- [ ] Record a clean Pedro Tag Discord agent run; the live Discord demo worked and should stay.
- [ ] Save representative benchmark output; the benchmark demo worked and should stay.
- [ ] Calculate cost per completed demo job from measured GPU time and successful completions.
- [ ] Refresh Modal and RunPod rates immediately before the next talk.
- [ ] Add one real Pedro CLI harness trace showing phases, scoped tools, retries, compaction, and telemetry.
- [ ] Rehearse the harness explanation separately; distinguish the model, agent loop, and harness responsibilities.

Proven demo elements:

- Pedro Tag in Discord
- local llama.cpp benchmark: TTFT, prompt tok/s, generation tok/s, p50/p95 latency, and MTP acceptance

Demo fallback plan:

- [ ] Keep recorded runs for the multistep web agent and Pedro Tag.
- [ ] Keep static screenshots of every tool-call transition and the final verified result.
- [ ] Keep saved benchmark output in the deck directory.
- [ ] Download external video/GIF assets locally before the next conference.

Optional appendix topics:

- LoRAs and Unsloth Studio
- CPU control plane and GPU cycling
- GPU scheduling details
- model-quality discussion
- detailed Modal/RunPod cost calculations
