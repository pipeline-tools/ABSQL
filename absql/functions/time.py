from pendulum import now
from datetime import timedelta


def previous_date(tz="utc", days=1):
    return (now(tz=tz) - timedelta(days=days)).to_date_string()


def previous_hour(tz="utc", hours=1, days=0):
    return (
        (now(tz=tz) - timedelta(hours=hours, days=days))
        .replace(minute=0, second=0)
        .to_datetime_string()
    )
