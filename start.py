#/home/fed/code/par_2/start.py (ffe2a7e)

from bs4 import BeautifulSoup
import requests
import fake_useragent
from time import sleep


def connect_tor(url):
            # Just a line
    line = "---------------------------------------------------------------"

    # Random User-Agent
    ua = fake_useragent.UserAgent()
    user = ua.random
    header = {'User-Agent': str(user)}

    # Connection to the ip-site
    ipSite = 'http://icanhazip.com'
    adress = requests.get(ipSite, headers=header)

    # Check your ip adress
    print(line + "\n[*] IP your network:\n"+adress.text + line)
    print("[!] Connecting to the Tor network /", end="")

    # Just points
    for _ in range(5):
        sleep(0.2)
        print(end='.', flush=True)

    # Proxie tor's
    proxie = {
        # 'http': '144.202.3.139:10464',
        # 'https': '144.202.3.139:10464'
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }

    # Connecting to the network tor
    try:
        adress = requests.get(ipSite, proxies=proxie, headers=header)

    # Not connected
    except:
        connection = False
        print("/\n[x] Stopping connect to the Tor network\n" + line)

    # Connected
    else:
        connection = True
        print("/\n[+] Connected to the Tor network\n" + line)
        print("[*] IP Tor network:\n" + adress.text + line)

    # Parse site
    finally:
        #url = input("[!] Uniform Resource Locator:\n")

        if connection == True:
            page = requests.get(
                # "http://"+
                url.split()
                [0], proxies=proxie, headers=header)
        else:
            page = requests.get(
                # "http://" +
                url.split()[0], headers=header)

        soup = BeautifulSoup(page.text, "html.parser")
    return(soup)


def __main():
    url = "https://www.betexplorer.com/soccer/"
    connect_tor(url)


if __name__ == "__main__":
    __main()

