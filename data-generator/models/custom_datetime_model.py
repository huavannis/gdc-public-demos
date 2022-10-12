from datetime import datetime


class CustomDateTimeModel:
    def __init__(self, date_time: datetime):
        self.date_time = date_time

    def format_date(self):
        return self.date_time.strftime("%Y-%m-%d")

    def format_datetime(self):
        return self.date_time.strftime("%Y-%m-%d %H-%M-%S")
