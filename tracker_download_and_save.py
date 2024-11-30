#!/usr/bin/env python3
from datetime import datetime
import urllib
import urllib.request

from decryptor import Decryptor


BASE_URL = "https://tracking2024.vendeeglobe.org/data/"
FILES = ["tracker_config", "tracker_live", "tracker_tracks", "tracker_reports"]
VERSION = datetime.now().strftime("%Y%m%d%H%M%S")

decryptor = Decryptor()
for element in FILES:
    print("Downloading", element)
    url = BASE_URL + element + ".hwx?version=" + VERSION
    request = urllib.request.Request(url,  headers={'User-Agent' : "Browser"})
    encrypted = urllib.request.urlopen(request).read()
    open(element + "_" + VERSION + ".hrw", "wb").write(encrypted)

    decrypted = decryptor.decrypt(encrypted)
    open(element + "_" + VERSION + ".xml", "w").write(decrypted)

print("Done")
