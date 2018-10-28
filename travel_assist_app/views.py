
from django.db.models import Max
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.http.response import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from travel_assist_app.models import Country, City, PlacesList, Place
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *

from travel_assist_app.serializers import PlacesListSerializer
from .serializers import UserSerializer, CountrySerializer, CitySerializer, PlaceSerializer


UserModel = get_user_model()

# Create your views here.


def index(request):
    return HttpResponse('<h5> HOME PAGE <h5>')


def home(request):
    return HttpResponse('Hello Django!')


class ViewCountries(APIView):

    def get(self, request, format=None):
        countries_query = Country.objects.all()
        countries_serializer = CountrySerializer(countries_query, many=True)
        return Response(countries_serializer.data)


class ViewCities(APIView):

    def get(self, request, country, format=None):
        country = Country.objects.get(name=country)
        cities_query = City.objects.filter(country=country)
        cities_serializer = CitySerializer(cities_query, many=True)
        return Response(cities_serializer.data)


class ViewPlaces(APIView):

    def get(self, request, country, city):
        country = Country.objects.get(name=country)
        city = City.objects.get(name=city, country=country)
        places = Place.objects.filter(city=city)
        places_serializer = PlaceSerializer(places, many=True)

        return Response(places_serializer.data, HTTP_200_OK)


class ViewUserLists(LoginRequiredMixin, APIView):

    login_url = '/signup/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        user = UserModel.objects.get(username=request.user)
        places_list = PlacesList.objects.filter(user=user)
        places_list_serializer = PlacesListSerializer(places_list, many=True)
        return Response(places_list_serializer.data, HTTP_200_OK)

    def post(self, request):
        user = UserModel.objects.get(username=request.user)

        if 'list_id' in request.data:
            list_id = request.data['list_id']
        else:
            list_id = PlacesList.objects.all().aggregate(Max('list_id'))['list_id__max'] + 1

        if 'place_id' in request.data:
            place = Place.objects.get(id=request.data['place_id'])
            places_list = PlacesList.objects.get_or_create(list_id=list_id, user=user, places=place)

            if places_list[1]:
                return HttpResponseRedirect(redirect_to='user_list/{0}/'.format(list_id))
        return Response({"Place already in the list!"}, HTTP_400_BAD_REQUEST)


class ViewUserList(LoginRequiredMixin, APIView):
    login_url = '/signup/'
    redirect_field_name = 'redirect_to'

    def get(self, request, list_id):
        if list_id:
            user_places_list = PlacesList.objects.filter(list_id=list_id)
            places_list = [user_place.places for user_place in user_places_list]
            places = PlaceSerializer(places_list, many=True)
            return Response(places.data)

        return Response({}, HTTP_400_BAD_REQUEST)

    def post(self, request):
        # TODO place_id -> insert place
        pass

    def delete(self, request, list_id):
        places = PlacesList.objects.filter(list_id=list_id).delete()
        if places:
            return Response({}, HTTP_204_NO_CONTENT)
        return Response({}, HTTP_400_BAD_REQUEST)


class SignupUser(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            user = UserModel.objects.get(username=request.user)
            return Response({"Hello " + user.username})
        return Response({"Please login!"})

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

