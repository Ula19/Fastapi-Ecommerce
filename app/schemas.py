from pydantic import BaseModel


class CreateProduct(BaseModel):
    """
    Модель CreateProduct будет отвечать за создание продукта и будет принимать следующие поля:
        name: Имя товара, тип поля строка
        description: Описание товара, тип поля строка
        price: Цена товара, тип поля целое число
        image_url: Ссылка на изображение товара, тип поля строка
        stock: Количество товара в наличии, тип поля целое число
        category: ID категории товара, тип поля целое число
    """
    name: str
    description: str
    price: int
    image_url: str
    stock: int
    category: int


class CreateCategory(BaseModel):
    """
    Модель CreateCategory будет отвечать за создание категории товаров, и имеет 2 поля:
        name: Имя категории, тип поля строка
        parent_id: ID родительской категории, тип поля целое число
    """
    name: str
    parent_id: int | None
