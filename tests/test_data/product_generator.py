"""Генератор реалистичных тестовых данных для продуктов."""
import random
import string
from dataclasses import dataclass


@dataclass
class ProductData:
    """Сгенерированные данные продукта."""
    article: str
    name: str
    description: str
    category: str
    brand: str
    marketplace: str
    price: str
    product_link: str
    task_type: str = "Товар"


# ── Шаблоны продуктов по категориям ───────────────────────────

PRODUCT_TEMPLATES = [
    {
        "category": "Строительство и ремонт",
        "brands": ["FEDAST", "HILTI", "Makita", "Bosch", "DeWALT"],
        "marketplace": "ВсеИнструменты",
        "names": [
            "Гвозди для монтажного пистолета {size} мм",
            "Саморезы кровельные оцинкованные {size} мм",
            "Дюбель-гвоздь забивной {size} мм",
            "Анкер клиновой оцинкованный {size} мм",
            "Шуруп универсальный потайной {size} мм",
        ],
        "descriptions": [
            "Профессиональный крепёж для строительных и монтажных работ. Оцинкованное покрытие обеспечивает защиту от коррозии. Упаковка {qty} шт.",
            "Высокопрочный крепёж из углеродистой стали. Подходит для работы с бетоном, кирпичом и деревом. В упаковке {qty} шт.",
            "Надёжный строительный крепёж с антикоррозийным покрытием. Рекомендован для наружных работ. Комплект {qty} шт.",
        ],
        "link_base": "https://www.vseinstrumenti.ru/product/",
        "sizes": [14, 16, 20, 25, 30, 35, 40, 50, 60, 75],
        "qty": [100, 200, 500, 1000],
    },
    {
        "category": "Электроника",
        "brands": ["Xiaomi", "Samsung", "Baseus", "Anker", "UGREEN"],
        "marketplace": "Ozon",
        "names": [
            "Беспроводная зарядка {brand} {power}W быстрая",
            "USB-C кабель {brand} {length}м плетёный",
            "Повербанк {brand} {capacity} мАч быстрая зарядка",
            "Bluetooth наушники {brand} TWS с шумоподавлением",
            "Сетевое зарядное устройство {brand} {power}W GaN",
        ],
        "descriptions": [
            "Компактный и стильный аксессуар от {brand}. Совместим со всеми современными устройствами. Гарантия производителя 12 месяцев.",
            "Оригинальный аксессуар {brand}. Быстрая зарядка, надёжные материалы. Сертифицирован по стандартам безопасности.",
            "Премиальное качество от {brand}. Высокая скорость передачи данных и зарядки. Упаковка: коробка.",
        ],
        "link_base": "https://www.ozon.ru/product/",
        "powers": [15, 20, 25, 30, 33, 65],
        "lengths": [1, 1.5, 2, 3],
        "capacities": [5000, 10000, 20000, 30000],
    },
    {
        "category": "Красота и уход",
        "brands": ["SHENY Professional", "Luna mea", "YourDoc", "Holly Polly", "White Wolsy"],
        "marketplace": "Wildberries",
        "names": [
            "Шампунь восстанавливающий {brand} {volume} мл",
            "Крем для лица увлажняющий {brand} {volume} мл",
            "Сыворотка для волос {brand} с кератином {volume} мл",
            "Маска для лица {brand} с гиалуроновой кислотой {volume} мл",
            "Спрей термозащита {brand} для укладки {volume} мл",
        ],
        "descriptions": [
            "Профессиональное средство от {brand}. Натуральный состав, без парабенов и сульфатов. Подходит для ежедневного использования.",
            "Уходовое средство {brand} с активными компонентами. Видимый результат после первого применения. Объём {volume} мл.",
            "Инновационная формула от {brand}. Клинически протестировано. Производство — Южная Корея.",
        ],
        "link_base": "https://www.wildberries.ru/catalog/",
        "volumes": [100, 150, 200, 250, 300, 500],
    },
    {
        "category": "Авто и мото",
        "brands": ["Xoda", "ReMarco", "TRUNKÄR", "BlackRED", "dods"],
        "marketplace": "Ozon",
        "names": [
            "Органайзер в багажник {brand} универсальный",
            "Автомобильный пылесос {brand} беспроводной {power}W",
            "Полироль для кузова {brand} {volume} мл",
            "Держатель для телефона {brand} магнитный",
            "Видеорегистратор {brand} Full HD с GPS",
        ],
        "descriptions": [
            "Качественный автоаксессуар от {brand}. Универсальная совместимость с большинством автомобилей. Простая установка.",
            "Автоаксессуар {brand} премиум-класса. Прочные материалы, стильный дизайн. Гарантия 12 месяцев.",
            "Надёжный аксессуар для вашего автомобиля от {brand}. Проверено на совместимость с российскими авто.",
        ],
        "link_base": "https://www.ozon.ru/product/",
        "powers": [60, 80, 100, 120, 150],
        "volumes": [200, 300, 500],
    },
    {
        "category": "Спорт и отдых",
        "brands": ["PENKA", "FLYFIT", "SportLine", "FitPro", "GymMax"],
        "marketplace": "Wildberries",
        "names": [
            "Скакалка скоростная {brand} с подшипниками",
            "Массажный ролл {brand} МФР {size} см",
            "Фитнес-резинка {brand} набор {qty} шт",
            "Коврик для йоги {brand} TPE {size} мм",
            "Гантели разборные {brand} {weight} кг комплект",
        ],
        "descriptions": [
            "Спортивный инвентарь от {brand}. Профессиональное качество для домашних тренировок и зала.",
            "Оборудование {brand} для фитнеса. Износостойкие материалы, эргономичный дизайн. Подходит для любого уровня подготовки.",
            "Тренировочный аксессуар от {brand}. Рекомендован фитнес-тренерами. Сертифицирован.",
        ],
        "link_base": "https://www.wildberries.ru/catalog/",
        "sizes": [30, 45, 60, 90],
        "qty": [3, 4, 5],
        "weights": [2, 3, 5, 8, 10],
    },
]


