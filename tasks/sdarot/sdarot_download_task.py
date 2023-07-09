import time

import tls_client

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
            "cookie": "Sdarot=S5TmQUWUOjTQVeVr4GKSWDIUz0YwktHWcDfFC9eu%2CWtTV2rULFJI1n499R1B1k3JEbYl6IpkWnqhLDX01GXxeyn%2Cx0qTXDUyc55wt2D0VPJ1ycqmH3gMYu1UFPLAzthk",
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
        self.client.headers = self.headers

    def start(self):
        token = self.get_token()
        self.sleep(31)
        video_url = self.get_video_url(token)
        if video_url == 'error':
            self.start()
            return

        print(video_url)
        success = self.download(video_url)

    def sleep(self, seconds):
        for i in range(seconds * 100):
            print(f"\rSleeping for {(seconds - (i / 100)):.5} seconds", end='', flush=True)
            time.sleep(0.01)

        print('\rDone Sleeping!')

    def get_token(self):
        r = self.client.post('https://sdarot.tw/ajax/watch', data={'preWatch': True,
                                                                   'SID': self.series_id,
                                                                   'season': self.season,
                                                                   'ep': self.episode})
        print("Obtained watch token " + r.text)
        return r.text

    def get_video_url(self, token):
        r = self.client.post('https://sdarot.tw/ajax/watch', data={'watch': False,
                                                                   'token': token,
                                                                   'serie': self.series_id,
                                                                   'season': self.season,
                                                                   'episode': self.episode,
                                                                   'type': 'episode'})
        if 'error' in r.json():
            print(r.json())
            return 'error'

        return 'https:' + r.json()['watch']['480']
