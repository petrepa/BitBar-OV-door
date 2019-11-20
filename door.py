#!/usr/bin/env python

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re
import subprocess

ssl._create_default_https_context = ssl._create_unverified_context
encoding = 'utf-8'

def ssid_fetch():
    process = subprocess.Popen(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport','-I'], stdout=subprocess.PIPE)
    out, err = process.communicate()
    process.wait()
    out_string = out.decode(encoding)

    ssid_check = re.search("eduroam", out_string)

    return ssid_check

def door_status():
    find_string = ('Omega Verksted er åpent!').encode(encoding)

    try:
        html = urlopen("https://omegav.no/door")

    except HTTPError as e:
        print(e)
    except URLError:
        print("Server down or incorrect domain")

    else:
        res = BeautifulSoup(html.read(),"lxml")
        tags = res.find("a", {"href": "/door"})
        status = (tags.getText()).encode(encoding)
        
        if status == find_string:
            return True
        else:
            return False

def door_status_length():
    try:
        html = urlopen("https://omegav.no/door")

    except HTTPError as e:
        print(e)
    except URLError:
        print("Server down or incorrect domain")

    else:
        res = BeautifulSoup(html.read(),"lxml")
        tags = res.find("a", {"href": "/door"})["title"]
        try:
            found = re.search('(.+?) siden', tags).group(1)
        except AttributeError:
            found = 'Ukjent' 
        return found

def main():
    if ssid_fetch():
        if door_status() == True:
            print("🚪");
            print ("---");
            print("OV har vore ope i " + door_status_length());
        else:
            print("⛔");

if __name__ == "__main__":
    main()
