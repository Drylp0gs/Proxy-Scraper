# Proxy Scraper

<p align="center">
  <b>Python Proxy Scraper & Checker</b>
</p>

<p align="center">
  Scrape public proxies from multiple sources, remove duplicates, and check proxy connectivity.
</p>

---

## Features

* Scrape proxies from multiple public sources(You can edit it)
* Automatically remove duplicate proxies
* Validate IPv4 addresses and ports
* Multithreaded proxy checking
* Configurable timeout
* Random User-Agent support
* Custom website testing
* Verbose checking mode
* Automatically save working proxies
* Simple terminal interface

---

## Requirements

* Python 3.9 or newer
* Internet connection
* Windows, Linux, or macOS

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Drylp0gs/Proxy-Scraper.git
```

### 2. Enter the project directory

```bash
cd Proxy-Scraper
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

### 4. Run the scraper

```bash
python proxyscraper.py
```

---

## Usage

When the program starts, it collects proxies from the configured public sources.

After downloading, you will see:

```text
Proxy Sudah Di Unduh, Mau Check? (Y/N):
```

Enter:

```text
Y
```

to check the collected proxies.

Enter:

```text
N
```

to exit.

---

## Command-Line Options

| Option                 | Description                  | Default  |
| ---------------------- | ---------------------------- | -------- |
| `-t`, `--timeout`      | Proxy timeout in seconds     | `15`     |
| `-s`, `--site`         | Website used for testing     | Google   |
| `-v`, `--verbose`      | Display detailed results     | Disabled |
| `-r`, `--random_agent` | Use a random User-Agent      | Disabled |
| `-w`, `--workers`      | Number of concurrent workers | `50`     |

---

## Examples

### Basic

```bash
python ProxyScraper.py
```

### Verbose mode

```bash
python ProxyScraper.py -v
```

### 10-second timeout

```bash
python ProxyScraper.py -t 10
```

### 100 concurrent workers

```bash
python ProxyScraper.py -w 100
```

### Custom website

```bash
python ProxyScraper.py -s https://example.com
```

### Combine options

```bash
python ProxyScraper.py -t 10 -w 100 -v -r
```

---

## Output

The scraper creates:

```text
proxy.txt
```

The file initially contains the proxies collected from the configured sources.

After checking, only proxies that successfully connect to the selected test website are retained.

Example:

```text
192.168.1.100:8080
45.12.34.56:3128
103.21.45.67:80
```

---

## Project Structure

```text
Proxy-Scraper/
│
├── ProxyScraper.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── proxy.txt
```

`proxy.txt` is generated automatically and is excluded from Git using `.gitignore`.

---

## Requirements

The project uses:

* [Requests](https://pypi.org/project/requests/)
* [Colorama](https://pypi.org/project/colorama/)

Install them with:

```bash
pip install -r requirements.txt
```

---

## Disclaimer

This project is intended for educational purposes and authorized network testing.

The scraper collects publicly available proxy addresses from third-party sources. Public proxies may be unreliable, insecure, or monitored by their operators.

Do not use untrusted public proxies for passwords, banking, PayPal, financial transactions, or other sensitive activities.

The author is not responsible for
