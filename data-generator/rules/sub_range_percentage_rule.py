from rules.range_rule import RangeRule
from rules.rule import Rule

"""
 0                                23
 |--------------------------------|
        7                         23
        |-------------------------|
                   >=95%
 SubRangePercentageRule(0, 23).select(7, 23, 95)
"""


class SubRangePercentageRule(Rule):
    def __init__(self, start: int, end: int):
        self._start = start
        self._end = end
        self._in_range = 0
        self._total = 0
        self._range_rule = RangeRule()

    def apply(self, sub_start: int, sub_end: int, min_percentage: int) -> int:
        if self._total == 0:
            return self._random_value_in_range(sub_start, sub_end)
        in_range_percentage = (self._in_range * 100) / (self._total + 1)
        if in_range_percentage < min_percentage:
            return self._random_value_in_range(sub_start, sub_end)
        else:
            return self._random_value_out_range(sub_start, sub_end)

    def increase_in_range(self):
        self._in_range += 1

    def increase_total(self):
        self._total += 1

    def _random_value_in_range(self, sub_start: int, sub_end: int) -> int:
        value = self._range_rule.apply(sub_start, sub_end)
        self.increase_in_range()
        self.increase_total()
        return value

    def _random_value_out_range(self, sub_start: int, sub_end: int) -> int:
        val = self._get_out_range_position(sub_start, sub_end)
        if val == 0:
            value = self._range_rule.apply(self._start, sub_start - 1 if sub_start > self._start else sub_start)
        else:
            value = self._range_rule.apply(sub_end + 1 if sub_end < self._end else sub_end, self._end)
        self.increase_total()
        return value

    # 0 -> select before sub_start
    # 1 -> select after sub_end
    def _get_out_range_position(self, sub_start: int, sub_end: int):
        if sub_start > self._start and sub_end < self._end:
            return self._range_rule.apply(0, 1)
        elif sub_start > self._start:
            return 0
        return 1
