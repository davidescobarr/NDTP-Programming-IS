# Career Guidance Service

Локальный сервис для адаптивного профориентационного теста.

Сервис не использует внешние LLM, облачные API или OSTIS. При старте он обучает небольшой классификатор на встроенной профессиографической базе, затем выбирает следующий вопрос по неопределенности текущего профиля пользователя.

## Docker Compose

Из корня репозитория:

```bash
docker compose up --build career-ai
```

API будет доступен на `http://localhost:8010`.

## Локальный запуск без Docker

```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8010
```

## Проверка качества подбора

```bash
.venv\Scripts\python -m unittest discover -s tests
```

Тесты проверяют ширину базы профессий и вопросов, классификацию встроенных профессиограмм, адаптивный лимит в 15 вопросов и отсутствие повторов в сценариях прохождения.
