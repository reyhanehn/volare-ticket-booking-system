# companies/serializers/companySerializer.py

from rest_framework import serializers
from accounts.serializers.signupSerializer import AccountSignupSerializer
from ..models import Company
from django.db import connection


class CompanyCreateSerializer(serializers.ModelSerializer):
    owner_data = AccountSignupSerializer(write_only=True)

    class Meta:
        model = Company
        fields = ['name', 'logo_url', 'website', 'owner_data']

    def create(self, validated_data):
        owner_data = validated_data.pop('owner_data')
        owner_data['role'] = 'Company_Owner'

        # Use AccountSignupSerializer which must use raw SQL internally
        owner_serializer = AccountSignupSerializer(data=owner_data)
        owner_serializer.is_valid(raise_exception=True)
        owner = owner_serializer.save()

        # Raw SQL insert for Company
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO companies_company (owner_id, name, logo_url, website)
                VALUES (%s, %s, %s, %s)
                RETURNING company_id
            """, [
                owner.account_id,
                validated_data.get('name'),
                validated_data.get('logo_url'),
                validated_data.get('website')
            ])
            company_id = cursor.fetchone()[0]

        # Return a fake instance for serialization
        return type("CompanyObj", (), {
            "company_id": company_id,
            "name": validated_data.get('name'),
            "owner": type("OwnerObj", (), {"account_id": owner.account_id}),
            "logo_url": validated_data.get('logo_url'),
            "website": validated_data.get('website')
        })

    def to_representation(self, instance):
        return {
            "company_id": instance.company_id,
            "name": instance.name,
            "owner_id": instance.owner.account_id,
            "website": instance.website,
            "logo_url": instance.logo_url
        }
