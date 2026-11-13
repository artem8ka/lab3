from collections.abc import Iterator

from catalog.errors import DuplicateID, InvalidEntity, ObjectNotFound
from catalog.mediaclass import Media


class Catalog:
    def __init__(self):
        self._items: dict[str, Media] = {}

    def add(self, item: Media) -> None:
        if not isinstance(item, Media):
            raise InvalidEntity
        if item.id in self._items:
            raise DuplicateID
        self._items[item.id] = item

    def get(self, item_id: str) -> Media:
        if item_id not in self._items:
            raise ObjectNotFound
        return self._items[item_id]

    def remove(self, item_id: str) -> None:
        if item_id not in self._items:
            raise ObjectNotFound
        del self._items[item_id]

    def find_by_category(self, category: str) -> list[Media]:
        media_list = []
        for item in self:
            if item.category == category:
                media_list.append(item)
        return media_list

    def find_by_name(self, query: str) -> list[Media]:
        media_list = []
        for item in self:
            if query.lower() in item.name.lower():
                media_list.append(item)
        return media_list

    def __len__(self):
        return len(self._items)

    def __iter__(self) -> Iterator[Media]:
        ##Итерация по каталогу в порядке добавления объектов
        return iter(self._items.values())

    def __contains__(self, item_id: str) -> bool:
        return item_id in self._items
