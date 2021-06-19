import urllib.request
import socket
import urllib.error
import time
from socket import timeout


# Проверка прокси сервера
class ProxyCheck():
    def __init__(self):
        self.server = ''

    def is_bad_proxy(self, pip):
        try:
            proxy_handler = urllib.request.ProxyHandler({'https': pip})
            opener = urllib.request.build_opener(proxy_handler)
            opener.addheaders = [
                ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36')]
            urllib.request.install_opener(opener)
            req = urllib.request.Request(self.server)  # change the URL to test here
            sock = urllib.request.urlopen(req, timeout=15)
        except urllib.error.HTTPError as e:
            # print('Error code: ', e.code)
            return True
        except Exception as detail:
            # print("ERROR:", detail)
            return True
        return False

    def proxy_check(self, url, proxy):
        self.server = url
        # socket.setdefaulttimeout(120)
        print(f"Проверка прокси, ожидаем {proxy}")
        if self.is_bad_proxy(proxy):
            return False
        else:
            print(f"Прокси сервер найден")
            time.sleep(3)
            return True
