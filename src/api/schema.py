from src.api.favoris.favori_resolver import FavorisResolver
from src.api.formation.formation_resolver import FormationResolver
import strawberry

from strawberry.tools import merge_types
from strawberry.extensions import QueryDepthLimiter
from strawberry.extensions import MaxTokensLimiter
from strawberry.extensions import MaxAliasesLimiter

types: tuple = (FormationResolver, FavorisResolver)

Queries = merge_types("Queries", types)

schema = strawberry.Schema(
    query=Queries,
    extensions=[
        QueryDepthLimiter(max_depth=10),
        MaxTokensLimiter(max_token_count=1000),
        MaxAliasesLimiter(max_alias_count=15),
    ],
)
# https://strawberry.rocks/docs/guides/tools
