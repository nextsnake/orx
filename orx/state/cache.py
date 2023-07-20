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


import typing as t


class _stored:
    __slots__ = ("parents", "id", "storing")

    def __init__(self, parents: set[t.Any], self_id: t.Any, storing: t.Any) -> None:
        self.parents = parents
        self.id = self_id
        self.storing = storing


T = t.TypeVar("T")


class Store:
    __slots__ = ("_store", "max_items")

    _store: set[_stored]

    def __init__(self, max_items: int | None = None) -> None:
        self._store = set()
        self.max_items = max_items

    async def fetch_one(self, parents: list[t.Any], id: t.Any) -> t.Any | None:
        ps = set(parents)

        for store in self._store:
            if store.parents & ps and store.id == id:
                return store.storing

    async def fetch_from_id(self, id: t.Any) -> tuple[set[t.Any], t.Any] | None:
        for store in self._store:
            if store.id == id:
                return store.parents, store.storing

    async def insert(self, parents: list[t.Any], id: t.Any, data: t.Any) -> None:
        if self.max_items and len(self._store) == self.max_items:
            self._store = set()

        self._store.add(_stored(set(parents), id, data))

    async def replace(
        self, parents: list[t.Any], id: t.Any, data: t.Any
    ) -> t.Any | None:
        ps = set(parents)

        for store in self._store:
            if store.parents & ps and store.id == id:
                old_data = store.storing
                self._store.discard(store)
                store.storing = data
                self._store.add(store)
                return old_data
        else:
            if self.max_items and len(self._store) == self.max_items:
                self._store = {}

            store = _stored(set(parents), id, data)
            self._store.add(store)

    async def delete(
        self, parents: list[t.Any], id: t.Any, type: t.Type[T] | T = None
    ) -> T:
        ps = set(parents)

        for store in self._store:
            if store.parents & ps or store.id == id:
                self._store.remove(store)
                return store

    async def fetch_all(self):
        for store in self._store:
            yield store.storing

    async def fetch_children(self, parents: list[t.Any]):
        ps = set(parents)

        for store in self._store:
            if store.parents & ps:
                yield store.storing

    async def clear(self) -> None:
        self._store.clear()

    async def delete_children(self, parents: list[t.Any]) -> None:
        ps = set(parents)

        for store in self._store:
            if store.parents & ps:
                self._store.remove(store)
