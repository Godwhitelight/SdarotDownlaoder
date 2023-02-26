import requests


class BaseTask:
    def __init__(self):
        self.client = requests.session()
        self.client.verify = False

    def start(self):
        pass


class BaseDownloadTask(BaseTask):
    def __init__(self):
        super().__init__()
        # self.url = url

    def download(self, url):
        # TODO: download the file
        pass
