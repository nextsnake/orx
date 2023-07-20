# cython: language_level=3
# Copyright (c) 2023 tag-epic
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import asyncio
import typing as t

from nextcore.gateway import ShardManager
from nextcore.http import BotAuthentication, HTTPClient

from .events.dispatcher import ClassDispatcher
from .flags import Intents
from .models import Model
from .state import DEFAULT_MODELS, State


class Bot:
    """A class representing a Discord bot controlled by the user."""

    def __init__(
        self,
        token: str,
        intents: Intents,
        state_cls: t.Type[State] = State,
        models: dict[Model, Model] = DEFAULT_MODELS,
        shards: int | None = None,
        shard_ids: list[int] | None = None,
        **state_kwargs
    ) -> None:
        mods = DEFAULT_MODELS
        for k, v in models.items():
            mods[k] = v

        self._state = state_cls(token, mods, **state_kwargs)
        self._auth = BotAuthentication(token)
        self._http_client = HTTPClient()
        self._shard_manager = ShardManager(
            self._auth,
            int(intents),
            self._http_client,
            shard_count=shards,
            shard_ids=shard_ids,
        )
        self.intents = intents
        self._dispatcher = ClassDispatcher()

    async def _on_gateway_event(self, event: str, data: dict[str, t.Any]) -> None:
        print(event)

    async def connect(self, block: bool = True) -> None:
        self._shard_manager.event_dispatcher.add_listener(
            self._on_gateway_event, event_name=None
        )
        await self._http_client.setup()
        await self._shard_manager.connect()

        if block:
            try:
                await asyncio.Future()
            except (asyncio.CancelledError, KeyboardInterrupt):
                await self._shard_manager.close()
                await self._http_client.close()
                self._dispatcher.close()

    def start(self, *, debug: bool = False) -> None:
        asyncio.run(self.connect(), debug=debug)
