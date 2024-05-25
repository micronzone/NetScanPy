import os
import subprocess
import sys
from tqdm import tqdm
import time
import ipaddress
import difflib
from colorama import Fore, Style

# Micronzone's NetScanPy
def print_signature():
    print("### NetScanPy v1.0 ###")

# nmap 옵션 모듈화
nmap_options = [
    {"cmd": "nmap -sn", "desc": "[recommended for first-time use] - Ping scan to check which hosts are up without port scanning."},
    {"cmd": "nmap --open", "desc": "Displays only open ports."},
    {"cmd": "nmap --iflist", "desc": "Shows network interface information."},
    {"cmd": "sudo nmap -sS -v -T1", "desc": "Performs a slow TCP SYN scan. ** run as root **"},
    {"cmd": "sudo nmap -sF -v", "desc": "Looks for closed ports (FIN scan). ** run as root **"},
    {"cmd": "sudo nmap -sS -T4 -PE -PP -PS80,443 -PY -g 53 -A -p1-65535 -v", "desc": "Rapidly scans network with various techniques. ** run as root **"},
    {"cmd": "sudo nmap -sA -p1-65535 -v -T4", "desc": "Scans for ACK responses. ** run as root **"},
    {"cmd": "nmap -PS -PA", "desc": "Combines TCP SYN and ACK scans."},
    {"cmd": "nmap -F -T5 --version-light --top-ports 300", "desc": "Rapidly scans top ports."},
    {"cmd": "sudo nmap -sV -p1-65535 -O --osscan-guess -T4 -Pn", "desc": "Identifies services and OS fingerprints. ** run as root **"},
    {"cmd": "nmap --script=vuln", "desc": "Runs vulnerability scripts."},
    {"cmd": "sudo nmap -sS -sU -T4 -A -v -PE -PS22,25,80 -PA21,23,80,443,3389", "desc": "Conducts TCP SYN and UDP scans. ** run as root **"},
    {"cmd": "sudo nmap -sP -PE -PS22,25,80 -PA21,23,80,3389 -PU -PO --traceroute", "desc": "Host scan with traceroute. ** run as root **"},
    {"cmd": "sudo nmap -sS -sU -T4 -A -v -PE -PP -PS21,22,23,25,80,113,31339 -PA80,113,443,10042 -PO --script all", "desc": "Scans with various techniques and executes all scripts. ** run as root **"},
    {"cmd": "sudo nmap -p 80,443 -O -v --osscan-guess --fuzzy", "desc": "Scans specific ports and guesses OS details. ** run as root **"},
    {"cmd": "nmap -n -sP", "desc": "Host discovery without DNS resolution."},
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
    while True:
        ip_range = input("Enter IP address or range (e.g., 0.0.0.0 or 0.0.0.0/24): ")
        try:
            ip_obj = ipaddress.ip_network(ip_range, strict=False)
            if ip_obj.version == 4:
                return [ip_range]
            else:
                print("IPv6 addresses are not supported. Please enter an IPv4 address or range.")
        except ValueError:
            print("Invalid IP address or range. Please enter a valid IPv4 address or range.")

def scan_local_network():
    if sys.platform == 'darwin':
        result = subprocess.run(["ifconfig"], capture_output=True, text=True)
        gateway_result = subprocess.run(["netstat", "-nr"], capture_output=True, text=True)
    elif sys.platform == 'win32':
        result = subprocess.run(["ipconfig"], capture_output=True, text=True)
        gateway_result = subprocess.run(["route", "print"], capture_output=True, text=True)
    else:
        result = subprocess.run(["ip", "addr"], capture_output=True, text=True)
        gateway_result = subprocess.run(["ip", "route"], capture_output=True, text=True)
    
    ips = []
    for line in result.stdout.splitlines():
        if sys.platform == 'win32' and "IPv4 Address" in line:
            ip = line.split(":")[1].strip()
        elif "inet " in line:
            if sys.platform == 'darwin':
                ip = line.split()[1]
            else:
                ip = line.split()[1].split('/')[0]
        else:
            continue

        try:
            ip_obj = ipaddress.ip_address(ip)
            if ip_obj.version == 4 and ip_obj.is_private:
                ips.append(ip)
        except ValueError:
            continue

    for line in gateway_result.stdout.splitlines():
        if sys.platform == 'win32' and "0.0.0.0" in line:
            gateway_ip = line.split()[-2]
        elif "default" in line or "UG" in line:
            gateway_ip = line.split()[1] if sys.platform == 'darwin' else line.split()[2]
        else:
            continue

        try:
            gateway_ip_obj = ipaddress.ip_address(gateway_ip)
            if gateway_ip_obj.version == 4 and gateway_ip_obj.is_private:
                ips.append(gateway_ip)
        except ValueError:
            continue

    if not ips:
        print("No IP addresses found.")
        return get_ip_choice()

    ips = list(set(ips))
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

# 이전 스캔 결과를 저장할 파일 경로
previous_scan_file = "previous_scan.txt"

# 이전 스캔 결과를 저장하는 함수
def save_previous_scan(output):
    with open(previous_scan_file, "w") as file:
        file.write(output)

# 현재 스캔 결과와 이전 스캔 결과를 비교하여 차이점을 출력하는 함수
def compare_results(current_output, previous_output):
    diff = difflib.unified_diff(previous_output.splitlines(), current_output.splitlines(), lineterm='')
    print("Difference between previous and current scan results:")
    for line in diff:
        if line.startswith('+'):
            print(Fore.CYAN + line)
        elif line.startswith('-'):
            print(Fore.MAGENTA + line)
        else:
            print(line)
    print(Style.RESET_ALL)  # 리셋하여 이후 출력이 정상적으로 이뤄지도록 함

# 이전 스캔 결과 파일이 존재하는지 확인하고 있다면 내용을 반환하는 함수
def get_previous_scan():
    if os.path.isfile(previous_scan_file):
        with open(previous_scan_file, "r") as file:
            return file.read()
    else:
        return None

# 이전 스캔 결과와 현재 스캔 결과를 비교하고 저장하는 함수
def run_nmap(cmd, targets, use_diff=False, debug=False):
    full_cmd = cmd + " " + " ".join(targets)
    
    if debug:
        print(f"Running command: {full_cmd}")

    process = subprocess.Popen(full_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    current_output = ""

    with tqdm(total=100, desc="Scanning", unit="tick") as pbar:
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                current_output += output
                pbar.update(1)
        process.stdout.close()
        process.stderr.close()
        process.wait()
        pbar.n = 100
        pbar.refresh()

        if use_diff:
            previous_output = get_previous_scan()
            if previous_output:
                compare_results(current_output, previous_output)

        save_previous_scan(current_output)

def print_help():
    help_text = """
Usage: script [-h | --help] [-l] [-n {number}] [-d] [--debug]
Options:
  -h, --help          Show this help message and exit.
  -l                  List all available nmap options.
  -n {number}         Select and run a specific nmap option by its number.
  -d                  Use difflib to compare current and previous scan results.
  --debug             Run the script in debug mode.
"""
    print(help_text)

def main():
    print_signature()
    use_diff = '-d' in sys.argv
    debug = '--debug' in sys.argv
    args = [arg for arg in sys.argv[1:] if arg not in ['-d', '--debug']]
    
    if debug:
        print(f"Arguments: {args}")
        print(f"Use difflib: {use_diff}")
    
    if args:
        if args[0] in ['-h', '--help']:
            print_help()
            return
        elif args[0] == '-l':
            list_options()
            return
        elif args[0] == '-n' and len(args) == 2:
            try:
                choice = int(args[1])
                if 1 <= choice <= len(nmap_options):
                    option = nmap_options[choice - 1]
                    targets = get_ip_choice()
                    run_nmap(option["cmd"], targets, use_diff=use_diff, debug=debug)
                    return
            except ValueError:
                pass
        print("Invalid arguments. Usage: script [-h | --help] [-l] [-n {number}] [-d] [--debug]")
        return

    while True:
        option = select_option()
        targets = get_ip_choice()
        run_nmap(option["cmd"], targets, use_diff=use_diff, debug=debug)
        again = input("Do you want to run another scan? (y/n): ").strip().lower()
        if again != 'y':
            break

if __name__ == "__main__":
    main()
