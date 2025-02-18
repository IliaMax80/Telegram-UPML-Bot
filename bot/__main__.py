import asyncio

from loguru import logger

from bot.database.db_session import database_init
from bot.middlewares import setup_middlewares
from bot.setup import make_bot, make_dispatcher, setup_logs
from bot.schedule import run_schedule_jobs
from bot.settings import get_settings


async def main() -> None:
    """И поехали! :)."""
    setup_logs()
    settings = get_settings()

    await database_init(settings.db)

    bot = await make_bot(settings.bot.BOT_TOKEN)
    dp = make_dispatcher()
    dp["settings"] = settings

    setup_middlewares(bot, dp)

    asyncio.create_task(run_schedule_jobs(bot, settings.other.TIMEOUT))

    logger.info("Запуск пулинга...")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        polling_timeout=settings.other.TIMEOUT,
        allowed_updates=dp.resolve_used_update_types(),
    )

    logger.info("Бот выключен")


if __name__ == "__main__":
    asyncio.run(main())
