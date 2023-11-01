from dataclasses import dataclass

from src.models.formation import Formation


@dataclass
class Facet:
    key: str
    doc_count: int


@dataclass
class SearchedFormations:
    total: int
    formations: list[Formation]
