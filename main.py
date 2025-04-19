"""
Основной модуль для запуска Telegram бота.

Содержит точку входа и настройку приложения.
"""

import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from animal_api import AnimalAPI
from bot_handlers import BotHandlers
from logging_config import setup_logging
import logging

logger = logging.getLogger(__name__)


async def post_init(application):
    """
    Функция инициализации после запуска бота.

    Args:
        application (Application): Экземпляр приложения бота
    """
    try:
        logger.info("Настройка команд бота")
        await handlers.setup_bot_commands(application)
    except Exception as e:
        logger.error(f"Ошибка в post_init: {e}", exc_info=True)
        raise


def main():
    """Основная функция для запуска и настройки бота."""
    try:
        setup_logging()
        logger.info("Запуск бота")

        token = os.getenv("API_TELEGRAM_KITTY")
        if not token:
            logger.error("Токен бота не найден в переменных окружения")
            raise ValueError("Токен бота не найден")

        logger.info("Инициализация компонентов бота")
        animal_api = AnimalAPI()
        global handlers
        handlers = BotHandlers(animal_api)

        application = Application.builder().token(token).post_init(post_init).build()

        # Регистрация обработчиков
        application.add_handler(CommandHandler("start", handlers.start))
        application.add_handler(CommandHandler("help", handlers.help_command))
        application.add_handler(CommandHandler("newcat", handlers.send_random_animal))
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_message)
        )

        logger.info("Бот готов к работе")
        print("Бот запущен! Мяу! 😺")
        application.run_polling()

    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске бота: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    load_dotenv()
    main()
