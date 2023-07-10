import time

import tls_client

from tasks.basetask import BaseDownloadTask
from tasks.sdarot.sdarot_task import SdarotTask


class SdarotDownloadTask(SdarotTask, BaseDownloadTask):
    def __init__(self, series_id: int, season: int, episode: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.series_id = series_id
        self.season = season
        self.episode = episode

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
