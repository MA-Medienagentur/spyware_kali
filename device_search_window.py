from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QPushButton, QLabel, QListWidget, QTextEdit

class DeviceSearchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerätesuche")
        self.setGeometry(200, 200, 600, 400)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.search_input = QLineEdit()
        self.search_types = QComboBox()
        self.search_types.addItems(["IP Address", "Phone Number", "MAC Address"])
        self.search_btn = QPushButton("Suchen")
        self.results_list = QListWidget()
        layout = QVBoxLayout()
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Suche nach:"))
        search_layout.addWidget(self.search_types)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        layout.addLayout(search_layout)
        layout.addWidget(self.results_list)
        layout.addWidget(self.output)
        self.setLayout(layout)
        self.search_btn.clicked.connect(self.search_target)
        self.results_list.itemClicked.connect(self.select_target)

    def search_target(self):
        import requests
        query = self.search_input.text()
        search_type = self.search_types.currentText()
        self.output.append(f"[+] Suche nach {search_type}: {query}")
        response = None
        if search_type == "Phone Number":
            clean_query = ''.join(c for c in query if c.isdigit())
            if len(clean_query) > 10:
                query = clean_query
            response = requests.get(f"https://phone-api.com/search?number={query}")
        elif search_type == "IP Address":
            if not query.strip():
                # Automatischer Netzwerkscan im Hintergrund-Thread
                import threading
                import subprocess
                import re
                def scan_network():
                    self.output.append("[+] Starte Netzwerkscan im lokalen Subnetz...")
                    try:
                        ip_route = subprocess.check_output(["ip", "route"], text=True)
                        match = re.search(r'(\d+\.\d+\.\d+\.\d+/\d+)', ip_route)
                        subnet = match.group(1) if match else "192.168.1.0/24"
                    except Exception:
                        subnet = "192.168.1.0/24"
                    self.output.append(f"[+] Scanne Subnetz: {subnet}")
                    try:
                        nmap_out = subprocess.check_output(["nmap", "-sn", subnet], text=True)
                        ips = re.findall(r'Nmap scan report for (\d+\.\d+\.\d+\.\d+)', nmap_out)
                        self.results_list.clear()
                        for ip in ips:
                            self.results_list.addItem(ip)
                        self.output.append(f"[+] {len(ips)} Geräte gefunden.")
                        # Nach Scan: Auswahl eines Geräts als Target durch Klick
                        def select_ip_target(item):
                            ip = item.text()
                            self.output.append(f"[+] Ziel ausgewählt: {ip}")
                            from main import show_main_window
                            self.main_window = show_main_window()
                            self.main_window.findChild(type(self)).ip_input.setText(ip)
                            self.close()
                        self.results_list.itemClicked.connect(select_ip_target)
                    except Exception as e:
                        self.output.append(f"[-] Netzwerkscan-Fehler: {str(e)}")
                threading.Thread(target=scan_network, daemon=True).start()
                return
            else:
                response = requests.get(f"https://ip-api.com/json/{query}")
        elif search_type == "MAC Address":
            response = requests.get(f"https://macvendors.com/query/{query}")
        # Bluetooth capability removed
        if response:
            try:
                results = response.json()
                # Automatische Anzeige von IP-Adresse und Gerätedaten, falls vorhanden
                if search_type == "Phone Number" and isinstance(results, dict):
                    ip = results.get('ip') or results.get('ip_address')
                    device = results.get('device') or results.get('model') or results.get('type')
                    info = f"Gefunden: IP={ip}, Gerät={device}" if ip or device else str(results)
                    self.output.append(info)
                self.populate_results(results)
            except Exception as e:
                self.output.append(f"[-] Fehler beim Parsen der Ergebnisse: {str(e)}")

    def populate_results(self, results):
        self.results_list.clear()
        if isinstance(results, dict):
            # Einzelnes Ergebnis
            self.results_list.addItem(str(results))
        else:
            for item in results:
                self.results_list.addItem(str(item))

    def select_target(self, item):
        target_info = item.text()
        self.output.append(f"[+] Ziel ausgewählt: {target_info}")
        from main import show_main_window
        self.main_window = show_main_window()
        self.close()
