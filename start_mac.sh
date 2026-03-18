#!/bin/zsh
# Start script for PyQt5 app on macOS with correct Qt plugin path


# Set Qt plugin path to venv PyQt5 plugins (auto-detect Python version)
PYVER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
export QT_QPA_PLATFORM_PLUGIN_PATH="$(pwd)/.venv/lib/python${PYVER}/site-packages/PyQt5/Qt5/plugins/platforms"


# Activate venv
source .venv/bin/activate

# Start the Python app from venv
python main.py
