import urllib.request
import socket
import urllib.error


# Проверка прокси сервера
class ProxyCheck():
    def __init__(self):
        self.url = ''

    def is_bad_proxy(self, pip):
        try:
            proxy_handler = urllib.request.ProxyHandler({'https': pip})
            opener = urllib.request.build_opener(proxy_handler)
            opener.addheaders = [
                ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36')]
            urllib.request.install_opener(opener)
            req = urllib.request.Request(self.url)  # change the URL to test here
            sock = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            # print('Error code: ', e.code)
            return e.code
        except Exception as detail:
            # print("ERROR:", detail)
            return True
        return False

    def proxy_check(self, url, proxy):
        self.url = url
        socket.setdefaulttimeout(160)

        if self.is_bad_proxy(proxy):
            print(f"Прокси не работает {proxy}")
            return False
        else:
            print(f"Прокси рабочий {proxy}")
            return True
