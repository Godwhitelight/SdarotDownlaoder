import threading

from tasks.sdarot.sdarot_download_task import SdarotDownloadTask

task = SdarotDownloadTask(1, 2, 3, sdarot_creds='username:password')
task.start()
