import threading

from tasks.sdarot.sdarot_download_task import SdarotDownloadTask

task = SdarotDownloadTask(1, 2, 3, sdarot_creds='abuser159:abuser')
task.start()
