from django.core.cache import cache
from ao3_web_reader_django.consts import ProcessesConsts


def get_keys_by_pattern(pattern):
    keys = cache._cache.get_client().keys(pattern)
    cleared_keys = []

    for key in keys:
        cleared_keys.append(key.decode().split(":")[2])

    return cleared_keys


def get_tasks_keys_by_type(task_type):
    keys = get_keys_by_pattern(f"*{task_type}*")

    return keys


def get_tasks_keys_by_type_and_owner_id(task_type, owner_id):
    keys = get_keys_by_pattern(f"*{owner_id}_{task_type}*")

    return keys


def get_task_data_by_key(key):
    data = cache.get(key)
    return data


def get_tasks_data_for_user(owner_id, task_type):
    keys = get_tasks_keys_by_type_and_owner_id(task_type, owner_id)
    data = [get_task_data_by_key(key) for key in keys]

    return data


def get_task_data_for_user_and_work(owner_id, task_type, work_id):
    keys = get_tasks_keys_by_type_and_owner_id(task_type, owner_id)
    data = None

    for key in keys:
        task_data = get_task_data_by_key(key)

        if task_data[ProcessesConsts.WORK_ID] == work_id:
            data = task_data
            break

    return data
