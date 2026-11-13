import json
from dataclasses import asdict

import pytest

from catalog.catalogclass import Catalog
from catalog.errors import DamagedFile, UnsupportedFormatVersion
from catalog.jsoncatalog import FORMAT_VERSION, load_catalog, save_catalog
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


def write_json(file, data):
    file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def test_json_round_trip(tmp_path):
    catalog = Catalog()
    film1 = make_media("id3")
    film2 = make_media(
        "id1",
        name="film2",
        category="Драма",
        date=1997,
        time=95,
        country="Франция",
    )

    catalog.add(film1)
    catalog.add(film2)

    file = tmp_path / "catalog.json"
    save_catalog(catalog, str(file))

    data = json.loads(file.read_text(encoding="utf-8"))

    assert data["format_version"] == FORMAT_VERSION
    assert data["items"] == [asdict(film1), asdict(film2)]

    loaded = load_catalog(str(file))

    assert loaded is not catalog
    assert list(loaded) == [film1, film2]


def test_damaged_json(tmp_path):
    file = tmp_path / "catalog.json"
    file.write_text('{"items": 124532', encoding="utf-8")

    with pytest.raises(DamagedFile):
        load_catalog(str(file))


def test_unsupported_format_version(tmp_path):
    file = tmp_path / "catalog.json"
    write_json(
        file,
        {
            "format_version": 2,
            "items": [],
        },
    )

    with pytest.raises(UnsupportedFormatVersion):
        load_catalog(str(file))


def test_invalid_entity_in_file(tmp_path):
    file = tmp_path / "catalog.json"

    entity = asdict(make_media("id1"))
    entity["time"] = 0

    write_json(
        file,
        {
            "format_version": FORMAT_VERSION,
            "items": [entity],
        },
    )

    with pytest.raises(DamagedFile):
        load_catalog(str(file))


def test_failed_load_does_not_change_catalog(tmp_path):
    catalog = Catalog()
    catalog.add(make_media("old"))

    before = [asdict(item) for item in catalog]

    good_entity = asdict(make_media("new"))
    bad_entity = asdict(make_media("broken"))
    bad_entity["time"] = 0

    file = tmp_path / "partially_invalid.json"
    write_json(
        file,
        {
            "format_version": FORMAT_VERSION,
            "items": [good_entity, bad_entity],
        },
    )

    with pytest.raises(DamagedFile):
        catalog = load_catalog(str(file))

    assert [asdict(item) for item in catalog] == before
    assert "new" not in catalog
