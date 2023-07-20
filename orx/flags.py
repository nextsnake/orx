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


# TODO: test whether performance of these flags are subnominal

import typing as t
from enum import IntFlag

T = t.TypeVar("T")


class BaseFlag(IntFlag):
    @classmethod
    def all(cls: t.Type[T]) -> T:
        value: int = 0

        for name in dir(cls):
            attr = getattr(cls, name)

            if isinstance(attr, BaseFlag):
                value += int(attr)

        return cls(value)


class Intents(BaseFlag):
    guilds = 1 << 0
    guild_members = 1 << 1
    guild_moderation = 1 << 2
    guild_emojis_and_stickers = 1 << 3
    guild_integrations = 1 << 4
    guild_webhooks = 1 << 5
    guild_invites = 1 << 6
    guild_voice_states = 1 << 7
    guild_presences = 1 << 8
    guild_messages = 1 << 9
    guild_message_reactions = 1 << 10
    guild_message_typing = 1 << 11
    direct_messages = 1 << 12
    direct_message_reactions = 1 << 13
    direct_message_typing = 1 << 14
    message_content = 1 << 15
    guild_scheduled_events = 1 << 16
    auto_moderation_configuration = 1 << 20
    auto_moderation_execution = 1 << 21
