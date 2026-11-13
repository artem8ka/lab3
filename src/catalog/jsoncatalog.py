import json
from dataclasses import asdict

from pydantic import ValidationError

from catalog.catalogclass import Catalog
from catalog.errors import (
    DamagedFile,
    DuplicateID,
    InvalidEntity,
    UnsupportedFormatVersion,
)
from catalog.mediaclass import Media

FORMAT_VERSION = 1


def save_catalog(catalog: Catalog, file: str) -> None:
    data = {"format_version": FORMAT_VERSION, "items": []}
    for item in catalog:
        data["items"].append(asdict(item))

    with open(file, "w", encoding="utf-8") as catalog_file:
        json.dump(data, catalog_file, ensure_ascii=False, indent=4)


def load_catalog(file: str) -> Catalog:
    try:
        with open(file, "r", encoding="utf-8") as load_file:
            data = json.load(load_file)
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise DamagedFile

    if not (type(data) is dict):
        raise DamagedFile

    if "format_version" not in data:
        raise DamagedFile

    if not (type(data["format_version"]) is int):
        raise DamagedFile

    if data["format_version"] != FORMAT_VERSION:
        raise UnsupportedFormatVersion

    if "items" not in data:
        raise DamagedFile

    if not (type(data["items"]) is list):
        raise DamagedFile

    new_catalog = Catalog()
    for item in data["items"]:
        if not (type(item) is dict):
            raise DamagedFile
        try:
            media = Media(**item)
            new_catalog.add(media)
        except (ValidationError, InvalidEntity, DuplicateID):
            raise DamagedFile
    return new_catalog
