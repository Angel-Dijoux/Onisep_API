import strawberry

from src.business_logic.formation.get_formation_details import (
    FormationDetails,
    get_formation_details_by_id,
)
from src.business_logic.formation.scrap.get_main_formation import get_main_formations
from src.business_logic.formation.scrap.get_repartition_formations import (
    get_libelle_type_formation,
)
from src.business_logic.formation.scrap.types import Facet, FormationsWithTotal
from src.business_logic.formation.scrap.search_formation import (
    search_formations,
)


# TODO : Deprecated REST a migrate here for get_feed_formations and search_formations
@strawberry.type
class FormationResolver:
    get_formation_details_by_id: FormationDetails = (
        strawberry.field(resolver=get_formation_details_by_id),
    )
    get_libelle_type_formation: list[Facet] = strawberry.field(
        resolver=get_libelle_type_formation
    )
    search_formations: FormationsWithTotal = strawberry.field(
        resolver=search_formations
    )
    get_feed_formations: FormationsWithTotal = strawberry.field(
        resolver=get_main_formations
    )
