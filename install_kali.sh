#!/bin/bash
# Installer für das Spyware Framework auf Kali Linux
set -e

# System-Updates und Abhängigkeiten
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-pyqt5 nmap git

# Projekt klonen (falls nicht vorhanden)
if [ ! -d "spyware_framework" ]; then
    git clone https://github.com/MA-Medienagentur/spyware_kali.git spyware_framework
fi
cd spyware_framework

# Virtuelle Umgebung anlegen
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install PyQt5 requests python-nmap

# Startskript erzeugen
cat <<EOF > start_kali.sh
#!/bin/bash
source .venv/bin/activate
python3 main.py
EOF
chmod +x start_kali.sh

# Hinweis
clear
echo "Installation abgeschlossen! Starte das Framework mit:"
echo "cd spyware_framework && ./start_kali.sh"
