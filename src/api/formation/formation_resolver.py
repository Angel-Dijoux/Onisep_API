from src.business_logic.formation.get_formation_details import (
    FormationDetails,
    get_formation_by_id,
)
import strawberry


@strawberry.type
class FormationResolver:
    get_formation_by_id: FormationDetails = strawberry.field(
        resolver=get_formation_by_id
    )
