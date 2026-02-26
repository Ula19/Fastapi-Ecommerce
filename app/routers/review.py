from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, func
from typing import Annotated

from app.models.review import Review
from app.models.products import Product
from app.backend.db_depends import get_db
from app.schemas import CreateReviewAndRating
from app.routers.permissions import get_current_user


router = APIRouter(prefix='/review', tags=['review'])



@router.get("/all_reviews")
async def get_all_reviews(db: Annotated[AsyncSession, Depends(get_db)]):
    """
    Метод получения всех отзывов
    """

    reviews = await db.scalars(select(Review).where(Review.is_active == True))
    return reviews.all()


@router.get("/products_reviews")
async def get_products_reviews(db: Annotated[AsyncSession, Depends(get_db)], product_id: int):
    """
    Метод получения отзывов и его рейтингов об определенном товаре
    """

    reviews = await db.scalars(select(Review).where(Review.product_id == product_id, Review.is_active == True))
    return reviews.all()


@router.post("/add_review")
async def add_review(db: Annotated[AsyncSession, Depends(get_db)],
                     current_user: Annotated[dict, Depends(get_current_user)],
                     product_id: int,
                     create_review_rating: CreateReviewAndRating,
                     get_user: Annotated[dict, Depends(get_current_user)]):
    """
    Метод добавления отзыва и рейтинга об определенном товаре.
    """
    if get_user.get("is_customer"):
        await db.execute(insert(Review).values(user_id=current_user.get("id"),
                                               product_id=product_id,
                                               comment=create_review_rating.comment,
                                               grade=create_review_rating.grade))

        avg_grade = await db.scalar(
            select(func.avg(Review.grade))
            .where(Review.product_id == product_id, Review.is_active == True)
        )

        await db.execute(update(Product).where(Product.id == product_id).values(rating=avg_grade))
        await db.commit()

        return {
            "status_code": status.HTTP_201_CREATED,
            "transaction": "Успешный"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='У вас нет прав на использование этого метода'
        )


@router.delete("/delete_reviews")
async def delete_reviews(db: Annotated[AsyncSession, Depends(get_db)],
                         get_user: Annotated[dict, Depends(get_current_user)],
                         review_id: int,
                         ):
    if get_user.get("is_admin"):
        rating_delete = await db.scalar(select(Review).where(Review.id == review_id))

        if rating_delete is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Отзыв не найден'
            )

        await db.execute(update(Review).where(Review.id == review_id).values(is_active=False))
        await db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Удаление отзыва прошло успешно'
        }

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='У вас нет прав на использование этого метода'
        )
