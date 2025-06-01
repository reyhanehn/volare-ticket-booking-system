from rest_framework import serializers
from ..models import Station, Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['location_id', 'country', 'city']


class StationSerializer(serializers.ModelSerializer):
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    class Meta:
        model = Station
        fields = ['station_id', 'name', 'type', 'location']

    def validate_name(self, value):
        import re
        if not re.match(r'^[A-Za-z]+(\s[A-Za-z]+)*$', value):
            raise serializers.ValidationError("Station name must contain only letters and spaces.")
        return value