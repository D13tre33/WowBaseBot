from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Message


class ConfigMiddleware(BaseMiddleware):
    def __init__(self, config) -> None:
        self.config = config

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        data['config'] = self.config
        return await handler(event, data)


class DispatcherMiddleware(BaseMiddleware):
    def __init__(self, dispatcher: Dispatcher) -> None:
        self.dispatcher = dispatcher

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        data['dispatcher'] = self.dispatcher
        return await handler(event, data)
