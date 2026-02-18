# Stage — сохранённые состояния авторизации

Файлы `*_state.json` генерируются скриптом `generate_auth.py`.

## Генерация

```bash
python tests/stage/generate_auth.py
```

Создаёт:
- `advertiser_state.json` — cookie рекламодателя
- `blogger_state.json` — cookie блогера

## Использование

Фикстуры `tests/test_suites/filters/conftest.py` и `tests/test_suites/products/conftest.py`
подгружают cookie из этих файлов. Браузер НЕ запускается для авторизации.

## Перегенерация

Запусти скрипт заново если cookie протухли.