def generate_product_data() -> ProductData:
    """Сгенерировать реалистичные рандомные данные продукта."""
    template = random.choice(PRODUCT_TEMPLATES)

    brand = random.choice(template["brands"])
    name_template = random.choice(template["names"])
    desc_template = random.choice(template["descriptions"])

    # Подстановки в шаблон
    replacements = {"brand": brand}

    if "sizes" in template:
        replacements["size"] = random.choice(template["sizes"])
    if "qty" in template:
        replacements["qty"] = random.choice(template["qty"])
    if "volumes" in template:
        replacements["volume"] = random.choice(template["volumes"])
    if "powers" in template:
        replacements["power"] = random.choice(template["powers"])
    if "lengths" in template:
        replacements["length"] = random.choice(template["lengths"])
    if "capacities" in template:
        replacements["capacity"] = random.choice(template["capacities"])
    if "weights" in template:
        replacements["weight"] = random.choice(template["weights"])

    name = name_template.format(**replacements)
    description = desc_template.format(**replacements)

    # Артикул: буквы + цифры, минимум 5 символов
    article_prefix = "".join(random.choices(string.ascii_uppercase, k=3))
    article_num = random.randint(10000, 99999)
    article = f"{article_prefix}-{article_num}"

    # Цена: 50–95 ₽
    price = str(random.randint(50, 95))

    # Ссылка
    slug = name.lower().replace(" ", "-").replace(",", "")
    slug = "".join(c for c in slug if c.isalnum() or c == "-")[:60]
    product_link = f"{template['link_base']}{slug}-{article_num}"

    return ProductData(
        article=article,
        name=name,
        description=description,
        category=template["category"],
        brand=brand,
        marketplace=template["marketplace"],
        price=price,
        product_link=product_link,
    )
