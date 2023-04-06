#!/bin/sh
#install python and update system
sudo apt update 
sudo apt install python -y
# Install the Python script
sudo cp internet-monitor.py /usr/local/bin/internet-monitor.py
sudo chmod +x /usr/local/bin/internet-monitor.py

# Install the systemd service file
sudo tee /etc/systemd/system/internet-monitor.service > /dev/null <<EOT
[Unit]
Description=Internet Connection Monitor

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/internet-monitor.py
Restart=always

[Install]
WantedBy=multi-user.target
EOT

# Reload the systemd configuration
sudo systemctl daemon-reload

# Install the internet-monitor command
sudo tee /usr/local/bin/internet-monitor > /dev/null <<EOT
#!/bin/sh
/usr/bin/python3 /usr/local/bin/internet-monitor.py "\$@"
EOT
sudo chmod +x /usr/local/bin/internet-monitor

echo "Installation complete."