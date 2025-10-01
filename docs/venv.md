# Setting Up a Python Virtual Environment (venv)

A virtual environment (venv) helps isolate project dependencies and ensures reproducible builds. Follow these steps to set up and activate a venv for this workspace:

## 1. Create a Virtual Environment

Open a terminal in the project root and run:

```
python -m venv .venv
```

This creates a `.venv` folder containing the isolated Python environment.

## 2. Activate the Virtual Environment

- **Windows (PowerShell):**
  ```
  .venv\Scripts\Activate.ps1
  ```
- **Windows (Command Prompt):**
  ```
  .venv\Scripts\activate.bat
  ```
- **macOS/Linux:**
  ```
  source .venv/bin/activate
  ```

## 3. Install Project Dependencies

Once activated, install required packages:

```
pip install -r requirements.txt
```

## 4. Deactivate the Environment

To exit the venv, run:

```
deactivate
```

---

**Tip:** Always activate the venv before running or developing the project to avoid dependency conflicts.
