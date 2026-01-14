# Python Version Guide

## ⚠️ Important: Python 3.11+ Required

This project **requires Python 3.11 or higher** because the `mcp-use` library uses modern Python features.

## Quick Check

```bash
python --version
# or
python3 --version
```

You need to see **Python 3.11.x** or higher (3.12, 3.13, etc.)

---

## Easy Launch (Recommended)

We've created launcher scripts that automatically use the correct Python version:

### macOS/Linux:
```bash
./start.sh
```

### Windows:
```bash
start.bat
```

These scripts will:
- ✅ Find Python 3.11+ automatically
- ✅ Check dependencies
- ✅ Launch the application

---

## If You Have Python 3.9 or 3.10

Your system might have an older Python as default. Here's how to install Python 3.11+:

### macOS (Homebrew):
```bash
brew install python@3.11

# Then use explicitly:
python3.11 run.py
```

### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3.11 python3.11-pip python3.11-venv

# Then use explicitly:
python3.11 run.py
```

### Windows:
1. Download Python 3.11+ from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Run `python --version` to verify

### Using pyenv (Cross-Platform):
```bash
# Install pyenv first (see https://github.com/pyenv/pyenv)
pyenv install 3.11.14
pyenv local 3.11.14

# Now python points to 3.11
python --version
```

---

## Manual Launch with Specific Python Version

If you have Python 3.11+ installed but it's not the default:

```bash
# Find your Python 3.11 installation
which python3.11
# or
which python3.12

# Install dependencies
python3.11 -m pip install -r requirements.txt

# Run the application
python3.11 run.py
```

---

## Virtual Environment (Recommended for Development)

Create an isolated environment with Python 3.11+:

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
python run.py

# Deactivate when done
deactivate
```

---

## Troubleshooting

### "No module named 'mcp_use'"

**Problem:** You're using Python 3.9 or 3.10

**Solution:** Use Python 3.11+ (see installation steps above)

### "python: command not found"

**Problem:** Python not in PATH

**Solution:**
```bash
# macOS/Linux: Use full path
/usr/local/bin/python3.11 run.py

# Windows: Reinstall Python and check "Add to PATH"
```

### Multiple Python Versions Installed

**Find all Python installations:**
```bash
# macOS/Linux
which -a python python3 python3.11 python3.12

# Check each version
python3.11 --version
python3.12 --version
```

**Use the right one:**
```bash
# Example: Use Python 3.11 specifically
python3.11 -m pip install -r requirements.txt
python3.11 run.py
```

---

## Why Python 3.11+?

The `mcp-use` library requires Python 3.11+ because it uses:
- Modern type hints (`TypedDict`, `Self`)
- Improved async/await features
- Better performance optimizations
- Structural pattern matching

---

## Quick Reference

| Task | Command |
|------|---------|
| **Check Python version** | `python --version` |
| **Install deps (specific version)** | `python3.11 -m pip install -r requirements.txt` |
| **Run with specific version** | `python3.11 run.py` |
| **Use launcher script** | `./start.sh` (macOS/Linux) or `start.bat` (Windows) |
| **Create venv** | `python3.11 -m venv venv` |
| **Activate venv** | `source venv/bin/activate` (macOS/Linux) |

---

## Still Having Issues?

1. Check [GETTING_STARTED.md](GETTING_STARTED.md) for setup instructions
2. Verify you have Python 3.11+ installed: `python3.11 --version`
3. Use the launcher scripts: `./start.sh`
4. Create a virtual environment with Python 3.11+
5. Open an issue: https://github.com/majidraza1228/mcp-toolkit/issues

---

**TL;DR:** Use `./start.sh` (or `start.bat` on Windows) - it handles everything for you! 🚀
