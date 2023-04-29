import celery
import logging
from django.conf import settings
from django.core.cache import cache
from datetime import datetime
from consts import ProcessesConsts


class TaskBase(celery.Task):
    def __init__(self):
        self.timestamp = str(datetime.timestamp(datetime.now()))
        self.logger = logging.getLogger(settings.CELERY_LOGGER_NAME)

    def get_process_name(self):
        return type(self).__name__

    def mainloop(self):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        pass

    def save_to_cache(self, key, value):
        cache.set(key, value)

    def read_from_cache(self, key):
        return cache.get(key)

    def clear_process_cache_entry(self, key):
        cache.delete(key)

    def finish_process(self):
        self.clear_process_cache_entry(self.timestamp)

    def get_process_data(self):
        process_data = {
            ProcessesConsts.PROCESS_NAME: self.get_process_name(),
            ProcessesConsts.PROCESS_TIMESTAMP: self.timestamp,
        }

        return process_data

    def update_process_data(self):
        process_data = self.get_process_data()
        self.save_to_cache(self.timestamp, process_data)
