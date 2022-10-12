class ProductTemplateModel:
    def __init__(self, name: str, brand: str, category: str, image: str, rating: float, client_id: str,
                 round_rating: int):
        self.name = name
        self.brand = brand
        self.category = category
        self.image = image
        self.rating = rating
        self.client_id = client_id
        self.round_rating = round_rating


class ProductModel:
    def __init__(self, id_value: str, template: ProductTemplateModel):
        self.id_value = id_value
        self.template = template
