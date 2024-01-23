from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base


Model = declarative_base(name="Model")


class BaseModel(Model):
    __abstract__: bool = True
    __allow_unmapped__: bool = True

    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}
