from dataclasses import dataclass


@dataclass
class Facet:
    key: str
    doc_count: int


@dataclass
class Formation:
    code_nsf: str
    type: str
    libelle: str
    tutelle: str
    url: str
    domain: str
    niveau_de_sortie: str
    duree: str


@dataclass
class SearchedFormations:
    total: int
    formations: list[Formation]
