import asyncio
from contextlib import suppress
from datetime import datetime
from typing import Optional, List, Any
from uuid import uuid4

from aiogram import Dispatcher, Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Update, CallbackQuery, User

from tgbot.misc.base import Base


class TaskData(CallbackData, prefix="form"):
    uuid: str
    type: str


class Task(Base):

    def __init__(self, dict_: dict):
        super().__init__()

        uuid: str = dict_.get("uuid", str(uuid4()))
        callback_data: str = dict_.get("callback_data", TaskData(uuid=uuid, type="default").pack())
        start_datetime: Optional[str] = dict_.get("start_datetime", None)
        interval_datetime: Optional[str] = dict_.get("interval_datetime", None)
        finish_datetime: Optional[str] = dict_.get("finish_datetime", None)
        run_on_complete: bool = dict_.get("run_on_complete", True)
        completed: bool = dict_.get("completed", False)
        is_started: bool = dict_.get("is_started", False)
        exists: bool = dict_.get("exists", False)

        self.uuid = uuid
        self.callback_data = callback_data
        self.start_datetime = start_datetime
        self.interval_datetime = interval_datetime
        self.finish_datetime = finish_datetime
        self.run_on_complete = run_on_complete
        self.completed = completed
        self.is_started = is_started
        self.exists = exists

        self._task = None

        self.storage: Optional[Any] = None
        self.scheduler: Optional[Scheduler] = None
        self.dispatcher: Optional[Dispatcher] = None
        self.bot: Optional[Bot] = None

        dict.__init__(
            self,
            uuid=uuid,
            callback_data=callback_data,
            start_datetime=start_datetime,
            interval_datetime=interval_datetime,
            finish_datetime=finish_datetime,
            is_started=is_started,
            run_on_complete=run_on_complete,
            completed=completed,
            exists=exists,
        )

    def set_env(self, storage, scheduler_: 'Scheduler', dp: Dispatcher, bot: Bot):
        self.storage = storage
        self.scheduler = scheduler_
        self.dispatcher = dp
        self.bot = bot

    async def start(self) -> bool:
        if not self.is_started and not self.completed:
            current_timestamp = datetime.now().timestamp()
            finish_timestamp = datetime.strptime(self.finish_datetime, '%Y/%m/%d %H:%M:%S').timestamp()
            if current_timestamp < finish_timestamp:
                self.is_started = True
                # Start task to call func periodically:
                self._task = asyncio.ensure_future(self._try_run())
                return True
            else:
                await self._try_run()
                self.completed = True
                self['completed'] = True  # TODO почему так
                await self._save()
                return False
        return False

    async def stop(self):
        if self.is_started:
            self.is_started = False
            # Stop task and await it stopped:
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task

    async def force_stop(self, condition: bool = True):
        if condition and self.run_on_complete:
            await self._run()
        self.completed = True
        self['completed'] = True
        await self._save()

    async def _save(self):
        if type(self.scheduler) is Scheduler:
            self.scheduler.save_task(self)
            await self.storage.save_scheduler(self.scheduler)  # TODO разобрать с типа (по факту просто сделать нормальное хранилище)
            # await Storage.save_scheduler(self.scheduler)

    def _next_time(self, step: int = 1) -> float:
        if not self.completed:
            current_timestamp: float = datetime.now().timestamp()
            finish_timestamp: float = datetime.strptime(self.finish_datetime, '%Y/%m/%d %H:%M:%S').timestamp()
            if type(self.interval_datetime) is str:
                # interval_timestamp: float = datetime.strptime(self.interval_datetime, '%Y/%m/%d %H:%M:%S').timestamp()
                interval_timestamp: float = float(self.interval_datetime)
                next_timestamp = interval_timestamp * step + current_timestamp  # TODO где-то тут кроется причина того, что задача выполняется лишний раз
                if next_timestamp <= finish_timestamp:
                    return next_timestamp - current_timestamp
            if current_timestamp < finish_timestamp:
                return finish_timestamp - current_timestamp
        return -1

    async def _try_run(self):
        while True:
            next_time = self._next_time()
            is_completed = next_time < 0
            double_next_time = self._next_time(2)
            is_last_run = not is_completed and double_next_time < 0
            await asyncio.sleep(next_time)
            if is_completed:
                if not self.completed:
                    await self.force_stop(not self.is_started)
                    # if not self.is_started and self.run_on_complete:
                    #     await self._run()
                    # self.completed = True
                    # self['completed'] = True  # TODO почему так
                    # await self._save()
                await self.stop()
                break  # TODO не уверен что нужен
            else:
                if is_last_run:
                    await self.force_stop()
                    # if self.run_on_complete:
                    #     await self._run()
                    # await self.stop()
                    # self.completed = True
                    # self['completed'] = True  # TODO почему так
                    # await self._save()
                    break  # TODO не уверен что нужен
                else:
                    await self._run()

    async def _run(self):
        if type(self.dispatcher) is Dispatcher and type(self.bot) is Bot:
            await self.dispatcher.feed_update(
                bot=self.bot,
                update=Update(
                    update_id=self.bot.id,
                    message=None,
                    callback_query=CallbackQuery(
                        id=self.bot.id,
                        from_user=User(
                            id=self.bot.id,
                            is_bot=True,
                            first_name="qwe"
                        ),
                        chat_instance=str(self.bot.id),
                        data=self.callback_data
                    )
                )
            )


class Scheduler(Base):

    def __init__(self, global_data: dict):
        super().__init__()

        scheduler_: dict = global_data.get("scheduler", {})

        self.scheduler = scheduler_

        dict.__init__(self, scheduler=scheduler_)

    def get_tasks(self) -> List[Task]:
        result: List[Task] = list()
        for task_ in self.scheduler.values():
            result.append(task(**task_))
        return result
        # return list(map(lambda task_: task(**task_), self.scheduler.values()))
        # start_datetime = datetime.now()
        # task_: dict = {
        #     "uuid": str(uuid4()),
        #     "prefix": "task",
        #     "start_datetime": start_datetime.strftime('%Y/%m/%d %H:%M:%S'),
        #     "interval_datetime": "30",
        #     "finish_datetime": (start_datetime + timedelta(minutes=5)).strftime('%Y/%m/%d %H:%M:%S'),
        #     "exists": True
        # }
        # # return list(task(
        # #     **task_,
        # #     callback_data=CallbackData(**task_).pack(),
        # # ))
        # result: List[Task] = list()
        # result.append(task(
        #     **task_,
        #     callback_data=TaskData(
        #         uuid=task_.get("uuid"),
        #         type="test",
        #     ).pack(),
        # ))
        # return result

    def get_task(self, uuid_: str) -> Task:
        return task(**self.scheduler.get(uuid_, {}))

    def save_task(self, task_: Task):
        # self.scheduler[task_.uuid] = task_
        self['scheduler'][task_.uuid] = task_  # TODO ... ???


def task(**kwargs) -> Task:
    return Task(kwargs)


def scheduler(**kwargs) -> Scheduler:
    return Scheduler(kwargs)
