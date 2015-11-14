# /usr/bin/env python3.5
# A simple script to google from command line
# Author: psaux0
# Date: 2015.10.20
# Python version: >= 3.5

import argparse
import subprocess
import urllib.parse, sys

def encodeAdr(s: str) -> str:
    return urllib.parse.urlencode({'q': s})

def exeCmd(cmd):
    subprocess.run(["open",cmd])

def main():
    parser = argparse.ArgumentParser(description = "google from command line")
    parser.add_argument('-a', '--address' , dest='addr', help='Search contents')
    arg = parser.parse_args()
    searchAdr = ''.join(["https://www.google.com/#",encodeAdr(arg.addr)])

    #open browser
    try:
        exeCmd(searchAdr)
        print("[+] Success: directing to google")
    except e:
        print("[-] Error: open browser")
        sys.exit(1)

if __name__ == "__main__":
    main()
