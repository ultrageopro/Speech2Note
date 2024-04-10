import telebot  # type: ignore
from modules.logger import CustomLogger
from data.user_database import UserDatabase


class StartRoute:
    def __init__(self, bot: telebot.TeleBot, logger: CustomLogger, user_database: UserDatabase) -> None:  # type: ignore
        self.bot = bot
        self.logger = logger
        self.database = user_database

        @bot.message_handler(commands=["start"])
        def start(message: telebot.types.Message) -> None:  # type: ignore
            self.__start(message)

        self.logger.info("Start route initialized.", "server")

    def __start(self, message: telebot.types.Message) -> None:  # type: ignore

        code, user = self.database.get_user(message.chat.id)

        if code != 200:
            self.bot.send_message(
                message.chat.id,
                "Произошла ошибка. Попробуйте ещё раз позже.\nМы уже работаем над этим.",
            )

        if user is None:
            self.database.new_user(message.chat.id, message.from_user.username)
            self.bot.send_message(
                message.chat.id,
                f"Привет, {message.from_user.username}!\n"
                + "---------------\n"
                + "Я бот, который поможет тебе создать полноценный конспект из аудио!"
                + "Пришли мне аудиофайл, и я помогу тебе создать конспект из него!\n"
                + "---------------\n"
                + "Посмотреть профиль /profile\n"
                + "Запросить токены /tokens\n"
                + "Посмотреть цены /prices\n"
                + "---------------",
            )
            return

        self.bot.send_message(
            message.chat.id,
            f"С возвращением, {user.name}!\n"
            + "---------------\n"
            + "Пришли мне аудиофайл, и я помогу тебе создать полноценный конспект из него!\n"
            + "---------------\n"
            + "Посмотреть профиль /profile\n"
            + "Запросить токены /tokens\n"
            + "Посмотреть цены /prices\n"
            + "---------------",
        )