import os


class MessagesConsts:
    LOGIN_ERROR = "Wrong username or password"
    SCRAPING_PROCESS_STARTED = "Started work scraping"
    SCRAPING_PROCESS_FOR_WORK_ID_RUNNING = "Scraper process for {work_id} is running"
    CANT_ACCESS_WORK = "Can't access work"
    WORK_ALREADY_ADDED = "Work already added"
    WORK_REMOVED = "Work removed successfully"
    TAG_ALREADY_ADDED = "Tag already added"
    ADDED_TAG = "New tag has been added: {tag_name}"
    TAG_DOESNT_EXIST = "Tag doesn't exist"
    TAG_REMOVED = "Tag removed"
    CHAPTERS_MARKED_AS_COMPLETED = "All chapters of '{work_name}' marked as completed"
    CHAPTERS_MARKED_AS_INCOMPLETE = "All chapters of '{work_name}' marked as incomplete"


class PaginationConsts:
    UPDATE_MESSAGES_PER_PAGE = 25
    WORKS_PER_PAGE = 10


class AO3Consts:
    AO3_URL = "https://archiveofourown.org"
    AO3_WORKS_URL = AO3_URL + "/works/{work_id}"
    AO3_WORKS_NAVIGATION_URL = AO3_URL + "/works/{work_id}/navigate"


class ProcessesConsts:
    PID = "pid"
    OWNER_ID = "owner_id"
    WORK_ID = "work_id"
    WORK_TITLE = "work_title"
    PROCESS_NAME = "process_name"
    PROGRESS = "progress"
    PROCESS_TIMESTAMP = "timestamp"

    IS_RUNNING = "is_running"


class WorksConsts:
    NAME = "name"
    URL = "url"
    ID = "id"
    WORK_ID = "work_id"
    CHAPTERS_DATA = "chapters_data"
    CONTENT = "content"


class ChaptersConsts:
    NAME = "name"
    URL = "url"
    ID = "id"
    CONTENT = "content"
    DATE = "date"
    ORDER_ID = "order_id"
    WORK_ID = "work_id"


class UpdateMessagesConsts:
    MESSAGE_ADDED_TYPE = "added"
    MESSAGE_REMOVED_TYPE = "removed"


class TasksDelays:
    WORKS_UPDATER_JOBS_DELAY = 5
    WORKS_EXIST_CHECK_JOBS_DELAY = 5
    WORKS_UPDATER_INTERVAL = int(os.getenv("WORKS_UPDATER_INTERVAL", 7200))
