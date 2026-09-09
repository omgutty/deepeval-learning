# DeepEval Learning — project_01

Learning project for [DeepEval](https://deepeval.com/docs/getting-started) — an open-source
LLM evaluation framework (pytest-native evals for LLM apps/agents/RAG).

This project is deliberately **separate** from the other learning repos
(Python, CrewAI, etc.). It uses its own `uv` virtual environment and its own git repo.

## Environment

| Tool | Version / value | Notes |
|------|-----------------|-------|
| OS | Windows | PowerShell terminal |
| uv | 0.12.3 | Python + env manager |
| Python | 3.13 (managed by uv) | DeepEval needs Python >= 3.9 |
| DeepEval | 4.2.1 | Installed in `.venv` |
| Judge LLM provider | OpenRouter | `OPENROUTER_*` env vars, see `.env` |
| git identity | omgutty <om.gutty@gmail.com> | global config |

---

## Setup commands used (in order)

All commands below were run inside this folder
(`D:\Projects\deepeval-learning\project_01`) in a PowerShell terminal.

### 1. Verify prerequisites

```powershell
uv --version                 # uv 0.12.3
uv python list               # shows installed + downloadable Pythons
git --version                # git 2.55.0
```

### 2. Create the virtual environment

```powershell
uv venv .venv --python 3.13
```

> Note: `--python 3.12` initially failed with a network error because uv tried to
> download CPython 3.12. Since **3.13 was already installed locally** (no download
> needed), `.venv` was created with 3.13 instead.

### 3. Activate the environment

PowerShell (current terminal only):

```powershell
.venv\Scripts\Activate.ps1
```

Your prompt shows `(.venv)`. If the execution policy blocks scripts, run once:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

Deactivate with `deactivate`.

### 4. Install DeepEval

```powershell
uv pip install -U deepeval
deepeval --version           # 4.2.1
```

`uv pip` installs into the active `.venv`; no separate `pip` / `virtualenv` /
`python3 -m venv` needed, and no `requests` package (DeepEval pulls its own
HTTP stack).

---

## Remaining manual steps (not yet done)

### A. Add your real OpenRouter API key

1. Create a key at <https://openrouter.ai/settings/keys>.
2. Open `.env` (already created, gitignored) and replace the placeholder:

   ```env
   OPENROUTER_API_KEY=sk-or-v1-paste-your-real-key-here
   ```

   The other two variables are already set:

   ```env
   USE_OPENROUTER_MODEL=1
   OPENROUTER_MODEL_NAME=openai/gpt-4.1
   ```

   - `USE_OPENROUTER_MODEL=1` makes OpenRouter the default judge for all
     LLM-as-a-judge metrics.
   - `OPENROUTER_MODEL_NAME` picks the scoring model (any slug from
     <https://openrouter.ai/models>).
   - DeepEval autoloads `.env` at import time (precedence: process env > `.env.local`
     > `.env`). After editing `.env`, start a new terminal or re-activate so the
     process picks it up.

### B. Create your first eval test

Create `test_example.py` in this folder:

```python
from deepeval import assert_test
from deepeval.test_case import LLMTestCase, SingleTurnParams
from deepeval.metrics import GEval

def test_correctness():
    correctness_metric = GEval(
        name="Correctness",
        criteria="Determine if the 'actual output' is correct based on the 'expected output'.",
        evaluation_params=[SingleTurnParams.ACTUAL_OUTPUT, SingleTurnParams.EXPECTED_OUTPUT],
        threshold=0.5,
    )
    test_case = LLMTestCase(
        input="I have a persistent cough and fever. Should I be worried?",
        actual_output="A persistent cough and fever could be a viral infection or something more serious. See a doctor if symptoms worsen or don't improve in a few days.",
        expected_output="A persistent cough and fever could indicate a range of illnesses, from a mild viral infection to more serious conditions like pneumonia or COVID-19. You should seek medical attention if your symptoms worsen, persist for more than a few days, or are accompanied by difficulty breathing, chest pain, or other concerning signs.",
    )
    assert_test(test_case, [correctness_metric])
```

### C. Run the test

```powershell
deepeval test run test_example.py
```

Expected: a 0–1 score, PASS/FAIL against the 0.5 threshold, and the judge's reasoning.

---

## Git / GitHub

This repo is **not yet committed** — the scaffold files were just created. To finish:

```powershell
git init
git add -A
git commit -m "chore: scaffold deepeval-learning project_01 (README, gitignore, env example)"
git branch -M main
gh repo create deepeval-learning-project_01 --public --source=. --remote=origin --push
```

> `gh` (GitHub CLI) is installed and authenticated as **omgutty**. `.env` and
> `.venv/` are ignored, so the API key is **not** pushed. The command above creates a
> **public** repo; use `--private` instead if you prefer.

Verify the secret was not committed:

```powershell
git status
git ls-files
```

`.env` must **not** appear in `git ls-files`.

---

## Cheat sheet

| Goal | Command |
|------|---------|
| Create the venv | `uv venv .venv --python 3.13` |
| Activate | `.venv\Scripts\Activate.ps1` |
| Install/upgrade DeepEval | `uv pip install -U deepeval` |
| Check version | `deepeval --version` |
| Run an eval test | `deepeval test run test_example.py` |
| Provider env vars | see `.env` / `.env.example` |
| Useful docs | <https://deepeval.com/docs/getting-started> |

## What I am learning / next steps

- LLM-as-a-judge metrics (GEval, AnswerRelevancy, Hallucination, Faithfulness, …).
- `LLMTestCase` and `assert_test`.
- Running evals as pytest-style tests via `deepeval test run`.
- Comparing LLM outputs against expected outputs with a configurable judge model.
- Later: datasets, metrics catalog, tracing/agents, Confident AI (optional cloud
  dashboard via `deepeval login`).
