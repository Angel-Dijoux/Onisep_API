import strawberry
from strawberry.extensions import MaxAliasesLimiter, MaxTokensLimiter, QueryDepthLimiter


@strawberry.type
class Book:
    title: str
    author: str


@strawberry.type
class Query:
    books: list[Book]


schema = strawberry.Schema(
    query=Query,
    extensions=[
        QueryDepthLimiter(max_depth=10),
        MaxTokensLimiter(max_token_count=1000),
        MaxAliasesLimiter(max_alias_count=15),
    ],
)
# https://strawberry.rocks/docs/guides/tools
