from rest_framework.serializers import ModelSerializer

from .models import Country


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ['name','num_of_students']