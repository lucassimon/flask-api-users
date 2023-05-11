import factory

from apps.users.models import Admin, User


class AdminFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = Admin

    full_name = factory.Sequence(lambda n: "Admin %d" % n)
    email = factory.Sequence(lambda n: "admin-%d@gmail.com" % n)
    password = "123456"


class UserFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = User

    full_name = factory.Sequence(lambda n: "User %d" % n)
    email = factory.Sequence(lambda n: "admin-%d@gmail.com" % n)
    cpf_cnpj = factory.Sequence(lambda n: "cpf-%d" % n)
    date_of_birth = "2019-07-23"
    password = "123456"
