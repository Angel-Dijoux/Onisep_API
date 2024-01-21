from dataclasses import dataclass

import strawberry

from src.models.formation import Formation


@dataclass
@strawberry.type
class Facet:
    key: str
    doc_count: int


@dataclass
@strawberry.type
class FormationIsFavorite:
    formation: Formation
    is_favorite: bool


@dataclass
@strawberry.type
class FormationsWithTotal:
    total: int
    formations: list[Formation | FormationIsFavorite]
