from slugify import slugify
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from typing import Annotated

from app.models import *
from app.backend.db_depends import get_db
from app.schemas import CreateProduct
from app.routers.permissions import get_current_user


router = APIRouter(prefix='/products', tags=['products'])



async def admin_or_supplier_required(current_user: Annotated[dict, Depends(get_current_user)]):
    if not (current_user.get("is_admin") or current_user.get("is_supplier")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="У вас нет прав на использование этого метода"
        )
    return current_user


@router.get('/')
async def all_products(db: Annotated[AsyncSession, Depends(get_db)]):
    """
    Метод получения всех товаров
    """
    products = await db.scalars(select(Product).where(Product.is_active == True, Product.stock > 0))
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Нет товаров")
    return products.all()


@router.post('/create', dependencies=[Depends(admin_or_supplier_required)])
async def create_product(db: Annotated[AsyncSession, Depends(get_db)],
                         create_product: CreateProduct,
                         current_user: Annotated[dict, Depends(get_current_user)]):
    """
    Метод создания товара
    """
    await db.execute(insert(Product).values(name=create_product.name,
                                      description=create_product.description,
                                      price=create_product.price,
                                      image_url=create_product.image_url,
                                      stock=create_product.stock,
                                      slug=slugify(create_product.name),
                                      rating=0.0,
                                      category_id=create_product.category,
                                      supplier_id=current_user.get("id")))
    await db.commit()
    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "Успешный"
    }


@router.get('/{category_slug}')
async def product_by_category(db: Annotated[AsyncSession, Depends(get_db)], category_slug: str):
    """
    Метод получения товаров определенной категории
    """

    category = await db.scalar(select(Category).where(Category.slug == category_slug))
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Категория не найдена")
    subcategories = await db.scalars(select(Category).where(Category.parent_id == category.id)).all()
    categories_and_subcategories = [category.id] + [i.id for i in subcategories]
    products_category = await db.scalars(
        select(Product).where(Product.category_id.in_(categories_and_subcategories),
                              Product.is_active == True, Product.stock > 0)
    )
    return products_category.all()


@router.get('/detail/{product_slug}')
async def product_detail(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str):
    """
    Метод получения детальной информации о товаре
    """

    product = await db.scalar(
        select(Product).where(Product.slug == product_slug, Product.is_active == True, Product.stock > 0)
    )
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Нет товара")
    return product


@router.put('/detail/{product_slug}')
async def update_product(db: Annotated[AsyncSession, Depends(get_db)],
                         product_slug: str,
                         update_product_model: CreateProduct,
                         get_user: Annotated[dict, Depends(get_current_user)]):
    """
        Метод изменения товара
    """
    product_update = await db.scalar(select(Product).where(Product.slug == product_slug))
    if product_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Товар не найден'
        )
    if get_user.get('is_supplier') or get_user.get('is_admin'):
        if get_user.get('id') == product_update.supplier_id or get_user.get('is_admin'):
            await db.execute(
                update(Product).where(Product.slug == product_slug)
                .values(name=update_product_model.name,
                        description=update_product_model.description,
                        price=update_product_model.price,
                        image_url=update_product_model.image_url,
                        stock=update_product_model.stock,
                        category_id=update_product_model.category,
                        slug=slugify(update_product_model.name)))
            await db.commit()
            return {
                'status_code': status.HTTP_200_OK,
                'transaction': 'Обновление продукта прошло успешно'
            }
        else:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='У вас нет прав на использование этого метода'
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='У вас нет прав на использование этого метода'
        )


@router.delete('/delete/{product_slug}', dependencies=[Depends(admin_or_supplier_required)])
async def delete_product(db: Annotated[AsyncSession, Depends(get_db)],
                         product_slug: str,
                         get_user: Annotated[dict, Depends(get_current_user)]):
    """
    Метод удаления товара
    """

    product_delete = await db.scalar(select(Product).where(Product.slug == product_slug))
    if product_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Товар не найден'
        )
    if get_user.get('is_supplier') or get_user.get('is_admin'):
        if get_user.get('id') == product_delete.supplier_id or get_user.get('is_admin'):
            await db.execute(update(Product).where(Product.slug == product_slug).values(is_active=False))
            await db.commit()
            return {
                'status_code': status.HTTP_200_OK,
                'transaction': 'Удаление продукта прошло успешно'
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='У вас нет прав на использование этого метода'
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='У вас нет прав на использование этого метода'
        )
