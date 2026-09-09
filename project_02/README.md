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
