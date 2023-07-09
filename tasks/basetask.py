import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from requests import HTTPError
from util.dns_adapter import HostHeaderSSLAdapter


class BaseTask:
    def __init__(self):
        self.client = requests.session()
        self.headers = {

        }

        self.client.mount('https://', HostHeaderSSLAdapter())

    def start(self):
        pass


class BaseDownloadTask(BaseTask):
    def __init__(self):
        super().__init__()
        self.chunk_size = 4096 * 4096
        self.url = None

    def make_headers(self, start):
        end = start + self.chunk_size - 1
        return {
            'Range': f'bytes={start}-{end}',
            **self.headers
        }

    def download_part(self, url, headers, partfile):
        while True:
            try:
                response = self.client.get(url, headers=headers, timeout=999999, stream=True)

                with open(partfile, 'wb') as f:
                    for chunk in response.iter_content(2048):  # Try to change this to 1024 to increse speed
                        if chunk:
                            f.write(chunk)
                break
            except HTTPError:
                pass

    def download(self, url, filename: str = None) -> bool:
        self.url = url

        if not filename:
            filename = url.split('/')[-1].split('?')[0]

        response = self.client.get(url, stream=True)
        if response.status_code != 200:
            print('error', response.status_code)
            return False

        file_size = int(response.headers.get('content-length', 0))

        chunks = range(0, file_size, self.chunk_size)
        my_iter = [(url, self.make_headers(chunk), f'{filename}.part{i}') for i, chunk in enumerate(chunks)]

        with ThreadPoolExecutor(max_workers=7) as executor:
            jobs = [executor.submit(self.download_part, *i) for i in my_iter]
            start = time.time()
            print('start', file_size)
            for job in as_completed(jobs):
                size = job.result()

            print(f'{time.time() - start:.5}', size)

        with open(filename, 'wb') as outfile:
            for i in range(len(chunks)):
                chunk_path = f'{filename}.part{i}'
                with open(chunk_path, 'rb') as s:
                    outfile.write(s.read())
                os.remove(chunk_path)

        return True
