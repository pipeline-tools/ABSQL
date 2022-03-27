from absql.functions.env import env_var
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine


def table_exists(table_location, engine_env="AB__URI", engine=None):
    table_parts = split_parts(table_location)
    engine = (
        handle_engine(env_var(engine_env)) if engine is None else handle_engine(engine)
    )
    if hasattr(engine, "has_table"):
        return engine.has_table(
            table_name=table_parts["target"], schema=table_parts["namespace"]
        )
    else:
        return engine.reflection.Inspector.has_table(
            table_name=table_parts["target"], schema=table_parts["namespace"]
        )


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
    field_parts = split_parts(field_location)

    query = "SELECT MAX({field}) AS value FROM {table}".format(
        field=field_parts["target"], table=field_parts["namespace"]
    )
    try:
        return query_db(query, engine_env, engine)[0].value
    except Exception:
        return None


def get_min_value(field_location, engine_env="AB__URI", engine=None):
    field_parts = split_parts(field_location)

    query = "SELECT MIN({field}) AS value FROM {table}".format(
        field=field_parts["target"], table=field_parts["namespace"]
    )
    try:
        return query_db(query, engine_env, engine)[0].value
    except Exception:
        return None


def split_parts(location):
    parts = {}
    location_parts = location.split(".")
    target = location_parts[-1]
    namespace = (
        None
        if len(location_parts) == 1
        else ".".join(location_parts[: len(location_parts) - 1])
    )
    parts["target"] = target
    parts["namespace"] = namespace
    return parts
