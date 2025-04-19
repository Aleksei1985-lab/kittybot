# KittyBot - Telegram бот с котиками 🐱

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Бот для Telegram, который отправляет фотографии котиков (а если не получается - то собачек) по запросу пользователя.

## Возможности

- Отправка случайных фото котиков из [TheCatAPI](https://thecatapi.com/)
- Автоматический fallback на [TheDogAPI](https://thedogapi.com/) при ошибках
- Интерактивное меню с кнопками
- Логирование всех событий
- Обработка ошибок и исключений

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/kittybot.git
cd kittybot
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` и добавьте токен бота:
```ini
API_TELEGRAM_KITTY=ваш_токен_бота
```

## Запуск

```bash
python main.py
```

## Структура проекта

```
kittybot/
├── animal_api.py        # Логика работы с API животных
├── bot_handlers.py      # Обработчики команд бота
├── logging_config.py    # Конфигурация логирования
├── main.py              # Точка входа
├── requirements.txt     # Зависимости
├── .env.example         # Пример файла конфигурации
└── README.md            # Документация
```

## Команды бота

- `/start` - Начать работу с ботом
- `/help` - Показать справку
- `/newcat` - Получить нового котика

## Логирование

Логи сохраняются в папку `logs/kittybot.log` с ежедневной ротацией (хранятся 7 дней).

## Лицензия

Проект распространяется под лицензией MIT. Подробнее см. [LICENSE](LICENSE).