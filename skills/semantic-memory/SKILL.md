---
name: semantic-memory
description: Семантическая долгосрочная память (Graph-RAG). Используй при любом разговоре для сохранения важных фактов и поиска ранее сохранённых знаний. Автоматически активируется когда нужно запомнить информацию, найти что-то из прошлых разговоров, или когда пользователь спрашивает "помнишь?", "что ты знаешь о...", "запомни".
---

# Semantic Memory — Graph-RAG

Долгосрочная память на базе SPO (Subject-Predicate-Object) графа с семантическим поиском.

## API

Базовый URL: `http://host.docker.internal:18800` (из Docker) или `http://127.0.0.1:18800` (с хоста).

### Сохранить факт

```bash
curl -s http://host.docker.internal:18800/store \
  -H "Content-Type: application/json" \
  -d '{
    "namespace": "<bot-name>",
    "subject": "Entity Name EN",
    "predicate": "relationship",
    "object": "Entity Name EN",
    "content": "Полный текст факта",
    "context": "Оригинальный контекст откуда взят факт",
    "source_url": "https://...",
    "metadata": {}
  }'
```

### Поиск по памяти

```bash
curl -s http://host.docker.internal:18800/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "текст запроса",
    "namespace": "<bot-name>",
    "limit": 5
  }'
```

### Статистика

```bash
curl -s http://host.docker.internal:18800/stats
```

## Правила использования

### Когда СОХРАНЯТЬ факты:

1. Пользователь просит запомнить что-то
2. Выявлены важные факты из документов/статей/разговоров
3. Принято решение, которое важно помнить
4. Новая информация о проекте, человеке, технологии

### Когда ИСКАТЬ в памяти:

1. Пользователь спрашивает "помнишь?", "что ты знаешь о..."
2. Нужен контекст по теме, которая обсуждалась ранее
3. Перед принятием решения — проверить, есть ли релевантные факты

### Формат сохранения:

- **subject/object** — всегда на английском (нормализация)
- **predicate** — глагол-связка на английском (is, has, uses, works_at, prefers, decided_to)
- **content** — полный текст факта на языке оригинала
- **context** — исходный фрагмент разговора/документа
- **namespace** — имя бота (hr, barter, qa, sale, main)

### Примеры:

Пользователь: "Наш офис переехал на Тверскую 15"
```json
{
  "namespace": "hr",
  "subject": "Company Office",
  "predicate": "located_at",
  "object": "Tverskaya 15",
  "content": "Офис компании переехал на Тверскую 15",
  "context": "Пользователь сообщил о переезде офиса"
}
```

Пользователь: "Используй для деплоя только Docker"
```json
{
  "namespace": "main",
  "subject": "Deployment",
  "predicate": "requires",
  "object": "Docker",
  "content": "Для деплоя используется только Docker",
  "context": "Пользователь установил правило деплоя"
}
```
