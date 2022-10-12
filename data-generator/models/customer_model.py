from datetime import datetime

from models.custom_datetime_model import CustomDateTimeModel


class CustomerTemplateModel:
    def __init__(self, name: str, email: str, city: str, city_pushpin: str, country: str, state: str):
        self.name = name
        self.email = email
        self.city = city
        self.city_pushpin = city_pushpin
        self.country = country
        self.state = state


class CustomerModel:
    def __init__(self, id_value: str, created_date: CustomDateTimeModel, client_id: str,
                 template: CustomerTemplateModel):
        self.id_value = id_value
        self.created_date = created_date
        self.client_id = client_id
        self.template = template


class CustomerRowModel:
    def __init__(self, created_date: datetime, client_id: str):
        self.created_date = created_date
        self.client_id = client_id
