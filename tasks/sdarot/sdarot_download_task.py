from typing import Self

from tasks.basetask import BaseDownloadTask


class SdarotDownloadTask(BaseDownloadTask):
    def __init__(self, series_id: int, season: int, episode: int):
        super().__init__()

        self.series_id = series_id
        self.season = season
        self.episode = episode

        self.headers = {
            "accept": "*/*",
             "accept-encoding": "gzip, deflate, br",
             "accept-language": "he-IL,he;q=0.8",
             "cache-control": "no-cache",
             "content-length": "33",
             "cookie": "_ga=GA1.2.1213031456.1660079839; Sdarot=TODO: ADD COOKIE",
             "origin": "https://sdarot.tw",
             "pragma": "no-cache",
             "referer": "https://sdarot.tw/",
             "sec-fetch-dest": "empty",
             "sec-fetch-mode": "cors",
             "sec-fetch-site": "same-origin",
             "sec-gpc": "1",
             "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
             "x-requested-with": "XMLHttpRequest"
        }

# s.post("https://sdarot.tw/ajax/watch", data={"vast": "true"}, headers={"accept": "*/*", "accept-encoding": "gzip, deflate, br", "accept-language": "he-IL,he;q=0.8", "cache-control": "no-cache", "content-length": "9", "cookie": "_ga=GA1.2.1213031456.1660079839; Sdarot=Ox1wQDi%2CQuja3Da82SRsGAqdonazx0ke14WU0WeDeEh%2CteO-kxdfFtHHX0w8%2Cww5ubbZxMt2WISjD4xPjFPQ7SCjD6CeKJ3bN7AnKpOwl5uzrw1SHhJWXiUSp8TmBXHZ", "origin": "https://sdarot.tw", "pragma": "no-cache", "referer": "https://sdarot.tw/", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "sec-gpc": "1", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36", "x-requested-with": "XMLHttpRequest"}, cookies={"_ga": "GA1.2.1213031456.1660079839", "Sdarot": "Ox1wQDi%2CQuja3Da82SRsGAqdonazx0ke14WU0WeDeEh%2CteO-kxdfFtHHX0w8%2Cww5ubbZxMt2WISjD4xPjFPQ7SCjD6CeKJ3bN7AnKpOwl5uzrw1SHhJWXiUSp8TmBXHZ"})
 #        s.post("https://sdarot.tw/ajax/watch", data={"watch": "false", "token": "63fba34f83b5c", "serie": "1", "season": "2", "episode": "3", "type": "episode"}, headers={"accept": "application/json, text/javascript, */*; q=0.01", "accept-encoding": "gzip, deflate, br", "accept-language": "he-IL,he;q=0.8", "cache-control": "no-cache", "content-length": "71", "cookie": "_ga=GA1.2.1213031456.1660079839; Sdarot=Ox1wQDi%2CQuja3Da82SRsGAqdonazx0ke14WU0WeDeEh%2CteO-kxdfFtHHX0w8%2Cww5ubbZxMt2WISjD4xPjFPQ7SCjD6CeKJ3bN7AnKpOwl5uzrw1SHhJWXiUSp8TmBXHZ", "origin": "https://sdarot.tw", "pragma": "no-cache", "referer": "https://sdarot.tw/", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "sec-gpc": "1", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36", "x-requested-with": "XMLHttpRequest"}, cookies={"_ga": "GA1.2.1213031456.1660079839", "Sdarot": "Ox1wQDi%2CQuja3Da82SRsGAqdonazx0ke14WU0WeDeEh%2CteO-kxdfFtHHX0w8%2Cww5ubbZxMt2WISjD4xPjFPQ7SCjD6CeKJ3bN7AnKpOwl5uzrw1SHhJWXiUSp8TmBXHZ"})

        # self.client.get(f'https://sdarot.tw/watch/{series_id}')
        # print(self.client.cookies.values())

    def start(self):
        token = self.get_token()
        video_url = self.get_video_url(token)

    def get_token(self):
        r = self.client.post('https://sdarot.tw/ajax/watch', data={'preWatch': True,
                                                                   'SID': self.series_id,
                                                                   'season': self.season,
                                                                   'ep': self.episode}, headers=self.headers)
        print("TOKEN " + r.text)
        return r.text

    def get_video_url(self, token):
        r = self.client.post('https://sdarot.tw/ajax/watch', data={'watch': False,
                                                                   'token': token,
                                                                   'serie': self.series_id,
                                                                   'season': self.season,
                                                                   'episode': self.episode,
                                                                   'type': 'episode'}, headers=self.headers)
        print(r.json())
        return r.text
