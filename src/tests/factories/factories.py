import factory
from src import models


class UserFactory(factory.Factory):
    class Meta:
        model = models.User

    username = factory.Faker("uuidv4")
    email = factory.Faker("uuidv4")


class UserFavorisFactory(factory.Factory):
    class Meta:
        model = models.UserFavori


class FormationFactory(factory.Factory):
    class Meta:
        model = models.Formation

    code_nsf = 334
    type = "baccalauréat technologique"
    libelle = (
        "bac techno STHR Sciences et technologies de l'hôtellerie et de la restauration"
    )
    tutelle = "Ministère chargé de l'Éducation nationale et de la Jeunesse"
    url = "http://www.onisep.fr/http/redirection/formation/slug/FOR.494"
    domain = "hôtellerie-restauration, tourisme/hôtellerie | hôtellerie-restauration, tourisme/restauration"
    niveau_de_sortie = "Bac ou équivalent"
    duree = "1 an"
