from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.backend.db import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
