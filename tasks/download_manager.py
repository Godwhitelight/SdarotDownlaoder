import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import cycle
from typing import List

from tasks.sdarot.sdarot_download_task import SdarotDownloadTask


class DownloadManager:
    def __init__(self, tasks: List[dict], accounts: list = None):
        self.accounts = accounts or [i.strip() for i in open('sdarot_creds.txt', 'w').readlines()]
        self.tasks = tasks
        self._status = 'Waiting in queue...'

    def start(self):
        acc = cycle(self.accounts)
        with ThreadPoolExecutor(max_workers=len(self.accounts)) as executor:
            self._status = 'Starting...'
            jobs = [executor.submit(SdarotDownloadTask(i['series_id'], i['season'], i['episode'],
                                                       sdarot_creds=next(acc).strip()).start) for i in self.tasks]
            start = time.time()
            done_counter = 0
            self._status = f'{done_counter}/{len(self.tasks)}'
            for job in as_completed(jobs):
                done_counter += 1
                self._status = f'{done_counter}/{len(self.tasks)}'
                job.result()

            self._status = 'done'
            print(f'{time.time() - start:.5}')

    @property
    def status(self):
        return self._status


if __name__ == '__main__':
    DownloadManager([{'series_id': 1, 'season': 1, 'episode': 2}], accounts=["abuser122:abuser"]).start()
