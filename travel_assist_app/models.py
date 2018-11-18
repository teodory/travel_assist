from django.db import models
from django.contrib.auth.models import AbstractUser, AnonymousUser

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return "{0}".format(self.name)


class City(models.Model):
    name = models.CharField(max_length=50, null=False)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return "{0}, {1}".format(self.name, self.country)


class Place(models.Model):
    name = models.CharField(max_length=100, null=False)
    website = models.TextField()
    price = models.CharField(max_length=30)
    work_hours = models.CharField(max_length=30)
    location = models.CharField(max_length=50)
    city = models.ForeignKey(to=City, on_delete=models.CASCADE, null=False)
    description = models.TextField()

    def __str__(self):
        return "{0}".format(self.name)


# class User(models.Model):
# class User(AnonymousUser):
class User(AbstractUser):
    pass
    # places_list = models.ForeignKey(to=PlacesList, on_delete=models.CASCADE, null=True)

    # # def get_by_natural_key(self, username):
    # #     return self.get(**{self.model.USERNAME_FIELD: username})
    #
    # #     objects = models.Manager()
    # REQUIRED_FIELDS = ('first_name', 'last_name', 'password')
    # # USERNAME_FIELD = 'email'
    # # is_anonymous = False
    # # is_authenticated = True
    #
    # # objects = UserAccountManager()
    #
    # first_name = models.CharField(max_length=100, null=False)
    # last_name = models.CharField(max_length=100, null=False)
    # email = models.CharField(unique=True, max_length=60, null=False)
    # password = models.CharField(max_length=50, null=False)
    #
    # # def __str__(self):
    # #     return "{0} {1}".format(self.first_name, self.last_name)


class PlacesList(models.Model):
    name = models.CharField(max_length=30, primary_key=False, null=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    places = models.ManyToManyField(to=Place)

    # name = models.CharField(max_length=60)
    # id = models.PositiveIntegerField(unique=False, null=False)

    def __str__(self):
        return "{0} - {1} (2)".format(self.pk, self.name, self.places.name)


# class CustomUserAdmin(UserAdmin):
#     model = User
# admin.site.register(User, UserAdmin)
