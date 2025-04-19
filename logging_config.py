import logging
import logging.handlers
from pathlib import Path


def setup_logging():
    """Настройка системы логирования"""
    # Создаем директорию для логов, если ее нет
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Основной логгер
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Форматтер для логов
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Файловый обработчик (ротация по дням)
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename="logs/kittybot.log", when="midnight", backupCount=7, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Логирование ошибок requests и telegram
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("telegram").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logger.info("Логирование настроено")
