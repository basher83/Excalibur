# The Consolidated KB: Core Techniques for Coding Tasks

Pulled from X threads (e.g., @karpathy's "tight leash" rhythm for production code, @ericzakariasson's prompting/context loops) and repos (e.g., OpenAI Cookbook's reliability tricks). Categorized by coding phase—focus: Reliability over hype.

| Phase | Technique | Tip/Trick | X/Web Source |
|-------|-----------|-----------|--------------|
| **Planning** | Metacognitive Scaffolding | Pre-gen: List 3 assumptions + edges + 2-sentence approach. Catches bullshit early (e.g., "Assume no Jinja eval—edge: Nested loops?"). | @godofprompt [post:11]; OpenAI Cookbook  |
| **Planning** | Incremental Change Framing | Describe *one* concrete delta (e.g., "Add auth flow without breaking existing API"). Pros/cons 3 approaches first—no full rewrites. | @karpathy [post:10]; Anthropic Claude Code  |
| **Context** | Environment-Aware Onboarding | Stuff codebase (e.g., `files-to-prompt . --cxml`) + rules (style, tools access). For no-tools: "Manually run test, paste results." | @ericzakariasson [post:1]; PromptingGuide.ai Gemini  |
| **Execution** | Role + Constraint Stack | "Act as senior backend eng: Optimize for speed, not mem. Explain trade-offs." + Format: "JSON w/ comments." | @SwapAgarwal [post:18]; Lenny's Techniques  |
| **Execution** | Self-Verification Loop | "Write code → Run lint/test → Explain fixes." Delegate to agent if tools avail (e.g., Claude's terminal). | @ericzakariasson [post:1]; Vellum Claude Tips  |
| **Debug/Refine** | Error Explanation Chain | "Paste error + code: Explain why → Minimal fix (no breaks) → Test stub." Iterate drafts. | @SwapAgarwal [post:18]; Medium Confidence Trick  |
| **Debug/Refine** | Few-Shot + Critique | 2-3 examples (good/bad code) + "Critique this draft: Strengths/weaknesses." For logic: "Reason step-by-step before fix." | @freeCodeCamp [post:12]; Reddit "Only Prompt"  |
| **Output** | Structured Escapes | XML/JSON delimiters for input (e.g., <code>[snippet]</code>) + "Output: Markdown table of changes." | @viipin8 [post:5]; Abacus.AI Survey  |
| **Scale** | Parallel Scoped Agents | 2-3 agents: "Agent1: Refactor auth; Agent2: Test edge." No overlap—review PR-style. | @ericzakariasson [post:1]; HN Gemini CLI  |
| **Scale** | Confidence Scoring | End w/ "Confidence: 90%+? Explain gaps." Kills hallucinations. | @heynmodi [post:4]; Google Masterclass  |

## The Pipeline: Task → Tuned Prompt Factory

Rigged as a simple flow: Input your coding task (e.g., "Debug idempotency in CEPH OSD script") + model (Gemini CLI/Claude Code/ChatGPT) → Select 3-4 techniques (e.g., Metacognitive + Self-Verif + Confidence) → Output a chained prompt. Tuned per model: Gemini for multimodal (e.g., "Visualize YAML structure"); Claude for agentic (e.g., "Use tools for lint"); GPT for broad CoT.

**Stealable Pipeline Prompt (For Any Model):**  
"Task: [Your coding task, e.g., Refactor Python auth flow]. Model: [Gemini CLI].  
Select 3 techniques from KB: [Paste table above].  
Chain: Role (senior eng) + Context (stuff codebase rules) + Technique1 (e.g., Incremental: 3 approaches pros/cons) + Technique2 (Self-Verif: Write → Test → Fix) + Technique3 (Confidence score).  
Output: Tuned prompt template + Example run on task."

**Example Output (For "Debug Python loop in ArgoCD deploy" on Claude Code):**  
**Tuned Prompt:** "Act as senior DevOps eng specializing in K8s/ArgoCD. Context: Optimize for idempotency; excuse helm command if commented. Assumptions: Loop handles 10k+ JSON—edge: Empty arrays? Approach: Step-by-step: 1) Explain current loop flaws. 2) Propose 3 minimal fixes (pros/cons). 3) Draft code w/ tests. 4) Run lint (use tools). Confidence: 90%+? Explain. Output: JSON {flaws: [], fixes: [{code, test, conf}]}. Task: Debug this loop [paste code]."
