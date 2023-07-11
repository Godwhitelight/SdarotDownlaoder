import time
from typing import Dict, List

from bs4 import BeautifulSoup

from tasks.basetask import BaseTask


class SdarotTask(BaseTask):
    def __init__(self, sdarot_cookie: str = None, sdarot_creds: str = None, force_login: bool = True):
        super().__init__()

        self.sdarot_cookie = sdarot_cookie
        self.sdarot_creds = sdarot_creds
        self.search_cache = []
        self.series_cache = {
            # id: (data, time)
        }
        self.cache_time = -1

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

        if not self.sdarot_cookie and force_login:
            if not self.sdarot_creds:
                raise Exception("No sdarot creds provided and no cookie provided")

            self.sdarot_cookie = self.login()

        self.headers['cookie'] = self.sdarot_cookie

    def search(self, query: str):
        if time.time() - self.cache_time > 3600:
            self.search_cache = self.client.get(f"https://sdarot.tw/ajax/index?srl=1", data='cumtrack').json()

        query = self.clean_text(query)
        results = []
        for item in self.search_cache:
            if query.lower() in self.clean_text(item['eng']).lower() or\
                    query.lower() in self.clean_text(item['heb']).lower():
                results.append(item)

        return results

    def search_by_id(self, series_id: int):
        if time.time() - self.cache_time > 3600:
            self.search_cache = self.client.get(f"https://sdarot.tw/ajax/index?srl=1", data='cumtrack').json()

        for item in self.search_cache:
            if item['id'] == series_id:
                return item

        return '404'

    @staticmethod
    def clean_text(text: str, unicodes: List[str] = '!@#$%&^*()_+`\'"') -> str:
        for char in unicodes:
            text = text.replace(char, '')
        return text

    def login(self) -> str:
        args = self.sdarot_creds.split(":")
        r = self.client.get("https://www.sdarot.tw", data='cummobile')
        self.headers['cookie'] = r.headers['Set-Cookie'].split(';')[0]
        r = self.client.post("https://www.sdarot.tw/login",
                             data={"username": args[0], "password": args[1],
                                   "submit_login": ''}
                             )
        if 'ברוך שובך לאתר סדרות' not in r.text:
            raise Exception("Failed to login to sdarot")

        return self.headers['cookie']

    def get_series(self, series_id: int) -> Dict[str, List[int]]:
        if series_id in self.series_cache and time.time() - self.series_cache[series_id][1] < 3600:
            return self.series_cache[series_id][0]

        res = {}
        for i in range(3):
            try:
                res = self._get_series(series_id)
                break
            except Exception as e:
                if i == 2:
                    raise e

        self.series_cache[series_id] = (res, time.time())
        return res

    def _get_series(self, series_id: int) -> Dict[str, List[int]]:
        r = self.client.get(f"https://www.sdarot.tw/watch/{series_id}", data='cumtrack')
        season_element = BeautifulSoup(r.text, 'html.parser').find('ul', {'id': 'season'})
        seasons: List[int] = [int(season['data-season']) for season in season_element.find_all('li')]
        res = {}
        for season in seasons:
            r = self.client.get(f"https://www.sdarot.tw/watch/{series_id}/season/{season}", data='cumtrack')
            episodes_element = BeautifulSoup(r.text, 'html.parser').find('ul', {'id': 'episode'}).find_all('li')
            res[str(season)] = [int(episode['data-episode']) for episode in episodes_element]

        return res
