#!/bin/zsh
# Start script for PyQt5 app on macOS using Homebrew PyQt5 (system-wide, no venv)

# Deactivate venv if active
if [[ -n "$VIRTUAL_ENV" ]]; then
    deactivate
fi

# Set Qt plugin path to Homebrew Qt5
export QT_QPA_PLATFORM_PLUGIN_PATH="$(brew --prefix qt@5)/plugins/platforms"

# Start the Python app with system Python
python3 main.py
