import os
import subprocess
import sys
from tqdm import tqdm
import time
import ipaddress

# nmap 옵션 모듈화
nmap_options = [
    {"cmd": "nmap --open", "desc": "Open Ports Scan"},
    {"cmd": "nmap --iflist", "desc": "List Interfaces"},
    {"cmd": "sudo nmap -sS -v -T1", "desc": "Slow Scan"},
    {"cmd": "sudo nmap -sF -v", "desc": "FIN Scan"},
    {"cmd": "sudo nmap -sS -T4 -PE -PP -PS80,443 -PY -g 53 -A -p1-65535 -v", "desc": "Full Scan"},
    {"cmd": "sudo nmap -sA -p1-65535 -v -T4", "desc": "Check for Firewall"},
    {"cmd": "nmap -PS -PA", "desc": "Ping Through Firewall"},
    {"cmd": "nmap -F -T5 --version-light --top-ports 300", "desc": "Fast Scan"},
    {"cmd": "sudo nmap -sV -p1-65535 -O --osscan-guess -T4 -Pn", "desc": "Detect Versions"},
    {"cmd": "nmap --script=vuln", "desc": "Check for Vulnerabilities"},
    {"cmd": "sudo nmap -sS -sU -T4 -A -v -PE -PS22,25,80 -PA21,23,80,443,3389", "desc": "Full UDP Scan"},
    {"cmd": "sudo nmap -sP -PE -PS22,25,80 -PA21,23,80,3389 -PU -PO --traceroute", "desc": "Traceroute"},
    {"cmd": "sudo nmap -sS -sU -T4 -A -v -PE -PP -PS21,22,23,25,80,113,31339 -PA80,113,443,10042 -PO --script all", "desc": "Full Scan with Scripts"},
    {"cmd": "sudo nmap -p 80,443 -O -v --osscan-guess --fuzzy", "desc": "Web Safe OS Scan"},
    {"cmd": "nmap -n -sP", "desc": "Ping Scan"},
]

def list_options():
    for i, option in enumerate(nmap_options, 1):
        print(f"[{i}] {option['desc']}")

def select_option():
    while True:
        list_options()
        try:
            choice = int(input("Select an option by number: "))
            if 1 <= choice <= len(nmap_options):
                return nmap_options[choice - 1]
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_ip_choice():
    print("[1] Enter IP address manually")
    print("[2] Scan local network for IP addresses")
    while True:
        try:
            choice = int(input("Select an option by number: "))
            if choice == 1:
                return enter_ip_manually()
            elif choice == 2:
                return scan_local_network()
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def enter_ip_manually():
    ip_range = input("Enter IP address or range (e.g., 0.0.0.0 or 0.0.0.0/24): ")
    return [ip_range]

def scan_local_network():
    if sys.platform == 'darwin':  # macOS
        result = subprocess.run(["ifconfig"], capture_output=True, text=True)
        gateway_result = subprocess.run(["netstat", "-nr"], capture_output=True, text=True)
    elif sys.platform == 'win32':  # Windows
        result = subprocess.run(["ipconfig"], capture_output=True, text=True)
        gateway_result = subprocess.run(["route", "print"], capture_output=True, text=True)
    else:  # Linux and other Unix-like systems
        result = subprocess.run(["ip", "addr"], capture_output=True, text=True)
        gateway_result = subprocess.run(["ip", "route"], capture_output=True, text=True)
    
    ips = []
    for line in result.stdout.splitlines():
        if sys.platform == 'win32' and "IPv4 Address" in line:
            ip = line.split(":")[1].strip()
        elif "inet " in line:  # Filter only IPv4 addresses
            if sys.platform == 'darwin':
                ip = line.split()[1]
            else:
                ip = line.split()[1].split('/')[0]
        else:
            continue

        try:
            ip_obj = ipaddress.ip_address(ip)
            if ip_obj.version == 4 and ip_obj.is_private:  # Ensure it's IPv4 and private
                ips.append(ip)
        except ValueError:
            continue

    # Find the default gateway
    for line in gateway_result.stdout.splitlines():
        if sys.platform == 'win32' and "0.0.0.0" in line:
            gateway_ip = line.split()[-2]
        elif "default" in line or "UG" in line:
            gateway_ip = line.split()[1] if sys.platform == 'darwin' else line.split()[2]
        else:
            continue

        try:
            gateway_ip_obj = ipaddress.ip_address(gateway_ip)
            if gateway_ip_obj.version == 4 and gateway_ip_obj.is_private:  # Ensure it's IPv4 and private
                ips.append(gateway_ip)
        except ValueError:
            continue

    if not ips:
        print("No IP addresses found.")
        return get_ip_choice()

    ips = list(set(ips))  # Remove duplicates
    for i, ip in enumerate(ips, 1):
        print(f"[{i}] {ip}")
    
    while True:
        try:
            print(f"[{len(ips)+1}] Enter IP address manually (e.g., 0.0.0.0 or 0.0.0.0/24)")
            choice = int(input("Select an IP address by number: "))
            if 1 <= choice <= len(ips):
                return [ips[choice - 1]]
            elif choice == len(ips) + 1:
                return enter_ip_manually()
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def run_nmap(cmd, targets):
    full_cmd = cmd + " " + " ".join(targets)
    process = subprocess.Popen(full_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for _ in tqdm(range(100), desc="Scanning", unit="tick"):
        if process.poll() is not None:
            break
        time.sleep(0.1)
    stdout, stderr = process.communicate()
    print(stdout.decode())
    if stderr:
        print(stderr.decode())

def print_help():
    help_text = """
Usage: script [-h | --help] [-l] [-n {number}]
Options:
  -h, --help          Show this help message and exit.
  -l                  List all available nmap options.
  -n {number}         Select and run a specific nmap option by its number.
"""
    print(help_text)

def main():
    while True:
        if len(sys.argv) > 1:
            if sys.argv[1] in ['-h', '--help']:
                print_help()
                return
            elif sys.argv[1] == '-l':
                list_options()
                return
            elif sys.argv[1] == '-n' and len(sys.argv) == 3:
                try:
                    choice = int(sys.argv[2])
                    if 1 <= choice <= len(nmap_options):
                        option = nmap_options[choice - 1]
                        targets = get_ip_choice()
                        run_nmap(option["cmd"], targets)
                        return
                except ValueError:
                    pass
            print("Invalid arguments. Usage: script [-h | --help] [-l] [-n {number}]")
            return

        option = select_option()
        targets = get_ip_choice()
        run_nmap(option["cmd"], targets)
        again = input("Do you want to run another scan? (y/n): ").strip().lower()
        if again != 'y':
            break

if __name__ == "__main__":
    main()

