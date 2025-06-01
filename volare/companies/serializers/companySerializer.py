from rest_framework import serializers
from accounts.serializers.signupSerializer import AccountSignupSerializer
from ..models import Company


class CompanyCreateSerializer(serializers.ModelSerializer):
    owner_data = AccountSignupSerializer(write_only=True)

    class Meta:
        model = Company
        fields = ['name', 'logo_url', 'website', 'owner_data']

    def create(self, validated_data):
        owner_data = validated_data.pop('owner_data')

        # Force the role to 'Company_Owner' regardless of what's passed
        owner_data['role'] = 'Company_Owner'

        # Use existing signup logic to create the account and wallet
        owner_serializer = AccountSignupSerializer(data=owner_data)
        owner_serializer.is_valid(raise_exception=True)
        owner = owner_serializer.save()

        # Now create the company with the new owner
        company = Company.objects.create(owner=owner, **validated_data)
        return company

    def to_representation(self, instance):
        return {
            "company_id": instance.company_id,
            "name": instance.name,
            "owner_id": instance.owner.account_id,
            "website": instance.website,
            "logo_url": instance.logo_url
        }
