from rest_framework import serializers
from ..models.passenger import Passenger
import re


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ['country', 'city']

    def validate_country(self, value):
        if not re.match(r'^[A-Za-z]+(\s[A-Za-z]+)*$', value):
            raise serializers.ValidationError("Country name must contain only letters and spaces.")
        return value

    def validate_city(self, value):
        if not re.match(r'^[A-Za-z]+(\s[A-Za-z]+)*$', value):
            raise serializers.ValidationError("City name must contain only letters and spaces.")
        return value

    def validate(self, data):
        if Passenger.objects.filter(country=data['country'], city=data['city']).exists():
            raise serializers.ValidationError("This location already exists.")
        return data
