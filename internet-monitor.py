import os
import sys
import time
import urllib.request

def internet_on(site):
    try:
        urllib.request.urlopen(site, timeout=1)
        return True
    except urllib.request.URLError:
        return False

def read_config():
    if os.path.exists(config_file):
        with open(config_file) as f:
            lines = f.read().splitlines()
            site = lines[0] if lines else 'http://google.com'
            muted = 'muted' in lines
            duration = int(lines[-1]) if lines and lines[-1].isdigit() else 1
            return site, muted, duration
    return 'http://google.com', False, 40

def write_config(site, muted, duration):
    with open(config_file, 'w') as f:
        f.write(site + '\n')
        if muted:
            f.write('muted\n')
        f.write(str(duration) + '\n')

def print_help():
    print(r"""
 ______          __                                 __                                          __                   
/\__  _\        /\ \__                             /\ \__           /'\_/`\                  __/\ \__                
\/_/\ \/     ___\ \ ,_\    __   _ __    ___      __\ \ ,_\         /\      \    ___     ___ /\_\ \ ,_\   ___   _ __  
   \ \ \   /' _ `\ \ \/  /'__`\/\`'__\/' _ `\  /'__`\ \ \/  _______\ \ \__\ \  / __`\ /' _ `\/\ \ \ \/  / __`\/\`'__\
    \_\ \__/\ \/\ \ \ \_/\  __/\ \ \/ /\ \/\ \/\  __/\ \ \_/\______\\ \ \_/\ \/\ \L\ \/\ \/\ \ \ \ \ \_/\ \L\ \ \ \/ 
    /\_____\ \_\ \_\ \__\ \____\\ \_\ \ \_\ \_\ \____\\ \__\/______/ \ \_\\ \_\ \____/\ \_\ \_\ \_\ \__\ \____/\ \_\ 
    \/_____/\/_/\/_/\/__/\/____/ \/_/  \/_/\/_/\/____/ \/__/          \/_/ \/_/\/___/  \/_/\/_/\/_/\/__/\/___/  \/_/ 
                                                                                                                     
                                                                                                                     
""")
    print("Usage: internet-monitor [command]")
    print()
    print("Commands:")
    print("  silence\tMute the alarm")
    print("  test\t\tTest the alarm for the specified duration")
    print("  ping [site]\tSet the site to ping for testing the internet connection")
    print("  duration [n]\tSet the duration of the alarm in seconds")
    print("  help\t\tShow this help message")

config_file = '/etc/internet-monitor.conf'
ping_site, muted, duration = read_config()

if len(sys.argv) > 1:
    if sys.argv[1] == 'silence':
        write_config(ping_site, True, duration)
        print("Alarm muted.")
        sys.exit(0)
    elif sys.argv[1] == 'test':
        print("Testing alarm...")
        for _ in range(duration):
            os.system("espeak 'Internet connection lost'")
            os.system("echo -n '\a'")
            time.sleep(1)
        sys.exit(0)
    elif sys.argv[1] == 'ping':
        if len(sys.argv) > 2:
            ping_site = sys.argv[2]
            write_config(ping_site, muted, duration)
            print(f"Pinging {ping_site}")
        else:
            print("Usage: internet-monitor ping [site]")
        sys.exit(0)
    elif sys.argv[1] == 'duration':
        if len(sys.argv) > 2 and sys.argv[2].isdigit():
            duration = int(sys.argv[2])
            write_config(ping_site, muted, duration)
            print(f"Alarm duration set to {duration} seconds")
        else:
            print("Usage: internet-monitor duration [n]")
        sys.exit(0)
    elif sys.argv[1] == 'help':
        print_help()
        sys.exit(0)

while True:
    if not internet_on(ping_site):
        print(f"Internet connection lost. Pinging {ping_site}. Playing alarm...")
        alarm_time = time.time() + duration
        while not internet_on(ping_site) and time.time() < alarm_time:
            if not muted:
                os.system("say 'Internet connection lost'")
                os.system("echo -n '\a'")
            time.sleep(1)
    time.sleep(5)