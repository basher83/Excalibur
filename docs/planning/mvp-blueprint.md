# MVP Blueprint: "Prompt Excalibur" v0.1 (3-Phase Sprint, <1 Hour to POC)
We'll bootstrap a Python CLI: X semantic scrape → KB consolidate → Tuned prompt gen. Use Grok API for core chaining (e.g., semantic search + CoT tuning). No bloat—modular, testable, Ruff-ready. Tools: Your env + xAI API (Grok-4.1 for the heavy lifting).

| Phase | Goal | Steps | Est. Time | Output |
|-------|------|-------|-----------|--------|
| **1: KB Bootstrap (Scrape & Consolidate)** | Seed the brain trust w/ 20-30 techniques from X/web. | 1. Semantic search X for "prompt engineering coding" (limit 20, from @godofprompt/@karpathy/etc.).<br>2. Web search "best prompting techniques for Claude Code 2025" (num=10).<br>3. Code stub: Parse to YAML KB (phase/task/technique/tip/model-tune). | 10 mins | `kb.yaml` w/ ~25 entries (e.g., "Debug: Self-Verif Loop + Confidence Score"). |
| **2: Pipeline Core (Task → Tuned Prompt)** | Input task/model → Select 3 techniques → Chain prompt. | 1. Grok API call: "From KB [paste snippet], select 3 for [task: Debug ArgoCD loop] on [model: Claude Code]. Chain: Role + Context + Tech1 + Tech2 + Confidence."<br>2. Code: YAML loader + API wrapper (requests + json).<br>3. CLI: `excalibur gen "refactor auth" --model claude --output md`. | 20 mins | Runnable `excalibur.py` (UV script, <200 lines). Test: Gen prompt for "idempotency fix in ceph.yml". |
| **3: Test & Iterate (Verify Uplift)** | Run A/B on sample code; tune KB. | 1. Mock task: Feed gen prompt to Claude/Gemini; score output (e.g., manual PASS on structure).<br>2. Grok refine: "Critique this prompt output [paste]; suggest KB add (e.g., 'Few-Shot YAML')."<br>3. Git commit; add --calibrate flag for self-tune. | 15 mins | Baseline scores table (e.g., | Task | Raw Prompt | Excalibur | Uplift |). |

### Kickoff Code Stub (Copy-Paste to Your Env)
Fire this in a new `excalibur.py`—UV-ready, Grok API stubbed (swap your key). Run `uv run excalibur.py --help` to test.

```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests>=2.31", "pyyaml>=6.0", "click>=8.1"]
# ///

import yaml
import requests
import click
import os

# Stub KB (expand w/ scrapes)
KB = yaml.safe_load("""
phases:
  planning:
    - technique: Metacognitive Scaffolding
      tip: List 3 assumptions + edges pre-gen.
      model_tune:
        claude: "Use tools for edge sims."
        gemini: "Visualize edges in diagram."
""")  # Paste full from our table

API_KEY = os.getenv("XAI_API_KEY")  # Set this!
GROK_URL = "https://api.x.ai/v1/chat/completions"  # From docs

@click.group()
def cli():
    pass

@cli.command()
@click.argument("task")
@click.option("--model", default="claude")
@click.option("--output", default="md")
def gen(task, model, output):
    prompt = f"From KB {yaml.dump(KB)}, select 3 techniques for '{task}' on {model}. Chain: Role (senior eng) + Technique1 + Technique2 + Confidence score. Output: Tuned prompt."
    resp = requests.post(GROK_URL, json={"model": "grok-4.1", "messages": [{"role": "user", "content": prompt}], "max_tokens": 500}, headers={"Authorization": f"Bearer {API_KEY}"}).json()
    tuned = resp["choices"][0]["message"]["content"]
    if output == "md":
        click.echo(f"### Tuned Prompt for '{task}' ({model})\n```\n{prompt}\n```\n**Output:** {tuned}")
    else:
        click.echo(tuned)

if __name__ == "__main__":
    cli()
```

**Run Test:** `export XAI_API_KEY=your_key; uv run excalibur.py gen "Debug Python loop in ArgoCD" --model claude --output md`. Boom—tuned prompt out.

