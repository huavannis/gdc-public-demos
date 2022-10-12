import random
from datetime import datetime, timedelta
from typing import List, Dict

from grouper import Grouper


class DateDimension:
    def __init__(self, days: int):
        self._days = days
        self._current_date_time = self._get_current_date_time()
        self._available_date_times = self._generate_date_times()
        self._available_date_times_by_month = self._group_date_times_by_month()
        self._first_day = self._get_first_day()

    @property
    def available_date_times(self):
        return self._available_date_times

    @property
    def available_date_times_by_month(self):
        return self._available_date_times_by_month

    @staticmethod
    def plus_n_days(date_time: datetime, days: int) -> datetime:
        return date_time + timedelta(days=days)

    @staticmethod
    def parse_month_key(month_key: str) -> datetime:
        parsed_date = datetime.strptime(month_key, "%Y%m").date()
        return datetime(parsed_date.year, parsed_date.month, parsed_date.day)

    @staticmethod
    def parse_day_key(day_key: str) -> datetime:
        parsed_date = datetime.strptime(day_key, "%Y%m%d").date()
        return datetime(parsed_date.year, parsed_date.month, parsed_date.day)

    @staticmethod
    def parse_date(date: str, format_str: str) -> datetime:
        parsed_date = datetime.strptime(date, format_str).date()
        return datetime(parsed_date.year, parsed_date.month, parsed_date.day)

    @staticmethod
    def is_last_day_in_month(date: datetime) -> bool:
        tomorrow = date + timedelta(days=1)
        return tomorrow.year > date.year or tomorrow.month > date.month

    def get_month_key(self, date_time: datetime = None) -> str:
        selected_date_time = self._current_date_time if date_time is None else date_time
        return selected_date_time.strftime("%Y%m")

    def get_day_key(self, date_time: datetime = None) -> str:
        selected_date_time = self._current_date_time if date_time is None else date_time
        return selected_date_time.strftime("%Y%m%d")

    def get_previous_month(self, date_time: datetime = None) -> datetime:
        selected_date_time = self._current_date_time if date_time is None else date_time
        previous_month = datetime(selected_date_time.year, selected_date_time.month, 1) - timedelta(days=1)
        return datetime(previous_month.year, previous_month.month, previous_month.day, selected_date_time.hour,
                        selected_date_time.minute, selected_date_time.second)

    def random_date_time(self, after_date_time: datetime = None) -> datetime:
        if after_date_time is not None:
            range_date_times = [date_time for date_time in self._available_date_times if date_time > after_date_time]
        else:
            range_date_times = self._available_date_times
        return random.choice(range_date_times if len(range_date_times) > 0 else [self._current_date_time])

    def get_last_n_month_keys(self, n: int):
        results = []
        date_time = self._current_date_time
        for _ in range(n):
            date_time = self.get_previous_month(date_time)
            month_key = self.get_month_key(date_time)
            results.append(month_key)
        return results

    @staticmethod
    def _get_current_date_time():
        today = datetime.today()
        return datetime(today.year, today.month, 1, 0, 0, 0) - timedelta(days=1)

    def _generate_date_times(self) -> List[datetime]:
        results = [self._current_date_time]
        for day in range(self._days):
            n_days_ago = self._current_date_time - timedelta(days=day + 1)
            results.append(n_days_ago)
        return results

    def _group_date_times_by_month(self) -> Dict[str, List[datetime]]:
        return Grouper().group_array_by_field_condition(self._available_date_times, self.get_month_key)

    def _get_first_day(self) -> datetime:
        self._available_date_times.sort()
        return self._available_date_times[0]
