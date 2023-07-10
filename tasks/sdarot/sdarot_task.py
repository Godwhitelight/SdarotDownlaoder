import tls_client

from tasks.basetask import BaseTask
from util.dns_adapter import HostHeaderSSLAdapter


class SdarotTask(BaseTask):
    def __init__(self, sdarot_cookie: str = None, sdarot_creds: str = None):
        super().__init__()

        self.sdarot_cookie = sdarot_cookie
        self.sdarot_creds = sdarot_creds

        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "he-IL,he;q=0.8",
            "cache-control": "no-cache",
            "content-length": "33",
            "origin": "https://sdarot.tw",
            "pragma": "no-cache",
            "referer": "https://sdarot.tw/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "Upgrade-Insecure-Requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }

        if not self.sdarot_cookie:
            if not self.sdarot_creds:
                raise Exception("No sdarot creds provided and no cookie provided")

            print('Logging in to sdarot')
            self.sdarot_cookie = self.login()

        self.headers['cookie'] = self.sdarot_cookie
        print(self.client.headers)

    def login(self) -> str:
        args = self.sdarot_creds.split(":")
        r = self.client.get("https://www.sdarot.tw",
                            data='cummobile'
                            )
        self.headers['cookie'] = r.headers['Set-Cookie'].split(';')[0]
        r = self.client.post("https://www.sdarot.tw/login",
                             data={"username": args[0], "password": args[1],
                                   "submit_login": ''}
                             )
        print("Logged in?", 'ברוך שובך לאתר סדרות' in r.text)
        return self.headers['cookie']
