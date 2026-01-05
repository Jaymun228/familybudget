import asyncio
import logging

from telegram.ext import Application, AIORateLimiter

from app.config import load_settings
from app.handlers import register_handlers
from app.services.db import create_engine, create_session_factory, init_models


def setup_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        level=logging.INFO,
    )


async def main() -> None:
    setup_logging()
    settings = load_settings()

    engine = create_engine(settings.db)
    await init_models(engine)
    session_factory = create_session_factory(engine)

    app = (
        Application.builder()
        .token(settings.bot.token)
        .rate_limiter(AIORateLimiter())
        .post_init(
            lambda application: application.bot_data.update(
                {"session_factory": session_factory, "settings": settings}
            )
        )
        .build()
    )

    register_handlers(app)
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.wait()
    await app.stop()
    await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
