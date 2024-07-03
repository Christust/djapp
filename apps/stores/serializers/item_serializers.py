from rest_framework import serializers
from apps.stores.models import Item

# from apps.branches.serializers import ItemSerializer


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ["created_at", "modified_at", "deleted_at", "is_active"]


class ItemOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ["created_at", "modified_at", "deleted_at", "is_active"]
