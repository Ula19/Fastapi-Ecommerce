from fastapi import APIRouter


router = APIRouter(prefix='/products', tags=['products'])


@router.get('/')
async def all_products():
    """
    Метод получения всех товаров
    """
    pass


@router.post('/create')
async def create_product():
    """
    Метод создания товара
    """
    pass


@router.get('/{category_slug}')
async def product_by_category(category_slug: str):
    """
    Метод получения товаров определенной категории
    """
    pass


@router.get('/detail/{product_slug}')
async def product_detail(product_slug: str):
    """
    Метод получения детальной информации о товаре
    """
    pass


@router.put('/detail/{product_slug}')
async def update_product(product_slug: str):
    """
    Метод изменения товара
    """
    pass


@router.delete('/delete')
async def delete_product(product_id: int):
    """
    Метод удаления товара
    """
    pass
