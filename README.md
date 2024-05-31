<p align="right">
  [English]
  [<a href="README-ko.md">한국어</a>]
</p>

# NetScanPy

NetScanPy is a network scanning tool written in Python. This project helps network security administrators or system administrators gather information about networks and identify security vulnerabilities. It is based on nmap and can perform various scans based on user-friendly options.

> NetScanPy was created to meet the demand for a scanning tool that facilitates the easy execution of frequently used options while continuously monitoring the network.

Features
- Cross-platform support for macOS, Linux, and Windows
- Execute network scans using various nmap options
- Select targets manually by entering IP addresses or through local network scans
- Display progress in real-time with tqdm progress bar
- Compare current and previous scans using the ndiff option
- Provides a user-friendly CLI interface

<img width="682" alt="ss" src="https://github.com/micronzone/NetScanPy/assets/47780105/5a71d584-1b86-4a29-874f-b601f29f1499">

### Installation
NetScanPy is a tool based on Nmap. If not already installed, on macOS, you can install it via brew install nmap or refer to the Nmap Install Guide for various installation methods.

Clone the project:

```
git clone https://github.com/micronzone/NetScanPy.git
cd NetScanPy
```

(Optional) Create and activate a virtual environment:

```
python3 -m venv .venv
source .venv/bin/activate  # Linux or macOS
.\.venv\Scripts\activate   # Windows
```

Install the required libraries:

```
pip3 install -r requirements.txt
```

Alternatively, you can install tqdm>=4.62.3, colorama>=0.4.0, or higher:

```
pip3 install tqdm
pip3 install colorama
```

### Usage

Interactive execution:

```
netscanpy
```

Quick scan execution:

```
netscanpy [options]
```

### Options

- `-l`: List all scanning option numbers
- `-n` {`1`, `2`, ..}: Select a scanning option number for quick execution (e.g., selecting option 1 is `-n 1`)
- `-d`: Compare current scan with previous scan using `difflib`
- `--debug`: Run in debug mode
- `-h`, `--help`: NetScanPy help

### Examples

Execute Nmap scanning options interactively:

```
netscanpy
```

Execute Nmap scanning options interactively with comparison mode:

```
netscanpy -d
```

Execute Nmap scanning options interactively with comparison mode and debug mode:

```
netscanpy -d --debug
```

Output Nmap scanning options for quick scan:

```
netscanpy -l
```

Execute with Nmap scanning options for quick scan:

```
netscan.py -n 1
```

Execute with Nmap scanning options for quick scan with comparison mode:

```
netscan.py -d -n 1
```

Execute with Nmap scanning options for quick scan with comparison mode and debug mode:

```
netscan.py -d -n 1 --debug
```

### Updates

It's recommended to check for updates to the NetScanPy repository!

```
cd NetScanPy
git status
```

### Fetch changes:

```
git pull origin main
```

### Contributing

Thank you for contributing! To contribute to this project, follow these steps:

1. Fork this repository
2. Create a feature branch (micronzone branch) (git checkout -b micronzone/NetScanPy)
3. Commit your changes (git commit -m 'Add some NetScanPy')
4. Push to the branch (git push origin micronzone/NetScanPy)
5. Open a pull request
License
This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for details.
