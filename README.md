# Luatools Plugin Installer

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Platform-Windows-lightgrey.svg" alt="Platform Support">
  <img src="https://img.shields.io/badge/Author-dominicsolanke-green.svg" alt="Author">
  <img src="https://img.shields.io/badge/Community-CHEATGLOBAL-red.svg" alt="Community">
</p>

A professional, multilingual installer designed to automatically set up **Luatools**, **Millennium**, and **Steamtools** plugins directly into your Steam directory. Powered by Python and clean console virtualization.

---

## 🚀 Features

- **Automated Dependency Setup**: Detects, downloads, and installs required core components (wsock32.dll, Python dependencies, Steamtools library, and Millennium framework).
- **Multilingual Support**: Fully localized in 5 languages:
  - 🇺🇸 English
  - 🇹🇷 Turkish
  - 🇧🇷 Portuguese
  - 🇪🇸 Spanish
  - 🇫🇷 French
- **Steam Lifecycle Management**: Gracefully stops and re-launches Steam during the configuration process to ensure all dll hooks attach correctly.
- **System Tweaks & Cleanups**: Automatically sweeps Steam beta flags, cleans local configuration conflicts (`steam.cfg`), and removes legacy `ForceX86` registry keys.
- **Easy Uninstallation**: Complete cleanup utility to completely remove all installed plugins and hooks, returning Steam back to its pristine default state.

---
<img width="1110" height="623" alt="image" src="https://github.com/user-attachments/assets/a9118e01-9e7f-405b-a7b2-d7ae6c4e9111" />

## 🛠️ How to Use

### Prerequisites
- Windows OS (7 / 8 / 10 / 11)
- [Python 3.8+](https://www.python.org/downloads/) installed on your path

### Running the Installer

1. Download the script file `luatools.py` to your system.
2. Open terminal (Command Prompt or PowerShell) inside the directory where the script is located.
3. Run the following command:
   ```bash
   python luatools.py
   ```
4. Choose an option from the menu:
   - `1`: Install Luatools and dependencies.
   - `2`: Uninstall all files and configurations.
   - `3`: Change the installer's active language dynamically.
   - `4`: Quit.

---

## 📂 Project Structure

- `install-plugin.py`: Core installation logic, ANSI terminal setup, translation dictionaries, registry lookup helper, process supervisor, and remote ZIP retrieval operations.
- `README.md`: Project documentation.

---

## ⚙️ Environment Variables

The installer supports configuration overrides through environment variables:
- `LT_DOWNLOAD_LINK`: Overrides the target plugin zip URL.
- `LT_PLUGIN_NAME`: Overrides the folder name where the plugin extracts.
- `LT_BRANCH`: Choose branch selection (`1` for default Luatools, `2` for steamtools-collection).
- `LT_CULTURE`: Overrides the auto-detected system language (e.g. `tr`, `en`, `es`, `fr`, `pt-BR`).

---

## 🤝 Community & Credits

- Created and maintained by **dominicsolanke**.
- Official Community: **[CHEATGLOBAL](https://cheatglobal.com)**
- Powered by the Millennium installer backend.

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE details for info.
