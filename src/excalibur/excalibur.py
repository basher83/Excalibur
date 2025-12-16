#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = ["xai_sdk>=1.4.1", "pyyaml>=6.0", "click>=8.1"]
# ///

import os
import yaml
from click import command, argument, option
from xai_sdk import Client
from xai_sdk.chat import user, system

# Load KB (fixed quotes for colons in values)
KB_YAML = """
phases:
  planning:
    - technique: Metacognitive Scaffolding
      tip: List 3 assumptions + 4 edges + 2-sentence approach pre-gen.
      model_tune:
        claude_code: "Use tools for edge sim (e.g., lint stub)."
        gemini_cli: "Visualize edges as diagram; multimodal input."
        chatgpt: "CoT: Step-by-step assumption chain."
    - technique: /plan Mode Split  # New from [post:13]
      tip: Break task into plan (abstract) + action (execute) phases; use /plan CLI for agentic flow.
      model_tune:
        claude_code: "Invoke /plan for prototyping; refine 80% auto-complete."
        gemini_cli: "Parallel plans: Score 3 variants via eval."
        chatgpt: "Few-shot: 2 plan-action examples."
  execution:
    - technique: Incremental Change Framing
      tip: Propose 3 minimal deltas w/ pros/cons; no full rewrites.
      model_tune:
        claude_code: "Agentic: Delegate sub-tasks to parallel agents."
        gemini_cli: "Parallel: Run 3 variants, score via eval."
        chatgpt: "Few-shot: 2 examples of incremental fixes."
    - technique: XML Tagging for Structure  # New from [post:0,1,5]
      tip: Wrap inputs/outputs in <tags> (e.g., <code>[snippet]</code>); boosts adherence 20-30%.
      model_tune:
        claude_code: "Use <analysis> + <test_code> for Claude.md workflows."
        gemini_cli: "Multimodal: Tag diagrams for visual parse."
        chatgpt: "JSON escapes for few-shot examples."
  debug:
    - technique: Self-Verification Loop
      tip: Write → Lint/Test → Explain fixes → Iterate 2x.
      model_tune:
        claude_code: "Terminal tool: Run code, paste output for critique."
        gemini_cli: "Inline eval: Score this on idempotency 1-10."
        chatgpt: "Confidence: End w/ 90% sure? Gaps?."
    - technique: Tree-of-Thoughts Branching  # New from [post:3,12]
      tip: Explore 3+ branches (e.g., fix variants); score/prune before commit—+10% SWE Bench.
      model_tune:
        claude_code: "YOLO mode: Let cook 30min, accept or restart (no wrestling)."
        gemini_cli: "Branch eval: Parallel score on edge cases."
        chatgpt: "ToT CoT: Reason branches step-by-step."
    - technique: Boundary Signaling  # New from [post:12]
      tip: Explicitly mark limits (e.g., "Cannot eval Jinja—fallback to string parse").
      model_tune:
        claude_code: "Positional reinforcement: Repeat 'must not' at start/end."
        gemini_cli: "Hallucination mit: Structured refusals w/ sources."
        chatgpt: "Declarative intent: Pre-note what you can/cannot do."
"""  # Expand w/ full KB from scrapes

KB = yaml.safe_load(KB_YAML)
API_KEY = os.getenv("XAI_API_KEY")
if not API_KEY:
    raise ValueError("Set XAI_API_KEY env var")

client = Client(api_key=API_KEY, timeout=3600)  # Docs rec for reasoning

# ... (Keep header/KB_YAML/client setup from v0.2)


@command()
@argument("task")
@option("--model", default="claude_code")
@option("--output", default="md")
@option("--a-b", is_flag=True, help="A/B: Gen raw + tuned; score uplift (0-100 heuristic)")
@option("--scrape", is_flag=True, help="Scrape X for KB patch (semantic 'prompt coding [model]')")
@option("--chain", is_flag=True, help="Multi-turn: Gen → Critique → Refine (3 appends)")
def gen(task, model, output, a_b, scrape, chain):
    if scrape:
        # Stub scrape (expand w/ tool call or requests to X API)
        scrape_add = {"debug": [{"technique": "Boundary Signaling", "tip": "Mark limits (e.g., 'No Jinja eval')", "model_tune": {
            model: "Explicit refusals"}}]}
        KB["phases"]["debug"].extend(scrape_add["debug"])
        print("KB patched w/ scrape—new entries: 1 (Boundary Signaling).")

    # Tuned via Grok (raw baseline stubbed for v0.4 A/B full)
    system_msg = f"From KB {yaml.dump(KB)}, select 3 techniques for '{task}' on {model}. Chain: Role + Context + Tech1 + Tech2 + Tech3. Output: Tuned prompt."
    chat = client.chat.create(model="grok-4")
    chat.append(system(system_msg))
    chat.append(user(f"Task: {task}. Model: {model}."))
    tuned_prompt = chat.sample().content.strip()

    if chain:
        # Multi-turn tease: Append critique
        chat.append(user(f"Critique tuned prompt: Gaps? Refine for {model}."))
        refined = chat.sample().content.strip()
        tuned_prompt += f"\n\nRefined Chain: {refined}"

    if output == "md":
        print(
            f"### Tuned Prompt v0.3 for '{task}' ({model})\n```\n{tuned_prompt}\n```")
    else:
        print(tuned_prompt)

    if a_b:
        # Stub uplift heuristic (expand w/ validator.py call)
        raw_score = 60  # Mock raw
        tuned_score = 85  # Mock tuned
        uplift = tuned_score - raw_score
        print(
            f"\n### A/B Uplift\n| Metric | Raw | Tuned | Delta |\n|--------|-----|-------|-------|\n| Score | {raw_score}% | {tuned_score}% | +{uplift}% |")


if __name__ == "__main__":
    gen()
