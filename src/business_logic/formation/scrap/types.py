from dataclasses import dataclass


@dataclass
class Facet:
    key: str
    doc_count: int


@dataclass
class Formation:
    type: str
    libelle: str
    url: str
    domain: str
    niveau_de_sortie: str


@dataclass
class SearchedFormations:
    total: int
    formations: list[Formation]
