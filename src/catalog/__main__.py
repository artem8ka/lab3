from catalog.catalogclass import Catalog
from catalog.jsoncatalog import load_catalog, save_catalog
from catalog.mediaclass import Media


def main() -> None:
    print("Демонстрация, добавляем 2 фильма в каталог")
    catalog = Catalog()
    for item_id, name in [("id1001", "Колобок"), ("id1002", "Колобок-2")]:
        catalog.add(
            Media(
                id=item_id,
                name=name,
                category="Комедия",
                date=2026,
                time=109,
                country="Россия",
            )
        )

    save_catalog(catalog, "demo_catalog.json")
    loaded = load_catalog("demo_catalog.json")
    print(f"В новом каталоге материалов: {len(loaded)}")
    for media in loaded:
        print(f"{media.id}: {media.name}, {media.time} мин.")


if __name__ == "__main__":
    main()
