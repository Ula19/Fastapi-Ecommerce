from slugify import slugify
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete
from typing import Annotated

from app.models import *
from app.backend.db_depends import get_db
from app.schemas import CreateCategory


router = APIRouter(prefix='/category', tags=['category'])


@router.get('/all_categories')
async def get_all_categories(db: Annotated[Session, Depends(get_db)]):
    """
    Метод получения всех категорий
    """

    categories = db.scalars(select(Category).where(Category.is_active == True)).all()
    return categories


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_category(db: Annotated[Session, Depends(get_db)], create_category: CreateCategory):
    """
    Метод создания категории
    """
    try:
        db.execute(insert(Category).values(name=create_category.name,
                                           parent_id=create_category.parent_id,
                                           slug=slugify(create_category.name)))
        db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такая категрия уже существует')
    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "Успешный"
    }



@router.put('/update_category')
async def update_category(db: Annotated[Session, Depends(get_db)], category_id: int, update_category: CreateCategory):
    """
    Метод изменения категории
    """

    category = db.scalar(select(Category).where(Category.id == category_id))
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Категория не найдена")
    db.execute(update(Category).where(Category.id == category_id).values(
        name=update_category.name,
        slug=slugify(update_category.name),
        parent_id=update_category.parent_id
    ))
    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "Обновление категории прошло успешно"
    }



@router.delete('/delete')
async def delete_category(db: Annotated[Session, Depends(get_db)], category_id: int):
    """
    Метод удаления категории
    """

    category = db.scalar(select(Category).where(Category.id == category_id))
    if category is None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail="Категория не найдена")
    db.execute(update(Category).where(Category.id == category_id).values(is_active=False))  # Мягкое удаление
    # db.execute(delete(Category).where(Category.id == category_id))  # Жесткое удаление
    db.commit()
    return {"status_code": status.HTTP_200_OK,
            "transaction": "Удаление категории прошло успешно"}
