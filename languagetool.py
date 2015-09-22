__author__ = 'siredvin'
import subprocess
import os
import requests


def start_server(path, server_port):
    server = subprocess.Popen(
        ['java', '-cp', os.path.join(path, 'languagetool-server.jar'), 'org.languagetool.server.HTTPServer'
            , '--port ' + str(server_port)])
    r = requests.post("http://localhost:" + str(server_port), {"language": 'en', 'text': 'my texd'})
    print(r.text)
