# vehicles/serializers/vehicleSerializer.py

from rest_framework import serializers
from ..models import Vehicle, TransportType
from django.db import connection


class VehicleSerializer(serializers.ModelSerializer):
    sections = serializers.ListField(
        child=serializers.DictField(), required=False, write_only=True
    )

    class Meta:
        model = Vehicle
        fields = ['vehicle_id', 'name', 'type', 'class_code', 'total_seats', 'layout', 'sections']
        read_only_fields = ['vehicle_id']

    def validate_class_code(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("class_code must be between 1 and 5.")
        return value

    def validate_total_seats(self, value):
        if value <= 0:
            raise serializers.ValidationError("total_seats must be positive.")
        return value

    def validate(self, data):
        type_ = data.get("type")
        layout = data.get("layout")
        total_seats = data.get("total_seats")
        sections = data.get("sections", [])

        if type_ == TransportType.AIRPLANE:
            if layout not in ['1', '2', '3']:
                raise serializers.ValidationError("Layout for airplane must be 1, 2, or 3.")
            if not sections:
                raise serializers.ValidationError("Sections data is required for airplane.")

            expected_sections_count = int(layout)
            if len(sections) != expected_sections_count:
                raise serializers.ValidationError(
                    f"Layout {layout} requires {expected_sections_count} sections, but {len(sections)} were provided."
                )

            seat_sum = sum([s.get("seats_count", 0) for s in sections])
            if seat_sum != total_seats:
                raise serializers.ValidationError("Sum of section seats must equal total_seats.")


        elif type_ == TransportType.TRAIN:
            try:
                layout_int = int(layout)
            except ValueError:
                raise serializers.ValidationError("Layout must be an integer (number of cabins).")
            if layout_int <= 0:
                raise serializers.ValidationError("Cabin count must be positive.")
            if total_seats % layout_int != 0:
                raise serializers.ValidationError("total_seats must be divisible by number of cabins.")
            if total_seats % 4 != 0 and total_seats % 6 != 0:
                raise serializers.ValidationError("total_seats must be divisible by 4 or 6 for train.")

        elif type_ == TransportType.BUS:
            if '-' not in layout:
                raise serializers.ValidationError("Layout for bus must be like '1-2' or '2-2'.")
            parts = layout.split('-')
            if len(parts) != 2 or not all(p.isdigit() for p in parts):
                raise serializers.ValidationError("Bus layout should be digits like '1-2'")
            if total_seats % 3 != 0:
                raise serializers.ValidationError("total_seats must be divisible by 3 for buses.")

        return data

    def create(self, validated_data):
        sections_data = validated_data.pop('sections', [])
        request = self.context['request']
        user_id = request.user.account_id  # FIX: use correct primary key

        # Step 1: Get company_id using raw SQL
        with connection.cursor() as cursor:
            cursor.execute("SELECT company_id FROM companies_company WHERE owner_id = %s", [user_id])
            result = cursor.fetchone()
            if not result:
                raise serializers.ValidationError("No company found for this user.")
            company_id = result[0]

        # Step 2: Insert into Vehicle table
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO companies_vehicle (company_id, name, type, class_code, total_seats, layout)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING vehicle_id
            """, [
                company_id,
                validated_data.get('name'),
                validated_data['type'],
                validated_data['class_code'],
                validated_data['total_seats'],
                validated_data['layout']
            ])
            vehicle_id = cursor.fetchone()[0]

            # Step 3: Create vehicle sections
            type_ = validated_data['type']
            layout = validated_data['layout']
            total_seats = validated_data['total_seats']

            if type_ == TransportType.AIRPLANE:
                for section in sections_data:
                    cursor.execute("""
                        INSERT INTO companies_vehiclesection (vehicle_id, name, seats_count)
                        VALUES (%s, %s, %s)
                    """, [vehicle_id, section.get('name'), section.get('seats_count')])

            elif type_ == TransportType.TRAIN:
                num_cabins = int(layout)
                seats_per_cabin = total_seats // num_cabins
                for i in range(num_cabins):
                    cursor.execute("""
                        INSERT INTO companies_vehiclesection (vehicle_id, name, seats_count)
                        VALUES (%s, %s, %s)
                    """, [vehicle_id, f"Cabin {i+1}", seats_per_cabin])

            elif type_ == TransportType.BUS:
                left, right = map(int, layout.split('-'))
                if left == right:
                    # Single section (e.g., 2-2)
                    cursor.execute("""
                        INSERT INTO companies_vehiclesection (vehicle_id, name, seats_count)
                        VALUES (%s, %s, %s)
                    """, [vehicle_id, "Standard", total_seats])
                else:
                    # Two sections (e.g., 1-2 layout → 1/3 and 2/3)
                    one_third = total_seats // 3
                    cursor.execute("""
                        INSERT INTO companies_vehiclesection (vehicle_id, name, seats_count)
                        VALUES (%s, %s, %s)
                    """, [vehicle_id, "Single Seat Side", one_third])
                    cursor.execute("""
                        INSERT INTO companies_vehiclesection (vehicle_id, name, seats_count)
                        VALUES (%s, %s, %s)
                    """, [vehicle_id, "Double Seat Side", total_seats - one_third])

        # Return dummy vehicle object
        return Vehicle(vehicle_id=vehicle_id, company_id=company_id, **validated_data)
