from src.models.formation import Formation


def get_formation_by_url(url: str) -> Formation | None:
    return Formation.query.filter(Formation.url == url).first()
