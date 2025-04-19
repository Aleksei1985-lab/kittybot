from telegram import ReplyKeyboardMarkup, MenuButtonCommands, BotCommand
from telegram.ext import ContextTypes
from telegram import Update
import logging

logger = logging.getLogger(__name__)


class BotHandlers:
    """
    Класс обработчиков команд и сообщений для Telegram бота.

    Отвечает за:
    - Создание интерактивных клавиатур
    - Обработку команд (/start, /help, /newcat)
    - Обработку текстовых сообщений и кнопок
    - Логирование всех действий

    Attributes:
        animal_api (AnimalAPI): Экземпляр API для работы с животными
    """

    def __init__(self, animal_api):
        """
        Инициализация обработчиков бота.

        Args:
            animal_api: Экземпляр класса для работы с API животных
        """
        self.animal_api = animal_api
        logger.info("Инициализирован BotHandlers")

    def get_main_menu(self) -> ReplyKeyboardMarkup:
        """
        Создает клавиатуру главного меню.

        Returns:
            ReplyKeyboardMarkup: Клавиатура с кнопками:
            - 🐱 Фото котика
            - 🕒 Который час?
            - 🌐 Мой IP
            - 🎲 Случайное число
        """
        return ReplyKeyboardMarkup(
            [
                ["🐱 Фото котика", "🕒 Который час?"],
                ["🌐 Мой IP", "🎲 Случайное число"],
            ],
            resize_keyboard=True,
        )

    def get_cat_menu(self) -> ReplyKeyboardMarkup:
        """
        Создает клавиатуру меню котиков.

        Returns:
            ReplyKeyboardMarkup: Клавиатура с кнопками:
            - 🐱 Новый котик
            - 🔙 Назад
        """
        return ReplyKeyboardMarkup(
            [["🐱 Новый котик", "🔙 Назад"]], resize_keyboard=True
        )

    async def setup_bot_commands(self, app) -> None:
        """
        Настраивает меню команд бота в интерфейсе Telegram.

        Args:
            app: Экземпляр Application бота

        Устанавливает команды:
        - /start - Запустить бота
        - /help - Помощь
        - /newcat - Новый котик
        """
        commands = [
            BotCommand("start", "Запустить бота"),
            BotCommand("help", "Помощь"),
            BotCommand("newcat", "Новый котик"),
        ]
        await app.bot.set_my_commands(commands)
        await app.bot.set_chat_menu_button(menu_button=MenuButtonCommands())

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Обработчик команды /start.

        Отправляет приветственное сообщение и главное меню.

        Args:
            update: Объект Update от Telegram
            context: Контекст выполнения
        """
        try:
            chat = update.effective_chat
            name = update.message.chat.first_name
            logger.info(f"Обработка команды /start от {name} (ID: {chat.id})")

            await context.bot.send_message(
                chat_id=chat.id,
                text=f"Привет, {name}! Я KittyBot 😺\n\n"
                "Я умею:\n"
                "• Показывать котиков 🐱\n"
                "• Шутить про время ⏰\n"
                '• И даже "определять" IP 🌐',
                reply_markup=self.get_main_menu(),
            )
        except Exception as e:
            logger.error(f"Ошибка в обработчике start: {e}", exc_info=True)
            raise

    async def help_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Обработчик команды /help.

        Отправляет пользователю справку по командам.

        Args:
            update: Объект Update от Telegram
            context: Контекст выполнения
        """
        help_text = (
            "🐱 <b>KittyBot Help</b> 🐱\n\n"
            "• /start - Запустить бота\n"
            "• /help - Эта справка\n"
            "• /newcat - Новый котик\n\n"
            "Используй кнопки для быстрого доступа к функциям!"
        )
        await update.message.reply_text(help_text, parse_mode="HTML")

    async def send_random_animal(
        self, chat_id: int, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Отправляет случайное изображение животного (котика или собаки).

        Args:
            chat_id: ID чата для отправки
            context: Контекст выполнения

        Логирует результат операции:
        - Успешное получение и отправку изображения
        - Ошибки при запросе или отправке
        """
        try:
            logger.info(f"Запрос изображения животного для чата {chat_id}")
            image_url, caption = await self.animal_api.get_animal_image()

            if image_url:
                try:
                    await context.bot.send_photo(
                        chat_id=chat_id,
                        photo=image_url,
                        caption=caption,
                        reply_markup=self.get_cat_menu(),
                    )
                    logger.info(f"Изображение успешно отправлено в чат {chat_id}")
                except Exception as e:
                    logger.error(f"Ошибка при отправке фото в чат {chat_id}: {e}")
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text="Не удалось отправить фото 😿 Попробуй ещё раз!",
                        reply_markup=self.get_main_menu(),
                    )
            else:
                logger.warning(f"Не удалось получить изображение для чата {chat_id}")
                await context.bot.send_message(
                    chat_id=chat_id, text=caption, reply_markup=self.get_main_menu()
                )
        except Exception as e:
            logger.error(f"Ошибка в send_random_animal: {e}", exc_info=True)
            raise

    async def handle_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Обработчик текстовых сообщений и нажатий на кнопки.

        Args:
            update: Объект Update от Telegram
            context: Контекст выполнения

        Обрабатывает:
        - Запросы котиков (по тексту или кнопке)
        - Запросы времени
        - Запросы IP
        - Генерацию случайного числа
        - Возврат в главное меню
        """
        text = update.message.text
        chat = update.effective_chat

        if "котик" in text.lower() or text == "🐱 Фото котика":
            await self.send_random_animal(chat.id, context)
        elif text == "🕒 Который час?":
            await context.bot.send_message(
                chat_id=chat.id,
                text="⌚ Сейчас точно кошачье время! Мяу!",
                reply_markup=self.get_main_menu(),
            )
        elif text == "🌐 Мой IP":
            await context.bot.send_message(
                chat_id=chat.id,
                text="🌍 Ваш IP: 127.0.0.1 (локальный адрес котика)",
                reply_markup=self.get_main_menu(),
            )
        elif text == "🎲 Случайное число":
            await context.bot.send_message(
                chat_id=chat.id,
                text=f"🎲 Ваше число: {hash(text) % 100}",
                reply_markup=self.get_main_menu(),
            )
        elif text == "🔙 Назад":
            await context.bot.send_message(
                chat_id=chat.id,
                text="Возвращаюсь в главное меню",
                reply_markup=self.get_main_menu(),
            )
