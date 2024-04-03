import factory
from src import models


class UserFactory(factory.Factory):
    class Meta:
        model = models.User

    username = factory.Faker("uuid4")
    email = factory.Faker("uuid4")
    password = factory.Faker("uuid4")


class FormationFactory(factory.Factory):
    class Meta:
        model = models.Formation

    code_nsf = 334
    type = "baccalauréat technologique"
    libelle = (
        "bac techno STHR Sciences et technologies de l'hôtellerie et de la restauration"
    )
    tutelle = "Ministère chargé de l'Éducation nationale et de la Jeunesse"
    url = factory.Faker("uuid4")
    domain = "hôtellerie-restauration, tourisme/hôtellerie | hôtellerie-restauration, tourisme/restauration"
    niveau_de_sortie = "Bac ou équivalent"
    duree = "1 an"


class UserFavorisFactory(factory.Factory):
    class Meta:
        model = models.UserFavori

    formation = factory.SubFactory(FormationFactory)
    users = factory.SubFactory(UserFactory)
