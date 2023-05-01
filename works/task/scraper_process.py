from celery_tasks.user_task_base import UserTaskBase
from utils import works_utils, models_utils
from works import models
from consts import ProcessesConsts


class ScraperProcess(UserTaskBase):
    def __init__(self):
        super().__init__()

        self.tag_name = None
        self.work_id = None
        self.work_title = None

        self.cache_data_timeout = 60

        self.task_progress = 0

    def run(self, owner_id, tag_name, work_id):
        self.owner_id = owner_id
        self.tag_name = tag_name
        self.work_id = work_id

        self.process_cache_key = f"{self.owner_id}_{self.get_process_name()}_{self.timestamp}"

        self.mainloop()

    def calc_progres(self, current_step, max_steps):
        self.task_progress = int(current_step * 100 / max_steps)

    def get_work_update_callback(self, current_step, total_steps):
        self.calc_progres(current_step, total_steps)
        self.update_process_data()

    def get_process_data(self):
        process_data = {
            ProcessesConsts.OWNER_ID: self.owner_id,
            ProcessesConsts.WORK_ID: self.work_id,
            ProcessesConsts.WORK_TITLE: self.work_title,
            ProcessesConsts.PROCESS_NAME: self.get_process_name(),
            ProcessesConsts.PROGRESS: self.task_progress,
        }

        return process_data

    def mainloop(self):
        self.work_title = works_utils.get_work_name(self.work_id)
        self.update_process_data()

        try:
            tag = models.Tag.objects.filter(owner_id=self.owner_id, name=self.tag_name).first()
            user_work = models.Work.objects.filter(owner_id=self.owner_id, work_id=self.work_id).first()

            work_data = works_utils.get_work(self.work_id, progress_callback=self.get_work_update_callback)
            work_description = works_utils.get_work_description(self.work_id)

            work = models_utils.create_work_model(work_data, self.owner_id, tag.id, work_description)

            if not user_work:
                work.save()
                chapters = models_utils.create_chapters_models(work.id, work_data)

                for chapter in chapters:
                    chapter.work_id = work.id
                    chapter.save()

                work.chapters.set(chapters)

        except Exception as e:
            self.logger.error(f"[{self.get_process_name()}] - {str(e)}")

        finally:
            self.finish_process()
