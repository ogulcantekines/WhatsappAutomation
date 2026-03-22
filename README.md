# WhatsApp Automation Tool

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A professional-grade terminal-based automation tool for WhatsApp. Designed for simplicity, speed, and efficiency.

## Key Features
- **Interactive CLI**: Dynamic input for phone numbers and messages.
- **Smart Delays**: Built-in timers to simulate human interaction and reduce ban risk.
- **Clean Exit**: Automated browser tab management for memory efficiency.
- **Cross-Platform**: Fully compatible with **Windows**, **Fedora**, **Ubuntu**, and **Arch Linux**.

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

Simply run the script and follow the on-screen instructions:
```bash
python main.py
```

## Troubleshooting (Linux/Fedora/Arch)
If you encounter display or permission errors, try the following:

### 1. X11 Display Error
If you see `Xlib.error.DisplayConnectionError`, run this command in your terminal:
```bash
xhost +local:$(whoami)
```

### 2. Missing Tkinter/Development Headers
If the script complains about `tkinter` or `MouseInfo`, install the following

*(For Ubuntu: `sudo apt-get install python3-tk python3-dev`)*
*(For Fedora: `sudo dnf install python3-tk python3-dev`)*
*(For Arch Linux: `sudo pacman -S python3-tk python3-dev`)*

## Roadmap
- [ ] Multi-contact support (Comma-separated numbers)
- [ ] Scheduled messaging for future dates
- [ ] Advanced logging and error handling
- [ ] Professional CLI with Banners and Colors (rich/argparse support)

## License
Distributed under the MIT License. See `LICENSE` for more information.
