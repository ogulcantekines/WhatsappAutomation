# WhatsApp Automation Tool

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A professional-grade terminal-based automation tool for WhatsApp. Send messages to individuals or groups directly from the CLI.

## Key Features
- **Personal & Group Messaging**: Send to a phone number or a WhatsApp group via invite link or group ID.
- **Interactive CLI**: Mode selection and dynamic input when no flags are provided.
- **Configurable Wait Time**: `-w/--wait-time` controls how long the tool waits before sending.
- **Clean Exit**: Automated browser tab management after sending.
- **Cross-Platform**: Designed to work across **Windows**, **Fedora**, **Ubuntu**, and **Arch Linux** (browser required).

## Installation

```bash
# Clone the repository
git clone https://github.com/ogulcantekines/WhatsappAutomation.git

# Navigate to project directory
cd WhatsappAutomation

# Setup Virtual Environment
# For Linux/macOS:
python3 -m venv venv
source venv/bin/activate

# For Windows:
python -m venv venv
venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt
```

## Usage

*before usage you must have logged your whatsapp web account in your default browser!!

Interactive mode (prompts for mode, target, and message):
```bash
python main.py
```

Send to a personal number:
```bash
python main.py -n "+905551234567" -m "Hello!" -w 30
```

Send to a WhatsApp group (via invite link or group ID):
```bash
python main.py -g "https://chat.whatsapp.com/XXXXXXXXXXXXXXX" -m "Hello group!"
python main.py -g "XXXXXXXXXXXXXXX" -m "Hello group!"
```

Available flags:
- `-n` / `--number`: Target phone number (with country code, e.g. `+905551234567`)
- `-g` / `--group`: WhatsApp group ID or invite link (`https://chat.whatsapp.com/...`)
- `-m` / `--message`: Message text
- `-w` / `--wait-time`: Seconds to wait before sending (default: `25`, minimum: `5` for personal, `25` for group)

## Troubleshooting (Linux/Fedora/Arch)
If you encounter display or permission errors, try the following:

### 1. X11 Display Error
If you see `Xlib.error.DisplayConnectionError`, run this command in your terminal:
```bash
xhost +local:$(whoami)
```

### 2. Missing Tkinter/Development Headers
If the script complains about `tkinter` or `MouseInfo`, install the following:

*(For Ubuntu: `sudo apt-get install python3-tk python3-dev`)*
*(For Fedora: `sudo dnf install python3-tk python3-devel`)*
*(For Arch Linux: `sudo pacman -S tk`)*

## Roadmap
- [ ] Multi-contact support (comma-separated numbers)
- [ ] Scheduled messaging for future dates
- [ ] Advanced logging and history viewer
- [x] Group messaging support via invite link or group ID
- [x] Professional CLI with banners and colors (Rich + argparse)

## License
Distributed under the MIT License. See `LICENSE.md` for more information.
