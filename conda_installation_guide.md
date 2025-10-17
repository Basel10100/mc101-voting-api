# Conda Installation Guide (Windows, macOS, Linux)

This guide explains how to **install Conda** — either **Miniconda** (lightweight) or **Anaconda** (full distribution) — on **Windows**, **macOS**, and **Linux**.

---

## **1. Choosing Between Miniconda and Anaconda**

| Feature      | **Miniconda** 🟢 | **Anaconda** 🔵 |
|------------|--------------------|-----------------|
| Size       | ~80 MB            | ~3 GB |
| Included Packages | Minimal, installs only `conda` + `pip` | Comes with 200+ scientific libraries |
| Flexibility | Install only what you need | Best if you want **everything pre-installed** |
| Recommended for | Developers who prefer a clean setup | Data science beginners |

For most users, **Miniconda** is recommended.

---

## **2. Install Conda on Windows**

### **Step 1 — Download the Installer**
- Go to the official Miniconda page:  
  [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
- Choose the **Windows** installer:
    - 64-bit `.exe`
    - Python 3.x version

### **Step 2 — Run the Installer**
1. Double-click the `.exe` file.
2. Select **"Just Me"** or **"All Users"**.
3. Choose the installation folder (default is fine).
4. Check **"Add Miniconda to PATH"** *(optional but recommended)*.
5. Finish installation.

### **Step 3 — Verify Installation**
Open **PowerShell** or **Command Prompt**:

```powershell
conda --version
```

You should see something like:

```
conda 24.7.1
```

---

## **3. Install Conda on macOS**

### **Step 1 — Download the Installer**
```bash
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
```

For Apple Silicon (M1/M2/M3 chips):

```bash
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
```

### **Step 2 — Run the Installer**
```bash
bash Miniconda3-latest-MacOSX-x86_64.sh
# or for Apple Silicon
bash Miniconda3-latest-MacOSX-arm64.sh
```

Follow the prompts and **accept the license**. When asked:

```
Do you wish the installer to initialize Miniconda? [yes|no]
```
Type `yes`.

### **Step 3 — Activate Conda**
```bash
source ~/.bashrc  # or source ~/.zshrc if using Zsh
```

### **Step 4 — Verify Installation**
```bash
conda --version
```

---

## **4. Install Conda on Linux**

### **Step 1 — Download the Installer**
```bash
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

### **Step 2 — Run the Installer**
```bash
bash Miniconda3-latest-Linux-x86_64.sh
```

Accept the license, choose an install location, and **initialize Conda** when prompted.

### **Step 3 — Activate Conda**
```bash
source ~/.bashrc
```

### **Step 4 — Verify Installation**
```bash
conda --version
```

---

## **5. Updating Conda**

After installation, always update Conda to the latest version:

```bash
conda update conda
```

---

## **6. Uninstalling Conda**

### On Windows:
- Open **Control Panel → Programs → Uninstall a program**.
- Select **Miniconda** or **Anaconda** → **Uninstall**.

### On macOS/Linux:
Remove the installation directory (example for Miniconda):

```bash
rm -rf ~/miniconda3
rm -rf ~/.conda
```

---

## **7. Verify Installation**

After installation on any OS:

```bash
conda info
```

Example output:

```
     active environment : base
    conda version : 24.7.1
    python version : 3.11.5
    base environment : /home/user/miniconda3
```

---

## **8. Useful Resources**
- Miniconda Downloads: [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
- Anaconda Downloads: [https://www.anaconda.com/download](https://www.anaconda.com/download)
- Conda Docs: [https://docs.conda.io/](https://docs.conda.io/)
