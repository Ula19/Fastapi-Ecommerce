from slugify import slugify
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from typing import Annotated

from app.models import *
from app.backend.db_depends import get_db
from app.schemas import CreateProduct


router = APIRouter(prefix='/products', tags=['products'])


@router.get('/')
async def all_products(db: Annotated[Session, Depends(get_db)]):
    """
    Метод получения всех товаров
    """

    products = db.scalars(select(Product).where(Product.is_active == True, Product.stock > 0)).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Нет товаров")
    return products


@router.post('/create')
async def create_product(db: Annotated[Session, Depends(get_db)], create_product: CreateProduct):
    """
    Метод создания товара
    """

    db.execute(insert(Product).values(name=create_product.name,
                                      description=create_product.description,
                                      price=create_product.price,
                                      image_url=create_product.image_url,
                                      stock=create_product.stock,
                                      slug=slugify(create_product.name),
                                      rating='0.0',
                                      category_id=create_product.category))
    db.commit()
    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "Успешный"
    }


@router.get('/{category_slug}')
async def product_by_category(category_slug: str, db: Annotated[Session, Depends(get_db)]):
    """
    Метод получения товаров определенной категории
    """

    category = db.scalar(select(Category).where(Category.slug == category_slug))
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Категория не найдена")
    subcategories = db.scalars(select(Category).where(Category.parent_id == category.id)).all()
    categories_and_subcategories = [category.id] + [i.id for i in subcategories]
    products_category = db.scalars(
        select(Product).where(Product.category_id.in_(categories_and_subcategories),
                              Product.is_active == True, Product.stock > 0)
    ).all()
    return products_category


@router.get('/detail/{product_slug}')
async def product_detail(product_slug: str, db: Annotated[Session, Depends(get_db)]):
    """
    Метод получения детальной информации о товаре
    """

    product = db.scalar(
        select(Product).where(Product.slug == product_slug, Product.is_active == True, Product.stock > 0)
    )
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Нет товара")
    return product


@router.put('/detail/{product_slug}')
async def update_product(product_slug: str, db: Annotated[Session, Depends(get_db)], update_product_model: CreateProduct):
    """
    Метод изменения товара
    """

    product = db.scalar(select(Product).where(Product.slug == product_slug))
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Товар не найден")
    db.execute(update(Product).where(Product.slug == product_slug).values(
        name=update_product_model.name,
        description=update_product_model.description,
        price=update_product_model.price,
        image_url=update_product_model.image_url,
        stock=update_product_model.stock,
        category_id=update_product_model.category,
        slug=slugify(update_product_model.name),
    ))
    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "Обновление категории прошло успешно"
    }


@router.delete('/delete/{product_slug}')
async def delete_product(product_slug: str, db: Annotated[Session, Depends(get_db)]):
    """
    Метод удаления товара
    """

    product = db.scalar(select(Product).where(Product.slug == product_slug))
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Товар не найден")
    db.execute(update(Product).where(Product.slug == product_slug).values(is_active=False))  # Мягкое удаление
    # db.execute(delete(Product).where(Product.slug == product_slug))  # Жесткое удаление
    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "Удаление продукта прошло успешно"
    }
