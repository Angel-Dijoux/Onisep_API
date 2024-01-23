import strawberry
from strawberry.extensions import MaxAliasesLimiter, MaxTokensLimiter, QueryDepthLimiter

# from strawberry.tools import merge_types

from src.api.formation.formation_resolver import FormationResolver

# types: tuple = (FormationResolver, ...)
# Queries = merge_types("Queries", types)

schema = strawberry.Schema(
    query=FormationResolver,
    extensions=[
        QueryDepthLimiter(max_depth=10),
        MaxTokensLimiter(max_token_count=1000),
        MaxAliasesLimiter(max_alias_count=15),
    ],
)
# https://strawberry.rocks/docs/guides/tools
