from typing import Self

from tasks.basetask import BaseDownloadTask


class SdarotDownloadTask(BaseDownloadTask):
    def __init__(self, series_id: int, season: int, episode: int):
        super().__init__()

        self.series_id = series_id
        self.season = season
        self.episode = episode

        self.headers = {
            'origin': 'https://sdarot.tw',
            'pragma': 'no-cache',
            'referer': 'https://sdarot.tw/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        self.client.get(f'https://sdarot.tw/watch/{series_id}')
        print(self.client.cookies.values())
        self.token = self.get_token()


    def start(self):
        pass

    def get_token(self):
        r = self.client.post('https://sdarot.tw/ajax/watch', data={'preWatch': True,
                                                                   'SID': self.series_id,
                                                                   'season': self.season,
                                                                   'ep': self.episode}, cookies={'Sdarot': 'Ox1wQDi%2CQuja3Da82SRsGAqdonazx0ke14WU0WeDeEh%2CteO-kxdfFtHHX0w8%2Cww5ubbZxMt2WISjD4xPjFPQ7SCjD6CeKJ3bN7AnKpOwl5uzrw1SHhJWXiUSp8TmBXHZ'})
        print("TOKEN " + r.text)
        return r.text
