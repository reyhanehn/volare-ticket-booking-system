from rest_framework import serializers
from ..models import Vehicle, TransportType


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['vehicle_id', 'name', 'type', 'class_code', 'total_seats', 'layout']
        read_only_fields = ['vehicle_id']

    def validate_type(self, value):
        if value not in TransportType.values:
            raise serializers.ValidationError("Invalid vehicle type.")
        return value

    def validate_class_code(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("class_code must be between 1 and 5.")
        return value

    def validate_total_seats(self, value):
        if value <= 0:
            raise serializers.ValidationError("total_seats must be positive.")
        return value

    def create(self, validated_data):
        request = self.context['request']
        company = request.user.company
        return Vehicle.objects.create(company=company, **validated_data)
