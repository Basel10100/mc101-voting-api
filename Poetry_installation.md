# Poetry Installation Guide

This guide explains how to **install Poetry** — the Python dependency management and packaging tool — on **Windows**, **macOS**, and **Linux**.

---

## 1. Install Poetry on Windows

### **Option A — Recommended (Official Installer)**
Run this in **PowerShell**:

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

After installation, make sure Poetry is added to your PATH. The installer usually places Poetry in:

```
%APPDATA%\Python\Scripts
```

Verify installation:

```powershell
poetry --version
```

---

### **Option B — Using pip (Not Recommended)**
```powershell
pip install poetry
```

> ⚠️ **Note:** Using pip for Poetry may cause conflicts. Use only if the official installer fails.

---

## 2. Install Poetry on macOS

### **Option A — Recommended (Official Installer)**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Poetry will be installed in:

```
$HOME/.local/bin
```

If Poetry isn't found, add it to your PATH:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Verify installation:

```bash
poetry --version
```

---

### **Option B — Using Homebrew**
```bash
brew install poetry
```

> ⚠️ **Note:** Homebrew versions may lag behind the latest release.

---

## 3. Install Poetry on Linux

### **Option A — Recommended (Official Installer)**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Add Poetry to your PATH if needed:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

To make the change permanent:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Verify installation:

```bash
poetry --version
```

---

### **Option B — Using pipx (Recommended Alternative)**
```bash
pipx install poetry
```

---

## 4. Verify Installation
After installation on any platform, confirm with:

```bash
poetry --version
```

---

## 5. Upgrade Poetry
To update Poetry to the latest version:

```bash
poetry self update
```

---

## 6. Quick Summary Table

| Platform    | Recommended Command | Alternative |
|------------|----------------------|------------|
| **Windows** | `(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -` | `pip install poetry` |
| **macOS**   | `curl -sSL https://install.python-poetry.org | python3 -` | `brew install poetry` |
| **Linux**   | `curl -sSL https://install.python-poetry.org | python3 -` | `pipx install poetry` |

---

**Official Documentation:** [https://python-poetry.org/docs/](https://python-poetry.org/docs/)
