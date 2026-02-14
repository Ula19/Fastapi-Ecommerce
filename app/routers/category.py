from fastapi import APIRouter


router = APIRouter(prefix='/category', tags=['category'])


@router.get('/all_categories')
async def get_all_categories():
    """
    Метод получения всех категорий
    """
    pass


@router.post('/create')
async def crate_category():
    """
    Метод создания категории
    """
    pass


@router.put('/update_category')
async def update_category():
    """
    Метод изменения категории
    """
    pass


@router.delete('/delete')
async def delete_category():
    """
    Метод удаления категории
    """
    pass
