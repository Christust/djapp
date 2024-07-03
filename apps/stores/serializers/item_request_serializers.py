from rest_framework import serializers
from apps.stores.models import ItemRequest

# from apps.branches.serializers import ItemRequestSerializer

class ItemRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemRequest
        exclude = ["created_at", "modified_at", "deleted_at", "is_active"]


class ItemRequestOutSerializer(serializers.ModelSerializer):
    item = serializers.StringRelatedField()
    material_request = serializers.StringRelatedField()

    class Meta:
        model = ItemRequest
        exclude = ["created_at", "modified_at", "deleted_at", "is_active"]
