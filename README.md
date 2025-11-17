# Comsol Project Manager

**Simple GUI for managing and running Comsol Multiphysics simulations with Python**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey.svg)

---

## What Does It Do?

This tool lets you:
- ✨ Run Comsol simulations with one click
- 📝 Edit simulation parameters without opening Comsol
- 🔍 View and modify .mph files directly (no Comsol needed!)
- 📄 Generate standalone scripts for batch processing

---

## Quick Start (3 Steps!)

### 1. Install Requirements

**Windows:**
```bash
WIN_run.bat
```

**Mac/Linux:**
```bash
./MAC_run.sh
```

That's it! The launcher installs everything automatically.

### 2. Add Your Files

Put your `.mph` files in the `comsol_projects` folder.

### 3. Run!

The app opens automatically. Click a project, then click **Quick Run** ▶

---

## Features

### 🎯 Quick Run
One-click simulation execution. No configuration needed.

### 🔧 Advanced Mode
- Connect to Comsol server
- Edit parameters interactively
- Run simulations with live feedback

### 🔍 Inspect & Edit (No Comsol Required!)
- View .mph file contents
- Edit parameters directly
- Save modified files
- **Works without mph library or Comsol!**

### 📄 Launcher Generator
Creates standalone scripts for your simulations:
- `run_simulation.py` - Python script
- `run.sh` - Mac/Linux script
- `run.bat` - Windows script

---

## Installation

### Option 1: Automatic (Recommended)

**Windows:**
```bash
WIN_run.bat
```

**Mac/Linux:**
```bash
chmod +x MAC_run.sh
./MAC_run.sh
```

### Option 2: Manual

```bash
# Install dependencies
pip install mph numpy

# Run application
python comsol_manager.py
```

### Option 3: With UV (10-100x faster!)

```bash
# Install UV
pip install uv

# Run with UV
uv pip install mph numpy
uv run python comsol_manager.py
```

---

## Requirements

### Minimum (Inspect & Edit only):
- Python 3.8 or higher
- tkinter (usually included with Python)

### Full Features:
- Python 3.8+
- mph library: `pip install mph`
- Comsol Multiphysics installed
- Java Runtime (comes with Comsol)

---

## Usage Guide

### Running a Simulation

1. **Start the app**
   - Windows: Double-click `WIN_run.bat`
   - Mac/Linux: Run `./MAC_run.sh`

2. **Select a project**
   - Click on any project card

3. **Click "Quick Run" ▶**
   - Progress window shows status
   - Results saved automatically

### Editing Parameters

#### Method 1: Inspect & Edit (No Comsol needed!)

1. Select a project
2. Click **"🔍 Inspect & Edit"**
3. Go to **"Parameters"** tab
4. Double-click any parameter to edit
5. Click **"💾 Save Changes"**

#### Method 2: Advanced Mode (Requires Comsol)

1. Select a project
2. Click **"⚙️ Advanced"**
3. Click **"🔌 Connect"**
4. Click **"📋 Load Parameters"**
5. Double-click parameters to edit
6. Click **"▶ Run"**

### Creating Launcher Scripts

1. Select a project
2. Click **"📄 Create Launcher"**
3. Scripts created in project folder
4. Run anytime without the GUI!

---

## Project Structure

```
ComsoleLauncher/
├── WIN_run.bat              ← Windows launcher
├── MAC_run.sh               ← Mac/Linux launcher
├── comsol_manager.py        ← Main application
├── comsol_projects/         ← Put your .mph files here
├── ui/                      ← User interface modules
├── features/                ← Feature implementations
├── core/                    ← Core functionality
└── utils/                   ← Utility functions
```

---

## Troubleshooting

### "mph library not found"

**Solution:**
```bash
pip install mph
```
Or use the **"Install mph"** button in the app.

### "No .mph files found"

**Solution:**
Put your Comsol `.mph` files in the `comsol_projects` folder, then click **↻ Refresh**.

### "Comsol connection failed"

**Solutions:**
1. Make sure Comsol Multiphysics is installed
2. Check Java is available: `java -version`
3. Try restarting the application
4. Use **"Inspect & Edit"** mode instead (no Comsol needed)

### First run shows warnings

This is normal! Java/Comsol connection may show warnings on first run. The app will still work.

---

## Tips & Tricks

### 💡 Tip 1: Use Inspect & Edit for Quick Changes
No need to open Comsol just to change a parameter value!

### 💡 Tip 2: Generate Launchers for Batch Processing
Create scripts once, run anywhere - perfect for clusters.

### 💡 Tip 3: Install UV for Speed
UV is 10-100x faster than pip. Install with `pip install uv`.

### 💡 Tip 4: Organize with Subfolders
Use folders in `comsol_projects/` to organize by type:
```
comsol_projects/
├── thermal/
├── structural/
└── fluid/
```

---

## Example Workflow

### Scenario: Parameter Sweep

1. **Edit base model**
   - Click "🔍 Inspect & Edit"
   - Change parameter: `power = 10[W]`
   - Save as: `model_10W_modified.mph`

2. **Repeat for different values**
   - Edit: `power = 20[W]`, save as `model_20W_modified.mph`
   - Edit: `power = 30[W]`, save as `model_30W_modified.mph`

3. **Generate launchers**
   - Select each model
   - Click "📄 Create Launcher"

4. **Run batch**
   ```bash
   python model_10W/run_simulation.py
   python model_20W/run_simulation.py
   python model_30W/run_simulation.py
   ```

---

## Architecture

Modern modular design with separation of concerns:

- **ui/** - User interface components
- **features/** - Quick Run, Advanced Mode, Inspect & Edit
- **core/** - Project scanning and management
- **utils/** - File parsing, dependencies, utilities

Each module is ~100-400 lines for easy maintenance.

---

## FAQ

**Q: Do I need Comsol installed?**
A: Only for running simulations. "Inspect & Edit" works without Comsol!

**Q: Can I edit .mph files without the GUI?**
A: Yes! .mph files are ZIP archives. See `examples/` for code samples.

**Q: Does this work on remote servers?**
A: Yes! Use the launcher scripts or run in headless mode.

**Q: Can I automate this?**
A: Yes! Generate launchers, then schedule with cron/Task Scheduler.

**Q: What versions of Comsol are supported?**
A: Any version supported by the mph Python library (6.0+).

---

## Contributing

Contributions welcome! This project follows:
- PEP 8 style guide
- Type hints throughout
- Comprehensive docstrings
- Modular architecture

---

## License

MIT License - See LICENSE file for details

---

## Support

- **Issues:** Report bugs on GitHub Issues
- **Questions:** Check FAQ above
- **Examples:** See `examples/` folder for code samples

---

## Credits

Built with:
- Python tkinter for GUI
- mph library for Comsol integration
- UV for fast package management (optional)

---

**Made with ❤️ for scientists and engineers using Comsol Multiphysics**
