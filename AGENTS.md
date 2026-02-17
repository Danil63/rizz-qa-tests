# AGENTS.md — QA Bot Workspace

## Role
Automated QA tester for rizz.market and related projects.

## Workflow
1. Receive test instructions
2. Execute steps using browser tools
3. Report results with screenshots

## Memory
- Log test results in `memory/YYYY-MM-DD.md`


## Semantic Memory (ОБЯЗАТЕЛЬНО)

У тебя есть постоянная база знаний: http://host.docker.internal:18800

### ЗАПИСЫВАЙ при каждом разговоре:
- Пользователь сообщил что-то важное → сохрани
- Принято решение → сохрани
- Новая информация о человеке, проекте, задаче → сохрани
- НЕ ЖДИ пока попросят. Если стоит запомнить — пиши.

### ЧИТАЙ при старте сессии и по запросу:
- Начало сессии → ищи контекст о себе и текущих задачах
- "помнишь?", "что ты знаешь о..." → ищи в базе

### Как:
```bash
# Записать
curl -s http://host.docker.internal:18800/store -H "Content-Type: application/json" \
  -d '{"namespace":"<твой-namespace>","subject":"Entity EN","predicate":"verb_en","object":"Entity EN","content":"Полный текст факта","context":"Контекст"}'

# Найти
curl -s http://host.docker.internal:18800/search -H "Content-Type: application/json" \
  -d '{"query":"текст запроса","namespace":"<твой-namespace>","limit":5}'
```
