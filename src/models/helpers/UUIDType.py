import uuid
from sqlalchemy.types import TypeDecorator, CHAR


class UUIDType(TypeDecorator):
    impl = CHAR(length=32)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return value.hex
        return None

    def process_literal_param(self, value, dialect):
        return value.hex

    def process_result_value(self, value, dialect):
        if value is not None:
            return uuid.UUID(value)
