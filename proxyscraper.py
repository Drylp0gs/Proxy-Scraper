
import os
import re
import sys
import time
import random
import argparse
import threading
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init

init(autoreset=True)

# ==============================
# DRYLPOGS PROXY SCRAPER
# ==============================

BANNER = r"""
                        █▓█
▀▄▓▀█▓▄ ▀▄▓▀█▓▄ ▀▄▓▀█▓█ ▀▄▓ ▓▀█ █▀▓ █▓█      █▓▀▀█▓█ █▀▓▀██▓ ▀▄▓▀█▓▄ █▀▓▀█▓█ ▀▄▓▀█▓▄ █▀▓▀██▓ ▀▄▓▀█▓▄
▓▓   ▀█ ▓▓   ▀█ ▓▓   ▀█ ▓▓  ▀▓▓ ▓▓▀  █▓      ▓ ▀  █  ▓▀█ ██▀ ▓▓   ▀█ ▓▓▀  █▓ ▓▓   ▀█ ▓▀█ ██▀ ▓▓   ▀█
▄█ ▀▀▀  ▄█ ▀█▓▄ ▄█  █ ▀ ▄█                    ██ ▄ █ ▀     ▓ ▄█ ▀█▓▄         ▄█ ▀▀▀  ▀     ▓ ▄█ ▀█▓▄
▓▄█     ▓▄█ ▓█▒ ▓▄█ ▓█▄ ▀▄█▄▄▓▀ ▀▀▀▄▄▓       █▄▓▄▄▄▄ █▄▓     ▓▄█ ▓█▒ ██▄▄▄▓  ▓▄█     █▄▓▄    ▓▄█ ▓█▒
█▓█     █▓█ ███ █▓█▄███ ▓▓█ ███ ▄▄▄ ███      ▄▄▄▄██▓ ▓██▄▄▄▄ █▓█ ███ ▓█▓ ███ █▓█     ▓██▄▄▄▄ █▓█ ███
                            ▓█▓ ▀▀▀▄▓██                                  ▓█▓

                              by DrylPogs
"""

OUTPUT_FILE = "proxy.txt"

# ==============================
# PROXY SOURCES
# ==============================

proxy_urls = [
    "https://api.proxyscrape.com/v2/?request=displayproxies",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/yuceltoluyag/GoodProxy/main/raw.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
    "https://proxyspace.pro/http.txt",
    "https://api.proxyscrape.com/?request=displayproxies&proxytype=http",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://api.openproxylist.xyz/http.txt",
    "https://multiproxy.org/txt_all/proxy.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
]

# ==============================
# COLORS
# ==============================

RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
WHITE = Fore.WHITE
CYAN = Fore.CYAN
RESET = Style.RESET_ALL

# ==============================
# USER AGENTS
# ==============================

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Chrome/120.0 Safari/537.36",
]

# ==============================
# DOWNLOAD PROXIES
# ==============================

def download_and_save_proxies(url):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        found = re.findall(
            r"\b(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}\b",
            response.text
        )

        print(f"{GREEN}[+] Collect {WHITE}{url}")

        return found

    except requests.RequestException:
        print(f"{RED}[-] Failed {WHITE}{url}")
        return []


def download_proxies():
    print(f"{YELLOW}Downloading...\n")

    all_proxies = set()

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(download_and_save_proxies, url)
            for url in proxy_urls
        ]

        for future in as_completed(futures):
            all_proxies.update(future.result())

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        for proxy in sorted(all_proxies):
            file.write(proxy + "\n")

    print(f"\n{GREEN}[+] Total unique proxies: {YELLOW}{len(all_proxies)}")

    return len(all_proxies)


# ==============================
# PROXY VALIDATION
# ==============================

def is_valid_proxy(proxy):
    pattern = r"^(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}$"

    if not re.fullmatch(pattern, proxy):
        return False

    ip, port = proxy.split(":")

    try:
        import ipaddress
        ipaddress.IPv4Address(ip)

        return 1 <= int(port) <= 65535

    except ValueError:
        return False


# ==============================
# CHECK PROXY
# ==============================

