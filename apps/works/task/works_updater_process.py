from celery_tasks.background_task_base import BackgroundTaskBase
from apps.core.consts import ProcessesConsts, ChaptersConsts, UpdateMessagesConsts, TasksDelays
from utils import works_utils, models_utils
from apps.works import models
from apps.users import models
import time
from datetime import datetime


class WorksUpdaterProcess(BackgroundTaskBase):
    def __init__(self):
        super().__init__()

        self.cache_data_timeout = 60

        self.task_progress = 0

    def get_process_data(self):
        process_data = {
            ProcessesConsts.PROGRESS: self.task_progress,
            ProcessesConsts.PROCESS_NAME: self.get_process_name(),
            ProcessesConsts.PROCESS_TIMESTAMP: self.timestamp,
        }

        return process_data

    def run(self):
        if not self.check_if_same_task_running():
            self.process_cache_key = f"{self.get_process_name()}_{self.timestamp}"
            self.mainloop()

        else:
            self.logger.info(f"[{self.get_process_name()}] - skipped, already running")

    def check_if_new_chapter(self, chapter_id, work_chapters):
        status = False if chapter_id in [chapter.chapter_id for chapter in work_chapters] else True

        return status

    def get_chapter_by_id(self, chapters, chapter_id):
        result_chapter = None

        for chapter in chapters:
            if chapter.chapter_id == chapter_id:
                result_chapter = chapter
                break

        return result_chapter

    def check_chapters_for_removed_ones(self, chapters_struct, work):
        work_chapters_ids = [chapter.chapter_id for chapter in work.get_not_removed_chapters()]
        source_chapters_ids = [chapter.get(ChaptersConsts.ID) for chapter in chapters_struct]

        if all(work_chapters_ids) and all(source_chapters_ids):
            removed_chapters_ids = list(set(work_chapters_ids).difference(source_chapters_ids))

            for chapter_id in removed_chapters_ids:
                chapter = self.get_chapter_by_id(work.chapters, chapter_id)

                if chapter:
                    self.mark_chapter_as_removed(work, chapter)

    def update_chapters_order_ids(self, chapters):
        not_removed_chapters = [chapter for chapter in chapters if not chapter.was_removed]
        not_removed_chapters.sort(key=lambda chapter: chapter.order_id)

        for order_id, chapter in enumerate(not_removed_chapters):
            chapter.order_id = order_id
            chapter.save()

    def update_works(self, works):
        for work in works:
            if not works_utils.check_if_work_exists(work.work_id):
                work.was_removed = True
                work.save()

            time.sleep(TasksDelays.WORKS_EXIST_CHECK_JOBS_DELAY)

    def chapter_added(self, work, chapter):
        work.last_updated = datetime.now()

        update_message = models_utils.create_update_message_model(work.id,
                                                                  chapter.title,
                                                                  UpdateMessagesConsts.MESSAGE_ADDED_TYPE)

        update_message.save()

    def mark_chapter_as_removed(self, work, chapter):
        chapter.was_removed = True
        chapter.order_id = None
        work.last_updated = datetime.now()

        chapter.save()

        update_message = models_utils.create_update_message_model(work.id,
                                                                  chapter.title,
                                                                  UpdateMessagesConsts.MESSAGE_REMOVED_TYPE)

        update_message.save()

    def mainloop(self):
        try:
            processed_works = 0
            self.update_process_data()

            users = models.User.objects.all()
            works_count = sum([len(user.works.all()) for user in users])

            for user in users:
                works = user.works.all()
                self.update_works(works)

                for id, work in enumerate(works):
                    if not work.was_removed:
                        if id > 0:
                            time.sleep(TasksDelays.WORKS_UPDATER_JOBS_DELAY)

                        chapters_struct = works_utils.get_chapters_struct(work.work_id)

                        if len(chapters_struct) > 0:
                            for chapter_struct in chapters_struct:
                                if self.check_if_new_chapter(chapter_struct.get(ChaptersConsts.ID),
                                                             work.chapters.all()):

                                    chapter_struct_data = works_utils.get_chapter_data_struct(chapter_struct)

                                    new_chapter = models_utils.create_chapter_model(work.id, chapter_struct_data)
                                    new_chapter.save()

                                    self.chapter_added(work, new_chapter)

                            self.check_chapters_for_removed_ones(chapters_struct, work)
                            self.update_chapters_order_ids(work.chapters.all())

                        work.save()

                    processed_works += 1
                    self.task_progress = int(processed_works * 100 / works_count)

                    self.update_process_data()

        except Exception as e:
            self.logger.error(f"[{self.get_process_name()}] - {str(e)}")

        finally:
            self.finish_process()
