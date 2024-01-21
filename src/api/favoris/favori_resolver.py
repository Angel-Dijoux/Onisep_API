import strawberry

from src.business_logic.favoris.get_favoris import get_favoris_by_user_id
from src.business_logic.formation.scrap.types import FormationsWithTotal

# https://strawberry.rocks/docs/integrations/flask#options


@strawberry.type
class FavorisResolver:
    get_favoris_by_user_id: FormationsWithTotal = strawberry.field(
        resolver=get_favoris_by_user_id
    )
