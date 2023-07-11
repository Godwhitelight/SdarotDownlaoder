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

    def start(self, location: str = None):
        token = self.get_token()
        self.sleep(31)
        video_url = self.get_video_url(token)

        if video_url == '404':
            return False, '404'

        if video_url == 'error':
            return self.start()

        # print(video_url)
        success = self.download(video_url, location)
        return success, video_url

    def sleep(self, seconds):
        for i in range(seconds * 100):
            # print(f"\rSleeping for {(seconds - (i / 100)):.5} seconds", end='', flush=True)
            time.sleep(0.01)

        # print('\rDone Sleeping!')

    def get_token(self):
        r = self.client.post('https://sdarot.tw/ajax/watch', data={'preWatch': True,
                                                                   'SID': self.series_id,
                                                                   'season': self.season,
                                                                   'ep': self.episode})

        return r.text

    def get_video_url(self, token):
        r = self.client.post('https://sdarot.tw/ajax/watch', data={'watch': False,
                                                                   'token': token,
                                                                   'serie': self.series_id,
                                                                   'season': self.season,
                                                                   'episode': self.episode,
                                                                   'type': 'episode'})

        if 'error' in r.json():
            return '404' if r.json()['error'] == 'מצטערים, הפרק לא קיים במערכת.' else 'error'

        print(sorted(r.json()['watch'], key=lambda x: int(x)))
        return 'https:' + r.json()['watch']['480']
