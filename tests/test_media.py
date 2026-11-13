import pytest
from pydantic import ValidationError

from catalog.mediaclass import Media


def test_create_valid_entity():
    media = Media(
        id="id1001",
        name="Колобок",
        category="Комедия",
        date=2026,
        time=109,
        country="Россия",
    )

    assert media.id == "id1001"
    assert media.time == 109
    assert media.country == "Россия"


def test_invalid_time():
    with pytest.raises(ValidationError):
        Media(
            id="id1002",
            name="Test film",
            category="Category",
            date=2020,
            time=0,
            country="Counrty",
        )


def test_empty_field():
    with pytest.raises(ValidationError):
        Media(
            id="id1003",
            name="     ",
            category="Category",
            date=2020,
            time=94,
            country="Counrty",
        )


def test_invalid_year():
    with pytest.raises(ValidationError):
        Media(
            id="id1004",
            name="Film Name",
            category="Category",
            date=2028,
            time=100,
            country="Counrty",
        )
