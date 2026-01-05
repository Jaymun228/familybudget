from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category, Subcategory
from app.utils.constants import CategoryKind


DEFAULT_CATEGORIES: dict[str, list[str]] = {
    "Транспорт": ["Такси", "Автобус", "Метро", "Электричка", "Другой транспорт"],
    "Еда": ["Обед (работа)", "Перекус", "Фаст-Фуд", "Сладости", "Еда вне работы"],
    "Рестораны": ["Бар", "Ресторан", "Бургерная", "Доставка", "Кальянная"],
    "Алкоголь": ["Вино", "Пиво", "Сидр", "Крепкое", "Закуски"],
    "Подарки": ["Родственники", "Друзья", "Работа"],
    "Продукты": [],
    "Здоровье, красота, гигиена": [],
    "Одежда": [],
    "Творчество, книги, обучение": [],
    "Кино, театры, музеи": [],
    "Связь": [],
    "Прочее": [],
}


async def ensure_seed_categories(session: AsyncSession) -> None:
    existing = await session.scalar(select(Category.id).limit(1))
    if existing:
        return
    for sort, (cat_name, subs) in enumerate(DEFAULT_CATEGORIES.items(), start=1):
        cat = Category(name=cat_name, kind=CategoryKind.DAILY, sort_order=sort)
        session.add(cat)
        await session.flush()
        for sub_sort, sub_name in enumerate(subs, start=1):
            session.add(Subcategory(category_id=cat.id, name=sub_name, sort_order=sub_sort))
    await session.commit()
