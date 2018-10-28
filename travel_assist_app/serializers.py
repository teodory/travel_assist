from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from travel_assist_app.models import User, Country, Place, City, PlacesList

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(UserModel.objects.all())]
    )
    password = serializers.CharField(
        min_length=4,
        write_only=True
    )

    def create(self, validated_data):
        fields = ['username', 'password', 'email']
        # fields = ['username', 'first_name', 'last_name', 'password', 'email']
        data = {field: validated_data.get(field) for field in fields}
        print(data)
        return UserModel.objects.create_user(**data)

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'email', 'password')

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        # instance.password = validated_data.get('password', instance.password)
        instance.save()

        return instance


class CountrySerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        read_only=True,
    )

    class Meta:
        model = Country
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ['name']


class PlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Place
        fields = "__all__"


class PlacesListSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlacesList
        fields = "__all__"
