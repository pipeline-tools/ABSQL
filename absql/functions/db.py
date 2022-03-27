from absql.functions.env import env_var
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


def get_max_value(field_location, engine_env="AB__URI", engine=None):
    field_parts = field_location.split(".")
    field = field_parts[-1]
    namespace = (
        None if len(field_parts) == 1 else ".".join(field_parts[: len(field_parts) - 1])
    )

    query = "SELECT MAX({field}) AS value FROM {table}".format(
        field=field, table=namespace
    )
    return query_db(query, engine_env, engine)[0].value


def get_min_value(field_location, engine_env="AB__URI", engine=None):
    field_parts = field_location.split(".")
    field = field_parts[-1]
    namespace = (
        None if len(field_parts) == 1 else ".".join(field_parts[: len(field_parts) - 1])
    )

    query = "SELECT MIN({field}) AS value FROM {table}".format(
        field=field, table=namespace
    )
    return query_db(query, engine_env, engine)[0].value
