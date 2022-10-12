from datetime import datetime

from rules.range_rule import RangeRule
from rules.sub_range_percentage_rule import SubRangePercentageRule
from rules.rule import Rule


class TimePercentageRule(Rule):
    def __init__(self):
        self._hour_rule = SubRangePercentageRule(0, 23)
        self._range_rule = RangeRule()

    def apply(self, date_time: datetime, hour_from: int, hour_to: int, hour_percentage: int) -> datetime:
        hour = self._hour_rule.apply(hour_from, hour_to, hour_percentage)
        minute = self._range_rule.apply(0, 59)
        second = self._range_rule.apply(0, 59)
        return datetime(date_time.year, date_time.month, date_time.day, hour, minute, second)
