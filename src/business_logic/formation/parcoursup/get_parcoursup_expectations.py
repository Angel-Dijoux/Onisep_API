from typing import Optional
from src.business_logic.formation.parcoursup.helper.html_parser import (
    HtmlParser,
    ParcourSupExpectations,
)


def get_parcoursup_expectations(
    expectations: Optional[str],
) -> Optional[ParcourSupExpectations]:
    if expectations:
        return HtmlParser(expectations).parse_html()
