from dataclasses import dataclass

import strawberry

from src.models.formation import Formation


@strawberry.type
@dataclass
class Facet:
    key: str
    doc_count: int


@strawberry.type
@dataclass
class FormationIsFavorite:
    formation: Formation
    is_favorite: bool


@strawberry.type
@dataclass
class FormationsWithTotal:
    total: int
    formations: list[Formation | FormationIsFavorite]
