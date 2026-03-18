
try:
    import bluetooth
    BLUETOOTH_AVAILABLE = True
except ImportError:
    BLUETOOTH_AVAILABLE = False

import threading

class BluetoothScanner:
    def __init__(self):
        self.devices = []

    def discover_devices(self, duration=8):
        """Discover nearby Bluetooth devices"""
        self.devices = []
        if not BLUETOOTH_AVAILABLE:
            return []
        nearby_devices = bluetooth.discover_devices(duration=duration, lookup_names=True)
        for addr, name in nearby_devices:
            device_info = {
                'address': addr,
                'name': name,
                'type': 'Bluetooth',
                'signal_strength': self.get_signal_strength(addr)
            }
            self.devices.append(device_info)
        return self.devices

    def get_signal_strength(self, address):
        """Get signal strength for a device"""
        if not BLUETOOTH_AVAILABLE:
            return 0
        try:
            info = bluetooth.lookup_name(address, timeout=5)
            return info.get('RSSI', 0)
        except:
            return 0

    def scan_device(self, address):
        """Scan specific device for services"""
        if not BLUETOOTH_AVAILABLE:
            return []
        services = bluetooth.find_service(address=address)
        return services
