from src import db
from sqlalchemy import func


class BaseModel(db.Model):
    __abstract__: bool = True
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}
