from absql.macros.env import env_var
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine


def table_exists(table_location, engine_env="AB__URI", engine=None):
    table_parts = table_location.split(".")
    table = table_parts[-1]
    namespace = (
        None if len(table_parts) == 1 else ".".join(table_parts[: len(table_parts) - 1])
    )
    engine = (
        handle_engine(env_var(engine_env)) if engine is None else handle_engine(engine)
    )
    if hasattr(engine, "has_table"):
        return engine.has_table(table_name=table, schema=namespace)
    else:
        return engine.reflection.Inspector.has_table(table_name=table, schema=namespace)


def query_db(query, engine_env="AB__URI", engine=None):
    engine = (
        handle_engine(env_var(engine_env)) if engine is None else handle_engine(engine)
    )
    return engine.execute(query).fetchall()


def handle_engine(engine):
    if isinstance(engine, Engine):
        return engine
    else:
        return create_engine(engine)
