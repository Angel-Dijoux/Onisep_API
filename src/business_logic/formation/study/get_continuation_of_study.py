from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ContinuationOfStudies:
    title: str = ""
    formations: list[str] = field(default_factory=list)


def process_continuation_studies(
    continuations: dict,
) -> Optional[ContinuationOfStudies]:
    if continuations:
        formations = list(
            continuations["poursuite_etudes"]["formation_poursuite_Etudes"]
        )
        return ContinuationOfStudies(
            title=continuations["poursuite_etudes"]["type_Poursuite"],
            formations=formations,
        )
