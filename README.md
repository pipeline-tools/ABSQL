# ABSQL

[![PyPi](https://img.shields.io/pypi/v/ABSQL.svg)](https://pypi.org/project/ABSQL/)
![build](https://github.com/chriscardillo/ABSQL/workflows/build/badge.svg)
[![codecov](https://codecov.io/gh/chriscardillo/ABSQL/branch/main/graph/badge.svg?token=KHJ6RHD56F)](https://codecov.io/gh/chriscardillo/ABSQL)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

ABSQL is a format for templated SQL, and the ABSQL package is a rendering engine for this format.

ABSQL allows users to inject limitless context - text, objects, and functions - into their SQL templates, both within the rendering engine (the _Runner_) and in the SQL file itself.

The flexibility and extendibility of ABSQL affords SQL engineers a consistent interface for generating templated SQL, while simultaneously giving downstream orchestration solutions (e.g. Airflow) the opportunity to develop orchestrator-specific implementations for ABSQL. (A proto-implementation of this approach can be seen in the Airflow-related [gusty](https://github.com/chriscardillo/gusty) package.)

ABSQL leverages the familiar Jinja2 templating engine, as well as YAML-style frontmatter to provide users with a unique and intuitive SQL authoring experience.

# Getting Started

## Rendering Text

The ABSQL Runner is robust, but we will start simple. The static `render_text` method will render user-provided text with any provided context.

```python
from absql import Runner

Runner.render_text('{{greeting}}, World!', greeting="Hello")
# 'Hello, World!'
```

## Reusing Context

We might want to reuse the context we provide. In this case, we can instantiate a runner and provide it with context. We can then render any text with this saved context. An instantiated runner has a `render` method, that works with text and - as we will see later - file paths, as well.

```python
from absql import Runner

r = Runner(greeting = "Hello")
r.render("{{greeting}}, World!")
# 'Hello, World!'
```

## Rendering Files (and Frontmatter Context)

The runner is not bound to plain text, and the context provided by the user is not confined to just the runner. Context can also be passed in through a frontmatter block at the top of a `.sql` file. This frontmatter block is parsed as YAML.

In the example file below, `my_file.sql`, the `table_name` context is provided in the frontmatter block, which starts and ends with three hyphens (`---`). The body of the file contains the templated SQL we want to render.

```sql
---
table_name: my_table
---

SELECT *
FROM {{table_name}}
WHERE greeting = '{{greeting}}'
```

Now, using the same runner as above, we can render the SQL, with our `table_name` context being provided from the file itself, and the `greeting` context being fed in from the runner.

```python
r.render("my_file.sql")

# SELECT *
# FROM my_table
# WHERE greeting = 'Hello'
```

## Providing an Engine

There are cases when templated queries require data from a database. In ABSQL, this can be accomplished by providing a SQLAlchemy engine to a runner, and using some of the default ABSQL-provided functions. While we could instantiate a new runner with this engine, we will use our existing runner's `set_context` method to add a SQLite engine. It is important that we set the engine as `engine` in the context.

```python
from sqlalchemy import create_engine

engine = create_engine("sqlite:///:memory:")

r.set_context(engine=engine)
```

Now, we can update our query in `my_file.sql` to use ABSQL's builtin `table_exists` function. We will arbitrarily add a limit to our query, based on if a table exists.

```sql
---
table_name: my_table
---

SELECT *
FROM {{table_name}}
WHERE greeting = '{{greeting}}'
{% if table_exists("a_nonexistent_table") %}
LIMIT 10
{% else %}
LIMIT 1
{% endif %}
```

Then, we can render again.

```python
r.render("my_file.sql")

# SELECT *
# FROM my_table
# WHERE greeting = 'Hello'
# LIMIT 1
```

See below for a full list of builtin functions.

# Functions and Context

## Default Functions

The following functions are available in any instantiated runner:

| Category | Function        | Description                                                                                   | Example                                           |
| -------- | --------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| database | `get_max_value` | Get the maximum value of a column.                                                            | `get_max_value("my_schema.my_table.my_column")`   |
| database | `get_min_value` | Get the minimum value of a column.                                                            | `get_min_value("my_schema.my_table.my_column")`   |
| database | `table_exists`  | TRUE/FALSE if the table exists in the database.                                               | `table_exists("my_schema.my_table")`              |
| database | `query_db`      | Send any query to the database and get back the results.                                      | `query_db("SELECT name FROM my_schema.my_table")` |
| env      | `env_switch`    | Switch a value based on the given environment (an environment variable of "ENV" by default).  | `env_switch(dev=10, prod=500, default=30)`        |
| env      | `env_var`       | Retrieve a value from an environment variable.                                                | `env_var("MY_ENVIRONMENT_VARIABLE")`              |
| time     | `datetime`      | Python's `datetime.datetime` function.                                                        | `datetime(2022, 1, 1)`                            |
| time     | `previous_date` | Get a date string for the previous date (based on UTC by default).                            | `previous_date()`                                 |
| time     | `previous_hour` | Get a datetime string the previous hour (based on UTC by default).                            | `previous_hour()`                                 |
| time     | `timedelta`     | Python's `datetime.timedelta` function.                                                       | `timedelta(hours=1)`                              |

For the database functions, it is recommended that you pass in an engine to the runner ahead of rendering (e.g. `runner = Runner(engine=engine)`). If no engine is provided, the runner will search for a URI in the environment variable `AB__URI`.

Also note that these functions are accessible in both the frontmatter and body of a file. Below is an example illustrating this.

```sql
---
schema: "{{ env_switch(prod='prod_schema', dev=env_var('DEV_SCHEMA')) }}"
---

SELECT *
FROM {{schema}}.my_table
```

## Adding Functions and Context

As mentioned elsewhere, users can add functions and context:

- In a file's frontmatter
- When instantiating a new runner
- By using the `set_context` method on an existing runner

Note that functions which contain a keyword argument `engine` will automatically be passed the engine object attached to the runner.

# Environment Configuration

While no configuration is required to get started with ABSQL, there are two environment variables you can set:

- `AB__URI` - The URI for the database that should be used by ABSQL's default database functions. As mentioned, it is advisable that you just pass in your own SQLAlchemy engine object to a runner under the context name `engine`, if you are going to use the database functions.
- `AB__ENV` - The name of the environment variable that designates what the environment is. By default, ABSQL assumes this environment variable is called "ENV".

# Development

The below assumes you have [Docker](https://www.docker.com/) installed.

## Starting for the First Time

First, `git clone` this repository.

Then:

```bash
export ABSQL_HOME="~/path/to/this/project"
cd $ABSQL_HOME
make build-image
make run-image
```

The above will build the development image under the name `absql-testing` and run a container called `absql-testing`.

From here, you can:

- `make exec` - Exec into a terminal in the running container.
- `make test` - Runs `pytest` in a temporary container.
- `make coverage` - Runs `pytest` and generates a coverage report.
- `make browse-coverage` - Opens up the coverage report in your browser.
- `make stop-container` - Stop the running container.
- `make start-container` - Start a stopped container.

## Rebuilding the Image

```bash
make stop-container # if you have a running container
docker rm absql-testing
make build-image
make run-image
```
