from celery_tasks.task_base import TaskBase
from consts import ProcessesConsts


class UserTaskBase(TaskBase):
    def __init__(self):
        self.owner_id = None

        super().__init__()

    def get_process_data(self):
        process_data = {
            ProcessesConsts.OWNER_ID: self.owner_id,
            ProcessesConsts.PROCESS_NAME: self.get_process_name(),
            ProcessesConsts.PROCESS_TIMESTAMP: self.timestamp,
        }

        return process_data
