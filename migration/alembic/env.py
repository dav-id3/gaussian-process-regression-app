import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def build_url() -> str:
    """
    build Python MySQL driver specific database url string

    Returns:
        str: database uri string
    Examples:
        >>> build_url()
        "mysql+mysqldb://username:password@hostname:port?charset=utf8"
    """
    hostname = os.environ.get("MYSQL_HOST")
    username = os.environ.get("MYSQL_USER")
    password = os.environ.get("MYSQL_PASSWORD")
    database = os.environ.get("MYSQL_DATABASE")
    port = os.environ.get("MYSQL_PORT")

    # use pymysql driver instead
    protocol = "mysql+pymysql"
    identity = f"{username}:{password}"
    host = f"{hostname}:{port}"

    pathname = f"/{database}"
    qs = "?charset=utf8"

    origin = f"{protocol}://{identity}@{host}"

    return origin + pathname + qs


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = build_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    ini_section = config.get_section(config.config_ini_section)
    ini_section["sqlalchemy.url"] = build_url()

    connectable = engine_from_config(
        ini_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(compare_type=True, connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    print("run migraiton scripts in offline mode")
    run_migrations_offline()
else:
    print("run migraiton scripts in online mode")
    run_migrations_online()
