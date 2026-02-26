from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, Date, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.backend.db import Base
from app.models import *


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    comment = Column(Text)
    grade = Column(Integer)
    comment_date = Column(Date, default=datetime.now())
    is_active = Column(Boolean, default=True)
