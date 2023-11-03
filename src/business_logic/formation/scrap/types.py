from dataclasses import dataclass

from src.models.formation import Formation


@dataclass
class Facet:
    key: str
    doc_count: int


@dataclass
class FormationIsFavortite:
    formation: Formation
    is_favorite: bool


@dataclass
class FormationsWithTotal:
    total: int
    formations: list[Formation | FormationIsFavortite]
