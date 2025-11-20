# ComsoleLauncher

**Simple GUI for managing and running COMSOL Multiphysics simulations with Python**

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey.svg)

---

## Quick Start (60 Seconds!)

### 1. Run the Installer

**Windows:**
```bash
WIN_run.bat
```

**Mac/Linux:**
```bash
./MAC_run.sh
```

The installer will:
- Check for Python 3.13 and Java JDK
- Create a virtual environment
- Install dependencies (JPype1, MPh, NumPy)
- Launch the application

### 2. Add Your Files

Put your `.mph` files in the `comsol_projects` folder.

### 3. Run Simulations

- Click a project card
- Click **"▶ Quick Run"**
- Done! Results saved as `yourfile_result.mph`

---

## Features

### 🎯 Quick Run
One-click simulation execution. No configuration needed.

### 🔧 Advanced Mode
- Connect to COMSOL server
- Edit parameters interactively
- Run simulations with live feedback

### 🔍 Inspect & Edit (No COMSOL Required!)
- View `.mph` file contents
- Edit parameters directly
- Save modified files
- **Works without COMSOL installed!**

### 📄 Launcher Generator
Creates standalone scripts for your simulations:
- `run.py` - Python script
- `run.sh` - Mac/Linux script
- `run.bat` - Windows script

---

## Requirements

### Required
- **Python 3.13** - [Download](https://www.python.org/downloads/)
- **Java JDK 17+** - [Download](https://adoptium.net/)
- **COMSOL Multiphysics** - (optional, only needed for running simulations)

### Dependencies (Auto-installed)
- JPype1 1.6.0 (Java-Python bridge)
- MPh 1.2+ (COMSOL Python interface)
- NumPy 1.20+ (Numerical computing)

---

## Manual Installation

If you prefer manual setup:

```bash
# Create virtual environment
python3.13 -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install mph numpy

# Run
python launcher.py
```

---

## Project Structure

```
ComsoleLauncher/
├── WIN_run.bat          # Windows installer
├── MAC_run.sh           # Mac/Linux installer
├── launcher.py          # Main launcher (handles setup)
├── comsol_manager.py    # Application entry point
├── requirements.txt     # Python dependencies
├── wheels/              # Pre-built JPype1 wheel for Windows Python 3.13
│   └── jpype1-1.6.0-cp313-cp313-win_amd64.whl
├── ui/                  # UI components
├── core/                # Core functionality
├── features/            # Feature modules
├── utils/               # Utility functions
└── comsol_projects/     # Put your .mph files here
```

---

## Troubleshooting

### "Python 3.13 not found"
- Install Python 3.13 from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation
- Restart your terminal/computer

### "Java JDK not found"
- Install Temurin JDK 17 from [adoptium.net](https://adoptium.net/)
- Restart your computer after installation

### "No .mph files found"
- Place your `.mph` files in the `comsol_projects` folder
- Click the **Refresh** button

### "Cannot connect to COMSOL"
- Use **"Inspect & Edit"** mode instead (doesn't require COMSOL)
- Make sure COMSOL is installed if you need to run simulations

---

## License

MIT License - See LICENSE file for details

---

## Credits

- Built with [MPh](https://mph.readthedocs.io/) - COMSOL Python interface
- Uses [JPype1](https://github.com/jpype-project/jpype) - Java-Python bridge
- Powered by Python and tkinter

---

**Enjoy! 🚀**
