from celery_tasks.task_base import TaskBase
from apps.core.consts import ProcessesConsts


class BackgroundTaskBase(TaskBase):
    def __init__(self):
        super().__init__()

    def get_process_data(self):
        process_data = {
            ProcessesConsts.PROCESS_NAME: self.get_process_name(),
            ProcessesConsts.PROCESS_TIMESTAMP: self.timestamp,
        }

        return process_data
