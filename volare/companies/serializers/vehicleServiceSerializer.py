from rest_framework import serializers
from django.db import connection


class VehicleServiceAssignSerializer(serializers.Serializer):
    vehicle_id = serializers.IntegerField()
    service_names = serializers.ListField(
        child=serializers.CharField(), allow_empty=False
    )

    def validate_vehicle_id(self, value):
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM companies_vehicle WHERE vehicle_id = %s", [value])
            if not cursor.fetchone():
                raise serializers.ValidationError("Vehicle with this ID does not exist.")
        return value

    def validate_service_names(self, value):
        if not value:
            raise serializers.ValidationError("At least one service name must be provided.")

        placeholders = ','.join(['%s'] * len(value))
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT name, service_id FROM companies_service WHERE LOWER(name) IN ({placeholders})",
                [name.lower() for name in value]
            )
            rows = cursor.fetchall()

        name_to_id = {row[0].lower(): row[1] for row in rows}
        missing = [name for name in value if name.lower() not in name_to_id]

        if missing:
            raise serializers.ValidationError(f"Invalid service names: {missing}")

        # Store mapping for use in `create`
        self.service_id_list = list(name_to_id.values())
        return value

    def create(self, validated_data):
        vehicle_id = validated_data['vehicle_id']
        inserted = []

        with connection.cursor() as cursor:
            for service_id in self.service_id_list:
                try:
                    cursor.execute("""
                        INSERT INTO companies_vehicleservice (vehicle_id, service_id)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING
                    """, [vehicle_id, service_id])
                    inserted.append(service_id)
                except Exception:
                    continue  # Skip duplicates or DB errors

        return {
            "vehicle_id": vehicle_id,
            "assigned_services": inserted
        }