def check_proxy(proxy, site, timeout, random_agent):
    proxy_url = f"http://{proxy}"

    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }

    headers = {
        "User-Agent": (
            random.choice(user_agents)
            if random_agent
            else user_agents[0]
        )
    }

    try:
        start = time.perf_counter()

        response = requests.get(
            site,
            proxies=proxies,
            headers=headers,
            timeout=timeout
        )

        elapsed = time.perf_counter() - start

        response.raise_for_status()

        return proxy, True, elapsed

    except requests.RequestException:
        return proxy, False, 0


# ==============================
# CHECK ALL PROXIES
# ==============================

def check_all_proxies(
    timeout=15,
    site="https://www.google.com/",
    verbose=False,
    random_agent=False,
    workers=50
):

    if not os.path.isfile(OUTPUT_FILE):
        print(f"{RED}[-] proxy.txt tidak ditemukan!")
        return

    with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
        proxies = list(set(
            line.strip()
            for line in file
            if is_valid_proxy(line.strip())
        ))

    print(f"\n{GREEN}[+] Checking {YELLOW}{len(proxies)}{GREEN} Proxy\n")

    valid_proxies = []
    completed = 0
    lock = threading.Lock()

    with ThreadPoolExecutor(max_workers=workers) as executor:

        futures = {
            executor.submit(
                check_proxy,
                proxy,
                site,
                timeout,
                random_agent
            ): proxy
            for proxy in proxies
        }

        for future in as_completed(futures):
            proxy, valid, elapsed = future.result()

            with lock:
                completed += 1

                if valid:
                    valid_proxies.append(proxy)

                    if verbose:
                        print(
                            f"{GREEN}[VALID] {WHITE}{proxy} "
                            f"{CYAN}| {elapsed:.2f}s"
                        )

                elif verbose:
                    print(f"{RED}[INVALID] {WHITE}{proxy}")

                print(
                    f"\r{YELLOW}Progress: {completed}/{len(proxies)} "
                    f"| Valid: {GREEN}{len(valid_proxies)}",
                    end=""
                )

    print("\n")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        for proxy in sorted(valid_proxies):
            file.write(proxy + "\n")

    print(f"{GREEN}[+] Found {YELLOW}{len(valid_proxies)}{GREEN} valid proxies")

    print(f"{GREEN}[+] Saved to {WHITE}{OUTPUT_FILE}")


# ==============================
# MAIN
# ==============================

def main():

    os.system("cls" if os.name == "nt" else "clear")

    print(f"{CYAN}{BANNER}{RESET}")

    if os.path.isfile(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        print(f"{RED}'proxy.txt' was Deleted.{RESET}")

    total = download_proxies()

    if total == 0:
        print(f"{RED}[-] No proxies downloaded.")
        return

    print(
        f"\n{WHITE}( {YELLOW}{total}{WHITE} ) "
        f"{GREEN}The proxy is downloaded, want to check? "
        f"{WHITE}({GREEN}Y{WHITE}/{RED}N{WHITE}): ",
        end=""
    )

    choice = input().strip().lower()

    if choice == "y":

        parser = argparse.ArgumentParser(
            description="DrylPogs Proxy Scraper"
        )

        parser.add_argument(
            "-t", "--timeout",
            type=int,
            default=15,
            help="Proxy timeout in seconds"
        )

        parser.add_argument(
            "-s", "--site",
            default="https://www.google.com/",
            help="Website used for proxy testing"
        )

        parser.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="Show detailed proxy results"
        )

        parser.add_argument(
            "-r", "--random_agent",
            action="store_true",
            help="Use random user agent"
        )

        parser.add_argument(
            "-w", "--workers",
            type=int,
            default=50,
            help="Number of concurrent workers"
        )

        args = parser.parse_args()

        if args.timeout <= 0 or args.workers <= 0:
            print(f"{RED}[-] Timeout and workers must be positive.")
            return

        check_all_proxies(
            timeout=args.timeout,
            site=args.site,
            verbose=args.verbose,
            random_agent=args.random_agent,
            workers=args.workers
        )

    else:
        print(f"\n{YELLOW}Thanks for using the script!a!.\n")


if __name__ == "__main__":
    main()
