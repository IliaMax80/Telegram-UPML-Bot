import asyncio
from logging.config import fileConfig

from alembic import context
from alembic.script import ScriptDirectory
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from bot.settings import get_settings
from bot.database.models import *  # noqa
from bot.database.db_session import SqlAlchemyBase


config = context.config
db_settings = get_settings().db

section = config.config_ini_section
config.set_section_option(section, "POSTGRES_HOST", db_settings.POSTGRES_HOST)
config.set_section_option(
    section,
    "POSTGRES_HOST_PORT",
    str(db_settings.POSTGRES_HOST_PORT),
)
config.set_section_option(section, "POSTGRES_DB", db_settings.POSTGRES_DB)
config.set_section_option(section, "POSTGRES_USER", db_settings.POSTGRES_USER)
config.set_section_option(section, "POSTGRES_PASSWORD", db_settings.POSTGRES_PASSWORD)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SqlAlchemyBase.metadata


def process_revision_directives(context, revision, directives):
    migration_script = directives[0]
    head_revision = ScriptDirectory.from_config(context.config).get_current_head()

    if head_revision is None:
        new_rev_id = 1
    else:
        last_rev_id = int(head_revision.lstrip("0"))
        new_rev_id = last_rev_id + 1
    migration_script.rev_id = "{0:04}".format(new_rev_id)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        process_revision_directives=process_revision_directives,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        process_revision_directives=process_revision_directives,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
