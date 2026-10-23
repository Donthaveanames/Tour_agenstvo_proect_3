Тема
Разработка backend-приложения для тур-агентства через REST API.

Главная сущность | Tour — тур (страна, даты заезда/выезда, места, цена)
Связанная сущность (1:N) | Booking — бронирование тура (пока не реализовано, задел на будущее)
Фишка | Валидация бизнес-полей (places > 0, price > 0) + кастомный обработчик ошибок валидации с кодом 400
Стек | Python 3.11, FastAPI, Pydantic v2, Uvicorn

Установка и запуск
1. Клонирование / создание виртуального окружения
bash
py -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
2. Установка зависимостей
bash
py - m pip install -r requirements.txt
3. Запуск сервера
bash
py -m uvicorn Tour_agenstvo_proect_3.Tour_agenstvo_proect_3:app --reload


🔌 Эндпоинты
|Метод | Путь | Назначение | ✅ Успех | ❌ Ошибки|
| --- | --- | --- | --- | --- |
|GET | /health | Проверка | работоспособности | 200 | —|
|POST | /api/tours | Создать тур | 201 | 400|
|GET | /api/tours | Список всех туров | 200 | —|
|GET | /api/tours/{id} | Получить тур по id | 200 | 404|
|PUT | /api/tours/{id} | Полностью заменить тур | 200 | 400, 404|
|PATCH | /api/tours/{id} | Частично обновить тур | 200 | 400, 404|
|DELETE | /api/tours/{id} | Удалить тур | 204 | 404|