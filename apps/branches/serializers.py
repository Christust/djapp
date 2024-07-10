from rest_framework import serializers
from apps.branches.models import Branch, Country, State, City

# from apps.branches.serializers import BranchSerializer


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        exclude = ["created_at", "modified_at", "deleted_at", "is_active"]


class StateSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()

    class Meta:
        model = State
        exclude = ["created_at", "modified_at", "deleted_at", "is_active"]


class CitySerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField()

    class Meta:
        model = City
        exclude = ["created_at", "modified_at", "deleted_at", "is_active"]


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        exclude = ["created_at", "modified_at", "deleted_at", "is_active"]


class BranchOutSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    state = StateSerializer()
    city = CitySerializer()

    class Meta:
        model = Branch
        exclude = ["created_at", "modified_at", "deleted_at", "is_active"]
