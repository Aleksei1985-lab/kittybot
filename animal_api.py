import requests
import logging

logger = logging.getLogger(__name__)


class AnimalAPI:
    def __init__(self):
        self.cat_api_url = "https://api.thecatapi.com/v1/images/search"
        self.dog_api_url = "https://api.thedogapi.com/v1/images/search"
        self.timeout = 5
        logger.info("Инициализирован AnimalAPI")

    async def get_animal_image(self, prefer_cat=True):
        """Получение случайного изображения животного"""
        try:
            if prefer_cat:
                url, error = await self._get_image(self.cat_api_url, "котика")
                if url:
                    logger.info("Успешно получено изображение котика")
                    return url, "Мяу! Вот тебе котик! 😊"

            url, error = await self._get_image(self.dog_api_url, "собаки")
            if url:
                logger.info("Получено изображение собаки вместо котика")
                return url, "Не смог найти котика 😿 Но вот тебе собачка! 🐶"

            logger.error("Не удалось получить изображения ни котика, ни собаки")
            return None, "Не удалось найти ни котика, ни собачку 😿 Попробуй позже!"

        except Exception as e:
            logger.error(f"Неожиданная ошибка в get_animal_image: {e}", exc_info=True)
            return None, "Что-то пошло не так 😿"

    async def _get_image(self, api_url, animal_type):
        """Внутренний метод для получения изображения"""
        try:
            logger.debug(f"Запрос к {api_url} для получения {animal_type}")
            response = requests.get(api_url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Успешный ответ от API для {animal_type}")
            return data[0]["url"], None
        except Exception as e:
            logger.warning(f"Ошибка при запросе {animal_type}: {str(e)}")
            return None, e
