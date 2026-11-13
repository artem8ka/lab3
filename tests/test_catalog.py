import pytest

from catalog.catalogclass import Catalog
from catalog.errors import DuplicateID, InvalidEntity, ObjectNotFound
from catalog.mediaclass import Media


def make_media(
    id, name="Колобок", category="Комедия", date=2026, time=109, country="Россия"
):
    media = Media(
        id=id,
        name=name,
        category=category,
        date=date,
        time=time,
        country=country,
    )
    return media


def test_add_get_remove():
    catalog = Catalog()
    media = make_media("id1")

    assert len(catalog) == 0

    catalog.add(media)

    assert len(catalog) == 1
    assert media.id in catalog
    assert catalog.get(media.id) == media

    catalog.remove(media.id)

    assert len(catalog) == 0
    assert media.id not in catalog


def test_invalid_entity():
    catalog = Catalog()

    with pytest.raises(InvalidEntity):
        catalog.add(124325)

    assert len(catalog) == 0


def test_duplicate_id():
    catalog = Catalog()
    film1 = make_media("id1", name="film1")
    film2 = make_media("id1", name="film2")

    catalog.add(film1)

    with pytest.raises(DuplicateID):
        catalog.add(film2)

    assert len(catalog) == 1
    assert catalog.get("id1") == film1


def test_object_not_found():
    catalog = Catalog()

    with pytest.raises(ObjectNotFound):
        catalog.get("iddd")

    with pytest.raises(ObjectNotFound):
        catalog.remove("iddd")

    assert len(catalog) == 0


def test_find_by_category():
    catalog = Catalog()
    film1 = make_media("id1", category="Комедия")
    film2 = make_media("id2", category="Драма")
    film3 = make_media("id3", category="Комедия")

    for media in (film1, film2, film3):
        catalog.add(media)

    assert catalog.find_by_category("Комедия") == [film1, film3]
    assert catalog.find_by_category("Ужасы") == []


def test_find_by_name():
    catalog = Catalog()
    film1 = make_media("id1")
    film2 = make_media("id2", name="Название1")
    film3 = make_media("id3", name="Название2")

    for media in (film1, film2, film3):
        catalog.add(media)

    assert catalog.find_by_name("НАЗв") == [film2, film3]
    assert catalog.find_by_name("абвгд") == []


def test_iteration_order():
    catalog = Catalog()
    media_list = [
        make_media("id3"),
        make_media("id1"),
        make_media("id2"),
    ]

    for media in media_list:
        catalog.add(media)

    assert list(catalog) == media_list
