from sqlalchemy import Column, Integer, String

from fastapi_skeleton.common.util.database import Base


class Example(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=100))
