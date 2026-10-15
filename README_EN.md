# AJZ Sentinel · AI Degradation Detector (ajz-sentinel)

[中文 README](README.md)

A **single-file, zero-dependency, fully browser-local** AI capability testing tool. Its positioning is a **capability-based model picker**: it helps everyday users answer "which model performs best on the tasks I actually need to do, at the best cost-performance" — rather than auditing service authenticity or serving as an authoritative academic benchmark.

- Ready out of the box: double-click `index.html` to run, nothing to install
- Privacy-safe: API keys live only in page memory; test history stays in the browser's localStorage and is never uploaded
- Verifiable question bank: 32 questions, including AIME 2026 problems, official ARC-AGI-2 evaluation tasks, and other questions from the past year, each with a labeled source

## Features

| Module | Description |
| --- | --- |
| Paper Builder | 33 profession presets + 5-dimension weight sliders (Logic / Instruction / Knowledge / Code / Multimodal), three tiers: Quick · Standard · Complete |
| Weight-driven assembly (v8) | Question counts in Quick/Standard tiers are allocated proportionally by dimension weights (largest-deficit first) instead of fixed counts; once a dimension's pool is exhausted, the remainder flows to other dimensions |
| Model presets (v8) | Built-in API formats for OpenAI / Claude / DeepSeek / Grok / Doubao / Qwen / Xiaomi MiMo / GLM / Kimi / Gemini; selecting one auto-fills the config, model name remains editable |
| Behavior probes | Thinking-trace detection, tool-list check, computation anchor (369) — auxiliary signals for server-side downgrades |
| Scoring engine | 9 scorers (numeric / strict match / JSON / grid / code-run / manual rubric / refusal probe, etc.), all executed locally |
| Benchmark scorecard | 15 benchmark-mapped rows scored item by item like mainstream model leaderboards, plus a composite index |
| History & trends (v8) | Auto-grouped by "host + model"; each group keeps its own baseline and trend chart; repeated tests of the same host+model are compared directly to catch intermittent substitution |
| Community cost-performance board (v8) | Zero-backend multi-user comparison: board data is hosted in this repo and pulled by the tool; submissions go through GitHub Issue + Action for automatic aggregation |
| Hot-swappable question bank | Load question JSON from a URL (e.g. this repo's `questions.json`), or paste JSON to import |

## Quick Start

### Option 1: Use locally
Download `index.html` and double-click to open it in a browser.

### Option 2: Deploy with GitHub Pages (recommended, free)

1. Fork this repo, or create a new repository and push these files to the `main` branch
2. Repo **Settings → Pages → Build and deployment**
3. Source: **Deploy from a branch**; Branch: **main / (root)**; save
4. Wait 1–2 minutes, then visit `https://<your-username>.github.io/<repo-name>/`

> GitHub Pages is pure static hosting, which exactly matches this tool's "all logic runs in the browser" architecture. It cannot run server code, so cross-user leaderboard aggregation goes through "Issue + GitHub Action" (see below) — no backend required.

### Point the tool at your repo

After deployment, fill in two URLs in the tool (replace `<user>/<repo>` with yours):

- **Question bank URL** (Paper Builder): `https://raw.githubusercontent.com/<user>/<repo>/main/questions.json`
- **Leaderboard JSON URL** (section 06, community board): `https://raw.githubusercontent.com/<user>/<repo>/main/community/leaderboard.json`

## Community Board Data Flow (zero backend)

```text
Your browser                          GitHub repo
──────────                          ──────────────────────────
Finish a test and save it
  ↓ "Generate my anonymous report"
Copy the sanitized JSON ──paste into──> the "Data Report" Issue
                              ↓ triggers
                          GitHub Action (scripts/aggregate.py)
                          validates schema → aggregates by host+model
                              ↓ auto-commits
                          community/leaderboard.json
                              ↓
Anyone's browser ←──"Pull leaderboard"── raw.githubusercontent.com
```

- Reports contain only: source **domain** (no path), model name, mode, total score, per-dimension scores, judged count, question count, timestamp
- They **never** contain API keys, full base URLs, answer text, or personal identifiers
- The aggregation script validates field ranges; non-compliant JSON is ignored

> You can also maintain the board manually: just edit `community/leaderboard.json` directly; see format `schema: ajz-board-v1`.

## Privacy & Security

- The API key is only used for requests initiated from the current page; it is not written to localStorage and never uploaded anywhere
- Test history lives in your browser; clearing browser data deletes it
- Reporting is a **manual copy-paste** action; the tool itself never sends any report

## Disclaimer

This tool is for personal capability assessment and model-selection reference. Questions and scorers come from public benchmarks and community question banks (sources are labeled in each question's `src` field). Scores are affected by prompts, sampling, and grading granularity. **This tool makes no evaluative claims about any model vendor and does not constitute procurement advice.**

## License

MIT — see [LICENSE](LICENSE). Copyright of individual questions belongs to their original benchmarks/authors (labeled in each question's `src` field).
