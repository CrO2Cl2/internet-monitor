#!/bin/sh
#install python and update system
apt update 
apt install python -y
#installing mpg123
apt install mpg123 -y
# Install the Python script
cp internet-monitor.py /usr/local/bin/internet-monitor.py
chmod +x /usr/local/bin/internet-monitor.py
cp alarm.mp3 /etc/internet-monitor-alarm.mp3

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