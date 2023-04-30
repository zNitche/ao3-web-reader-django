import celery
import logging
from django.conf import settings
from django.core.cache import cache
from datetime import datetime
from consts import ProcessesConsts


class TaskBase(celery.Task):
    def __init__(self):
        self.timestamp = str(datetime.timestamp(datetime.now()))
        self.process_cache_key = f"{self.get_process_name()}_{self.timestamp}"
        self.cache_data_timeout = 30

        self.logger = logging.getLogger(settings.CELERY_LOGGER_NAME)

    def get_process_name(self):
        return type(self).__name__

    def run(self, *args, **kwargs):
        self.mainloop()

    def mainloop(self):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        pass

    def save_to_cache(self, key, value):
        cache.set(key, value, self.cache_data_timeout)

    def read_from_cache(self, key):
        return cache.get(key)

    def clear_process_cache_entry(self, key):
        cache.delete(key)

    def finish_process(self):
        self.clear_process_cache_entry(self.process_cache_key)

    def get_process_data(self):
        process_data = {
            ProcessesConsts.PROCESS_NAME: self.get_process_name(),
            ProcessesConsts.PROCESS_TIMESTAMP: self.timestamp,
        }

        return process_data

    def update_process_data(self):
        process_data = self.get_process_data()
        self.save_to_cache(self.process_cache_key, process_data)
