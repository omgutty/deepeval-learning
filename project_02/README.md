# project_02 — Deepeval Learning Setup

Learning project for [DeepEval](https://github.com/confident-ai/deepeval) using `uv` for Python environment and package management.

**Environment:** Windows + PowerShell · uv 0.12.3 · Python 3.13.14

---

## Setup commands (in order of execution)

### 1. Create the virtual environment

```powershell
uv venv
```

| | |
|---|---|
| **What it does** | Creates a virtual environment (`.venv/` folder) in the current directory, isolated from your system Python. It uses uv's managed Python 3.13, so no separate Python install is needed. |
| **Why we ran it** | Every project should have its own isolated environment so packages installed here never clash with other projects or the system Python. |

### 2. Activate the environment

```powershell
.venv\Scripts\activate
```

| | |
|---|---|
| **What it does** | "Turns on" the venv for the current PowerShell session — the prompt changes to `(project_02) PS ...`, and now `python`/`pip`/installed packages point into `.venv`. |
| **Why we ran it** | Commands after this install and run packages inside this project's venv, not globally. |

> **Note:** We first tried `uv shell` (uv's shortcut for activation), but this uv version no longer has that subcommand (`error: unrecognized subcommand 'shell'`). On Windows, activate directly with the script above.

### 3. Install the DeepEval package

```powershell
uv pip install deepeval
```

| | |
|---|---|
| **What it does** | Resolves and installs `deepeval` **plus all its dependencies** (67 packages in our case) into the active venv, using uv's fast resolver instead of `pip`. |
| **Why we ran it** | DeepEval is the library we're learning to use. Note: plain `pip` is **not available** inside a uv-created venv, so you must use `uv pip install` (or `uv add` once a `pyproject.toml` exists). There is also **no need** to run `pip install --upgrade pip` — uv manages its own environment. |

---

## Everyday uv commands to remember

```powershell
# Run any command inside the venv without activating it first
uv run python myscript.py

# Add a package AND record it as a project dependency (needs uv init first)
uv init
uv add deepeval

# See what's installed
uv pip list
```

## Verify your setup

### Option 1 — After activating the venv (the command from sir)

```powershell
.venv\Scripts\activate
python -c "import deepeval, requests; print(deepeval.__version__, requests.__version__)"
```

**What it does, piece by piece:**
- `python -c "..."` → runs the Python code inside the quotes as a one-liner (no script file needed)
- `import deepeval, requests` → loads both libraries; raises `ModuleNotFoundError` if either is missing
- `print(deepeval.__version__, requests.__version__)` → prints both versions

Expected output (verified on this machine):

```
4.2.2 2.34.2
```

> **Important caveat:** this only works while the venv is **activated**, so `python` points to `.venv\Scripts\python.exe`. In a fresh terminal without activation, `python` is your system Python and the import will fail — even though deepeval is installed. Check with `where python` if unsure.

### Option 2 — Direct path to the venv's Python (no activation needed)

```powershell
.venv\Scripts\python.exe -c "import deepeval, requests; print(deepeval.__version__, requests.__version__)"
```

### Option 3 — Via uv (uv's own runner, no activation needed)

```powershell
uv run python -c "import deepeval; print(deepeval.__version__)"
```

---

## Run your first test

```powershell
deepeval test run test_01_Ans_Relevency.py
```

| | |
|---|---|
| **What it does** | Runs pytest on the test file and evaluates the `LLMTestCase` against the metric (`AnswerRelevancyMetric`). Every metric is an **LLM-as-a-judge**: deepeval asks an LLM to grade the output, so an API key + provider must be configured (see below). |
| **Why we ran it** | This is the standard way to run deepeval tests. It prints a results table with per-metric score, pass/fail status (threshold), the judge model used, and the LLM's reason. |

Expected result (verified on this machine): the test **passes** — Answer Relevancy scored **1.0** against a **0.9 threshold**, judged by `openai/gpt-5.4` served through **OpenRouter**.

> **Cosmetic warnings you can ignore:** the `portalocker` "Shared locks on Windows" message and the PostHog telemetry SSL error happen after the test finishes and do not affect results. Silence them with `uv pip install "portalocker[win32]"` and `DEEPEVAL_TELEMETRY_OPT_OUT=true`.

---

## Configuring the LLM provider (API keys)

DeepEval does **not** read `pip install`-style global config — it reads **environment variables**, and it loads them automatically from a `.env` file in the project folder. So: no manual `export` needed; just keep the variables in `.env`.

### This project: OpenRouter

OpenRouter is an OpenAI-compatible gateway that lets you call many models with one API key. Copy `.env.example` to `.env` and fill in your key:

| Variable | Meaning |
|---|---|
| `USE_OPENROUTER_MODEL=true` | **Opts into** OpenRouter as the active provider. Without an explicit provider choice deepeval falls back to OpenAI. |
| `OPENROUTER_API_KEY=sk-or-...` | Your OpenRouter key (note the exact name — `OPEN_ROUTER_API_KEY` with an extra underscore is NOT read and silently ignored). |
| `OPENROUTER_MODEL_NAME=` | Optional. Leave empty to use deepeval's default (see below). |

> **Why the error said "OpenAI API key is not configured":** the metric needs *an* LLM, and OpenAI is deepeval's built-in **fallback provider**. Because we hadn't opted into any provider (and the key name in `.env` was wrong), deepeval fell back to OpenAI and demanded `OPENAI_API_KEY`.

### Default judge model (nothing configured)

- **Provider fallback:** if no `USE_*_MODEL` flag is set → **OpenAI**, and it will fail unless `OPENAI_API_KEY` exists.
- **With OpenRouter selected** but no `OPENROUTER_MODEL_NAME` → the default judge model is **`openai/gpt-5.4`** (routed through OpenRouter). You can override with any model id OpenRouter supports, e.g. `OPENROUTER_MODEL_NAME=anthropic/claude-opus-5`.

To use OpenAI instead of OpenRouter, your `.env` would contain `USE_OPENAI_MODEL=true` + `OPENAI_API_KEY=sk-...` instead.
