from django.db import connection
from rest_framework import serializers

from ..models.service import Service


class ServiceCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)

    def validate_name(self, value):
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM companies_service WHERE LOWER(name) = LOWER(%s)", [value])
            if cursor.fetchone():
                raise serializers.ValidationError("Service with this name already exists.")
        return value

    def create(self, validated_data):
        name = validated_data['name']
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO companies_service (name) VALUES (%s) RETURNING service_id", [name])
            service_id = cursor.fetchone()[0]
        return Service(service_id=service_id, name=name)

class ServiceListSerializer(serializers.Serializer):
    service_id = serializers.IntegerField()
    name = serializers.CharField()

    @classmethod
    def fetch_all(cls):
        with connection.cursor() as cursor:
            cursor.execute("SELECT service_id, name FROM companies_service ORDER BY name ASC")
            rows = cursor.fetchall()
        return [cls({"service_id": sid, "name": name}) for sid, name in rows]